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

If there are changes, stash them first:
Run: !`git stash push -m "WIP: Stashed before creating new branch"`

### Step 2: Get branch name

First, check if user provided a branch name in $ARGUMENTS.

If $ARGUMENTS is empty, ASK THE USER:
"What are you working on? (e.g., 'fix commands', 'update docs')"

Wait for their response, then:
- If they provide text, convert it to a branch name (lowercase, replace spaces with hyphens)
- If they just press Enter, use "general-fixes" as the branch name

### Step 3: Create the branch

Now that you have a branch name (either from $ARGUMENTS or from asking the user):
- Create the branch using: git checkout -b [the branch name you determined]

### Step 4: Track with TodoWrite

Create a simple todo:
- Content: "Work on: [branch name]"
- Status: "in_progress"
- ActiveForm: "Working on: [branch name]"

### Step 5: Tell user what happened

Say:
- "Created branch: [branch name]"
- "This is for iterative work - no issue created"
- "Commit with: git add -A && git commit -m 'wip: your message'"
- "Create PR when ready: gh pr create --fill"