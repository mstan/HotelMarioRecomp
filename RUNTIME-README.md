# HotelMarioRecomp development preview

This Windows x64 build runs the original CD-RTOS BIOS and Hotel Mario through
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

The archive contains the executable, SDL2, a configuration example, this
README, and third-party notices. Supply assets separately. The native build
uses no OS-9 HLE replacements.
