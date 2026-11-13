# Hotel Mario - native CD-i research preview

Open HotelMarioRecomp to enter the shared CD-i launcher. Select your own supported player BIOS and Hotel Mario USA CUE/BIN disc. The launcher verifies them and remembers their paths. Firmware and disc images are not included.

Choose keyboard, mouse or a connected gamepad and configure bindings. Display settings offer Original 4:3 and Fit to screen, window width, fullscreen and filtering. Audio settings control volume and output enable. Fresh profiles use Fit to screen; existing choices are preserved. Fit scales the original picture and does not expand its field of view.

Press Play, then use the real CD-i shell's Play CD-I control. Default keys: arrows/WASD, Z/Enter/Space for button 1, X/Backspace for button 2. F11 or Alt+Enter toggles fullscreen; Esc quits. Both original-game player modes share the CD-i controller input.

Preferences and native saves remain in the per-user cdirecomp/player directory printed at startup. Preserve player.cfg and nvram.bin together across updates. Do not replace them with player.cfg.example. CDI_PLAYER_CONFIG_PATH can select a separate profile. Selecting different media does not delete native NVRAM.

For explicit-path launches: HotelMarioRecomp player.rom --disc game.cue --no-launcher. Add --launcher to show settings with those paths prefilled.

This remains development software. Complete campaigns, every boss/ending, correct restored stage and sustained audio/gameplay acceptance are unverified. Keep native save backups.

See THIRD-PARTY-NOTICES.md and LICENSES/ for redistributable component notices. No rights to Nintendo or Philips software are granted.
