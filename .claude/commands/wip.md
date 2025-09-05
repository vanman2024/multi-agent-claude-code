---
allowed-tools: Bash(*), TodoWrite(*)
description: Start work-in-progress branch for iterative development without issues
argument-hint: [branch-name] or empty for prompted branch
---

# WIP - Work In Progress

## Your Task

When user runs `/wip $ARGUMENTS`, create a simple workspace for iterative work.

### Step 1: Check current state

First check if there are uncommitted changes:
Run: !`git status --short`

If there are uncommitted changes, stash them:
Run: !`git stash push -m "WIP: Stashed before creating new branch"`

### Step 2: Create the branch

Check if user provided a branch name in $ARGUMENTS:

**If $ARGUMENTS is provided:**
- Use it as the branch name
- Create branch: !`git checkout -b $ARGUMENTS`

**If $ARGUMENTS is empty:**
- Ask user: "What are you working on? (e.g., 'fix commands', 'update docs')"
- Wait for their response
- Convert their response to a branch name (lowercase, hyphens for spaces)
- If they give no response, use branch name "general-fixes"
- Create the branch with the determined name using git checkout -b

### Step 3: Track the work

Use TodoWrite to create a simple todo:
- If working on something specific, todo content: "Work on: [their description]"
- If general fixes, todo content: "Work on: general improvements"
- Set status: in_progress

### Step 4: Show next steps

Tell the user:
- "You're now on branch: [branch name]"
- "This is for iterative work - no issue needed"
- "To commit: git add -A && git commit -m 'wip: description'"
- "When ready for PR: gh pr create --fill"