# Phase 3 Summary: Codebase Restructuring

**Phase:** 03-codebase-restructuring
**Status:** COMPLETE ✓
**Date:** 2026-08-28

## What Was Done

1. **Decision made:** Option B — Source-managed modularization with build step
   - User explicitly selected modularization with a build script
   - AME Wizard requires monolithic `custom.yml` — modular files are source-of-truth, build script generates the runtime file

2. **Split script created** (`scripts/split-playbook.py`):
   - Parses `custom.yml`, extracts the YAML header (comment block + `actions:` key) into `header.yml`
   - Splits the 40 sections into `Configuration/sections/01-*.yml` through `40-*.yml`
   - Preserves CRLF line endings and exact byte content

3. **Build script created** (`scripts/build-playbook.py`):
   - Reads `header.yml` + all section files in numeric order (01 → 40)
   - Concatenates into `Configuration/custom.yml`
   - Validates output: `actions:` key present, all 40 section headers, non-empty
   - `--dry-run` flag: preview without writing
   - `--verify` flag: compare against `custom.yml.bak` for byte-identical output
   - Creates backup before overwriting

4. **Split executed** — All 40 section files + header.yml created from current custom.yml

5. **Build verified** — Build script regenerated `custom.yml` that is **byte-identical** to the original (verified via `cmp`)

6. **Fix applied** — Line 24 stale comment: `firefoxdev` → `librewolf`

7. **README.md updated** — Repository structure section expanded + new Development Workflow section with build instructions

## Directory Structure Created

```
Configuration/
├── custom.yml              (build output — regenerated from sections)
├── header.yml              (template: comment block + 'actions:' key)
└── sections/               (40 modular section files, source-of-truth)
    ├── 01-initialize.yml
    ├── 02-theme-*.yml
    └── ... through 40-end.yml

scripts/
├── split-playbook.py       (one-time split: custom.yml → sections)
└── build-playbook.py       (build: sections → custom.yml)
```

## Key Design Decisions

- **`custom.yml` remains committed** — AME Wizard ships it directly; no build step needed when loading an existing release
- **Section files are source-of-truth** — Users edit sections, then run `build-playbook.py` to regenerate `custom.yml`
- **Both custom.yml AND sections committed** — custom.yml for AME Wizard, sections for development
- **40 separate files** — one per section, matching the 40-section structure documented throughout
- **Zero-padded filenames** — `01-initialize.yml`, `02-theme.yml`, etc. for deterministic numeric ordering
- **Byte-identical regeneration verified** — `cmp` confirms no data loss through split/build cycle

## Trade-offs Accepted

- User must run `python scripts/build-playbook.py` after editing sections before loading in AME Wizard
- Git diffs show section file changes (better granularity, but more files to review)
- Additional tooling to maintain (build script, split script)
- AME Wizard still receives monolithic file at runtime (unchanged)

## Deferred Items

- Remove orphaned `firefox.png` from Images/
- General cleanup of dead references (EnableDefender.ps1, ControlPanelSettings.reg) — left as-is per Phase 2 direction

## Next Phase

**Phase 4: Bug Verification** — Verify NCSI fix, desktop cleanup registry delete, and LibreWolf winget install.
