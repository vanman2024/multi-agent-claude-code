---
allowed-tools: Bash(*)
description: Show status of all WIP branches and current work
argument-hint: none
---

# WIP Status - View All Work In Progress

<!--
WHEN TO USE THIS COMMAND:
- See all your WIP branches at once
- Check which branches are worktrees (📁) vs regular (🌿)
- Find that branch you were working on yesterday
- Clean overview of all work in progress

WHAT IT SHOWS:
- Current branch you're on
- All worktree branches and their locations
- All local WIP branches
- All GitHub WIP branches
- Stashed work that needs attention

USE THIS TO: Get oriented when you have multiple things going.
-->

## Your Task

Show the user all their WIP branches and what's being worked on.

### Step 1: Show current branch

Run: !`git branch --show-current`
Tell user: "Currently on branch: [branch name]"

### Step 2: Show worktree branches FIRST

Run: !`git worktree list`
This shows all worktrees with their paths and current branches.

If there are worktrees, display them clearly:
```
📁 WORKTREE BRANCHES (checked out in separate directories):
  - [branch-name] at [path]
  - [branch-name] at [path]
```

### Step 3: Show ALL GitHub branches FIRST

First, prune old remote references: !`git remote prune origin`

Get ALL GitHub branches: !`gh api repos/vanman2024/multi-agent-claude-code/branches --paginate | jq -r '.[].name' | sort`

Display as numbered list:
**🌐 ALL GITHUB BRANCHES:**
Number and list EVERY branch found (could be 7, 25, 50, 100+):
1. [first branch]
2. [second branch]
3. [third branch]
...
N. [last branch]

### Step 4: Show sync status

Get local branches with tracking info: !`git branch -vv`

Now categorize based on what you found:

**✅ SYNCED (local + GitHub):**
- List branches that exist both locally and on GitHub
- Mark with 📁 if it's a worktree branch

**❌ GitHub-Only (not local):**
- List branches that are ONLY on GitHub
- Suggest: `git checkout -b [branch] origin/[branch]`

**⚠️ Local-Only (not on GitHub):**
- Branches that exist locally but NOT pushed to GitHub
- These need: `git push -u origin [branch]`

**🔴 STALE Local (remote deleted):**
- Branches marked as "[gone]" (were on GitHub but deleted/merged)
- Suggest cleanup: `git branch -d [branch-name]`

**📤 UNPUSHED COMMITS:**
- Any branches with "ahead X" status
- Show: `[branch] - X commits need pushing`

### Step 5: Show stashed work

Run: !`git stash list`

If there are stashes, display ALL of them:
**📦 STASHED WORK (unsaved changes):**
- stash@{0}: message
- stash@{1}: message
- stash@{2}: message
(show every single stash, no limit)

### Step 6: Provide options

Tell user they can:
- Resume any branch: `/wip [branch-name]`
- Create new work: `/wip`
- Clean up old branches: `git branch -d [branch-name]`
- See all branches on GitHub: https://github.com/vanman2024/multi-agent-claude-code/branches