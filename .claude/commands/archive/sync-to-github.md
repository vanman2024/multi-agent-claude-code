# Sync to GitHub

## Purpose
Force sync all local changes to GitHub so @claude bot can see the latest code.

## Usage
```
/sync-to-github
```

## Your Task

When user runs `/sync-to-github`, synchronize all local changes to GitHub:

### Step 1: Check Git Status
```bash
# Check current status
git status --short

# Get current branch
BRANCH=$(git branch --show-current)

# Count changes
MODIFIED=$(git status --porcelain | wc -l)
```

### Step 2: Stage All Changes
```bash
# Add all changes
git add -A

# Show what will be committed
git status
```

### Step 3: Create Sync Commit
```bash
# Create commit with timestamp
git commit -m "sync: push local changes for @claude visibility

Synced at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Files changed: $MODIFIED
Branch: $BRANCH

This ensures @claude bot sees latest code for testing."
```

### Step 4: Push to GitHub
```bash
# Push to current branch
git push origin "$BRANCH"

# If push fails due to diverged branches
git pull --rebase origin "$BRANCH"
git push origin "$BRANCH"
```

### Step 5: Notify @claude
After successful push, add comment to any open PR:
```bash
# Find PR for current branch
PR_NUMBER=$(gh pr list --head "$BRANCH" --json number -q '.[0].number')

if [ ! -z "$PR_NUMBER" ]; then
  gh pr comment "$PR_NUMBER" --body "🔄 **Code Synced to GitHub**

All local changes have been pushed. @claude can now see the latest code.

Changed files: $MODIFIED
Latest commit: $(git rev-parse --short HEAD)

@claude Please proceed with testing the latest code."
fi
```

### Step 6: Provide Summary
```
✅ Synced to GitHub
📦 Files changed: $MODIFIED  
🌿 Branch: $BRANCH
📝 Commit: $(git rev-parse --short HEAD)
🔗 PR: #$PR_NUMBER (if exists)

@claude can now see all your changes!
```

## Notes
- This ensures @claude always tests the latest code
- Useful before asking for PR reviews or testing
- Automatically notifies @claude in PR comments
- Works with the auto-sync hook for continuous sync