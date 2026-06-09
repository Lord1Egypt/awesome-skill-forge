# GitHub Contribution Skill

## Purpose
Automated GitHub contribution workflow that handles fork synchronization, branch creation, and PR submission while maintaining clean fork state.

## Core Features

### 1. Fork Protection & Synchronization
- **Main Branch Protection**: Never commit directly to main branch
- **Automatic Sync**: Regularly sync fork main with upstream official repository  
- **Clean State Enforcement**: Ensure fork main branch matches official repository exactly
- **Pollution Prevention**: Prevent local work files from contaminating main branch

### 2. Automated Contribution Workflow
- **Fork Setup**: Automatically configure upstream remote if not exists
- **Branch Creation**: Create feature branches based on latest official code
- **PR Submission**: Handle pull request creation with proper templates
- **Issue Integration**: Link fixes to relevant GitHub issues

### 3. Safety Measures
- **Pre-flight Validation**: Verify fork cleanliness before starting
- **Atomic Operations**: All changes happen in isolated feature branches
- **Rollback Support**: Easy recovery if something goes wrong
- **Permission Handling**: Work within GitHub token permission constraints

## Usage

### Basic Command
```bash
./github-contribution.sh <username> <owner/repo> <issue-number> <branch-name> [projects-root]
```

### Examples
```bash
# Fix issue #123 in openclaw/openclaw
./github-contribution.sh Linux2010 openclaw/openclaw 123 fix/issue-description

# Specify custom project root
./github-contribution.sh Linux2010 openclaw/openclaw 456 fix/bug-fix /custom/path
```

## Fork Protection Best Practices

### Main Branch Rules
1. **Never commit directly** to fork's main branch
2. **Always sync first** before creating new branches
3. **Use feature branches** for all development work
4. **Regular cleanup** of local pollution files

### Safe Synchronization Script
```bash
#!/bin/bash
# sync-fork.sh - Safe fork synchronization

git checkout main
git fetch upstream
git reset --hard upstream/main
git clean -fdx  # Remove all untracked files

# Verify clean state
if [[ $(git status --porcelain) ]]; then
    echo "❌ Warning: Working tree not clean"
    exit 1
fi
echo "✅ Fork synchronized successfully"
```

### Local Git Configuration
```bash
# Prevent accidental main branch pushes
git config branch.main.pushRemote no_push

# Set safe push default
git config push.default nothing
```

## Workflow Steps

### Step 1: Fork Validation
- Check if fork exists and is accessible
- Verify upstream remote configuration
- Validate current fork state cleanliness

### Step 2: Synchronization  
- Fetch latest from upstream official repository
- Reset local main branch to match upstream exactly
- Clean any untracked/local pollution files
- Push synchronized state to fork (if permissions allow)

### Step 3: Feature Branch Creation
- Create new branch from clean main
- Apply necessary changes and fixes
- Commit with proper semantic format
- Push feature branch to fork

### Step 4: PR Creation
- Generate PR with complete template
- Link to relevant issue numbers
- Include proper change type and scope
- Add security impact assessment

---

## 🩺 Bug Fix Module: Change Plan

Before fixing any bug, **always write a change plan first**. This ensures minimal, safe changes and makes PR review easier.

### The 5-Point Analysis

Answer these 5 questions in plain language before writing any code:

| # | Question | Purpose |
|---|----------|---------|
| 1 | **Observed behavior** | What's broken? (What the user sees) |
| 2 | **Expected behavior** | What should happen? (Correct behavior) |
| 3 | **Suspected root cause** | Where's the bug? (Specific code location) |
| 4 | **Safest seam to modify** | Minimal change location? (Narrowest fix) |
| 5 | **Risk surface** | What else could break? (Impact scope) |

### Change Plan Template

