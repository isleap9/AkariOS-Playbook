# Codebase Structure

**Analysis Date:** 2026-08-28

## Directory Layout

```
AkariOS-Playbook/
├── .git/                       # Git repository
├── .planning/                  # GSD planning artifacts (created during mapping)
│   └── codebase/               # Codebase mapping documents
├── Configuration/              # Playbook action definitions
│   └── custom.yml              # Main action list (~1315 lines, 40 sections)
├── Executables/                # Bundled scripts/binaries deployed to target system
│   ├── ControlPanelSettings.reg # Legacy .reg file (reference only, inlined in custom.yml)
│   ├── DisableDefender.ps1     # AkariV5 Defender disable script
│   ├── EnableDefender.ps1      # Restoration script for Defender
│   ├── profile.png             # User profile picture source
│   ├── SetFileTypeAssociation.ps1 # File association helper (SFTA)
│   ├── settimerresolutionservice.cs # C# source for Timer Resolution service
│   ├── start2.bin              # Start menu pin layout binary (empty Win11 layout)
│   ├── NoDefender.cab          # Used by DisableDefender.ps1
│   └── Files/                  # Content tree copied to target system (Section 01 robocopy)
│       ├── AkariOS/
│       │   └── Ultimate/       # Post-install toolkit (50+ scripts in 8 categories)
│       │       ├── 1 Check/           # Hardware checks (Space, RAM, GPU, BIOS, CPU, GPU tests)
│       │       ├── 2 Refresh/         # Factory reset, local account, reinstall, Autounattend
│       │       ├── 3 Setup/           # BitLocker, Memory Compression, Home→Pro, Keys, Activation
│       │       ├── 4 Installers/      # MSI Afterburner, Nvidia Profile Inspector, etc.
│       │       ├── 5 Graphics/        # DDU, Nvidia/AMD/Intel settings, HDCP, P0 State, MSI Mode
│       │       ├── 6 Windows/         # Start menu, taskbar, gaming, bloatware, Edge, Notepad
│       │       ├── 7 Hardware/        # Scaling, polling rate, controller, monitor, network
│       │       └── 8 Advanced/        # Defender, Firewall, Spectre, DEP, MMAgent, ReBar, etc.
│       └── Windows/
│           ├── NoDefender.cab          # Duplicate (also at Executables/)
│           └── Web/
│               └── AkariOS/
│                   └── img0.png        # Wallpaper/lockscreen image
├── Images/                     # Browser picker images for playbook.conf
│   ├── brave.png
│   ├── chrome.png
│   ├── edge.png
│   ├── firefox.png
│   ├── librewolf.png
│   ├── mercury.png
│   ├── next.png
│   └── thorium.png
├── AkariOS-Playbook.apbx       # Compiled AME Wizard playbook package (binary)
├── CLAUDE.md                   # Project memory for Claude sessions
├── playbook.conf               # AME Wizard UI config (XML): feature pages, options
├── playbook.png                # Playbook thumbnail for AME Wizard
└── README.md                   # User-facing documentation
```

## Directory Purposes

