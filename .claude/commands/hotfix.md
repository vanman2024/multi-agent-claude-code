---
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), mcp__github(*)
description: Creates and manages hotfix branches for urgent issues
argument-hint: #issue-number | --deploy | --status
---

# Hotfix - Emergency Fix Handler

## Context
- Current branch: !`git branch --show-current`
- Urgent issues: !`gh issue list --label "urgent OR critical OR hotfix" --state open --json number,title`

## Your Task

When user runs `/hotfix $ARGUMENTS`, handle urgent fixes that need to bypass normal process.

### For Creating Hotfix (`/hotfix #123`)

1. **Verify it's urgent**:
```bash
gh issue view $ISSUE_NUMBER --json labels | grep -E "urgent|critical|hotfix|P0"
```

2. **Create hotfix branch**:
```bash
git checkout main
git pull origin main
git checkout -b hotfix-$ISSUE_NUMBER-urgent-fix
```

3. **Fast implementation** - Fix the issue quickly

4. **Create PR with bypass**:
```bash
gh pr create \
  --title "[HOTFIX] Issue Title (#$ISSUE_NUMBER)" \
  --body "🚨 **URGENT FIX**\n\nCloses #$ISSUE_NUMBER\n\n## Critical Issue\n[Description]\n\n## Quick Fix\n[What was done]\n\n- [x] Hotfix applied\n- [x] Bypassing normal checks" \
  --label "hotfix,urgent"
```

### For Deploy (`/hotfix --deploy`)
```bash
# Quick deploy current hotfix
gh pr merge --squash --delete-branch
vercel --prod  # or your deploy command
```

### For Status (`/hotfix --status`)
```bash
# Show all urgent issues and hotfix PRs
gh issue list --label "urgent OR critical OR hotfix"
gh pr list --label "hotfix"
```

## Examples

```bash
# Create hotfix for urgent issue
/hotfix #123

# Deploy current hotfix
/hotfix --deploy  

# Check hotfix status
/hotfix --status
```