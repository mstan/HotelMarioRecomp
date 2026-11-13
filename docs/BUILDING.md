# Building and packaging

Initialize `git submodule update --init --recursive`. Both the engine and shared launcher are real Git pins. Supply the exact BIOS and USA disc identities in DISC.md. Inputs stay private and are never copied into the executable.

## One build pipeline

```sh
python3 tools/build.py --bios /path/to/cdi490a.rom --disc /path/to/game.cue --jobs 2
```

Windows: `tools/build.ps1 -Bios <rom> -Disc <cue> -Jobs 2`. Linux: `sh tools/build-linux.sh --bios <rom> --disc <cue>`. The Windows wrapper also accepts the existing backend switches.

The driver builds the two pinned compiler tools under the selected build directory, verifies media identities and generates `generated/bios` and `generated/modules`. The game owns the observed entry catalog in `seeds/module-entries.txt`. Generation is staged and only changed output files replace existing outputs, avoiding a full guest-code rebuild when a compiler update emits identical C.

`--build-dir` and `--generated-dir` select explicit output locations. `--engine` and `--ui` are deliberate developer overrides; ordinary builds use the pinned root submodules. `--module-seeds` selects an observed catalog, and `--static-module-entries` omits observed entries. `--regenerate` repeats generation. No command opens an asset picker during automated builds.

`--reference` selects all LLE implementations. Individual `--video-backend`, `--loader-backend`, `--drawing-backend`, `--memory-backend`, `--service-backend`, `--streaming-backend`, `--board-backend` and `--gpu-backend` choices override that selection. Default builds retain the qualified HLE implementations.

## Checks

```sh
cmake -S . -B build/project-checks -DHOTELMARIO_BUILD_PLAYER=OFF
ctest --test-dir build/project-checks --output-on-failure
```

Engine component checks run from `cdirecomp/` without game assets. A built player also registers the engine's component tests. Game-specific TCP scenarios and acceptance tools live under tools/. Use isolated preferences/saves and dummy audio for unattended runs.

## Runtime packages

On Windows, `python tools/package.py --build build` creates the current-version ZIP in dist/. On Linux, `python3 tools/package.py --build build-linux` creates an AppImage using the pinned engine packaging tools. Windows also provides tools/package.ps1; Linux provides tools/package_appimage.sh.

The package audits the named target's source graph, link-time provenance, required dependencies and exact CD-i launcher asset manifest. Original firmware/discs, compilers, development tools and state/provenance sidecars are excluded. Source/build caches remain outside delivery folders. Keep only one verified current build per game in delivery folders, preserving saves and settings.
