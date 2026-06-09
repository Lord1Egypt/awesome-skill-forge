---
name: thothterm
description: "GPU-accelerated terminal emulator with AI-native and Web3-native features built on wgpu+WASM."
version: 1.0.0
author: Lord1Egypt
license: MIT
platforms: [linux, macos, windows]
category: software-dev
tags: [terminal, gpu, wgpu, wasm, rust, ai, web3, emulator]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/ThothTerm
---

# ThothTerm

GPU-accelerated terminal emulator built with Rust, wgpu, and WASM. Designed to be AI-native and Web3-native — the terminal that thinks and connects to the chain.

## Repository

- GitHub: https://github.com/Lord1Egypt/ThothTerm
- Local dev: `/home/lordegypt/ThothTerm/`
- Based on: wezterm fork (wez/wezterm)
- Strategy: maintain as fork during dev, detach to standalone at v1.0

## Architecture

```
ThothTerm/
├── wezterm-gui/       # Main GUI (wgpu renderer)
├── wezterm-mux/       # Terminal multiplexer
├── wezterm-font/      # Font shaping (harfbuzz)
├── wezterm-ssh/       # SSH integration
├── config/            # Config schema
└── wasm/              # WASM bindings (planned)
```

## AI-Native Features (Planned)

- Inline LLM suggestions in the terminal prompt
- Command auto-explain (pipe any command output to AI)
- Session summarization
- Smart history search via embedding similarity
- MCP server integration for tool calls from terminal

## Web3-Native Features (Planned)

- Built-in wallet address detection and ENS resolution
- Transaction hash hover → on-chain details
- RPC endpoint status indicator in status bar
- Inline gas price display
- One-click `cast` / `forge` command helpers (Foundry)

## Build

```bash
# Prerequisites: Rust, wgpu dependencies
cd /home/lordegypt/ThothTerm
cargo build --release

# Run dev version
cargo run --bin wezterm
```

## When to Use This Skill

- Working on ThothTerm codebase (Rust, wgpu, terminal emulation)
- Adding AI features to the terminal
- Integrating Web3/blockchain tools into terminal UI
- Debugging wgpu rendering issues
- Planning features for the next ThothTerm milestone

## Key Dependencies

- `wgpu` — GPU rendering backend
- `harfbuzz` — Font shaping
- `openssl` — SSH/TLS
- `lua` — Config scripting (same as wezterm)
- `serde` — Config serialization
