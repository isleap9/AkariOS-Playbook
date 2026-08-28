# Phase 3 Context: Codebase Restructuring

**Gathered:** 2026-08-28
**Status:** Ready for discussion

<domain>
## Phase Boundary

Decide on modularization approach for the monolithic `custom.yml` (~1310 lines, 40 sections). Present plan and get user approval before any changes.

**Key technical constraint from codebase scouting:**

AME Wizard (closed-source execution engine) parses `custom.yml` as a single monolithic YAML file — the `actions:` list at the top level is a flat sequence of directives. AME Wizard's YAML parser does NOT support `!include` or any form of file inclusion. This means:

- **True structural modularization** (splitting into per-section `.yml` files) would BREAK AME Wizard — it expects one file
- **A pre-processor** (build script that concatenates section files into `custom.yml`) is possible but adds complexity and a build step the user must run before each play
- **No pre-processing is currently in place** — there is no Makefile, build script, or generator

**What the August 2026 session decided:** "decided against it for now (user said 'i was just asking') — keep as monolithic unless it grows significantly larger"

**Current line count:** 1310 lines (Phase 2 added 7 lines for Legacy Photo Viewer entries)
**Original line count (August 2026 note):** ~1315 lines
**Net change:** Essentially unchanged — custom.yml has remained stable around 1310-1315 lines through all changes

</domain>

## Options

### Option A: Keep Monolithic (No Change)
**What:** Leave `custom.yml` as a single file. No structural changes.
**Why:**
- AME Wizard requires a single monolithic file — there is no include mechanism
- 1310 lines is large but manageable with good section headers and navigation
- User explicitly said "i was just asking" in August 2026 when modularization was floated
- No build step required — user can edit and run directly
- Git diff/review is straightforward (all changes in one file)
- Risk of breakage is zero (no structural changes)

**Trade-offs:** Merge conflicts on concurrent edits, harder to find specific sections

### Option B: Source-Managed Modularization (Build Step)
**What:** Split `custom.yml` into `Configuration/sections/01.yml` through `40.yml`, with a build script that concatenates them into `Configuration/custom.yml` before running in AME Wizard.
**Why:** Better organization, easier per-section editing, cleaner diffs
**Trade-offs:**
- Adds a build step — user must run the preprocessor before loading in AME Wizard
- Risk of section ordering errors during concatenation
- Additional tooling to maintain (build script)
- AME Wizard still receives monolithic file — source/edit experience improves but runtime doesn't change
- Breaks existing workflow (user currently edits custom.yml directly)

**Technical feasibility:** High — a simple Python/Bash script could concatenate. But:
- The `actions:` header and top-level structure must be preserved in the build
- YAML merge requires careful handling of the root `actions:` key
- Need to document the build process clearly

### Option C: Hybrid — Section-Based Comments + Navigation Aids
**What:** Keep `custom.yml` monolithic but add structural improvements: a section index at the top, consistent separator comments, and maybe a "jump table." No file splitting.
**Why:** Improves navigability without breaking AME Wizard or adding a build step
**Trade-offs:** Minimal overhead, but doesn't solve merge conflict issue

### Option D: External Preprocessor (Advanced)
**What:** Use a YAML preprocessor tool (like `yq` or a custom Python script) that supports `!include`-style directives, generating `custom.yml` from modular sources.
**Why:** Cleanest source structure
**Trade-offs:**
- AME Wizard doesn't support `!include` — the preprocessor must run BEFORE AME Wizard
- Requires installing/using external tooling
- Significant complexity for marginal benefit at 1310 lines

## Recommendation

**Option A (Keep Monolithic)** is recommended because:

1. **Technical constraint:** AME Wizard requires a single file — any splitting requires a build step
2. **User preference:** In August 2026, user explicitly said "i was just asking" when modularization was floated
3. **Scale:** 1310 lines is large but manageable; the file has clear section headers and navigation is adequate with `grep -n` or editor folding
4. **Risk:** Any structural change carries risk of breaking the playbook; current state is stable and tested
5. **Workflow:** Current workflow (edit custom.yml directly, commit) is simple and reliable

**However, if the user wants better organization:** Option C (hybrid — section index + improved comments) is a low-risk improvement that doesn't change the file structure or require a build step.

## Notes

- Section 10 header fix (Firefox Dev → Librewolf) and Section 12 remove-uwp-photos wiring from Phase 2 confirmed in place
- custom.yml line count: 1310 (stable since Phase 1/2 edits)
- No external build tools, scripts, or preprocessors exist in the project
- The `AkariOS-Playbook.apbx` is the compiled package — AME Wizard generates this from custom.yml + playbook.conf at packaging time
- RESTRUCT-01 (decide approach) is the blocking requirement; RESTRUCT-02 and RESTRUCT-03 are conditional on modularization being approved

## Key Decision

**User must approve or reject modularization.** Per CLAUDE.md constraint: "Always present a full plan and get approval before editing any file."
