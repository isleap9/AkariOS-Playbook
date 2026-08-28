# Phase 4 Context: Bug Verification

**Gathered:** 2026-08-28
**Status:** Ready for discussion

<domain>
## Phase Boundary

Verify three bug fixes from the August 2026 session by static analysis of the codebase and documentation. Document findings with pass/fail status and recommended follow-up.

**Key constraint:** This is a Windows 11 AME Wizard playbook project. I am running on a Linux/WSL environment without a Windows VM. I CANNOT execute the playbook or verify runtime behavior on a live Windows system. However, I CAN verify that the fixes are correctly implemented in the code via static analysis.
</domain>

## Bugs to Verify

### BUG-01: NCSI "Not connected" cosmetic fix
**CLAUDE.md description:** Settings showed "Not connected / Offline" even though internet works fine. Root causes identified:
- `netprofm` (Network List Service) was not in the networking safety-net — `NlaSvc` depends on it
- NCSI active probing was not explicitly enabled

**Fix in place (Section 17):**
- Line 613: `netprofm=2` added to safety-net hashtable (`@{iphlpsvc=2;tcpipreg=2;Dnscache=2;NlaSvc=2;netprofm=2}`)
- Line 615: `!registryKey: {path: 'HKLM\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet', operation: add}` — creates the key
- Line 616: `!registryValue: {path: 'HKLM\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet', value: 'EnableActiveProbing', type: REG_DWORD, data: '1'}` — enables active probing
- Line 617: `Restart-Service netprofm -Force -EA 0; Restart-Service NlaSvc -Force -EA 0` — restarts both services

**What I can verify:**
- ✅ `netprofm` is in the safety-net hashtable (line 613)
- ✅ `EnableActiveProbing=1` registry value is present (line 616)
- ✅ The `NlaSvc\Parameters\Internet` key is created via `operation: add` (line 615) — important because the key may not exist
- ✅ Services are restarted after the registry change (line 617)
- ✅ `NlaSvc` is in the safety-net (line 613) — ensures NLA service is set to auto

**What I CANNOT verify:**
- ❌ Whether "Not connected" is actually resolved on a live Windows system after running the playbook

### BUG-02: Desktop cleanup via registry key delete
**CLAUDE.md description:** A PowerShell `SendMessage`/`FindWindow` approach failed because Explorer's window hierarchy isn't live at apply-time. Replaced with registry key delete.

**Fix in place (Section 40):**
- Line 1308: Comment: "Desktop icon cleanup: wipe stored icon positions so Windows resets to a clean layout on first login"
- Line 1309: `!registryKey: {path: 'HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop', operation: delete}`
- Line 1310: `!status: {status: 'AkariOS V6 - Done'}`

**What I can verify:**
- ✅ The `SendMessage`/`FindWindow` approach has been removed (no references to `Progman`, `SHELLDLL_DefView`, `FindWindow` in custom.yml)
- ✅ The registry key delete approach is in place (line 1309)
- ✅ The comment documents the design decision (lines 1308)
- ✅ The key path matches the documented approach: `HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop`

**What I CANNOT verify:**
- ❌ Whether Windows actually resets to a clean icon layout on first login (requires live Windows test)
- ❌ Whether the key exists at the time of deletion (but `operation: delete` should handle non-existent key gracefully)

### BUG-03: LibreWolf via winget
**CLAUDE.md description:** The `librewolf-community/browser-windows` GitHub repo returns 404 — it no longer exists. LibreWolf moved Windows builds to `dl.librewolf.net`.

**Fix in place (Section 10):**
- Line 220: `- !status: {status: 'Installing LibreWolf', option: 'browser-librewolf'}`
- Line 221: `- !run: {exe: 'winget', args: 'install -e --id LibreWolf.LibreWolf --silent --accept-package-agreements --accept-source-agreements', runas: currentUserElevated, option: 'browser-librewolf'}`
- Line 370: `Microsoft.DesktopAppInstaller` is in the AppX KEEP list (line 370) — this provides winget

**What I can verify:**
- ✅ The broken `git:` download directive is gone (no references to `librewolf-community/browser-windows` in custom.yml)
- ✅ winget install command uses the correct package ID: `LibreWolf.LibreWolf`
- ✅ Command flags are correct: `--silent`, `--accept-package-agreements`, `--accept-source-agreements`
- ✅ `runas: currentUserElevated` — runs with elevation
- ✅ `Microsoft.DesktopAppInstaller` (winget) is preserved in AppX allowlist (Section 16, line 370)
- ✅ `librewolf.png` exists in `Images/` directory (confirmed in Phase 2 audit)
- ✅ `browser-librewolf` toggle exists in `playbook.conf` (confirmed in Phase 2 audit)
- ✅ Edge removal still works via `!browser-edge` gate (LibreWolf doesn't trigger Edge removal since `browser-edge` is separate)

**What I CANNOT verify:**
- ❌ Whether winget is actually present and functional in the AME environment
- ❌ Whether the `LibreWolf.LibreWolf` winget package ID is still valid
- ❌ Whether the install succeeds end-to-end

**Additional note:** The old approach used `!download {git: '...librewolf-community/browser-windows'}` followed by `!cmd` to run the installer. The new approach uses `!run {exe: 'winget'}` which is simpler and always pulls the latest version. This is a correct and robust fix.

## Verification Approach

Since I cannot run the playbook on a live Windows system, this phase will be a **static verification** — confirming that the fixes are correctly implemented in the code. Each fix will be assessed as:

- **Implementation Status:** VERIFIED (code is present and correct) / NOT FOUND (fix missing) / PARTIAL (fix incomplete)
- **Runtime Status:** UNVERIFIED (requires Windows AME Wizard VM test) / N/A
- **Follow-up:** Recommended next steps for live verification

## Notes

- The August 2026 CLAUDE.md session documented these as fixes already applied
- This phase confirms they are still in place and correct after Phases 1-3
- No code changes are expected in this phase (verification only)
- Bug-03 (LibreWolf) was also partially verified in Phase 1 (AUDIT-04 confirmed librewolf.png exists)
