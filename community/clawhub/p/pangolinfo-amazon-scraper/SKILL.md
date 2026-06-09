---
name: pangolinfo-amazon-scraper
description: Scrape Amazon as JSON — products, keywords, reviews, BSR. 13 regions. Anti-bot. 60 free credits. Claude Code, Cursor, LangChain.
homepage: https://pangolinfo.com/?referrer=clawhub_amz
license: MIT-0
metadata:
  openclaw:
    emoji: "🛒"
    os: ["darwin", "linux"]
    requires:
      env:
        - PANGOLINFO_API_KEY
        - PANGOLINFO_EMAIL
        - PANGOLINFO_PASSWORD
      primaryEnv: PANGOLINFO_API_KEY
      bins: ["python3"]
      notes: "Set PANGOLINFO_API_KEY (recommended). OR set PANGOLINFO_EMAIL + PANGOLINFO_PASSWORD to auto-fetch a key. Register free at https://tool.pangolinfo.com/?referrer=clawhub_amz — 60 free credits, no card."
tags: [amazon, amazon-scraper, asin, bsr, reviews, keyword-research, ecommerce, json, agent-tool, ai-agent, claude-code, cursor, langchain, free-tier, web-scraping, python]
version: 2.0.3
---

# Pangolinfo Amazon Scraper

Get Amazon product data in under a minute.

Use this skill when you want to:
- get **price, rating, and BSR** from an ASIN
- search **Amazon keywords** and compare results
- extract **critical reviews** and summarize complaints
- track **seller storefronts**, **best sellers**, and **product variants**

