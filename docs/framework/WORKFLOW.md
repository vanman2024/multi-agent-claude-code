# Development Workflow Guide

## 🎯 Quick Decision Tree

```
What are you doing?
├── Starting New Project → Use `/project-setup` → `/plan:generate` → `/test:generate`
│   └── Creates vision, docs, and tests first
├── Building Real Features → Use `/create-issue` then `/work`
│   └── Issue stays open during entire development
├── Infrastructure Setup → Work locally, no issue needed
│   └── DevOps, CI/CD, monitoring are local tasks
├── Resuming Issue Work → Use `/wip branch-name`
│   └── Quick way back to your issue branch
├── Quick Fix/Typo → Use `/wip`
│   └── No issue needed for trivial changes
└── Experimenting → Use `/wip`
    └── Try ideas before creating issues
```

## 🚀 Three Main Workflows

### Workflow 0: Project Planning (New Projects Only)

**For:** Brand new projects that need comprehensive planning

```bash
# 1. Interactive discovery and vision creation
/project-setup
# Creates: docs/PROJECT_PLAN.md (high-level vision)

# 2. Generate detailed technical documentation
/plan:generate
# Creates: ARCHITECTURE.md, INFRASTRUCTURE.md, FEATURES.md, DESIGN_SYSTEM.md

# 3. Generate comprehensive test suites
/test:generate --all
# Creates: Unit tests, API tests (Postman), E2E tests
# 90% test coverage before writing any code!

# 4. Now ready for implementation
/create-issue "First major feature"
/work #1
```

**Key Points:**
- Only run once at project start
- Creates all documentation upfront
- Tests ready before implementation
- Infrastructure tasks stay local (no issues)
- Only major features become issues (10-20 total)

### Workflow 1: Feature Development (After Planning)

**For:** Building actual features from your plan - the major work items

```bash
# 1. Create issue first (planning document)
/create-issue "Add user authentication"
# Issue #150 created

# 2. Start development
/work #150
# Creates: 150-add-user-authentication branch
# Issue stays OPEN during development

# 3. Work for days/weeks
/wip 150-add-user-authentication  # Resume work
git add -A && git commit -m "feat: implement login form"
git push

# 4. Only create PR when feature is COMPLETE
gh pr create --body "Closes #150"
# Issue closes when PR merges
```

### Workflow 2: Quick Fixes & Experiments (Secondary)

**For:** Typos, small tweaks, experiments, template fixes

```bash
# Quick fix
/wip fix-typo
git add -A && git commit -m "fix: typo in README"
gh pr create --fill
# No issue needed for trivial changes

# Experiment
/wip test-payment-api
# Try things out
# If it works, THEN create issue
/create-issue "Integrate payment API"
```

## 📊 Understanding When to Use What

| Scenario | Command | Creates Issue? | Creates PR? |
|----------|---------|---------------|-------------|
| "Start new project" | `/project-setup` | No | No |
| "Generate tech docs" | `/plan:generate` | No | No |
| "Create test suites" | `/test:generate` | No | No |
| "Set up CI/CD" | Work locally | No | No |
| "Configure monitoring" | Work locally | No | No |
| "Build user authentication" | `/create-issue` + `/work` | Yes | When complete |
| "Continue auth development" | `/wip 150-auth-branch` | Already exists | When complete |
| "Fix typo in README" | `/wip` | No | Immediately |
| "Try new API approach" | `/wip` | No | If it works |
| "Fix bug #145" | `/work #145` | Already exists | When complete |

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
| **Planning Phase** | | |
| `/project-setup` | Create project vision | New projects only |
| `/plan:generate` | Generate technical docs | After project-setup |
| `/test:generate` | Create test suites | After plan:generate |
| **Implementation Phase** | | |
| `/create-issue` | Plan new feature | Major features (10-20 total) |
| `/work #123` | Implement issue | Working on tracked items |
| `/wip` | Start exploratory work | Quick fixes, experiments |
| `/wip branch-name` | Resume existing branch | Continue previous work |
| `/wip-status` | See all WIP branches | Check what you're working on |
| `/copilot-review` | Review Copilot's PR | When Copilot creates PRs |
| `/deploy` | Deploy to Vercel | When ready for production |

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

The key insight: **Plan first, then build. Not everything needs issues.**

### For New Projects:
1. **Plan** → `/project-setup` + `/plan:generate` + `/test:generate`
2. **Build** → `/create-issue` for major features only (10-20 issues)
3. **Deploy** → `/deploy` when ready

### What Needs Issues:
- ✅ Major features (user auth, payments, dashboards)
- ✅ Bug fixes that need tracking
- ✅ Work requiring approval

### What Doesn't Need Issues:
- ❌ Infrastructure setup (do locally)
- ❌ CI/CD configuration (do locally)
- ❌ Database migrations (do locally)
- ❌ Quick fixes and typos
- ❌ Exploratory work

Keep it simple. Use the process that matches your work.