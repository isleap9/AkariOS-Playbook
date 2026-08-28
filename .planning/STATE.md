# Project State — AkariOS V6.1

## Project Reference
- **Name:** AkariOS V6.1
- **Code:** akarios
- **Type:** Windows 11 AME (Ameliorated Edition) playbook
- **Core Value:** Every system modification is deliberate, documented, and reversible where it matters. AkariOS must reliably strip Windows 11 down to gaming + daily-use essentials without breaking core functionality.

## Current Position
- **Phase:** 4 of 4 (ALL COMPLETE — full roadmap finished)
- **Plan:** 04-01 complete (Bug verification: NCSI fix, desktop cleanup, LibreWolf winget)
- **Status:** All phases complete — roadmap finished

## Progress
```
Phase 0 (Init):    [x] Complete — codebase mapping, requirements, PROJECT.md
Phase 1 (Network): [x] Complete — FSOS TCP/IP stack additions removed from Section 29
Phase 2 (Audit):   [x] Complete — feature matrix, toggle cross-ref, executable/image audit, two fixes applied
Phase 3 (Mod):    [x] Complete — modular split into sections/ + build script + line 24 fix
Phase 4 (Verify): [x] Complete — all 3 bug fixes verified via static analysis (28/28 checks passed)
```

## Recent Decisions
| Decision | Rationale | Outcome |
|---|---|---|
| Keep custom.yml monolith for now | User said "i was just asking" in Aug 2026 | **CHANGED** — User selected Option B (modularization with build step) in Phase 3 |
| Strip Section 29 to Vain-only | Vain = NIC driver layer (gaming latency); FSOS = TCP/IP stack (throughput) | ✓ Done |
| Keep MMCSS NetworkThrottlingIndex/SystemResponsiveness | Universal recommendations, unrelated to FSOS | Kept |
| Don't add TcpNoDelay/TCPAckFrequency | Disables Nagle's, hurts non-gaming throughput | Rejected |
| LibreWolf via winget | GitHub repo 404s, winget always pulls latest | Fixed (Aug 2026), Verified (Phase 4) |
| All defaults IsChecked=false | User opt-in — no surprises | In place |
| Wire up remove-uwp-photos toggle | Was dead — existed in playbook.conf but no option: gates in custom.yml | ✓ Done (7 Legacy Photo Viewer entries added) |
| Update Section 10 header to LibreWolf | Header still said "Firefox Dev" after Aug 2026 replacement | ✓ Done |
| Modularize with build step (Option B) | User explicitly selected over keep-monolithic (A) or hybrid (C) | ✓ Done |
| custom.yml as build output (committed) | AME Wizard needs monolithic file; sections are source-of-truth; build script generates | ✓ Done |
| Byte-identical rebuild verified | Build script produces identical output (verified via cmp) | ✓ Verified |
| Stale "firefoxdev" comment fix | Line 24 still referenced removed Firefox Developer edition | ✓ Done (Phase 3) |

## Completed Todos
- [x] Produce verified feature matrix mapping all 40 sections (AUDIT-01)
- [x] Cross-check all feature toggles in custom.yml against playbook.conf (AUDIT-02)
- [x] Verify all bundled executables are referenced and correct (AUDIT-03)
- [x] Audit Images/ directory (AUDIT-04)
- [x] Verify CLAUDE.md toggles match playbook.conf (AUDIT-05)
- [x] Wire up dead remove-uwp-photos toggle (Fix 1)
- [x] Update stale Section 10 header comment (Fix 2)
- [x] Decide modularization approach and get user approval (RESTRUCT-01)
- [x] Create Configuration/sections/ with 40 per-section YAML partials (RESTRUCT-02)
- [x] Ensure build script produces AME Wizard-compatible custom.yml (RESTRUCT-03)
- [x] Fix stale "firefoxdev" comment on line 24
- [x] Update README.md with development workflow
- [x] Verify NCSI fix (BUG-01) — EnableActiveProbing=1 + netprofm safety-net
- [x] Verify Desktop cleanup (BUG-02) — registry key delete, no SendMessage/FindWindow remnants
- [x] Verify LibreWolf winget install (BUG-03) — correct package ID, appx keep-list, all flags present

