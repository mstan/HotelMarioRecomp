"""Exercise the production SDL input path in a dummy-driver test process."""
import argparse
import os
from pathlib import Path
import subprocess
import engine_tools
from drawing_runtime_fixture import build_fixture

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build',type=Path)
    parser.add_argument('--sdl-include',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    executable,_,_=build_fixture(args.build.resolve(),args.output.resolve(),
        engine_tools.ENGINE/'runner/tests/cdi_frontend_input_test.c',
        wrap_vblank=False,includes=(args.sdl_include.resolve(),))
    environment={**os.environ,'SDL_VIDEODRIVER':'dummy','SDL_AUDIODRIVER':'dummy',
                 'SDL_RENDER_DRIVER':'software'}
    for arguments in ([],['--original'],['--disabled']):
        subprocess.run([str(executable),*arguments],check=True,env=environment,timeout=20)

if __name__=='__main__':main()
