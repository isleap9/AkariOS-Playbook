# Coding Conventions

**Analysis Date:** 2026-08-28

## Naming Patterns

**Files:**
- `custom.yml` - Main playbook (lowercase, descriptive)
- `playbook.conf` - AME Wizard config (lowercase, standard name)
- `playbook.png` - Thumbnail (lowercase, standard name)
- `AkariOS-Playbook.apbx` - Package (PascalCase project name + hyphen + type)
- `CLAUDE.md` - AI context (UPPERCASE, standard)
- `README.md` - Documentation (UPPERCASE, standard)
- `.gitattributes` - Git config (dotfile, lowercase)
- PowerShell scripts: `PascalCase.ps1` or `Descriptive Name.ps1` (spaces allowed, e.g., `DisableDefender.ps1`, `1 Space Check.ps1`)
- C# source: `lowercase.cs` (e.g., `settimerresolutionservice.cs`)
- Binary: `lowercase.bin` (e.g., `start2.bin`)
- Images: `lowercase.png` (browser names + `next.png`)
- Registry: `ControlPanelSettings.reg` (PascalCase, .reg extension)

**Directories:**
- `Configuration/` - PascalCase, singular
- `Executables/` - PascalCase, plural
- `Images/` - PascalCase, plural
- `Files/AkariOS/Ultimate/` - PascalCase project, PascalCase tier
- Category folders: `N Description/` (number + space + title, e.g., `1 Check/`, `6 Windows/`)
- Script files in toolkit: `N Description.ps1` (number + space + title)

**YAML (custom.yml):**
- Section comments: `# ==========================================================================`
- Section headers: `# SECTION NN - NAME` (zero-padded 2-digit)
- Feature toggles: kebab-case (e.g., `disable-defender`, `browser-librewolf`, `enable-dark-mode`)
- AME directives: `!directiveName` (bang prefix, camelCase: `!registryValue`, `!powerShell`, `!scheduledTask`)
- Directive properties: camelCase (e.g., `runas: currentUserElevated`, `wait: true`, `operation: change`)
- Registry paths: Single backslash in YAML string (e.g., `HKLM\\SOFTWARE\\Microsoft\\...`)
- Registry types: UPPER_SNAKE_CASE (e.g., `REG_DWORD`, `REG_SZ`, `REG_BINARY`, `REG_EXPAND_SZ`)

**XML (playbook.conf):**
- Elements: PascalCase (e.g., `Playbook`, `FeaturePages`, `CheckboxPage`, `RadioImagePage`)
- Attributes: PascalCase (e.g., `IsRequired`, `IsChecked`, `DefaultOption`, `DependsOn`)
- Option names: kebab-case matching YAML toggles (e.g., `disable-defender`, `browser-mercury`)
- FileName values: lowercase, no extension (e.g., `mercury`, `librewolf`, `next`)

**PowerShell (inline in YAML and .ps1 files):**
- Cmdlets: PascalCase (e.g., `Get-ChildItem`, `Set-ItemProperty`, `New-Item`)
- Parameters: PascalCase (e.g., `-Path`, `-Name`, `-Value`, `-Force`, `-ErrorAction`)
- Variables: `$camelCase` or `$PascalCase` (e.g., `$kv`, `$p`, `$guids`, `$data`)
- Hashtables: `@{key=value}` with camelCase keys
- ErrorAction: `SilentlyContinue` or `Ignore` (alias `0` or `EA 0`)
- Pipeline: Used heavily for filtering (`Where-Object`, `ForEach-Object`)

**C# (settimerresolutionservice.cs):**
- Standard .NET conventions (PascalCase types/methods, camelCase parameters)
- Windows Service pattern (ServiceBase, Installer)

## Code Style

**Formatting (YAML):**
- 2-space indentation
- Block sequences with `- ` for list items
- Inline mappings for simple directives: `{key: value, key2: value2}`
- Multi-line for complex directives with nested properties
- Comments on own line above section/action

**Formatting (XML):**
- 4-space indentation (tabs in original)
- Self-closing tags for empty elements
- Attributes on same line for simple elements, multi-line for complex

**Formatting (PowerShell):**
- Inline in YAML: Single line with semicolons or escaped newlines
- .ps1 files: Standard indentation, one cmdlet per line typically
- Heavy use of pipeline (`|`)
- Splatting for complex parameters (rare)

**Linting:**
- No formal linters configured
- AME Wizard validates YAML syntax at load time
- XML validated by AME Wizard against schema
- PowerShell syntax checked at runtime

## Import Organization

**Not Applicable:** No module imports in playbook format
- PowerShell: No `Import-Module` or `using` statements in playbook
- C#: Standard `using` directives at top of .cs file
- YAML: No import mechanism (monolithic file)

## Error Handling

**Patterns:**
- `ignoreErrors: true` on `!taskKill` and some `!appx` operations
- `errorAction: Ignore` on PowerShell `Remove-AppxPackage` calls
- `-EA 0` / `-ErrorAction SilentlyContinue` on many PowerShell commands
- `try { } catch { }` blocks in inline PowerShell for critical sections
- `if (Test-Path) { ... }` guards before file operations
- `2>$null` / `2>&1 | Out-Null` for stderr suppression in cmd
- `>nul 2>&1` for cmd output suppression

**Error Types:**
- Missing files/keys: Ignored (idempotent deletes)
- Service not found: Ignored (startup change on missing = no-op)
- Download failures: AME Wizard handles retry/logging
- Access denied: Logged, continues (some protected paths)
- In-use files: AME Wizard retries (ActivationStore.dat)

**Logging:**
- `!status` directives for progress messages
- AME Wizard generates `Log.yml` (structured) and `Output.txt` (raw)
- PowerShell `Write-Host` / `Write-Output` captured in Output.txt
- Errors in Log.yml with directive context

## Comments

**When to Comment:**
- Section headers (mandatory - every section)
- Design decisions (why this approach, source attribution)
- Safety-net explanations (why something is NOT done)
- Feature toggle gating explanations
- Complex PowerShell one-liners (what it does)
- "Atlas gap" / "FSOS" / "Vain" / "WinSux" / "AkariV5" source markers

**Comment Style:**
- YAML: `# Comment` on own line
- XML: `<!-- Comment -->` (rare, mostly in playbook.conf for disclaimer)
- PowerShell: `# Comment` (inline or own line)
- C#: `// Comment` or `/// XML doc`

**TODO Comments:**
- Not used in playbook (tracking via CLAUDE.md and git issues)
- "Pending" markers in CLAUDE.md for known future work

## Function Design

**Not Applicable:** No functions in playbook format
- PowerShell scripts in Executables/ use functions (standard PS patterns)
- C# service has standard methods (OnStart, OnStop)

## Module Design

**Exports:**
- Not applicable (no modules)

**Barrel Files:**
- Not applicable

---

*Convention analysis: 2026-08-28*
*Update when patterns change or new file types added*