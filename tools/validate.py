#!/usr/bin/env python3
"""Validate all SKILL.md files in the registry."""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_DIRS = ["skills", "optional-skills", "lord1egypt-skills"]
REQUIRED_FIELDS = ["name", "description", "category"]
VALID_CATEGORIES = {
    # Hermes official categories
    "ai-agents", "autonomous-ai-agents", "software-dev", "software-development",
    "productivity", "apple", "blockchain", "gaming", "security", "data-science",
    "devops", "finance", "writing", "research", "media", "communication",
    "education", "web-development", "mobile", "design", "testing", "database",
    "networking", "other",
    # Extended categories used in the wild
    "creative", "mlops", "mcp", "github", "email", "note-taking", "smart-home",
    "social-media", "health", "migration", "red-teaming", "dogfood",
    "autonomous-agents", "data-engineering", "infrastructure",
}

errors = []
warnings = []
checked = 0


def parse_skill_md(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    if not m:
        return None, None
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, str(e)
    body = m.group(2).strip()
    return meta, body


def validate_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    global checked
    checked += 1

    meta, body = parse_skill_md(path)

    if meta is None:
        errors.append(f"{rel}: missing or invalid YAML frontmatter — {body}")
        return False

    ok = True

    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            errors.append(f"{rel}: missing required field '{field}'")
            ok = False

    cat = meta.get("category", "")
    if cat and cat not in VALID_CATEGORIES:
        warnings.append(f"{rel}: unknown category '{cat}'")

    name = meta.get("name", "")
    if name and " " in name:
        warnings.append(f"{rel}: skill name '{name}' contains spaces (use hyphens)")

    if not body or len(body) < 50:
        warnings.append(f"{rel}: body content is very short ({len(body)} chars)")

    return ok


def main():
    parser = argparse.ArgumentParser(description="Validate SKILL.md files")
    parser.add_argument("--dir", help="Specific directory to validate")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="Only show errors")
    args = parser.parse_args()

    dirs = [ROOT / args.dir] if args.dir else [ROOT / d for d in SKILL_DIRS]

    for d in dirs:
        if not d.exists():
            continue
        for skill_md in sorted(d.rglob("SKILL.md")):
            validate_file(skill_md)

    if not args.quiet:
        for w in warnings:
            print(f"  WARN  {w}")

    for e in errors:
        print(f" ERROR  {e}")

    total_issues = len(errors) + (len(warnings) if args.strict else 0)

    print(f"\nChecked {checked} SKILL.md files — {len(errors)} errors, {len(warnings)} warnings")

    if total_issues > 0:
        sys.exit(1)
    else:
        print("All files valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
