# HotelMarioRecomp

Hotel Mario (USA) running as a native CD-i player build on the sibling
[`cdirecomp`](https://github.com/mstan/cdirecomp) clean-room runtime.

## Status

Early preview: the real CD-RTOS BIOS boots, the player shell opens the disc,
the Philips Interactive Media bumper plays with decoded XA audio, and Hotel
Mario reaches and runs its attract sequence. The Fantasy Factory title card is
pixel-exact against the regression capture, later animated scenes advance, and
the verified path has zero native dispatch misses and zero dropped audio
frames. Gameplay and a full playthrough are not yet certified.

This repository contains only game-specific build glue, identity metadata, and
acceptance tooling. It does **not** contain a CD-i BIOS, Hotel Mario disc data,
generated game binaries, or emulator/tooling forks.

## Playing

You must supply both:

1. A legally dumped 512 KiB CD-i player BIOS (`cdi490a.rom` for the currently
   verified target).
2. A legally dumped Hotel Mario (USA) Mode-2 disc image. Use the `.cue` beside
   its raw `.bin`.

Build, then launch through the persistent-path helper:

```powershell
./tools/build.ps1
./tools/launch.ps1
```

The first launch asks for both files and saves their paths in ignored
`bios.cfg` and `disc.cfg` sidecars. Later launches reuse them. The runtime still
validates both assets at startup and never embeds either one in the executable.

Player preferences such as captured mouse control and one-shot host RTC sync
live in the runtime's persistent `player.cfg`.

## Building

Place this repository beside `cdirecomp`, matching the other per-game recomp
projects:

```text
Projects/
|-- cdirecomp/
`-- HotelMarioRecomp/
```

Requirements are CMake, Ninja or another supported generator, a C11 compiler,
and the SDL2 development package. To use a differently located engine:

```powershell
cmake -S . -B build -G Ninja -DCDIRECOMP_ROOT=C:/src/cdirecomp
cmake --build build --config Release -j
```

The resulting executable is `build/HotelMarioRecomp.exe` on Windows.

## Acceptance gate

With your own BIOS and disc image:

```powershell
./tools/accept-attract.ps1 -Bios C:/path/cdi490a.rom `
  -Disc C:/path/HotelMario.cue
```

The gate enters through the real player-shell input path and requires the
pixel-exact title, a populated background plane in the later intro, clean
bumper and intro XA audio with zero drops, expected disc progress, zero native
dispatch misses, and real-time field pacing.

`HotelMarioRecomp.exe` itself also enforces the asset contract: a BIOS-only
launch is rejected, and `--disc` is mandatory for this game-specific build.

See [DISC.md](DISC.md) for the verified asset identities and
[ISSUES.md](ISSUES.md) for the intentionally narrow current certification.
