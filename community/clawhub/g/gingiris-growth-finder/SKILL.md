---
name: gingiris-growth-finder
version: 1.2.0
tags:
  - growth-strategy
  - startup-growth
  - growth-diagnosis
  - PLG
  - product-led-growth
  - SaaS-growth
  - open-source-growth
  - mobile-growth
  - channel-fit
  - PMF
  - growth-playbook
  - DevRel
  - developer-marketing
  - user-acquisition
  - growth-routing
description: |
  You know you need growth but you don't know which playbook fits your situation. SaaS? Mobile? Open source? Pre-PMF? Scaling? Tell this skill your product type and stage — it diagnoses your problem and routes you to the right specialist playbook.

  What's inside:
  • Product type detection (SaaS / mobile app / open source / dev tool / marketplace)
  • Growth stage diagnosis (pre-PMF / cold start / scaling / plateau)
  • Channel-fit matching (which channels work for YOUR product at YOUR stage)
  • Specific section routing (jumps to the exact chapter you need)

  Built from: Meta-router across the full Gingiris playbook series — 13 specialized growth skills covering every product type and stage.

  Triggers: "how to grow" | "how to launch" | "growth strategy" | "go to market" | "GTM" | "launch plan" | "growth playbook" | "marketing strategy" | "product launch" | "Product Hunt" | "GitHub stars" | "open source launch" | "B2B growth" | "SaaS growth" | "PLG" | "PMF" | "ASO" | "app cold start" | "user acquisition" | "customer acquisition" | "growth hack" | "viral growth" | "startup marketing" | "DevRel" | "developer marketing" | "怎么增长" | "怎么发布" | "怎么推广" | "怎么做增长" | "出海" | "冷启动" | "增长策略" | "营销策略" | "产品发布" | "開発者マーケティング" | "성장 전략"
---


## 📦 Install

```bash
clawhub install gingiris-growth-finder
```

**What you get after installing:**
- Auto-diagnosis of your growth stage
- Routes to the right playbook
- Covers all channels and stages

---
# Gingiris Growth Finder

