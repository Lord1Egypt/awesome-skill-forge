---
name: ethsmith
description: "Ethereum smart contract development environment: Foundry + Ganache + LevelDB in one tool."
version: 1.0.0
author: Lord1Egypt
license: MIT
platforms: [linux, macos, windows]
category: blockchain
tags: [ethereum, solidity, foundry, ganache, web3, smart-contracts, leveldb, npm]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/ethsmith
---

# ethsmith

All-in-one Ethereum development environment. Combines Foundry (forge/cast/anvil), Ganache local blockchain, and LevelDB state persistence — no configuration needed.

## Install

```bash
npm install -g ethsmith
# or
pip install ethsmith
```

## Repository

- GitHub: https://github.com/Lord1Egypt/ethsmith
- npm: https://www.npmjs.com/package/ethsmith
- Version: v1.0.0 (live)
- Local: `/home/lordegypt/ethsmith/`

## Quick Start

```bash
# Start local Ethereum node
ethsmith start

# Compile contracts
ethsmith compile

# Deploy contract
ethsmith deploy --contract MyToken

# Cast a call
ethsmith cast call <address> "balanceOf(address)(uint256)" <wallet>

# Forge test
ethsmith test
```

## What It Wraps

| Tool | Purpose |
|------|---------|
| `forge` | Compile, test, deploy Solidity contracts |
| `cast` | Interact with deployed contracts |
| `anvil` | Local Ethereum node (fast, ephemeral) |
| Ganache | Persistent local blockchain with LevelDB |
| LevelDB | State persistence between sessions |

## Smart Contract Development Flow

```bash
# 1. Initialize project
ethsmith init my-project && cd my-project

# 2. Write contracts in src/
# 3. Write tests in test/

# 4. Test
ethsmith test

# 5. Deploy to local node
ethsmith deploy --local

# 6. Interact
ethsmith cast send <address> "transfer(address,uint256)" <to> <amount>
```

## When to Use This Skill

- Developing Solidity smart contracts
- Setting up Ethereum dev environment from scratch
- Writing Foundry tests
- Debugging contract interactions
- Auditing and reviewing Solidity code
