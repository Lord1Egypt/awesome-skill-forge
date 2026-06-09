---
name: trustboost-pii-sanitizer
version: "2.6.0"
description: Context-aware PII sanitization for autonomous AI agent pipelines. Sanitizes text before LLMs with 5 context modes (legal/financial/medical/code/general), Privacy Budget per agent, and TrustBoost Score for M2M trust verification. Supports EN, ES (LATAM), PT (BR/PT), DE, JA, FR, IT, KO with country-specific patterns (RFC, CUIT, CPF, CNPJ, Personalausweis, マイナンバー, NIR, Codice Fiscale, 주민등록번호). Returns sanitized text, safety_score (0.0-1.0), risk_category (CRITICAL/PRIVATE/SENSITIVE/CLEAN), and context_applied. No SDK required — single POST request. 50 free requests per wallet with tx_hash="TRIAL".
license: MIT
compatibility: Requires internet access to reach the TrustBoost API. No local dependencies. Compatible with any agent that can make HTTP POST requests. No authentication required.
metadata:
  author: teodorofodocrispin-cmyk
  version: "2.6.0"
  endpoint: https://api.trustboost.dev/sanitize
  health: https://api.trustboost.dev/health
  payment: Solana USDC (149 USDC = 10,000 sanitizations)
  trial: tx_hash=TRIAL (50 free sanitizations per wallet, no payment required)
  preview: https://api.trustboost.dev/sanitize/preview (3 free requests per IP, no wallet required)
  autonomy_score: 8.5/10
  audit_score: 9.8/10
  languages: English, Spanish, Portuguese, German, Japanese, French, Italian, Korean
  compliance: GDPR, LGPD, APPI, CCPA, DPDPA, EU-AI-Act-2026
  requires_env: none
  wallet_security: >
    TrustBoost NEVER requires wallet private keys, seed phrases, or signing credentials.
    The wallet_address field is only used as an identifier for quota tracking.
  x402_compatible: true
  proof_on_chain: true
  mcp_endpoint: https://api.trustboost.dev/mcp
  agent_card: https://api.trustboost.dev/.well-known/agent-card.json
  llms_txt: https://api.trustboost.dev/llms.txt
  verify_endpoint: https://api.trustboost.dev/verify/{anchor_tx}
---

# TrustBoost PII Sanitizer v2.6.0

Privacy firewall for autonomous AI agent pipelines. Sanitizes PII before text reaches LLMs. Every paid sanitization anchored on Solana — verifiable forever.

**Live Demo:** https://huggingface.co/spaces/TrustBoost/pii-sanitizer
**Verify proof:** https://api.trustboost.dev/verify/{anchor_tx}
**Landing page:** https://teodorofodocrispin-cmyk.github.io/TrustBoost-PII-Sanitizer/

## What it does

TrustBoost sits between your agent and the LLM. It detects and redacts PII — emails, phone numbers, national IDs, API keys, passwords, financial data — before the text reaches the model. Every paid sanitization is anchored on Solana via Helius, providing an immutable audit trail verifiable by anyone.

## Why use TrustBoost

- **EU AI Act** enforcement begins August 2, 2026 — Articles 12, 13, 26 require verifiable audit trails
- **Zero friction** — single POST request, no SDK, no setup
- **8 languages** — including LATAM identifiers not covered by regex tools
- **x402 native** — agents pay autonomously in USDC on Solana
- **Proof on-chain** — immutable evidence for regulators and auditors
- **Fail-closed** — if unreachable, blocks the request rather than passing unsanitized text

## Quick Start — TRIAL mode (no wallet needed)

```bash
curl -X POST https://api.trustboost.dev/sanitize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "My email is john@example.com and SSN is 123-45-6789",
    "tx_hash": "TRIAL",
    "wallet_address": "your-agent-id",
    "context": "general"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "sanitized_content": "My email is [REDACTED] and SSN is [REDACTED]",
    "safety_score": 0.6,
    "risk_category": "PRIVATE",
    "context_applied": "general",
    "usage_metrics": {
      "quota_remaining": 49,
      "quota_limit": 50
    }
  }
}
```

