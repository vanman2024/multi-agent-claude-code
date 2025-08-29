---
allowed-tools: mcp__github(*), Bash(*)
description: Request Copilot code review on a pull request
argument-hint: [PR-number]
---

# Copilot Review - Request AI Code Review

## Context
- Open PRs: !`gh pr list --state open --json number,title,author`
- Recent PRs: !`gh pr list --state all --limit 5 --json number,title,state`

## Your Task

When user runs `/copilot-review $ARGUMENTS`, request Copilot review on PR.

### Step 1: Determine PR Number

```bash
if [[ "$ARGUMENTS" =~ ^#?([0-9]+) ]]; then
  PR_NUMBER="${BASH_REMATCH[1]}"
else
  # Get most recent PR
  PR_NUMBER=$(gh pr list --state open --limit 1 --json number --jq '.[0].number')
  echo "No PR specified, using most recent: #$PR_NUMBER"
fi
```

### Step 2: Check PR Status

```bash
# Get PR details
gh pr view $PR_NUMBER --json state,isDraft,author,labels

# Check if it's ready for review
STATE=$(gh pr view $PR_NUMBER --json state --jq .state)
IS_DRAFT=$(gh pr view $PR_NUMBER --json isDraft --jq .isDraft)

if [[ "$STATE" != "OPEN" ]]; then
  echo "PR #$PR_NUMBER is not open (state: $STATE)"
  exit 1
fi

if [[ "$IS_DRAFT" == "true" ]]; then
  echo "PR #$PR_NUMBER is still a draft"
  echo "Convert to ready for review first"
  exit 1
fi
```

### Step 3: Request Copilot Review

Use mcp__github__request_copilot_review to trigger review:
- This assigns Copilot to review the PR
- Copilot will analyze code quality, bugs, security issues
- Will provide actionable feedback

### Step 4: Add Review Instructions

```bash
# Add comment with specific review focus areas
gh pr comment $PR_NUMBER --body "🤖 **Copilot Review Requested**

Please review for:
- ✅ Code quality and best practices
- 🐛 Potential bugs or edge cases
- 🔒 Security vulnerabilities
- ⚡ Performance issues
- 📝 Missing tests or documentation
- 🎨 Code style consistency

Focus areas:
$(# Check what type of changes
if gh pr view $PR_NUMBER --json files --jq '.files[].path' | grep -q "test"; then
  echo "- Test coverage and quality"
fi
if gh pr view $PR_NUMBER --json files --jq '.files[].path' | grep -q "api"; then
  echo "- API design and validation"
fi
if gh pr view $PR_NUMBER --json files --jq '.files[].path' | grep -q -E "\.(tsx?|jsx?)$"; then
  echo "- Frontend component patterns"
fi
if gh pr view $PR_NUMBER --json files --jq '.files[].path' | grep -q "sql"; then
  echo "- Database query optimization"
fi)

Copilot will provide feedback shortly."
```

### Step 5: Track Review Status

```bash
# Add label to track Copilot review
gh pr edit $PR_NUMBER --add-label "copilot-review-requested"

# Check if CI is passing
CI_STATUS=$(gh pr checks $PR_NUMBER --json name,status)
echo "CI Status: $CI_STATUS"

# Notify user
echo "✅ Copilot review requested for PR #$PR_NUMBER"
echo "🔗 URL: $(gh pr view $PR_NUMBER --json url --jq .url)"
echo ""
echo "Copilot will:"
echo "- Review code quality"
echo "- Check for bugs and security issues"
echo "- Suggest improvements"
echo "- Verify test coverage"
```

## Additional Capabilities

### Request Specific Review Type

```bash
# For security-focused review
if [[ "$ARGUMENTS" =~ "--security" ]]; then
  echo "Requesting security-focused review..."
  # Add security review instructions
fi

# For performance review
if [[ "$ARGUMENTS" =~ "--performance" ]]; then
  echo "Requesting performance review..."
  # Add performance review instructions
fi

# For test review
if [[ "$ARGUMENTS" =~ "--tests" ]]; then
  echo "Requesting test coverage review..."
  # Add test review instructions
fi
```

## Examples

```bash
# Review specific PR
/copilot-review 42
/copilot-review #42

# Review most recent PR
/copilot-review

# Security-focused review
/copilot-review 42 --security

# Performance review
/copilot-review 42 --performance
```

## Important Notes

- Copilot review requires the PR to be ready (not draft)
- CI should ideally be passing before review
- Copilot can review any size PR but works best on focused changes
- Review feedback appears as PR comments
- Can request multiple reviews as code changes