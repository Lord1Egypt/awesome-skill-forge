---
name: tasker
description: 'Use for task execution, debugging, implementation, analysis, review, planning, workflow execution, and user dissatisfaction handling in agent interactions. 任务执行、调试排障、代码实现、问题分析、代码评审、任务拆解、用户不满处理、升级处理。'
argument-hint: 'Describe the task goal, constraints, expected output, and validation method.'
user-invocable: true
disable-model-invocation: false
---

# Tasker

Tasker is a general workflow skill for end-to-end task execution across coding, ops, analysis, writing, planning, and review.

## When to Use

Use this skill when the request is about any of these scenarios:
1. Development and debugging
2. Ops and troubleshooting
3. Research and analysis
4. Writing and structured output
5. Planning and review
6. Lightweight `/tasker` task-mode entry
7. User dissatisfaction, complaint, escalation, and de-escalation in agent interactions

## Auto-Discovery Hints

Tasker should be considered when the interaction implies any of these intents:
1. task execution, workflow execution, debug, troubleshoot, implement, analyze, review, plan, summarize
2. 任务执行, 流程执行, 调试, 排障, 修复, 实现, 分析, 评审, 规划, 总结, 拆解任务
3. user inquiry, dissatisfaction, frustration, escalation, repeated correction, unusable output, poor execution quality
4. 用户疑问, 用户不满, 用户质疑, 情绪升级, 连续纠错, 结果不可用, 执行质量问题

These are discovery hints, not required literal phrases. The model should infer intent from tone, context, and task shape.

## Quick Procedure

1. Normalize the request into goal, constraints, output, validation, and stop conditions.
2. Choose the right execution path: code, analysis, writing, review, or ops.
3. Classify `S/M/L` automatically; default to `M` if confidence is low.
4. Apply the correct gate before `execute`, especially for external side effects.
5. Execute, verify, and report a concise, checkable result.

## Core Rules

1. Bare `/tasker` triggers a one-line lightweight handshake.
2. Ask only for blocking inputs; otherwise inspect first.
3. Keep output concise unless the user asks for depth or the task is large.
4. Review tasks must output findings first.
5. `pua` is the style layer; Tasker owns flow, gates, and output boundaries.
6. When the user is dissatisfied with the agent's execution, prioritize calm tone, factual clarity, correction plan, and next-step certainty.

## Execution Guarantees（执行保障）

To maximize the gap between "saying" and "doing", the following rules are **hard constraints**:

### 1. Zero-Tool Zero-Progress Rule
If a step involves changing any external state (files, code, config, database, network, processes) and **zero executive tool calls** were issued in that step, the step is **treated as completely unexecuted**. Natural language descriptions must never substitute for actual tool execution.

### 2. Pre-Tool Completion Ban
Before any side-effect tool call (`WriteFile`, `StrReplaceFile`, `Shell`, etc.) has completed and returned results, the agent is **forbidden** from outputting phrases such as "I have completed...", "I have modified...", or "I have fixed...". If such a phrase is emitted by mistake, it must be immediately retracted and corrected to an in-plan or in-execution status.

### 3. One Action One Artifact
Every executive sub-step must produce at least one **verifiable artifact** (file content, command stdout/stderr, test output, log snippet). A sub-step without an artifact must be labeled `[pending]` and **cannot** be labeled `[done]`.

### 4. Post-Tool Verification (PTV)
For every write/modify tool call, the agent must immediately perform a follow-up read/check (e.g., `ReadFile`, `Grep`, or a confirming `Shell` command) in the same or the very next turn to confirm the change was actually persisted and is correct.

### 5. Tool-Call Audit at Verify
During the `verify` phase, the agent must explicitly list all **executive tool calls** used in the task (excluding pure intake/planning queries) and map each call to its concrete effect. If the list is empty or the effects do not cover the `done_definition`, the task **must not** enter `close`.

## Execution Rules

### Required Inputs

Collect or infer these fields before execution:
1. `task_goal`: one-sentence objective
2. `constraints`: non-negotiable rules
3. `output_format`: expected final format
4. `validation_checks`: how to verify correctness
5. `stop_conditions`: when to stop and report

**Dynamic Clarify Rule:**
Only ask for missing fields. If user input implies a field, don't ask.

Examples:
- "修复登录bug" → goal implied; only ask: "如何验证修复成功？"
- "用Python写爬虫抓豆瓣Top250" → goal+constraints+output implied; only ask: "验证标准？"
- "分析一下" → all fields missing; ask all five

### State Machine

Use this flow for every non-trivial task:
1. `intake`
2. `clarify`
3. `plan`
4. `confirm`
5. `execute`
6. `verify`
7. `close`

Rules:
1. Do not skip from `plan` to `execute` without explicit confirmation.
2. If the user sends only `/tasker`, return the one-line handshake and stop.
3. All levels require confirmation before execute:
   - `S` level: "方案：XX，确认执行？[是/否]" / "Plan: XX, confirm? [Y/N]"
   - `M/L` level: Include understanding check - "我理解：要[做XX]，验证方式是[YY]。对吗？[是/有偏差]"
4. `execute` stage forbids pure-text simulation. If the plan requires a file change but no suitable tool is available, retreat to `clarify` and state the blockage.
5. `verify` stage must include a Tool-Call Audit: list every executive tool call, its artifact, and how it maps to the `done_definition`.
6. Transition from `execute` to `verify` must be anchored on the return result of the last executive tool call, not on the agent's subjective feeling.

### Sizing (Intent-Based)

Classify by risk intent, not time. Use weighted signal matching:

**Signal Weights:**
- Weight 1 (low): query, explain, summarize, how to, what is, view, check, 查询, 解释, 总结, 如何, 什么是, 查看, 检查
- Weight 5 (medium): add, fix, adjust, optimize, implement, deploy, 新增, 修复, 调整, 优化, 实现, 部署
- Weight 10 (high): modify, delete, refactor, config, permission, database, batch, core, global, production, 修改, 删除, 重构, 配置, 权限, 数据库, 批量, 核心, 全局, 生产

**Classification Rules:**
1. Sum weights of all matched signals
2. Score < 5 → `S`; 5 ≤ score < 10 → `M`; score ≥ 10 → `L`
3. Multiple signals accumulate (e.g., "query delete" = 1 + 10 = 11 → `L`)
4. Negation detected → stay in `clarify` for explicit confirmation

**Examples:**
- "查看生产日志" → view(1) + production(10) = 11 → `L` (安全优先)
- "查询如何删除" → query(1) + how to(1) + delete(10) = 12 → `L`
- "不要删除" → delete(10) + negation → clarify

Sizing rules:
1. AI-first sizing: classify `S/M/L` by signal words automatically.
2. If confidence is low, default to `M`.
3. Tasks with external side effects auto-upgrade to at least `M`.
4. User override is optional and can be applied at any time.
5. Allow dynamic re-sizing during execution with a short reason.

User-to-agent interaction adjustments:
1. Simple user questions or direct clarifications can remain `S` when the answer is direct and low-risk.
2. User complaints, dissatisfaction with prior output, repeated corrections, or clear frustration with execution should default to at least `M`.
3. Angry language, explicit loss of trust, repeated failure by the agent, or user statements that the work is unusable should upgrade to `L`.
4. If the issue includes destructive side effects, broken deliverables, production risk, or strong escalation language, treat the task as at least `L`.

Interpretation rule:
1. Do not rely on literal trigger words alone.
2. Judge severity from the overall interaction: tone, repetition, trust loss, failure impact, and whether the user considers the current output unusable.

### Acceptance Gate

Before `execute`, confirm all three:
1. `done_definition`: what counts as done
2. `validation_method`: how correctness is checked
3. `fail_condition`: what is considered failure

If any is missing, stay in `clarify` or `plan`.

**Understanding Check (M/L level):**
Before gate, add one-sentence reverse confirmation:
- "我理解：要完成[具体目标]，通过[验证方式]确认。对吗？[是/有偏差]"
- If user says "有偏差", return to `clarify`

S-level lightweight gate:
1. For `S` tasks, require only `done_definition` plus minimal validation.
2. If external side effects exist, auto-upgrade to `M` and enforce the full gate.

User-dissatisfaction gate additions:
1. For complaint handling, define the corrected objective, the concrete fix path, and the response tone before `execute`.
2. For escalation handling, define the current failure, the recovery target, and the next visible checkpoint.

**Tool-Call Audit Gate (M/L mandatory, S recommended):**
During `verify`, the agent must answer:
1. How many executive tool calls were made in this task?
2. What is the direct effect of each call?
3. Do these effects 100% cover the `done_definition`?
If the answer to #3 is "no" or "uncertain", return to `execute` to fill the gap. Do not proceed to `close`.

**External Validation (L-level mandatory):**
For `L` tasks, verification must include at least one external anchor:
- Automated tests passing
- User acceptance test
- Code review by another agent or user
- Static analysis tools
Self-check alone is insufficient for `L` tasks.

### Output Contract

Output modes:
1. `compact` (default): concise answer without forced sections.
2. `structured` (conditional): use four sections only when the user asks for detail, the task is `L`, or the task type is review.

Output discipline (all modes):
- Lead with deliverable, not background.
- One-sentence priority: if it can be said in one sentence, do so.
- Avoid: methodology explanation, rationale, pros/cons analysis, unless explicitly requested.

Structured sections:
1. Result
2. Key Findings or Changes
3. Validation
4. Next Action

### Review Rules

If the user asks for review:
1. Output findings first, sorted by severity.
2. Each finding must include impact, location, and recommendation.
3. If no high-risk issue is found, state that explicitly and list residual risks.

### User Interaction Rules

If the user is dissatisfied with the agent's work:
1. Separate facts, mistake scope, correction plan, and next action.
2. Do not argue with the user's emotion or minimize the failure.
3. Use calm, direct language and avoid defensive wording.
4. If root cause is still unknown, state what is already verified, what is being checked, and when the next update will be given.
5. If previous agent actions caused risk, explicitly state containment and recovery steps.

### PUA Layering

1. Tasker owns flow, sizing, gates, and output boundaries.
2. `pua` owns execution intensity and investigation depth.
3. Apply Tasker first, then `pua`.
4. If `pua.instructions.md` or `pua.prompt.md` is unavailable, continue without fallback patches.
5. Never block delivery because PUA is unavailable.
6. Optional PUA project URL: `https://github.com/tanweai/pua`.

### Safety Rules

1. Do not invent files, commands, or test results.
2. Ask only for blocking inputs.
3. Validate outcomes against the same checklist used to plan the task.
4. Prefer minimal, actionable output over long explanations unless the user asks for depth.
5. **Never** simulate or fabricate tool-call output in natural language.
6. **Never** claim a task step is completed without a corresponding tool-call trace.
7. **Never** emit final deliverables during the `plan` phase.

## Minimal Response Template

Result:
- <one-line outcome>

Key Findings or Changes:
- <main point>

Validation:
- <checks passed/failed>
- **Tool-Call Audit**: <list of executive tool calls and their direct artifacts>
- **Coverage Check**: <whether artifacts fully cover done_definition>

Next Action:
- <single recommended next step>

Acceptance Check (always include):
- "交付完成。是否符合预期？[是/需调整]" / "Delivered. Meet expectations? [Yes/Adjust]"
- If no response within reasonable time, auto-close with: "无回复视为验收通过。随时可提出调整。"
