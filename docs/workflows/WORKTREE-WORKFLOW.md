# Worktree Workflow Guide

## Overview
Git worktrees allow parallel development on multiple branches without switching contexts. This guide ensures smooth integration between worktrees and the main branch.

## Key Problems Solved
1. **Port Conflicts**: Each worktree server runs on different ports (8080 main, 8081+ worktrees)
2. **File Sync Issues**: Changes in worktrees weren't visible in main branch
3. **Testing Isolation**: Can test features without affecting main project
4. **Merge Complexity**: Simplified merging process

## Worktree Setup & Management

### Creating a Worktree for an Issue
```bash
# From main project directory
gh issue develop 155 --checkout

# This creates: /home/gotime2022/Projects/worktrees/155-[issue-title]
```

### Worktree Directory Structure
```
/home/gotime2022/Projects/
├── multi-agent-claude-code/        # Main project (port 8080)
└── worktrees/
    ├── 155-todo-github-sync/       # Worktree (port 8081)
    ├── 156-feature-xyz/            # Worktree (port 8082)
    └── ...
```

## Using the Worktree Sync Tool

### Quick Commands
```bash
# From main project directory
cd /home/gotime2022/Projects/multi-agent-claude-code

# List all worktrees
./.claude/scripts/worktree-sync.sh list

# Check differences
./.claude/scripts/worktree-sync.sh diff 155-todo-github-sync

# Sync files from worktree to main
./.claude/scripts/worktree-sync.sh sync 155-todo-github-sync

# Create PR from worktree
./.claude/scripts/worktree-sync.sh pr 155-todo-github-sync

# Merge worktree branch
./.claude/scripts/worktree-sync.sh merge 155-todo-github-sync
```

## Server Port Management

### Default Port Assignments
- **Port 8080**: Main project server
- **Port 8081**: First worktree
- **Port 8082**: Second worktree
- **Port 8083+**: Additional worktrees

### Setting Up Worktree Server

#### Auto-Reload Server (Recommended)
```bash
# Start with auto-reload - restarts automatically when files change
cd /home/gotime2022/Projects/worktrees/155-todo-github-sync/todo-viewer
npm run dev:8081  # Auto-restarts on any JS/HTML/CSS changes

# For main project
cd /home/gotime2022/Projects/multi-agent-claude-code/todo-viewer
npm run dev  # Runs on port 8080 with auto-reload
```

#### Manual Server (Old Way)
```bash
# Setup port for worktree (automatically updates server.js)
./.claude/scripts/worktree-sync.sh port 155-todo-github-sync 8081

# Start server in worktree
cd /home/gotime2022/Projects/worktrees/155-todo-github-sync/todo-viewer
node server.js
```

## ⚠️ CRITICAL: Worktree Branch Point

**IMPORTANT**: When creating a worktree, it branches from the commit where the issue was created, NOT from the latest main!

This means:
- Your worktree might have OLD code
- Recent fixes might be missing
- Always merge main into your worktree first

```bash
# After creating worktree, IMMEDIATELY merge latest main
cd /home/gotime2022/Projects/worktrees/155-todo-github-sync
git fetch origin main
git merge origin/main
```

## Complete Workflow Example

### 1. Start Working on Issue
```bash
# Create worktree from issue
gh issue develop 155 --checkout

# Navigate to worktree
cd /home/gotime2022/Projects/worktrees/155-todo-github-sync

# CRITICAL: Merge latest main to get recent fixes
git fetch origin main
git merge origin/main
```

### 2. Develop Features
```bash
# Make your changes
# Test locally with worktree server on port 8081
cd todo-viewer && node server.js

# Visit http://localhost:8081 to test
```

### 3. Commit Changes
```bash
git add -A
git commit -m "[WORKING] feat: Add new feature

Related to #155"
git push
```

### 4. Integration Options

#### Option A: Direct Merge (Small Changes)
```bash
# From main project
./.claude/scripts/worktree-sync.sh merge 155-todo-github-sync
git push origin main
```

#### Option B: Pull Request (Recommended)
```bash
# Create PR from worktree
./.claude/scripts/worktree-sync.sh pr 155-todo-github-sync

# Review and merge on GitHub
```

#### Option C: File Sync (Testing Only)
```bash
# Sync specific files without merging
./.claude/scripts/worktree-sync.sh sync 155-todo-github-sync
```

## Best Practices

### DO:
✅ Always use different ports for each worktree server
✅ Commit and push changes in worktree before merging
✅ Check differences before merging
✅ Create PRs for significant changes
✅ Keep worktree branches focused on single issues

### DON'T:
❌ Run multiple servers on the same port
❌ Make changes directly in main when worktree exists
❌ Forget to push worktree changes before merging
❌ Leave worktrees around after merging

## Cleanup After Merge

```bash
# After PR is merged, remove worktree
git worktree remove /home/gotime2022/Projects/worktrees/155-todo-github-sync

# Delete remote branch
git push origin --delete 155-todo-github-sync
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -i :8081

# Kill the process
kill <PID>
```

### Files Not Syncing
```bash
# Check differences first
./.claude/scripts/worktree-sync.sh diff 155-todo-github-sync

# Force sync if needed
rsync -av --update /path/to/worktree/file /path/to/main/
```

### Merge Conflicts
```bash
# In main project
git checkout main
git pull origin main
git merge origin/worktree-branch

# Resolve conflicts manually
git add .
git commit
git push
```

## Quick Reference Card

| Task | Command | Port |
|------|---------|------|
| Create worktree | `gh issue develop 155 --checkout` | - |
| Start main server | `cd todo-viewer && node server.js` | 8080 |
| Start worktree server | `cd worktrees/155-*/todo-viewer && node server.js` | 8081 |
| Check differences | `./worktree-sync.sh diff 155-todo-github-sync` | - |
| Create PR | `./worktree-sync.sh pr 155-todo-github-sync` | - |
| Merge to main | `./worktree-sync.sh merge 155-todo-github-sync` | - |
| List worktrees | `./worktree-sync.sh list` | - |

## Summary

The worktree workflow allows you to:
1. Work on features in isolation
2. Test on different ports without conflicts
3. Easily merge changes back to main
4. Keep the main branch stable

Use the `worktree-sync.sh` tool to manage the integration smoothly!