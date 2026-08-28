# Phase 1: Network Restructuring - Context

**Gathered:** 2026-08-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Strip Section 29 ("NIC / NETWORK TWEAKS") of `Configuration/custom.yml` down to Vain-only changes. Remove the three FSOS (FrostySecOS) TCP/IP stack registry additions while keeping all Vain NIC driver-layer tweaks, binding trims, TCP timestamps, UDP URO, and RSC. No other sections are modified. The monolithic `custom.yml` file structure is preserved (no modularization in this phase).
</domain>

<decisions>
## Implementation Decisions

### Removal scope
- **D-01:** Remove exactly three `!registryValue` directives from Section 29 (lines 1179-1184 of custom.yml):
  1. `MaxUserPort=65534` in `HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters` (comment: "Open full TCP ephemeral port range (FSOS)")
  2. `DisableBandwidthThrottling=1` in `HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters` (comment: "LAN bandwidth throttling off (FSOS)")
  3. `FastSendDatagramThreshold=1500` in `HKLM\SYSTEM\CurrentControlSet\Services\AFD\Parameters` (comment: "UDP datagram send-path optimization (FSOS)")
- **D-02:** Everything else in Section 29 stays as-is — the per-adapter NIC PowerShell block, binding trims (ms_lldp, ms_lltdio, ms_implat, ms_rspndr), TCP timestamps disabled, UDP URO enabled, and RSC enabled via Set-NetOffloadGlobalSetting.

### Comment handling
- **D-03:** Remove the inline `# (FSOS)` comments along with their registryValue directives (they are part of the removed lines). No replacement comments needed — the Section 29 header already documents this is a Vain block.

### IPv6 preservation
- **D-04:** Keep IPv6 enabled (the Section 29 header explicitly notes "IPv6 is intentionally PRESERVED (unlike WinSux)"). The FSOS removals do not touch IPv6, and no new IPv6 changes are introduced.

### Section header update
- **D-05:** Update the Section 29 header comment from "Vain block + WinSux PnPCapabilities=24" to "Vain-only" to reflect that FSOS TCP/IP stack additions have been removed. This aligns with the design decision documented in CLAUDE.md.

### Out-of-scope (no changes)
- **D-06:** Section 17 (Services + NCSI fix) stays untouched — netprofm safety-net and EnableActiveProbing=1 are not network performance tweaks.
- **D-07:** Section 25 (MMCSS) stays untouched — NetworkThrottlingIndex=FFFFFFFF and SystemResponsiveness=0 are universal recommendations, not FSOS-specific.

### Claude's Discretion
- Verification approach in this non-Windows environment
</decisions>

<canonical_refs>
## Canonical References

### Section 29 (current state)
- `Configuration/custom.yml` §SECTION 29 — Current NIC/Network Tweaks section (lines 1165-1184)
- `CLAUDE.md` §Planned future change — Network section — Full plan for Section 29 Vain-only stripping, including exact lines to keep and remove
- `CLAUDE.md` §Key Decisions — "Strip Section 29 to Vain-only" (Approved) and "Keep MMCSS NetworkThrottlingIndex/SystemResponsiveness" (Approved)

### Safety-net / non-FSOS sections
- `Configuration/custom.yml` §SECTION 17 — Services safety-net + NCSI fix (lines 606-611)
- `Configuration/custom.yml` §SECTION 25 — MMCSS block with NetworkThrottlingIndex/SystemResponsiveness (lines 873-876)

### Conventions
- `.planning/codebase/CONVENTIONS.md` — YAML comment style (section headers, source attribution markers)
</canonical_refs>

<specifics>
## Specific Ideas

- User already decided to keep the monolith for now (from August 2026 session: "i was just asking")
- The removal targets are precisely documented in CLAUDE.md's "Planned future change — Network section" subsection
</specifics>

<deferred>
## Deferred Ideas

- Modularizing custom.yml into Configuration/sections/ — Phase 3
- Full verified feature matrix — Phase 2
- Bug verification — Phase 4
</deferred>

---

*Phase: 01-network-restructuring*
*Context gathered: 2026-08-28*
