#!/usr/bin/env python3
"""
Build registry.json — agentskills.io-compatible manifest.
Also generates REGISTRY.md index table.
"""

import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
SKILL_DIRS = [
    ("skills",          "built-in"),
    ("optional-skills", "optional"),
    ("lord1egypt-skills", "lord1egypt"),
]


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def collect_skills() -> list:
    skills = []
    for dir_name, source in SKILL_DIRS:
        d = ROOT / dir_name
        if not d.exists():
            continue
        for skill_md in sorted(d.rglob("SKILL.md")):
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            meta = parse_frontmatter(text)
            if not meta.get("name"):
                continue
            rel = skill_md.parent.relative_to(ROOT)
            skills.append({
                "name": meta.get("name", ""),
                "description": meta.get("description", ""),
                "version": str(meta.get("version", "1.0.0")),
                "author": meta.get("author", "community"),
                "license": meta.get("license", "MIT"),
                "category": meta.get("category", "other"),
                "tags": meta.get("tags", []),
                "platforms": meta.get("platforms", []),
                "compatible": meta.get("compatible", []),
                "source": source,
                "source_url": meta.get("source_url", ""),
                "local_path": str(rel),
                "install_cmd": f"awesome-skill-forge install {meta.get('name', '')}",
                "registry": "awesome-skill-forge",
            })
    return skills


def build_registry(skills: list) -> dict:
    by_cat = {}
    by_source = {}
    for s in skills:
        c = s["category"]
        src = s["source"]
        by_cat[c] = by_cat.get(c, 0) + 1
        by_source[src] = by_source.get(src, 0) + 1

    return {
        "registry": "awesome-skill-forge",
        "version": "1.0.1",
        "description": "Universal AI agent skill registry — Hermes-compatible SKILL.md format",
        "homepage": "https://github.com/Lord1Egypt/awesome-skill-forge",
        "author": "Lord1Egypt",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(skills),
        "by_category": dict(sorted(by_cat.items(), key=lambda x: x[1], reverse=True)),
        "by_source": dict(sorted(by_source.items(), key=lambda x: x[1], reverse=True)),
        "skills": skills,
    }


def build_registry_md(skills: list) -> str:
    by_cat = {}
    for s in skills:
        by_cat.setdefault(s["category"], []).append(s)

    lines = [
        "# REGISTRY",
        "",
        f"**{len(skills)} official skills** across {len(by_cat)} categories.",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "",
        "## By Category",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]
    for cat, cat_skills in sorted(by_cat.items(), key=lambda x: len(x[1]), reverse=True):
        lines.append(f"| {cat} | {len(cat_skills)} |")

    lines += ["", "## All Skills", "", "| Name | Description | Category | Source |", "|------|-------------|----------|--------|"]
    for s in sorted(skills, key=lambda x: x["name"]):
        name = s["name"]
        desc = (s["description"] or "")[:80]
        cat = s["category"]
        src = s["source"]
        lines.append(f"| `{name}` | {desc} | {cat} | {src} |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build registry.json and REGISTRY.md")
    parser.add_argument("--output", default=str(ROOT / "registry.json"))
    parser.add_argument("--md", default=str(ROOT / "REGISTRY.md"))
    parser.add_argument("--no-md", action="store_true", help="Skip REGISTRY.md generation")
    args = parser.parse_args()

    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required — pip install pyyaml")
        sys.exit(1)

    print("Collecting skills...")
    skills = collect_skills()
    print(f"Found {len(skills)} skills")

    registry = build_registry(skills)
    out = Path(args.output)
    out.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written: {out} ({out.stat().st_size // 1024}KB)")

    if not args.no_md:
        md = build_registry_md(skills)
        md_out = Path(args.md)
        md_out.write_text(md, encoding="utf-8")
        print(f"Written: {md_out}")


if __name__ == "__main__":
    main()
