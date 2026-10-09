# Hotel Mario v0.0.2 build notes

Built on 2026-10-09 from the committed LLE checkpoint, following the sibling
TombaRecomp Windows ZIP/Linux AppImage workflow. No runtime, hardware or HLE
changes were introduced. Both packages require your matching BIOS and USA
CUE/BIN; neither includes original assets, generated sources or developer tools.

## Artifacts

Local outputs are in `dist/`, with individual `.sha256` files, `SHA256SUMS`,
and a Linux `.audit.json` manifest. They have not been published as a GitHub release.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `HotelMarioRecomp-v0.0.2-windows-x64.zip` | 10533722 | `c22829a59f3668e2bb6a9d5e0baa2907436e539c51f7351ddd0812b700497e83` |
| `HotelMarioRecomp-v0.0.2-linux-x86_64.AppImage` | 14903800 | `ff3e6cdc6c73ac7dfffc857a312d813dc2e29f6ce85cf78c8f4ba0cf5bfaa442` |

The Windows ZIP has five runtime/support files. The Linux AppImage has 129
audited files, including SDL2 dependencies and 37 library notice records.
Linux is experimental: the build/test baseline is Ubuntu 24.04 x86_64 under
WSL. Older distributions and physical desktops were not tested.

## Provenance

Compiled-input snapshots: engine `5d482e772290bf130b118f9c7df28803a9a12c3d`,
product `6fd6fc1c232a1800866b5f0c10f4a4fc6aedaf38`, core
`ddfa4e1b090b643a9ee596050e7eb345b8b276a2`. Windows regenerated all 174
default game module identities; Linux used the same generated BIOS/modules.
There are no additional observed callback seeds in these packages.

Final shared packaging helper: engine commit `6363191`, file SHA-256
`91367af3e83430c8b9b2b084b4c93baa3816fb85841195df6e30a1e86c5c4544`.
Later documentation/pin updates do not change the compiled runtime inputs.

Windows packaged executable SHA-256:
`57c511e0036840d06ed5cbac7111801d768ff00c56fdaa8e480456bd3b9e1cc3`.
Linux linked executable SHA-256:
`4e14b9809a1b32cd83a5eb13e3a627d63b1ff29e1479365fd9c5c7d0d3a16b5e`.
Linux packaged executable SHA-256:
`c6a10eb0bd0a4fbc9ad89abab42612316623705849dc61a8db55edb1cd32fad7`.
linuxdeploy changes the ELF library search paths, explaining the Linux hash
difference. The audit binds the verified linked executable to the packaged ELF
and compares the final extracted payload with the staged manifest. Link-input
sidecars remain local, outside both runtime packages.

## Tested and untested

- Both fresh Release/COSIM OFF builds linked; package provenance and build-graph
  checks passed. Windows passed PE imports and the five-file allowlist. Linux
  passed x86_64 ELF, dependency, library-notice and extracted-payload checks.
- All eleven Linux runtime and six compiler component tests passed. Windows
  component checks passed at the earlier checkpoint; they were not rerun here.
- Exact packaged Windows executable: normal-speed headless BIOS/shell/intro
  boot to title at field 1912. Actual AppImage: normal-speed windowed boot under
  Xvfb using `APPIMAGE_EXTRACT_AND_RUN=1`, title at field 1905. Both captured
  framebuffer `1b902b2f985afb5f`, zero native dispatch misses and zero guest
  resets, with 174 compiled module identities. Both used SDL dummy audio.
- No new full playthrough, stage progression, input stress, save/restore,
  sustained audio/performance, controller or flicker checks were performed.
  Physical Linux display/audio, FUSE mounting and GUI asset selection remain
  untested. Earlier owner feedback reports good basic gameplay and a working
  title background, with minor flicker. Full campaigns remain unverified.

Windows evidence: `build/release-v0.0.2-windows.log`,
`build/release-v0.0.2-windows-smoke/` and the build's `.exe.build.json`.
Linux evidence: `/home/matthew/hotelmario-release-0.0.2-20261009/`, including
`input-revisions.json`, `build-linux.log`, `runtime-tests.log`,
`compiler-tests.log`, `package-linux.log`, `package-linux-smoke/` and linked
ELF `.build.json`. Failed packaging attempts were retained as rejected evidence;
the delivered AppImage is the one with the successful audit and checksum above.

Beads build tasks: `beads-ssy9.2`, `beads-ttbl.2`. Campaign/validation issues
`beads-6v0p`, `beads-bcha`, `beads-z8yh`, `beads-mq6t` and flicker issue
`beads-ssy9.1` stay open. Beads updates are local; its Dolt remote currently
references missing data and has not synchronized successfully.
