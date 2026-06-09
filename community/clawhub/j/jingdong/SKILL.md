---
name: Jingdong Shopping
slug: jingdong
version: 2.0.0
homepage: https://clawic.com/skills/jingdong
description: Navigate JD.com (京东) with expert shopping strategies, authenticity checks, logistics optimization, and browser-based product search, reviews, price comparison, and cart operations. Supports logged-in workflows for personalized results while keeping checkout/ payment for user control.
metadata:
  clawdbot:
    emoji: "📦"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

## When to Use

User wants to shop on JD.com (京东), China's premier B2C e-commerce platform. Agent helps with product authenticity verification, price optimization, and leveraging JD's superior logistics network.

## Quick Reference

| Topic | File |
|-------|------|
| Store type guide | `stores.md` |
| Price strategies | `pricing.md` |
| Logistics mastery | `shipping.md` |

## Browser Workflow Upgrade

When the task requires live JD page inspection, follow the shared **browser-commerce-base** workflow:
- public search/detail pages → `openclaw`
- logged-in carts, coupons, orders, PLUS pages → `user` only when needed
- re-snapshot after region switch, coupon reveal, or SKU changes
- capture store type and logistics promise as first-class evidence

### Supported Operations (v2.0)

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by price/rating/brand |
| **Product Detail** | Optional | View specs, images, pricing, promotions |
| **Reviews** | Optional | Read user reviews, ratings, photos |
| **Price Compare** | Optional | Compare prices across sellers/variants |
| **Add to Cart** | ✅ Required | Add items to shopping cart |
| **View Cart** | ✅ Required | Review cart contents, quantities |
| **Apply Coupons** | ✅ Required | Check and apply available coupons |
| **Generate Order** | ✅ Required | Fill address, select shipping, calculate final price |
| **Payment** | ❌ Blocked | User must complete payment manually |

**Important**: All checkout operations stop before payment. User retains full control over final purchase decision and payment execution.

Key browser extraction order on JD:
- 商品标题
- 京东价 / PLUS价 / 到手价
- 店铺类型（自营 / 旗舰店 / 第三方）
- 物流时效 / 配送承诺
- 优惠券 / 满减 / 补贴
- 规格切换后的价格刷新
- 用户评价 / 好评率 / 晒单图片

## Core Rules

### 1. JD Store Types Decoded

Understanding JD's ecosystem is crucial for safe shopping:

| Store Badge | Chinese | Trust Level | Best For |
|-------------|---------|-------------|----------|
| **JD Self** | 京东自营 | ⭐⭐⭐⭐⭐ | Electronics, urgent items |
| **Flagship** | 官方旗舰店 | ⭐⭐⭐⭐⭐ | Brand authenticity |
| **Authorized** | 专卖店 | ⭐⭐⭐⭐☆ | Specific brands |
| **3rd Party** | 第三方商家 | ⭐⭐⭐☆☆ | Price hunting |

**Priority Order:** 自营 > 旗舰店 > 专卖店 > 第三方

### 2. The 自营 Advantage

**Why JD Self-Operated Wins:**

| Factor | 自营 | 3rd Party |
|--------|------|-----------|
| Authenticity | 100% guaranteed | Varies |
| Shipping speed | Same/next day | 2-5 days |
| Return service | Pickup included | Self-return |
| Customer service | JD handles | Seller handles |
| Price protection | Automatic | Manual claim |

**识别自营:**
- Look for "京东自营" red badge
- Ships via "京东物流"
- Product URL contains "jd.com"

### 3. Price Optimization

**Understanding JD Pricing Tiers:**

| Price Label | Meaning | Strategy |
|-------------|---------|----------|
| **划线价** | Crossed-out "original" | Often inflated |
| **京东价** | Current listed price | Baseline |
| **PLUS价** | Member discount | Join if frequent buyer |
| **秒杀价** | Flash sale | Set alerts |
| **到手价** | After coupons | Real cost |

**Best Deal Formula:**
```
Final Price = 京东价 - 店铺券 - 平台券 - PLUS折扣 - 支付优惠
```

**Timing for Best Prices:**
- **618** (June 1-18) - Mid-year mega sale
- **双11** (Nov 11) - Singles Day
- **双12** (Dec 12) - Year-end clearance
- **Monthly 18th** - Regular promotions

### 4. PLUS Membership Deep Dive

**Annual Cost:** ¥198 (often ¥99-149 on promotion)

**Core Benefits:**

| Benefit | Value |
|---------|-------|
| Free shipping | Saves ¥6-15/order |
| 10x 京豆 (beans) | 1% cashback |
| Member-only prices | 5-20% off |
| Return shipping | Free pickup |
| Priority service | Faster support |

**Worth It Calculator:**
- Order 2+ times/month → Yes
- Average order >¥150 → Yes
- Buy electronics regularly → Definitely yes

### 5. Logistics Excellence

**JD's 211 Promise:**

| Order Time | Delivery Commitment |
|------------|---------------------|
| Before 11 AM | Same day by 11 PM |
| Before 11 PM | Next day by 3 PM |

**Delivery Options:**

| Service | Speed | Use Case |
|---------|-------|----------|
| 标准快递 | 1-3 days | Regular orders |
| 京准达 | Scheduled window | Time-sensitive |
| 夜间配 | 7-10 PM | Working professionals |
| 自提点 | Flexible pickup | Privacy/convenience |

