# Architecture

**Analysis Date:** 2026-08-28

## Pattern Overview

**Overall:** Monolithic AME Wizard Playbook - Sequential action list executed by AME Wizard runner

**Key Characteristics:**
- Single YAML action list (`Configuration/custom.yml`) with ~1315 lines, 40 sections
- Declarative directives executed in order by AME Wizard
- Feature-gated sections via `option:` / `option: '!name'` conditions matching `playbook.conf` toggles
- No runtime logic/loops in playbook - all control flow in AME Wizard engine
- Idempotent-ish operations (registry sets, service changes, file copies)
- Side effects applied directly to target Windows system

## Layers

**Playbook Definition Layer:**
- Purpose: Define what changes to make to Windows
- Contains: `Configuration/custom.yml` (actions), `playbook.conf` (UI/feature toggles)
- Location: Root and `Configuration/`
- Depends on: AME Wizard YAML schema
- Used by: AME Wizard runner

**Execution Engine Layer (External):**
- Purpose: Parse YAML, evaluate conditions, execute directives on target system
- Contains: AME Wizard (closed-source tool)
- Location: User's AME Wizard installation
- Depends on: Windows APIs, .NET runtime
- Used by: End user running the playbook

**Bundled Assets Layer:**
- Purpose: Provide files/binaries copied to target system at runtime
- Contains: `Executables/` (scripts, binaries, images), `Images/` (browser picker art)
- Location: `Executables/`, `Images/`
- Depends on: Section 01 robocopy deployment
- Used by: Various sections (DisableDefender.ps1, start2.bin, settimerresolutionservice.cs, profile.png, browser images)

