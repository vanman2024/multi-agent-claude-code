#!/bin/bash

# save-work-state.sh - Runs when session ends (SessionEnd event)
# Provides safety net for uncommitted work and saves work state

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORK_JOURNAL="$PROJECT_ROOT/.claude/work-journal.json"

# Save work state for next session
save_work_state() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        exit 0
    fi
    
    # Get current branch
    branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    
    # Count uncommitted changes
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    
    # Get unpushed commits
    unpushed=$(git log @{u}.. --oneline 2>/dev/null | wc -l || echo "0")
    
    # Get last commit
    last_commit=$(git log -1 --oneline 2>/dev/null || echo "no commits")
    
    # Save only if there's work to preserve
    if [ "$changes" -gt 0 ] || [ "$unpushed" -gt 0 ]; then
        # Create or update work journal
        timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        
        # Initialize journal if it doesn't exist
        if [ ! -f "$WORK_JOURNAL" ]; then
            echo '{"entries": []}' > "$WORK_JOURNAL"
        fi
        
        # Check if journal has old format and convert it
        if grep -q '"last_session"' "$WORK_JOURNAL" 2>/dev/null; then
            echo '{"entries": []}' > "$WORK_JOURNAL"
        fi
        
        # Create session end entry
        end_entry=$(cat <<EOF
{
    "timestamp": "$timestamp",
    "event": "session_end",
    "branch": "$branch",
    "uncommitted": $changes,
    "unpushed": $unpushed,
    "last_commit": "$last_commit"
}
EOF
        )
        
        # Append to journal (keep last 100 entries)
        cat "$WORK_JOURNAL" | jq --argjson entry "$end_entry" '.entries = ([$entry] + .entries)[0:100]' > "$WORK_JOURNAL.tmp"
        mv "$WORK_JOURNAL.tmp" "$WORK_JOURNAL"
        
        # Show session summary
        echo ""
        echo "📋 Session Summary Saved"
        echo "   Branch: $branch"
        if [ "$changes" -gt 0 ]; then
            echo "   ⚠️ Uncommitted changes: $changes files"
            echo "   Run '/git status' when you return to see details"
        fi
        if [ "$unpushed" -gt 0 ]; then
            echo "   ⬆️ Unpushed commits: $unpushed"
            echo "   Run '/git push' when ready to sync"
        fi
        echo ""
        echo "Work journal saved to .claude/work-journal.json"
    fi
}

# Emergency stash if critical
emergency_stash() {
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
    # Save work state
    save_work_state
    
    # Check for emergency conditions
    emergency_stash
    
    # Output empty JSON for Claude Code (hooks must output valid JSON)
    echo '{}'
}

# Run main function
main "$@"