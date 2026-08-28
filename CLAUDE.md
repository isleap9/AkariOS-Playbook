# AkariOS V6 — Project Memory for Claude

This file captures everything done in the Claude Cowork session (August 2026) so future Claude sessions can pick up without re-explaining context.

---

## What AkariOS is

A custom Windows 11 AME (Ameliorated Edition) playbook built with the AME Wizard tool. It debloats, hardens privacy, and tunes performance. The playbook runs as a YAML action list (`custom.yml`) paired with a UI configuration (`playbook.conf`). Everything lives in `C:\Users\isleap\Desktop\playbooks\AkariOSV6.1\`.

**Key rule from the user:** Always present a full plan and get approval before editing any file.

---

## Directory structure

```
AkariOSV6.1/
├── playbook.conf          ← AME UI config (XML): feature pages, options, description
├── playbook.png           ← Playbook thumbnail shown in AME Wizard
├── CLAUDE.md              ← This file
├── Configuration/
│   └── custom.yml         ← Main action list (~1315 lines, 40 sections)
├── Executables/           ← Bundled scripts/binaries copied to system at runtime
│   ├── DisableDefender.ps1
│   ├── start2.bin         ← Windows 11 Start menu pin layout binary
│   ├── settimerresolutionservice.cs
│   ├── SetFileTypeAssociation.ps1
│   ├── profile.png        ← Used by wallpaper/profile setup
│   └── NoDefender.cab     ← Used indirectly by DisableDefender.ps1
└── Images/                ← Browser picker images (mercury.png, thorium.png, etc.)
    └── librewolf.png      ← User renamed an existing file to this
```

> `ControlPanelSettings.reg` is referenced in old notes but is a dead reference — kept for historical context only.

---

## AME YAML syntax reminders

| Directive | Purpose |
|---|---|
| `!registryValue` | Set/delete a registry value |
| `!registryKey` | Create/delete a registry key |
| `!service` | Change service startup (`startup: 4` = disabled, `startup: 2` = automatic) |
| `!powerShell` | Run PowerShell (use `runas: currentUserElevated` for elevated) |
| `!run` | Run an executable directly |
| `!cmd` | Run a cmd command |
| `!download` | Download a file; `git:` pulls latest GitHub release, `url:` is direct |
| `!appx` | Remove/clear-cache UWP package |
| `!file` | Delete a file or folder |
| `!taskKill` | Kill a process by name |
| `option: 'name'` | Gates action on feature toggle being ON |
| `option: '!name'` | Gates action on feature toggle being OFF |

---

## Feature toggles (must match `playbook.conf` `<Name>` values)

```
disable-defender            disable-uac
disable-process-mitigations disable-spectre-meltdown
enable-dark-mode            legacy-context-menu
remove-uwp-photos           disable-print
disable-bluetooth           disable-wu
disable-powersave           remove-onedrive
disable-hyperv              disable-memory-compression
7zip

Browser picker (RadioImagePage):
  browser-mercury   browser-thorium    browser-brave
  browser-librewolf browser-firefox    browser-chrome    browser-edge

Note: browser-edge = KEEP Edge. Any other browser choice triggers Edge removal
      via !browser-edge gate (Section 15).
