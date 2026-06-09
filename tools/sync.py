#!/usr/bin/env python3
"""
Auto-sync official skills from hermes-agent.nousresearch.com.
Fetches built-in and optional skills, writes SKILL.md files, rebuilds index.
"""

import json
import os
import re
import sys
import time
import zipfile
import argparse
import urllib.request
import urllib.error
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).parent.parent
HERMES_BASE = "https://hermes-agent.nousresearch.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"User-Agent": "awesome-skill-forge/1.0"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def fetch(url: str, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"  rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif e.code in (404, 403):
                raise
            else:
                time.sleep(2)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2)
    raise RuntimeError(f"Failed after {retries} attempts: {url}")


def fetch_json(url: str) -> dict:
    return json.loads(fetch(url))


def get_skill_list() -> list:
    data = fetch_json(f"{HERMES_BASE}/api/v1/skills?limit=500&type=built-in")
    skills = data.get("skills", [])
    data2 = fetch_json(f"{HERMES_BASE}/api/v1/skills?limit=500&type=optional")
    skills += data2.get("skills", [])
    return skills


def fetch_skill_zip(slug: str, version: str) -> str | None:
    url = f"{HERMES_BASE}/api/v1/download?slug={slug}&version={version}"
    try:
        raw = fetch(url)
        zf = zipfile.ZipFile(BytesIO(raw))
        for name in zf.namelist():
            if name.endswith("SKILL.md"):
                return zf.read(name).decode("utf-8", errors="replace")
    except Exception:
        pass
    return None


def fetch_skill_raw(slug: str) -> str | None:
    url = f"{HERMES_BASE}/skills/{slug}/raw"
    try:
        return fetch(url).decode("utf-8", errors="replace")
    except Exception:
        return None


def skill_dir(skill: dict) -> Path:
    skill_type = skill.get("type", "built-in")
    slug = skill.get("slug", skill.get("name", "unknown"))
    slug_safe = re.sub(r"[^\w\-]", "_", slug).lower()[:80]
    if skill_type == "optional":
        return ROOT / "optional-skills" / slug_safe
    return ROOT / "skills" / slug_safe


def needs_update(path: Path, remote_version: str) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
    if not m:
        return True
    return m.group(1).strip() != str(remote_version)


def sync_skill(skill: dict, dry_run: bool = False) -> str:
    slug = skill.get("slug", skill.get("name", ""))
    version = str(skill.get("version", "1.0.0"))
    out_dir = skill_dir(skill)
    out_file = out_dir / "SKILL.md"

    if not needs_update(out_file, version):
        return "skip"

    content = fetch_skill_zip(slug, version) or fetch_skill_raw(slug)
    if not content:
        return "fail"

    if dry_run:
        return "would-update"

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file.write_text(content, encoding="utf-8")
    return "updated"


def main():
    parser = argparse.ArgumentParser(description="Sync official skills from Hermes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--type", choices=["built-in", "optional", "all"], default="all")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild index after sync")
    args = parser.parse_args()

    print("Fetching skill list from Hermes...")
    try:
        skills = get_skill_list()
    except Exception as e:
        print(f"ERROR: Failed to fetch skill list: {e}")
        sys.exit(1)

    if args.type != "all":
        skills = [s for s in skills if s.get("type") == args.type]

    print(f"Found {len(skills)} skills to check")

    counts = {"updated": 0, "skip": 0, "fail": 0, "would-update": 0}
    for skill in skills:
        slug = skill.get("slug", skill.get("name", "?"))
        result = sync_skill(skill, dry_run=args.dry_run)
        counts[result] = counts.get(result, 0) + 1
        if result not in ("skip",):
            print(f"  [{result:12}] {slug}")
        time.sleep(0.1)

    print(f"\nSync complete: {counts['updated']} updated, {counts['skip']} unchanged, {counts['fail']} failed")

    if args.rebuild and counts["updated"] > 0:
        print("\nRebuilding index...")
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "tools" / "build_index.py")], check=True)


if __name__ == "__main__":
    main()
