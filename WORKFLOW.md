# Development Workflow Guide

## 🎯 Quick Decision Tree

```
What are you doing?
├── Exploring/Iterating/Fixing → Use `/wip`
│   └── No issue needed, just branch and work
├── Building a Feature → Use `/create-issue` then `/work`
│   └── Full tracking with issues and PRs
└── Continuing Previous Work → Use `/wip branch-name`
    └── Resume any existing branch
```

## 🚀 Two Main Workflows

### Workflow 1: Exploratory/Iterative Work (Most Common with Claude)

**For:** Quick fixes, explorations, iterative improvements

```bash
# Start new exploratory work
/wip
# "What are you working on?" → "fixing commands"
# Creates: fix-commands branch
# Pushes to GitHub automatically

# Work iteratively with Claude
git add -A && git commit -m "wip: improving commands"
git push

# When ready (could be days later)
gh pr create --fill
# NO ISSUE NEEDED!
```

### Workflow 2: Planned Features (For Tracked Work)

**For:** New features, bugs that need tracking, work requiring review

```bash
# 1. Create issue with planning
/create-issue "Add user authentication"

# 2. Start work (creates branch + draft PR)
/work #123

# 3. Implement with tracking
# TodoWrite syncs with issue checkboxes

# 4. PR already linked to issue
gh pr merge
# Issue auto-closes
```

## 📊 Understanding When to Use What

| Scenario | Command | Creates Issue? | Creates PR? |
|----------|---------|---------------|-------------|
| "Let me try fixing this" | `/wip` | No | When ready |
| "Quick documentation update" | `/wip` | No | When ready |
| "Implement user auth feature" | `/create-issue` + `/work` | Yes | Yes (draft) |
| "Resume yesterday's work" | `/wip branch-name` | No | Already exists |
| "Fix bug #145" | `/work #145` | Already exists | Yes |

## 🔧 The `/wip` Command - Your Swiss Army Knife

### Creating New Work
```bash
/wip
# Asks: "What are you working on?"
# Creates branch from your description
# Pushes to GitHub for visibility
```

### Resuming Existing Work
```bash
# See your WIP branches on GitHub
# Copy branch name
/wip fix-auth-bug
# Resumes exactly where you left off
```

### Seeing All WIP Work
```bash
/wip-status
# Shows all WIP branches
# Shows TodoWrite tracking
# Shows what's active vs paused
```

## 🌳 Working with Branches

### Key Principles

1. **Branches are just workspaces** - Create them freely
2. **Not every branch needs an issue** - Issues are for planning/tracking
3. **Branches live on GitHub** - All WIP branches are pushed for backup/visibility
4. **PRs connect everything** - When ready, PR can reference issues or stand alone

### Branch Scope: One Branch = One Logical Feature

**The Golden Rule: A branch represents a coherent piece of work, NOT individual tiny tasks.**

#### ✅ CORRECT: One branch for entire feature
```bash
/wip add-user-auth
# This ONE branch includes ALL auth work:
# - Login form (might be issue #123)
# - Password reset (might be issue #124)
# - JWT tokens (might be issue #125)
# - User profile (might be issue #126)
# All related → Same branch!

# When done:
gh pr create --body "Complete auth system
Closes #123, #124, #125, #126"
```

#### ❌ WRONG: Separate branches for each piece
```bash
# DON'T create 10 branches for 1 feature:
/wip add-login-form      # Unnecessary!
/wip add-password-field  # Too granular!
/wip create-jwt-token    # Cluttered!
```

### Branch Lifecycle

```
Create Branch → Work Locally → Push to GitHub → Create PR → Merge → Delete
      ↑                              ↓
      └──── Can resume anytime ──────┘
```

### Continuing After Merge

Even after merging, you can:
- Continue the same branch (if not deleted)
- Create a follow-up branch
- Cherry-pick specific commits
- Revert if needed

```bash
# Continue working on merged branch
/wip previously-merged-branch

# Or create follow-up
git checkout -b feature-v2
```

## 📝 Commit Message Patterns

### For WIP/Exploratory Work
```bash
git commit -m "wip: trying new approach"
git commit -m "wip: fix command parsing"
git commit -m "wip: update docs"
```

### For Issue-Based Work
```bash
git commit -m "feat: Add user authentication

Related to #123"

git commit -m "fix: Resolve login error

Fixes #145"
```

## 🔄 Staying Synced

### Critical Sync Points

**ALWAYS `git pull origin main` at these times:**
1. Before starting any new work
2. After any PR merges (yours or others)
3. Start of each work session
4. Before creating issues

### Why This Matters
- Copilot works on GitHub, you work locally
- Without pulling, you work on outdated code
- Prevents conflicts and duplicate work

## 🤖 AI Agent Assignment

### Automatic Routing
- **Simple + Small** (Complexity ≤2, Size ≤S) → GitHub Copilot
- **Complex OR Large** → Claude Code locally
- **Exploratory** → Always Claude Code locally

### Using Copilot's PRs
```bash
# When Copilot creates PR #143
/copilot-review #143
# Choose: --quick (simple) or --thorough (complex)
# Reviews, tests, and merges if good
```

## ⚠️ Common Pitfalls to Avoid

### DON'T
- ❌ Create issues for every tiny fix
- ❌ Work directly on main branch
- ❌ Create PRs before issues (for planned work)
- ❌ Forget to pull after merges
- ❌ Delete branches immediately after merge

### DO
- ✅ Use `/wip` for exploratory work
- ✅ Keep branches on GitHub for visibility
- ✅ Pull frequently to stay synced
- ✅ Use TodoWrite for tracking WIP
- ✅ Create PRs when code is ready to share

## 🎓 Mental Models

### Issues vs Branches vs PRs

- **Issue** = Planning document (optional!)
- **Branch** = Workspace (always needed)
- **PR** = Code review request (when ready to merge)

### When Issues Are Needed

**Need Issue:**
- New features requiring planning
- Bugs that need tracking
- Work requiring approval
- Anything for sprint/project tracking

**Don't Need Issue:**
- Exploratory work
- Quick fixes
- Documentation updates
- Refactoring
- Maintenance tasks

## 📚 Command Reference

### Essential Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/wip` | Start exploratory work | Most work with Claude |
| `/wip branch-name` | Resume existing branch | Continue previous work |
| `/wip-status` | See all WIP branches | Check what you're working on |
| `/create-issue` | Plan new feature | Starting planned work |
| `/work #123` | Implement issue | Working on tracked items |
| `/copilot-review` | Review Copilot's PR | When Copilot creates PRs |

### Git Essentials

```bash
# Start new work
git checkout -b branch-name

# Save work
git add -A && git commit -m "wip: description"
git push

# Update from main
git pull origin main

# Create PR
gh pr create --fill

# Merge PR
gh pr merge --squash --delete-branch
```

## 🏁 Summary

The key insight: **Not everything needs the full ceremony of issues and PRs.**

- **Exploring?** → `/wip` and iterate
- **Building?** → `/create-issue` for planning
- **Continuing?** → `/wip branch-name` to resume

Keep it simple. Use the process that matches your work.