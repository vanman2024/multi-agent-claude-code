# Complete Feature Development Walkthrough

## From Idea to Production - Step by Step

### Step 1: Initial Idea (in scratchpad)
```bash
# Start with an idea document
echo "Feature idea: User authentication system" > scratchpad/ideas/auth-system.md
```

### Step 2: Create Issue (Planning Phase)
```bash
/create-issue "Add user authentication system with login/logout"
```
This creates:
- Issue #XX with title and description
- NO branch (just planning)
- NO PR (just planning)
- Assigns to project board
- Adds appropriate labels

### Step 3: Start Work (Implementation Phase)
```bash
/work #XX
```
This does:
- Pulls latest from main
- Creates branch: feature/XX-user-authentication
- Creates draft PR linked to issue #XX
- Switches to the new branch
- Ready to start coding

### Step 4: Implement Feature
```bash
# Make code changes
# Commit frequently
git add .
git commit -m "feat: Add login endpoint"
git push
```

### Step 5: Update PR Status
```bash
# When ready for review
gh pr ready
```

### Step 6: Review & Merge
```bash
# After approval
gh pr merge --squash --delete-branch
```
This:
- Merges to main
- Closes issue #XX automatically
- Deletes feature branch
- Triggers deployment

### Step 7: Clean Up
```bash
git checkout main
git pull origin main
# Ready for next feature
```

## What Each Component Does

### Slash Commands
- `/create-issue` - Creates planning document (issue)
- `/work #XX` - Creates branch and draft PR when starting work

### GitHub Issues
- Planning documents only
- Define WHAT to build
- NO code, NO branches

### GitHub PRs  
- Implementation containers
- Contain HOW it's built
- All code changes
- All CI/CD checks

### GitHub Actions
- Run tests
- Check labels
- Deploy after merge
- NO intelligent decisions

## Current State vs Target State

### ❌ CURRENT (Broken)
1. Create issue → Auto-creates branch
2. Auto-creates draft PR
3. 72+ unused branches accumulate

### ✅ TARGET (Fixed)
1. Create issue → Just planning
2. `/work #XX` → Creates branch/PR
3. Clean branch management

## Next Steps

1. Test `/create-issue` command
2. Test `/work` command with an issue
3. Verify no automatic branch creation
4. Complete full cycle on test feature