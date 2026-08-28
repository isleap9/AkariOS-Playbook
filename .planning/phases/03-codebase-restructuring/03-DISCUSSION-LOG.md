# Phase 3 Discussion Log

**Phase:** 03-codebase-restructuring
**Date:** 2026-08-28
**Mode:** default

## Discussion

### Gray Areas Identified
1. Keep monolithic (Option A) vs modularize with build step (Option B) vs hybrid (Option C)
2. Which modularization approach if Option B
3. How to handle the stale "firefoxdev" comment on line 24
4. Whether to also fix the line 24 comment as part of Phase 3 or leave for later

### User Selection
- **User selected:** Option 2 (Option B — Source-Managed Modularization with build step)
- User did not respond to secondary gray areas (firefoxdev comment, output format) — Claude's discretion applied

### Decisions Made
1. **Option B chosen** — Split custom.yml into Configuration/sections/01-40.yml + header.yml, with a Python build script that concatenates
2. **Firefoxdev comment** — Will fix as part of Phase 3 (it's a stale reference discovered during audit)
3. **Build script** — Python (already used in project for GSD tooling, available in environment)
4. **Build output** — custom.yml remains committed (AME Wizard ships it); section files are source-of-truth
5. **One-time split** — Create split-playbook.py to bootstrap the modular structure from the current monolithic file

### Deferred Items
- Removing firefox.png orphan from Images/ (noted in Phase 2 AUDIT.md, pending)
- General cleanup of dead references (EnableDefender.ps1, ControlPanelSettings.reg) — per Phase 2 user direction, left as-is

---
*Phase: 03-codebase-restructuring*
*Discussion completed: 2026-08-28*
