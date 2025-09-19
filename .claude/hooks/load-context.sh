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

# Previous session info (simplified without journal)
PREVIOUS_SESSION=""

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

# Get todos summary for display
TODOS_SUMMARY=""
if [ -f "$PYTHON_MANAGER" ]; then
  # Get todos stats from Python manager
  TODOS_STATS=$(python3 "$PYTHON_MANAGER" --project "$PROJECT_DIR" stats 2>/dev/null | grep -E "Completed:|In Progress:|Pending:" || echo "")
  if [ -n "$TODOS_STATS" ]; then
    TODOS_SUMMARY="
### 📋 Active Todos
$TODOS_STATS"
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
$TODOS_SUMMARY

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

# Show existing todos from previous sessions
TODO_DIR="$HOME/.claude/todos"
PROJECT_HASH=$(echo "$PROJECT_DIR" | sed 's/\//-/g')
PROJECT_SESSIONS_DIR="$HOME/.claude/projects/$PROJECT_HASH"

# Find todo files that belong to this project
if [ -d "$PROJECT_SESSIONS_DIR" ]; then
  # Get list of session IDs for this project
  SESSION_IDS=$(ls "$PROJECT_SESSIONS_DIR"/*.jsonl 2>/dev/null | xargs -I {} basename {} .jsonl | head -5)
  
  for SESSION_ID in $SESSION_IDS; do
    TODO_FILE="$TODO_DIR/${SESSION_ID}.json"
    if [ -f "$TODO_FILE" ] && [ -s "$TODO_FILE" ]; then
      TODO_COUNT=$(jq 'length' "$TODO_FILE" 2>/dev/null || echo 0)
      if [ "$TODO_COUNT" -gt 0 ]; then
        echo "" >&2
        echo "### 📋 Recent Todos (from previous sessions)" >&2
        jq -r '.[] | "- [\(.status | .[0:1] | ascii_upcase)] \(.content)"' "$TODO_FILE" 2>/dev/null | head -10 >&2
        COMPLETED=$(jq '[.[] | select(.status == "completed")] | length' "$TODO_FILE" 2>/dev/null || echo 0)
        PENDING=$(jq '[.[] | select(.status == "pending")] | length' "$TODO_FILE" 2>/dev/null || echo 0) 
        IN_PROGRESS=$(jq '[.[] | select(.status == "in_progress")] | length' "$TODO_FILE" 2>/dev/null || echo 0)
        echo "Total: $TODO_COUNT (✅ $COMPLETED completed, 🔄 $IN_PROGRESS in progress, ⏳ $PENDING pending)" >&2
        echo "" >&2
        break # Only show first session with todos
      fi
    fi
  done
fi

PYTHON_MANAGER="$PROJECT_DIR/.claude/scripts/todo-manager.py"
if [ -f "$PYTHON_MANAGER" ]; then
  # Just register the session
  echo "✅ Session registered with project" >&2
else
  # Fallback to old method if Python manager doesn't exist
  TODO_DIR="$HOME/.claude/todos"
  PROJECT_HASH=$(echo "$PROJECT_DIR" | sed 's/\//-/g')
  PROJECT_SESSIONS_DIR="$HOME/.claude/projects/$PROJECT_HASH"

  if [ -d "$PROJECT_SESSIONS_DIR" ]; then
    # Get the most recent session file
    RECENT_SESSION=$(ls -t "$PROJECT_SESSIONS_DIR"/*.jsonl 2>/dev/null | head -1)
    
    if [ -f "$RECENT_SESSION" ]; then
      SESSION_ID=$(basename "$RECENT_SESSION" .jsonl)
      PREVIOUS_TODO_FILE="$TODO_DIR/${SESSION_ID}.json"
      
      if [ -f "$PREVIOUS_TODO_FILE" ]; then
        TODO_COUNT=$(jq 'length' "$PREVIOUS_TODO_FILE" 2>/dev/null || echo 0)
        
        if [ "$TODO_COUNT" -gt 0 ]; then
          # Find the current session's todo file (most recently modified)
          CURRENT_TODO=$(ls -t "$TODO_DIR"/*.json 2>/dev/null | head -1)
          
          if [ -f "$CURRENT_TODO" ] && [ "$CURRENT_TODO" != "$PREVIOUS_TODO_FILE" ]; then
            # Check if current file is empty or very new (less than 1 minute old)
            CURRENT_COUNT=$(jq 'length' "$CURRENT_TODO" 2>/dev/null || echo 0)
            FILE_AGE=$(( $(date +%s) - $(stat -c %Y "$CURRENT_TODO" 2>/dev/null || echo 0) ))
            
            if [ "$CURRENT_COUNT" -eq 0 ] || [ "$FILE_AGE" -lt 60 ]; then
              # Copy todos from previous session to current
              cp "$PREVIOUS_TODO_FILE" "$CURRENT_TODO"
              
              # Add an anchor todo to prevent TodoWrite from clearing the file
              jq '. + [{"content": "📌 Session anchor (keeps todos visible)", "status": "pending", "activeForm": "Maintaining session"}]' \
                 "$CURRENT_TODO" > "${CURRENT_TODO}.tmp" && mv "${CURRENT_TODO}.tmp" "$CURRENT_TODO"
              
              echo "✅ Loaded $TODO_COUNT todos from previous session" >&2
            fi
          fi
        fi
      fi
    fi
  fi
fi

# Register this session
bash "$(dirname "$0")/register-session.sh" 2>/dev/null

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