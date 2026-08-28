# Codebase Concerns

**Analysis Date:** 2026-08-28

## Tech Debt

**Monolithic custom.yml (~1315 lines, 40 sections):**
- Issue: Single massive YAML file with all playbook logic
- Files: `Configuration/custom.yml`
- Why: Historical growth from AkariV5, no modularization in AME Wizard format
- Impact: Hard to review, merge conflicts likely, difficult to find specific sections
- Fix approach: Consider splitting into include files if AME Wizard supports it, or external generator script

**Inline PowerShell in YAML:**
- Issue: Complex PowerShell one-liners embedded directly in YAML (Sections 17, 23, 26, 29, 31, 36, etc.)
- Files: `Configuration/custom.yml` (multiple sections)
- Why: AME Wizard `!powerShell` directive accepts inline commands; no external script reference for small blocks
- Impact: Hard to read, debug, and test; escaping issues (backslashes, quotes)
- Fix approach: Move complex blocks to `.ps1` files in `Executables/` and call via `exeDir: true`

**Hardcoded URLs for downloads:**
- Issue: Direct URLs for VC++ redists, DirectX, browsers (Section 08, 10)
- Files: `Configuration/custom.yml`
- Why: No package manager for these; GitHub releases API used for some but not all
- Impact: Link rot (URLs change), version drift, maintenance burden
- Fix approach: Use winget/chocolatey where possible; maintain URL mapping document

**Duplicate NoDefender.cab:**
- Issue: `NoDefender.cab` exists in both `Executables/` and `Executables/Files/Windows/`
- Files: `Executables/NoDefender.cab`, `Executables/Files/Windows/NoDefender.cab`
- Why: Section 01 robocopies `Files/` tree; `DisableDefender.ps1` references `Executables/` version
- Impact: Wasted space, confusion about which is used
- Fix approach: Remove duplicate, ensure `DisableDefender.ps1` uses correct path

**ControlPanelSettings.reg dead reference:**
- Issue: `.reg` file kept but not imported (inlined in Section 26)
- Files: `Executables/ControlPanelSettings.reg`
- Why: Historical - was imported via `reg import`, now inlined for reliability
- Impact: Confusion, stale file
- Fix approach: Delete or clearly mark as archived reference

## Known Bugs

**LibreWolf GitHub repo 404 (FIXED in custom.yml):**
- Symptoms: `git: 'https://github.com/librewolf-community/browser-windows'` returns 404
- Trigger: Section 10 browser-librewolf download
- Files: `Configuration/custom.yml` (line ~222-223)
- Workaround: **FIXED** - Changed to winget install (`LibreWolf.LibreWolf`)
- Root cause: LibreWolf moved Windows builds to `dl.librewolf.net`, GitHub repo archived
- Fix: Already applied - winget always pulls latest

**Error 1392 during AppX removal:**
- Symptoms: "Error 1392" logged in Log.yml during Section 16 AppX removal
- Trigger: `!appx` directives removing packages
- Workaround: Benign - AME Wizard file-path cleanup artifact, harmless
- Root cause: AME Wizard internal cleanup after package removal

**ActivationStore.dat in-use:**
- Symptoms: Access denied / in-use errors for ActivationStore.dat
- Trigger: AppX removal (Section 16)
- Workaround: Benign - Windows holds handles on packages being removed, AME retries
- Root cause: System file locks during package uninstall

**"pris" folder access denied (SystemApps):**
- Symptoms: Access denied removing protected SystemApps folders
- Trigger: AppX removal / file cleanup
- Workaround: Benign - Protected system path, AME skips gracefully
- Root cause: Windows protects critical system app containers

**"Could not get app executable location":**
- Symptoms: Warning in Log.yml during AppX removal
- Trigger: Package already removed before location query
- Workaround: Benign - Race condition in AME Wizard query order

**ScheduledTask Compatibility Appraiser / ProgramDataUpdater fail:**
- Symptoms: "Task not found" errors in Section 28
- Trigger: `!scheduledTask` disable on tasks that don't exist on all builds
- Workaround: Benign - Tasks may not exist on all Windows builds
- Fix approach: Could add existence check, but `ignoreErrors: true` handles it

## Security Considerations

**Defender disable method (toggle: disable-defender):**
- Risk: System left without AV if user doesn't install alternative
- Current mitigation: `EnableDefender.ps1` provided for restoration; toggle is opt-in (default off)
- Recommendations: Clear warning in playbook.conf description (already present)

**UAC disable (toggle: disable-uac):**
- Risk: Elevation prompts disabled - malware can run elevated silently
- Current mitigation: Opt-in toggle (default off); user must consciously enable
- Recommendations: Stronger warning in playbook.conf

