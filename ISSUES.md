# Hotel Mario checkpoint and known limits

Updated 2026-10-09. The owner stopped gameplay implementation and testing,
then authorized documentation, README updates and default-branch integration.
All game probes are stopped. This remains an early LLE research preview;
there is no end-to-end playthrough claim and no HLE was added.

## Owner playtest and session closeout

On 2026-10-09 the owner reported that basic gameplay works well and the
title-screen background now works. Minor visual flickering was also reported;
it is tracked as open bug `beads-ssy9.1`. No exact scene, frequency, layer,
impact or root cause has been established. No flicker investigation or fix
was attempted during closeout.

This feedback comes from the indexed LLE build launched manually at normal
speed with DirectSound and the original BIOS/USA CUE. Launch metadata and logs
are retained in ignored `build/playable-lle/manual-play-20261009-095749/`.
The player's manual session is left under the owner's control. No automated
controller or campaign probe was resumed. Full-playthrough validation remains
open; this update records early gameplay feedback rather than a completed game.

## What is implemented

The LLE product statically compiles 174 distinct executable module identities
from the user-supplied USA disc. The real recompiled CD-RTOS loader still
loads/links them. Bindings match the complete image SHA-256, are invalidated
by CPU/DMA RAM writes, and guard resumable native execution with epochs.
Uncovered code uses the clean-room interpreter. Coverage uses a bounded,
indexed 262144-entry image/offset ledger; capture exhaustion is an error.

Intro file-wide trigger delivery now changes the original game's background
pages. Buffered audio and selection headers reach the first complete stage
record through the real ROM drivers. Decoder reset preserves the independent
audio processor, plain PLAY0 resumes it, and repeated death/restart paths
survive the former audio-CIL error. SDL polling and scripted/TCP input use
separate producer states and the same timed IKAT path.

These fixes are component-tested and exercised in early gameplay. They do not
establish complete CIAP/IKAT silicon accuracy or broader title compatibility.

## Tested versus unverified

| Area | Evidence actually observed | Remaining gate |
| --- | --- | --- |
| Components | Six compiler and eleven runtime checks passed | Every real module path, wider titles and complete hardware behavior |
| Latest default startup | 30/30 normal-speed headless cold boots to exact title, linked provenance and all 174 compiled identities | Complete current windowed launch batch |
| Latest windowed batches | First batch: three passes, fourth exited with code 0; second: fourteen passes, fifteenth exited with code 0; both failed before required capture | Explain shutdowns and complete a fresh 30-launch batch |
| Historical startup | Preceding executable passed 30 headless and 30 windowed cold launches | Does not certify the newer indexed executable |
| Intro | Eight distinct background pages observed; normal-speed windowed talk scene renders | Later campaign scenes and exact visual/audio timing |
| Latest one-player | Hotel 1 Stages 1–3 cleared; entered Stage 4 at field 51281 | Remaining stages, all hotels/bosses and ending |
| Seeded two-player | Mario entered Stage 3; Luigi entered Stage 5; final checkpoint field 145679, zero resets/misses | Both complete campaigns; only Mario's first two and Luigi's first four stages cleared |
| Attract | Earlier 120000/160000-field runs had no observed guest reset/miss but exhausted coverage; latest DirectSound run lost connection after field 68067 | Three actual nine-demo circuits with successful complete evidence |
| Audio | Early dummy-output probes had no PCM drops; older long seeded gameplay dropped 318656 PCM frames | Sustained real output, no drops, listening quality and normal-speed performance |
| Persistence | Named save `AAA` visible after normal close and cold boot with the same 32768-byte battery | Correct active hotel/stage restored through the original chooser |
| Packaging | Local five-file preview passed allowlist, Release/COSIM OFF graph, PE imports and linked provenance | Archive predates indexed ledger; rebuild/audit the final executable and complete release acceptance |

Normal-speed gameplay uses ordinary input, including original-game continues;
the controller reads state and sends buttons, never writes progress or patches
guest code. Its own early reversed door-state interpretation invalidated older
attempts. The corrected runs require the original zero-open-door count and
stage increment. The final helper changes are development tooling, not a
certified campaign driver.

Selecting a restore slot first loads unlocked progress; the original game then
uses a chooser for the active stage. Seeing the slot alone is not correct-stage
restore proof. The later two-player run selected new players.

The short `tools/accept-attract.ps1` probe is not three-cycle acceptance. The
engine's `hotelmario_attract_gate.py` checks the original AV map, ordered demos
1–9, and a return to demo 1 after each circuit. A failed scenario capture cannot
pass that gate; elapsed fields and a zero process exit are insufficient.

## Build identity and retained evidence

The tested indexed executable is 29906954 bytes, SHA-256
`1d330205d80d1b61bb8dc4e12a10b09c6ba0f44d7ce26baa58abe4d6e70682c0`.
Its tested core remains pinned to
`ddfa4e1b090b643a9ee596050e7eb345b8b276a2`; the engine pin in
`cdirecomp.pin` identifies the documented source checkpoint. Updating that
pin for documentation does not claim an executable was rebuilt.

Shared-core `main` also contains the feature through merge `eaeec13`, with all
six compiler checks passing against that combined core. Product generation
continues using the exact recorded `ddfa4e1` pin. Promoting a newer core would
require regeneration and fresh product acceptance.

The asset contract remains the USA CUE/BIN and `cdi490a.rom` in [DISC.md](DISC.md).
Runtime enforces the generated BIOS identity and full native-module hashes;
acceptance tooling records the entire disc SHA-256. BIOS/disc data, generated
sources, recompiler tools and development oracles stay out of packages.

Evidence is local and ignored under the sibling engine's `build/tmp/`:

- `indexed-lle-headless-matrix-20261009`
- `indexed-lle-windowed-matrix-20261009`
- `indexed-lle-windowed-matrix-second-20261009`
- `indexed-lle-windowed-attract-20261009`
- `indexed-lle-oneplayer-20261009`
- `normal-campaign-controller-20261009`
- `normal-production-save-20261009`, including `user-stop-checkpoint.json`,
  controller histories, save/restore screenshots and original battery file.

See the engine's [detailed validation ledger](https://github.com/mstan/cdirecomp/blob/master/ISSUES.md)
for exact earlier build identities, root causes, component test names and
resume cautions. Central Beads owners are `beads-6v0p`, `beads-bcha`,
`beads-z8yh` and `beads-mq6t`; the checkpoint integration is `beads-ttbl.1`.
The campaign/validation issues stay open. Gameplay work requires explicit
authorization to resume; no probe is currently running.
