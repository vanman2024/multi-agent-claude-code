---
allowed-tools: Bash(*), TodoWrite(*)
description: Start new work-in-progress branch OR resume existing branch
argument-hint: [branch-name] or empty for new branch
---

# WIP - Work In Progress

## Your Task

Either create a new workspace OR resume existing work based on arguments.

### Step 1: Check for uncommitted changes

Run: !`git status --short`

If there are changes, stash them first:
Run: !`git stash push -m "WIP: Stashed before switching branches"`

### Step 2: Determine if NEW or EXISTING branch

Check if user provided a branch name in $ARGUMENTS.

**If $ARGUMENTS contains a branch name:**
- This means they want to RESUME work on an existing branch
- Check if branch exists locally: !`git branch --list $ARGUMENTS`
- If exists locally:
  - Switch to it: !`git checkout $ARGUMENTS`
  - Pull latest from GitHub: !`git pull origin $ARGUMENTS`
  - Say: "Resumed work on branch: $ARGUMENTS"
- If doesn't exist locally but exists on GitHub:
  - Fetch and checkout: !`git checkout -b $ARGUMENTS origin/$ARGUMENTS`
  - Say: "Fetched and resumed branch: $ARGUMENTS from GitHub"
- If doesn't exist anywhere:
  - Create new: !`git checkout -b $ARGUMENTS`
  - Push to GitHub: !`git push -u origin HEAD`
  - Say: "Created new branch: $ARGUMENTS"

**If $ARGUMENTS is empty:**
- This means they want to CREATE a new branch
- ASK THE USER: "What are you working on? (e.g., 'fix commands', 'update docs')"
- Wait for their response
- Convert response to branch name (lowercase, replace spaces with hyphens)
- If no response, use "general-fixes"
- Create branch: git checkout -b [converted name]
- Push to GitHub: !`git push -u origin HEAD`
- Say: "Created new branch: [branch name]"

### Step 3: Track with TodoWrite

Create or update the todo:
- If resuming: "Resume work on: [branch name]"
- If new: "Work on: [branch name/description]"
- Status: "in_progress"

### Step 4: Show relevant info

Tell user:
- Current branch name
- Whether it was created new or resumed
- "Commit and push: git add -A && git commit -m 'wip: message' && git push"
- "Create PR when ready: gh pr create --fill"