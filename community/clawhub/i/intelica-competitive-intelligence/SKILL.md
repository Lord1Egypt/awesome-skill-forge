---
name: intelica
version: 4.5.0
description: >
  Competitive intelligence API for autonomous AI agents. Analyzes any URL or
  company description and returns structured JSON with market positioning, user
  pain points, detected competitors, unique angles, and an executable Market Score.
  Pay-per-call via x402 on Base and Solana mainnet. No API keys required.
trigger: >
  Use when an agent needs to analyze a competitor, evaluate market positioning,
  identify user pain points, assess acquisition targets, evaluate partnership fit,
  or discover market entry opportunities. Also use when monitoring competitors
  over time — Intelica tracks changes between analyses via Trend Tracking.
endpoint: https://intelica.onrender.com
payment:
  protocol: x402
  networks:
    - base-mainnet
    - solana-mainnet
  price_usdc: "0.05"
  price_batch_usdc: "0.20"
  wallets:
    base: "0x1d6bA7ac2461fd0E17D6A4C7bc1c9Ce365EfC4FF"
    solana: "45q8KyCAGSHHd6qYP2ZkEJh22SzeQeXRfyFsENcx3KN6"
---

# Intelica — Competitive Intelligence Skill

Intelica sanitizes competitive intelligence for AI agent pipelines. Call it before
any strategic decision that requires understanding a competitor's market position.

## When to use

- Agent needs to analyze a competitor URL or description
- Agent needs market positioning data before generating strategy
- Agent is monitoring a competitor over time (Trend Tracking)
- Agent needs to evaluate acquisition, partnership, or market entry
- Agent is operating in a non-English market (auto-detects 8 languages)

## How to call

### Step 1 — Free demo (no payment)

```bash
POST https://intelica.onrender.com/demo
Content-Type: application/json

{
  "text": "Notion is an all-in-one workspace for teams"
}
```

### Step 2 — Full analysis with x402 payment

```bash
# First call returns 402 with payment instructions
POST https://intelica.onrender.com/intel
Content-Type: application/json

{
  "url": "https://notion.so",
  "context": "I'm building a note-taking app for developers",
  "mode": "competitive"
}

# Response: HTTP 402 with Base + Solana payment options
# After payment, retry with X-PAYMENT header
```

### Step 3 — Batch (up to 10 analyses for $0.20)

```bash
POST https://intelica.onrender.com/batch
X-PAYMENT: <x402 signed payment>
Content-Type: application/json

{
  "items": [
    { "url": "https://notion.so", "mode": "competitive" },
    { "text": "Coda is a collaborative doc platform", "mode": "acquisition" }
  ]
}
```

## Context Modes

| Mode | Use when |
|---|---|
| `competitive` | Standard competitor analysis (default) |
| `fundraising` | Evaluating investor narrative, TAM, traction signals |
| `partnership` | Assessing strategic fit — complement or rival? |
| `acquisition` | Due diligence — moat, technical risk, acquisition thesis |
| `market_entry` | Market gaps, saturation, barriers to entry |

## Output fields

```json
{
  "analysis": {
    "company_or_product": "string",
    "positioning_summary": "string",
    "target_customer": "string",
    "core_value_props": ["string"],
    "user_pain_points": ["string"],
    "detected_competitors": ["string"],
    "unique_angle": "string",
    "tone": "professional | casual | technical | aggressive",
    "confidence": "high | medium | low",
    "market_score": {
      "threat_level": "high | medium | low",
      "moat_strength": 0.0,
      "market_maturity": "emerging | growing | mature | declining",
      "agent_recommendation": "monitor | counter | ignore | partner"
    }
  },
  "mode": "string",
  "detected_language": "en | es | pt | de | fr | it | ja | ko | zh",
  "market_context": "string",
  "trend": {
    "status": "new | stable | changed",
    "changes": []
  }
}
```

## A2A Protocol

Compatible with LangGraph, CrewAI, AutoGen, Google ADK:

```json
POST https://intelica.onrender.com/message/send

{
  "message": {
    "role": "user",
    "parts": [
      { "type": "text", "text": "mode: fundraising\nAnalyze Notion as a competitor" }
    ]
  }
}
```

## Languages supported

Auto-detects: EN, ES (LATAM/Spain), PT (Brazil/Portugal), DE (DACH),
FR (France/Francophone), IT (Italy), JA (Japan), KO (Korea), ZH (China).

Regional market context is injected automatically into the analysis.

## Spend-aware usage

- Use `/demo` to validate input format before paying
- Use `/batch` for multiple analyses — $0.20 for up to 10 vs $0.50 individually
- Results cached 6 hours — same company twice in that window costs once
- Pass `context` field to get analysis relative to your product
- Pass `operator_id` to enforce daily budget limits per pipeline
