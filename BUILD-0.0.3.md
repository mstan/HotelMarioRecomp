# Hotel Mario v0.0.3 Windows release

Published on2026-11-01 after the owner authorized merging all reviewed work.
Core PR7 and engine/consumer PR1-7 are merged.

- [Windows release](https://github.com/mstan/HotelMarioRecomp/releases/tag/v0.0.3)
- Release source: `e85d362fecf8c7f6221e145295361a5d2883cfcd`.
- Engine pin: `0410fa81c29d20756d0639ed7b317c02dd62e1b5`.
- Core pin: `cd1e5e28dc26ec6a887197aac7eaaf8c8c870019`.
- ZIP SHA256: `60201b238985ce575844341a792d762b05d41dafce1d9534c418b93f10775f84`.
- EXE SHA256: `09e14fdb74f8102f42972e0fa7e2b1fc1892fac996e3fb3bf9e4829d4d4569f0`.

Release/OFF build graph, linked-input hashes, PE imports and five-file package
allowlist pass. The cached executable matches all reviewed PE section hashes;
its relink changes the PE timestamp/checksum only. It is tested from the ZIP.
Both uploaded packages were downloaded and their hashes verified.

The packaged Hotel Mario and generic CD-i executables match complete canonical
contracts through13000 scripted fields. Each uses real OpenGL16x,216 native
readbacks/zero mismatches and zero GPU fallbacks. This pace4/dummy-audio setup
is packaging/correctness qualification, not a new performance A/B. Both host
audio queues overflow at the accelerated pace; all6181056 decoded PCM frames
and hash `eef10d6fb4b83854` match. Normal-speed listening is untested here.

Earlier required16x normal-cadence qualification and neutral native1x CPU
scope remain unchanged. Desired32x/64x full-speed and lower-end16x remain
unqualified. Full campaigns/bosses/ending, correct active-stage save restoration
and flicker remain open. No new Linux package is included.

Exact per-product evidence is in the engine's
`docs/releases/v0.0.3-windows.json`; raw files and the reusable current generic
build are at `G:/Temp/Codex/cdirecomp/release-v0.0.3-20261101`. Only verified
superseded Windows delivery ZIPs, download duplicates and empty temp were
removed. Existing Linux artifacts, immutable inputs, owner saves/settings and
the active owner playtest are preserved. Tracking: `beads-ttbl.9`, `beads-7t8h`.
