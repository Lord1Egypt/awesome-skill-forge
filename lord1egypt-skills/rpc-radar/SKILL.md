---
name: rpc-radar
description: "Inspect, benchmark, and monitor Web3 RPC endpoints — latency checks, method support, chain detection, and health scoring."
version: 1.0.0
author: Lord1Egypt
license: MIT
platforms: [linux, macos, windows]
category: blockchain
tags: [web3, rpc, ethereum, evm, monitoring, latency, health-check, endpoints, blockchain]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/rpc-radar
---

# rpc-radar

Inspect, benchmark, and continuously monitor **EVM-compatible RPC endpoints**. Detects chain ID, measures latency, checks supported methods, and assigns a health score — useful for selecting reliable public RPCs or auditing private node performance.

## Quick Scan

```bash
# Single endpoint
rpc-radar scan https://eth.llamarpc.com

# Multiple endpoints from file
rpc-radar scan --file endpoints.txt

# Output as JSON
rpc-radar scan https://mainnet.infura.io/v3/KEY --json
```

## What It Checks

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Chain ID | `eth_chainId` | Returns expected chain |
| Block height | `eth_blockNumber` | Non-zero, synced |
| Latency | timed request | < 500ms = good |
| Batch support | batch JSON-RPC | Response array |
| Archive depth | `eth_getBalance` (old block) | Returns value |
| Filter support | `eth_newFilter` | No error |
| WebSocket | ws:// upgrade | Handshake success |

## Benchmark Mode

```bash
# 100 requests, measure p50/p95/p99
rpc-radar bench https://eth.llamarpc.com --requests 100

# Compare two endpoints
rpc-radar compare https://eth.llamarpc.com https://rpc.ankr.com/eth
```

## Monitor Mode (continuous)

```bash
# Poll every 30s, alert if latency > 1000ms or block falls behind
rpc-radar monitor https://eth.llamarpc.com --interval 30 --alert-latency 1000

# Monitor multiple and export to CSV
rpc-radar monitor --file endpoints.txt --output monitor.csv
```

## Health Score

Each endpoint gets a 0–100 score:
- **Latency** (40 pts): < 200ms = 40, < 500ms = 20, > 500ms = 0
- **Uptime** (30 pts): based on consecutive successful checks
- **Block sync** (20 pts): within 2 blocks of best known
- **Method support** (10 pts): supports batch + filters + archive

## Supported Chains

Auto-detected by chain ID: Ethereum, Polygon, BSC, Arbitrum, Optimism, Avalanche, Base, Fantom, and any other EVM-compatible chain.

## Output Example

```
Endpoint: https://eth.llamarpc.com
Chain: Ethereum Mainnet (1)
Block: 19,845,231 ✅
Latency: 87ms ✅
Batch: supported ✅
Archive: supported ✅
Health Score: 94/100 🟢
```
