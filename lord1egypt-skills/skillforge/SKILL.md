---
name: skillforge
description: "Lazy-loading Python/JS package with 539 AI agent skills for Claude, Gemini, and Scientific agents."
version: 1.0.5
author: Lord1Egypt
license: MIT
platforms: [linux, macos, windows]
category: ai-agents
tags: [skills, ai-agents, claude, gemini, scientific, lazy-loading, python, npm]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/ai-skillforge
---

# skillforge-agent

Lazy-loading skill library with 539 production-ready AI agent skills. Skills load on demand — zero startup cost, zero wasted tokens.

## Install

```bash
pip install skillforge-agent
npm install skillforge-agent
```

## Repository

- GitHub: https://github.com/Lord1Egypt/ai-skillforge
- PyPI: https://pypi.org/project/skillforge-agent/
- npm: https://www.npmjs.com/package/skillforge-agent
- Version: v1.0.5 (live)

## Skill Counts

| Category | Count |
|----------|-------|
| Claude Code | 340 |
| Scientific | 148 |
| Gemini | 51 |
| **Total** | **539** |

## Python Usage

```python
from skillforge_agent import load, search, list_skills, categories

# Load a skill — reads from disk only at this moment
skill = load("scientific-brainstorming")
print(skill.prompt)  # Full skill content

# Search
results = search("data analysis")

# List by category
claude_skills = list_skills(category="claude")

# Stats
print(categories())
# {"claude": 340, "scientific": 148, "gemini": 51, "total": 539}
```

## JavaScript Usage

```js
const { load, search, listSkills, categories } = require('skillforge-agent')

const skill = load('exploratory-data-analysis')
console.log(skill.prompt)

const results = search('protein', 'scientific', 5)
console.log(categories())
// { claude: 340, scientific: 148, gemini: 51, total: 539 }
```

## CLI

```bash
skillforge stats
skillforge search "data analysis"
skillforge load scientific-brainstorming
npx skillforge stats
```

## When to Use This Skill

- Loading Claude Code system prompts into an agent
- Using scientific research skills in a pipeline
- Integrating Gemini-specific agent skills
- Building lazy-loading skill systems for your own agents
