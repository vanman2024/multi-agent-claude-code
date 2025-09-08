---
allowed-tools: Bash(*), TodoWrite(*), mcp__github(*)
description: Continue/resume work from branches, commits, or issues
argument-hint: [branch-name | commit-sha | #issue] | --continue | --list
---

# WIP - Work In Progress (Continue/Resume)

<!--
WHEN TO USE THIS COMMAND:
- Resuming work on EXISTING branches (most common)
- Continuing from a specific commit
- Jumping between different work in progress
- Picking up where you left off on an issue
- Quick fixes that don't need issues

EXAMPLES:
/wip 150-add-authentication  - Resume work on branch
/wip abc123def              - Continue from specific commit
/wip #150                   - Resume work on issue #150
/wip --continue             - Continue from last commit on current branch
/wip --list                 - Show all WIP branches and their status
/wip fix-typo              - Quick fix without issue

PRIMARY USE: Continue/resume existing work
SECONDARY USE: Jump between different WIP items

For STARTING NEW work from an issue, use /work #123 instead!
-->

## Your Task

Continue or resume existing work based on the type of argument provided.

### Step 0: Determine Entry Point

Parse $ARGUMENTS to determine what we're continuing from:

1. **--list**: Show all WIP branches
   ```bash
   git branch -a | grep -v "remotes/origin/HEAD"
   echo "Your WIP todos:"
   # Show todos marked as WIP from TodoWrite
   ```
   Exit after showing list

2. **--continue**: Continue from last commit on current branch
   ```bash
   LAST_COMMIT=$(git log -1 --format="%H %s")
   echo "Continuing from: $LAST_COMMIT"
   ```
   Show the last commit and what was being worked on

3. **#number**: Resume work on issue's branch
   ```bash
   ISSUE_NUM=$(echo "$ARGUMENTS" | grep -oE '[0-9]+')
   # Find branch for this issue
   BRANCH=$(git branch -a | grep -E "$ISSUE_NUM-" | head -1 | sed 's/.*\///')
   if [ -n "$BRANCH" ]; then
     git checkout "$BRANCH"
   else
     echo "No branch found for issue #$ISSUE_NUM. Use /work #$ISSUE_NUM to start."
   fi
   ```

4. **Commit SHA** (if matches [a-f0-9]{7,40}):
   ```bash
   # Check if it's a valid commit
   if git rev-parse --verify "$ARGUMENTS" >/dev/null 2>&1; then
     COMMIT_MSG=$(git log -1 --format="%s" "$ARGUMENTS")
     echo "Continuing from commit: $COMMIT_MSG"
     git checkout "$ARGUMENTS"
   fi
   ```

5. **Branch name** (default): Continue as currently implemented

### Step 1: Check for uncommitted changes

First check: !`git status --short | grep -v work-journal.json`

If there are changes shown (excluding work-journal.json), stash them:
Run: !`git stash push -m "WIP: Stashed before switching branches" -- . ':!.claude/work-journal.json'`

Note: The work-journal.json is excluded from stashing to preserve the work history.

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

**IMPORTANT: Use TodoWrite to maintain a persistent list of WIP items**

Track based on what we're continuing:

**For Issue-based work (#123):**
- Add/update todo: "Issue #123: [issue title] - continuing"
- Status: "in_progress"
- Include issue number for tracking

**For Commit-based work (SHA):**
- Add todo: "WIP from commit: [commit message]"
- Status: "in_progress"
- Include first 7 chars of SHA

**For Branch-based work:**
- Add/update todo: "WIP: [branch name] - [description]"
- Status: "in_progress"
- Mark if in worktree

**For --continue:**
- Update existing todo for current branch
- Add note: "Continued at [timestamp]"

All WIP todos persist until the work is merged or explicitly completed.
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