```markdown
## Change Plan for Issue #<number>

1. **Observed behavior**:
   <Describe what's broken - the user-visible symptom>

2. **Expected behavior**:
   <Describe what should happen instead>

3. **Suspected root cause**:
   <Point to specific file/line/function that causes the bug>

4. **Safest seam to modify**:
   <Identify the minimal code change location - smallest safe fix>

5. **Risk surface**:
   <List what could be affected by this change>
```

### Example: Issue #5968

```markdown
## Change Plan for Issue #5968

1. **Observed behavior**:
   `extract_content_or_reasoning()` crashes when `response.choices` is None, missing, or empty list.

2. **Expected behavior**:
   Function should return empty string gracefully when no usable choices exist.

3. **Suspected root cause**:
   Line `msg = response.choices[0].message` in `agent/auxiliary_client.py` assumes choices is always non-empty.

4. **Safest seam to modify**:
   Add a guard at the top of `extract_content_or_reasoning()` before accessing choices:
   `if not getattr(response, "choices", None): return ""`

5. **Risk surface**:
   Minimal - only affects edge cases where API response is malformed.
```

### When to Use Change Plan

| Scenario | Required? |
|----------|-----------|
| Bug fix | ✅ Always |
| Paper-cut UX improvement | ✅ Always |
| Feature addition | ❌ Use feature spec instead |
| Refactoring | ❌ Use refactor plan instead |
| Documentation fix | ❌ Not needed |

### Benefits of Change Plan

| Benefit | Why It Matters |
|---------|----------------|
| **Forces understanding** | Can't fix what you don't understand |
| **Defines boundaries** | Prevents scope creep and "opportunistic" changes |
| **Reduces risk** | Identifies potential side effects upfront |
| **Speeds review** | Maintainer can understand intent in 20 seconds |
| **Enables rollback** | Clear what was changed and why |

### Change Plan Checklist

Before coding:
- [ ] Can you describe the bug in one sentence?
- [ ] Can you point to the exact line causing it?
- [ ] Is your fix the smallest possible change?
- [ ] Have you identified what else could break?
- [ ] Will this change need a regression test?

If you answered "no" to any question, **do more investigation before coding**.

---

## Error Handling

### Common Issues & Solutions

#### Fork Not Clean
- **Problem**: Local main branch has extra commits/files
- **Solution**: Force reset to upstream and clean untracked files

#### Permission Denied (Workflow Scope)
- **Problem**: Token lacks workflow permissions
- **Solution**: Use web-based PR creation or update token permissions

#### Upstream Not Configured  
- **Problem**: Missing upstream remote
- **Solution**: Auto-add upstream remote pointing to official repository

#### Branch Already Exists
- **Problem**: Feature branch already exists
- **Solution**: Use unique branch naming or delete existing branch

## Security Considerations

### Token Permissions
- **Minimum Required**: `repo` scope
- **Optional**: `workflow` scope (for full automation)
- **Never Grant**: Excessive permissions beyond contribution needs

### Local Security
- **File Cleanup**: Always clean working directory after contributions
- **Credential Management**: Use secure credential storage
- **Audit Trail**: Maintain logs of all contribution activities

## Integration with Other Skills

### PR Advocacy Skill
- Hand off created PRs to PR Advocacy for monitoring
- Share PR tracking information for continuous follow-up
- Coordinate review response and maintenance

### Document Spell Check Skill  
- Pre-validate documentation changes before PR creation
- Ensure all text content passes spell checking
- Maintain documentation quality standards

## High-Quality PR Best Practices (Maximize Merge Success Rate)

### 🎯 Merge Success Rate Formula (Based on 30+ Merged PRs Analysis)

```
Merge Success Rate = 
  (PR Description Completeness × 0.2) +
  (Review Response Speed × 0.25) +
  (Test Coverage × 0.2) +
  (Conflict Resolution Status × 0.15) +
  (Review Resolution Rate × 0.2)
```

**Target**: > 80% success rate

### ✅ 10 Success Characteristics (Must Follow 100%)

