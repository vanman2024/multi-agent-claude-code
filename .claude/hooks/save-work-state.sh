#!/bin/bash

# save-work-state.sh - Runs when session ends (SessionEnd event)
# Provides safety net for uncommitted work

set -euo pipefail

# Emergency stash if critical
emergency_stash() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        exit 0
    fi
    
    # Only stash if there are many changes and no stash exists
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    
    if [ "$changes" -gt 30 ]; then
        echo ""
        echo "🚨 Large amount of uncommitted work detected!"
        echo "   Creating emergency stash for safety..."
        git stash push -m "Emergency stash: Session ended $(date +%Y%m%d-%H%M%S)" || true
        echo "   Use 'git stash list' to see stashes when you return"
        echo ""
    fi
}

# Main execution
main() {
    # Check for emergency conditions
    emergency_stash
    
    # Output empty JSON for Claude Code (hooks must output valid JSON)
    echo '{}'
}

# Run main function
main "$@"