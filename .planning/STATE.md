# Project State — AkariOS V6.1

## Project Reference
- **Name:** AkariOS V6.1
- **Code:** akarios
- **Type:** Windows 11 AME (Ameliorated Edition) playbook
- **Core Value:** Every system modification is deliberate, documented, and reversible where it matters. AkariOS must reliably strip Windows 11 down to gaming + daily-use essentials without breaking core functionality.

## Current Position
- **Phase:** 1 of 4 (Phase 1 complete — Network Restructuring)
- **Plan:** 01-01 complete (FSOS removal done)
- **Status:** Ready for Phase 2 (Feature Audit)

## Progress
```
Phase 0 (Init):    [x] Complete — codebase mapping, requirements, PROJECT.md
Phase 1 (Network): [x] Complete — FSOS TCP/IP stack additions removed from Section 29
Phase 2 (Audit):   [ ] Not started — needs planning
Phase 3 (Mod):    [ ] Not started
Phase 4 (Verify):  [ ] Not started
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

## Pending Todos
- Audit full feature set against actual custom.yml to produce a verified feature matrix (Phase 2)
- Decide on modularization approach for monolithic custom.yml — present plan and get user approval (Phase 3)
- Verify all bundled executables are referenced and correct (Phase 2)
- Verify NCSI fix works (EnableActiveProbing=1 + netprofm safety-net) (Phase 4)
- Verify Desktop cleanup via registry key delete produces clean icon layout (Phase 4)
- Verify LibreWolf winget install works in AME environment (Phase 4)

## Blockers/Concerns
- No ROADMAP.md existed until now (created 2026-08-28)
- No STATE.md existed until now (reconstructed 2026-08-28)
- This is a declarative YAML playbook project, not traditional code — GSD phases map to playbook restructuring tasks rather than code features
- No automated testing (manual AME Wizard VM runs only)

## Session Continuity
- **Last session:** 2026-08-28 — /gsd-resume-work initiated, ROADMAP.md + STATE.md created, Phase 1 discussed/planned/executed
- **Stopped at:** Phase 1 complete — ready to discuss/plan Phase 2 (Feature Audit)
- **Resume file:** None
- **Interrupted agents:** None

## Key Project Files
- **Main playbook:** `Configuration/custom.yml` (1303 lines, 40 sections — Section 29 trimmed to Vain-only)
- **UI config:** `playbook.conf` (AME Wizard feature pages, last restructured Aug 2026)
- **Planning:** `.planning/` directory with PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json, and codebase/ mapping docs
- **Codebase maps:** ARCHITECTURE.md, CONCERNS.md, CONVENTIONS.md, INTEGRATIONS.md, STACK.md, STRUCTURE.md, TESTING.md

## Requirements Summary
- **17 v1 requirements** defined across 4 phases:
  - Network Restructuring (NET-01 through NET-06) — Phase 1 ✓ Complete
  - Feature Audit (AUDIT-01 through AUDIT-05) — Phase 2
  - Codebase Restructuring (RESTRUCT-01 through RESTRUCT-03) — Phase 3
  - Bug Verification (BUG-01 through BUG-03) — Phase 4
- Phase 1: 6/6 requirements complete

---
*Last updated: 2026-08-28 (Phase 1 complete, ready for Phase 2)*