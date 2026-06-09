# awesome-skill-forge — Project Plan
> Written: 2026-06-09 | Status: Planning

---

## Concept

A GitHub repository serving as a **Hermes-compatible skills registry** with:
- 170 official Hermes Agent skills (75 Built-in + 95 Optional)
- Lord1Egypt custom skills (ThothTerm, AI Mate, RPC Radar, ethsmith, PokeGypt, etc.)
- A sync tool to pull from the 90,896-skill community API
- Full compatibility with agentskills.io registry format

**This is different from `skillforge-agent`** (which is a lazy-loading Python/JS package with 539 skills in a custom format).  
This repo uses the **Hermes SKILL.md standard** natively.

---

## Repository Name

**`Lord1Egypt/awesome-skill-forge`**

### Why This Name
- Follows existing brand pattern: `awesome-prompt-forge` + `skillforge-agent`
- "awesome" = curated collection (community-standard prefix)
- "skill-forge" = our brand identity for skill creation/packaging
- Distinct from `ai-skillforge` (the private build folder for skillforge-agent)

---

## Hermes SKILL.md Format

Each skill follows this standard:

```markdown
---
name: skill-name
description: One-line description of what this skill does.
overview: |
  Detailed explanation of the skill's capabilities and use cases.
category: AI Agents | Productivity | Software Dev | Security | ...
source: lord1egypt | hermes | clawHub | skills.sh | ...
tags: [tag1, tag2, tag3]
platforms: [linux, macos, windows]
author: Lord1Egypt
version: "1.0.0"
installCmd: hermes install skill-name
sourceUrl: https://github.com/Lord1Egypt/awesome-skill-forge/tree/main/lord1egypt-skills/skill-name
---

# Skill Title

Full skill content / system prompt here...
```

---

## Repository Structure

```
awesome-skill-forge/
├── README.md                        # Showcase + install instructions + shields
├── REGISTRY.md                      # Skills index table (all skills listed)
├── registry.json                    # agentskills.io compatible manifest
│
├── skills/                          # 75 Built-in skills (from hermes-agent)
│   ├── claude-code/
│   │   └── SKILL.md
│   ├── github-pr-workflow/
│   │   └── SKILL.md
│   └── ...  (75 total)
│
├── optional-skills/                 # 95 Optional skills (from hermes-agent)
│   ├── ...  (95 total)
│
├── lord1egypt-skills/               # Custom Lord1Egypt skills
│   ├── thothterm/
│   │   └── SKILL.md
│   ├── ai-mate/
│   │   └── SKILL.md
│   ├── rpc-radar/
│   │   └── SKILL.md
│   ├── ethsmith/
│   │   └── SKILL.md
│   ├── pokegypt/
│   │   └── SKILL.md
│   ├── skillforge/
│   │   └── SKILL.md
│   └── awesome-prompt-forge/
│       └── SKILL.md
│
├── tools/
│   ├── sync.py                      # Sync new skills from API JSON (90k+)
│   ├── fetch_skill.py               # Fetch individual skill by sourceUrl
│   ├── validate.py                  # Validate SKILL.md frontmatter format
│   └── build_registry.py           # Generate registry.json from all SKILL.md files
│
└── .github/
    └── workflows/
        ├── sync.yml                 # Auto-sync from API twice daily
        └── validate.yml             # Validate SKILL.md on every PR
```

---

## API Endpoints (Data Sources)

```
# Full 90k skills index (~10MB)
GET https://hermes-agent.nousresearch.com/docs/api/skills.json

# Metadata only (faster)
GET https://hermes-agent.nousresearch.com/docs/api/skills-meta.json
```

Each skill entry in the JSON contains:
`name, description, overview, category, source, tags, platforms, author, version, installCmd, sourceUrl`

### Source Repos for Built-in/Optional Skills
- `github.com/NousResearch/hermes-agent/tree/main/skills/` — 75 built-in
- `github.com/NousResearch/hermes-agent/tree/main/optional-skills/` — 95 optional