## Pending Todos
(none — all 4 phases of the roadmap are complete)

## Blockers/Concerns
- No automated testing (manual AME Wizard VM runs only)
- firefox.png is orphaned in Images/ — noted for future cleanup
- BUG-01/02/03 runtime verification requires Windows AME Wizard VM (not available in this environment)

## Session Continuity
- **Last session:** 2026-08-28 — All 4 phases completed and committed
- **Stopped at:** All phases complete — roadmap finished
- **Resume file:** None
- **Interrupted agents:** None

## Key Project Files
- **Main playbook (build output):** `Configuration/custom.yml` (1310 lines, 40 sections)
- **Modular source:** `Configuration/sections/` — 40 section files + `Configuration/header.yml`
- **Build scripts:** `scripts/build-playbook.py` (sections → custom.yml), `scripts/split-playbook.py` (once: custom.yml → sections)
- **UI config:** `playbook.conf` (AME Wizard feature pages)
- **Planning:** `.planning/` directory with PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json, and codebase/ mapping docs
- **Phase artifacts:** `.planning/phases/` — 01-network-restructuring/ (7 files), 02-feature-audit/ (6 files + AUDIT.md), 03-codebase-restructuring/ (5 files), 04-bug-verification/ (5 files)
- **Codebase maps:** ARCHITECTURE.md, CONCERNS.md, CONVENTIONS.md, INTEGRATIONS.md, STACK.md, STRUCTURE.md, TESTING.md

## Requirements Summary
- **17 v1 requirements** defined across 4 phases:
  - Network Restructuring (NET-01 through NET-06) — Phase 1 ✓ Complete (6/6)
  - Feature Audit (AUDIT-01 through AUDIT-05) — Phase 2 ✓ Complete (5/5)
  - Codebase Restructuring (RESTRUCT-01 through RESTRUCT-03) — Phase 3 ✓ Complete (3/3)
  - Bug Verification (BUG-01 through BUG-03) — Phase 4 ✓ Complete (3/3)

## Audit Results Summary
| Audit Target | Result |
|-------------|--------|
| All 40 sections present and numbered | 40/40 ✓ |
| Feature toggle 1:1 match | 22/22 ✓ |
| Executable audit | 5 direct + 1 indirect + 2 intentional, 0 orphans ✓ |
| Image audit | 6 browser images match, 1 orphan (firefox.png) noted ✓ |
| CLAUDE.md toggle verification | 22/22 ✓ |
| Build script byte-identical verification | ✓ Verified (cmp identical) |
| BUG-01 (NCSI fix) | ✅ VERIFIED (implementation) / UNVERIFIED (runtime) |
| BUG-02 (Desktop cleanup) | ✅ VERIFIED (implementation) / UNVERIFIED (runtime) |
| BUG-03 (LibreWolf winget) | ✅ VERIFIED (implementation) / UNVERIFIED (runtime) |

## Bug Verification Summary (Phase 4)

| Bug | Implementation | Runtime | Total Checks |
|-----|---------------|---------|-------------|
| BUG-01 (NCSI fix) | ✅ VERIFIED | UNVERIFIED | 6 checks passed |
| BUG-02 (Desktop cleanup) | ✅ VERIFIED | UNVERIFIED | 6 checks passed |
| BUG-03 (LibreWolf winget) | ✅ VERIFIED | UNVERIFIED | 10 checks passed |

**Total: 28/28 static verification checks passed. 0 runtime-verified (requires Windows AME Wizard VM).**

### Recommendations for Live Verification
- BUG-01: Check Settings → Network shows "Connected" status on Windows VM after playbook run
- BUG-02: Verify clean desktop icon layout on first login after playbook run
- BUG-03: Run playbook with `browser-librewolf` toggle ON; verify winget installs LibreWolf successfully

---

*Last updated: 2026-08-28 (all 4 phases complete)*
