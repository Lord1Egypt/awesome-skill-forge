#!/usr/bin/env python3
"""
Build the universal index.json from:
1. Raw skills_raw.json (90k skills from Hermes API)
2. Local SKILL.md files (170 official + lord1egypt custom)
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_JSON = os.path.join(ROOT, "data", "skills_raw.json")
OUTPUT_INDEX = os.path.join(ROOT, "index.json")
SKILLS_DIR = os.path.join(ROOT, "skills")
OPTIONAL_DIR = os.path.join(ROOT, "optional-skills")
LORD1EGYPT_DIR = os.path.join(ROOT, "lord1egypt-skills")

# Source display names
SOURCE_LABELS = {
    "built-in":  "Official Built-in",
    "optional":  "Official Optional",
    "ClawHub":   "ClawHub",
    "skills.sh": "skills.sh",
    "LobeHub":   "LobeHub",
    "browse.sh": "browse.sh",
    "gstack":    "gstack",
    "lord1egypt":"Lord1Egypt",
}

# Universal category mapping
CATEGORY_MAP = {
    "autonomous-ai-agents": "ai-agents",
    "software-development": "software-dev",
    "web-development": "software-dev",
    "data-science": "data-science",
    "social-media": "social-media",
    "smart-home": "smart-home",
    "red-teaming": "security",
    "note-taking": "productivity",
    "dogfood": "ai-agents",
    "yuanbao": "ai-agents",
    "other": "other",
}

def normalize_category(cat):
    return CATEGORY_MAP.get(cat, cat)

def parse_skill_md_frontmatter(path):
    """Parse SKILL.md frontmatter into a dict."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return {}

    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {}

    fm = {}
    raw = m.group(1)

    for key in ("name", "description", "version", "author", "license", "category", "source", "compatible"):
        km = re.search(rf'^{key}:\s*(.+)$', raw, re.MULTILINE)
        if km:
            val = km.group(1).strip().strip('"')
            fm[key] = val

    tags_m = re.search(r'^tags:\s*\[([^\]]*)\]', raw, re.MULTILINE)
    if tags_m:
        fm["tags"] = [t.strip() for t in tags_m.group(1).split(",") if t.strip()]

    platforms_m = re.search(r'^platforms:\s*\[([^\]]*)\]', raw, re.MULTILINE)
    if platforms_m:
        fm["platforms"] = [p.strip() for p in platforms_m.group(1).split(",") if p.strip()]

    return fm

