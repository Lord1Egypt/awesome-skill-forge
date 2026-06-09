#!/usr/bin/env python3
"""
Fetch all 170 official skills (built-in + optional) from NousResearch/hermes-agent
and transform them to Universal Skill Format.
"""

import urllib.request
import json
import os
import re
import time
import sys

BASE_API = "https://api.github.com/repos/NousResearch/hermes-agent/contents"
RAW_BASE = "https://raw.githubusercontent.com/NousResearch/hermes-agent/main"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")
OUTPUT_OPT = os.path.join(os.path.dirname(__file__), "..", "optional-skills")

_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"User-Agent": "awesome-skill-forge/1.0"}
if _TOKEN:
    HEADERS["Authorization"] = f"Bearer {_TOKEN}"

def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def get_text(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

def transform_skill_md(content, skill_name, category, source_type):
    """
    Transform Hermes SKILL.md to Universal Skill Format.
    Removes hermes-specific metadata, makes compatible with any agent.
    """
    # Extract frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not fm_match:
        return content

    frontmatter_raw = fm_match.group(1)
    body = fm_match.group(2)

    # Parse key fields from frontmatter
    name_m = re.search(r'^name:\s*(.+)$', frontmatter_raw, re.MULTILINE)
    desc_m = re.search(r'^description:\s*(.+)$', frontmatter_raw, re.MULTILINE)
    ver_m = re.search(r'^version:\s*(.+)$', frontmatter_raw, re.MULTILINE)
    author_m = re.search(r'^author:\s*(.+)$', frontmatter_raw, re.MULTILINE)
    license_m = re.search(r'^license:\s*(.+)$', frontmatter_raw, re.MULTILINE)
    platforms_m = re.search(r'^platforms:\s*(.+)$', frontmatter_raw, re.MULTILINE)

    # Extract tags from hermes metadata block
    tags_m = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter_raw)
    tags = []
    if tags_m:
        tags = [t.strip() for t in tags_m.group(1).split(',')]

    # Extract prerequisites
    prereq_commands = re.search(r'commands:\s*\[([^\]]*)\]', frontmatter_raw)
    prereq_envs = re.search(r'env_vars:\s*\[([^\]]*)\]', frontmatter_raw)

    name = name_m.group(1).strip() if name_m else skill_name
    description = desc_m.group(1).strip().strip('"') if desc_m else ""
    version = ver_m.group(1).strip() if ver_m else "1.0.0"
    author = author_m.group(1).strip() if author_m else "community"
    # Replace Hermes Agent authorship with community attribution
    if author.lower() in ("hermes agent", "hermes-agent", "hermes"):
        author = "community"
    license_val = license_m.group(1).strip() if license_m else "MIT"
    platforms = platforms_m.group(1).strip() if platforms_m else "[linux, macos, windows]"

    commands_val = prereq_commands.group(1).strip() if prereq_commands else ""
    envs_val = prereq_envs.group(1).strip() if prereq_envs else ""

    # Build universal frontmatter (no Hermes-specific fields)
    new_fm_lines = [
        f"name: {name}",
        f'description: "{description}"',
        f"version: {version}",
        f"author: {author}",
        f"license: {license_val}",
        f"platforms: {platforms}",
        f"category: {category}",
    ]
    if tags:
        tags_str = ", ".join(tags)
        new_fm_lines.append(f"tags: [{tags_str}]")
    if commands_val:
        new_fm_lines.append(f"requires_commands: [{commands_val}]")
    if envs_val:
        new_fm_lines.append(f"requires_env: [{envs_val}]")

    # Universal compatibility — works with Claude Code, any LLM agent
    new_fm_lines.append("compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]")
    new_fm_lines.append(f"source: {source_type}")

    new_frontmatter = "\n".join(new_fm_lines)

    # Clean body — remove any "hermes" tool references in prose (keep commands)
    body_clean = body

    return f"---\n{new_frontmatter}\n---\n{body_clean}"

def fetch_skill_dir(api_url, output_root, category, source_type, skill_name):
    """Fetch all files in a skill directory and write to output."""
    try:
        files = get_json(api_url)
    except Exception as e:
        print(f"  ERROR listing {skill_name}: {e}")
        return False

    skill_dir = os.path.join(output_root, skill_name)
    os.makedirs(skill_dir, exist_ok=True)

    for f in files:
        if f["type"] != "file":
            continue
        fname = f["name"]
        try:
            content = get_text(f["download_url"])
            if fname == "SKILL.md":
                content = transform_skill_md(content, skill_name, category, source_type)
            out_path = os.path.join(skill_dir, fname)
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(content)
        except Exception as e:
            print(f"    WARN: could not fetch {fname}: {e}")
        time.sleep(0.1)

    return True

def fetch_category(base_path, output_root, source_type):
    """Fetch all skill directories in a category path."""
    try:
        items = get_json(f"{BASE_API}/{base_path}")
    except Exception as e:
        print(f"ERROR listing {base_path}: {e}")
        return 0

    count = 0
    for cat_item in items:
        if cat_item["type"] != "dir":
            continue
        category = cat_item["name"]
        if category == "index-cache":
            continue

        print(f"  Category: {category}")
        try:
            skill_items = get_json(cat_item["url"])
        except Exception as e:
            print(f"    ERROR listing category: {e}")
            continue

        for skill_item in skill_items:
            if skill_item["type"] != "dir":
                continue
            skill_name = skill_item["name"]
            print(f"    Fetching: {skill_name}")
            ok = fetch_skill_dir(skill_item["url"], output_root, category, source_type, skill_name)
            if ok:
                count += 1
            time.sleep(0.3)

    return count

def main():
    print("=== awesome-skill-forge: Fetching Official Skills ===\n")

    # Built-in skills
    print("Fetching built-in skills...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    n_builtin = fetch_category("skills", OUTPUT_DIR, "built-in")
    print(f"  Done: {n_builtin} built-in skills\n")

    # Optional skills
    print("Fetching optional skills...")
    os.makedirs(OUTPUT_OPT, exist_ok=True)
    n_optional = fetch_category("optional-skills", OUTPUT_OPT, "optional")
    print(f"  Done: {n_optional} optional skills\n")

    print(f"Total official skills fetched: {n_builtin + n_optional}")

if __name__ == "__main__":
    main()
