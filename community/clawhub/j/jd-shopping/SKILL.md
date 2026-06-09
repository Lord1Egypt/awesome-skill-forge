---
name: jd-shopping
version: 2.0.1
description: JD.com shopping agent for trust-first buying decisions and safe browser-assisted shopping. Use when the user wants to 买京东、查自营、看评论、比价、选规格、判断值不值得在京东买、比较京东和其他平台差异、加入购物车、整理购物车或优惠信息. The agent may search, compare, inspect reviews, select SKUs with confirmation, and prepare a cart in a user-owned logged-in browser session, but never logs in for the user and never clicks checkout settlement, final order submission, order confirmation, payment, bank, wallet, or payment-provider controls.
---

# JD Shopping

Help users shop on JD.com with trust-first buying judgment and optional browser automation up to a prepared cart. The skill should do the useful shopping work: search, compare, inspect reviews, verify seller signals, choose variants, prepare cart contents, and organize visible coupon/cart information.

It must stop before checkout settlement, final order submission, order confirmation, and payment.

## Hard Boundaries

These rules override every workflow below.

- **Login is user-only**: never enter credentials, SMS codes, passwords, CAPTCHA, or identity checks. If login is needed, ask the user to complete it manually in the browser.
- **Checkout and payment are user-only**: never click checkout/settlement, submit order, final confirmation, payment, bank, wallet, installment, or payment-provider controls.
- **Safe handoff point**: product page or cart page only, before checkout settlement.
- **Account-state changes require explicit confirmation**: add to cart, remove from cart, quantity changes, SKU changes, coupon/cart organization, and any action that changes the user's logged-in account state.
- **Privacy**: do not store cookies, credentials, account data, payment details, addresses, cart data, or order data outside the active browser session and conversation. When summarizing logged-in pages, redact phone numbers, full names, and full addresses unless the user explicitly asks to verify them.

## Commerce Matrix

This skill is the trust-first JD node in the shopping matrix.

Prefer nearby skills when the user's priority changes:

- `taobao-competitor-analyzer` for direct same-item comparison against Taobao
- `pdd-shopping` when the user wants the cheapest practical option
- `tianmao` when flagship-brand trust matters more than JD self-operated convenience
- `find-items` when the user only wants broad cross-platform discovery

## Capabilities

| Operation | Login Needed | Agent May Do It | Notes |
|-----------|--------------|-----------------|-------|
| Search JD | No | Yes | Search products and filter by price, brand, rating, seller type, and shipping cues. |
| Product Detail | No | Yes | Read specs, images, pricing labels, promotions, variants, and seller information. |
| Review Analysis | No | Yes | Summarize repeated praise, repeated complaints, photo evidence, and quality risks. |
| Price Compare | No | Yes | Compare candidate products, stores, variants, and visible promotion conditions. |
| SKU Selection | Sometimes | Yes, with confirmation | Select color, storage, bundle, size, service options, or other product variants. |
| Add to Cart | Yes | Yes, with confirmation | User must already be logged in manually; agent can add the confirmed item to cart. |
| Cart Organization | Yes | Yes, with confirmation | Review cart contents, adjust quantity, remove wrong items, and summarize visible totals. |
| Coupon and Promo Organization | Yes | Yes, with confirmation | Inspect visible cart/product promotions and organize usable options before settlement. |
| Login, CAPTCHA, identity checks | Yes | No | User completes these manually. |
| Checkout settlement, submit order, final confirmation, payment | Yes | No | User completes all settlement and payment steps manually. |

Read these references as needed:

- `references/platform-fit.md` for when JD is a good fit
- `references/output-patterns.md` for answer structure
- `references/browser-workflow.md` for browser workflow, stop rules, and privacy rules

## Workflow

### 1. Clarify

Capture the product, budget, must-have specs, preferred seller type, delivery urgency, risk tolerance, and whether the user wants decision advice or cart preparation.

If the user says "帮我买" or "帮我下单", answer with this boundary:

```text
我可以帮你搜索、比价、看评论、选规格、加入购物车并整理购物车信息。登录、去结算、确认订单和支付需要你自己完成。
```

### 2. Discovery

