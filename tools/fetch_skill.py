#!/usr/bin/env python3
"""
Fetch content for any community skill by sourceUrl.
Usage: python3 fetch_skill.py <skill-name-or-sourceUrl>

Supports:
  - skills.sh URLs   → fetch raw markdown from skills.sh API
  - ClawHub URLs     → fetch skill page text
  - GitHub URLs      → fetch raw content from GitHub
  - LobeHub          → fetch from LobeHub API
  - gstack (GitHub)  → same as GitHub
"""

import sys
import json
import os
import re
import urllib.request
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.json")
OUTPUT_DIR = os.path.join(ROOT, "fetched-skills")

HEADERS = {
    "User-Agent": "awesome-skill-forge/1.0",
    "Accept": "application/json, text/plain, */*",
}

def load_index():
    with open(INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)

def find_skill(index, query):
    for skill in index["skills"]:
        if skill["name"].lower() == query.lower():
            return skill
        if skill.get("identifier", "").lower() == query.lower():
            return skill
    return None

def fetch_url(url, as_json=False):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        content = r.read().decode("utf-8")
    if as_json:
        return json.loads(content)
    return content

def fetch_github_skill(url):
    """Fetch content from a GitHub tree URL (convert to raw content)."""
    # Convert tree URL to raw API
    # https://github.com/garrytan/gstack/tree/main/autoplan
    # -> https://api.github.com/repos/garrytan/gstack/contents/autoplan
    m = re.match(r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)', url)
    if not m:
        return None
    owner, repo, branch, path = m.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    try:
        files = fetch_url(api_url, as_json=True)
    except Exception as e:
        return f"ERROR fetching GitHub: {e}"

    if isinstance(files, list):
        # Look for SKILL.md, skill.md, README.md, or any .md file
        for fname_pref in ("SKILL.md", "skill.md", "README.md"):
            for f in files:
                if f.get("name") == fname_pref and f.get("download_url"):
                    return fetch_url(f["download_url"])
        # Fallback: any .md
        for f in files:
            if f.get("name","").endswith(".md") and f.get("download_url"):
                return fetch_url(f["download_url"])
    elif isinstance(files, dict) and files.get("download_url"):
        return fetch_url(files["download_url"])
    return None

def fetch_skillssh_skill(url):
    """Fetch from skills.sh — convert to raw content URL."""
    # https://skills.sh/author/repo/skill-name
    # skills.sh may have a raw content endpoint
    raw_url = url.rstrip("/") + "/raw"
    try:
        return fetch_url(raw_url)
    except Exception:
        pass
    # Fallback: just GET the page
    try:
        return fetch_url(url)
    except Exception as e:
        return f"ERROR: {e}"

def fetch_lobehub_skill(identifier):
    """Fetch from LobeHub agents API."""
    # identifier: lobehub/agent-name
    parts = identifier.split("/")
    agent_id = parts[-1] if parts else identifier
    api_url = f"https://chat-agents.lobehub.com/agent/{agent_id}"
    try:
        data = fetch_url(api_url, as_json=True)
        system_role = data.get("config", {}).get("systemRole", "")
        name = data.get("meta", {}).get("title", agent_id)
        desc = data.get("meta", {}).get("description", "")
        return f"# {name}\n\n{desc}\n\n## System Prompt\n\n{system_role}"
    except Exception as e:
        return f"ERROR fetching LobeHub: {e}"

def build_universal_skill_md(skill, content):
    """Wrap fetched content in Universal Skill Format frontmatter."""
    name = skill.get("name", "unknown")
    description = skill.get("description", "")
    category = skill.get("category", "other")
    tags = skill.get("tags", [])
    platforms = skill.get("platforms", ["linux", "macos", "windows"])
    author = skill.get("author", "community")
    version = skill.get("version", "1.0.0")
    license_val = skill.get("license", "MIT")
    source = skill.get("source", "community")
    source_url = skill.get("sourceUrl", "")

    tags_str = ", ".join(tags) if tags else ""
    plat_str = ", ".join(platforms) if platforms else "linux, macos, windows"

    fm = f"""---
name: {name}
description: "{description}"
version: {version}
author: {author}
license: {license_val}
platforms: [{plat_str}]
category: {category}
tags: [{tags_str}]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: {source}
source_url: {source_url}
---

{content}
"""
    return fm

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_skill.py <skill-name>")
        print("       python3 fetch_skill.py <sourceUrl>")
        sys.exit(1)

    query = sys.argv[1]
    index = load_index()

    # Find skill in index
    skill = find_skill(index, query)
    if not skill:
        print(f"Skill '{query}' not found in index")
        sys.exit(1)

    source = skill.get("source", "")
    source_url = skill.get("sourceUrl", "")
    identifier = skill.get("identifier", "")

    print(f"Fetching: {skill['name']} (source: {source})")
    print(f"URL: {source_url}")

    content = None

    if source in ("built-in", "optional", "lord1egypt"):
        print("This skill already has local content.")
        sys.exit(0)
    elif source == "gstack" or "github.com" in source_url:
        content = fetch_github_skill(source_url)
    elif source == "skills.sh":
        content = fetch_skillssh_skill(source_url)
    elif source == "LobeHub":
        content = fetch_lobehub_skill(identifier)
    elif source == "ClawHub":
        print(f"ClawHub skills require browser access: {source_url}")
        print("Manual fetch needed for ClawHub content.")
        sys.exit(1)
    else:
        print(f"Unknown source: {source}")
        sys.exit(1)

    if not content:
        print("Could not fetch content")
        sys.exit(1)

    # Save to fetched-skills/
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_name = re.sub(r'[^\w\-]', '_', skill['name'])[:80]
    skill_dir = os.path.join(OUTPUT_DIR, safe_name)
    os.makedirs(skill_dir, exist_ok=True)

    skill_md = build_universal_skill_md(skill, content)
    out_path = os.path.join(skill_dir, "SKILL.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
