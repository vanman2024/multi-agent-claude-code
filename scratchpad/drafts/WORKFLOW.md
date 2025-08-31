# GitHub Development Workflow - AUTHORITATIVE VERSION

## ⚠️ THIS IS THE ONLY WORKFLOW - NO EXCEPTIONS

### Core Principle: Issues → PRs → Merge → Deploy

## 🔴 CRITICAL: The Standard Flow

### 1. ISSUE (Planning Phase)
**Purpose**: Define WHAT needs to be built
- **No commits** - just requirements
- **No code** - just specifications  
- **No branches** - just planning
- **No checks** - just discussion

**Triggers**:
- Project board assignment
- Milestone assignment  
- Label assignment
- Agent routing (Copilot vs Claude Code)

### 2. PULL REQUEST (Implementation Phase)
**Purpose**: HOW it's actually built
- **Contains all commits**
- **Has all code changes**
- **Runs all checks/CI/CD**
- **Shows diffs**
- **Branch created just-in-time**

### 3. MERGE (Integration Phase)
- PR approved
- All checks pass
- All checkboxes checked
- Merged to main branch
- Branch deleted

### 4. DEPLOY (Release Phase)
- Happens AFTER merge
- Only from main branch
- Tagged releases
- Rollback capability

## 📋 Step-by-Step Process

### Step 0: ALWAYS Start Fresh
```bash
git checkout main
git pull origin main
```
**IF NOT ON MAIN WITH LATEST → STOP!**

### Step 1: Create Issue (Planning)
```bash
/create-issue "Clear description of what needs to be built"
```
- Issue created with requirements
- NO branch created yet
- NO PR created yet
- Just planning documentation

### Step 2: Start Work (Implementation Begins)
```bash
/work #123  # This creates branch AND draft PR
```
OR manually:
```bash
git checkout -b feature/[issue-number]-short-name
git push -u origin feature/[issue-number]-short-name
gh pr create --draft --title "Implements #123"
```

### Step 3: Implement Solution
- Make changes
- Commit frequently
- Push to feature branch
- Update PR description

### Step 4: Ready for Review
```bash
gh pr ready  # Convert draft to ready
```
- All tests pass
- All checkboxes checked
- Request reviews

### Step 5: Merge
```bash
gh pr merge --squash --delete-branch
```
- Squash commits
- Delete branch
- Issue auto-closes

### Step 6: Clean Up
```bash
git checkout main
git pull origin main
```
Ready for next issue!

## ❌ What Should NOT Happen

**NEVER:**
- Create branches when issues are created
- Create PRs automatically from issues  
- Make commits without PRs
- Deploy before merge
- Make intelligent decisions in workflows
- Reuse old branches
- Work without an issue

## 🚨 Current Problems We're Fixing

### WRONG (Current State)
1. Issue created → Workflow creates branch immediately ❌
2. Workflow creates draft PR immediately ❌
3. 72+ unused branches accumulate ❌
4. Work may never happen on these branches ❌

### RIGHT (Target State)
1. Issue created (planning only) ✅
2. NO automatic branch ✅
3. NO automatic PR ✅
4. Branch/PR created when work starts ✅
5. Clean branch management ✅

## 📊 Open Work Status

### Issues (Planning Documents)
- **#71**: Copilot Auto-Assignment - IN PROGRESS (has PR #72)
- **#64**: Slash Command Redesign - PLANNED
- **#54**: Fix GitHub Workflows - IN PROGRESS (has PR #69 from Copilot)
- **#53**: PR Checkbox Auto-sync - PLANNED

### PRs (Implementation)
- **#72**: Our Copilot integration work (DRAFT)
- **#69**: Copilot's workflow fixes (DRAFT - needs review)

## 🔧 What Needs Fixing

### High Priority
1. **issue-to-implementation.yml** - Remove automatic branch/PR creation
2. **/work command** - Add branch/PR creation logic
3. **/create-issue command** - Remove branch creation triggers

### Medium Priority
- Review and merge Copilot's PR #69
- Complete our PR #72
- Update all templates

### Low Priority
- Documentation updates
- Hook adjustments

## ✅ Success Criteria

When properly implemented:
- Issues contain ZERO commits
- ALL commits exist in PRs
- Branches created just-in-time
- Deployment only after merge
- Workflows make no intelligent decisions
- No unused branches accumulate

## 🎯 Component Responsibilities

### GitHub Issues
Planning documents only

### GitHub PRs  
Implementation container only

### GitHub Actions
Plumbing only - no decisions

### Slash Commands
- `/create-issue`: Creates planning doc
- `/work`: Starts implementation

### Agents
- **Copilot**: Simple tasks (complexity ≤2, size XS-S)
- **Claude Code**: Complex tasks

## 📝 Notes

This workflow is **NOT A DRAFT** - it's the standard GitHub flow that the industry uses. We're just not following it correctly yet. Our automation is creating branches/PRs too early, at issue creation instead of when work starts.

The fix is simple: Move branch/PR creation from issue workflows to the /work command.