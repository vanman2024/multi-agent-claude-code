---
allowed-tools: Bash(*), TodoWrite(*)
description: Start work-in-progress branch for iterative development without issues
argument-hint: [branch-name] or empty for prompted branch
---

# WIP - Work In Progress

## Your Task

When user runs `/wip $ARGUMENTS`, create a simple workspace for iterative work.

### Step 1: Check current state

Run: !`git status --short`

If there are uncommitted changes, stash them:
Run: !`git stash push -m "WIP: Stashed before creating new branch"`

### Step 2: Determine branch name

If arguments provided, use as branch name: `$ARGUMENTS`

If no arguments:
- Ask: "What are you working on? (brief description like 'fix commands' or 'update docs')"
- Convert the response to a branch name (lowercase, replace spaces with hyphens)
- If no response, use "general-fixes"

### Step 3: Create the branch

Run: !`git checkout -b [BRANCH_NAME]`

### Step 4: Set up simple tracking

Use TodoWrite to create one simple todo:
- Content: "Work on: [description]"
- Status: in_progress

### Step 5: Show next steps

Tell the user:
- You're now on branch: [BRANCH_NAME]
- No issue was created (this is for iterative work)
- Commit with: `git add -A && git commit -m "wip: description"`
- When ready, create PR with: `gh pr create --fill`