1. ✅ **Complete PR Description** - Use template, fill ALL required fields
2. ✅ **Fast Review Response** - < 30 minutes average response time
3. ✅ **Small Focused Commits** - 1 commit solves 1 problem
4. ✅ **100% Test Coverage** - Include edge cases and regression tests
5. ✅ **Zero Conflicts** - Daily rebase upstream, keep CLEAN
6. ✅ **Changelog Updated** - All user-visible changes
7. ✅ **Security Checklist** - 5 required security questions
8. ✅ **Human Verification Statement** - Manual test content + untested areas
9. ✅ **Review Conversations Resolved** - 100% resolve bot review comments
10. ✅ **Rollback Plan** - Rollback steps + known issues

### 📋 Pre-Submission Checklist

Before pushing PR:

**Code Quality:**
- [ ] Title format: `type(scope): description`
- [ ] Commit message: includes "what" + "why"
- [ ] At least 1 new test case
- [ ] CHANGELOG.md updated
- [ ] 4-7 meaningful commits

**CI Pre-flight (MUST pass locally):**
- [ ] `pnpm protocol:check` - Protocol validation
- [ ] `pnpm test` - All tests pass
- [ ] `pnpm lint` - No lint errors
- [ ] `pnpm tsc --noEmit` - TypeScript compilation

**Review Readiness:**
- [ ] Ready to respond within 24h
- [ ] Greptile/Aisle Security comments addressed
- [ ] Security questions answered (5 required)

### 📊 High Success Rate PR Patterns

#### Pattern 1: Security Fix Response (vincentkoc #44437)
```
7 commits in same day:
1. Main fix implementation
2. Changelog update
3. Merge main (resolve conflicts)
4. Tests: add coverage for review comments
5. Fix: address Greptile suggestions
6. Extra hardening (defensive programming)
7. Merge main (final sync)
```

**Key Learnings:**
- ✅ Separate commits for review responses
- ✅ Tests and docs as separate commits
- ✅ Frequent merge main to resolve conflicts
- ✅ Extra hardening shows professionalism

#### Pattern 2: Security Report Response (gumadeiras #44176)
```markdown
When Aisle Security reports issues:

1. Quote SECURITY.md to explain why it's out of scope
2. But still fix it (defensive programming)
3. List specific hardening done
4. Provide verification commands
```

**Key Learnings:**
- ✅ Respond to security reports first
- ✅ Explain scope判断 basis
- ✅ Still fix it (show cooperation)
- ✅ Provide verification method

### ⚠️ Common Mistakes That Reduce Merge Rate

| Mistake | Impact | Solution |
|---------|--------|----------|
| ❌ Missing Changelog | -20% | Always update CHANGELOG.md |
| ❌ Slow review response (>24h) | -25% | Respond within 24h, ideally <30min |
| ❌ Incomplete test coverage | -20% | Add tests for edge cases |
| ❌ Merge conflicts | -15% | Daily rebase upstream |
| ❌ Unresolved bot reviews | -20% | 100% resolve all comments |
| ❌ CI failures | Automatic reject | Pre-flight check locally |

### 🎯 Quality Metrics

| Metric | Target | Current Best Practice |
|--------|--------|----------------------|
| **Greptile Score** | ≥ 4/5 | Address all P1/P2 issues |
| **Aisle Security** | 0 unresolved | Respond or fix all |
| **Test Coverage** | ≥ 1 new test | Include edge cases |
| **CI Pass Rate** | 100% | Pre-check locally |
| **Behind upstream** | 0 commits | Daily rebase |
| **Response Time** | < 24h | Same day preferred |

### 📝 PR Template Best Practices

**Title Format:**
```
✅ fix(hooks): fail closed on unreadable loader paths
✅ feat(context-engine): plumb sessionKey into all methods
✅ docs: codify American English spelling convention
✅ security: include accountId in session keys
```

**Commit Message Structure:**
```
First line: What was done (concise description)

Second paragraph: Why (problem background, impact)

Optional: Regeneration-Prompt / AI assistance notes
```

