# AkariOS V6.1

## What This Is

A custom Windows 11 AME (Ameliorated Edition) playbook that debloats, hardens privacy, and tunes performance. Built with the AME Wizard tool and structured as a monolithic YAML action list (`Configuration/custom.yml`, ~1309 lines, 40 sections) paired with an XML UI configuration (`playbook.conf`). The user's goal is to restructure the playbook — specifically stripping Section 29 (network tweaks) down to Vain-only changes and modularizing the monolith — while auditing the current feature set.

## Core Value

The single most important thing is that every system modification is deliberate, documented, and reversible where it matters. AkariOS must reliably strip Windows 11 down to gaming + daily-use essentials without breaking core functionality.

## Business Context

<!-- This is an open-source project, not monetized or customer-facing -->

## Requirements

### Validated

- ✓ Windows 11 support (Builds 19044, 19045, 22621, 22631, 26100, 26200) — confirmed via `playbook.conf` SupportedBuilds
- ✓ Security configuration page with Defender, UAC, Process Mitigations, Spectre/Meltdown toggles — present in sections 6, 7, 21, 22
- ✓ Browser picker with 7 options (Mercury, Thorium, Brave, LibreWolf, Firefox, Chrome, Edge) and Edge removal gate — present in section 10 + playbook.conf pages 1-2
- ✓ LibreWolf installs via winget (fix from August 2026 session) — section 10
- ✓ Post-install toolkit deployed to `C:\AkariOS\Ultimate\` with 8 categories of scripts — section 34
- ✓ Start menu pre-pin layout via `start2.bin` — section 26
- ✓ Desktop cleanup via `HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop` registry key delete — section 39
- ✓ NCSI fix: `EnableActiveProbing=1` + `netprofm` safety-net service — section 17
- ✓ All playbook options default to `IsChecked="false"` (user opt-in) — playbook.conf

### Active

- [ ] Strip Section 29 (network tweaks) to Vain-only — remove FSOS TCP/IP stack additions
- [ ] Audit full feature set against actual `custom.yml` to produce a verified feature matrix
- [ ] [Decision point TBD] Modularize the monolithic `Configuration/custom.yml` into a `Configuration/sections/` directory structure
- [ ] Verify all bundled executables are referenced and correct

### Out of Scope

- Building a GUI installer — AME Wizard is the installer
- Adding new feature toggles beyond what the user requests
- Supporting Windows 10 or Insider builds
- Replacing the AME Wizard YAML syntax or directive format

## Context

**Technical environment:** Windows 11 AME (Ameliorated Edition) ecosystem. Playbook runs as YAML action list executed by AME Wizard, with embedded PowerShell scripts, registry edits, service modifications, AppX removal, and binary asset deployment.

**Prior work:** The August 2026 Claude cowork session (documented in `CLAUDE.md`) made several changes: added Atlas OS gap services/registries (Office Source Engine, Store auto-downloads, ContentDelivery bans, Network Location Wizard, LSA anonymous restrictions), replaced Firefox Developer with LibreWolf via winget, restructured `playbook.conf` (browser picker first, all defaults off, Hyper-V disclaimer, updated descriptions), preserved Photos/Music/Snipping Tool in AppX removal, reverted system tray icons to Windows default, switched desktop cleanup to registry-key-delete approach, and fixed the NCSI "Not connected" bug.

**Current state:** The playbook is a single 1309-line `custom.yml` with 40 sections (Section 01 Initialize through Section 41 End). A codebase map exists in `.planning/codebase/`.

**Key insight:** `playbook.conf` comment line 26 says `'akariserv' dropped entirely` and `AKARIOSERV` references were removed from `custom.yml`, but there are inconsistencies: `playbook.conf` has `install-browser` as a CheckboxPage (not reflected in CLAUDE.md's feature toggles list), and the `librewolf` entry in `playbook.conf` comments on line 24 still says `firefoxdev`.

## Constraints

- **Tech stack**: AME Wizard YAML format, no external build tools
- **Compatibility**: Must support all 6 listed Windows 11 builds
- **Reversibility**: Security/privacy changes must be documented as reversible where possible
- **User preference**: User must present a full plan and get approval before editing any file (per CLAUDE.md)
- **Modularity decision pending**: The monolith is ~1309 lines — user asked about modularization but decided against it; this is being revisited

## Key Decisions

| Decision | Rationale | Outcome |
|---|---|---|
| Keep custom.yml monolith for now | User said "i was just asking" when modularization was mentioned in August 2026 session | — Pending (revisiting) |
| Strip Section 29 to Vain-only | Vain operates at NIC driver layer (hardware latency); FSOS TCP/IP stack tweaks are throughput-focused, not gaming-relevant | ✓ Good |
| Keep MMCSS NetworkThrottlingIndex/SystemResponsiveness | Universal recommendations, unrelated to FSOS | ✓ Good |
| Don't add TcpNoDelay/TCPAckFrequency | Disables Nagle's algorithm, hurts non-gaming throughput; AtlasOS-specific, explicitly rejected | ✓ Good |
| LibreWolf via winget | librewolf-community/browser-windows GitHub repo 404s; winget always pulls latest | ✓ Good |
| Desktop cleanup via registry key delete | SendMessage/FindWindow approach fails during AME runner execution | ✓ Good |
| NCSI fix via EnableActiveProbing + netprofm | NlaSvc depends on netprofm; active probing not previously enabled | ✓ Good |
| All defaults IsChecked="false" | User chooses what to disable — no surprises | ✓ Good |
| AppX Photos/Music/Snipping kept | Useful defaults the user wants to retain | ✓ Good |
| Network Location Wizard suppress | Added from Atlas OS gap comparison | ✓ Good |

---
*Last updated: 2026-08-28 after /gsd-new-project initiation (resumed from .planning/codebase/)*