"""
Lazy-loading skill engine for forge-skills.
Index is loaded once; skill content is read only when requested.
"""

import json
import os
import re
from typing import Optional, List, Dict, Any

# Path resolution — works installed or from source
_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_PACKAGE_DIR))  # project root when dev
_INDEX_FILE = os.path.join(_PACKAGE_DIR, "data", "index.json")
if not os.path.isfile(_INDEX_FILE):
    _INDEX_FILE = os.path.join(_ROOT, "index.json")

_index_cache: Optional[Dict] = None


def _load_index() -> Dict:
    global _index_cache
    if _index_cache is None:
        with open(_INDEX_FILE, encoding="utf-8") as f:
            _index_cache = json.load(f)
    return _index_cache


class Skill:
    """A loaded skill with metadata and full prompt content."""

    def __init__(self, meta: Dict, content: str):
        self.name: str = meta.get("name", "")
        self.description: str = meta.get("description", "")
        self.category: str = meta.get("category", "")
        self.tags: List[str] = meta.get("tags", [])
        self.platforms: List[str] = meta.get("platforms", [])
        self.author: str = meta.get("author", "community")
        self.version: str = meta.get("version", "1.0.0")
        self.license: str = meta.get("license", "MIT")
        self.source: str = meta.get("source", "")
        self.source_url: str = meta.get("sourceUrl", "")
        self.compatible: List[str] = meta.get("compatible", [])
        self.local_path: str = meta.get("localPath", "")
        self.has_content: bool = meta.get("hasContent", False)
        self.prompt: str = content
        self._meta = meta

    def __str__(self) -> str:
        return self.prompt

    def __repr__(self) -> str:
        return f"<Skill name={self.name!r} category={self.category!r} source={self.source!r}>"


def _read_skill_content(meta: Dict) -> str:
    """Read SKILL.md content — from embedded content first, then local path."""
    # Embedded content (pre-loaded in index.json for official skills)
    if meta.get("content"):
        return meta["content"]

    local_path = meta.get("localPath", "")
    if not local_path:
        return meta.get("description", "")

    # Try relative to package dir first, then project root
    for base in [_PACKAGE_DIR, _ROOT]:
        skill_md = os.path.join(base, local_path, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md, encoding="utf-8") as f:
                raw = f.read()
            m = re.match(r'^---\n.*?\n---\n(.*)', raw, re.DOTALL)
            return m.group(1).strip() if m else raw

    return meta.get("description", "")


def load(name: str, category: Optional[str] = None, source: Optional[str] = None) -> Skill:
    """
    Load a skill by name. Returns a Skill object with full content.

    Args:
        name: Skill name (exact match, case-insensitive)
        category: Optional category filter (e.g. "ai-agents", "productivity")
        source: Optional source filter (e.g. "built-in", "ClawHub", "lord1egypt")

    Returns:
        Skill object

    Raises:
        KeyError: If skill not found
    """
    index = _load_index()
    name_lower = name.lower()

    for meta in index["skills"]:
        if meta["name"].lower() != name_lower:
            continue
        if category and meta.get("category", "").lower() != category.lower():
            continue
        if source and meta.get("source", "").lower() != source.lower():
            continue

        content = _read_skill_content(meta) if meta.get("hasContent") else meta.get("description", "")
        return Skill(meta, content)

    raise KeyError(f"Skill not found: '{name}'")


def search(
    query: str,
    category: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 10,
    has_content: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """
    Search skills by keyword across name, description, and tags.

    Args:
        query: Search string
        category: Optional category filter
        source: Optional source filter
        limit: Max results (default 10)
        has_content: If True, only return skills with local content

    Returns:
        List of skill metadata dicts (not full Skill objects — use load() for content)
    """
    index = _load_index()
    query_lower = query.lower()
    results = []

    for meta in index["skills"]:
        if category and meta.get("category", "").lower() != category.lower():
            continue
        if source and meta.get("source", "").lower() != source.lower():
            continue
        if has_content is not None and meta.get("hasContent", False) != has_content:
            continue

        # Score: name match > description match > tag match
        score = 0
        name_l = meta.get("name", "").lower()
        desc_l = meta.get("description", "").lower()
        tags_l = " ".join(meta.get("tags", [])).lower()

        if query_lower in name_l:
            score += 10
        if query_lower in desc_l:
            score += 5
        if query_lower in tags_l:
            score += 3

        if score > 0:
            results.append((score, meta))

    results.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in results[:limit]]


def list_skills(
    category: Optional[str] = None,
    source: Optional[str] = None,
    has_content: Optional[bool] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    List skills, optionally filtered by category or source.

    Args:
        category: Filter by category (e.g. "ai-agents", "productivity", "security")
        source: Filter by source (e.g. "built-in", "optional", "ClawHub", "lord1egypt")
        has_content: If True, only skills with local SKILL.md content
        limit: Max results

    Returns:
        List of skill metadata dicts
    """
    index = _load_index()
    results = []

    for meta in index["skills"]:
        if category and meta.get("category", "").lower() != category.lower():
            continue
        if source and meta.get("source", "").lower() != source.lower():
            continue
        if has_content is not None and meta.get("hasContent", False) != has_content:
            continue
        results.append(meta)
        if len(results) >= limit:
            break

    return results


def categories() -> Dict[str, int]:
    """Return skill counts per category."""
    index = _load_index()
    return dict(sorted(index.get("byCategory", {}).items(), key=lambda x: x[1], reverse=True))


def sources() -> Dict[str, int]:
    """Return skill counts per source registry."""
    index = _load_index()
    return dict(sorted(index.get("bySource", {}).items(), key=lambda x: x[1], reverse=True))


def stats() -> Dict[str, Any]:
    """Return overall index statistics."""
    index = _load_index()
    return {
        "total": index.get("totalSkills", 0),
        "with_content": index.get("skillsWithContent", 0),
        "by_source": sources(),
        "by_category": categories(),
        "format": index.get("format", ""),
        "version": index.get("version", ""),
    }
