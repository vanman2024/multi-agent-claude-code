#!/bin/bash

# Worktree Status Display Script
# Shows all active worktrees and their current state

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                    WORKTREE STATUS                          ${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Get main branch status
echo -e "${GREEN}📍 MAIN BRANCH (Port 8080)${NC}"
cd /home/gotime2022/Projects/multi-agent-claude-code
BRANCH=$(git branch --show-current)
UNCOMMITTED=$(git status --porcelain | wc -l)
LAST_COMMIT=$(git log -1 --pretty=format:"%h %s" 2>/dev/null || echo "No commits")
echo "   Branch: $BRANCH"
echo "   Path: $(pwd)"
echo "   Uncommitted: $UNCOMMITTED files"
echo "   Last: $LAST_COMMIT"
echo ""

# Get worktree status
echo -e "${YELLOW}🌳 ACTIVE WORKTREES (Port 8081)${NC}"
WORKTREES=$(git worktree list --porcelain | grep "^worktree " | sed 's/worktree //')

if [ -z "$WORKTREES" ]; then
    echo "   No active worktrees"
else
    for WORKTREE_PATH in $WORKTREES; do
        # Skip main
        if [[ "$WORKTREE_PATH" == *"/multi-agent-claude-code" ]]; then
            continue
        fi
        
        if [ -d "$WORKTREE_PATH" ]; then
            cd "$WORKTREE_PATH" 2>/dev/null || continue
            
            BRANCH=$(git branch --show-current)
            UNCOMMITTED=$(git status --porcelain | wc -l)
            ISSUE_NUM=$(echo "$BRANCH" | grep -oE '^[0-9]+' || echo "N/A")
            LAST_COMMIT=$(git log -1 --pretty=format:"%h %s" 2>/dev/null || echo "No commits")
            
            echo ""
            echo -e "   ${BLUE}Worktree: $(basename $WORKTREE_PATH)${NC}"
            echo "   Issue: #$ISSUE_NUM"
            echo "   Branch: $BRANCH"
            echo "   Path: $WORKTREE_PATH"
            echo "   Uncommitted: $UNCOMMITTED files"
            echo "   Last: $LAST_COMMIT"
        fi
    done
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Tips:${NC}"
echo "  • Main development: http://localhost:8080"
echo "  • Worktree testing: http://localhost:8081"
echo "  • Switch worktrees: Stop server (Ctrl+C) and start in new worktree"
echo "  • Create worktree: ./.claude/scripts/safe-worktree.sh create <issue-num>"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"