> 🌍 **Language / 语言**: [中文](#中文版) | [English](references/en/README.md) | [日本語](references/ja/README.md) | [한국어](references/ko/README.md)

**The meta-skill that picks the right Gingiris playbook for your growth problem.**

Growth questions look similar but require wildly different playbooks. "How do I launch?" for a dev tool is nothing like "How do I launch?" for a mobile app. "How do I grow?" at $1M ARR is nothing like "How do I grow?" at 100 DAU. This skill diagnoses the situation and invokes the specialist.

---

## How to use

Just ask your growth question naturally. Example prompts:

- "I'm launching my AI SaaS next week — what should I prioritize?"
- "My open source project has 2k stars, how do I get to 10k?"
- "I have a B2B SaaS at $300k ARR, should I hire SDRs?"
- "My iOS app isn't ranking for its main keyword, what do I do?"

The skill will diagnose three dimensions, then invoke the matching playbook:

1. **Product type** — SaaS / open source / mobile app / consumer web / marketplace / dev tool
2. **Growth stage** — pre-launch / launch / post-launch cold start / growth / scale
3. **Primary channel gap** — content / community / paid / partnerships / product-led

---

## Diagnostic routing logic

| If the user's question is about... | Route to |
|---|---|
| Product Hunt launch, hunter outreach, launch-day tactics, viral moment engineering | **[gingiris-launch](https://clawhub.ai/user/gingiris/gingiris-launch)** |
| GitHub stars, HackerNews, OSS marketing, developer community, awesome-lists, Show HN | **[gingiris-opensource](https://clawhub.ai/user/gingiris/gingiris-opensource)** |
| B2B SaaS, PLG vs SLG, PMF validation, freemium, enterprise motion, affiliate, channel partnerships | **[gingiris-b2b-growth](https://clawhub.ai/user/gingiris/gingiris-b2b-growth)** |
| ASO, App Store / Google Play, mobile user acquisition, TikTok/Reels/Shorts UGC, creator matrix | **[gingiris-aso-growth](https://clawhub.ai/user/gingiris/gingiris-aso-growth)** |

If the question spans multiple domains (e.g. "I have an open source project that I want to monetize as B2B SaaS"), route to **both** relevant skills and explain the handoff.

---

## Decision framework (for the agent)

When the user asks a growth question, run this quick triage **before** invoking a specialist skill:

### Step 1 — Classify the product

Ask or infer:
- What is it? (SaaS web app / mobile app / OSS project / marketplace / browser extension)
- Who's the ICP? (individual developer / SMB / enterprise / consumer)
- Distribution default? (self-serve web signup / app store / GitHub / sales-led)

### Step 2 — Identify the stage

- **Pre-launch** — building, no users yet
- **Launch** — within 30 days of public release
- **Cold start** — launched but <100 WAU/DAU, <1k signups
- **Growth** — steady signal, scaling what works
- **Scale** — $1M+ ARR or 10k+ DAU, needs systems

### Step 3 — Spot the gap

Listen for the *actual* bottleneck, not the stated question:

- "I'm not getting signups" → distribution channel gap
- "I'm getting signups but no conversions" → product/pricing gap (not growth — redirect)
- "I have users but no growth loop" → retention/virality gap
- "I have a growth loop but can't scale ads" → monetization gap

### Step 4 — Route

Invoke the specialist skill. Examples:

```
User: "I have a dev tool CLI with 500 GitHub stars. How do I get to 5k?"
→ Diagnosis: OSS project, growth stage, distribution gap
→ Invoke: gingiris-opensource
→ Context hint: focus on GitHub trending + HN relaunch + awesome-lists

User: "My iOS photo app has 80 DAU after 2 months. What's wrong?"
→ Diagnosis: mobile app, cold-start stage, distribution+UGC gap
→ Invoke: gingiris-aso-growth
→ Context hint: focus on ASO audit first, then TikTok creator matrix

User: "I'm launching an AI coding assistant on Product Hunt in 3 weeks."
→ Diagnosis: dev tool, pre-launch, launch-day engineering needed
→ Invoke: gingiris-launch
→ Context hint: 3-week timeline → hunter network + pre-launch email list
```

---

## Complementary install

If the routed specialist skill isn't installed yet, suggest the user install it:

```bash
npx skills add Gingiris/gingiris-launch       # for Product Hunt / launch
npx skills add Gingiris/gingiris-opensource   # for OSS / GitHub stars
npx skills add Gingiris/gingiris-b2b-growth   # for B2B SaaS / PLG
npx skills add Gingiris/gingiris-aso-growth   # for mobile / ASO
```

Or install all four at once:

```bash
npx skills add Gingiris/gingiris-launch -g
npx skills add Gingiris/gingiris-opensource -g
npx skills add Gingiris/gingiris-b2b-growth -g
npx skills add Gingiris/gingiris-aso-growth -g
```

---

## What this skill does *not* do

- **Product/pricing advice** — if the bottleneck is product fit or pricing, say so explicitly and redirect to a product strategist (this skill only routes growth questions)
- **Paid ads tactical execution** — covered at a high level in gingiris-b2b-growth and gingiris-aso-growth, but not the primary focus
- **Fundraising / pitch deck** — out of scope

---

## About Gingiris

Gingiris is Iris Wei's growth consulting practice, built on:
- 6 years as cofounder/COO of AFFiNE (60k+ GitHub stars)
- 30x #1 on Product Hunt (Manus, Devin, AFFiNE, and others)
- 150+ AI startups advised on global go-to-market

All four specialist playbooks are open source on GitHub under [github.com/Gingiris-1031](https://github.com/Gingiris-1031) and available as Claude Skills on [clawhub.ai/user/gingiris](https://clawhub.ai/user/gingiris).

---

*Version 1.2.0 — Released 2026-06-02*


---

## 🔗 About the Author

**Iris Wei** — Growth consultant for 150+ AI startups. Ex-COO at AFFiNE (69K GitHub stars).

- 🐦 Twitter: [@WeiYipei](https://twitter.com/WeiYipei) — Daily growth tactics
- 💬 Consulting: [@Iris_carrot on Telegram](https://t.me/Iris_carrot)
- 🛒 Premium Bundle (all 5 playbooks + templates): [Get on Gumroad ($249)](https://gingiris.gumroad.com/l/gingiris-complete-global-launch-bundle)
- 📚 40+ Free Playbooks: [gingiris.tools/skills](https://gingiris.tools/skills/)
