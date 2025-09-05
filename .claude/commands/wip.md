---
allowed-tools: Bash(*), TodoWrite(*)
description: Start new work-in-progress branch OR resume existing branch
argument-hint: [branch-name] or empty for new branch
---

# WIP - Work In Progress

## Your Task

Either create a new workspace OR resume existing work based on arguments.

### Step 1: Check for uncommitted changes

First check: !`git status --short`

If there are changes shown, stash them:
Run: !`git stash push -m "WIP: Stashed before switching branches"`

### Step 2: Handle based on arguments

**If $ARGUMENTS is empty (user just typed /wip):**
1. ASK THE USER: "What are you working on? (e.g., 'fix commands', 'update docs')"
2. Wait for their response
3. Convert response to branch name (lowercase, replace spaces with hyphens)
4. If no response, use "general-fixes" as branch name
5. Create the new branch with git checkout -b [branch-name]
6. Push to GitHub with git push -u origin HEAD
7. Add to TodoWrite: "WIP: [branch-name] - [description]"

**If $ARGUMENTS has a value (user typed /wip branch-name):**
1. First try to checkout existing branch with: git checkout $ARGUMENTS
2. If that succeeds:
   - Pull latest: git pull origin $ARGUMENTS
   - Say: "Resumed work on branch: $ARGUMENTS"
3. If checkout fails (branch doesn't exist):
   - Create new branch: git checkout -b $ARGUMENTS
   - Push to GitHub: git push -u origin HEAD
   - Say: "Created new branch: $ARGUMENTS"
4. Update TodoWrite to mark this branch as "in_progress"

### Step 3: Show status

Tell user:
- Current branch name
- Whether it was created or resumed
- "Commit: git add -A && git commit -m 'wip: message' && git push"
- "Create PR when ready: gh pr create --fill"