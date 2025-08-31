---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), Edit(*), TodoWrite(*)
description: Intelligently selects and implements work based on sprint priorities and dependencies
argument-hint: [#issue-number] [--deploy] [--test]
---

# Work - Intelligent Implementation Command

## Context
- Current branch: !`git branch --show-current`
- Sprint issues: !`gh issue list --label "sprint:current" --state open --json number,title,labels`
- Blocked issues: !`gh issue list --label "blocked" --state open --json number,title`
- In progress: !`gh issue list --label "status:in-progress" --state open --json number,title,assignees`

## Your Task

When user runs `/work $ARGUMENTS`, intelligently select and implement work.

### Step 0: 🔴 ENFORCE WORKFLOW - MUST BE ON MAIN WITH LATEST

**CRITICAL: Before doing ANYTHING else, check branch and sync status:**

```bash
# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if on main
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "❌ ERROR: You must be on main branch to start work!"
  echo ""
  echo "Run these commands first:"
  echo "  git checkout main"
  echo "  git pull origin main"
  echo ""
  echo "Current branch: $CURRENT_BRANCH"
  echo "Required branch: main"
  echo ""
  echo "See WORKFLOW.md for the required process."
  exit 1
fi

# Check if main is up to date
git fetch origin main --quiet
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

if [[ "$LOCAL" != "$REMOTE" ]]; then
  echo "⚠️ Your main branch is not up to date!"
  echo "Local:  $LOCAL"
  echo "Remote: $REMOTE"
  echo ""
  echo "🔄 Auto-pulling latest changes..."
  git pull origin main
  
  if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to pull latest changes"
    echo "Please resolve any conflicts and try again"
    exit 1
  fi
  
  echo "✅ Successfully pulled latest changes"
fi

echo "✅ On main branch with latest changes - proceeding..."
```

If not on main or not up to date, STOP and tell the user to:
1. `git checkout main`
2. `git pull origin main`
3. Then retry the command

**DO NOT PROCEED if not on main with latest changes!**

### Step 1: Determine Work Mode

Check if specific issue provided or auto-select:
- If `#123` provided → work on that specific issue
- If `--deploy` → deploy current branch to Vercel
- If `--test` → run test suite
- If no arguments → intelligently select next work item

### Step 2: Intelligent Work Selection (when no issue specified)

#### Check Current Sprint
```bash
gh issue list --label "sprint:current" --state open --json number,title,labels,body
```

#### Check Project Board Status
```bash
# Get issues from project board columns
gh project item-list 1 --owner vanman2024 --format json

# Check "In Progress" column - don't start new work if something's in progress
gh issue list --label "status:in-progress" --state open
```

#### Analyze Dependencies and Blockers
Use mcp__github__get_issue for each sprint issue to:
- Check for "blocked" label
- Look for "Depends on #XX" in issue body
- Check if dependency issues are closed
- Find issues that unblock the most other work

#### Priority Rules for Selection
1. **Unblocked work that unblocks others** - Issues that when completed, unblock other issues
2. **High priority unblocked issues** - Check for P0, P1, P2 labels
3. **Small quick wins** - Issues labeled "good first issue" or "size:XS"
4. **Continue in-progress work** - If user has work in progress, suggest continuing it
5. **Next in sprint sequence** - Follow logical order if issues are numbered sequentially

### Step 3: Verify Selection Is Valid

Before starting work, check:
```bash
# Is it blocked?
gh issue view $ISSUE_NUMBER --json labels | grep -q "blocked"

# Are its dependencies resolved?
gh issue view $ISSUE_NUMBER --json body | grep -oP "Depends on #\K\d+"
# For each dependency found, check if closed:
gh issue view $DEPENDENCY --json state

# Is someone else working on it?
gh issue view $ISSUE_NUMBER --json assignees
```

### Step 4: Get Complete Issue Context

Use mcp__github__get_issue to get full details:
- Title and full description
- All labels (type, priority, size, etc.)
- Current state and assignees
- Comments for additional context
- Linked PRs if any

### Step 5: Create Feature Branch

```bash
# Get issue type from labels
ISSUE_TYPE=$(gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name' | grep -E "feature|bug|enhancement|refactor|task" | head -1)

# Create branch name
BRANCH_NAME="$ISSUE_TYPE-$ISSUE_NUMBER-short-description"

# Create and checkout
git checkout -b $BRANCH_NAME
```

### Step 6: Implementation Routing

Based on issue type and complexity from labels:

#### For Simple Issues (Complexity 1-2, Size XS-S)
- Implement directly using Read/Write/Edit tools
- Follow the issue's implementation checklist
- Create straightforward solution

#### For Complex Issues (Complexity 3+, Size M+)
Use Task tool with appropriate agent:
- **Features/Bugs** → general-purpose agent
- **Refactoring** → code-refactorer agent  
- **Security** → security-auth-compliance agent
- **Integration** → integration-architect agent

### Step 7: Update Issue Status

```bash
# Add in-progress label
gh issue edit $ISSUE_NUMBER --add-label "status:in-progress"

# Add comment about starting work
gh issue comment $ISSUE_NUMBER --body "🚀 Started implementation on branch \`$BRANCH_NAME\`"
```

### Step 8: Run Tests

```bash
# Detect and run appropriate test suite
if [ -f "package.json" ]; then
  npm test
  npm run lint
elif [ -f "requirements.txt" ]; then
  pytest
fi
```

### Step 9: Create Pull Request

```bash
# Push branch
git push -u origin $BRANCH_NAME

# Create PR linked to issue
gh pr create \
  --title "$ISSUE_TYPE: Issue Title (#$ISSUE_NUMBER)" \
  --body "Closes #$ISSUE_NUMBER" \
  --base main \
  --head $BRANCH_NAME
```

### Step 10: Update Issue and Dependencies

```bash
# Update issue status
gh issue edit $ISSUE_NUMBER --add-label "status:review" --remove-label "status:in-progress"

# Check if this unblocks other issues
gh issue list --label "blocked" --state open --json number,body | \
  grep -l "Depends on #$ISSUE_NUMBER"
# For each unblocked issue, remove blocked label
```

## Special Actions

### Deploy (--deploy)
```bash
vercel --prod --token=$VERCEL_TOKEN
```

### Test (--test)
```bash
npm test || pytest || echo "No test suite found"
```

## Examples

```bash
# Intelligent auto-selection
/work
# Finds: Issue #35 is unblocked and unblocks 3 other issues → selects it

# Work on specific issue
/work #42

# Deploy current work
/work --deploy

# Run tests
/work --test
```

## Intelligence Summary

The `/work` command intelligently:
- ✅ Checks sprint and project board
- ✅ Analyzes dependencies and blockers
- ✅ Prioritizes work that unblocks other work
- ✅ Considers work in progress
- ✅ Respects assignments and priorities
- ✅ Updates issue status throughout
- ✅ Manages dependency chains