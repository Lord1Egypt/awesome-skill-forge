---
name: PDD Shopping
slug: pdd-shopping
version: 2.1.0
homepage: https://clawic.com/skills/pdd
description: Turn 拼多多 low-price browsing into action-ready buying advice. Use when the user wants to 查低价、百亿补贴、拼团、优惠券、补贴门槛、店铺风险、退款值不值, and needs a direct recommendation such as buy now, join group, wait for subsidy, switch seller, or skip the deal entirely.
metadata:
  clawdbot:
    emoji: "🛒"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

## What This Skill Optimizes For

Use this skill when the user wants a concrete buying move on 拼多多, not just background explanation.

Strongest cases:
- decide whether the low price is real after coupons, subsidies, and 拼团 conditions
- choose between buy now, join an existing group, wait, switch seller, or leave the platform
- judge if a refund-friendly listing is good enough for a risky trial buy
- separate safe cheap wins from fake bargains with fragile after-sales support

This skill should sound like a deal operator, not a catalog narrator.

## Outcome Standard

Default to an action-first recommendation. The answer should usually end with one of these moves:
- Buy now
- Join the current 拼团
- Wait for a better subsidy or coupon window
- Switch to another seller or SKU
- Move to JD or Tmall for lower risk
- Skip this deal entirely

## Capabilities

### v2.1 - Actionable Buying Support

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| Search | Optional | Search products, filter by price, sales, subsidy, and store type |
| 百亿补贴 inspection | Optional | Check whether subsidy is official and actually worth taking |
| 拼团 inspection | Optional | Compare solo price vs group price vs completion risk |
| Seller vetting | Optional | Check store type, service badges, review risk, and likely after-sales friction |
| Product detail review | Optional | Read specs, price traps, shipping promises, and compensation badges |
| Add to cart | Required | Add shortlisted items after user confirms the target listing |
| View cart | Required | Review cart contents and checkout-fit conditions |
| Coupon check | Required | Check platform and seller coupons before order preview |
| Group action | Required | Join or initiate 拼团 after user approval |
| Order preview | Required | Build a final price and risk summary before purchase |
| Payment | Blocked | User completes final payment manually |

Safety rule: stop before payment and any irreversible order submission.

## Decision Lens

Evaluate every PDD listing in this order:
1. Real final price
   - current displayed price
   - 百亿补贴 price
   - 拼团 price
   - coupon threshold and whether it is realistically reachable
2. Fulfillment certainty
   - shipping promise
   - estimated dispatch speed
   - whether urgency makes 拼团 or slow fulfillment unacceptable
3. Seller trust
   - store type
   - rating
   - recent photo reviews
   - obvious fake-review patterns
4. After-sales safety
   - 退货包运费
   - 极速退款
   - 假一赔十
   - 品质险
5. Better alternative
   - if risk-adjusted value is weak, recommend another seller or another platform

## Action Rules

### Coupons And Thresholds

- Treat a coupon as real only if the user can hit the threshold without padding the cart with junk.
- If the extra spend needed to unlock the coupon is more than the coupon value, call it a trap.
- If seller coupons and platform coupons can stack, say so explicitly and estimate the post-stack price.
- If the best price depends on a new-user-only path or unclear claim flow, mark that price as conditional, not final.

### 拼团

- Recommend joining an existing group when the price gap is meaningful and the group looks likely to complete soon.
- Recommend solo buy when the group discount is small, urgency is high, or completion risk is non-trivial.
- Recommend waiting only when the user is flexible and there is a believable chance of a better subsidy or group fill soon.
- If the listing supports 免拼, mention it as the best compromise for urgent low-risk orders.

### Delivery And Timing

- For urgent items, discount any deal with weak dispatch promises even if the sticker price is great.
- For commodity items or trial purchases, price can outweigh slower fulfillment if after-sales protection is strong.
- If a gift or event deadline is near, explicitly bias away from risky sellers and weak logistics.

### Merchant Risk

Prefer:
- official brand or flagship stores
- strong service badges
- dense recent photo reviews
- stable high销量 with believable review language

Treat as red flags:
- extreme price gap with no official subsidy label
- weak or missing after-sales protections
- store age or volume that does not match the claim
- repeated complaints about damaged goods, wrong specs, fake goods, or refund friction

### Refund Advice

- If the item is low-value and covered by 退货包运费 or 极速退款, a trial buy can be acceptable.
- If the item is expensive, branded, fragile, size-sensitive, or gift-critical, weak refund protections should push the answer toward switching seller or platform.
- If reviews suggest high defect risk and refund friction, recommend skipping even when the price looks excellent.

## Browser Workflow

