# HotelMarioRecomp development preview

The Windows x64 ZIP and experimental Linux x86_64 AppImage run the original
CD-RTOS BIOS and Hotel Mario through
the low-level runtime. Full campaigns and save/restore validation are still in
progress; this archive is a local development preview.

Supply your own matching `cdi490a.rom` and Hotel Mario (USA) Mode-2 CUE/BIN.
Keep the CUE beside its referenced BIN and launch from PowerShell:

```powershell
.\HotelMarioRecomp.exe "C:\your\cdi490a.rom" --disc "C:\your\Hotel Mario (USA).cue"
```

Choose **Play CD-i** in the player shell. After the intro, select one or two
players and a new game. Press button 1 at the stage title to begin.

Arrows/WASD move the controller. Enter, Space, or Z is button 1 (jump);
Backspace or X is button 2 (open/close a door). Up enters an open door or an
elevator; down exits. A controller maps D-pad/A/B to those inputs. F11 or
Alt+Enter toggles fullscreen; Esc exits.

On normal launch, preferences and the player battery live in SDL's per-user
preference directory; the runtime prints the path. Mouse capture is optional
in `player.cfg` and releases when the window loses focus. Keep `nvram.bin` to
retain the player's saved data. Game-level save/restore is not yet certified.

The Windows ZIP contains the executable, SDL2, a configuration example, this
README, and third-party notices. Supply assets separately. The native build
uses no OS-9 HLE replacements.

For Linux, make the AppImage executable and pass your own assets:

```sh
chmod +x HotelMarioRecomp-*-linux-x86_64.AppImage
./HotelMarioRecomp-*-linux-x86_64.AppImage /path/to/cdi490a.rom --disc "/path/to/Hotel Mario (USA).cue"
```

Alternatively place `cdi490a.rom` and `Hotel Mario (USA).cue` with its BIN beside
the AppImage. With no arguments, the launcher uses those filenames or offers
file selection when the desktop's `zenity` is available. The AppImage bundles
SDL2 and its redistributable dependencies; it needs a Linux desktop and the
host's glibc. The build baseline is Ubuntu 24.04. If FUSE is unavailable, use
`--appimage-extract-and-run` before the BIOS argument. Preferences and NVRAM
remain in SDL's writable per-user directory, outside the AppImage.

The owner reports working basic gameplay and the title-screen background.
Minor visual flickering remains. Both full campaigns, ending, correct save
restoration, and sustained audio/performance are not yet certified.

The native runtime is licensed under
[PolyForm Noncommercial 1.0.0](https://github.com/mstan/cdirecomp/blob/master/LICENSE).
SDL2's notice is included. The AppImage also carries the installed-package
copyright notices and referenced common license texts for its bundled libraries.
