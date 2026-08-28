# Project State — AkariOS V6.1

## Project Reference
- **Name:** AkariOS V6.1
- **Code:** akarios
- **Type:** Windows 11 AME (Ameliorated Edition) playbook
- **Core Value:** Every system modification is deliberate, documented, and reversible where it matters. AkariOS must reliably strip Windows 11 down to gaming + daily-use essentials without breaking core functionality.

## Current Position
- **Phase:** 2 of 4 (Phase 2 complete — Feature Audit)
- **Plan:** 02-01 complete (Feature matrix + two fixes)
- **Status:** Ready for Phase 3 (Codebase Restructuring)

## Progress
```
Phase 0 (Init):    [x] Complete — codebase mapping, requirements, PROJECT.md
Phase 1 (Network): [x] Complete — FSOS TCP/IP stack additions removed from Section 29
Phase 2 (Audit):   [x] Complete — feature matrix, toggle cross-ref, executable/image audit, two fixes applied
Phase 3 (Mod):    [ ] Not started — modularization decision pending user approval
Phase 4 (Verify):  [ ] Not started — NCSI fix, desktop cleanup, LibreWolf winget
```

## Recent Decisions
| Decision | Rationale | Outcome |
|---|---|---|
| Keep custom.yml monolith for now | User said "i was just asking" in Aug 2026 | Pending (revisiting in Phase 3) |
| Strip Section 29 to Vain-only | Vain = NIC driver layer (gaming latency); FSOS = TCP/IP stack (throughput) | ✓ Done |
| Keep MMCSS NetworkThrottlingIndex/SystemResponsiveness | Universal recommendations, unrelated to FSOS | Kept |
| Don't add TcpNoDelay/TCPAckFrequency | Disables Nagle's, hurts non-gaming throughput | Rejected |
| LibreWolf via winget | GitHub repo 404s, winget always pulls latest | Fixed (Aug 2026) |
| All defaults IsChecked=false | User opt-in — no surprises | In place |
| Wire up remove-uwp-photos toggle | Was dead — existed in playbook.conf but no option: gates in custom.yml | ✓ Done (7 Legacy Photo Viewer entries added) |
| Update Section 10 header to LibreWolf | Header still said "Firefox Dev" after Aug 2026 replacement | ✓ Done |

## Completed Todos
- [x] Produce verified feature matrix mapping all 40 sections (AUDIT-01)
- [x] Cross-check all feature toggles in custom.yml against playbook.conf (AUDIT-02)
- [x] Verify all bundled executables are referenced and correct (AUDIT-03)
- [x] Audit Images/ directory (AUDIT-04)
- [x] Verify CLAUDE.md toggles match playbook.conf (AUDIT-05)
- [x] Wire up dead remove-uwp-photos toggle (Fix 1)
- [x] Update stale Section 10 header comment (Fix 2)

## Pending Todos
- Decide on modularization approach for monolithic custom.yml — present plan and get user approval (Phase 3)
- Verify NCSI fix works (EnableActiveProbing=1 + netprofm safety-net) (Phase 4)
- Verify Desktop cleanup via registry key delete produces clean icon layout (Phase 4)
- Verify LibreWolf winget install works in AME environment (Phase 4)

## Blockers/Concerns
- No automated testing (manual AME Wizard VM runs only)
- firefox.png is orphaned in Images/ — noted for Phase 3 cleanup

## Session Continuity
- **Last session:** 2026-08-28 — Phase 1 (Network Restructuring) completed and committed; Phase 2 (Feature Audit) discussed, planned, and executed
- **Stopped at:** Phase 2 complete — ready to discuss/plan Phase 3 (Codebase Restructuring)
- **Resume file:** None
- **Interrupted agents:** None

## Key Project Files
- **Main playbook:** `Configuration/custom.yml` (1310 lines, 40 sections — Section 29 trimmed to Vain-only, Section 10 header updated, Section 12 remove-uwp-photos wired)
- **UI config:** `playbook.conf` (AME Wizard feature pages, last restructured Aug 2026)
- **Planning:** `.planning/` directory with PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json, and codebase/ mapping docs
- **Phase artifacts:** `.planning/phases/` — 01-network-restructuring/ (7 files), 02-feature-audit/ (6 files + AUDIT.md)
- **Codebase maps:** ARCHITECTURE.md, CONCERNS.md, CONVENTIONS.md, INTEGRATIONS.md, STACK.md, STRUCTURE.md, TESTING.md

## Requirements Summary
- **17 v1 requirements** defined across 4 phases:
  - Network Restructuring (NET-01 through NET-06) — Phase 1 ✓ Complete
  - Feature Audit (AUDIT-01 through AUDIT-05) — Phase 2 ✓ Complete
  - Codebase Restructuring (RESTRUCT-01 through RESTRUCT-03) — Phase 3
  - Bug Verification (BUG-01 through BUG-03) — Phase 4
- Phase 1: 6/6 requirements complete
- Phase 2: 5/5 requirements complete

## Audit Results Summary
| Audit Target | Result |
|-------------|--------|
| All 40 sections present and numbered | 40/40 ✓ |
| Feature toggle 1:1 match | 22/22 ✓ |
| Executable audit | 5 direct + 1 indirect + 2 intentional, 0 orphans ✓ |
| Image audit | 6 browser images match, 1 orphan (firefox.png) noted ✓ |
| CLAUDE.md toggle verification | 22/22 ✓ |

---

*Last updated: 2026-08-28 (Phase 2 complete, ready for Phase 3)*
