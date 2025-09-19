#!/bin/bash

# work-checkpoint.sh - Runs when Claude Code session stops (Stop event)
# Provides work continuation safety and state preservation

set -euo pipefail

# Auto-stash functionality for large uncommitted work
auto_stash_if_needed() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        return 0
    fi
    
    # Count uncommitted changes
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    
    # Only create stash if significant uncommitted work exists (>15 files) and no recent stash
    if [ "$changes" -gt 15 ]; then
        # Check if there's a recent stash (within last 10 minutes)
        recent_stash=$(git stash list --since="10 minutes ago" 2>/dev/null | head -1)
        
        if [ -z "$recent_stash" ]; then
            echo ""
            echo "💾 Auto-stashing large uncommitted work for safety..."
            echo "   Uncommitted files: $changes"
            
            # Create descriptive stash message
            current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
            stash_msg="Auto-checkpoint: $current_branch - $(date +%Y%m%d-%H%M%S)"
            
            if git stash push -m "$stash_msg" 2>/dev/null; then
                echo "   ✅ Work stashed successfully"
                echo "   To restore: git stash pop"
            else
                echo "   ⚠️ Could not stash work"
            fi
            echo ""
        fi
    fi
}

# Show current status for continuity
show_status() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        uncommitted=$(git status --porcelain 2>/dev/null | wc -l)
        
        if [ "$uncommitted" -gt 0 ] || [ "$(git stash list 2>/dev/null | wc -l)" -gt 0 ]; then
            echo ""
            echo "📋 Work Status Checkpoint"
            echo "   Branch: $current_branch"
            [ "$uncommitted" -gt 0 ] && echo "   Uncommitted: $uncommitted files"
            
            stash_count=$(git stash list 2>/dev/null | wc -l)
            [ "$stash_count" -gt 0 ] && echo "   Stashes: $stash_count available"
            echo ""
        fi
    fi
}

# Main execution
main() {
    # Perform auto-stash if needed
    auto_stash_if_needed
    
    # Show status for next session
    show_status
    
    # Output empty JSON for Claude Code (hooks must output valid JSON)
    echo '{}'
}

# Run main function
main "$@"