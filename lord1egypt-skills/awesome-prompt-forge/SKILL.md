---
name: awesome-prompt-forge
description: "2,592 curated AI system prompts from Claude, ChatGPT, Cursor, v0, Devin, Grok, and more."
version: 1.0.3
author: Lord1Egypt
license: MIT
platforms: [linux, macos, windows]
category: ai-agents
tags: [prompts, system-prompts, claude, chatgpt, cursor, v0, devin, grok, python, npm]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/awesome-prompt-forge
---

# awesome-prompt-forge

2,592 curated AI system prompts extracted from real production AI tools. Organized by tool, lazy-loaded on demand.

## Install

```bash
pip install awesome-prompt-forge
npm install awesome-prompt-forge
```

## Repository

- GitHub: https://github.com/Lord1Egypt/awesome-prompt-forge
- PyPI: https://pypi.org/project/awesome-prompt-forge/
- npm: https://www.npmjs.com/package/awesome-prompt-forge
- Version: v1.0.3 (live)

## Prompt Categories (14 total, 2,592 prompts)

| Category | Examples |
|----------|---------|
| claude | Claude 3.5 Sonnet, Claude 5 full system prompt |
| chatgpt | GPT-4o, ChatGPT Canvas, o4-mini |
| v0 | Vercel v0 prompt (Nov 2024, Sep 2024) |
| cursor | Cursor IDE system prompt |
| devin | Devin 2.0 agent prompt |
| copilot | GitHub Copilot, Microsoft Copilot |
| grok | Grok 3 system prompt |
| writing | 88 writing-focused system prompts |
| general | 163 general-purpose personas |
| tools | Manus, Windsurf, Loveable, Replit, Bolt |

## Python Usage

```python
from awesome_prompt_forge import load, search, list_prompts, categories

# Load a specific prompt
prompt = load("claude-5")
print(prompt.content)

# Search
results = search("coding assistant")

# List by category
claude_prompts = list_prompts(category="claude")

# Stats
print(categories())
```

## When to Use This Skill

- Finding real system prompts from production AI tools
- Studying prompt engineering techniques used by top AI companies
- Building prompt libraries for your own agents
- Comparing prompts across different AI tools
- Using real prompts as templates for new agent instructions
