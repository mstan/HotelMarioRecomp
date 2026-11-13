#!/usr/bin/env python3
"""Generate and build Hotel Mario using its pinned engine; never opens dialogs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
JOBS = ("video", "loader", "drawing", "memory", "service", "streaming", "board", "gpu")


def run(*args, cwd=ROOT):
    subprocess.run([str(arg) for arg in args], cwd=cwd, check=True)


def saved_asset(value, name):
    config = ROOT / f"{name}.cfg"
    if not value and config.is_file():
        value = config.read_text(encoding="utf-8-sig").strip()
    if not value:
        raise ValueError(f"Supply --{name} <path> or a local {name}.cfg")
    return Path(value).expanduser().resolve(strict=True)


def digest(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def disc_binary(path):
    if path.suffix.lower() == ".bin":
        return path
    files = re.findall(r'^\s*FILE\s+"([^"]+)"\s+BINARY\s*$',
                       path.read_text(encoding="utf-8-sig"), re.M | re.I)
    if len(files) != 1:
        raise ValueError("Hotel Mario requires a single-track raw Mode-2 CUE/BIN")
    return (path.parent / files[0]).resolve(strict=True)


def executable(build, name):
    suffix = ".exe" if os.name == "nt" else ""
    for path in (build / (name + suffix), build / "Release" / (name + suffix)):
        if path.is_file():
            return path
    raise ValueError(f"Missing built tool: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bios")
    parser.add_argument("--disc")
    parser.add_argument("--engine", type=Path, default=Path(os.environ.get("CDIRECOMP_ROOT", ROOT / "cdirecomp")))
    parser.add_argument("--ui", type=Path, default=Path(os.environ.get("RECOMP_UI_ROOT", ROOT / "recomp-ui")))
    parser.add_argument("--build-dir", type=Path, default=ROOT / "build")
    parser.add_argument("--generated-dir", type=Path, default=ROOT / "generated")
    parser.add_argument("--cmake", default=shutil.which("cmake"))
    parser.add_argument("--generator", default="Ninja")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--module-seeds", type=Path)
    parser.add_argument("--static-module-entries", action="store_true")
    parser.add_argument("--reference", action="store_true", help="Build all faithful LLE implementations")
    for job in JOBS:
        parser.add_argument(f"--{job}-backend", choices=("HLE", "LLE"))
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    if not args.cmake or not 1 <= args.jobs <= 64:
        parser.error("CMake is required; --jobs must be 1..64")
    engine = args.engine.resolve(strict=True)
    if not (engine / "cmake/CdiGame.cmake").is_file():
        parser.error("Initialize the engine: git submodule update --init --recursive")
    bios, disc = saved_asset(args.bios, "bios"), saved_asset(args.disc, "disc")
    manifest = tomllib.loads((ROOT / "game.toml").read_text(encoding="utf-8"))
    binary = disc_binary(disc)
    for path, name in ((bios, "bios"), (binary, "disc")):
        if path.stat().st_size != manifest["assets"][f"{name}_size"] or digest(path, "sha1") != manifest["assets"][f"{name}_sha1"]:
            raise ValueError(f"{name} does not match the supported image in DISC.md")
    build, generated = args.build_dir.resolve(), args.generated_dir.resolve()
    tools = build / "tools"
    run(args.cmake, "-S", engine / "recompiler", "-B", tools, "-G", args.generator,
        "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_TESTING=OFF")
    run(args.cmake, "--build", tools, "--config", "Release", "--target", "CdiRecomp", "CdiRecompBios", "--parallel", args.jobs)
    compiler, bios_compiler = executable(tools, "CdiRecomp"), executable(tools, "CdiRecompBios")
    seeds = args.module_seeds or ROOT / manifest["recompiler"]["module_seeds"]
    if args.static_module_entries and args.module_seeds:
        parser.error("Choose --module-seeds or --static-module-entries")
    signature = {"bios": digest(bios), "disc": digest(binary),
                 "compiler": digest(compiler), "bios_compiler": digest(bios_compiler),
                 "bios_seeds": digest(engine / "bios/cdrtos_discovered.txt"),
                 "module_seeds": None if args.static_module_entries else digest(seeds),
                 "subr_exports": manifest["recompiler"]["subr_exports"], "game": manifest["game"]}
    stamp = generated / "inputs.json"
    required = (generated / "bios/bios_identity.h", generated / "bios/cdrtos_full.c",
                generated / "bios/cdrtos_dispatch.c", generated / "modules/module_manifest.c",
                generated / "modules/module_sources.cmake", generated / "modules/game_identity.h")
    previous = json.loads(stamp.read_text()) if stamp.is_file() else None
    if args.regenerate or previous != signature or not all(path.is_file() for path in required):
        generated.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="hotel-generation-", dir=generated.parent) as directory:
            staging = Path(directory)
            for name in ("bios", "modules"):
                (staging / name).mkdir()
            run(bios_compiler, bios, "--emit", "--out", staging / "bios", "--seeds", engine / "bios/cdrtos_discovered.txt")
            command = [compiler, disc, "--emit", "--out", staging / "modules",
                       "--subr-exports", manifest["recompiler"]["subr_exports"]]
            if not args.static_module_entries:
                command += ["--module-seeds", seeds.resolve(strict=True)]
            run(*command)
            identity = ",".join(f"0x{byte:02x}" for byte in bytes.fromhex(signature["disc"]))
            (staging / "modules/game_identity.h").write_text(
                "#pragma once\n#include <stdint.h>\n#define HOTELMARIO_GAME_NAME " + json.dumps(manifest["game"]["name"]) + "\n#define HOTELMARIO_GAME_REGION " + json.dumps(manifest["game"]["region"]) + "\nstatic const uint8_t hotelmario_disc_sha256[32] = {" + identity + "};\n",
                encoding="utf-8")
            # Preserve unchanged translation-unit timestamps across tool updates.
            for name in ("bios", "modules"):
                (generated / name).mkdir(parents=True, exist_ok=True)
                for source in (staging / name).iterdir():
                    destination = generated / name / source.name
                    if not destination.is_file() or destination.read_bytes() != source.read_bytes():
                        shutil.copyfile(source, destination)
        stamp.write_text(json.dumps(signature, indent=2) + "\n", encoding="utf-8")
    options = [f"-DCDIRECOMP_ROOT={engine}", f"-DCDI_BIOS_GENERATED_DIR={generated / 'bios'}",
               f"-DCDI_GAME_GENERATED_DIR={generated / 'modules'}", f"-DRECOMP_UI_ROOT={args.ui.resolve()}"]
    for job in JOBS:
        backend = getattr(args, f"{job}_backend") or ("LLE" if args.reference else "HLE")
        options.append(f"-DCDI_{job.upper()}_BACKEND={backend}")
    run(args.cmake, "-S", ROOT, "-B", build, "-G", args.generator,
        "-DCMAKE_BUILD_TYPE=Release", "-DCDI_COSIM_BUILD=OFF", *options)
    run(args.cmake, "--build", build, "--config", "Release", "--parallel", args.jobs)
    runtime=executable(build, "HotelMarioRecomp")
    for directory in (ROOT,runtime.parent):
        for name,path in (("bios",bios),("disc",disc)):
            sidecar=directory/f"{name}.cfg"
            if not sidecar.exists():
                sidecar.write_text(str(path)+"\n",encoding="utf-8")
    print(f"Built {runtime}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"ERROR: {error}")
