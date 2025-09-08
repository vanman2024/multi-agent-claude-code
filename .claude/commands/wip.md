---
allowed-tools: Bash(*)
description: Switch to or create a work-in-progress branch
argument-hint: [branch-name] or leave empty for current status
---

# WIP - Work In Progress

<!--
WHEN TO USE THIS COMMAND:
- Resume work on an existing branch
- Create a new WIP branch for quick fixes
- Switch between different branches

EXAMPLES:
/wip                      - Show current branch status
/wip fix-typo            - Switch to or create branch
/wip 150-add-auth        - Switch to issue branch
-->

## Your Task

Switch to a branch or show current status.

### If no arguments provided

Show current status:
Run: !git branch --show-current
Run: !git status --short

Tell user:
- Current branch name
- Number of uncommitted files
- Use `/wip-status` to see all branches
- Use `/wip branch-name` to switch branches

### If arguments provided (branch name)

First, check current status:
Run: !git status --short

If there are uncommitted changes:
Run: !git stash push -m "WIP: Saved work from $(git branch --show-current)"
Tell user: "Stashed changes from current branch"

Try to checkout the branch:
Run: !git checkout $ARGUMENTS

If checkout succeeds:
- Run: !git pull origin $ARGUMENTS --no-rebase 2>/dev/null || true
- Tell user: "Switched to branch: $ARGUMENTS"

If checkout fails (branch doesn't exist):
- Run: !git checkout -b $ARGUMENTS
- Run: !git push -u origin $ARGUMENTS
- Tell user: "Created new branch: $ARGUMENTS"

Show final status:
Run: !git status --short