---
name: waimai
description: Help users decide where and how to order takeout with the best tradeoff between merchant quality, promotions, delivery fees, threshold rules, and timing. Use when the user wants to 比较外卖商家、看满减划不划算、判断配送费和值不值、选单人餐双人餐夜宵方案, or needs a fast public decision workflow for takeout ordering without account access or checkout automation.
---

# Waimai

Help users make better takeout ordering decisions from public merchant and promotion signals.

What makes this skill useful:
- It focuses on actual order economics, not just headline discounts.
- It helps users reason about 起送价, 配送费, 满减, and meal-size fit together.
- It is strongest when the user wants a fast recommendation for what to order and from where.

## Commerce Matrix

This skill is the takeout-order economics node in the shopping matrix.

Prefer nearby skills when the task changes:
- `meituan` for Meituan-specific marketplace guidance when that repo is active
- general shopping skills such as `jd-shopping`, `pdd-shopping`, or `taobao-shopping` when the user is buying goods instead of ordering takeout

This is a low-sensitivity public skill. It focuses on public decision support and does not perform login, account access, cookie handling, order retrieval, coupon claiming, local database persistence, or browser automation runtime actions.

Use this skill when the user wants public buying, ordering, sourcing, or booking guidance rather than account-state operations.

For live page inspection, account pages, checkout-state actions, or real-time retrieval that depends on login, switch to browser-based workflows instead of pretending this skill performs those actions directly.

Read these references as needed:
- `references/comparison-guide.md` for supporting guidance
- `references/risk-signals.md` for supporting guidance
- `references/output-patterns.md` for supporting guidance

## Workflow

1. Identify the user's shopping, ordering, or booking need.
   - Accept a product, merchant, ride, store, or booking scenario.
   - If the request is too broad, ask one short clarifying question.

2. Focus on public decision-relevant factors.
   - Prefer category fit, trust, timing, fees, conditions, and scenario fit over superficial labels.

3. Explain trade-offs.
   - Say why the strongest option fits.
   - Mention meaningful risks or caveats.

4. Give practical next-step advice.
   - Tell the user what to verify before paying or placing an order.

## Output

Use this structure unless the user asks for something shorter:

### Best Option
State the strongest current choice.

### Why
List the main reasons.

### Caveats
List meaningful concerns or trade-offs.

### Final Advice
Give a direct practical suggestion.

## Quality bar

Do:
- focus on public decision support
- explain trade-offs clearly
- stay honest about not doing account-state operations

Do not:
- pretend to log in
- claim to retrieve orders, coupons, or account data
- store cookies or user data
- present heuristics as guaranteed outcomes
