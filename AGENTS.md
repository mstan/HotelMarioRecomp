# Working on HotelMarioRecomp

- This repository owns Hotel Mario facts, module seeds, launcher identity, generated outputs, packaging and game acceptance. Reusable CD-i behavior belongs in the pinned cdirecomp engine; generic launcher behavior belongs in recomp-ui.
- Track game work in the private central Beads database under the Hotel Mario epic. Keep private intake, session notes and raw evidence outside tracked source.
- Use the root engine/UI submodules. Development overrides are explicit build-driver options; never reintroduce sibling-checkout defaults or a text pin.
- Never edit generated guest C or commit firmware, discs, native saves or player settings. Build through tools/build.py; source-only project checks use HOTELMARIO_BUILD_PLAYER=OFF.
- Keep native LLE implementations functional. Consumer defaults select qualified HLE jobs; --reference builds the LLE alternatives.
- Automated QA uses explicit asset paths, isolated disposable preferences/saves, muted output and the runtime TCP interface. Never open native save-file pickers.
- Preserve original in-game NVRAM, saved aspect/control choices and individual validation caveats. Complete campaign/save restoration acceptance is still separate from bounded smoke checks.
- Package with tools/package.py; preserve its exact DLL and launcher asset audits. No recompiler, oracle, firmware, disc, generated source or development evidence belongs in a runtime archive.
