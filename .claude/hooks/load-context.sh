#!/bin/bash
# Hook: Load project context on session start
# Event: SessionStart
# Purpose: Inject project state and context when Claude Code starts
# Enhanced version with work journal integration

# Get current directory
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
WORK_JOURNAL="$PROJECT_DIR/.claude/work-journal.json"

# Check if we're in a git repository
if [ ! -d "$PROJECT_DIR/.git" ]; then
  echo "Not in a git repository"
  exit 0
fi

# Get recent commits
RECENT_COMMITS=$(git log --oneline -n 5 2>/dev/null || echo "No recent commits")

# Get current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Load previous session info if available
PREVIOUS_SESSION=""
if [ -f "$WORK_JOURNAL" ]; then
  LAST_BRANCH=$(jq -r '.last_session.branch // ""' "$WORK_JOURNAL" 2>/dev/null)
  LAST_CHANGES=$(jq -r '.last_session.uncommitted_changes // 0' "$WORK_JOURNAL" 2>/dev/null)
  LAST_UNPUSHED=$(jq -r '.last_session.unpushed_commits // 0' "$WORK_JOURNAL" 2>/dev/null)
  
  if [ -n "$LAST_BRANCH" ] && [ "$LAST_BRANCH" != "null" ]; then
    PREVIOUS_SESSION="
### 📚 Previous Session
- Last branch: $LAST_BRANCH"
    
    if [ "$LAST_CHANGES" -gt 0 ]; then
      PREVIOUS_SESSION="$PREVIOUS_SESSION
- ⚠️ Had $LAST_CHANGES uncommitted changes"
    fi
    
    if [ "$LAST_UNPUSHED" -gt 0 ]; then
      PREVIOUS_SESSION="$PREVIOUS_SESSION
- ⬆️ Had $LAST_UNPUSHED unpushed commits"
    fi
  fi
fi

# Check for stashes
STASH_COUNT=$(git stash list 2>/dev/null | wc -l)
STASH_INFO=""
if [ "$STASH_COUNT" -gt 0 ]; then
  STASH_INFO="
### 📦 Stashed Work
You have $STASH_COUNT stashed changes. Use 'git stash list' to review."
fi

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
$PREVIOUS_SESSION
$STASH_INFO

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