## x402 Autonomous Payment Flow

```bash
# Step 1: Call without payment → receive HTTP 402
curl -X POST https://api.trustboost.dev/sanitize \
  -H "Content-Type: application/json" \
  -d '{"text": "Contact john@example.com"}'
# → HTTP 402 with USDC payment instructions

# Step 2: Pay 149 USDC on Solana mainnet
# Address: giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4

# Step 3: Retry with tx_hash
curl -X POST https://api.trustboost.dev/sanitize \
  -H "Content-Type: application/json" \
  -d '{"text": "Contact john@example.com", "tx_hash": "YOUR_TX_HASH"}'
# → sanitized text + proof_of_sanitization on Solana
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sanitize` | POST | Core PII sanitization endpoint |
| `/redact` | POST | Alias for /sanitize |
| `/sanitize/preview` | POST | 3 free previews per IP/24h |
| `/demo` | POST | 3 free requests per hour |
| `/detect` | POST | Alias for /demo |
| `/verify/{anchor_tx}` | GET | Verify Proof of Sanitization on Solana |
| `/anchor/{anchor_tx}` | GET | Alias for /verify |
| `/score/{wallet}` | GET | TrustBoost Score M2M trust verification |
| `/health` | GET | Service health check |
| `/mcp` | POST | MCP Server JSON-RPC 2.0 |
| `/llms.txt` | GET | LLM and agent discovery |
| `/openapi.json` | GET | OpenAPI 3.0 specification |

## Context Modes

| Context | Use case |
|---------|----------|
| `general` | Standard PII detection (default) |
| `legal` | Maximum redaction for legal documents |
| `financial` | Financial identifiers focus |
| `medical` | HIPAA-grade sanitization |
| `code` | API keys and credentials only |

## Languages & PII Patterns

| Language | Region | Patterns |
|----------|--------|----------|
| 🇺🇸 English | Global | SSN, API keys, credit cards, passwords |
| 🇲🇽🇨🇴 Spanish LATAM | Latin America | RFC, CUIT, CURP, DNI, RUT, Cédula |
| 🇧🇷🇵🇹 Portuguese | BR & PT | CPF, CNPJ, RG, NIF |
| 🇩🇪 German | DE/AT/CH | Personalausweis, Steuernummer, IBAN DE |
| 🇯🇵 Japanese | Japan | マイナンバー, 運転免許証, 住所 |
| 🇫🇷 French | FR/BE/CA | NIR, SIRET, Carte Vitale, IBAN FR |
| 🇮🇹 Italian | Italy | Codice Fiscale, Partita IVA, Tessera Sanitaria |
| 🇰🇷 Korean | Korea | 주민등록번호 (RRN), 사업자등록번호 |

## Pricing

| Tier | Cost | Quota |
|------|------|-------|
| Preview | Free | 3 requests/IP/24h |
| Trial | Free | 50 sanitizations/wallet |
| Paid | 149 USDC | 10,000 sanitizations + on-chain proof |

## MCP Integration

```json
{
  "mcpServers": {
    "trustboost": {
      "url": "https://api.trustboost.dev/mcp"
    }
  }
}
```

Compatible with: Claude Code · Cursor · Windsurf · Glama

## Proof of Sanitization

```bash
# Verify any paid sanitization independently
curl https://api.trustboost.dev/verify/{anchor_tx}
# → {"status": "verified", "proof": {...}}
```

EU AI Act compliance — Articles 12, 13, 26.

## Resources

- GitHub: https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer
- Agent Card: https://api.trustboost.dev/.well-known/agent-card.json
- llms.txt: https://api.trustboost.dev/llms.txt
- OpenAPI: https://api.trustboost.dev/openapi.json
- Live Demo: https://huggingface.co/spaces/TrustBoost/pii-sanitizer
- Landing: https://teodorofodocrispin-cmyk.github.io/TrustBoost-PII-Sanitizer/
