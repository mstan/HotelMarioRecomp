# HotelMarioRecomp

Hotel Mario (USA) as a native CD-i application, built with the pinned [cdirecomp](https://github.com/mstan/cdirecomp) engine and [recomp-ui](https://github.com/mstan/recomp-ui) launcher.

This is a research preview. The real recompiled CD-RTOS BIOS boots the game; selected native jobs accelerate qualified work. Complete campaigns, all bosses/endings and correct game-save restoration remain unverified.

## Get started

Requirements: Git, Python 3.11+, CMake 3.20+, Ninja, a C/C++ toolchain, SDL2 development files and OpenGL. Windows MinGW and Linux are supported build paths.

```sh
git clone --recurse-submodules https://github.com/mstan/HotelMarioRecomp.git
cd HotelMarioRecomp
python tools/build.py --bios /path/to/cdi490a.rom --disc "/path/to/Hotel Mario (USA).cue"
```

On Linux use `python3`. Windows also provides `setup.ps1 -Bios <rom> -Disc <cue>`; Linux provides `sh setup.sh --bios <rom> --disc <cue>`. Setup initializes the pinned submodules and calls the same build driver.

The build verifies the supported BIOS/disc identities listed in [DISC.md](DISC.md), builds the pinned compilers, generates the BIOS and game modules, then builds `build/HotelMarioRecomp` (`.exe` on Windows). Existing local `bios.cfg` and `disc.cfg` selections may supply the input paths. No build step opens file dialogs.

## Play

Open the built executable, or run `tools/launch.ps1` on Windows. The shared CD-i launcher selects and verifies the BIOS and disc, remembers choices and offers the controls the runtime implements:

- Keyboard, mouse and selected gamepad input, with bindings.
- Original 4:3 or Fit to screen, window width, fullscreen and filtering.
- Audio enable/disable and volume.

The CD-i skin uses a dark teal palette, gold focus accents and the game's title artwork. Fit to screen is the fresh-profile default; it scales the original picture rather than expanding the game world. Saved choices remain authoritative.

Play boots the real player shell. Use its **Play CD-I** control to enter the game. Default keys are arrows/WASD, Z/Enter/Space for button 1 and X/Backspace for button 2. F11 or Alt+Enter toggles fullscreen; Esc quits.

Preferences and native NVRAM stay in the existing per-user `cdirecomp/player` location. Preserve `player.cfg` and `nvram.bin` together. A release update must not replace them. See [runtime instructions](RUNTIME-README.md).

## Project layout

- `cdirecomp/`, `recomp-ui/`: exact engine and launcher submodule pins.
- `game.toml`, `seeds/`: supported image facts and observed module entry points.
- `src/`, `assets/`: launcher adapter and title branding.
- `generated/`: ignored BIOS/module outputs owned by this project.
- `tools/`, `tests/`: build, packaging and game acceptance checks.

No adjacent engine checkout, firmware, disc data or generated guest source is included in Git. See [build details](docs/BUILDING.md) and [validation limits](docs/VALIDATION.md).

## License

For this project's code covered by the [PolyForm Noncommercial License](LICENSE),
[PERMISSIONS.md](PERMISSIONS.md) grants standing permission for voluntary
donations, sponsorships, and advertising revenue, including support for broader
development initiatives. Payment must not buy access to the software, games
built with it, or their updates, features, or game content, including early access.

Matthew Stanley has authority from the relevant copyright holders to grant
these permissions for the project's PolyForm-covered code. Third-party
components and code explicitly licensed under other terms retain those terms.

[PolyForm Noncommercial License 1.0.0](LICENSE) — © 2026 Matthew Stan. Covers
this repository's build glue and tooling only. It grants no rights to Nintendo,
Philips, or any other third-party intellectual property; you must supply your
own legally obtained BIOS and disc image.