```

---

## Everything changed in the August 2026 session

### 1. Atlas OS gap additions (Section 17 / Section 23 area)

Added services missing from Atlas OS comparison:
```yaml
- !service: {name: 'ose', operation: change, startup: 4}           # Office Source Engine
- !service: {name: 'osppsvc', operation: change, startup: 4}       # Office Software Protection Platform
- !service: {name: 'ClickToRunSvc', operation: change, startup: 4} # Office Click-to-Run
```

Added registry tweaks missing from Atlas OS:
```yaml
# Store auto-downloads
- !registryValue: {path: 'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsStore\WindowsUpdate', value: 'AutoDownload', type: REG_DWORD, data: '2'}
# Settings banners / ContentDelivery
- !registryValue: {path: 'HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager', value: 'SubscribedContent-338393Enabled', type: REG_DWORD, data: '0'}
- !registryValue: {path: 'HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager', value: 'SubscribedContent-353694Enabled', type: REG_DWORD, data: '0'}
- !registryValue: {path: 'HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager', value: 'SubscribedContent-353696Enabled', type: REG_DWORD, data: '0'}
# Network Location Wizard suppress
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Control\Network\NewNetworkWindowOff', value: '', type: REG_SZ, data: ''}
# LSA anonymous restrictions
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Control\Lsa', value: 'RestrictAnonymous', type: REG_DWORD, data: '1'}
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Control\Lsa', value: 'RestrictAnonymousSAM', type: REG_DWORD, data: '1'}
```

### 2. AppX section — preserved Photos, Music, Snipping Tool

User explicitly wants these kept (they are useful defaults):
- `Microsoft.Windows.Photos` — removed both occurrences (one was gated on `remove-uwp-photos`, one was unconditional)
- `Microsoft.ZuneMusic` — removed
- `Microsoft.ScreenSketch` / Snipping Tool — removed

The `remove-uwp-photos` toggle now only controls the Legacy Photo Viewer registry entries in Section 12. The UWP Photos app itself is always kept.

### 3. Browser section — replaced Firefox Developer with LibreWolf

**Why:** Firefox Developer Edition was removed; LibreWolf replaces it.

**Critical bug found and fixed:** `librewolf-community/browser-windows` GitHub repo returns 404 — it no longer exists. LibreWolf moved Windows builds to `dl.librewolf.net` (not GitHub releases). AME's `git:` directive cannot work with it.

**Fix applied:** Replaced the broken `!download` + `!cmd` with a single `winget` install:
```yaml
- !status: {status: 'Installing LibreWolf', option: 'browser-librewolf'}
- !run: {exe: 'winget', args: 'install -e --id LibreWolf.LibreWolf --silent --accept-package-agreements --accept-source-agreements', runas: currentUserElevated, option: 'browser-librewolf'}
```
This always pulls the latest LibreWolf via winget, no URL maintenance needed.

`librewolf.png` must exist in the `Images/` folder (user confirmed it does — renamed from another file).

### 4. playbook.conf restructure

Full rewrite with these changes:
- **Description updated** to: `"AkariOS strips Windows 11 down to its essentials — removing telemetry, disabling unnecessary services, hardening privacy, and tuning the system for peak gaming and daily-use performance. Every change is deliberate, documented, and reversible where it matters."`
- **Browser CheckboxPage + 2 RadioImagePages moved to FIRST position** in FeaturePages
- **All `IsChecked="true"` → `IsChecked="false"`** — every option unticked by default; user chooses what they want
- **LibreWolf replaces Firefox Developer** on page 2 of browser picker; `DefaultOption` changed to `browser-librewolf`
- **Hyper-V option** gained a disclaimer description:
  ```xml
  <Description>⚠️ Some anti-cheats (Valorant, PUBG, etc.) require Hyper-V/VBS. Only disable if you don't play games that enforce them.</Description>
  ```
- **Last page description** changed from `"Untick what you would like to keep."` → `"Tick what you would like to disable."`

### 5. System tray icons — reverted to Windows default

The old playbook had a PowerShell block that showed all tray icons. This was removed — Windows default behavior is better (user controls what's visible). The PS block is gone entirely from Section 40.

### 6. Desktop cleanup — registry key delete approach

**What failed:** A `SendMessage` PowerShell approach using `FindWindow("Progman")` + `FindWindowEx` for SHELLDLL_DefView returned null during playbook execution (Explorer's window hierarchy isn't live at that point in the AME runner).

**What works instead (now in place):**
```yaml
- !registryKey: {path: 'HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop', operation: delete}
```
Deleting this key wipes stored icon positions. On first login, Windows resets to a clean default layout. Does not require Explorer to be running at apply-time.

### 7. NCSI "Not connected" cosmetic fix

**Problem:** Settings showed "Not connected / Offline" even though internet works fine. Caused by:
- `netprofm` (Network List Service) not in the networking safety-net — `NlaSvc` depends on it
- NCSI active probing not explicitly enabled

**Fix applied:**
- Added `netprofm=2` to the existing safety-net hashtable (line ~607)
- Added registry key to enable NCSI probing:
```yaml
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet', value: 'EnableActiveProbing', type: REG_DWORD, data: '1'}
```

### 8. start2.bin explained

`start2.bin` is deployed to the `StartMenuExperienceHost` LocalState folder. It is the Windows 11 Start menu **pin layout binary** — it pre-pins specific app tiles so users get a clean, curated Start menu on first boot instead of Microsoft's default bloated layout. It does **not** affect the system tray.

---

## Log analysis findings (from actual AkariOS V6 run)

From `Log.yml` + `Output.txt` uploaded by the user:

| Error | Type | Verdict |
|---|---|---|
| LibreWolf 404 from `librewolf-community/browser-windows` | Critical | **Fixed** (winget now) |
| Error 1392 during appx removal | Benign | AME file-path cleanup artifact, harmless |
| ActivationStore.dat in-use | Benign | Windows holds handles on packages being removed, AME retries |
| "pris" folder access denied (SystemApps) | Benign | Protected system path, AME skips gracefully |
| "Could not get app executable location" | Benign | Package already removed before location query |
| ScheduledTask Compatibility Appraiser / ProgramDataUpdater fail | Benign | Tasks may not exist on all builds |

Installation completed and worked correctly despite those logged errors.

---

## Reference: old playbook location

`C:\Users\isleap\Desktop\playbooks\AkariOS-Playbook\` — the original AkariOS playbook (read-only reference). Used to cross-check approaches for desktop cleanup and FinalTasks. **Do not edit this folder.**

---

## What's pending / watch out for

- **Desktop cleanup** (registry key delete) — verify it produces a clean layout on next real run. The fix is in place but not yet confirmed on a fresh boot.
- **NCSI fix** — verify "Not connected" is gone after next full playbook run.
- **LibreWolf via winget** — verify winget is present in the AME environment (it should be; `Microsoft.DesktopAppInstaller` is in the appx keep-list).
- **custom.yml is ~1315 lines** — considered modularizing but decided against it for now (user said "i was just asking"). Keep as monolithic unless it grows significantly larger.

---

## Planned future change — Network section (approved by user)

**Goal:** Strip Section 29 down to Vain-only network tweaks. Remove FSOS network additions.

**Why:** Vain operates at the NIC driver layer (hardware-level latency reduction) and is the most impactful for gaming. FSOS network tweaks operate at the TCP/IP stack layer and are more relevant for throughput than gaming latency. They don't conflict, but keeping only Vain makes the section cleaner and more purposeful.

**What to KEEP (Vain):**
- Per-adapter NIC PowerShell block: `PnPCapabilities=24`, disable EEE/wake/FlowControl/InterruptModeration/RSS/SelectiveSuspend, enable checksum offloads (value=3), LSOv2, RSC
- Binding trims: disable `ms_lldp`, `ms_lltdio`, `ms_implat`, `ms_rspndr`
- TCP timestamps disabled (`netsh int tcp set global timestamps=disabled`)
- UDP URO enabled (`netsh int udp set global uro=enabled`)
- RSC enabled (`Set-NetOffloadGlobalSetting -ReceiveSegmentCoalescing Enable`)

**What to REMOVE (FSOS):**
```yaml
# Remove these three lines from Section 29:
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', value: 'MaxUserPort', ...}
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters', value: 'DisableBandwidthThrottling', ...}
- !registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Services\AFD\Parameters', value: 'FastSendDatagramThreshold', ...}
```

**What stays regardless (universal, not FSOS-specific):**
- `NetworkThrottlingIndex = FFFFFFFF` and `SystemResponsiveness = 0` in the MMCSS block (Section 27) — these are universally recommended and unrelated to FSOS. Do NOT remove them.
- NCSI fix block (Section 17 safety-net area) — unrelated to network performance tweaks.

**Do NOT add (AtlasOS-specific, explicitly rejected):**
- `TcpNoDelay` / `TCPAckFrequency` — disables Nagle's algorithm, hurts non-gaming throughput.
