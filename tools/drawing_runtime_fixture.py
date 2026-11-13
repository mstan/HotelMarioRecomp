"""Compare the production drawing job with actual generated Hotel Mario code.

Provide a supported built consumer, BIOS, and the two RAM banks retained by
loader_job_compare.py at its deterministic gameplay endpoint. The fixture uses
isolated RAM copies and never changes a running game or persistent save.
"""
import engine_tools
import argparse,hashlib,json,os,pathlib,shutil,subprocess,shlex
from build_provenance import verify

def build_fixture(build,output,test_source=None,wraps=(),wrap_vblank=True):
    repo=engine_tools.ENGINE
    windows=os.name=='nt'
    cache={}
    for line in (build/'CMakeCache.txt').read_text(encoding='utf-8').splitlines():
        if '=' in line and ':' in line.split('=',1)[0]:
            key,value=line.split('=',1);cache[key.split(':',1)[0]]=value
    compiler=pathlib.Path(cache['CMAKE_C_COMPILER'])
    linker=pathlib.Path(cache['CMAKE_CXX_COMPILER'])
    extension='.exe' if windows else ''
    objcopy=next((path for name in ('llvm-objcopy','objcopy')
                  if (path:=compiler.with_name(name+extension)).is_file()),None)
    if objcopy is None:
        objcopy=shutil.which('llvm-objcopy') or shutil.which('objcopy')
    if objcopy is None:raise RuntimeError('objcopy or llvm-objcopy is required')
    suffix='.obj' if windows else '.o'
    object_root=build/'cdirecomp-runtime/CMakeFiles/HotelMarioRecomp.dir'
    if not object_root.is_dir():object_root=build/'CMakeFiles/HotelMarioRecomp.dir'
    objects=sorted(object_root.rglob('*'+suffix));main_obj=next(x for x in objects if x.name=='main.c'+suffix)
    objects.remove(main_obj);renamed=output/('product-main'+suffix)
    subprocess.run([str(objcopy),'--redefine-sym','main=cdi_product_main',str(main_obj),str(renamed)],check=True)
    name=pathlib.Path(test_source).stem if test_source else 'DrawingRuntimeTest'
    exe=output/(name+('.exe' if windows else ''))
    runtime=build/('HotelMarioRecomp.exe' if windows else 'HotelMarioRecomp')
    provenance=verify(runtime)
    test_object=output/('fixture-test'+suffix)
    subprocess.run([str(compiler),'-std=c11','-O2','-I'+str(repo/'runner/include'),
                    '-I'+str(repo/'common'),'-c',str(test_source or repo/'runner/tests/cdi_drawing_runtime_test.c'),
                    '-o',str(test_object)],check=True)
    lines=(build/'build.ninja').read_text(encoding='utf-8').splitlines()
    start=next(i for i,line in enumerate(lines) if line.startswith('build '+runtime.name+':'))
    libraries=next(line.split('=',1)[1].strip() for line in lines[start+1:] if line.startswith('  LINK_LIBRARIES ='))
    libraries=shlex.split(libraries.replace('$ ', ' ').replace('$:', ':'))
    args=[str(test_object),*[str(x) for x in objects],str(renamed),*libraries,
          *(['-Wl,--wrap=glue_check_vblank'] if wrap_vblank else []),*['-Wl,--wrap='+name for name in wraps],'-o',str(exe)]
    rsp=output/'link.rsp'
    rsp.write_text('\n'.join('"'+x.replace('\\','/')+'"' for x in args),encoding='utf-8')
    subprocess.run([str(linker),'@'+str(rsp.resolve())],check=True,cwd=build)
    if windows:shutil.copy2(build/'SDL2.dll',output/'SDL2.dll')
    return exe,runtime,provenance

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('build','rom','ram0','ram1'):p.add_argument(name,type=pathlib.Path)
    p.add_argument('--output',type=pathlib.Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    exe,runtime,provenance=build_fixture(a.build,a.output)
    cases=[];frontiers={}
    def run_case(budget,queued,variant=0,irq=0,seed=0x91234,wrap=0):
        number=len(cases);states={}
        for mode in ('reference','native'):
            output=a.output/f'{number:03d}-{mode}.json'
            cmd=[str(exe),str(a.rom.resolve()),str(a.ram0.resolve()),str(a.ram1.resolve()),str(output),
                 mode,str(budget),str(queued),str(variant),str(irq),str(seed),str(wrap)]
            result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
            (a.output/f'{number:03d}-{mode}.stderr').write_bytes(result.stderr)
            if result.returncode:raise RuntimeError((cmd,result.returncode,result.stderr.decode(errors='replace')[-2000:]))
            states[mode]=json.loads(output.read_text())
        reference=states['reference'];native=states['native']
        points=reference.pop('reference_frontiers');native.pop('reference_frontiers')
        jobs=native.pop('jobs');reference.pop('jobs')
        differences=[key for key in reference if reference[key]!=native[key]]
        row={'case':number,'budget':budget,'queued':queued,'variant':variant,'irq_cycle':irq,
             'seed':seed,'wrap':wrap,'native_jobs':jobs,'differences':differences}
        cases.append(row);(a.output/'results.json').write_bytes((json.dumps(cases,indent=2)+'\n').encode())
        if differences:raise RuntimeError(row)
        assert jobs['jobs']==0 if budget==1025 else jobs['jobs']>0,row
        if not irq:
            if variant==1 and budget>0 and queued:assert native['painted'],row
            for point in points:frontiers.setdefault((variant,point['pc']),point['after_cycles'])
    for n in (0,1,2,8,16,-1,1025):run_case(n,0)
    for count in (1,3,15):
        for wrap in (0,1):run_case(8,count,wrap=wrap)
    for variant in (1,2,3,4,5):run_case(8,1,variant=variant,wrap=1)
    run_case(8,0,variant=6)
    run_case(8,3,variant=6,wrap=1)
    timed=sorted({cycle for (variant,pc),cycle in frontiers.items() if variant in (0,1) and cycle>0})
    # IRQ targets come from actual original operations, including callbacks and
    # wrapping. The native implementation never defines its own passing oracle.
    for cycle in timed:run_case(8,1,variant=1,irq=cycle,seed=1,wrap=1)
    summary={'status':'pass','cases':cases,'timed_reference_cycles':timed,'provenance':provenance,
        'binary_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),
        'production_binary_sha256':hashlib.sha256(runtime.read_bytes()).hexdigest(),
        'fixtures':{name:{'path':str(path.resolve()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                    for name,path in [('rom',a.rom),('ram0',a.ram0),('ram1',a.ram1)]},
        'notes':'Actual generated reference and production native objects; full RAM/register/physical-clock/IRQ/fault/redirect equality; real bitmap callback must paint.'}
    (a.output/'summary.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode())
    print(f'Drawing job: {len(cases)} production/reference cases PASS')
if __name__=='__main__':main()
