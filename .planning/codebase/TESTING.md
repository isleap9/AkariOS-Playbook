# Testing Patterns

**Analysis Date:** 2026-08-28

## Test Framework

**Runner:**
- None (no automated test framework)
- Manual verification via AME Wizard runs on test VMs

**Assertion Library:**
- None

**Run Commands:**
```bash
# Manual test process:
# 1. Create Windows 11 VM (target build: 22621, 22631, 26100, etc.)
# 2. Install AME Wizard
# 3. Load playbook (open .apbx or source folder)
# 4. Select feature toggles
# 5. Run playbook
# 6. Verify post-install state manually
# 7. Check Log.yml and Output.txt for errors
```

## Test File Organization

**Location:**
- No test files in repository
- Verification done on target VMs after playbook execution

**Naming:**
- N/A

**Structure:**
- N/A

## Test Structure

**Suite Organization:**
- N/A (no test suites)

**Patterns:**
- N/A

## Mocking

**Framework:**
- None

**Patterns:**
- N/A

**What to Mock:**
- N/A

**What NOT to Mock:**
- N/A

## Fixtures and Factories

**Test Data:**
- N/A

**Location:**
- N/A

## Coverage

**Requirements:**
- No enforced coverage target
- No coverage tooling

**Configuration:**
- N/A

**View Coverage:**
- N/A

## Test Types

**Unit Tests:**
- None (playbook is declarative YAML, not code with units)

**Integration Tests:**
- Manual end-to-end: Run playbook on clean VM, verify results
- Key verification points:
  - Services disabled (check `services.msc` or `Get-Service`)
  - Registry values set (check `reg query`)
  - AppX packages removed (check `Get-AppxPackage`)
  - Scheduled tasks disabled (check Task Scheduler)
  - Power plan active (check `powercfg /getactivescheme`)
  - Timer Resolution service running (check `services.msc` → STR)
  - Start menu layout clean (visual check)
  - Wallpaper/lockscreen applied (visual check)
  - Browser installed (if selected)
  - Defender disabled (if toggled) / restorable via EnableDefender.ps1
  - System Restore point exists (check `rstrui.exe`)

**E2E Tests:**
- Full playbook run on each supported Windows build
- Feature toggle combinations (all on, all off, selective)
- Browser picker combinations (each browser, Edge keep/remove)

## Common Patterns

**Async Testing:**
- N/A

**Error Testing:**
- Check Log.yml for expected benign errors:
  - Error 1392 during appx removal (file-path cleanup artifact)
  - ActivationStore.dat in-use (Windows holds handles, AME retries)
  - "pris" folder access denied (protected SystemApps path)
  - "Could not get app executable location" (package already removed)
  - ScheduledTask Compatibility Appraiser / ProgramDataUpdater fail (may not exist on all builds)

**File System Mocking:**
- N/A

**Snapshot Testing:**
- N/A

## Verification Checklist (Manual)

**Post-Playbook Verification:**

1. **Services** (Section 17, 18, 20, 31):
   - [ ] Telemetry services disabled (diagtrack, WerSvc, etc.)
   - [ ] Printing services disabled (if toggle on)
   - [ ] Bluetooth services disabled (if toggle on)
   - [ ] Hyper-V services disabled (if toggle on)
   - [ ] STR service installed and running
   - [ ] Networking safety-net services auto (iphlpsvc, tcpipreg, Dnscache, NlaSvc, netprofm)

2. **Registry** (Sections 02, 05, 06, 07, 11, 12, 17, 19, 21, 22, 23, 24, 25, 26):
   - [ ] Dark mode keys set (if toggle on)
   - [ ] Defender disabled keys (if toggle on)
   - [ ] UAC disabled keys (if toggle on)
   - [ ] Process mitigations disabled (if toggle on)
   - [ ] Spectre/Meltdown disabled (if toggle on)
   - [ ] Privacy/telemetry keys (HKLM/HKCU/HKU/.DEFAULT)
   - [ ] Firewall outbound blocks for Search/Cortana/Settings
   - [ ] MMCSS/NetworkThrottlingIndex/SystemResponsiveness
   - [ ] Timer resolution GlobalTimerResolutionRequests=1
   - [ ] NIC PnPCapabilities=24 on all adapters

3. **AppX** (Section 16):
   - [ ] Listed packages removed
   - [ ] Allowlist packages kept (Terminal, Store, AppInstaller, Notepad, Paint, SecHealthUI, etc.)
   - [ ] Copilot packages removed

4. **Scheduled Tasks** (Section 28):
   - [ ] Telemetry tasks disabled/deleted
   - [ ] UpdateOrchestrator tasks disabled
   - [ ] SystemRestore SR task NOT touched

5. **Power** (Sections 30, 33):
   - [ ] Ultimate Performance plan active (GUID 99999999-...)
   - [ ] Other plans deleted
   - [ ] Hibernate off
   - [ ] Extra power savings applied (if toggle on)

6. **Browsers** (Section 10):
   - [ ] Selected browser installed
   - [ ] Edge removed (unless browser-edge selected)

7. **Files/Shortcuts** (Sections 01, 26, 34, 36, 40):
   - [ ] C:\AkariOS\Ultimate\ deployed
   - [ ] start2.bin in StartMenuExperienceHost LocalState
   - [ ] Wallpaper/lockscreen set
   - [ ] Profile picture set
   - [ ] Desktop icon positions reset (Shell\Bags\1\Desktop deleted)
   - [ ] AkariOS Toolkit shortcut on Public Desktop

8. **System Restore** (Section 37):
   - [ ] System Restore enabled on C:
   - [ ] "AkariOS" restore point exists

9. **Logs/Errors** (Log.yml, Output.txt):
   - [ ] No unexpected critical errors
   - [ ] Benign errors match known list above

## Test Infrastructure

**Test VMs:**
- Clean Windows 11 ISO for each supported build
- Snapshots for rapid iteration
- AME Wizard installed

**Automation:**
- None currently (manual process)
- Could be automated with Packer + AME Wizard CLI (if available)

---

*Testing analysis: 2026-08-28*
*Update when test patterns change or automation added*