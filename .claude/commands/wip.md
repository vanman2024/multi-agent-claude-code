---
allowed-tools: Bash(*), TodoWrite(*)
description: Start work-in-progress branch for iterative development without issues
argument-hint: [branch-name]
---

# WIP - Work In Progress

## Your Task

Create a simple workspace for iterative work.

### Step 1: Check for uncommitted changes

Run: !`git status --short`

If there are changes, stash them:
Run: !`git stash push -m "WIP: Stashed before creating new branch"`

### Step 2: Determine branch name and create it

**If user provided arguments ($ARGUMENTS):**
1. Use $ARGUMENTS as the branch name
2. Create it with: !`git checkout -b $ARGUMENTS`

**If no arguments provided:**
1. Ask: "What are you working on? (e.g., 'fix commands', 'update docs', or just press Enter for 'general-fixes')"
2. Get their response
3. If they gave a description, convert it to a branch name (lowercase, hyphens)
4. If they gave nothing, use "general-fixes"
5. Create the branch with git checkout -b and the chosen name

### Step 3: Add to TodoWrite

Create a simple todo to track the work:
- Content: "Work on: [branch name or description]"
- Status: "in_progress"
- ActiveForm: "Working on: [branch name or description]"

### Step 4: Inform user

Tell them:
- "Created branch: [branch name]"
- "This is for iterative work - no issue created"
- "Commit with: git add -A && git commit -m 'wip: your message'"
- "Create PR when ready: gh pr create --fill"