**Configuration/**
- Purpose: Playbook logic - the action list executed by AME Wizard
- Contains: `custom.yml` (YAML with AME directives)
- Key files: `custom.yml` - 40 sections, ~1315 lines
- Subdirectories: None

**Executables/**
- Purpose: Runtime assets copied to target system during playbook execution
- Contains: PowerShell scripts, C# source, binary blobs, images, registry files
- Key files: 
  - `DisableDefender.ps1` - Core Defender disable logic (Section 06)
  - `EnableDefender.ps1` - User-run restoration script
  - `settimerresolutionservice.cs` - Compiled to service in Section 31
  - `start2.bin` - Deployed to StartMenuExperienceHost LocalState (Section 26)
  - `SetFileTypeAssociation.ps1` - File associations (Section 35)
  - `profile.png` - Profile picture source (Section 36)
  - `NoDefender.cab` - Used by DisableDefender.ps1
  - `ControlPanelSettings.reg` - Legacy reference (inlined in Section 26)
- Subdirectories:
  - `Files/AkariOS/Ultimate/` - Post-install toolkit (8 categories, 50+ scripts)
  - `Files/Windows/Web/AkariOS/` - Wallpaper image

**Images/**
- Purpose: Browser picker artwork for playbook.conf RadioImagePage options
- Contains: PNG files matching `FileName` values in playbook.conf
- Key files: `mercury.png`, `thorium.png`, `brave.png`, `librewolf.png`, `firefox.png`, `chrome.png`, `edge.png`, `next.png`
- Subdirectories: None

**Root/**
- Purpose: Playbook metadata, packaging, documentation
- Key files:
  - `playbook.conf` - AME Wizard UI configuration (XML)
  - `playbook.png` - Thumbnail shown in AME Wizard
  - `AkariOS-Playbook.apbx` - Compiled package for distribution
  - `CLAUDE.md` - AI assistant context/memory
  - `README.md` - User documentation
  - `.gitattributes` - Git LFS/config for binary files

## Key File Locations

**Entry Points:**
- `Configuration/custom.yml` - Main action list (AME Wizard executes this)
- `playbook.conf` - UI definition (AME Wizard reads this for feature toggles)

**Configuration:**
- `playbook.conf` - Feature toggles, browser picker, descriptions
- `Configuration/custom.yml` - All system modifications

**Core Logic (in custom.yml sections):**
- Sections 01-05: Initialize, Theme, PowerShell, NGEN, Notifications
- Sections 06-07: Defender, UAC (security toggles)
- Section 08: VC++ Redists + DirectX (runtimes)
- Section 09: 7-Zip (optional tool)
- Section 10: Browsers (7 options, 2-page picker)
- Section 11: Start Menu/Search
- Section 12: Legacy Notepad + Photo Viewer
- Section 13: Windows Features (DISM)
- Section 14: OneDrive removal
- Section 15: Edge removal (gated on !browser-edge)
- Section 16: AppX Debloat (explicit allowlist)
- Section 17: Services (mass disable + safety-net)
- Section 18: Printing + Bluetooth
- Section 19: BCDEDIT + Filesystem
- Section 20: Hyper-V/VBS
- Section 21: Process Mitigations
- Section 22: Spectre/Meltdown
- Section 23: Privacy/Telemetry (massive registry block)
- Section 24: Firewall (targeted blocks)
- Section 25: General Tweaks (MMCSS, GPU scheduling, etc.)
- Section 26: Control Panel Settings (inlined from .reg)
- Section 27: Legacy Context Menu
- Section 28: Scheduled Tasks
- Section 29: NIC/Network Tweaks
- Section 30: Power Plan (Ultimate Performance)
- Section 31: Timer Resolution Service
- Section 32: Windows Update Pause
- Section 33: Extra Power Savings
- Section 34: Post-Install Toolkit Deployment
- Section 35: File Associations
- Section 36: Wallpaper/Lockscreen/Profile
- Section 37: System Restore (safety net)
- Section 38: Perf Counters Rebuild
- Section 39: Cleanup
- Section 40: Desktop Cleanup + End

**Testing:**
- None (manual verification via AME Wizard runs on test VMs)

**Documentation:**
- `README.md` - User-facing overview
- `CLAUDE.md` - AI assistant project memory
- `Executables/Files/AkariOS/Ultimate/README.md` - Toolkit documentation
- `Executables/Files/AkariOS/Ultimate/LICENSE` - Toolkit license

## Naming Conventions

**Files:**
- `custom.yml` - Main playbook (lowercase, descriptive)
- `playbook.conf` - AME Wizard config (lowercase, standard name)
- `playbook.png` - Thumbnail (lowercase, standard name)
- `AkariOS-Playbook.apbx` - Package (PascalCase project name + hyphen + type)
- `CLAUDE.md` - AI context (UPPERCASE, standard)
- `README.md` - Documentation (UPPERCASE, standard)
- `.gitattributes` - Git config (dotfile, lowercase)
- PowerShell scripts: `PascalCase.ps1` or `Descriptive Name.ps1` (spaces allowed)
- C# source: `lowercase.cs` (settimerresolutionservice.cs)
- Binary: `lowercase.bin` (start2.bin)
- Images: `lowercase.png` (browser names + next.png)

**Directories:**
- `Configuration/` - PascalCase, singular
- `Executables/` - PascalCase, plural
- `Images/` - PascalCase, plural
- `Files/AkariOS/Ultimate/` - PascalCase project, PascalCase tier
- Category folders: `N Description/` (number + space + title)
- Script files: `N Description.ps1` (number + space + title)

**Special Patterns:**
- Section comments in custom.yml: `# ==========================================================================`
- Section headers: `# SECTION NN - NAME`
- Feature toggles: kebab-case (e.g., `disable-defender`, `browser-librewolf`)
- AME directives: `!directiveName` (bang prefix, camelCase)

## Where to Add New Code

**New Playbook Section:**
- Primary code: `Configuration/custom.yml` (append new section with header comment)
- Feature toggle (if needed): `playbook.conf` (add CheckboxOption/RadioImageOption)
- Assets (if needed): `Executables/` or `Images/` (add file, reference in custom.yml)

**New Post-Install Script:**
- Implementation: `Executables/Files/AkariOS/Ultimate/{Category}/N Name.ps1`
- Category: Choose existing (1-8) or create new numbered category
- Numbering: Next available number in category
- Documentation: Update `Executables/Files/AkariOS/Ultimate/README.md`

**New Browser Option:**
- Add image: `Images/{browser}.png`
- Add RadioImageOption: `playbook.conf` (in appropriate RadioImagePage)
- Add install actions: `Configuration/custom.yml` Section 10 (with `option: 'browser-{name}'`)
- Add Edge removal gate: `option: '!browser-{name}'` if not Edge

**New Feature Toggle:**
- Add CheckboxOption: `playbook.conf` (in appropriate CheckboxPage)
- Gate actions: `Configuration/custom.yml` with `option: 'toggle-name'`

**New Bundled Asset:**
- Script/binary: `Executables/` (copied by Section 01 robocopy)
- Image: `Images/` (referenced by playbook.conf FileName)
- Toolkit script: `Executables/Files/AkariOS/Ultimate/{Category}/`

## Special Directories

**Executables/Files/**
- Purpose: Content tree robocopied to `%SystemDrive%\` in Section 01
- Source: This directory in playbook source
- Destination: `C:\` on target system (creates `C:\AkariOS\`, `C:\Windows\Web\AkariOS\`, etc.)
- Committed: Yes (source of truth)

**Executables/Files/AkariOS/Ultimate/**
- Purpose: Post-install toolkit for end users
- Source: Committed in repo
- Destination: `C:\AkariOS\Ultimate\` on target system
- Committed: Yes (source of truth)
- User access: Desktop shortcut "AkariOS Toolkit" created in Section 34

**.planning/**
- Purpose: GSD planning artifacts (this mapping, requirements, roadmap)
- Source: Generated by GSD workflows
- Committed: Yes (if `commit_docs: true` in config)
- Not part of playbook distribution

---

*Structure analysis: 2026-08-28*
*Update when directory structure changes or new asset categories added*