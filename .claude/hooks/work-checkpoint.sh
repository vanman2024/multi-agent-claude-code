#!/bin/bash

# work-checkpoint.sh - Runs after Claude finishes responding (Stop event)
# Provides gentle reminders about uncommitted work at natural pause points

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

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
    
    # Output as JSON for Claude Code if we have a message
    if [ -n "$MESSAGE" ]; then
        cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "$MESSAGE"
  }
}
EOF
    fi
}

# Main execution
main() {
    check_and_remind
}

# Run main function
main "$@"