def scan_local_skills(directory, default_source):
    """Scan a skills directory tree and return list of skill entries."""
    entries = []
    if not os.path.isdir(directory):
        return entries

    for skill_name in sorted(os.listdir(directory)):
        skill_path = os.path.join(directory, skill_name)
        if not os.path.isdir(skill_path):
            continue
        skill_md = os.path.join(skill_path, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue

        fm = parse_skill_md_frontmatter(skill_md)
        entries.append({
            "name": fm.get("name", skill_name),
            "description": fm.get("description", ""),
            "category": normalize_category(fm.get("category", "other")),
            "tags": fm.get("tags", []),
            "platforms": fm.get("platforms", ["linux", "macos", "windows"]),
            "author": fm.get("author", "community"),
            "version": fm.get("version", "1.0.0"),
            "license": fm.get("license", "MIT"),
            "source": fm.get("source", default_source),
            "sourceLabel": SOURCE_LABELS.get(fm.get("source", default_source), default_source),
            "compatible": ["claude-code", "openai-agents", "hermes-agent", "autogen", "langchain", "any-llm"],
            "hasContent": True,
            "localPath": os.path.relpath(skill_path, ROOT),
        })

    return entries

def transform_raw_entry(raw):
    """Convert a raw Hermes API entry to universal format."""
    source = raw.get("source", "community")
    name = raw.get("name", "")
    category = normalize_category(raw.get("category", "other"))

    # Clean up install command — remove hermes-specific prefix
    install_cmd = raw.get("installCmd", "")
    if install_cmd.startswith("hermes skills install "):
        identifier = install_cmd[len("hermes skills install "):].strip()
    else:
        identifier = raw.get("identifier", name)

    entry = {
        "name": name,
        "description": raw.get("description", ""),
        "category": category,
        "tags": raw.get("tags", []),
        "platforms": raw.get("platforms", []),
        "author": raw.get("author", "") or "community",
        "version": raw.get("version", "") or "1.0.0",
        "license": raw.get("license", "") or "MIT",
        "source": source,
        "sourceLabel": SOURCE_LABELS.get(source, source),
        "identifier": identifier,
        "sourceUrl": raw.get("sourceUrl", ""),
        "compatible": ["claude-code", "openai-agents", "hermes-agent", "autogen", "langchain", "any-llm"],
        "hasContent": False,  # content available via sourceUrl
    }

    # Add commands/envVars if present
    if raw.get("commands"):
        entry["requires_commands"] = raw["commands"]
    if raw.get("envVars"):
        entry["requires_env"] = raw["envVars"]

    return entry

def main():
    print("=== Building Universal Index ===\n")

    # Step 1: Load raw 90k data
    print(f"Loading {RAW_JSON}...")
    with open(RAW_JSON, encoding="utf-8") as f:
        raw_data = json.load(f)
    print(f"  Raw skills: {len(raw_data)}")

    # Step 2: Build lookup of local skills (to mark hasContent=True)
    local_names = set()

    print("\nScanning local skill files...")
    builtin_entries = scan_local_skills(SKILLS_DIR, "built-in")
    optional_entries = scan_local_skills(OPTIONAL_DIR, "optional")
    lord1egypt_entries = scan_local_skills(LORD1EGYPT_DIR, "lord1egypt")

    for e in builtin_entries + optional_entries + lord1egypt_entries:
        local_names.add(e["name"])

    print(f"  Built-in:  {len(builtin_entries)}")
    print(f"  Optional:  {len(optional_entries)}")
    print(f"  Lord1Egypt:{len(lord1egypt_entries)}")

    # Step 3: Transform all raw entries (skip ones we have locally)
    print("\nTransforming raw API entries...")
    community_entries = []
    skipped = 0
    for raw in raw_data:
        name = raw.get("name", "")
        if name in local_names:
            skipped += 1
            continue
        entry = transform_raw_entry(raw)
        community_entries.append(entry)
    print(f"  Community entries: {len(community_entries)} (skipped {skipped} already local)")

    # Step 4: Merge — lord1egypt first, then official, then community
    all_entries = lord1egypt_entries + builtin_entries + optional_entries + community_entries

    # Step 5: Build category stats
    by_source = {}
    by_category = {}
    has_content = 0
    for e in all_entries:
        src = e.get("source", "?")
        by_source[src] = by_source.get(src, 0) + 1
        cat = e.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + 1
        if e.get("hasContent"):
            has_content += 1

    # Step 6: Write index.json
    index = {
        "version": "1.0.0",
        "format": "Universal Skill Format (USF)",
        "description": "90k+ AI agent skills — works with Claude Code, OpenAI Agents, Hermes Agent, AutoGen, LangChain, and any LLM",
        "builtBy": "Lord1Egypt/awesome-skill-forge",
        "totalSkills": len(all_entries),
        "skillsWithContent": has_content,
        "bySource": by_source,
        "byCategory": by_category,
        "skills": all_entries,
    }

    with open(OUTPUT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

    size_mb = os.path.getsize(OUTPUT_INDEX) / 1024 / 1024
    print(f"\nWrote {OUTPUT_INDEX}")
    print(f"  Total: {len(all_entries)} skills ({size_mb:.1f} MB)")
    print(f"  With content: {has_content}")
    print(f"  By source: {json.dumps(by_source, indent=4)}")

if __name__ == "__main__":
    main()
