"""Reuse built production objects to compare native loader jobs with real firmware."""
import engine_tools
import argparse,hashlib,json,pathlib,shutil,subprocess

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('build',type=pathlib.Path);p.add_argument('rom',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    root=engine_tools.ENGINE;a.output.mkdir(parents=True,exist_ok=False)
    from drawing_runtime_fixture import build_fixture
    exe,runtime,_=build_fixture(a.build,a.output,root/'runner/tests/cdi_loader_runtime_test.c',wrap_vblank=False)
    cases=[]
    # Every instruction frontier in the native fold, including both parity
    # branches and the pre-mutation timing of the register-count shift.
    cycles=[37,15,7,7,7,7,7,7,7,7,15,7,28,7,7,14,22,7,7,82,7,7,7,37,7,7,22,21,13,7]
    cumulative=[];n=0
    for c in cycles:n+=c;cumulative.append(n)
    settings=[(1,0,s,0) for s in (1,0xD9832,0xCE1212,0x12345678)]
    settings += [(n,0,0x21268070,0) for n in (2,17,255,256,257,513,1024)]
    settings += [(17,t,s,0) for s in (1,0xD9832) for t in cumulative]
    settings += [(17,0,0x91234,v) for v in (1,2,3)]
    for i,(words,irq,seed,variant) in enumerate(settings):
        states={}
        for mode in ('reference','native'):
            out=a.output/f'{i:03d}-{mode}.json';subprocess.run([str(exe),str(a.rom.resolve()),str(out),mode,str(words),str(irq),str(seed),str(variant)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            states[mode]=json.loads(out.read_text())
        jobs=states['native'].pop('jobs');states['reference'].pop('jobs')
        differences=[k for k in states['reference'] if states['reference'][k]!=states['native'][k]]
        result={'case':i,'words':words,'irq_cycle':irq,'seed':seed,'variant':variant,'native_jobs':jobs,'differences':differences};cases.append(result)
        (a.output/'results.json').write_text(json.dumps(cases,indent=2))
        if differences:raise RuntimeError(result)
        if variant:assert jobs['spans']==0,result
        else:assert jobs['spans']>0,result
    metadata={'status':'pass','cases':cases,'binary_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'rom_sha256':hashlib.sha256(a.rom.read_bytes()).hexdigest(),'production_binary_sha256':hashlib.sha256(runtime.read_bytes()).hexdigest(),'notes':'Actual generated firmware versus production native job; reference selected by instruction-observation mode. Source/objects are from the supported built runtime; no generated C was edited.'}
    (a.output/'summary.json').write_text(json.dumps(metadata,indent=2));print(f'Loader runtime differential: {len(cases)} cases PASS')
if __name__=='__main__':main()
