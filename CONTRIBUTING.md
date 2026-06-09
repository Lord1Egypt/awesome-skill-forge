# Contributing to awesome-skill-forge

Thanks for contributing! This guide covers how to add skills, fix bugs, and improve the packages.

## Adding a Custom Skill

Create a new folder under `lord1egypt-skills/` with a `SKILL.md` file:

```bash
mkdir lord1egypt-skills/my-skill
```

```markdown
---
name: my-skill
description: "What this skill does in one sentence."
version: 1.0.0
author: YourName
license: MIT
platforms: [linux, macos, windows]
category: software-dev
tags: [tag1, tag2]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/YourName/your-repo
---

# My Skill

Full instructions for the AI agent...
```

Then validate:
```bash
python tools/validate.py
```

## Skill Categories

| Category | Use for |
|----------|---------|
| `ai-agents` | AI agent frameworks, orchestration |
| `software-dev` | Coding, debugging, code review |
| `blockchain` | Web3, Ethereum, smart contracts |
| `productivity` | Task management, automation |
| `security` | Pentesting, auditing, OSINT |
| `devops` | Docker, CI/CD, infrastructure |
| `data-science` | ML, data analysis, notebooks |
| `creative` | Design, art, media generation |
| `mlops` | Model training, fine-tuning, deployment |

## Running Tests

```bash
# Python
pip install pytest
pytest tests/test_python.py -v

# JavaScript
node tests/test_js.js
```

## Rebuilding the Index

After adding or updating skills:

```bash
# Rebuild index.json
python tools/build_index.py

# Copy to packages
cp index.json python/forge_skills/data/index.json
cp index.json js/data/index.json
```

## Validating Skills

```bash
# Validate all SKILL.md files
python tools/validate.py

# Validate specific directory
python tools/validate.py --dir lord1egypt-skills
```

## Pull Request Process

1. Fork the repo and create a branch: `git checkout -b feat/my-skill`
2. Add your skill + validate: `python tools/validate.py`
3. Run tests: `pytest tests/test_python.py -v`
4. Open a PR with a clear title and description

## Reporting Issues

Use the issue templates:
- **Bug report** — something is broken
- **New skill request** — suggest a skill to add

## License

By contributing, you agree your contributions are licensed under MIT.
