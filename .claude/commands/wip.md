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
  # Ask what they're working on
  echo "What are you working on? (brief description)"
  echo "Examples: 'fix-commands', 'update-docs', 'explore-auth'"
  echo ""
  echo "Enter description (or press Enter for 'general-fixes'):"
  
  # In slash command context, we'll prompt for input
  # Default to something meaningful if no response
  read -r WORK_DESCRIPTION
  
  if [[ -z "$WORK_DESCRIPTION" ]]; then
    BRANCH_NAME="general-fixes"
  else
    # Convert description to branch name
    # "Fix slash commands" → "fix-slash-commands"
    BRANCH_NAME=$(echo "$WORK_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
  fi
  
  echo "📝 Branch name: $BRANCH_NAME"
fi

# Check if branch already exists
if git show-ref --quiet refs/heads/"$BRANCH_NAME"; then
  echo "⚠️ Branch '$BRANCH_NAME' already exists!"
  echo "Options:"
  echo "1. Switch to existing branch: git checkout $BRANCH_NAME"
  echo "2. Create new branch: /wip $BRANCH_NAME-2"
  exit 1
fi

# Create and switch to branch
git checkout -b "$BRANCH_NAME"
echo "✅ Created and switched to branch: $BRANCH_NAME"
```

### Step 3: Set Up Simple Tracking

Create a lightweight TodoWrite list for tracking:
```bash
# Use the description from branch creation
if [[ -z "$WORK_DESCRIPTION" ]]; then
  WORK_DESCRIPTION="General improvements"
fi

# Create simple todos
TodoWrite([
  {
    content: "Work on: $WORK_DESCRIPTION",
    status: "in_progress",
    activeForm: "Working on: $WORK_DESCRIPTION"
  }
])

echo "💡 Simple workspace ready. No issue created."
echo "📝 This is for iterative/exploratory work."
echo "📌 Working on: $WORK_DESCRIPTION"
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
# Interactive - asks what you're working on
/wip
→ Prompt: "What are you working on?"
→ You type: "fixing slash commands"
→ Creates: fix-slash-commands

# Direct - provide branch name
/wip update-docs
→ Creates: update-docs

# Default - just press Enter when asked
/wip
→ Prompt: "What are you working on?"
→ You press Enter
→ Creates: general-fixes

# Resume existing work
git checkout existing-branch
→ Switches to existing WIP branch
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