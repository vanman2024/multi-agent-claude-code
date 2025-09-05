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

### Step 2: Check for worktrees

Check if branch is in a worktree: !`git worktree list --porcelain | grep "branch refs/heads/$ARGUMENTS" | head -1`

If the branch exists in a worktree:
- Get the worktree path from the output
- Tell user: "⚠️ Branch '$ARGUMENTS' is already checked out in worktree at: [path]"
- Provide options:
  1. Navigate to that worktree: `cd [worktree path]`
  2. Work on a different branch: `/wip [different-name]`
- STOP HERE - don't try to checkout

### Step 3: Handle based on arguments

**If $ARGUMENTS is empty (user just typed /wip):**
1. ASK THE USER: "What are you working on? (e.g., 'fix commands', 'update docs')"
2. Wait for their response
3. Convert response to branch name (lowercase, replace spaces with hyphens)
4. If no response, use "general-fixes" as branch name
5. Check if this branch is in a worktree first (see Step 2)
6. ASK: "Do you want to create this as a worktree? (y/n)"
   - Explain: "Worktrees let you work on multiple branches simultaneously in different directories"
7. If YES to worktree:
   - Create worktree: `git worktree add ../worktrees/[branch-name] -b [branch-name]`
   - Tell user: "📁 Created worktree at: ../worktrees/[branch-name]"
   - Tell user: "Navigate there with: cd ../worktrees/[branch-name]"
8. If NO to worktree:
   - Create the new branch with git checkout -b [branch-name]
9. Push to GitHub with git push -u origin HEAD
10. Add to TodoWrite: "WIP: [branch-name] - [description] [worktree]" (mark if worktree)

**If $ARGUMENTS has a value (user typed /wip branch-name):**
1. Check for worktree first (see Step 2)
2. First try to checkout existing branch with: git checkout $ARGUMENTS
3. If that succeeds:
   - Pull latest: git pull origin $ARGUMENTS
   - Say: "Resumed work on branch: $ARGUMENTS"
4. If checkout fails (branch doesn't exist):
   - ASK: "Branch '$ARGUMENTS' doesn't exist. Create as worktree? (y/n)"
   - If YES to worktree:
     - Create worktree: `git worktree add ../worktrees/$ARGUMENTS -b $ARGUMENTS`
     - Tell user: "📁 Created worktree at: ../worktrees/$ARGUMENTS"
     - Tell user: "Navigate there with: cd ../worktrees/$ARGUMENTS"
   - If NO to worktree:
     - Create new branch: git checkout -b $ARGUMENTS
   - Push to GitHub: git push -u origin HEAD
   - Say: "Created new branch: $ARGUMENTS"
5. Update TodoWrite to mark this branch as "in_progress"

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
