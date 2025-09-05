---
allowed-tools: Bash(*), TodoWrite(*)
description: Start work-in-progress branch for iterative development without issues
argument-hint: [branch-name] or empty for auto-named branch
---

# WIP - Work In Progress

## Context
- Current branch: !`git branch --show-current`
- Existing WIP branches: !`git branch | grep -E "wip-|fix-|explore-|tweak-"`
- Uncommitted changes: !`git status --short`

## Your Task

When user runs `/wip $ARGUMENTS`, create a simple workspace for iterative work.

### Step 1: Handle Any Uncommitted Work

Check for uncommitted changes:
```bash
if [[ -n $(git status --porcelain) ]]; then
  echo "📝 You have uncommitted changes. Options:"
  echo "1. Commit them to current branch"
  echo "2. Stash them"
  echo "3. Discard them"
  # For now, we'll stash
  git stash push -m "WIP: Stashed before creating new branch"
  echo "✅ Changes stashed. Run 'git stash pop' to restore later."
fi
```

### Step 2: Create Branch

Determine branch name:
```bash
if [[ -n "$ARGUMENTS" ]]; then
  # User provided a name
  BRANCH_NAME="$ARGUMENTS"
else
  # Auto-generate name with date
  BRANCH_NAME="wip-$(date +%Y%m%d-%H%M)"
  echo "📝 Auto-generated branch name: $BRANCH_NAME"
fi

# Create and switch to branch
git checkout -b "$BRANCH_NAME"
echo "✅ Created and switched to branch: $BRANCH_NAME"
```

### Step 3: Set Up Simple Tracking

Create a lightweight TodoWrite list for tracking:
```bash
echo "What are you working on? (brief description)"
# Example: "Fixing slash commands"

# Create simple todos
TodoWrite([
  {
    content: "Explore/iterate on: $DESCRIPTION",
    status: "in_progress",
    activeForm: "Working on: $DESCRIPTION"
  }
])

echo "💡 Simple workspace ready. No issue created."
echo "📝 This is for iterative/exploratory work."
```

### Step 4: Provide Next Steps

```bash
echo ""
echo "🚀 You're now on branch: $BRANCH_NAME"
echo ""
echo "Common next steps:"
echo "• Work with Claude iteratively"
echo "• Commit whenever: git add -A && git commit -m 'wip: description'"
echo "• Push when ready: git push -u origin $BRANCH_NAME"
echo "• Create PR when done: gh pr create --fill"
echo ""
echo "No issue needed unless this becomes a feature!"
```

## Key Principles

- **No ceremony** - Just create branch and go
- **No issue required** - This is for exploration
- **Simple commits** - Use "wip:" prefix
- **Convert later** - Can always create issue if needed

## Examples

```bash
# Auto-named branch for quick exploration
/wip
→ Creates: wip-20250905-1430

# Named branch for specific work
/wip fix-typos
→ Creates: fix-typos

# Continue existing WIP
/wip --continue
→ Shows existing WIP branches to resume
```

## When to Use This vs /create-issue

Use `/wip` for:
- Quick fixes and tweaks
- Exploring solutions
- Iterative work with Claude
- Maintenance tasks
- "Let me try something" moments

Use `/create-issue` for:
- New features
- Planned work
- Work that needs tracking
- Anything requiring review/approval

## Important Notes

- WIP branches can live for days/weeks
- No pressure to create issues
- Can create multiple WIP branches
- Clean up old ones with: `git branch -d branch-name`
- If WIP becomes important, create issue later