"""
Tests for forge_skills Python package.
Run: pytest tests/test_python.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from forge_skills import load, search, list_skills, categories, sources, stats, Skill


# ── stats ──────────────────────────────────────────────────────────────────

def test_stats_returns_dict():
    s = stats()
    assert isinstance(s, dict)

def test_stats_total():
    s = stats()
    assert s['total'] > 90000

def test_stats_with_content():
    s = stats()
    assert s['with_content'] >= 160

def test_stats_by_source_includes_clawhub():
    s = stats()
    assert 'ClawHub' in s['by_source']

def test_stats_by_source_includes_builtin():
    s = stats()
    assert 'built-in' in s['by_source']


# ── search ─────────────────────────────────────────────────────────────────

def test_search_returns_list():
    results = search('github')
    assert isinstance(results, list)

def test_search_respects_limit():
    results = search('code', limit=5)
    assert len(results) <= 5

def test_search_result_has_required_fields():
    results = search('docker', limit=1)
    assert results
    r = results[0]
    for field in ('name', 'description', 'category', 'source'):
        assert field in r, f"Missing field: {field}"

def test_search_filter_by_source():
    results = search('agent', source='built-in', limit=10)
    for r in results:
        assert r['source'] == 'built-in'

def test_search_filter_by_category():
    results = search('ethereum', category='blockchain', limit=10)
    for r in results:
        assert r['category'] == 'blockchain'

def test_search_no_results_returns_empty():
    results = search('xyzzy_nonexistent_skill_12345', limit=5)
    assert results == []

def test_search_has_content_filter():
    results = search('github', has_content=True, limit=20)
    for r in results:
        assert r.get('hasContent') is True


# ── load ───────────────────────────────────────────────────────────────────

def test_load_returns_skill():
    skill = load('github-pr-workflow')
    assert isinstance(skill, Skill)

def test_load_official_skill_has_content():
    skill = load('github-pr-workflow')
    assert len(skill.prompt) > 200

def test_load_skill_fields():
    skill = load('github-pr-workflow')
    assert skill.name
    assert skill.description
    assert skill.category
    assert skill.source in ('built-in', 'optional', 'lord1egypt')

def test_load_case_insensitive():
    skill = load('GITHUB-PR-WORKFLOW')
    assert skill.name.lower() == 'github-pr-workflow'

def test_load_skill_str():
    skill = load('github-pr-workflow')
    assert str(skill) == skill.prompt

def test_load_not_found_raises():
    with pytest.raises(KeyError):
        load('this-skill-does-not-exist-xyzzy')

def test_load_filter_by_source():
    skill = load('github-pr-workflow', source='built-in')
    assert skill.source == 'built-in'

def test_load_optional_skill():
    skill = load('docker-management')
    assert skill.source == 'optional'
    assert len(skill.prompt) > 100

def test_load_lord1egypt_skill():
    skill = load('ethsmith')
    assert skill.source == 'lord1egypt'
    assert skill.author == 'Lord1Egypt'

def test_load_community_no_fetch_returns_description():
    # Community skills without fetch=True return description only
    results = search('', source='ClawHub', limit=1)
    if results:
        skill = load(results[0]['name'])
        assert isinstance(skill.prompt, str)


# ── list_skills ────────────────────────────────────────────────────────────

def test_list_skills_default():
    results = list_skills(limit=10)
    assert len(results) <= 10
    assert len(results) > 0

def test_list_skills_filter_source():
    results = list_skills(source='built-in', limit=100)
    assert all(r['source'] == 'built-in' for r in results)

def test_list_skills_filter_has_content():
    results = list_skills(has_content=True, limit=50)
    assert all(r.get('hasContent') for r in results)


# ── categories / sources ───────────────────────────────────────────────────

def test_categories_returns_dict():
    cats = categories()
    assert isinstance(cats, dict)
    assert len(cats) > 5

def test_categories_sorted_by_count():
    cats = categories()
    counts = list(cats.values())
    assert counts == sorted(counts, reverse=True)

def test_sources_returns_dict():
    srcs = sources()
    assert isinstance(srcs, dict)
    assert 'ClawHub' in srcs
    assert 'built-in' in srcs

def test_sources_clawhub_is_largest():
    srcs = sources()
    assert srcs['ClawHub'] == max(srcs.values())
