---
allowed-tools: Bash(*), TodoWrite(*)
description: Show status of all WIP branches and current work
argument-hint: none
---

# WIP Status - View All Work In Progress

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

### Step 3: Show all local WIP branches

Run: !`git branch | grep -E "wip-|fix-|explore-|update-|general-|^[0-9]+-"`
Show the list of WIP-style branches AND issue branches (starting with numbers).

For each branch, check if it's in a worktree:
- If it's in a worktree, mark with 📁 icon
- If not, mark with 🌿 icon

### Step 4: Show GitHub branches

Run: !`gh api repos/vanman2024/multi-agent-claude-code/branches --jq '.[].name' | grep -E "wip-|fix-|explore-|update-|general-|^[0-9]+-"`
Show WIP branches that exist on GitHub.

Cross-reference with worktree list:
- Mark worktree branches with 📁
- Mark regular branches with 🌿

### Step 4: Show TodoWrite WIP items

Check TodoWrite for all todos starting with "WIP:"
Display them with their status:
- in_progress = Currently working on
- pending = Paused/waiting
- completed = Done (can be cleaned up)

### Step 5: Provide options

Tell user they can:
- Resume any branch: `/wip [branch-name]`
- Create new work: `/wip`
- Clean up old branches: `git branch -d [branch-name]`
- See all branches on GitHub: https://github.com/vanman2024/multi-agent-claude-code/branches