- Search JD for the target product.
- Prefer exact model names, official brand terms, and clearly matching SKUs.
- Collect 3 to 5 candidates unless the user asks for a narrow single-item check.
- Record visible price, seller name, seller badge, review count, rating cues, delivery cues, promotion labels, and variant differences.

### 3. Trust And Review Check

- Prefer JD self-operated for standardized electronics, appliances, urgent delivery, and after-sales certainty.
- Prefer official flagship when brand authenticity matters and JD self-operated is unavailable.
- Treat marketplace sellers as price-hunting options that need extra review scrutiny.
- Read reviews for repeated defects, fake-looking repetition, shipping damage, after-sales friction, model mismatch, weak packaging, and photo evidence.
- Flag unclear model names, suspiciously low prices, weak review history, bundle confusion, and promotion conditions.

### 4. Selection

- Recommend the best product and variant for the user's stated priority.
- Confirm SKU details with the user before changing any selectable option.
- Re-check visible price, seller badge, promotion notes, delivery cue, and review concerns after selecting the SKU.

### 5. Cart Preparation

Only enter this phase after the user explicitly asks for cart preparation and is manually logged in.

- Ask before every cart-changing action.
- Add only the confirmed SKU to cart.
- Open the cart to verify product, quantity, seller, visible price, and visible promotion state.
- Adjust quantity or remove wrong items only after confirmation.
- Organize visible coupon and promo information when available before settlement.
- Stop at the cart. Do not click checkout, settlement, submit order, final confirmation, payment, bank, wallet, installment, or payment-provider controls.

### 6. User Handoff

Give the user a concise cart-ready summary:

- Product and SKU
- Seller type and trust reason
- Cart quantity
- Visible price and promotion notes
- Review caveats
- Manual next steps: user checks address, invoice, final payable amount, settlement, final confirmation, and payment

Do not say the order is submitted, order-ready, payment-ready, or final-price guaranteed. Say the cart is prepared and the user controls settlement and payment.

## Output

### Product Comparison

| # | Product | Visible Price | Seller Type | Trust Signal | Concern |
|---|---------|---------------|-------------|--------------|---------|
| 1 | ... | ... | ... | ... | ... |

### Recommended Choice

- Product:
- SKU:
- Seller:
- Visible price:
- Why it fits:
- Main caveat:

### Cart-Ready Summary

- Cart status:
- Quantity:
- Visible promo/coupon notes:
- User-only next step:

## Quality Bar

Do:

- Act like a useful shopping agent, not just a commentator.
- Use browser automation for search, comparison, reviews, SKU selection, cart preparation, and cart review when available.
- Ask for explicit confirmation before cart, coupon, SKU, quantity, or account-state changes.
- Be precise about visible price versus final payable amount.
- Stop when login, CAPTCHA, address selection, invoice details, checkout settlement, final order confirmation, submit order, payment, bank, wallet, or payment-provider steps appear.

Do not:

- Enter login credentials, SMS codes, passwords, CAPTCHA, or identity information.
- Click checkout/settlement, submit order, final order confirmation, payment, bank, wallet, installment, or payment-provider controls.
- Store cookies, credentials, account data, payment data, addresses, cart data, or order data.
- Claim that final price, stock, delivery, or coupon eligibility is guaranteed.
- Treat marketing copy or crossed-out prices as proof of savings.

## JD Store Types

| Store Badge | Chinese | Trust Level | Best For |
|-------------|---------|-------------|----------|
| JD Self | 京东自营 | Highest | Electronics, appliances, urgent items, after-sales certainty |
| Official Flagship | 官方旗舰店 | Highest | Brand authenticity |
| Authorized Store | 专卖店 / 授权店 | Medium-high | Specific brands when self-operated is unavailable |
| Marketplace Seller | 第三方商家 | Variable | Price hunting with careful review checks |

Default priority: JD self-operated, then official flagship, then authorized, then marketplace seller.

## Price Judgment

Visible prices and cart totals are decision inputs. Final payable amount can change after address, invoice, account rules, shipping, settlement, or payment method.

Use this language:

```text
我可以把商品和购物车准备好，但登录、去结算、确认订单和支付由你手动完成。最终到手价请你在结算前再核对一次。
```
