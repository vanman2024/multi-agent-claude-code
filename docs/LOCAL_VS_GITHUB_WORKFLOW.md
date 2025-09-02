# Local Development vs GitHub: The Complete Guide

## The Core Concept: Two Copies, One Truth

Think of it like Google Docs vs a Word document on your computer:
- **Local branch** = Your Word doc on your computer
- **GitHub branch** = The Google Doc online
- **They must be manually synced** = You have to "save to cloud" or "download latest"

## The Golden Rules

### Rule 1: Your Local Branch TRACKS a GitHub Branch
When you create a branch locally and push it:
```bash
git checkout -b fix/issue-123        # Creates LOCAL branch
git push -u origin fix/issue-123     # Creates GITHUB branch and LINKS them
```

Now your local `fix/issue-123` tracks `origin/fix/issue-123` on GitHub.

### Rule 2: Changes Don't Auto-Sync
- **Local commits stay local** until you `git push`
- **GitHub changes stay on GitHub** until you `git pull`
- **They can diverge** if you forget to sync

## The Proper Workflow

### 1. Starting Work on an Issue
```bash
# ALWAYS start from latest main
git checkout main
git pull origin main

# Create new branch
git checkout -b fix/issue-123

# Push immediately to create GitHub branch
git push -u origin fix/issue-123

# Create PR right away (can be draft)
gh pr create --draft --title "Fix: Issue 123" --body "Closes #123"
```

### 2. During Development
```bash
# Make changes
edit files...

# Commit locally
git add .
git commit -m "fix: Add validation"

# Push to GitHub (updates PR automatically)
git push

# If GitHub has changes (from Copilot, etc)
git pull
```

### 3. Common Scenarios

#### Scenario A: "My PR doesn't show my changes"
**Problem:** You committed locally but didn't push
**Fix:** 
```bash
git push
```

#### Scenario B: "Git says I'm behind origin"
**Problem:** GitHub has changes you don't have locally
**Fix:**
```bash
git pull
```

#### Scenario C: "Can't push - rejected"
**Problem:** GitHub has changes AND you have local changes
**Fix:**
```bash
git pull --rebase
git push
```

#### Scenario D: "Wrong branch is in my PR"
**Problem:** PR is looking at wrong branch
**Fix:** Check PR's base and head branches on GitHub

## Visual: What Happens When

```
LOCAL                          GITHUB
------                         -------
main                    <-->   origin/main
fix/issue-123          <-->   origin/fix/issue-123

When you:
- git commit  → Changes ONLY in LOCAL
- git push    → Copies LOCAL to GITHUB  
- git pull    → Copies GITHUB to LOCAL
```

## The Multi-Agent Confusion

### Why This Gets Confusing:
1. **Copilot works on GITHUB** - Makes commits directly to origin/branch
2. **You work LOCALLY** - Make commits to local branch
3. **Without pulling** - You don't see Copilot's changes
4. **Without pushing** - Copilot doesn't see your changes

### The Solution:
```bash
# Before EVERY work session
git pull

# After EVERY commit session  
git push

# Check status frequently
git status
```

## Checking Your Current State

### See Everything:
```bash
# What branch am I on?
git branch

# Am I synced with GitHub?
git status

# What's different locally vs GitHub?
git log origin/main..main  # Shows commits in local but not GitHub
git log main..origin/main  # Shows commits in GitHub but not local

# See all branches (local + remote)
git branch -a
```

## Emergency Fixes

### "I'm totally lost - just get me back to GitHub's version"
```bash
git fetch origin
git reset --hard origin/main  # WARNING: Loses local changes
```

### "I need to save my work but sync with GitHub"
```bash
git stash                    # Save local changes
git pull origin main         # Get GitHub's version
git stash pop               # Reapply your changes
```

## The Right Mental Model

Think of it as:
1. **GitHub is the source of truth** - That's what gets deployed
2. **Local is your workspace** - Where you make changes
3. **Push/Pull are the sync buttons** - You control when to sync
4. **Branches are just pointers** - They point to specific commits
5. **Origin/ prefix means GitHub's copy** - origin/main = GitHub's main

## Best Practices

### DO:
- ✅ Pull before starting work
- ✅ Push after commits
- ✅ Create PR immediately after creating branch
- ✅ Check `git status` frequently
- ✅ Keep branches short-lived

### DON'T:
- ❌ Work for hours without pushing
- ❌ Ignore "behind origin" warnings
- ❌ Create branches without pushing them
- ❌ Assume changes auto-sync
- ❌ Work directly on main

## Quick Reference Card

```bash
# Start work
git checkout main && git pull
git checkout -b feature/new
git push -u origin feature/new

# During work  
git add . && git commit -m "message"
git push

# Stay synced
git pull  # Get GitHub changes
git push  # Send local changes

# Check state
git status           # Am I synced?
git branch -vv       # What tracks what?
git log --oneline -5 # Recent commits
```

## Remember: Push Early, Pull Often!

The more frequently you sync, the fewer problems you'll have.