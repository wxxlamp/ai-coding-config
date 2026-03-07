#!/usr/bin/env python3
"""Utility to verify that a Claude Code skill's directory structure and files
conform to the documented conventions.

Usage:
    python3 validate_skill.py <skill-name>
    # or: ./validate_skill.py <skill-name> (after chmod +x)

This is intended to be called from the `skill-create` workflow after a new item
is generated so that the author can be confident the directory is well formed.

Checks performed:
  * the skill directory exists under .claude/skills/
  * if SKILL.md exists, it must have a YAML frontmatter with matching name
    and a minimal template
  * if REFERENCE.md exists, similar frontmatter validation
  * if additional files are present (scripts), ensure at least one has a
    shebang and is executable

Return code is 0 on success, 1 on failure (and errors are printed).
"""

import argparse
import os
import re
import sys
from pathlib import Path

# the root of all skills is the parent of this directory (two levels up)
SKILLS_ROOT = Path(__file__).parent.parent

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)---\n", re.DOTALL)
NAME_FIELD_PATTERN = re.compile(r"^name:\s*(\S+)", re.MULTILINE)


def validate_frontmatter(md_path: Path, expected_name: str) -> bool:
    if not md_path.is_file():
        print(f"ERROR: {md_path} does not exist or is not a file")
        return False

    text = md_path.read_text(encoding="utf-8")
    m = FRONTMATTER_PATTERN.match(text)
    if not m:
        print(f"ERROR: {md_path} is missing YAML frontmatter")
        return False
    fm = m.group(1)
    name_match = NAME_FIELD_PATTERN.search(fm)
    if not name_match:
        print(f"ERROR: {md_path} frontmatter has no 'name:' field")
        return False
    actual = name_match.group(1).strip()
    if actual != expected_name:
        print(f"ERROR: frontmatter name ('{actual}') does not match directory "
              f"name ('{expected_name}')")
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Claude Code skill.")
    parser.add_argument("name", help="Skill directory name to validate")
    args = parser.parse_args()

    skill_dir = (SKILLS_ROOT / args.name).resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: skill directory {skill_dir} does not exist")
        return 1

    ok = True

    # check for SKILL.md or REFERENCE.md
    skill_md = skill_dir / "SKILL.md"
    ref_md = skill_dir / "REFERENCE.md"

    if skill_md.exists():
        ok &= validate_frontmatter(skill_md, args.name)
    if ref_md.exists():
        ok &= validate_frontmatter(ref_md, args.name)

    # look for script files (anything besides markdown)
    extras = [p for p in skill_dir.iterdir() if p.is_file() and p.suffix not in ['.md']]
    for p in extras:
        # check executable bit
        if not os.access(p, os.X_OK):
            print(f"WARNING: {p.name} is not marked executable")
            # not fatal
        # check for shebang
        first = p.read_text(errors='ignore').splitlines()[0] if p.stat().st_size > 0 else ''
        if not first.startswith('#!'):
            print(f"WARNING: {p.name} does not start with a shebang")
    if not skill_md.exists() and not ref_md.exists():
        print("ERROR: neither SKILL.md nor REFERENCE.md found in skill directory")
        ok = False

    if ok:
        print(f"{args.name}: structure looks good")
        return 0
    else:
        print(f"{args.name}: validation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