**Process mitigations disable (toggle: disable-process-mitigations):**
- Risk: CFG, DEP, ASLR, etc. disabled - exploit mitigations removed
- Current mitigation: Opt-in toggle (default off)
- Recommendations: Warning about security impact

**Spectre/Meltdown disable (toggle: disable-spectre-meltdown):**
- Risk: CPU vulnerability mitigations disabled
- Current mitigation: Opt-in toggle (default off)
- Recommendations: Only for performance-critical workloads on trusted code

**Hyper-V/VBS disable (toggle: disable-hyperv):**
- Risk: Breaks anti-cheat (Valorant, FACEIT, etc.), VBS security features
- Current mitigation: Warning description in playbook.conf (added in August 2026 session)
- Recommendations: Keep warning prominent; consider per-game detection

**Firewall targeted outbound blocks:**
- Risk: Blocking SearchApp, SearchHost, SystemSettings may break legitimate features
- Current mitigation: Targeted (not full firewall wipe); only 3 rules
- Recommendations: Test thoroughly; consider making optional

**Smart App Control disabled (Section 01):**
- Risk: Unsigned code can run without warning
- Current mitigation: Required for playbook's own unsigned scripts to work
- Recommendations: Document clearly; user can re-enable post-install

## Performance Bottlenecks

**Section 08 VC++ Redist installs (sequential, 7 versions × 2 arch):**
- Problem: 14 sequential downloads + installs, each with `/wait: true`
- File: `Configuration/custom.yml` Section 08
- Measurement: ~5-10 minutes on slow connection
- Cause: Sequential execution, no parallelization in AME Wizard
- Improvement path: Could combine into single installer script; use winget for newer versions

**Section 10 Browser downloads (sequential per selection):**
- Problem: Each selected browser downloads + installs sequentially
- File: `Configuration/custom.yml` Section 10
- Measurement: ~2-5 minutes per browser
- Cause: Sequential, large downloads
- Improvement path: Parallel download not supported by AME Wizard

**Section 16 AppX removal (100+ packages):**
- Problem: 100+ `!appx` directives executed sequentially
- File: `Configuration/custom.yml` Section 16
- Measurement: ~3-5 minutes
- Cause: Each package removal is separate operation
- Improvement path: Batch removal via PowerShell (but loses AME Wizard tracking)

**Section 17 Services (80+ services):**
- Problem: 80+ `!service` directives sequentially
- File: `Configuration/custom.yml` Section 17
- Measurement: ~30-60 seconds
- Cause: Each service change is separate SCM call
- Improvement path: Batch via PowerShell (but loses AME Wizard tracking)

## Fragile Areas

**AME Wizard version compatibility:**
- File: `playbook.conf` (SupportedBuilds), `custom.yml` (directive usage)
- Why fragile: AME Wizard updates may change directive behavior or YAML schema
- Common failures: New directive options, changed defaults, schema validation
- Safe modification: Test on target AME Wizard version before committing
- Test coverage: Manual only (run on test VMs)

**Windows build differences:**
- File: `custom.yml` (many registry paths, service names, AppX package names)
- Why fragile: Windows 11 builds (22H2, 23H2, 24H2, LTSC) have different packages, services, registry keys
- Common failures: AppX package names change, services added/removed, registry paths move
- Safe modification: Test on each supported build; use `SupportedBuilds` in playbook.conf
- Test coverage: Manual per build

**Section 01 Robocopy deployment:**
- File: `custom.yml` line 40, `Executables/Files/` structure
- Why fragile: Source tree structure must match expected destination paths exactly
- Common failures: Missing files, path changes, permission issues on target
- Safe modification: Keep `Executables/Files/` in sync with Section 01 expectations
- Test coverage: Verify deployed files post-Section 01

**Section 31 Timer Resolution service compilation:**
- File: `custom.yml` Section 31, `Executables/settimerresolutionservice.cs`
- Why fragile: Depends on in-box `csc.exe` path (`.NET Framework 4.0.30319`); may not exist on minimal installs
- Common failures: csc.exe not found, compilation errors, service install fails
- Safe modification: Verify .NET Framework present; consider pre-compiled binary
- Test coverage: Run on clean VM

**Browser installer URL/regex changes:**
- File: `custom.yml` Section 10, `playbook.conf` Images/
- Why fragile: Browser vendors change download URLs, filename patterns, GitHub repo structures
- Common failures: Regex no longer matches, 404 on download, installer switches change
- Safe modification: Monitor browser release channels; test installs regularly
- Test coverage: Manual per browser

