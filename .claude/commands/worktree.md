---
allowed-tools: Bash(*)
description: Manage git worktrees - list, create, remove, or clean up
argument-hint: [list|add|remove|clean] or empty for menu
---

# Worktree Management

<!--
WHEN TO USE THIS COMMAND:
- Only for occasional cleanup of orphaned branches (branches without worktrees)
- When you manually deleted a worktree directory and need to clean up
- To see all worktrees at once across your entire project

YOU DON'T NEED THIS COMMAND FOR:
- Normal daily work - use /wip instead
- Creating worktree branches - /wip asks you automatically
- Switching between branches - /wip handles detection

BASICALLY: /wip handles 95% of worktree needs. This is just for cleanup.
-->

## Your Task

Manage git worktrees based on the argument provided.

### Step 1: Handle based on arguments

**If $ARGUMENTS is empty (user just typed /worktree):**
Show menu:
```
Worktree Management:
1. List all worktrees
2. Add new worktree
3. Remove worktree
4. Clean up stale worktrees
5. Help

Choose option (1-5):
```
Wait for response and execute chosen option.

**If $ARGUMENTS is "list":**
1. Run: !`git worktree list`
2. For each worktree, show:
   - Branch name
   - Directory path
   - Current commit
3. Also check for orphaned branches (branches that were in deleted worktrees):
   - Run: !`git branch --format='%(refname:short)' | while read branch; do if ! git worktree list | grep -q "$branch"; then echo "🔍 Orphaned: $branch"; fi; done`

**If $ARGUMENTS is "add [branch-name]":**
1. Extract branch name from arguments
2. Check if branch already exists: !`git branch --list [branch-name]`
3. If exists:
   - Create worktree from existing: !`git worktree add ../worktrees/[branch-name] [branch-name]`
4. If not exists:
   - Create new branch in worktree: !`git worktree add ../worktrees/[branch-name] -b [branch-name]`
5. Tell user: "📁 Created worktree at: ../worktrees/[branch-name]"
6. Tell user: "Navigate there with: cd ../worktrees/[branch-name]"

**If $ARGUMENTS is "remove [branch-name]":**
1. Extract branch name from arguments
2. Find worktree path: !`git worktree list --porcelain | grep -B1 "branch refs/heads/[branch-name]" | grep "worktree" | cut -d' ' -f2`
3. If worktree found:
   - Remove worktree: !`git worktree remove [path]`
   - ASK: "Also delete the branch? (y/n)"
   - If YES:
     - Delete local branch: !`git branch -D [branch-name]`
     - ASK: "Delete from GitHub too? (y/n)"
     - If YES: !`git push origin --delete [branch-name]`
4. If no worktree found:
   - Tell user: "No worktree found for branch [branch-name]"
   - Check if branch exists: !`git branch --list [branch-name]`
   - If exists, ASK: "Branch exists without worktree. Delete it? (y/n)"

**If $ARGUMENTS is "clean":**
1. Prune stale worktrees: !`git worktree prune -v`
2. List orphaned branches (branches without worktrees that look like worktree branches):
   - Run: !`git branch --format='%(refname:short)' | grep -E '^[0-9]+-' | while read branch; do if ! git worktree list | grep -q "$branch"; then echo "$branch"; fi; done`
3. If orphaned branches found:
   - ASK: "Found orphaned worktree branches. Review and clean? (y/n)"
   - If YES, for each branch:
     - Show branch info: !`git log -1 --oneline [branch]`
     - ASK: "Delete [branch]? (y/n/skip all)"

### Step 2: Best Practices Reminder

After any operation, remind user:
- "💡 Tip: Use worktrees for parallel work on multiple features"
- "💡 Tip: Always use 'git worktree remove' instead of deleting directories"
- "💡 Tip: Run '/worktree clean' periodically to remove stale entries"

### Step 3: Show current status

After operation completes:
1. Show updated worktree count
2. Show current branch
3. If in a worktree, show its path