**Example (#44411):**
```
fix(ci): restore generated protocol swift outputs

Regenerate the Swift protocol models so PushTestResult keeps the 
transport field required by the current gateway schema, and update 
protocol:check to diff both generated Swift destinations because 
the generator writes both files.

Regeneration-Prompt: |
  Investigate the protocol CI failure on current origin/main...
```

---

## Best Practices

### For Contributors
- Always start from clean, synchronized main branch
- Use descriptive branch names following convention
- Fill complete PR templates with all required fields
- Test changes locally before pushing
- **Always rebase on the original PR branch** (never create new branches for rebase)
- **Follow High-Quality PR Best Practices** (see section above)

### PR Rebase Best Practices (Critical!)

**Golden Rule**: Always rebase on the **original PR branch**, never create a new branch.

#### Correct Rebase Workflow

```bash
# 1. Confirm current branch
git branch --show-current

# 2. Confirm PR's branch name
gh pr view <PR-number> --json headRefName --jq .headRefName

# 3. Switch to correct branch if needed
git checkout <PR-branch-name>

# 4. Rebase on the SAME branch (do NOT create new branch)
git fetch upstream
git rebase upstream/main

# 5. Push to the SAME branch
git push -f origin <same-branch-name>
```

#### Common Mistakes to Avoid

| ❌ Wrong | ✅ Correct |
|---------|---------|
| `git checkout -b new-branch` then rebase | Stay on original branch, rebase there |
| Switch to different branch for rebase | Rebase on PR's own branch |
| Skip branch confirmation | Always run `git branch --show-current` first |
| Don't verify PR branch name | Use `gh pr view` to confirm |

#### Why This Matters?

1. **Clean branch history** - No duplicate branches created
2. **Avoid confusion** - PR always linked to same branch
3. **Reduce errors** - Won't push to wrong branch
4. **Easy management** - All changes in one place

#### Pre-Rebase Checklist

Before rebasing:
- [ ] Run `git branch --show-current` to confirm current branch
- [ ] Run `gh pr view <num> --json headRefName` to confirm PR branch
- [ ] Ensure both names match before proceeding
- [ ] If mismatch, `git checkout <PR-branch>` first

#### Post-Rebase Checklist

After rebasing:
- [ ] Run `git log --oneline -3` to verify commits
- [ ] Run `pnpm test` or relevant tests
- [ ] Run `git push -f origin <branch>` to update PR

#### Example: Rebase PR #48568

```bash
# Check current branch
$ git branch --show-current
fix/47752-final  # ✅ Correct!

# Confirm PR branch
$ gh pr view 48568 --json headRefName --jq .headRefName
fix/47752-final  # ✅ Matches!

# Rebase on same branch
git fetch upstream
git rebase upstream/main

# Test
pnpm test src/infra/heartbeat-runner.timeout.test.ts

# Push to same branch
git push -f origin fix/47752-final
```

#### Troubleshooting

**Problem**: Accidentally created new branch during rebase

**Solution**:
```bash
# Go back to original branch
git checkout <original-branch>

# Rebase there instead
git rebase upstream/main

# Delete the accidental branch
git branch -D <accidental-branch>

# Push to original branch
git push -f origin <original-branch>
```

---

### For Maintainers  
- Regularly audit fork cleanliness
- Update synchronization scripts as needed
- Monitor token permissions and security
- Document contribution workflows for team members

## Limitations

### GitHub Fork Restrictions
- Cannot set full branch protection rules on forks
- Limited automation capabilities without workflow permissions
- Manual intervention sometimes required for complex scenarios

### Workarounds
- Use local git hooks for additional protection
- Implement manual verification steps in workflow
- Leverage GitHub web interface for final PR creation when needed

## Maintenance

### Updates
- Regular script updates for new GitHub API changes
- Security patches for authentication methods
- Performance improvements for large repositories

### Monitoring
- Track success/failure rates of contribution attempts
- Monitor GitHub API rate limit usage
- Collect user feedback for workflow improvements