"""
Sync community skill metadata from upstream sources.
Checks for NEW skills not already in index.json and adds them.
Does NOT re-download content — metadata only.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_FILE = os.path.join(ROOT, "index.json")

CLAWHUB_API  = "https://clawhub.ai/api/v1"
GITHUB_API   = "https://api.github.com"
_TOKEN       = os.environ.get("GITHUB_TOKEN", "")


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _get(url, *, github=False, as_json=False, timeout=20, retries=3):
    headers = {"User-Agent": "awesome-skill-forge-sync/1.0"}
    if github and _TOKEN:
        headers["Authorization"] = f"Bearer {_TOKEN}"
        headers["Accept"] = "application/vnd.github+json"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
            return json.loads(raw) if as_json else raw.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s…", flush=True)
                time.sleep(wait)
            elif e.code in (403, 404):
                return None
            else:
                if attempt == retries - 1:
                    return None
                time.sleep(5)
        except Exception:
            if attempt == retries - 1:
                return None
            time.sleep(5)
    return None


# ── ClawHub ───────────────────────────────────────────────────────────────────

def fetch_clawhub_page(page=1, page_size=100):
    url = f"{CLAWHUB_API}/skills?page={page}&pageSize={page_size}"
    data = _get(url, as_json=True)
    if not isinstance(data, dict):
        return [], 0
    items = data.get("data", data.get("skills", data.get("items", [])))
    total = data.get("total", data.get("totalCount", 0))
    return items, total


def clawhub_to_meta(item):
    slug = item.get("slug", "")
    name = item.get("name", item.get("title", slug))
    return {
        "name": name,
        "description": (item.get("description", "") or "")[:300],
        "category": (item.get("category", item.get("tags", [""])) or [""])[0] if isinstance(
            item.get("category"), list) else item.get("category", ""),
        "tags": item.get("tags", [])[:10] if isinstance(item.get("tags"), list) else [],
        "platforms": [],
        "author": item.get("author", {}).get("name", "community") if isinstance(
            item.get("author"), dict) else item.get("author", "community"),
        "version": "1.0.0",
        "license": "MIT",
        "source": "ClawHub",
        "sourceLabel": "ClawHub",
        "identifier": f"clawhub/{slug}",
        "sourceUrl": f"https://clawhub.ai/skills/{slug}",
        "compatible": ["claude-code", "openai-agents", "hermes-agent", "autogen", "langchain", "any-llm"],
        "hasContent": False,
        "localPath": "",
    }


def sync_clawhub(existing_ids):
    print("Syncing ClawHub…", flush=True)
    added = []
    page = 1
    while True:
        items, total = fetch_clawhub_page(page)
        if not items:
            break
        for item in items:
            slug = item.get("slug", "")
            if not slug:
                continue
            iid = f"clawhub/{slug}"
            if iid not in existing_ids:
                meta = clawhub_to_meta(item)
                added.append(meta)
                existing_ids.add(iid)
        print(f"  Page {page} — {len(added)} new so far (total: {total})", flush=True)
        if len(items) < 100:
            break
        page += 1
        time.sleep(0.5)
    return added


# ── LobeHub ───────────────────────────────────────────────────────────────────

def sync_lobehub(existing_ids):
    print("Syncing LobeHub…", flush=True)
    url = f"{GITHUB_API}/repos/lobehub/lobe-chat-agents/contents/src"
    items = _get(url, github=True, as_json=True)
    if not isinstance(items, list):
        print("  Could not reach LobeHub API", flush=True)
        return []

    added = []
    for item in items:
        if item.get("type") != "file" or not item["name"].endswith(".json"):
            continue
        agent_id = item["name"].replace(".json", "")
        iid = f"lobehub/{agent_id}"
        if iid in existing_ids:
            continue

        raw_url = item.get("download_url", "")
        data = _get(raw_url, as_json=True) if raw_url else None
        if not isinstance(data, dict):
            continue

        meta = {
            "name": data.get("meta", {}).get("title", agent_id),
            "description": (data.get("meta", {}).get("description", "") or "")[:300],
            "category": (data.get("meta", {}).get("tags", ["ai-agents"]) or ["ai-agents"])[0],
            "tags": data.get("meta", {}).get("tags", [])[:10],
            "platforms": [],
            "author": data.get("author", {}).get("name", "LobeHub") if isinstance(
                data.get("author"), dict) else "LobeHub",
            "version": "1.0.0",
            "license": "MIT",
            "source": "LobeHub",
            "sourceLabel": "LobeHub",
            "identifier": iid,
            "sourceUrl": f"https://lobehub.com/agents/{agent_id}",
            "compatible": ["claude-code", "openai-agents", "hermes-agent", "autogen", "langchain", "any-llm"],
            "hasContent": False,
            "localPath": "",
        }
        added.append(meta)
        existing_ids.add(iid)
        time.sleep(0.1)

    print(f"  {len(added)} new LobeHub skills", flush=True)
    return added


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Loading {INDEX_FILE}…", flush=True)
    with open(INDEX_FILE, encoding="utf-8") as f:
        index = json.load(f)

    skills = index["skills"]

    # Build set of existing identifiers (identifier field or name)
    existing_ids = set()
    for s in skills:
        if s.get("identifier"):
            existing_ids.add(s["identifier"])

    print(f"Existing skills: {len(skills)}", flush=True)

    new_skills = []
    new_skills += sync_clawhub(existing_ids)
    new_skills += sync_lobehub(existing_ids)

    if not new_skills:
        print("No new skills found.", flush=True)
        return 0

    print(f"\nAdding {len(new_skills)} new skills…", flush=True)
    skills.extend(new_skills)

    # Update index stats
    index["totalSkills"] = len(skills)
    index["skillsWithContent"] = sum(1 for s in skills if s.get("hasContent"))

    by_source = {}
    by_cat    = {}
    for s in skills:
        src = s.get("source", "unknown")
        cat = s.get("category", "")
        by_source[src] = by_source.get(src, 0) + 1
        if cat:
            by_cat[cat] = by_cat.get(cat, 0) + 1

    index["bySource"]   = by_source
    index["byCategory"] = dict(sorted(by_cat.items(), key=lambda x: -x[1]))

    print(f"Writing {INDEX_FILE}…", flush=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Done. Total skills: {len(skills)}", flush=True)
    return len(new_skills)


if __name__ == "__main__":
    n = main()
    sys.exit(0)
