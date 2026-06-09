"""
On-demand content fetcher for community skills.
Called by loader.load() when fetch=True and skill has no embedded content.
Zero external dependencies — stdlib only.
"""

import base64
import io
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile

CLAWHUB_API = "https://clawhub.ai/api/v1"
LOBEHUB_RAW = "https://raw.githubusercontent.com/lobehub/lobe-chat-agents/main/src"
GITHUB_API = "https://api.github.com"

_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def _headers(github: bool = False) -> dict:
    h = {"User-Agent": "awesome-skill-forge/1.0"}
    if github and _TOKEN:
        h["Authorization"] = f"Bearer {_TOKEN}"
        h["Accept"] = "application/vnd.github+json"
    return h


def _get(url: str, *, github: bool = False, as_json: bool = False,
         as_bytes: bool = False, timeout: int = 20):
    req = urllib.request.Request(url, headers=_headers(github))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
        if as_bytes:
            return raw
        if as_json:
            return json.loads(raw)
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return None


def _github_file(repo: str, path: str) -> str | None:
    url = f"{GITHUB_API}/repos/{repo}/contents/{urllib.parse.quote(path)}"
    data = _get(url, github=True, as_json=True)
    if not isinstance(data, dict):
        return None
    if data.get("encoding") == "base64" and data.get("content"):
        try:
            return base64.b64decode(data["content"].replace("\n", "")).decode("utf-8", errors="replace")
        except Exception:
            return None
    dl = data.get("download_url")
    return _get(dl, github=True) if dl else None


def _fetch_clawhub(slug: str) -> str | None:
    meta = _get(f"{CLAWHUB_API}/skills/{slug}", as_json=True)
    if not isinstance(meta, dict):
        return None
    skill = meta.get("skill", meta)
    lv = meta.get("latestVersion") or skill.get("latestVersion")
    version = None
    if isinstance(lv, dict):
        version = lv.get("version")
    if not version:
        tags = skill.get("tags", {})
        version = tags.get("latest") if isinstance(tags, dict) else None
    if not version:
        return None
    raw = _get(
        f"{CLAWHUB_API}/download?slug={slug}&version={urllib.parse.quote(str(version))}",
        as_bytes=True, timeout=40,
    )
    if not raw:
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for name in zf.namelist():
                if name.lower().endswith("skill.md"):
                    return zf.read(name).decode("utf-8", errors="replace")
    except Exception:
        return None
    return None


def _fetch_lobehub(identifier: str) -> str | None:
    agent_id = identifier.split("/")[-1]
    data = _get(f"{LOBEHUB_RAW}/{agent_id}.json", as_json=True)
    if not isinstance(data, dict):
        return None
    cfg = data.get("config", {})
    meta = data.get("meta", {})
    body = cfg.get("systemRole", "").strip()
    if not body:
        return None
    title = meta.get("title", agent_id)
    desc = meta.get("description", "")
    tags = meta.get("tags", [])
    return (
        f"---\nname: {agent_id}\ndescription: \"{desc}\"\n"
        f"source: LobeHub\ntags: [{', '.join(tags)}]\n"
        f"compatible: [claude-code, openai-agents, hermes-agent, any-llm]\n---\n\n"
        f"# {title}\n\n{body}\n"
    )


def _fetch_skills_sh(identifier: str) -> str | None:
    ident = re.sub(r"^skills[-_]sh/", "", identifier)
    parts = ident.split("/")
    if len(parts) < 3:
        return None
    repo = f"{parts[0]}/{parts[1]}"
    skill = "/".join(parts[2:])
    for path in (
        f"skills/{skill}/SKILL.md",
        f".agents/skills/{skill}/SKILL.md",
        f"{skill}/SKILL.md",
        f"plugins/{parts[1]}-claude/skills/{skill}/SKILL.md",
        f"src/{skill}/SKILL.md",
    ):
        content = _github_file(repo, path)
        if content and len(content) > 80:
            return content
    return None


def _fetch_gstack(source_url: str) -> str | None:
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/[^/]+/(.+)", source_url)
    if not m:
        return None
    return _github_file(m.group(1), f"{m.group(2).rstrip('/')}/SKILL.md")


def fetch_content(meta: dict) -> str | None:
    """
    Fetch full SKILL.md content for a community skill on demand.
    Returns content string or None if unavailable.
    """
    source = meta.get("source", "")
    identifier = meta.get("identifier", meta.get("localPath", ""))
    source_url = meta.get("sourceUrl", "")

    if source == "ClawHub":
        slug = identifier.split("/")[-1]
        return _fetch_clawhub(slug)
    elif source == "LobeHub":
        return _fetch_lobehub(identifier)
    elif source == "skills.sh":
        return _fetch_skills_sh(identifier)
    elif source == "gstack":
        return _fetch_gstack(source_url)
    return None
