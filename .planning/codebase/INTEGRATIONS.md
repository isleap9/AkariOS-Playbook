# External Integrations

**Analysis Date:** 2026-08-28

## APIs & External Services

**Browser Downloads (GitHub Releases API):**
- Mercury Browser - `https://github.com/Alex313031/Mercury` - AVX2 Win64 installer
  - Regex: `^mercury.*win64.*AVX2.*.exe$`
  - Auth: None (public releases)
- Thorium Browser - `https://github.com/Alex313031/Thorium-Win` - AVX2 mini installer
  - Regex: `^thorium_AVX2_mini_installer\.exe$`
  - Auth: None (public releases)
- 7-Zip - `https://github.com/ip7z/7zip` - x64 installer
  - Regex: `^7z.*-x64\.exe$`
  - Auth: None (public releases)

**Direct Download URLs:**
- Brave Browser - `https://laptop-updates.brave.com/latest/winx64` - Latest x64 installer
- Firefox - `https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US` - Latest Win64 EN-US
- Chrome - `https://dl.google.com/dl/chrome/install/googlechromestandaloneenterprise64.msi` - Enterprise MSI
- VC++ 2005 - Microsoft Download Center (fixed URLs)
- VC++ 2008 - Microsoft Download Center (fixed URLs)
- VC++ 2010 - Microsoft Download Center (fixed URLs)
- VC++ 2012 - Microsoft Download Center (fixed URLs)
- VC++ 2013 - Microsoft aka.ms redirect (fixed URLs)
- VC++ 2015-2022 - `https://aka.ms/vs/17/release/vc_redist.x86.exe` and `.x64.exe`
- DirectX Jun2010 - Microsoft Download Center (fixed URL)

**Package Manager:**
- winget (Windows Package Manager) - Used for LibreWolf install
  - Package ID: `LibreWolf.LibreWolf`
  - Source: winget default source (Microsoft Community Repository)
  - Auth: `--accept-package-agreements --accept-source-agreements` flags

## Data Storage

**Databases:**
- None (playbook is stateless, modifies target system registry/files directly)

**File Storage:**
- `C:\AkariOS\Ultimate\` - Post-install toolkit scripts (copied from `Executables/Files/AkariOS/Ultimate/`)
- `C:\Windows\Web\AkariOS\` - Wallpaper/lockscreen images (copied from `Executables/Files/Windows/Web/AkariOS/`)
- `C:\Windows\SetTimerResolutionService.exe` - Compiled timer resolution service
- `Executables/start2.bin` - Start menu pin layout binary (deployed to StartMenuExperienceHost LocalState)

**Caching:**
- `%temp%` - Temporary downloads (VC++ redists, DirectX, browser installers)
- AME Wizard handles its own caching

## Authentication & Identity

**Auth Provider:**
- None (playbook runs with elevated privileges on target machine)

**OAuth Integrations:**
- None

## Monitoring & Observability

**Error Tracking:**
- None built-in
- AME Wizard provides its own logging (`Log.yml`, `Output.txt`)

**Analytics:**
- None (playbook explicitly disables telemetry)

**Logs:**
- AME Wizard generates `Log.yml` and `Output.txt` in playbook directory
- Windows Event Logs cleared in Section 39 (`wevtutil cl`)

## CI/CD & Deployment

**Hosting:**
- GitHub Repository: `https://github.com/isleap9/AkariOS-Playbook`
- Playbook distributed as `.apbx` package (AME Wizard format)

**CI Pipeline:**
- None (manual releases)

## Environment Configuration

**Development:**
- AME Wizard installed
- Playbook source in `C:\Users\isleap\Desktop\playbooks\AkariOSV6.1\` (original location)
- Git repo at `C:\Users\isleap.AKARIOS\Documents\GitHub\AkariOS-Playbook\`

**Staging:**
- Test VM with target Windows 11 build
- AME Wizard runs playbook against VM

**Production:**
- End-user runs AME Wizard with playbook on their Windows 11 system
- Requires: Internet, Admin rights, Plugged in (laptop)

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

---

*Integration audit: 2026-08-28*
*Update when adding/removing browser download sources or external dependencies*