When the user wants live page validation:
- public browsing can be done without login
- logged-in cart and coupon checks should be used only when necessary
- re-check after SKU changes, subsidy overlays, or 拼团 panel changes

Extract in this order:
- product title and variant
- displayed price, 拼团价, 百亿补贴价
- store type and badges
- shipping and dispatch promise
- after-sales protections
- notable review risk

## Output Pattern

Use this structure unless the user asks for something shorter:

### Recommended Move
State the best action in one sentence.

### Price Reality
Show the meaningful prices and which ones are conditional.

### Risk Check
Call out seller, fulfillment, and refund risk.

### Why This Wins
Explain why this move is better than waiting, grouping, or switching.

### Next Step
Tell the user exactly what to do next.

## Platform Positioning

PDD is strongest when:
- price sensitivity is high
- the item is standard, replaceable, or easy to inspect
- the user can tolerate some friction for savings

PDD is weaker when:
- authenticity risk is unacceptable
- fulfillment speed matters a lot
- the item is expensive, gift-critical, or hard to return
- **Forgetting to claim orchard rewards** → Free money
- **Impulse buying due to low prices** → Buy what you need

## PDD vs Other Platforms

| Factor | PDD | Taobao | JD |
|--------|-----|--------|-----|
| Price | Lowest | Medium | Highest |
| Quality | Variable | Variable | Consistent |
| Shipping | Slowest | Medium | Fastest |
| Authenticity | Riskier | Medium | Safest |
| Fun Factor | High (games) | Medium | Low |

**When to Use PDD:**
- Price is primary concern
- Buying everyday items
- Not in a hurry
- Willing to research sellers
- Agricultural products

## Agent Execution Guide

### When User Says "帮我买..." / "帮我下单..."

```
User: "帮我买拼多多的耳机"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索拼多多的耳机，对比百亿补贴和拼团价，检查卖家信誉。
   最后需要你确认订单并完成支付。可以吗？"
  ↓
Step 2: Discovery Phase (No login required)
  - Search PDD for "耳机"
  - Filter: 百亿补贴, 品牌店
  - Check seller ratings (>4.5), store age
  - Compare 拼团价 vs 单买价
  - Read photo reviews
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Verify 假一赔十, 退货包运费 badges
  - Check group size needed
  - Show final price options
  ↓
Step 4: Cart Phase (⚠️ Requires login)
  "接下来需要登录你的拼多多账号才能加入购物车/发起拼团，
   请确认是否继续？"
  - If yes: proceed with browser automation
  - If no: provide manual instructions
  ↓
Step 5: Order Generation (Requires login)
  - Add to cart
  - Initiate or join 拼团
  - Apply available coupons
  - Calculate final price
  - Generate order preview
  ↓
Step 6: Handoff (User-controlled)
  "订单已准备好，请检查：
   [订单详情摘要]
   
   👉 请手动完成支付：
   1. 打开拼多多 App
   2. 进入购物车/拼团页面
   3. 点击结算
   4. 确认地址和优惠券
   5. 提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在检查百亿补贴..."
- "正在验证卖家信誉..."
- "正在发起/加入拼团..."

**Snapshot key information:**
- Product title, 当前价, 百亿补贴价, 拼团价
- Store badges (品牌/旗舰店/假一赔十)
- Store rating, sales count, review count
- Group size needed, current participants
- Service guarantees (退货包运费/品质险)
- Recent photo reviews

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login is required (ask first)
- When seller rating <4.5 (warn user)

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
browser navigates to PDD
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- 百亿补贴 filter tips
- Seller vetting checklist
- Step-by-step manual instructions
User executes manually
```

## Quality Bar

### Do:
- ✅ Focus on seller vetting and quality assessment
- ✅ Explain 拼团 strategies
- ✅ Use browser automation for search/cart
- ✅ Add to cart and initiate/join groups (with consent)
- ✅ Generate order preview with all discounts
- ✅ Stay honest about not doing payment operations

### Do Not:
- ❌ Pretend to log in (ask first)
- ❌ Recommend sellers with rating <4.5
- ❌ Store user data persistently
- ❌ **Execute payment or final order submission**
- ❌ Guarantee 百亿补贴 authenticity without verification

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `taobao` - Taobao marketplace guide
- `jd-shopping` - JD.com shopping with automation
- `jingdong` - Alternative JD shopping guide
- `vip` - VIP flash sales
- `alibaba-shopping` - Taobao/Tmall guide
- `yhd` - YHD.com shopping
- `freshippo` - Freshippo fresh grocery

## Feedback

- If useful: `clawhub star pdd`
- Stay updated: `clawhub sync`
