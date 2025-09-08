# Multi-Instance Claude Code Workflow Guide

## The Core Problem

Building large applications with a single Claude instance is **slow**. But using multiple instances with worktrees creates **chaos** - lost code, merge conflicts, confusion about which version is running.

This guide provides strategies to safely use multiple Claude instances for faster development.

## Strategy Overview

### 🎯 The Golden Rule
**Separate by concern, not by convenience**

Multiple instances work well when they're working on COMPLETELY separate areas. They fail when there's ANY overlap.

## Safe Multi-Instance Patterns

### Pattern 1: Vertical Slice (AVOID for multi-instance)
❌ **DON'T DO THIS with multiple instances:**
- Instance 1: Backend API for user auth
- Instance 2: Frontend UI for user auth
- **Problem**: These are tightly coupled - can't test one without the other

### Pattern 2: Horizontal Separation (SAFE)
✅ **DO THIS instead:**
- Instance 1: Complete user authentication (backend + frontend)
- Instance 2: Complete reporting system (backend + frontend)
- **Why it works**: No overlap, each instance owns their full feature

### Pattern 3: Layer Separation (SAFE with rules)
✅ **Can work if strictly enforced:**
- Instance 1: Database migrations and models only
- Instance 2: API endpoints only (after Instance 1 completes)
- Instance 3: Frontend only (after Instance 2 completes)
- **Requirements**: Sequential work, clear handoffs

## Workflow Decision Tree

```
Is the feature backend + frontend coupled?
├─ YES → Use single instance on main branch
│        (Most features fall here)
│
└─ NO → Can features overlap?
    ├─ YES → Use single instance on main branch
    │
    └─ NO → Are you building foundation (DB/models)?
        ├─ YES → Use single instance first, then split
        │
        └─ NO → Safe to use multiple instances
```

## Practical Workflows

### Workflow A: Single Instance (Safest, Slower)
**When to use**: Frontend-heavy features, tightly coupled features, uncertain scope

```bash
# One Claude instance, main branch
git checkout main
git pull
/work #123
# Implement feature completely
# Test everything together
git add -A && git commit -m "feat: Complete feature"
git push
```

**Pros**: No conflicts, no confusion, everything works together
**Cons**: Slower development

### Workflow B: Multiple Instances - Separate Features
**When to use**: Building multiple independent features simultaneously

```bash
# Instance 1: Authentication system
git checkout -b feature/auth
/work #101  # Complete auth system

# Instance 2: Reporting system (different terminal)
git checkout -b feature/reports  
/work #102  # Complete reporting system

# Both can work simultaneously without conflicts
```

**Pros**: 2x faster development
**Cons**: Need careful planning to ensure no overlap

### Workflow C: Multiple Instances - Same Feature (DANGEROUS)
**When to use**: Only with VERY careful coordination

```bash
# Instance 1: Backend API
git worktree add ../worktrees/api-backend feature/api
cd ../worktrees/api-backend
# Work on ONLY backend files

# Instance 2: Frontend UI
git worktree add ../worktrees/ui-frontend feature/ui
cd ../worktrees/ui-frontend  
# Work on ONLY frontend files

# CRITICAL: Define exact file boundaries
# Backend: /api/*, /models/*, /services/*
# Frontend: /components/*, /pages/*, /styles/*
```

**Pros**: Parallel development on same feature
**Cons**: High risk of conflicts, ports issues, confusion

## Port Management for Multiple Instances

### Reserved Port Assignments
```
8080 - Main branch (production-like)
8081 - Worktree/Feature 1
8082 - Worktree/Feature 2
8083 - Worktree/Feature 3
3000 - Frontend dev server (main)
3001 - Frontend dev server (feature 1)
3002 - Frontend dev server (feature 2)
```

### Automatic Port Selection
```javascript
// In server.js
const BASE_PORT = 8080;
const BRANCH = process.env.GIT_BRANCH || 'main';
const PORT = BRANCH === 'main' ? BASE_PORT : BASE_PORT + hashCode(BRANCH) % 20;
```

## Critical Rules for Multi-Instance Success

### 1. File Ownership Rules
- Each instance must have EXCLUSIVE ownership of their files
- Never have two instances editing the same file
- Document ownership in each issue

### 2. Merge Frequency Rules  
- Merge at least every 4 hours
- Never let branches diverge more than 10 commits
- Always pull before starting work

### 3. Communication Rules
- Document which instance is doing what
- Use issue comments to coordinate
- Clear handoff points between instances

### 4. Testing Rules
- Each instance tests their own work
- Integration testing after EVERY merge
- Never merge untested code

## When to STOP Using Multiple Instances

STOP if you see:
- Frequent merge conflicts
- "Lost" code that was working before  
- Confusion about which version is running
- More time managing instances than coding
- Features breaking after merges

## Recommended Approach for Large Apps

### Phase 1: Foundation (Single Instance)
- Database schema
- Core models
- Authentication
- Basic routing

### Phase 2: Parallel Development (Multiple Instances)
- Instance 1: Admin dashboard
- Instance 2: User dashboard  
- Instance 3: API endpoints
- Instance 4: Background jobs

### Phase 3: Integration (Single Instance)
- Merge all branches
- Integration testing
- Bug fixes
- Polish

## Quick Reference Commands

### Check what's running where
```bash
# See all worktrees
git worktree list

# See what's on each port
lsof -i :8080-8090

# See all branches
git branch -a

# See divergence from main
git rev-list --count HEAD..origin/main
```

### Safe worktree creation
```bash
# ALWAYS do this sequence
gh issue develop 123 --checkout
cd /path/to/worktree
git fetch origin main
git merge origin main  # GET LATEST CODE!
```

### Emergency cleanup
```bash
# If everything is broken
git checkout main
git pull origin main
git worktree prune
killall node  # Stop all servers
# Start fresh
```

## The Bottom Line

**For speed**: Use multiple instances on completely separate features
**For safety**: Use single instance on main branch
**For sanity**: Document everything, merge often, test always

The fastest workflow that still works is better than the perfect workflow that creates chaos.