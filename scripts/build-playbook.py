#!/usr/bin/env python3
"""
build-playbook.py — Build custom.yml from modular section files + header.

Usage:
    python scripts/build-playbook.py [--dry-run] [--verify]

This script:
    1. Reads Configuration/header.yml (comment block + 'actions:' key)
    2. Reads all Configuration/sections/*.yml files in numeric order (01 → 40)
    3. Concatenates them into Configuration/custom.yml
    4. Validates the output (actions: key present, all 40 sections present)
    5. Optionally compares against a backup of the original

Flags:
    --dry-run    Print the generated content to stdout without writing
    --verify     After building, compare output against custom.yml.bak if it exists

This is the build step required because AME Wizard expects a monolithic custom.yml.
Edit section files, then run this script before loading the playbook in AME Wizard.
"""

import os
import re
import sys
import argparse
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT, "Configuration")
SECTIONS_DIR = os.path.join(CONFIG_DIR, "sections")
HEADER_FILE = os.path.join(CONFIG_DIR, "header.yml")
CUSTOM_YML = os.path.join(CONFIG_DIR, "custom.yml")
BACKUP_FILE = os.path.join(CONFIG_DIR, "custom.yml.bak")


def find_section_files():
    """Find all section files sorted by their numeric prefix."""
    if not os.path.isdir(SECTIONS_DIR):
        print(f"ERROR: Sections directory not found: {SECTIONS_DIR}", file=sys.stderr)
        sys.exit(1)

    files = []
    for f in os.listdir(SECTIONS_DIR):
        m = re.match(r'^(\d{2})-.*\.yml$', f)
        if m:
            files.append((int(m.group(1)), f))

    if not files:
        print(f"ERROR: No section files found in {SECTIONS_DIR}", file=sys.stderr)
        sys.exit(1)

    files.sort(key=lambda x: x[0])
    return files


def read_header():
    """Read the header file."""
    if not os.path.isfile(HEADER_FILE):
        print(f"ERROR: Header file not found: {HEADER_FILE}", file=sys.stderr)
        sys.exit(1)

    with open(HEADER_FILE, "r", encoding="utf-8") as f:
        header = f.read()

    # Verify header contains 'actions:' key
    if not re.search(r'^actions:\s*$', header, re.MULTILINE):
        print(f"WARNING: header.yml does not end with 'actions:' key", file=sys.stderr)

    return header


def build_content():
    """Build the full custom.yml content from header + sections."""
    header = read_header()
    section_files = find_section_files()

    parts = [header]
    for num, filename in section_files:
        filepath = os.path.join(SECTIONS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            section_content = f.read()
        parts.append(section_content)

    content = ''.join(parts)

    # Ensure file ends the same way as the original (no extra trailing newline)
    # The original custom.yml does NOT end with a trailing newline
    content = content.rstrip('\n\r')

    return content


def validate(content):
    """Validate the generated custom.yml content."""
    errors = []
    warnings = []

    # Check 1: 'actions:' key present
    if not re.search(r'^actions:\s*$', content, re.MULTILINE):
        errors.append("Missing 'actions:' key at top level")

    # Check 2: All 40 section headers present
    section_count = len(re.findall(r'# SECTION \d+ - ', content))
    if section_count < 40:
        errors.append(f"Only {section_count} section headers found (expected 40)")

    # Check 3: First section is SECTION 01
    m = re.search(r'# SECTION 01 - ', content)
    if not m:
        errors.append("SECTION 01 not found")

    # Check 4: Last section is SECTION 40
    m = re.search(r'# SECTION 40 - ', content)
    if not m:
        errors.append("SECTION 40 not found")

    # Check 5: Content not empty
    if len(content) < 100:
        errors.append("Generated content is too short (<100 chars)")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Build custom.yml from modular section files"
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Print generated content to stdout without writing')
    parser.add_argument('--verify', action='store_true',
                        help='Compare output against custom.yml.bak if it exists')
    args = parser.parse_args()

    print("=== Building custom.yml from modular sections ===")
    print(f"  Header: {os.path.relpath(HEADER_FILE, ROOT)}")

    section_files = find_section_files()
    print(f"  Sections: {len(section_files)} files from {os.path.relpath(SECTIONS_DIR, ROOT)}/")
    for num, filename in section_files:
        print(f"    {filename}")

    content = build_content()

    # Validate
    errors, warnings = validate(content)

    if warnings:
        for w in warnings:
            print(f"  WARNING: {w}")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        print("Build FAILED — do not use generated file.", file=sys.stderr)
        sys.exit(1)

    print(f"\n  Validation: PASSED ({len(content)} bytes)")

    if args.dry_run:
        print("\n  --- DRY RUN OUTPUT (first 20 lines) ---")
        for i, line in enumerate(content.split('\n')[:20], 1):
            print(f"  {i:>4}|{line}")
        print("  ...")
        print(f"\n  (Full content would be {len(content)} bytes)")
        print("  (Use without --dry-run to write to file)")
        sys.exit(0)

    if args.verify and os.path.isfile(BACKUP_FILE):
        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            backup = f.read()

        if content == backup:
            print(f"\n  VERIFY: PASSED — output matches backup exactly")
        else:
            # Show diff
            import difflib
            diff = difflib.unified_diff(
                backup.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile='backup (original custom.yml)',
                tofile='generated (from sections)',
                n=3
            )
            print(f"\n  VERIFY: DIFFERS from backup:")
            print('  --- (showing first 30 diff lines) ---')
            for i, line in list(enumerate(diff))[:30]:
                print(f"  {line.rstrip()}")
            if len(list(diff)) > 30:
                print("  ... (truncated)")
    else:
        if args.verify:
            print(f"\n  VERIFY: SKIPPED (no backup file at {os.path.relpath(BACKUP_FILE, ROOT)})")

    # Backup existing custom.yml before overwriting
    if os.path.isfile(CUSTOM_YML):
        shutil.copy2(CUSTOM_YML, BACKUP_FILE)
        print(f"\n  Backup: {os.path.relpath(BACKUP_FILE, ROOT)} (previous custom.yml)")

    # Write
    with open(CUSTOM_YML, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Written: {os.path.relpath(CUSTOM_YML, ROOT)}")
    print(f"\nDone! Load the playbook in AME Wizard.")
    return True


if __name__ == "__main__":
    main()