> 🎁 **New users get 60 free credits**. Enough for real product lookups, keyword tests, and review workflows before upgrading.
> 👉 [Get your free API key](https://tool.pangolinfo.com/?referrer=clawhub_amz) — about 30 seconds.

## First win in 30 seconds

1. Get your free API key: <https://tool.pangolinfo.com/?referrer=clawhub_amz>
2. Set the environment variable:

```bash
export PANGOLINFO_API_KEY="pgl_xxx"
```

3. Run your first lookup:

```bash
python3 scripts/pangolinfo.py --asin B0DYTF8L2W --site amz_us
```

4. If you see fields like these, the skill is working:
- `title`
- `price`
- `star`
- `bestSellersRank`

## What to do next

### Check your own product
```bash
python3 scripts/pangolinfo.py --asin YOUR_ASIN --site amz_us
```

### Search a keyword
```bash
python3 scripts/pangolinfo.py --q "wireless mouse" --site amz_us
```

### Find top complaints from reviews
```bash
python3 scripts/pangolinfo.py --asin YOUR_ASIN --mode review --filter-star critical --pages 1
```

## First-time setup (agent instructions)

**If `PANGOLINFO_API_KEY` is not set, the agent MUST guide the user as follows and stop there. Do not attempt the API call without credentials.**

> "This skill needs a free Pangolinfo API key.
>
> 1. Visit https://tool.pangolinfo.com/?referrer=clawhub_amz
> 2. Sign up and copy your API key
> 3. Run: `export PANGOLINFO_API_KEY='pgl_xxx'`
> 4. Verify: `python3 scripts/pangolinfo.py --auth-only`
>
> Then ask me to retry your request."

The API key does not expire. For interactive setup, see [references/setup-guide.md](references/setup-guide.md).

## What this skill can do

This skill returns structured Amazon data across **13 marketplaces** (US/UK/CA/DE/FR/JP/IT/ES/AU/MX/SA/AE/BR). CAPTCHA and anti-bot handling run in the cloud.

## 🎯 Capabilities (9 Parsers)

| Parser | Use case | Quick example |
|--------|----------|---------------|
| `amzProductDetail` *(default)* | ASIN details: price, BSR, rating, attributes | `--asin B0DYTF8L2W` |
| `amzKeyword` | Keyword search (organic + sponsored rank) | `--q "wireless mouse"` |
| `amzProductOfCategory` | Category listings | `--content <nodeID> --parser amzProductOfCategory` |
| `amzProductOfSeller` | Seller storefront products | `--content <sellerID> --parser amzProductOfSeller` |
| `amzBestSellers` | BSR rankings by category | `--content electronics --parser amzBestSellers` |
| `amzNewReleases` | New releases by category | `--content electronics --parser amzNewReleases` |
| `amzFollowSeller` | Follow seller updates *(separate endpoint)* | `--asin B0DYTF8L2W --parser amzFollowSeller` |
| `amzVariantAsin` | Get variant ASINs *(separate endpoint)* | `--asin B0G4QPYK4Z --parser amzVariantAsin` |
| `amzReviewV2` | Product reviews with star/sort filters | `--asin B0DYTF8L2W --mode review --filter-star critical` |

The script auto-infers parser from input (ASIN → `amzProductDetail`, keyword → `amzKeyword`).

---

## 🌍 Supported Marketplaces (13 regions)

| Code | Domain | Code | Domain |
|------|--------|------|--------|
| `amz_us` | amazon.com | `amz_jp` | amazon.co.jp |
| `amz_uk` | amazon.co.uk | `amz_it` | amazon.it |
| `amz_ca` | amazon.ca | `amz_es` | amazon.es |
| `amz_de` | amazon.de | `amz_au` | amazon.com.au |
| `amz_fr` | amazon.fr | `amz_mx` | amazon.com.mx |
| `amz_br` | amazon.com.br | `amz_sa` | amazon.sa |
| `amz_ae` | amazon.ae | | |

Default: `amz_us`. Pass via `--site amz_uk` etc.

---

## 💰 Credit Consumption

| Operation | Credits |
|-----------|---------|
| Product / keyword / category / seller / bestsellers (`--format json`) | **1** |
| Same with `--format rawHtml` or `markdown` | **0.75** |
| Follow Seller | **1** |
| Variant ASIN | **1** |
| Review page (`--mode review`) | **5 per page** |

→ 60 free credits = 60 product lookups, OR 12 review pages, OR 80 raw HTML fetches.
→ Credits are charged **only on success** (`api_code: 0`).

---

## 📤 Sample Output

**Success (`stdout`):**
```json
{
  "success": true,
  "task_id": "02b3e90810f0450ca6d41244d6009d0f",
  "url": "https://www.amazon.com/dp/B0DYTF8L2W",
  "metadata": {
    "executionTime": 1791,
    "parserType": "amzProductDetail",
    "parsedAt": "2026-04-27T06:42:01.861Z"
  },
  "results": [
    {
      "asin": "B0DYTF8L2W",
      "title": "Sweetcrispy Convertible Sectional Sofa Couch...",
      "price": "...",
      "star": "4.4",
      "rating": "(22)",
      "bestSellersRank": "#2,329,042 in Home & Kitchen",
      "reviews": [ /* ... */ ],
      "aiReviewsSummary": { /* ... */ }
    }
  ],
  "results_count": 1
}
```

**Error (`stderr`):**
```json
{
  "success": false,
  "error": {
    "code": "API_ERROR",
    "api_code": 2001,
    "message": "Insufficient credits",
    "hint": "Top up at https://pangolinfo.com/?referrer=clawhub_amz"
  }
}
```

---

## 🛑 Error Handling (Agent Directives)

The script outputs structured error JSON to **stderr** on failure. Agent should map `api_code` as follows:

| `api_code` | Meaning | Agent action |
|-----------|---------|-------------|
| `0` | Success | Process `results` |
| `1004` | Invalid token | **Auto-retried by script** with refreshed credentials. No action. |
| `1009` | Invalid parser name | Check `--parser` value matches one of the 9 supported parsers |
| `2001` | Insufficient credits | Show top-up link. **Do NOT retry.** |
| `2005` | No active plan | Ask user to subscribe. **Do NOT retry.** |
| `2007` | Account expired | Ask user to renew at https://tool.pangolinfo.com/. **Do NOT retry.** |
| `2009` | Usage limit reached | Wait for next billing cycle. **Do NOT retry.** |
| `2010` | Bill day not configured | Tell user to contact support. **Do NOT retry.** |
| `4029` | Rate limited | `sleep 5s`, retry **once**. |
| `10000` / `10001` | Task execution failed | Retry **once** with corrected URL/ASIN. Likely transient. |

**Critical rule:** Errors `2001`, `2005`, `2007`, `2009`, `2010` mean **stop immediately** — retries waste credits and won't succeed.

Full error reference: [references/error-codes.md](references/error-codes.md).

---

## 📝 Common Recipes

```bash
# Product detail (US)
python3 scripts/pangolinfo.py --asin B0DYTF8L2W --site amz_us

# Same product on UK marketplace
python3 scripts/pangolinfo.py --asin B0DYTF8L2W --site amz_uk

# Keyword search
python3 scripts/pangolinfo.py --q "wireless mouse" --site amz_us

# Bestsellers in Electronics
python3 scripts/pangolinfo.py --content electronics --parser amzBestSellers --site amz_us

# Critical reviews (3 pages = 15 credits)
python3 scripts/pangolinfo.py --asin B0DYTF8L2W --mode review --filter-star critical --pages 3

# Variant ASINs (color/size options)
python3 scripts/pangolinfo.py --asin B0G4QPYK4Z --parser amzVariantAsin

# Auth check (free, no credits charged)
python3 scripts/pangolinfo.py --auth-only

# Raw HTML output (cheaper, 0.75 credits)
python3 scripts/pangolinfo.py --asin B0DYTF8L2W --format rawHtml
```

---

## 🎯 Quick Start Prompts (try with your agent)

- *"Get the price, rating, and BSR for ASIN B0DYTF8L2W on Amazon US."*
- *"Fetch the top 10 bestsellers in the Electronics category and return as CSV."*
- *"Scrape the first 50 critical reviews for B0DYTF8L2W and summarize the top 3 complaints."*
- *"Search Amazon UK for 'wireless earbuds' and list price + rating for the top 20 results."*
- *"Get all color/size variants of ASIN B0G4QPYK4Z."*

---

## 🚫 When NOT to use

- **Non-Amazon sites** (Walmart, Shopify, eBay) → use the corresponding Pangolinfo skill instead.
- **Real-time inventory / checkout** — this is a read-only scraping API.
- **Personal account data** — only public listings are accessible.

---

## 🤝 Compatible Agents

OpenClaw · Claude Code · Cursor · LangChain · LangGraph · Dify · AutoGen · Devin · Trae · Copilot

---

## 📚 References

- [Setup Guide](references/setup-guide.md) — interactive first-time setup
- [Error Codes](references/error-codes.md) — full troubleshooting reference
- [Official API Docs](https://docs.pangolinfo.com/en-index)
- [Amazon Scrape API endpoint](https://docs.pangolinfo.com/en-api-reference/amazonApi/amazonScrapeAPI)
- [Pricing & credits](https://www.pangolinfo.com/scrape-api-pricing-2/)

---

## 🌐 中文用户

亚马逊全域数据抓取 API：ASIN 详情、关键词排名、类目 BSR、评论、变体、卖家店铺。**支持 13 个站点**（美国、英国、加拿大、德国、法国、日本、意大利、西班牙、澳大利亚、墨西哥、沙特、阿联酋、巴西）。云端反爬，结构化 JSON 输出。

完美适配 OpenClaw、Claude Code、Cursor、LangChain 等 AI Agent 工作流。

**新用户注册即送 60 免费积分**，无需信用卡。

注册地址：https://tool.pangolinfo.com/?referrer=clawhub_amz
