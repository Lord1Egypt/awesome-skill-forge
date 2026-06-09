# awesome-skill-forge

**90,000+ universal AI agent skills** — works with Claude Code, OpenAI Agents, Hermes, AutoGen, LangChain, and any LLM.

[![npm](https://img.shields.io/npm/v/forge-skills)](https://www.npmjs.com/package/forge-skills)
[![PyPI](https://img.shields.io/pypi/v/forge-skills)](https://pypi.org/project/forge-skills/)

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
from awesome_skill_forge import load, search, stats

# Search for skills
results = search("github", limit=5)
for s in results:
    print(s["name"], "-", s["description"])

# Load a skill with full content
skill = load("github-pr-workflow")
print(skill.prompt)

# Stats
print(stats())
```

```javascript
const { load, search, stats } = require('awesome-skill-forge')

const results = search('security', { limit: 5 })
results.forEach(s => console.log(s.name, '-', s.description))

const skill = load('code-review')
console.log(skill.prompt)
```

## CLI

```bash
forge search github --limit 5
forge show github-pr-workflow
forge stats
forge list --source built-in
```

## Structure

```
skills/          Official built-in skills (SKILL.md format)
lord1egypt-skills/ Lord1Egypt custom skills
optional-skills/ Optional skill collection
data/            Source registry data
python/          PyPI package source (awesome-skill-forge)
js/              npm package source (awesome-skill-forge)
tools/           Registry tools (fetch, build, sync)
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
---

# Skill Content

Full instructions for the AI agent...
```

## License

MIT — Lord1Egypt
