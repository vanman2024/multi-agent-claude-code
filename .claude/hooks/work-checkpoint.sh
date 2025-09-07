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
    
    # Only remind if there are changes
    if [ "$changes" -gt 15 ]; then
        echo ""
        echo "📝 Reminder: You have $changes uncommitted changes on branch '$branch'"
        echo "   Last commit: $last_commit"
        echo "   Consider: /git commit"
        echo ""
    elif [ "$changes" -gt 5 ]; then
        echo ""
        echo "📝 Note: $changes uncommitted changes on '$branch'"
        echo ""
    fi
    
    # Check for unpushed commits
    unpushed=$(git log @{u}.. --oneline 2>/dev/null | wc -l || echo "0")
    if [ "$unpushed" -gt 3 ]; then
        echo "⬆️ You have $unpushed unpushed commits. Consider: /git push"
        echo ""
    fi
}

# Main execution
main() {
    # Only run reminders in interactive sessions
    # Skip in CI/CD or automated environments
    if [ -t 1 ]; then
        check_and_remind
    fi
}

# Run main function
main "$@"