**start2.bin Start menu layout:**
- File: `Executables/start2.bin`, `custom.yml` Section 26 (deploy)
- Why fragile: Binary format undocumented; Windows version may change layout format
- Common failures: Start menu layout not applied, corruption, wrong format
- Safe modification: Test on target Windows build; regenerate if format changes
- Test coverage: Visual verification of Start menu

## Scaling Limits

**AME Wizard playbook size:**
- Current: ~1315 lines, 40 sections, ~137KB YAML
- Limit: Unknown (AME Wizard memory/parsing limits)
- Symptoms at limit: Load failures, parse errors, execution timeouts
- Scaling path: Modularize if AME Wizard supports includes; or external preprocessor

**Number of feature toggles:**
- Current: ~20 toggles (13 security, 4 UI, 7 browsers, 1 extra)
- Limit: UI usability (playbook.conf CheckboxPage/RadioImagePage)
- Symptoms at limit: Overwhelming UI, decision fatigue
- Scaling path: Group into categories; use sub-pages

**Post-Install Toolkit size:**
- Current: 50+ scripts in 8 categories
- Limit: Disk space, user overwhelm
- Symptoms at limit: Large `C:\AkariOS\Ultimate\`, hard to navigate
- Scaling path: Curate; move advanced scripts to separate repo

## Dependencies at Risk

**AME Wizard (closed source, single vendor):**
- Risk: Project abandoned, breaking changes, licensing changes
- Impact: Playbook cannot be executed without AME Wizard
- Migration path: Reverse-engineer directive format; build custom runner; migrate to PowerShell/DSC

**GitHub Releases API (for Mercury, Thorium, 7-Zip):**
- Risk: Rate limiting, API changes, repos archived/moved
- Impact: Browser/tool downloads fail
- Migration path: Mirror releases; use winget/chocolatey; vendor binaries

**winget (for LibreWolf):**
- Risk: Package ID changes, source removed, winget deprecated
- Impact: LibreWolf install fails
- Migration path: Fallback to direct download; maintain URL mapping

**Microsoft Download Center URLs (VC++, DirectX):**
- Risk: URLs change, files moved, downloads blocked
- Impact: Runtime installs fail
- Migration path: Use winget for VC++ (`Microsoft.VisualCpp.Redist.*`); vendor DirectX

**Windows builds (supported builds list):**
- Risk: New Windows 11 builds break assumptions (services, packages, registry)
- Impact: Playbook fails or produces broken system
- Migration path: Test on Insider builds; update `SupportedBuilds` and logic per build

## Missing Critical Features

**Automated testing / CI:**
- Problem: No automated verification of playbook changes
- Current workaround: Manual VM testing
- Blocks: Confidence in changes, regression detection, multi-build validation
- Implementation complexity: High (requires AME Wizard automation, VM orchestration)

**Playbook validation/linting:**
- Problem: No schema validation for custom.yml or playbook.conf
- Current workaround: AME Wizard load-time validation only
- Blocks: Catching YAML/XML errors before test run
- Implementation complexity: Medium (JSON schema for AME directives)

**Version/change tracking for playbook:**
- Problem: No formal changelog, versioning only in playbook.conf
- Current workaround: Git history, CLAUDE.md session notes
- Blocks: Users knowing what changed between versions
- Implementation complexity: Low (CHANGELOG.md)

**Rollback/undo capability:**
- Problem: No automated rollback except System Restore point
- Current workaround: System Restore (Section 37), EnableDefender.ps1
- Blocks: Reverting individual changes, partial rollback
- Implementation complexity: High (would need inverse operations for each directive)

**Documentation for end users:**
- Problem: README.md is minimal; no guide for feature toggles
- Current workaround: playbook.conf descriptions, CLAUDE.md (dev only)
- Blocks: Users understanding toggle implications
- Implementation complexity: Medium (user-facing docs)

## Test Coverage Gaps

**No automated tests:**
- What's not tested: All playbook functionality
- Risk: Regressions on every change
- Priority: High
- Difficulty to test: High (requires AME Wizard automation, Windows VM fleet)

**Multi-build testing:**
- What's not tested: Automated matrix across SupportedBuilds
- Risk: Build-specific breakage undetected
- Priority: High
- Difficulty to test: High (multiple VM images)

**Feature toggle combinations:**
- What's not tested: All 2^20 combinations
- Risk: Toggle interactions cause failures
- Priority: Medium
- Difficulty to test: High (combinatorial explosion)

**Post-install verification:**
- What's not tested: Automated verification of applied changes
- Risk: Silent failures (registry not set, service not disabled)
- Priority: High
- Difficulty to test: Medium (PowerShell verification script possible)

---

*Concerns audit: 2026-08-28*
*Update as issues are fixed or new ones discovered*