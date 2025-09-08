# ⚠️ WORKTREE SAFETY CHECKLIST

## The Main Problems with Worktrees

1. **OLD CODE PROBLEM**: `gh issue develop` creates worktrees from the commit when the issue was created, NOT from current main
2. **LOST WORK PROBLEM**: Changes in worktrees don't automatically sync to main
3. **MERGE CONFLICT PROBLEM**: Parallel development can create conflicts
4. **PORT CONFLICT PROBLEM**: Multiple servers on same port crash

## 🛡️ Safe Worktree Practices

### ✅ ALWAYS DO THIS

#### When Creating a Worktree
```bash
# DON'T use gh issue develop (it uses old code)
# DO use our safe script instead
./.claude/scripts/safe-worktree.sh create 156

# Or if you must use gh issue develop, IMMEDIATELY:
gh issue develop 156 --checkout
cd /home/gotime2022/Projects/worktrees/156-*
git fetch origin main
git merge origin/main  # GET LATEST CODE!
```

#### Before Starting Work
```bash
# Verify you have latest code
./.claude/scripts/safe-worktree.sh verify

# If behind, merge main
./.claude/scripts/safe-worktree.sh merge
```

#### While Working
```bash
# Use auto-reload server (no manual restarts)
npm run dev:8081  # Auto-restarts on changes

# Commit frequently
git add -A
git commit -m "[WIP] Working on feature"
git push
```

#### Before Creating PR
```bash
# Merge latest main one more time
git fetch origin main
git merge origin/main

# Resolve any conflicts
# Test everything still works
# Then create PR
```

### ❌ NEVER DO THIS

1. **NEVER** assume worktree has latest code
2. **NEVER** work for hours without committing
3. **NEVER** run multiple servers on same port
4. **NEVER** delete worktree without pushing changes
5. **NEVER** create worktree without merging main first

## 🔍 Quick Status Checks

### Check if Worktree is Behind Main
```bash
cd /path/to/worktree
git fetch origin main
git rev-list --count HEAD..origin/main
# If > 0, you're behind and need to merge
```

### Check All Worktrees Status
```bash
./.claude/scripts/worktree-sync.sh list
```

### Find Which Port to Use
```bash
# Issue 155 = port 8081
# Issue 156 = port 8082
# Issue 157 = port 8083
# Formula: 8080 + (issue_number % 100)
```

## 🚨 Emergency Recovery

### If You Lost Work
```bash
# Check git reflog for lost commits
git reflog

# Recover a lost commit
git cherry-pick <commit-hash>
```

### If Ports are Conflicting
```bash
# Find what's using the port
lsof -i :8081

# Kill it
kill <PID>

# Use a different port
PORT=8085 npm run dev
```

### If Merge Has Conflicts
```bash
# See what's conflicting
git status

# Use main's version
git checkout --theirs <file>

# Use worktree's version
git checkout --ours <file>

# Or manually edit and fix
```

## 📋 Complete Safe Workflow

```bash
# 1. Create SAFE worktree (from latest main)
./.claude/scripts/safe-worktree.sh create 157

# 2. Navigate and verify
cd /home/gotime2022/Projects/worktrees/157-worktree
./.claude/scripts/safe-worktree.sh verify

# 3. Start auto-reload server
cd todo-viewer
npm run dev:8081

# 4. Work and commit frequently
git add -A && git commit -m "feat: Add feature"
git push

# 5. Before PR, merge main again
./.claude/scripts/safe-worktree.sh merge

# 6. Create PR
./.claude/scripts/worktree-sync.sh pr 157-worktree

# 7. After merge, cleanup
git worktree remove /home/gotime2022/Projects/worktrees/157-worktree
```

## 🎯 Golden Rules

1. **Merge Main First** - Always get latest code before starting
2. **Commit Often** - Don't lose work
3. **Use Auto-Reload** - No manual server restarts
4. **Verify Before PR** - Check you're not behind main
5. **Clean Up After** - Remove worktrees after merging

## Remember

> "A worktree is like a parallel universe - it starts from the past, not the present. Always bring it to the present before working!"