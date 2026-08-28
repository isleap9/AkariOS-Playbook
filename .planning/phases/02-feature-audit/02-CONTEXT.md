# Phase 2: Feature Audit - Context

**Gathered:** 2026-08-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce a verified feature matrix mapping all 40 sections in `Configuration/custom.yml` to their feature toggles, actions, and dependencies. Cross-check all feature toggles between `custom.yml` and `playbook.conf` — confirm 1:1 match. Audit all bundled executables in `Executables/` — verify each is referenced by at least one section in `custom.yml`. Audit `Images/` directory — verify each PNG corresponds to a `playbook.conf` `RadioButtonOption` `FileName`. Verify all feature toggles from CLAUDE.md match the actual `playbook.conf` options.

This phase is a documentation/verification phase — it produces an audit report and feature matrix, fixing discrepancies where the fix is low-risk and approved by the user.
</domain>

<decisions>
## Implementation Decisions

### Discrepancy 1: remove-uwp-photos dead toggle
- **D-01:** Wire up the `remove-uwp-photos` toggle by adding `option: 'remove-uwp-photos'` gates to Legacy Photo Viewer registry entries in Section 12.
- **D-02:** The Legacy Photo Viewer entries do not currently exist in Section 12 (only a comment placeholder at line 266). Must add the standard registry entries that associate image file types with Windows Photo Viewer via `C:\Program Files\Windows Photo Viewer\PhotoViewer.dll`.
- **D-03:** The UWP Photos app (`Microsoft.Windows.Photos`) stays always-kept (no toggle needed) — only the Legacy Photo Viewer entries get the toggle gate.

### Discrepancy 2: Stale Section 10 header
- **D-04:** Update Section 10 header comment from "Firefox Dev" to "LibreWolf" to reflect the August 2026 replacement. The comment currently says `Firefox Dev` but Firefox Developer was replaced by LibreWolf via winget.

### Discrepancy 3: NoDefender.cab classification
- **D-05:** Classify `NoDefender.cab` as "referenced (indirect)" — it exists in `Executables/Files/Windows/NoDefender.cab`, is deployed to `C:\Windows\NoDefender.cab` by Section 01 robocopy, and is used by `DisableDefender.ps1` at runtime (`$CabPath = "C:\Windows\NoDefender.cab"`). It is not directly referenced in custom.yml directives but is an active runtime dependency.

### Discrepancy 4: ControlPanelSettings.reg and EnableDefender.ps1
- **D-06:** Classify as INTENDED — `ControlPanelSettings.reg` is a dead reference (content inlined in Section 26, kept for historical context per CLAUDE.md). `EnableDefender.ps1` is a restoration script for end-user use, not an apply-time directive. No action needed — note in audit report.

### Section header comment cleanup
- **D-07:** Update Section 10 header to say "LibreWolf" instead of "Firefox Dev" per user approval.

### Claude's Discretion
- Output format: Dedicated AUDIT.md file in the phase directory with feature matrix table and executable/image audit tables
- The Legacy Photo Viewer registry entries to add are the standard ones from WinSux/AkariV5: file type associations for .jpg, .jpeg, .png, .bmp, .gif, .tif, .tiff pointing to `rundll32.exe "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", ImageView_Fullscreen`
- Feature matrix will include: Section number, section name, toggles, directive types used, always-on vs gated, and notes

### Claude's Discretion (additional)
- Exact format of the feature matrix table (columns: Section, Name, Toggles, Directives, Gate Type, Notes)
- Whether to track directive counts per section (useful but not required by REQ)
</decisions>

<canonical_refs>
## Canonical References

### Playbook files
- `Configuration/custom.yml` — Main playbook (40 sections, ~1303 lines after Phase 1)
- `playbook.conf` — AME Wizard UI config (XML): 24 toggle Names + structural Names
- `CLAUDE.md` — Project memory with feature toggles list, design decisions, planned changes

### Codebase mapping
- `.planning/codebase/STRUCTURE.md` — Directory layout, file purposes, key file locations
- `.planning/codebase/CONVENTIONS.md` — Naming patterns, YAML/XML conventions, comment style
- `.planning/codebase/ARCHITECTURE.md` — Layer analysis, data flow, safety nets
- `.planning/codebase/CONCERNS.md` — Tech debt, known bugs, fragile areas
- `.planning/codebase/TESTING.md` — Manual verification checklist (reference for audit findings)

### Requirements
- `.planning/REQUIREMENTS.md` — v1 requirements: AUDIT-01 through AUDIT-05
- `.planning/PROJECT.md` — Project definition, validated requirements, active requirements
- `.planning/ROADMAP.md` — Phase details and success criteria for Phase 2
</canonical_refs>

<specifics>
## Specific Ideas

- The feature matrix should be comprehensive — all 40 sections, every toggle, every directive type
- Include a separate "Discrepancies Found" section in the audit report with severity and recommended fix
- The `remove-uwp-photos` toggle fix requires adding actual registry entries (not just gating existing ones) — standard Legacy Photo Viewer entries
</specifics>

<deferred>
## Deferred Ideas

- Modularizing custom.yml — Phase 3
- Bug verification (NCSI, desktop cleanup, LibreWolf winget) — Phase 4
</deferred>

---

*Phase: 02-feature-audit*
*Context gathered: 2026-08-28*
