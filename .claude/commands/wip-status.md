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

### Step 2: Show all local WIP branches

Run: !`git branch | grep -E "wip-|fix-|explore-|update-|general-"`
Show the list of WIP-style branches

### Step 3: Show GitHub branches

Run: !`gh api repos/vanman2024/multi-agent-claude-code/branches --jq '.[].name' | grep -E "wip-|fix-|explore-|update-|general-"`
Show WIP branches that exist on GitHub

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