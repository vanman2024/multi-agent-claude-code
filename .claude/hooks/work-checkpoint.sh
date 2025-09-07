#!/bin/bash

# work-checkpoint.sh - Runs after Claude finishes responding (Stop event)
# Provides gentle reminders about uncommitted work at natural pause points

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORK_JOURNAL="$PROJECT_ROOT/.claude/work-journal.json"

# Update work journal silently
update_work_journal() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        return 0
    fi
    
    # Get current state
    branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    unpushed=$(git log @{u}.. --oneline 2>/dev/null | wc -l || echo "0")
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    recent_commits=$(git log --oneline -5 2>/dev/null || echo "")
    
    # Update journal silently
    cat > "$WORK_JOURNAL.tmp" <<EOF
{
    "last_session": {
        "timestamp": "$timestamp",
        "branch": "$branch",
        "uncommitted_changes": $changes,
        "unpushed_commits": $unpushed,
        "recent_commits": [
$(echo "$recent_commits" | sed 's/^/            "/; s/$/",/' | sed '$ s/,$//')
        ],
        "work_summary": "Session active with $changes uncommitted changes and $unpushed unpushed commits on branch '$branch'"
    }
}
EOF
    
    # Move temp file to actual journal
    mv -f "$WORK_JOURNAL.tmp" "$WORK_JOURNAL" 2>/dev/null || true
}

# Only show reminders if we have significant changes
check_and_remind() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        exit 0
    fi
    
    # Count uncommitted changes
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    
    # Get last commit time
    last_commit=$(git log -1 --format="%cr" 2>/dev/null || echo "never")
    
    # Get current branch
    branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    
    # Build reminder message
    MESSAGE=""
    
    # Only remind if there are changes
    if [ "$changes" -gt 15 ]; then
        MESSAGE="📝 Reminder: You have $changes uncommitted changes on branch '$branch'
   Last commit: $last_commit
   Consider: /git commit"
    elif [ "$changes" -gt 5 ]; then
        MESSAGE="📝 Note: $changes uncommitted changes on '$branch'"
    fi
    
    # Check for unpushed commits
    unpushed=$(git log @{u}.. --oneline 2>/dev/null | wc -l || echo "0")
    if [ "$unpushed" -gt 3 ]; then
        if [ -n "$MESSAGE" ]; then
            MESSAGE="$MESSAGE
⬆️ You have $unpushed unpushed commits. Consider: /git push"
        else
            MESSAGE="⬆️ You have $unpushed unpushed commits. Consider: /git push"
        fi
    fi
    
    # Update work journal periodically (every Stop event)
    update_work_journal
    
    # Output as JSON for Claude Code if we have a message
    if [ -n "$MESSAGE" ]; then
        # Escape the message for JSON
        ESCAPED_MESSAGE=$(echo "$MESSAGE" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
        cat <<EOF
{
  "continue": true,
  "systemMessage": "$ESCAPED_MESSAGE"
}
EOF
    else
        # Must output valid JSON even when there's no message
        echo '{}'
    fi
}

# Main execution
main() {
    check_and_remind
}

# Run main function
main "$@"