---
allowed-tools: mcp__github(*), Bash(*), Read(*)
description: Review and merge Copilot-created PRs quickly
argument-hint: [pr-number]
---

# Copilot Merge

## Context
- Current branch: !`git branch --show-current`
- Recent PRs: !`gh pr list --limit 5`

## Your Task

When user runs `/copilot-merge $ARGUMENTS`, help them review and merge a Copilot PR:

### Step 1: Pull Latest Changes
Execute: !`git pull`

### Step 2: Get PR Details
Use mcp__github__get_pull_request with:
- owner: vanman2024
- repo: multi-agent-claude-code
- pullNumber: $ARGUMENTS

Show the user:
- PR title and description
- Files changed count
- Check status (passing/failing)
- Is it ready to merge?

### Step 3: Review Changes
Use mcp__github__get_pull_request_diff with:
- owner: vanman2024
- repo: multi-agent-claude-code
- pullNumber: $ARGUMENTS

Show a summary of:
- Key changes made
- Any potential issues spotted
- Whether it looks safe to merge

### Step 4: Check PR Status
Use mcp__github__get_pull_request_status with:
- owner: vanman2024
- repo: multi-agent-claude-code
- pullNumber: $ARGUMENTS

Verify:
- All checks passing
- No merge conflicts
- Ready for merge

### Step 5: Ask User to Confirm
Based on the review, ask:
"PR #$ARGUMENTS looks [good/has issues]. Merge now? (yes/no)"

### Step 6: Merge If Approved
If user says yes, use mcp__github__merge_pull_request with:
- owner: vanman2024
- repo: multi-agent-claude-code
- pullNumber: $ARGUMENTS
- merge_method: squash

### Step 7: Pull Merged Changes
After merge: !`git pull`

### Step 8: Verify Fix
If it was a bug fix (like #143 for /work command):
- Suggest testing the fixed command
- Example: "Try running `/work 142` to verify the fix works"

## Quick Mode
If user adds "quick" or "fast" to arguments, skip detailed review and just:
1. Check status
2. Auto-merge if all checks pass
3. Pull changes

## Notes
- Designed for Copilot PRs which are typically simple and safe
- For complex PRs, suggest using `/copilot-review` for detailed analysis
- Always pull before and after merge to stay in sync