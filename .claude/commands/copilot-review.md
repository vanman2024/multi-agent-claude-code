---
allowed-tools: mcp__github(*), Bash(*), TodoWrite(*)
description: Handle Copilot PRs - review, test, and merge workflow
argument-hint: [PR-number] [--quick|--thorough]
---

# Copilot Review - Handle Copilot-Created PRs

## Context
- Open PRs: !`gh pr list --state open --json number,title,author`
- Copilot PRs: !`gh pr list --state open --author app/github-copilot-agent --json number,title,isDraft`
- Recent merges: !`gh pr list --state merged --limit 3 --json number,title,mergedAt`

## Your Task

When user runs `/copilot-review $ARGUMENTS`, handle Copilot's PR with appropriate workflow.

### Step 1: Identify Copilot PR

First check if there's a Copilot PR to handle:

```bash
# Check for PR number in arguments or find latest Copilot PR
if [[ "$ARGUMENTS" =~ ^#?([0-9]+) ]]; then
  PR_NUMBER="${BASH_REMATCH[1]}"
  echo "Checking PR #$PR_NUMBER..."
else
  # Find most recent Copilot PR
  PR_NUMBER=$(gh pr list --state open --author app/github-copilot-agent --limit 1 --json number --jq '.[0].number')
  if [[ -z "$PR_NUMBER" ]]; then
    echo "No open Copilot PRs found"
    exit 1
  fi
  echo "Found Copilot PR #$PR_NUMBER"
fi

# Verify it's a Copilot PR
AUTHOR=$(gh pr view $PR_NUMBER --json author --jq .author.login)
if [[ "$AUTHOR" != "app/github-copilot-agent" ]]; then
  echo "⚠️ PR #$PR_NUMBER is not from Copilot (author: $AUTHOR)"
  echo "This command is for handling Copilot-created PRs"
  exit 1
fi
```

### Step 2: Check Current State & CI Status

```bash
# Get PR details
PR_DETAILS=$(gh pr view $PR_NUMBER --json state,isDraft,title,body,headRefName,checks)
STATE=$(echo "$PR_DETAILS" | jq -r .state)
IS_DRAFT=$(echo "$PR_DETAILS" | jq -r .isDraft)
BRANCH=$(echo "$PR_DETAILS" | jq -r .headRefName)
TITLE=$(echo "$PR_DETAILS" | jq -r .title)

echo "📋 PR #$PR_NUMBER: $TITLE"
echo "🌿 Branch: $BRANCH"
echo "📊 State: $STATE (Draft: $IS_DRAFT)"

# Check CI status
CI_PASSING=$(gh pr checks $PR_NUMBER --json name,status | jq -r 'all(.status == "COMPLETED" and .conclusion == "SUCCESS")')
if [[ "$CI_PASSING" == "true" ]]; then
  echo "✅ All CI checks passing"
else
  echo "⚠️ CI checks not all passing - review required"
  gh pr checks $PR_NUMBER
fi
```

### Step 3: Choose Workflow Option

Determine workflow based on flags or prompt user:

```bash
# Check for workflow flags
if [[ "$ARGUMENTS" =~ "--quick" ]]; then
  WORKFLOW="quick"
elif [[ "$ARGUMENTS" =~ "--thorough" ]]; then
  WORKFLOW="thorough"
else
  # Ask user to choose workflow
  echo ""
  echo "Choose workflow for Copilot PR #$PR_NUMBER:"
  echo ""
  echo "1️⃣ Quick Review + Merge (for simple/critical fixes)"
  echo "   - Quick visual review"
  echo "   - Run tests locally"
  echo "   - Merge if passing"
  echo ""
  echo "2️⃣ Thorough Claude Code Review (for complex changes)"
  echo "   - Full code review by Claude Code"
  echo "   - Test coverage analysis"
  echo "   - Security and performance checks"
  echo ""
  echo "Select (1 or 2):"
  # In slash command context, we'll default to thorough for safety
  WORKFLOW="thorough"
fi
```

### Step 4A: Option 1 - Quick Review + Merge

For critical bugs or simple changes:

```bash
if [[ "$WORKFLOW" == "quick" ]]; then
  echo "🚀 Starting Quick Review workflow..."
  
  # 1. Pull latest and checkout PR branch
  echo "📥 Fetching PR branch..."
  gh pr checkout $PR_NUMBER
  
  # 2. Quick review of changes
  echo "👀 Reviewing changes..."
  gh pr diff $PR_NUMBER --color always | head -100
  echo ""
  echo "📊 Files changed:"
  gh pr view $PR_NUMBER --json files --jq '.files[].path'
  
  # 3. Run tests locally
  echo "🧪 Running tests..."
  if [[ -f "package.json" ]]; then
    npm test 2>&1 | tail -20
    TEST_RESULT=$?
  elif [[ -f "requirements.txt" ]]; then
    pytest 2>&1 | tail -20
    TEST_RESULT=$?
  else
    echo "⚠️ No test command found"
    TEST_RESULT=0
  fi
  
  # 4. If tests pass, approve and merge
  if [[ $TEST_RESULT -eq 0 ]]; then
    echo "✅ Tests passing - approving PR"
    
    # Convert draft to ready if needed
    if [[ "$IS_DRAFT" == "true" ]]; then
      gh pr ready $PR_NUMBER
    fi
    
    # Approve the PR
    gh pr review $PR_NUMBER --approve --body "✅ Quick review completed. Tests passing, changes look good."
    
    # Merge
    echo "🔀 Merging PR..."
    gh pr merge $PR_NUMBER --squash --delete-branch
    
    # Switch back to main and pull
    git checkout main
    git pull origin main
    
    echo "✅ PR #$PR_NUMBER merged successfully!"
  else
    echo "❌ Tests failed - manual review required"
    gh pr comment $PR_NUMBER --body "⚠️ Quick review found test failures. Manual review required."
  fi
fi
```

### Step 4B: Option 2 - Thorough Claude Code Review

For complex changes requiring detailed review:

