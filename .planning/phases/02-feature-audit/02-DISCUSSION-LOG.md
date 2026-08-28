# Phase 2 Discussion Log

**Phase:** 02-feature-audit
**Date:** 2026-08-28
**Mode:** default

## Discussion

### Gray Areas Identified
1. Discrepancy 1: `remove-uwp-photos` dead toggle — wire it up, remove it, or leave as-is?
2. Discrepancy 2: Stale Section 10 header says "Firefox Dev" — update to "LibreWolf"?
3. Discrepancy 3: NoDefender.cab classification — referenced indirect, missing from custom.yml, or not used?
4. Discrepancy 4: ControlPanelSettings.reg and EnableDefender.ps1 dead references — flag as issue, note as intentional, or remove files?
5. Output format for feature matrix — dedicated file, embedded in CONTEXT, or JSON?

### User Selections
- **D-01:** Wire up `remove-uwp-photos` — add `option: 'remove-uwp-photos'` gates to Section 12 Legacy Photo Viewer entries
- **D-02:** Yes, update Section 10 header to say "LibreWolf" instead of "Firefox Dev"
- **D-03:** Leave ControlPanelSettings.reg and EnableDefender.ps1 as-is for now (classify as intentional)
- **Output format:** User did not select an option (timed out) — Claude's discretion: dedicated AUDIT.md file in phase directory

### Decisions Made
1. Wire up `remove-uwp-photos` toggle by adding Legacy Photo Viewer registry entries with `option: 'remove-uwp-photos'` gates in Section 12 (UWP Photos stays always-kept)
2. Update Section 10 header comment: "Firefox Dev" → "LibreWolf"
3. Classify NoDefender.cab as "referenced (indirect)" — used by DisableDefender.ps1 at runtime
4. Classify ControlPanelSettings.reg and EnableDefender.ps1 as INTENDED (historical reference / restoration script)
5. Output feature matrix and audit findings in dedicated AUDIT.md file

### Deferred Ideas
- Modularizing custom.yml — Phase 3
- Bug verification — Phase 4

---
*Phase: 02-feature-audit*
*Discussion completed: 2026-08-28*
