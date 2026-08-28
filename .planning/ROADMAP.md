# Roadmap: AkariOS V6.1

## Overview

Restructure and audit the AkariOS Windows 11 AME playbook. The playbook is organized into modular section files (`Configuration/sections/` with 40 YAML partials + `Configuration/header.yml`) and built into a monolithic `Configuration/custom.yml` via `scripts/build-playbook.py` — AME Wizard requires a single file. Four phases cover network restructuring, full feature audit, codebase modularization, and verification of bug fixes from the August 2026 session.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3, 4): Planned milestone work

- [x] **Phase 1: Network Restructuring** - Strip Section 29 to Vain-only network tweaks, remove FSOS TCP/IP stack additions
- [x] **Phase 2: Feature Audit** - Produce a verified feature matrix mapping all 40 sections, cross-check toggles, audit executables and images
- [x] **Phase 3: Codebase Restructuring** - Modularize custom.yml into Configuration/sections/ + build script, get user approval
- [ ] **Phase 4: Bug Verification** - Verify NCSI fix, desktop cleanup, and LibreWolf winget install

## Phase Details

### Phase 1: Network Restructuring
**Goal**: Strip Section 29 (NIC/Network Tweaks in `Configuration/custom.yml`) down to Vain-only changes. Remove FSOS TCP/IP stack additions (MaxUserPort, DisableBandwidthThrottling, FastSendDatagramThreshold) while keeping Vain NIC driver-layer tweaks, binding trims, TCP timestamps disabled, UDP URO enabled, and RSC enabled.
**Depends on**: Nothing (first phase)
**Requirements**: NET-01, NET-02, NET-03, NET-04, NET-05, NET-06
**Success Criteria** (what must be TRUE):
  1. Section 29 contains only Vain NIC driver-layer tweaks (PnPCapabilities=24, EEE/wake/FlowControl/InterruptModeration/RSS/SelectiveSuspend, checksum offloads, LSOv2, RSC)
  2. The three FSOS TCP/IP stack registry values (MaxUserPort, DisableBandwidthThrottling, FastSendDatagramThreshold) are removed from Section 29
  3. Binding trims (ms_lldp, ms_lltdio, ms_implat, ms_rspndr), TCP timestamps disabled, UDP URO enabled, and RSC enabled remain in Section 29
  4. MMCSS NetworkThrottlingIndex=FFFFFFFF and SystemResponsiveness=0 stay in Section 27 (universal, not FSOS-specific)
  5. The NCSI fix (EnableActiveProbing=1 + netprofm safety-net) in Section 17 remains untouched
**Plans**: 1 plan

Plans:
- [x] 01-01: Remove FSOS TCP/IP stack additions from Section 29

### Phase 2: Feature Audit
**Goal**: Produce a verified feature matrix mapping all 40 sections in custom.yml to their feature toggles, actions, and dependencies. Cross-check all feature toggles between custom.yml and playbook.conf, audit bundled executables and Images.
**Depends on**: Phase 1
**Requirements**: AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04, AUDIT-05
**Success Criteria** (what must be TRUE):
  1. A verified feature matrix table exists mapping all 40 sections to their toggles, actions, and dependencies
  2. All feature toggles in custom.yml match 1:1 with playbook.conf `<Name>` values
  3. Every bundled executable in `Executables/` is referenced by at least one section in custom.yml
  4. Every PNG in `Images/` corresponds to a playbook.conf RadioButtonOption FileName
  5. All feature toggles from CLAUDE.md match the actual playbook.conf options
**Plans**: 1 plan

Plans:
- [x] 02-01: Produce verified feature matrix and audit all assets

### Phase 3: Codebase Restructuring
**Goal**: Decide on modularization approach for the monolithic custom.yml (~1309 lines). Present plan and get user approval before any changes. If approved, create Configuration/sections/ directory and split sections into per-section YAML partials.
**Depends on**: Phase 2
**Requirements**: RESTRUCT-01, RESTRUCT-02, RESTRUCT-03
**Success Criteria** (what must be TRUE):
  1. User has reviewed and approved (or rejected) a modularization plan
  2. If approved: Configuration/sections/ directory exists with per-section YAML partials
  3. If approved: AME Wizard can still load the split structure (approach documented)
  4. custom.yml is updated to reference split files OR remains monolith if user rejected
**Plans**: 1 plan

Plans:
- [x] 03-01: Present modularization plan, get user approval, implement modularization

### Phase 4: Bug Verification
**Goal**: Verify three bug fixes from the August 2026 session: NCSI "Not connected" fix (EnableActiveProbing=1 + netprofm safety-net), Desktop cleanup via registry key delete (clean icon layout on first login), and LibreWolf winget install (winget availability in AME environment).
**Depends on**: Phase 3
**Requirements**: BUG-01, BUG-02, BUG-03
**Success Criteria** (what must be TRUE):
  1. NCSI fix verified: EnableActiveProbing=1 + netprofm safety-net produces "Connected" status in Settings
  2. Desktop cleanup verified: HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop registry key delete produces clean icon layout on first login
  3. LibreWolf winget install verified: winget is present in AME environment and LibreWolf.LibreWolf package installs successfully
  4. All findings documented with pass/fail status and any recommended follow-up
**Plans**: 1 plan

Plans:
- [ ] 04-01: Verify NCSI fix, desktop cleanup, and LibreWolf winget install

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
||-------|----------------|--------|-----------|
|| 1. Network Restructuring | 1/1 | Complete | 2026-08-28 |
|| 2. Feature Audit | 1/1 | Complete | 2026-08-28 |
|| 3. Codebase Restructuring | 1/1 | Complete | 2026-08-28 |
|| 4. Bug Verification | 0/1 | Not started | - |

## Canonical References

### Phase 1 - Network Restructuring
- `Configuration/custom.yml` §SECTION 29 — Current NIC/Network Tweaks section (lines 1165-1184)
- `Configuration/custom.yml` §SECTION 17 — Services safety-net + NCSI fix (lines 606-611)
- `Configuration/custom.yml` §SECTION 25 — MMCSS block with NetworkThrottlingIndex/SystemResponsiveness (lines 873-876)
- `CLAUDE.md` §Planned future change — Network section — Full plan for Section 29 Vain-only stripping
- `docs/reference/planning-artifacts.md` — Async-job manifest format (if needed for external verification)

### Phase 2 - Feature Audit
- `Configuration/custom.yml` — Full playbook (40 sections, 1309 lines)
- `playbook.conf` — AME Wizard UI config with feature toggles
- `Executables/` — All bundled scripts, binaries, and assets
- `Images/` — Browser picker images
- `CLAUDE.md` §Feature toggles — Feature toggles list for cross-checking

### Phase 3 - Codebase Restructuring
- `CLAUDE.md` §Key Decisions — Modularization decision (Pending, revisiting)
- `.planning/codebase/ARCHITECTURE.md` — Current monolithic architecture
- `.planning/codebase/STRUCTURE.md` — Directory layout and naming conventions
- `CLAUDE.md` Constraint — "User must present a full plan and get approval before editing any file"

### Phase 4 - Bug Verification
- `CLAUDE.md` §NCSI "Not connected" cosmetic fix — Current fix in place
- `CLAUDE.md` §Desktop cleanup — Registry key delete approach
- `CLAUDE.md` §Browser section — LibreWolf via winget fix
- `CLAUDE.md` §Log analysis findings — Benign error classification
- `.planning/codebase/TESTING.md` — Manual verification checklist

---
*Last updated: 2026-08-28*