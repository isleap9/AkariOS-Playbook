# Requirements: AkariOS V6.1

**Defined:** 2026-08-28
**Core Value:** Every system modification is deliberate, documented, and reversible where it matters — AkariOS must reliably strip Windows 11 down to gaming + daily-use essentials without breaking core functionality.

## v1 Requirements

### Network Restructuring

- [ ] **NET-01**: Strip Section 29 to Vain-only network tweaks — remove FSOS TCP/IP stack additions (MaxUserPort, DisableBandwidthThrottling, FastSendDatagramThreshold)
- [ ] **NET-02**: Keep Vain NIC driver-layer tweaks in Section 29 (PnPCapabilities, EEE/wake/FlowControl/InterruptModeration/RSS/SelectiveSuspend, checksum offloads, LSOv2, RSC)
- [ ] **NET-03**: Keep binding trims in Section 29 (ms_lldp, ms_lltdio, ms_implat, ms_rspndr)
- [ ] **NET-04**: Keep TCP timestamps disabled and UDP URO enabled in Section 29
- [ ] **NET-05**: Keep RSC enabled via Set-NetOffloadGlobalSetting in Section 29
- [ ] **NET-06**: Keep MMCSS NetworkThrottlingIndex=FFFFFFFF and SystemResponsiveness=0 in Section 27 (universal, not FSOS-specific)

### Feature Audit

- [ ] **AUDIT-01**: Produce a verified feature matrix mapping all 40 sections in custom.yml to their feature toggles, actions, and dependencies
- [ ] **AUDIT-02**: Cross-check all feature toggles in custom.yml against playbook.conf `<Name>` values — confirm 1:1 match
- [ ] **AUDIT-03**: Audit all bundled executables in Executables/ — verify each is referenced by at least one section in custom.yml
- [ ] **AUDIT-04**: Audit Images/ directory — verify each PNG corresponds to a playbook.conf RadioButtonOption
- [ ] **AUDIT-05**: Verify all feature toggles from CLAUDE.md ("Feature toggles" list) match the actual playbook.conf options

### Codebase Restructuring

- [ ] **RESTRUCT-01**: Decide on modularization approach for the monolithic custom.yml (~1309 lines) — present plan and get user approval
- [ ] **RESTRUCT-02**: If modularized, create Configuration/sections/ directory and split sections 01-41 into per-section YAML partials
- [ ] **RESTRUCT-03**: If modularized, ensure AME Wizard can still load the split structure (document the approach)

### Bug Verification

- [ ] **BUG-01**: Verify the NCSI fix works — EnableActiveProbing=1 + netprofm safety-net produces "Connected" status
- [ ] **BUG-02**: Verify Desktop cleanup via registry key delete produces clean icon layout on first login
- [ ] **BUG-03**: Verify LibreWolf winget install works in AME environment (winget availability)

## v2 Requirements

Deferred to future releases. Tracked but not in current roadmap.

### Future Enhancements
- **FUT-01**: Add automatic version tracking of bundled third-party tools (winget packages, scripts)
- **FUT-02**: Add checksum verification for downloaded binaries
- **FUT-03**: Add rollback/restore functionality verification in real AME runs

## Out of Scope

| Feature | Reason |
|---------|--------|
| Building a GUI installer | AME Wizard is the installer; AkariOS is a playbook, not an application |
| Adding new feature toggles beyond user requests | Scope discipline — only restructure + audit what exists |
| Supporting Windows 10 or Insider builds | Only Windows 11 builds listed in SupportedBuilds |
| Real-time test execution | Requires physical/virtual Windows 11 test environment; out of scope for planning |
| TcpNoDelay / TCPAckFrequency | Disables Nagle's algorithm, hurts non-gaming throughput; explicitly rejected |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| NET-01 | Phase 1 | Pending |
| NET-02 | Phase 1 | Pending |
| NET-03 | Phase 1 | Pending |
| NET-04 | Phase 1 | Pending |
| NET-05 | Phase 1 | Pending |
| NET-06 | Phase 1 | Pending |
| AUDIT-01 | Phase 2 | Pending |
| AUDIT-02 | Phase 2 | Pending |
| AUDIT-03 | Phase 2 | Pending |
| AUDIT-04 | Phase 2 | Pending |
| AUDIT-05 | Phase 2 | Pending |
| RESTRUCT-01 | Phase 3 | Pending |
| RESTRUCT-02 | Phase 3 | Pending |
| RESTRUCT-03 | Phase 3 | Pending |
| BUG-01 | Phase 4 | Pending |
| BUG-02 | Phase 4 | Pending |
| BUG-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0 ✓

---
*Requirements defined: 2026-08-28*
*Last updated: 2026-08-28 after initial definition*