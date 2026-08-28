#!/usr/bin/env python3
"""
split-playbook.py — One-time script to split Configuration/custom.yml into modular section files.

Usage:
    python scripts/split-playbook.py

This reads Configuration/custom.yml (the monolithic playbook) and produces:
    - Configuration/header.yml  (YAML comment block + 'actions:' key)
    - Configuration/sections/01-initialize.yml through 40-end.yml

After running this once, use build-playbook.py to regenerate custom.yml from the
section files + header.

NOTE: This script is designed to be run once to bootstrap the modular layout.
After that, edit section files and use build-playbook.py to regenerate.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUSTOM_YML = os.path.join(ROOT, "Configuration", "custom.yml")
SECTIONS_DIR = os.path.join(ROOT, "Configuration", "sections")
HEADER_FILE = os.path.join(ROOT, "Configuration", "header.yml")


def split_playbook():
    """Split custom.yml into header.yml + sections/*.yml"""
    with open(CUSTOM_YML, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # --- Parse the header (everything before 'actions:') ---
    header_lines = []
    actions_start = None
    for i, line in enumerate(lines):
        if line.rstrip() == "actions:":
            actions_start = i
            break
        header_lines.append(line)

    if actions_start is None:
        print("ERROR: Could not find 'actions:' line in custom.yml", file=sys.stderr)
        sys.exit(1)

    # --- Write header.yml (header lines + 'actions:' key, no extra blank line) ---
    header_content = ''.join(header_lines)  # lines 1..actions_start-1
    # Include the 'actions:' line itself in the header
    header_content += lines[actions_start]  # "actions:\n" or "actions:\r\n"

    os.makedirs(os.path.dirname(HEADER_FILE), exist_ok=True)
    with open(HEADER_FILE, "w", encoding="utf-8") as f:
        f.write(header_content)
    print(f"  Created: {os.path.relpath(HEADER_FILE, ROOT)}")

    # --- Parse sections ---
    # Sections start with: "  # SECTION NN - Name"
    section_pattern = re.compile(r'^  # SECTION (\d+) - (.+)$')

    sections = []  # list of (section_num, section_name, start_line, end_line)
    current_section = None
    current_start = None

    # Find all section start positions
    for i, line in enumerate(lines):
        m = section_pattern.match(line)
        if m:
            if current_section:
                sections.append({
                    'num': current_section['num'],
                    'name': current_section['name'],
                    'start': current_start,
                    'end': i - 1,  # ends at line before next section / end of file
                })
            current_section = {
                'num': int(m.group(1)),
                'name': m.group(2).strip(),
            }
            current_start = i

    # Don't forget the last section
    if current_section:
        sections.append({
            'num': current_section['num'],
            'name': current_section['name'],
            'start': current_start,
            'end': len(lines) - 1,
        })

    # --- Create sections directory and write section files ---
    os.makedirs(SECTIONS_DIR, exist_ok=True)

    # Generate slug from section name
    def slugify(name):
        # Remove parenthetical content, lowercase, dash-separate words
        clean = re.sub(r'\([^)]*\)', '', name).strip()
        # Replace common non-filename chars
        clean = clean.replace('/', '-')
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean).strip('-').lower()
        return slug if slug else 'section'

    for sec in sections:
        num_str = f"{sec['num']:02d}"
        slug = slugify(sec['name'])
        filename = f"{num_str}-{slug}.yml"
        filepath = os.path.join(SECTIONS_DIR, filename)

        # Write section lines (2-space indented, as they appear in custom.yml)
        section_lines = lines[sec['start']:sec['end'] + 1]
        # Strip trailing empty lines (but keep trailing newline)
        content = ''.join(section_lines)
        # Ensure file ends with newline
        if not content.endswith('\n'):
            content += '\n'

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Created: sections/{filename} ({sec['num']}: {sec['name'][:50]})")

    print(f"\n  Header: {HEADER_FILE}")
    print(f"  Sections: {len(sections)} files in {SECTIONS_DIR}/")
    print(f"\nNext: Edit section files as needed, then run:")
    print(f"  python scripts/build-playbook.py")


if __name__ == "__main__":
    print("=== Splitting custom.yml into modular sections ===")
    print(f"  Source: {os.path.relpath(CUSTOM_YML, ROOT)}")
    split_playbook()
    print("\nDone!")
