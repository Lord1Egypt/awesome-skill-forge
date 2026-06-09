---
name: ai-mate
description: "Persistent AI companion with long-term memory, project context awareness, and multi-session continuity across any LLM."
version: 1.0.0
author: Lord1Egypt
license: MIT
platforms: [linux, macos, windows]
category: ai-agents
tags: [memory, companion, context, multi-session, persistence, llm, agent, productivity]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/ai-mate
---

# ai-mate

A persistent AI companion layer that maintains **long-term memory**, project context, and conversation continuity across multiple sessions and LLM providers. Works as a wrapper around any model — Claude, GPT-4, Gemini, or local Ollama models.

## Core Capabilities

- **Session memory** — remembers facts, preferences, and decisions across restarts
- **Project awareness** — understands the codebase, tech stack, and ongoing tasks
- **Multi-model** — switch between Claude, GPT-4, Gemini, Mistral without losing context
- **Structured recall** — stores memories as typed facts (user, project, feedback, reference)
- **Auto-summarize** — compresses old context to stay within token limits

## Setup

```bash
pip install ai-mate

# Initialize for a project
cd my-project
ai-mate init

# Start a session
ai-mate chat
```

## Memory Types

```bash
# Save a fact
ai-mate remember "user prefers pytest over unittest"
ai-mate remember --type project "auth rewrite due to compliance, not tech debt"
ai-mate remember --type feedback "never use mocks for DB tests"
ai-mate remember --type reference "Linear project INGEST = pipeline bugs"

# Search memory
ai-mate recall "testing preferences"

# List all memories
ai-mate memories list
```

## Multi-Session Continuity

```python
from ai_mate import Mate

mate = Mate(project="my-project", model="claude-opus-4")

# Context is automatically restored from previous sessions
response = mate.chat("continue the auth refactor we started yesterday")

# Save important decisions
mate.remember("decided to use JWT with 24h expiry instead of sessions")
```

## Project Context Loading

```bash
# Auto-detect stack and summarize codebase
ai-mate context load

# Ask questions with full project awareness
ai-mate chat "what's the best place to add rate limiting?"
```

## Model Switching

```bash
# Switch model mid-project, memory follows
ai-mate config set model gpt-4o
ai-mate chat  # same memory, different model

# Available backends
ai-mate models list
# claude-opus-4, claude-sonnet-4, gpt-4o, gemini-pro, ollama/llama3
```

## Export & Sync

```bash
# Export memories to markdown (for CLAUDE.md or team sharing)
ai-mate export --format markdown > CONTEXT.md

# Sync across machines via git
ai-mate sync --remote git@github.com:you/ai-mate-memory
```

## Memory Storage

Memories stored in `~/.ai-mate/<project>/`:
- `memories/` — typed memory files (user, project, feedback, reference)
- `sessions/` — compressed session summaries
- `context/` — project snapshots (stack, structure, recent changes)
