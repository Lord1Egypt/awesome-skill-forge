# awesome-skill-forge

**90,000+ universal AI agent skills** — works with Claude Code, OpenAI Agents, Hermes, AutoGen, LangChain, and any LLM.

[![PyPI](https://img.shields.io/pypi/v/awesome-skill-forge)](https://pypi.org/project/awesome-skill-forge/)
[![npm](https://img.shields.io/npm/v/awesome-skill-forge)](https://www.npmjs.com/package/awesome-skill-forge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-90%2C896-green)](registry.json)

## Sources

| Registry | Skills |
|----------|--------|
| ClawHub  | 69,842 |
| skills.sh | 19,938 |
| LobeHub  | 505    |
| browse.sh | 389   |
| gstack   | 52     |
| Built-in | 75     |
| Optional | 95     |
| **Total** | **90,896** |

## Install

```bash
# Python
pip install awesome-skill-forge

# Node.js
npm install awesome-skill-forge
```

## Usage

```python
from forge_skills import load, search, stats

# Search across 90k+ skills
results = search("github", limit=5)
for s in results:
    print(s["name"], "-", s["description"])

# Load an official skill (full content, offline)
skill = load("github-pr-workflow")
print(skill.prompt)

# Load any community skill on demand (fetches from source API)
skill = load("ASO Playbook", fetch=True)
print(skill.prompt)

# Stats
print(stats())
# {'total': 90896, 'with_content': 160, 'by_source': {...}, ...}
```

```javascript
const { load, search, stats } = require('awesome-skill-forge')

// Search
const results = search('security', { limit: 5 })
results.forEach(s => console.log(s.name, '-', s.description))

// Load official skill (sync)
const skill = load('github-pr-workflow')
console.log(skill.prompt)

// Load community skill on demand (async, fetches from source API)
const skill = await load('ASO Playbook', { fetch: true })
console.log(skill.prompt)
```

## CLI

```bash
forge search github --limit 5
forge show github-pr-workflow
forge stats
forge list --source built-in
forge list --source ClawHub --limit 20
```

## On-Demand Fetch

Official skills (built-in + optional, 160 total) have full content embedded in the package — no network needed.

For the remaining 90k+ community skills, use `fetch=True` to pull content live from the source registry:

| Source | Fetch method |
|--------|-------------|
| ClawHub | ZIP download via API |
| LobeHub | GitHub raw JSON |
| skills.sh | GitHub API (multi-path) |
| gstack | GitHub tree API |

Set `GITHUB_TOKEN` env var for higher rate limits on GitHub-based sources.

```bash
export GITHUB_TOKEN=ghp_...
```

## Structure

```
skills/            Official built-in skills (SKILL.md format)
optional-skills/   Optional skill collection
lord1egypt-skills/ Lord1Egypt custom skills
data/              Source registry data (skills_raw.json — 90k entries)
python/            PyPI package source (forge_skills module)
js/                npm package source
tools/             Registry tools
  fetch_official.py  Pull 170 official skills from Hermes
  fetch_skill.py     Fetch single skill on demand (CLI)
  build_index.py     Build index.json from all sources
  build_registry.py  Build registry.json + REGISTRY.md
  sync.py            Auto-sync official skills from Hermes API
  validate.py        Validate all SKILL.md files
registry.json      agentskills.io-compatible manifest
REGISTRY.md        Full index table by category
```

## Hermes SKILL.md Format

Each skill follows the [Hermes Agent](https://hermes-agent.nousresearch.com) SKILL.md specification:

```markdown
---
name: skill-name
description: What this skill does
category: software-dev
tags: [git, github, pr]
platforms: [claude-code, openai-agents]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
---

# Skill Content

Full instructions for the AI agent...
```

## CI/CD

- **Validate** — runs on every push touching `skills/` directories
- **Sync** — weekly auto-sync from Hermes API (Monday 3am UTC), auto-commits new skills
- **Publish** — push a version tag to auto-publish to PyPI + npm:

```bash
git tag v1.0.3 && git push origin v1.0.3
```

## License

MIT — [Lord1Egypt](https://github.com/Lord1Egypt)
