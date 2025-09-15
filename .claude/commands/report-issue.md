---
allowed-tools: mcp__github(*), Read(*), Bash(*)
description: Quick issue creation using GitHub's web UI templates
argument-hint: [bug|feature|task|hotfix] "title"
---

# Report Issue

<!--
WHEN TO USE THIS COMMAND:
- Quick bug reports
- Simple feature requests  
- Task tracking
- When you don't need complex routing/assignment

WHEN NOT TO USE:
- Complex features needing agent orchestration (use /create-issue)
- Issues requiring sub-issues (use /create-issue)
- When you need Copilot auto-assignment (use /create-issue)

This command uses GitHub's actual issue templates from .github/ISSUE_TEMPLATE/
-->

## Context
- Current repository: !`gh repo view --json nameWithOwner -q .nameWithOwner`
- Current branch: !`git branch --show-current`

## Your Task

When user runs `/report-issue $ARGUMENTS`, follow these steps:

### Step 1: Parse Arguments

Parse the arguments to determine issue type and title:
```bash
# Extract type and title from arguments
ARGS="$ARGUMENTS"
TYPE=""
TITLE=""

# Check for type flags
if [[ "$ARGS" == bug* ]]; then
  TYPE="bug"
  TITLE="${ARGS#bug }"
elif [[ "$ARGS" == feature* ]]; then
  TYPE="feature"
  TITLE="${ARGS#feature }"
elif [[ "$ARGS" == task* ]]; then
  TYPE="task"
  TITLE="${ARGS#task }"
elif [[ "$ARGS" == hotfix* ]]; then
  TYPE="hotfix"
  TITLE="${ARGS#hotfix }"
else
  # No type specified, ask user
  echo "What type of issue?"
  echo "1) Bug - Something broken"
  echo "2) Feature - New functionality"
  echo "3) Task - Work item"
  echo "4) Hotfix - Emergency fix"
  read -p "Select (1-4): " CHOICE
  
  case $CHOICE in
    1) TYPE="bug";;
    2) TYPE="feature";;
    3) TYPE="task";;
    4) TYPE="hotfix";;
    *) echo "Invalid choice"; exit 1;;
  esac
  
  TITLE="$ARGS"
fi

echo "Creating $TYPE issue: $TITLE"
```

### Step 2: Get Repository Context

```bash
# Get repository owner and name
REPO_INFO=$(gh repo view --json owner,name 2>/dev/null)
if [ -z "$REPO_INFO" ]; then
  echo "Error: Not in a GitHub repository or gh CLI not configured"
  exit 1
fi

OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
REPO=$(echo "$REPO_INFO" | jq -r '.name')
```

### Step 3: Read Template and Gather Input

Based on the TYPE, read the appropriate template and ask for required fields:

#### For Bug Reports
If TYPE is "bug":
1. Read `.github/ISSUE_TEMPLATE/bug_report.yml`
2. Ask user for:
   - What's broken? (required)
   - Steps to reproduce (required)
   - Expected behavior (optional)
   - Actual behavior (optional)
   - Error logs (optional)

#### For Feature Requests
If TYPE is "feature":
1. Read `.github/ISSUE_TEMPLATE/feature_request.yml`
2. Ask user for:
   - Description (required)
   - Problem it solves (optional)
   - Proposed solution (optional)

#### For Tasks
If TYPE is "task":
1. Read `.github/ISSUE_TEMPLATE/task.yml`
2. Ask user for:
   - Description (required)
   - Tasks to complete (optional)

#### For Hotfixes
If TYPE is "hotfix":
1. Read `.github/ISSUE_TEMPLATE/hotfix.yml`
2. Ask user for:
   - What's critically broken? (required)
   - Immediate fix needed (required)

### Step 4: Create Issue Body

Format the responses into a proper issue body based on the template structure:

```markdown
# For Bug
## What's broken?
[User's response]

## Steps to Reproduce
[User's response]

## Expected Behavior
[User's response if provided]

## Actual Behavior
[User's response if provided]

## Error Logs
```
[User's response if provided]
```
```

### Step 5: Create the Issue

Use mcp__github__create_issue with:
- owner: $OWNER
- repo: $REPO
- title: Add appropriate prefix based on type
  - Bug: "[BUG]: $TITLE"
  - Feature: "[FEATURE]: $TITLE"
  - Task: "[TASK]: $TITLE"
  - Hotfix: "[HOTFIX]: $TITLE"
- body: The formatted content from Step 4
- labels: Based on type
  - bug → ["bug"]
  - feature → ["enhancement"]
  - task → ["task"]
  - hotfix → ["hotfix", "priority:high"]

### Step 6: Show Result

```bash
# Get the issue URL
ISSUE_URL=$(gh issue view $ISSUE_NUMBER --json url --jq .url)

echo "✅ Issue Created: #$ISSUE_NUMBER"
echo "📋 Type: $TYPE"
echo "🏷️ Labels: $(gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name' | tr '\n' ', ')"
echo "🔗 URL: $ISSUE_URL"
echo ""
echo "This is a simple issue without agent assignment."
echo "For complex features needing orchestration, use '/create-issue' instead."
```

## Key Differences from /create-issue

- **No complexity/size estimation** - Just create the issue
- **No agent assignment** - Simple issues for manual work
- **No sub-issues** - Single issue only
- **No milestone assignment** - Can be added manually later
- **Uses GitHub templates** - Consistent with web UI
- **Simpler workflow** - Fewer questions, faster creation

## Examples

```bash
/report-issue bug Login button not working on mobile
/report-issue feature Add dark mode toggle  
/report-issue task Update documentation
/report-issue hotfix Production API returning 500 errors
```