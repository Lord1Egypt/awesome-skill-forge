---
name: skill-distiller
description: "Auto-distill successful workflows into reusable skills. Use after completing any multi-step task to evaluate if the workflow should be saved as a skill. Triggers on: 'distill this', 'save as skill', 'make this reusable', or automatically at the end of complex tasks when compound learning is enabled. Evaluates task novelty, success, and reuse potential before generating a standard SKILL.md. Prevents skill bloat through quality gates."
---

# Skill Distiller

Turn successful workflows into reusable skills — automatically.

> Inspired by Hermes Agent's learning loop, but with quality gates to prevent skill bloat.

## When to Distill

Not every task deserves a skill. Evaluate these three criteria:

**All three must be YES to proceed:**

1. **Novel?** — Did this task require a workflow you haven't done before? (If you already have a skill for this, update it instead of creating a new one)
2. **Successful?** — Did the task complete with verified results? (Failed tasks produce lessons, not skills — write to memory/lessons-learned.md instead)
3. **Reusable?** — Will this exact workflow likely be needed again? (One-off tasks don't need skills)

**Quick scoring:**

```
Novel + Successful + Reusable = CREATE SKILL
Novel + Successful + One-off  = WRITE TO MEMORY (lesson learned, not a skill)
Novel + Failed                = WRITE TO LESSONS-LEARNED
Not Novel                     = UPDATE EXISTING SKILL (or skip)
```

## Distillation Process

### Step 1: Extract the Workflow

Look back at what you just did and identify:

- **Trigger**: What kind of request started this? (pattern, not specific instance)
- **Steps**: What were the key steps, in order?
- **Tools**: Which tools were used and how?
- **Decisions**: What non-obvious choices were made and why?
- **Gotchas**: What almost went wrong or required retry?

### Step 2: Generalize

Transform the specific instance into a reusable pattern:

- Replace specific file names with `<input_file>`, `<output_path>` etc.
- Replace specific content with descriptions of what goes there
- Extract magic numbers into named parameters
- Identify which steps are always needed vs. conditional

**Bad** (too specific):
```
1. Read ch10-multi-agent-comm-patterns.md
2. Convert markdown to docx using python-docx
3. Upload to feishu folder nodcnxdXVfsiCVDuiigFVpnCPoc
```

**Good** (generalized):
```
1. Read source markdown file(s)
2. Convert to docx using python-docx (see references/docx-patterns.md)
3. Upload to target feishu folder
```

### Step 3: Write SKILL.md

Generate the skill following the standard format:

```markdown
---
name: <slug>
description: "<when to use this skill — be specific about triggers>"
---

# <Skill Name>

## When to Use
<1-2 sentences on the trigger pattern>

## Workflow
<Numbered steps — the core of the skill>

## Key Decisions
<Non-obvious choices and their rationale>

## Gotchas
<Things that can go wrong and how to handle them>

## References
<Links to detailed docs if needed>
```

**Size target**: SKILL.md body should be **under 200 lines**. If longer, split into SKILL.md (workflow) + references/ (details).

### Step 4: Quality Check

Before saving, verify:

- [ ] Description clearly states when this skill should trigger
- [ ] Steps are ordered and each has a clear action
- [ ] No hardcoded values that should be parameters
- [ ] Gotchas are specific, not generic ("handle errors properly" = useless)
- [ ] Doesn't duplicate an existing skill (check `ls ~/.openclaw/skills/`)

### Step 5: Save and Register

Save to `~/.openclaw/skills/<slug>/SKILL.md`.

If the skill has reference materials, save them to `~/.openclaw/skills/<slug>/references/`.

After saving, verify the skill loads:
```bash
ls ~/.openclaw/skills/<slug>/SKILL.md
```

## Automatic Distillation Mode

When integrated with trinity-harness's Layer 3 (Compound), distillation happens automatically:

1. Task completes → Layer 3 Compound phase triggers
2. Evaluate Novel + Successful + Reusable
3. If all YES → run distillation process
4. If NO → write lesson to memory instead
5. Announce to user: "Distilled skill: <name>. Review with `read ~/.openclaw/skills/<slug>/SKILL.md`"

**Never auto-distill silently.** Always announce what was created so the user can review, edit, or delete.

## Skill Maintenance

### Update vs. Create

Before creating a new skill, check if a related one exists:
```bash
ls ~/.openclaw/skills/ | grep -i <keyword>
```

If a similar skill exists, **update it** (add the new pattern as a variant) rather than creating a near-duplicate.

### Pruning

Periodically (during Dream Task), review skills:
- Skills unused for 30+ days → candidate for archival
- Skills with overlapping triggers → merge
- Skills that have been superseded → mark deprecated

## Anti-Patterns

| Don't | Why | Do Instead |
|---|---|---|
| Distill every task | Skill bloat, noise drowns signal | Apply the 3-question gate |
| Include conversation history | Wastes tokens, not reusable | Extract only the workflow pattern |
| Write vague gotchas | "Be careful" helps no one | Specific: "API X returns 429 after 3 concurrent requests" |
| Hardcode paths/names | Not portable | Use `<parameter>` placeholders |
| Skip quality check | Garbage skills waste future context | Always verify before saving |

## Integration with Memory System

Distillation complements, not replaces, the memory system:

| Output | Goes to | When |
|---|---|---|
| Reusable workflow | `~/.openclaw/skills/<slug>/SKILL.md` | Novel + Successful + Reusable |
| Lesson learned | `memory/lessons-learned.md` | Successful but one-off, or failed |
| Quick note | `memory/YYYY-MM-DD.md` | Routine observations |
| Core insight | `MEMORY.md` | Fundamental principle change |
