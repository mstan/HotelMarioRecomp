# Known limits

- The verified boundary is BIOS boot through the later Hotel Mario attract
  intro (LBA 4650+), with both video planes and XA audio regression-gated. An
  extended run also advances through the record boundary that previously
  froze the background and stalled the sequence.
- Loaded game modules currently use cdirecomp's clean-room interpreter
  fallback. Static native module promotion is the next performance/maturation
  step; the accepted build already sustains real-time field pacing.
- Gameplay and a complete end-to-end playthrough remain unverified.
- The current project identity targets the USA raw Mode-2 CUE/BIN dump listed
  in `DISC.md` and the `cdi490a.rom` player BIOS.
- Release packaging is not established yet. Any future package must remain
  runtime-only and exclude BIOS, disc data, generated copyrighted artifacts,
  recompiler tools, and local development oracles.
