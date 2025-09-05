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

### Step 3: Track with TodoWrite PERSISTENTLY

**IMPORTANT: Use TodoWrite to maintain a persistent list of WIP branches**

When CREATING new branch:
- Add a NEW todo: "WIP: [branch name] - [description]"
- Status: "in_progress"
- This todo stays until the branch is merged or abandoned

When RESUMING existing branch:
- Find the existing todo for this branch if it exists
- If no todo exists, create one: "WIP: [branch name] - resumed work"
- Mark it as "in_progress" (others might be "pending")
- This helps track all active WIP branches

The TodoWrite list becomes your WIP dashboard showing:
- All branches you're working on
- Which one is currently active (in_progress)
- Which are paused (pending)

### Step 4: Show relevant info

Tell user:
- Current branch name
- Whether it was created new or resumed
- "Commit and push: git add -A && git commit -m 'wip: message' && git push"
- "Create PR when ready: gh pr create --fill"

### Step 5: When work is complete

When user is done with a WIP branch, they have options:

**Option A: Convert to PR (most common)**
- Run: `gh pr create --fill`
- This creates a PR from the WIP branch
- Update TodoWrite: Mark the WIP todo as "completed"
- The branch lives on in the PR

**Option B: Merge directly (for tiny fixes)**
- Merge to main locally
- Push main
- Delete the WIP branch
- Update TodoWrite: Mark as "completed"

**Option C: Abandon the work**
- Delete branch locally and on GitHub
- Update TodoWrite: Remove the todo or mark as "completed" with note

The TodoWrite list helps track which WIP branches are still active vs done.