**Post-Install Toolkit Layer:**
- Purpose: User-run scripts for further customization after playbook completes
- Contains: `Executables/Files/AkariOS/Ultimate/` (8 categories, 50+ scripts)
- Location: Deployed to `C:\AkariOS\Ultimate\`
- Depends on: Section 34 deployment
- Used by: End user manually after playbook

## Data Flow

**Playbook Execution (AME Wizard Runtime):**

1. **Initialize** (Section 01): Robocopy `Executables/Files/` → `%SystemDrive%\`, disable Smart App Control
2. **Theme/UI** (Sections 02, 11, 25, 26, 27): Registry tweaks for dark mode, Start menu, Explorer, context menu
3. **Runtime Config** (Sections 03, 04): PowerShell execution policy, NGEN precompile
4. **Notifications** (Section 05): Disable WpnService, toast notifications
5. **Security Features** (Sections 06, 07, 21, 22): Defender, UAC, process mitigations, Spectre/Meltdown
6. **Software/Runtimes** (Section 08): VC++ redists 2005-2022, DirectX Jun2010
7. **Optional Tools** (Section 09): 7-Zip via GitHub releases
8. **Browsers** (Section 10): Download/install selected browsers (winget for LibreWolf)
9. **Windows Features** (Section 13): DISM enable/disable features (DirectPlay, StepsRecorder, etc.)
10. **OneDrive** (Section 14): Full removal if toggled
11. **Edge** (Section 15): Full removal unless user picks "Keep Edge"
12. **AppX Debloat** (Section 16): Explicit allowlist - remove listed packages only
13. **Services** (Section 17): Mass disable telemetry/unneeded services + networking safety-net + NCSI fix
14. **Printing/Bluetooth** (Section 18): Disable if toggled
15. **BCD/FS** (Section 19): Boot config, filesystem tweaks (disablelastaccess, disable8dot3)
16. **Hyper-V/VBS** (Section 20): Disable if toggled (bcdedit, DISM, services)
17. **Privacy/Telemetry** (Section 23): Massive registry block (HKLM/HKCU/HKU/.DEFAULT)
18. **Firewall** (Section 24): Targeted outbound blocks for Search/Cortana/Settings
19. **General Tweaks** (Section 25): MMCSS, timer resolution, GPU scheduling, priority, etc.
20. **Control Panel** (Section 26): Inlined registry from old .reg file + runtime PS blocks
21. **Scheduled Tasks** (Section 28): Disable telemetry/maintenance tasks
22. **Network/NIC** (Section 29): Per-adapter PnPCapabilities=24, binding trims, TCP/UDP tuning
23. **Power Plan** (Section 30): Ultimate Performance plan, delete others, hibernate off
24. **Timer Resolution** (Section 31): Compile/install STR service (1ms timer)
25. **Windows Update** (Section 32): Pause 365 days if toggled
26. **Extra Power Savings** (Section 33): Aggressive powercfg on Ultimate plan
27. **Post-Install Toolkit** (Section 34): Unblock scripts, desktop shortcut
28. **File Associations** (Section 35): SetFileTypeAssociation.ps1
29. **Wallpaper/Lockscreen/Profile** (Section 36): Deploy images, set via COM/WinRT
30. **System Restore** (Section 37): Enable + create "AkariOS" restore point
31. **Perf Counters** (Section 38): lodctr /r, winmgmt /resyncperf
32. **Cleanup** (Section 39): Temp files, event logs (NO vssadmin delete shadows)
33. **Desktop Cleanup** (Section 40): Delete Shell\Bags\1\Desktop key for clean icon layout

**State Management:**
- File-based: All state lives in target system (registry, files, services)
- No persistent in-memory state in playbook
- Each AME Wizard run is independent (but cumulative on target system)
- System Restore point created at end for rollback

## Key Abstractions

**AME Wizard Directives (Custom YAML Tags):**
- `!registryValue` - Set/delete registry value (path, value, type, data, option?)
- `!registryKey` - Create/delete registry key (path, operation)
- `!service` - Change service startup (name, operation, startup, option?)
- `!powerShell` - Run PS command (command, exeDir?, runas?, wait?, option?)
- `!run` - Run executable directly (exe, args, option?)
- `!cmd` - Run cmd command (command, runas?, wait?, option?)
- `!download` - Download file (url: or git:, destination, regex?, overwrite?, option?)
- `!appx` - Remove/clear-cache UWP package (name, type?, unregister?, weight?, option?)
- `!file` - Delete file/folder (path, option?)
- `!taskKill` - Kill process by name (name, ignoreErrors?, option?)
- `!scheduledTask` - Disable/delete task (path, operation, option?)
- `!status` - Progress message (status, option?)

**Feature Toggle System:**
- Defined in `playbook.conf` as `<Name>` values in CheckboxOption/RadioImageOption
- Referenced in `custom.yml` via `option: 'name'` (enable if ON) or `option: '!name'` (enable if OFF)
- Browser picker uses RadioImagePage with `DependsOn` for 2-page flow

**Section Organization:**
- 40 numbered sections with clear headers
- Comments document design decisions and source attribution (Vain, FSOS, WinSux, Atlas, AkariV5)
- Safety-net comments mark intentionally preserved services (System Restore, networking)

## Entry Points

**AME Wizard Playbook Entry:**
- User opens playbook in AME Wizard → selects features → clicks "Run"
- AME Wizard parses `playbook.conf` for UI, `custom.yml` for actions
- Execution is sequential top-to-bottom with conditional gating

**Post-Install Toolkit Entry:**
- User runs scripts manually from `C:\AkariOS\Ultimate\` or desktop shortcut
- 8 categories: Check, Refresh, Setup, Installers, Graphics, Windows, Hardware, Advanced
- Each script independent, targets specific subsystem

## Error Handling

**Strategy:** Best-effort, continue on error
- `ignoreErrors: true` on `!taskKill` and some `!appx` operations
- `errorAction: Ignore` on PowerShell `Remove-AppxPackage` calls
- `-EA 0` (ErrorAction SilentlyContinue) on many PowerShell commands
- `try/catch` blocks in inline PowerShell for critical sections
- AME Wizard logs all errors to `Log.yml` and `Output.txt`

**Patterns:**
- Services: Change startup type, then stop (order matters)
- Registry: Set value, overwrite if exists (idempotent)
- Files: Delete with `-Force -EA 0` (ignore missing)
- Downloads: `overwrite: true` for idempotency
- Networking safety-net: Restore critical services to auto-start after mass disable

## Cross-Cutting Concerns

**Feature Gating:**
- Every optional action has `option: 'toggle-name'` or `option: '!toggle-name'`
- Browser picker: mutual exclusion via `!browser-edge` gate on Edge removal
- All toggles default to `IsChecked="false"` in playbook.conf (opt-in)

**Safety Nets:**
- System Restore: VSS/swprv/volsnap/sdrsvc/wbengine/SystemRestore NOT disabled
- WinRE: `recoveryenabled no` omitted, hibernation off but WinRE on
- Networking: `iphlpsvc`, `tcpipreg`, `Dnscache`, `NlaSvc`, `netprofm` restored to auto (2)
- Restore point created at end (Section 37)

**Attribution/Provenance:**
- Comments cite sources: Vain, FSOS (FrostySecOS), WinSux, Atlas OS, AkariV5
- Design decisions documented in header (Section 0)
- "Atlas gap" markers for additions from Atlas OS comparison

---

*Architecture analysis: 2026-08-28*
*Update when major patterns change or new directive types added*