**Tracking Features:**
- Real-time GPS map
- Driver contact info
- Photo confirmation
- Delivery time prediction

### 6. Smart Shopping Workflow (Agent-Assisted v2.0)

#### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches JD for target product
2. **Filter & Sort** - Apply filters (price range, rating, brand, 自营 only)
3. **Compare** - Agent compares top 3-5 options across stores
4. **Reviews** - Agent reads user reviews, extracts common pros/cons
5. **Price Analysis** - Agent checks current price, promotions, coupon stackability

#### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Variant Selection** - Confirm color, size, configuration
3. **Seller Verification** - Confirm 自营/旗舰店 status
4. **Final Price Check** - Calculate 到手价 after all discounts

#### Phase 3: Cart & Pre-Order (Agent-Assisted with Login)
1. **Add to Cart** - Agent adds item to cart (requires login)
2. **Cart Review** - Agent shows cart contents, quantities, subtotal
3. **Coupon Application** - Agent checks and applies best coupons
4. **Address Selection** - Agent confirms delivery address
5. **Shipping Options** - Agent shows available delivery methods
6. **Order Summary** - Agent generates complete order preview

#### Phase 4: Checkout (User-Controlled)
1. **Handoff** - Agent presents final order details
2. **User Review** - User confirms all details are correct
3. **Payment** - ⚠️ **User completes payment manually**
4. **Confirmation** - User shares order confirmation with agent if desired

**Agent Boundary**: Stops at Phase 3. Never executes payment or final order submission.

---

#### Legacy Workflow (for reference)

**Before Purchase:**
1. Check if 自营 available
2. Compare with 旗舰店 pricing
3. Apply all available coupons
4. Check price history (if possible)
5. Read photo reviews
6. Verify specifications

**During Purchase:**
1. Select correct variant (color/size)
2. Choose delivery speed
3. Apply payment discounts
4. Confirm address

**After Purchase:**
1. Track delivery progress
2. Inspect immediately on arrival
3. Test electronics within return window
4. Claim price protection if applicable

### 7. Returns & Protection

**Return Policy by Category:**

| Category | Window | Notes |
|----------|--------|-------|
| General | 7 days | Unused, tags on |
| Electronics | 7 days | Unactivated |
| Clothing | 7 days | Unworn |
| Food | No return | Unless spoiled |
| Custom | No return | Personalized |

**Price Protection (价保):**
- 7-day automatic for 自营
- 30-day manual claim for others
- Must be same product, same seller
- Refund difference to original payment

## Agent Execution Guide

### When User Says "帮我买..."

Follow this escalation path:

```
User: "帮我买 Mac mini"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索 Mac mini，对比选项，加入购物车。
   最后需要你确认订单并完成支付。可以吗？"
  ↓
Step 2: Discovery Phase (No login required)
  - Search JD for "Mac mini M4"
  - Filter: 自营/旗舰店, sort by rating
  - Compare top 3 options
  - Read reviews for each
  - Present comparison table
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Confirm variant/specs
  - Show final price
  ↓
Step 4: Cart Phase (⚠️ Requires login)
  "接下来需要登录你的京东账号才能加入购物车，
   请确认是否继续？"
  - If yes: proceed with browser automation
  - If no: provide manual instructions
  ↓
Step 5: Order Generation (Requires login)
  - Add to cart
  - Apply coupons
  - Select address
  - Calculate final price
  - Generate order preview
  ↓
Step 6: Handoff (User-controlled)
  "订单已准备好，请检查：
   [订单详情摘要]
   
   👉 请手动完成支付：
   1. 打开京东 App
   2. 进入购物车
   3. 点击结算
   4. 确认地址和优惠券
   5. 提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在打开商品页面..."
- "正在读取用户评价..."
- "正在加入购物车..."

**Snapshot key information:**
- Product title, price, promotions
- Store type badge
- Rating and review count
- Available variants
- Coupon information
- Delivery estimate

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login is required (ask first)
- When price differs significantly from expected

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
openclaw browser navigates to JD
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: User provides login via secure method**
```
⚠️ Never ask for password in chat
Guide user to login in their browser first
Then agent takes over with active session
```

**Option C: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- Product links
- Coupon codes to apply
- Step-by-step manual instructions
User executes manually
```

---

## Common Traps

- **Assuming JD = always authentic** → Check store type first
- **Ignoring PLUS pricing** → Significant savings missed
- **Not checking 211 coverage** → Your area may differ
- **Missing coupon stacking** → Multiple discounts available
- **Buying from new sellers** → Higher risk, less protection
- **Forgetting price protection** → Free money left behind
- **Rushing electronics activation** → Test first, activate later
- **Agent overstepping** → Never complete payment for user

## JD vs Competitors

| Factor | JD | Taobao | VIP |
|--------|-----|--------|-----|
| Authenticity | Best | Varies | Good |
| Shipping | Fastest | Varies | Standard |
| Electronics | Best choice | Riskier | Limited |
| Price | Higher | Lower | Discounted |
| Service | Excellent | Varies | Good |

**When to Choose JD:**
- Electronics and appliances
- Time-sensitive purchases
- High-value items
- When authenticity matters most

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `jd-shopping` - Alternative JD guide
- `taobao` - Taobao marketplace
- `vip` - VIP flash sales
- `alibaba-shopping` - Taobao/Tmall guide

## Feedback

- If useful: `clawhub star jingdong`
- Stay updated: `clawhub sync`
