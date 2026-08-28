# Phase 2 Summary: Feature Audit

**Phase:** 02-feature-audit
**Status:** COMPLETE ✓
**Date:** 2026-08-28
**Commit:** Pending

## What Was Done

1. **Scouted the full codebase** — Read all 40 sections of `custom.yml`, cross-referenced `playbook.conf` toggles, audited `Executables/` and `Images/` directories, and verified CLAUDE.md toggle list.

2. **Produced verified feature matrix** — 40-section matrix mapping each section to its header toggle, directive types, and gate type (always-on vs gated). Results in `AUDIT.md`.

3. **Feature toggle cross-reference** — Verified 1:1 match between all 22 `option:` gates in custom.yml and `<Name>` values in playbook.conf. 3 structural names correctly excluded.

4. **Executable audit** — Audited all 7 files in `Executables/`: 5 direct references, 1 indirect (NoDefender.cab), 2 intentional (EnableDefender.ps1 restoration script, ControlPanelSettings.reg dead reference).

5. **Image audit** — Verified 8 images in `Images/`: 6 browser images match FileName refs, 1 structural (next.png), 1 orphan (firefox.png — noted for Phase 3 cleanup).

6. **CLAUDE.md toggle verification** — All 22 feature toggles from CLAUDE.md confirmed present in playbook.conf.

7. **Fixed Discrepancy 1** — Wired up dead `remove-uwp-photos` toggle by adding 7 Legacy Photo Viewer registry entries (HKCR\.jpg, .jpeg, .png, .bmp, .gif, .tif, .tiff → PhotoViewer.JustOpen) gated on `option: 'remove-uwp-photos'`.

8. **Fixed Discrepancy 2** — Updated Section 10 header comment from "Firefox Dev" to "Librewolf".

## Code Changes (custom.yml only)

- **Line 204:** Section 10 header: "Firefox Dev" → "LibreWolf"
- **Lines 267-273:** 7 new `registryValue` directives with `option: 'remove-uwp-photos'` gate for Legacy Photo Viewer

## Decisions

- `remove-uwp-photos` wired up per user direction (D-01) — adds actual registry entries, not just gating existing ones
- Section 10 header updated per user direction (D-02)
- NoDefender.cab classified as indirect reference (by design)
- ControlPanelSettings.reg and EnableDefender.ps1 left as-is per user direction (leave for now)
- AUDIT.md created as dedicated file (output format default since user didn't select)

## Deferred Items

- Remove orphaned `firefox.png` from Images/ (Phase 3 cleanup)
- General codebase cleanup: orphaned assets, stale comments (Phase 3)

## Next Phase

**Phase 3: Codebase Restructuring** — Decide modularization approach, create section directories if needed, ensure AME Wizard compatibility.
