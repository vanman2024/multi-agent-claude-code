#!/bin/bash
# Hook: Load project context on session start
# Event: SessionStart
# Purpose: Inject project state and context when Claude Code starts

# Get current directory
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Check if we're in a git repository
if [ ! -d "$PROJECT_DIR/.git" ]; then
  echo "Not in a git repository"
  exit 0
fi

# Get recent commits
RECENT_COMMITS=$(git log --oneline -n 5 2>/dev/null || echo "No recent commits")

# Get current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Get assigned GitHub issues (if gh is available)
ASSIGNED_ISSUES=""
if command -v gh &> /dev/null; then
  ASSIGNED_ISSUES=$(gh issue list --assignee @me --state open --limit 5 2>/dev/null || echo "")
fi

# Get open PRs
OPEN_PRS=""
if command -v gh &> /dev/null; then
  OPEN_PRS=$(gh pr list --author @me --state open --limit 5 2>/dev/null || echo "")
fi

# Check current issue complexity if on a feature branch
COMPLEXITY_HINT=""
BRANCH_ISSUE=$(echo "$CURRENT_BRANCH" | grep -oE '[0-9]+' | head -1)
if [ -n "$BRANCH_ISSUE" ]; then
  ISSUE_BODY=$(gh issue view "$BRANCH_ISSUE" --json body -q .body 2>/dev/null || echo "")
  if echo "$ISSUE_BODY" | grep -q "Complexity: [3-5]"; then
    COMPLEXITY_HINT="
### 💭 Complex Task Detected
This appears to be a complex task. Consider:
- Using sequential thinking for structured analysis
- Breaking down the problem into smaller steps
- Taking time to understand all dependencies"
  fi
fi

# Build context output
CONTEXT="## Project Context Loaded

### Current Git State
- Branch: $CURRENT_BRANCH
- Recent Commits:
$RECENT_COMMITS

### Your Assigned Issues
${ASSIGNED_ISSUES:-No assigned issues}

### Your Open PRs
${OPEN_PRS:-No open PRs}
$COMPLEXITY_HINT
### Project Guidelines
- Run tests before pushing: npm test or pytest
- Use conventional commits: feat:, fix:, docs:, chore:
- Check linting: npm run lint
- Hooks are active - use Ctrl+R to see execution
"

# Output as JSON for SessionStart
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "$CONTEXT"
  }
}
EOF

exit 0