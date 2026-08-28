# Technology Stack

**Analysis Date:** 2026-08-28

## Languages

**Primary:**
- YAML (AME Wizard action format) - Main playbook logic in `Configuration/custom.yml`
- XML (AME Wizard UI config) - Feature pages and options in `playbook.conf`
- PowerShell 5.1+ - System modification scripts in `Executables/` and inline in YAML
- C# - `Executables/settimerresolutionservice.cs` (compiled to Windows service)

**Secondary:**
- Batch/CMD - Inline `!cmd` directives in YAML
- REG - Registry file format (referenced but inlined: `Executables/ControlPanelSettings.reg`)

## Runtime

**Environment:**
- Windows 11 (builds 19044, 19045, 22621, 22631, 26100, 26200)
- AME Wizard (Ameliorated Edition tool) - executes the playbook
- .NET Framework 4.8+ (in-box) - for compiling `settimerresolutionservice.cs`

**Package Manager:**
- winget (Windows Package Manager) - used for LibreWolf browser install
- No npm, Cargo, or other package managers

## Frameworks

**Core:**
- AME Wizard YAML action system - Custom directive format (`!registryValue`, `!service`, `!powerShell`, `!run`, `!cmd`, `!download`, `!appx`, `!file`, `!taskKill`, `!scheduledTask`, `!registryKey`, `!status`)

**Testing:**
- None (no test framework - manual verification via AME Wizard runs)

**Build/Dev:**
- csc.exe (in-box C# compiler) - compiles Timer Resolution service
- Robocopy - file deployment in Section 01

## Key Dependencies

**Critical:**
- AME Wizard - The execution engine that parses and runs the playbook
- Windows built-in tools: `bcdedit`, `powercfg`, `netsh`, `DISM.exe`, `fsutil`, `lodctr`, `winmgmt`, `wevtutil`, `reg`, `sc.exe`, `taskkill`, `label`

**Infrastructure:**
- Microsoft .NET Framework 4.8 (for Timer Resolution service compilation)
- winget (Microsoft.DesktopAppInstaller - kept in AppX allowlist)
- GitHub Releases API - for downloading browser installers (Mercury, Thorium, 7-Zip)

## Configuration

**Environment:**
- No environment variables required at playbook authoring time
- Runtime: `exeDir` context variable in AME Wizard points to `Executables/` folder

**Build:**
- No build configuration files - playbook is interpreted by AME Wizard
- `settimerresolutionservice.cs` compiled at runtime via in-box `csc.exe`

## Platform Requirements

**Development:**
- Windows 10/11 with AME Wizard installed
- Git (for version control)
- Text editor (VS Code recommended for YAML/XML editing)

**Production (Target System):**
- Windows 11 (supported builds listed in playbook.conf)
- Internet connection (for browser downloads, winget, VC++ redist downloads)
- Admin rights (playbook requires elevation for most operations)
- Plugged in (laptop requirement)

---

*Stack analysis: 2026-08-28*
*Update after major AME Wizard version changes or Windows build support changes*