---

## Phase Plan

### Phase 1 — Foundation (Day 1)
- [ ] Initialize GitHub repo: `Lord1Egypt/awesome-skill-forge`
- [ ] Copy 75 built-in skills from `NousResearch/hermes-agent/skills/`
- [ ] Copy 95 optional skills from `NousResearch/hermes-agent/optional-skills/`
- [ ] Write README.md with shields (skill count, registries, license)
- [ ] Write REGISTRY.md skills index table

### Phase 2 — Custom Lord1Egypt Skills (Day 1-2)
- [ ] `lord1egypt-skills/thothterm/SKILL.md` — GPU terminal emulator (Rust+wgpu+WASM)
- [ ] `lord1egypt-skills/ai-mate/SKILL.md` — AI chat assistant
- [ ] `lord1egypt-skills/rpc-radar/SKILL.md` — Ethereum/Web3 RPC node monitor
- [ ] `lord1egypt-skills/ethsmith/SKILL.md` — Solidity/Foundry dev environment
- [ ] `lord1egypt-skills/pokegypt/SKILL.md` — Pokemon TFS server management
- [ ] `lord1egypt-skills/skillforge/SKILL.md` — Install/manage skills via skillforge-agent
- [ ] `lord1egypt-skills/awesome-prompt-forge/SKILL.md` — Browse/load AI system prompts

### Phase 3 — Sync Tool (Day 2-3)
- [ ] `tools/sync.py`:
  - Fetch `skills-meta.json` from API
  - Diff against local SKILL.md files
  - Pull new/updated skills via `sourceUrl`
  - Write `sync_report.md` (new, updated, removed)
- [ ] `tools/fetch_skill.py`:
  - Given a sourceUrl, create a local SKILL.md
  - Auto-detect format (SKILL.md, JSON, text)
- [ ] `tools/build_registry.py`:
  - Scan all `*/SKILL.md` files
  - Generate `registry.json` for agentskills.io
- [ ] GitHub Actions `sync.yml`:
  - Runs twice daily (matches Hermes API refresh cadence)
  - Auto-commits new skills to `synced-skills/` folder

### Phase 4 — Registry Compatibility (Day 3-4)
- [ ] Generate `registry.json` manifest
- [ ] Submit `Lord1Egypt/awesome-skill-forge` to agentskills.io
- [ ] Add install badge + link to `skillforge-agent` README
- [ ] Add terminal demo GIF to README (VHS preferred, per standard)

---

## Stats Target

| Source | Count |
|--------|-------|
| Built-in (Hermes official) | 75 |
| Optional (Hermes official) | 95 |
| Lord1Egypt Custom | ~10 |
| **Total at launch** | **~180** |
| Community (via sync tool, opt-in) | up to 90k+ |

---

## Relation to Existing Projects

| Project | Role | Format |
|---------|------|--------|
| `skillforge-agent` (PyPI/npm) | Lazy-loading skill RUNNER | Custom SKILL.md (simple) |
| `awesome-prompt-forge` (PyPI/npm) | System prompts COLLECTION | Markdown prompts |
| `awesome-skill-forge` (this repo) | Hermes-compatible skill REGISTRY | Hermes SKILL.md standard |

The three repos are complementary, not redundant:
- Use `skillforge-agent` to load skills into Python/JS apps
- Use `awesome-prompt-forge` to browse/load AI system prompts
- Use `awesome-skill-forge` to discover/install Hermes-format agent skills

---

## Notes

- Keep the repo focused on **quality curation**, not raw mirroring of 90k skills
- The sync tool is for DISCOVERY and import — not for committing all 90k into git
- Each `lord1egypt-skills/` entry gets a demo GIF in its folder (per terminal demo standard)
- Prioritize skills that complement ThothTerm's AI-native + Web3-native identity
- Consider adding a `skill-sets/` folder: curated bundles (e.g., "web3-bundle", "ai-agent-bundle")

---

*Plan ready — awaiting build session*
