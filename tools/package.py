#!/usr/bin/env python3
"""Audit and package the player and shared launcher assets for Windows/Linux."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version",default=(ROOT/"VERSION").read_text().strip())
    parser.add_argument("--build",type=Path,default=ROOT/"build")
    parser.add_argument("--engine",type=Path,default=ROOT/"cdirecomp")
    parser.add_argument("--ui",type=Path,default=ROOT/"recomp-ui")
    parser.add_argument("--output",type=Path)
    parser.add_argument("--dll-dir",type=Path,action="append",default=[])
    args=parser.parse_args()
    build=args.build.resolve(strict=True)
    if sys.platform not in {"win32","linux"}:parser.error("Packaging currently supports Windows and Linux")
    windows=os.name=="nt"
    runtime=build/("HotelMarioRecomp.exe" if windows else "HotelMarioRecomp")
    if not runtime.is_file():runtime=build/"Release/HotelMarioRecomp.exe"
    suffix="windows-x64.zip" if windows else "linux-x86_64.AppImage"
    output=args.output or ROOT/"dist"/f"HotelMarioRecomp-{args.version}-{suffix}"
    with tempfile.TemporaryDirectory(prefix="hotel-licenses-",dir=build) as directory:
        licenses=Path(directory)
        for source,name in ((args.ui/"LICENSE","recomp-ui.txt"),
                            (args.ui/"src/third_party/imgui/LICENSE.txt","imgui.txt"),
                            (args.ui/"assets/common/fonts/NOTICE.md","launcher-fonts.md"),
                            (args.ui/"assets/common/img/NOTICE.md","launcher-images.md")):
            shutil.copyfile(source,licenses/name)
        for source in (ROOT/"LICENSES").glob("*"):
            shutil.copyfile(source,licenses/source.name)
        for source_root,name in ((ROOT,"HotelMarioRecomp"),(args.engine,"cdirecomp")):
            shutil.copyfile(source_root/"LICENSE",licenses/(name+".txt"))
            if (source_root/"PERMISSIONS.md").is_file():
                shutil.copyfile(source_root/"PERMISSIONS.md",licenses/(name+"-PERMISSIONS.md"))
        script="package_runtime_release.py" if windows else "package_runtime_appimage.py"
        command=[sys.executable,str(args.engine/"tools"/script),
                 "--product","HotelMarioRecomp","--version",args.version,
                 "--runtime",str(runtime),"--config",str(args.engine/"player.cfg.example"),
                 "--readme",str(ROOT/"RUNTIME-README.md"),
                 "--notices",str(ROOT/"THIRD-PARTY-NOTICES.md"),
                 "--assets",str(runtime.parent/"assets"),"--asset-manifest",str(build/"launcher-assets.txt"),
                 "--licenses",str(licenses),"--out",str(output)]
        if windows:
            command += ["--executable","HotelMarioRecomp.exe","--target","HotelMarioRecomp",
                        "--sdl",str(runtime.parent/"SDL2.dll")]
            cache=(build/"CMakeCache.txt").read_text(encoding="utf-8")
            compiler=re.search(r"^CMAKE_C_COMPILER:(?:FILEPATH|STRING)=(.+)$",cache,re.M)
            directories=args.dll_dir+([Path(compiler[1]).parent] if compiler else [])
            for path in directories:command += ["--dll-dir",str(path)]
        else:
            command += ["--apprun",str(ROOT/"packaging/linux/AppRun")]
        subprocess.run(command,check=True)
    return 0

if __name__=="__main__":raise SystemExit(main())
