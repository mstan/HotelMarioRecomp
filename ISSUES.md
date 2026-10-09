# Known limits

The LLE product now statically compiles 174 distinct executable module
identities from the user-supplied USA disc. The real recompiled CD-RTOS loader
still loads/links them; bindings match the complete image SHA-256 and are
invalidated by RAM writes. Uncovered code uses the clean-room interpreter.

Intro background triggers and buffered XA playback now reach initial
gameplay. A normal-speed windowed input scenario reaches one-player Stage 1
at field 12000, with zero resets/dispatch misses and zero SDL PCM drops.
SDL keyboard polling no longer erases scripted button input.

The former input-free attract restart failure was corrected; an earlier
normal-speed windowed build completed 120000 fields with zero resets,
dispatch misses or PCM drops. The current audio lifecycle also passed an
accelerated field-40000 controller probe through repeated deaths/restarts
and game over. Exact complete attract cycles, every level/boss, both player
campaigns, the ending, save/restore and continue remain unverified.
No full-playthrough claim is made.

The current default LLE build passed all 30 headless + 30 windowed normal-speed
cold boots to the exact title, with linked-input provenance and native binding
evidence. The current seeded build also legitimately cleared one-player
Hotel 1 Stage 1 and loaded Stage 2; full campaigns remain open. Audio listening
checks are still pending. A local preview archive passed the
runtime-only five-file allowlist, build-graph, PE import and provenance audits;
it is not a certified end-to-end release.
The current identity remains the USA CUE/BIN and `cdi490a.rom` in DISC.md.

See the sibling engine's ISSUES.md for root causes, evidence commands and
central Beads issue references. Packages must exclude BIOS/disc data,
generated sources, recompiler tools and development oracles.
