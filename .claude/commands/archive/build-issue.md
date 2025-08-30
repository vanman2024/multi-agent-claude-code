---
allowed-tools: Task(*), Bash(*), Read(*), Write(*), TodoWrite(*), mcp__github(*), Edit(*), MultiEdit(*)
description: Build implementation for any GitHub issue (feature, bug, enhancement, etc.)
argument-hint: [issue-number]
---

# Build Issue Implementation

## Context
- Current branch: !`git branch --show-current`
- Repository: !`git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/'`

## Your Task

When user runs `/build-issue $ARGUMENTS`, implement the solution for the specified issue:

### Step 1: Get Issue Details

```bash
# Parse repository info
REPO_URL=$(git remote get-url origin)
REPO_INFO=$(echo $REPO_URL | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
OWNER=$(echo $REPO_INFO | cut -d'/' -f1)
REPO=$(echo $REPO_INFO | cut -d'/' -f2)

# Get issue details
ISSUE_NUMBER=$ARGUMENTS
```

Use mcp__github__get_issue to retrieve:
- Issue title, body, labels
- Issue type from labels (feature, bug, enhancement, etc.)
- Complexity and size from issue body

### Step 2: Checkout Feature Branch

```bash
# Fetch latest changes
git fetch origin

# Check if feature branch exists (created by automation)
BRANCH_NAME="feature/${ISSUE_NUMBER}-$(echo $ISSUE_TITLE | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)"

if git branch -r | grep "origin/$BRANCH_NAME"; then
  git checkout $BRANCH_NAME
  git pull origin $BRANCH_NAME
else
  # Create branch if automation didn't
  git checkout -b $BRANCH_NAME
fi
```

### Step 3: Determine Implementation Approach

Based on issue type and labels:

#### For Features:
Use Task tool with:
- subagent_type: "general-purpose"  
- description: "Implement feature from issue #${ISSUE_NUMBER}"
- prompt: Full issue content + implementation requirements

#### For Bugs:
Use Task tool with:
- subagent_type: "general-purpose"
- description: "Fix bug from issue #${ISSUE_NUMBER}"
- prompt: Bug description + reproduction steps + fix requirements

#### For Enhancements:
Use Task tool with:
- subagent_type: "refactor"
- description: "Enhance existing feature from issue #${ISSUE_NUMBER}"
- prompt: Current state + desired improvements

#### For Refactoring:
Use Task tool with:
- subagent_type: "code-refactorer"
- description: "Refactor code from issue #${ISSUE_NUMBER}"
- prompt: Refactoring goals + code quality requirements

### Step 4: Implementation Tasks

Create TodoWrite list based on issue requirements:
1. Analyze existing code
2. Implement changes
3. Add/update tests
4. Update documentation
5. Verify solution

Execute implementation based on issue type.

### Step 5: Testing & Validation

```bash
# Run tests if they exist
if [ -f "package.json" ] && grep -q "\"test\":" package.json; then
  npm test
fi

# Run linting
if [ -f "package.json" ] && grep -q "\"lint\":" package.json; then
  npm run lint
fi

# Type checking
if [ -f "tsconfig.json" ]; then
  npx tsc --noEmit
fi
```

### Step 6: Commit Changes

```bash
# Stage all changes
git add -A

# Create commit with issue reference
git commit -m "fix: Implement issue #${ISSUE_NUMBER}

- ${KEY_CHANGES}

Closes #${ISSUE_NUMBER}"
```

### Step 7: Push and Create PR

```bash
# Push branch
git push -u origin $BRANCH_NAME
```

Use mcp__github__create_pull_request:
```javascript
{
  owner: owner,
  repo: repo,
  title: `${issueType}: ${issueTitle} (closes #${ISSUE_NUMBER})`,
  head: branchName,
  base: "main",
  body: `## Summary
  
Implements #${ISSUE_NUMBER}

## Changes
- ${changes}

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project conventions
- [ ] Documentation updated
- [ ] No console.logs or debug code
`
}
```

### Step 8: Update Issue Status

Add comment to issue:
```javascript
mcp__github__add_issue_comment({
  owner: owner,
  repo: repo,
  issue_number: issueNumber,
  body: `🚀 Implementation complete! 

PR: #${prNumber}
Branch: ${branchName}

Please review the pull request.`
})
```

## Success Output

Provide summary:
```
✅ Issue #${ISSUE_NUMBER} Implementation Complete
📋 Type: ${issueType}
🌿 Branch: ${branchName}
🔗 PR: #${prNumber}

Next steps:
1. Review PR at ${prUrl}
2. Run tests in CI/CD
3. Merge when approved
```

## Important Notes
- Works with any issue type (feature, bug, enhancement, refactor, task)
- GitHub Actions handle project board updates automatically
- Complexity determines which agent/approach to use
- Always verify tests pass before creating PR