# Copilot Workflow - The Right Way

## ✅ ALWAYS Start From Issues

### The Correct Flow:
```
1. Issue Created (with clear requirements)
     ↓
2. Issue Added to Project Board
     ↓
3. Issue Assigned to Copilot
     ↓
4. Copilot Creates Draft PR
     ↓
5. PR Links Back to Issue
     ↓
6. Project Board Tracks Progress
```

## How to Use Copilot Properly

### Method 1: Direct Assignment (Best)
```bash
# Create issue first
gh issue create --title "Fix login bug" --body "Details..."

# Then assign to Copilot
gh issue edit <number> --add-assignee copilot
```

### Method 2: Assignment via MCP
```javascript
// Use this MCP function
mcp__github__assign_copilot_to_issue({
  issueNumber: 26
})

// NOT this one (creates orphan PRs)
// mcp__github__create_pull_request_with_copilot()
```

### Method 3: Bulk Assignment
```bash
# Label issues for Copilot
gh issue list --label "copilot-ready" --json number -q '.[].number' | \
  xargs -I {} gh issue edit {} --add-assignee copilot
```

## Why This Matters

### When You Assign to Issue:
- ✅ Shows in Project Board
- ✅ Tracked in "In Progress"
- ✅ Visible in sprint planning
- ✅ Clear ownership
- ✅ PR automatically linked

### When You Create PR Directly:
- ❌ Not in Project Board
- ❌ No progress tracking
- ❌ Confusion about ownership
- ❌ Breaks workflow automation
- ❌ Might duplicate work

## Project Board Integration

The Project Board only tracks issues, not PRs directly:
```
Todo → In Progress → In Review → Done
        ↑
   Issues move here
   (PRs are just implementation details)
```

## Current Status Check

### Properly Tracked (via Issue Assignment):
- Issue #26 → PR #42 (Copilot assigned, shows in board)
- Issue #43 → Waiting for Copilot (assigned, shows in board)

### How to Check:
```bash
# See what Copilot is assigned to
gh issue list --assignee copilot

# See what PRs Copilot created
gh pr list --author app/copilot

# Check project board
gh project item-list 1 --owner vanman2024
```

## Golden Rules

1. **NEVER use `create_pull_request_with_copilot`** for existing issues
2. **ALWAYS assign Copilot to issues** not create PRs directly
3. **ALWAYS check issue assignees** before assigning
4. **ALWAYS verify in project board** after assignment

## Monitoring Copilot's Work

```bash
# Watch Copilot's progress
watch -n 60 'echo "=== Copilot Status ===" && \
  gh issue list --assignee copilot --state all && \
  echo && \
  echo "=== Recent PRs ===" && \
  gh pr list --author app/copilot'
```

## If Things Go Wrong

### Orphan PR Created:
1. Check if it fixes an issue
2. Manually link: Edit PR description, add "Fixes #X"
3. Add issue to project board if missing

### Duplicate Work:
1. Check both assignees
2. Close duplicate PR
3. Add `no-overlap` label to issue

### Not Showing in Project:
1. Manually add issue to project
2. Set correct status
3. Verify assignees