```bash
if [[ "$WORKFLOW" == "thorough" ]]; then
  echo "🔍 Starting Thorough Review workflow..."
  
  # Use TodoWrite to plan the review
  echo "Creating review checklist..."
  
  # 1. Checkout PR for local analysis
  echo "📥 Fetching PR branch for analysis..."
  gh pr checkout $PR_NUMBER
  
  # 2. Analyze the changes
  echo "📊 Analyzing PR changes..."
  FILES_CHANGED=$(gh pr view $PR_NUMBER --json files --jq '.files | length')
  ADDITIONS=$(gh pr view $PR_NUMBER --json additions --jq .additions)
  DELETIONS=$(gh pr view $PR_NUMBER --json deletions --jq .deletions)
  
  echo "Files changed: $FILES_CHANGED"
  echo "Lines added: $ADDITIONS"
  echo "Lines removed: $DELETIONS"
  
  # 3. Full code review
  echo "🔍 Performing detailed code review..."
  
  # List all changed files for review
  gh pr view $PR_NUMBER --json files --jq '.files[].path' > /tmp/changed_files.txt
  
  echo ""
  echo "Review checklist:"
  echo "□ Code follows project conventions"
  echo "□ No security vulnerabilities"
  echo "□ Proper error handling"
  echo "□ Tests included/updated"
  echo "□ Documentation updated"
  echo "□ Performance considerations"
  echo "□ No hardcoded values"
  echo "□ Follows DRY principle"
  
  # 4. Run comprehensive tests
  echo ""
  echo "🧪 Running comprehensive test suite..."
  
  # Run tests with coverage if available
  if [[ -f "package.json" ]] && grep -q "test:coverage" package.json; then
    npm run test:coverage 2>&1 | tail -30
    TEST_RESULT=$?
  elif [[ -f "package.json" ]]; then
    npm test 2>&1 | tail -30
    TEST_RESULT=$?
  elif [[ -f "requirements.txt" ]]; then
    pytest --cov 2>&1 | tail -30
    TEST_RESULT=$?
  else
    echo "⚠️ No test framework detected"
    TEST_RESULT=0
  fi
  
  # 5. Check for specific issues
  echo ""
  echo "🔒 Security and quality checks..."
  
  # Check for common issues
  ISSUES_FOUND=false
  
  # Check for console.logs in production code
  if grep -r "console.log" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --exclude-dir=node_modules --exclude-dir=test .; then
    echo "⚠️ Found console.log statements"
    ISSUES_FOUND=true
  fi
  
  # Check for TODO comments
  if grep -r "TODO\|FIXME\|XXX" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --exclude-dir=node_modules .; then
    echo "⚠️ Found TODO/FIXME comments"
    ISSUES_FOUND=true
  fi
  
  # 6. Provide detailed feedback
  echo ""
  echo "📝 Preparing review feedback..."
  
  if [[ $TEST_RESULT -eq 0 ]] && [[ "$ISSUES_FOUND" == "false" ]]; then
    # All checks passed
    echo "✅ All checks passed!"
    
    # Convert draft to ready
    if [[ "$IS_DRAFT" == "true" ]]; then
      gh pr ready $PR_NUMBER
    fi
    
    # Approve with detailed feedback
    gh pr review $PR_NUMBER --approve --body "✅ **Thorough Review Completed**

**Review Summary:**
- 📊 Files changed: $FILES_CHANGED
- ➕ Lines added: $ADDITIONS
- ➖ Lines removed: $DELETIONS

**Checks Passed:**
✅ Code follows project conventions
✅ No security vulnerabilities found
✅ Proper error handling in place
✅ Tests passing with good coverage
✅ No console.logs or debug code
✅ No unresolved TODOs

**Recommendation:** Ready to merge"
    
    # Ask if should merge
    echo ""
    echo "✅ Review complete - PR approved"
    echo "Would you like to merge now? (Run: gh pr merge $PR_NUMBER --squash --delete-branch)"
    
  else
    # Issues found - request changes
    echo "⚠️ Issues found during review"
    
    REVIEW_BODY="⚠️ **Thorough Review - Changes Requested**

**Review Summary:**
- 📊 Files changed: $FILES_CHANGED
- ➕ Lines added: $ADDITIONS
- ➖ Lines removed: $DELETIONS

**Issues Found:**"
    
    if [[ $TEST_RESULT -ne 0 ]]; then
      REVIEW_BODY="$REVIEW_BODY
❌ Tests are failing - please fix before merge"
    fi
    
    if [[ "$ISSUES_FOUND" == "true" ]]; then
      REVIEW_BODY="$REVIEW_BODY
⚠️ Code quality issues detected (console.logs, TODOs, etc.)"
    fi
    
    REVIEW_BODY="$REVIEW_BODY

Please address these issues and request another review."
    
    gh pr review $PR_NUMBER --request-changes --body "$REVIEW_BODY"
    
    echo "📝 Review feedback posted to PR #$PR_NUMBER"
  fi
  
  # Return to main branch
  git checkout main
fi
```

### Step 5: Post-Merge Actions

After merging (either workflow):

```bash
# Sync local main with remote
echo "🔄 Syncing local repository..."
git checkout main
git pull origin main

# Check for any follow-up issues
RELATED_ISSUE=$(gh pr view $PR_NUMBER --json body --jq '.body' | grep -oE "Closes #[0-9]+" | grep -oE "[0-9]+")
if [[ ! -z "$RELATED_ISSUE" ]]; then
  echo "✅ Issue #$RELATED_ISSUE automatically closed by PR merge"
fi

# Update project board if needed
echo "📋 Checking project board status..."
# Project board updates happen automatically via GitHub Actions
```

## Usage Examples

```bash
# Handle latest Copilot PR with choice prompt
/copilot-review

# Handle specific Copilot PR
/copilot-review #143

# Quick review and merge (for critical fixes)
/copilot-review #143 --quick

# Thorough review (for complex changes)
/copilot-review #143 --thorough

# Handle latest Copilot PR with quick merge
/copilot-review --quick
```

## Important Notes

- **Quick workflow** is for simple, critical fixes where CI is passing
- **Thorough workflow** is for complex changes needing detailed review
- Always pull latest main after merging to stay in sync
- If Copilot's PR has conflicts, resolve locally before merging
- Project board updates happen automatically via GitHub Actions
- Use this command specifically for Copilot-created PRs
- For regular PR reviews from other authors, request Copilot review via GitHub UI
- The workflows handle draft → ready conversion automatically when needed