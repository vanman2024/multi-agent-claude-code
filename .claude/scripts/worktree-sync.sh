#!/bin/bash

# Worktree Sync Script - Smooth integration between worktrees and main branch
# Usage: ./worktree-sync.sh [command] [options]

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the main project directory
MAIN_PROJECT="/home/gotime2022/Projects/multi-agent-claude-code"
WORKTREE_BASE="/home/gotime2022/Projects/worktrees"

# Function to sync specific files from worktree to main
sync_files() {
    local worktree_name=$1
    local worktree_path="$WORKTREE_BASE/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Syncing files from worktree: $worktree_name${NC}"
    
    # Define files that should be synced
    local sync_patterns=(
        "todo-viewer/*.js"
        "todo-viewer/*.html"
        "todo-viewer/*.css"
        ".claude/scripts/*.sh"
        ".claude/commands/*.md"
        ".claude/hooks/*.sh"
    )
    
    for pattern in "${sync_patterns[@]}"; do
        # Use rsync to sync files matching pattern
        if ls $worktree_path/$pattern 2>/dev/null 1>&2; then
            echo -e "${GREEN}Syncing: $pattern${NC}"
            rsync -av --update "$worktree_path/$pattern" "$MAIN_PROJECT/$(dirname $pattern)/" 2>/dev/null || true
        fi
    done
    
    echo -e "${GREEN}✓ Files synced successfully${NC}"
}

# Function to merge worktree branch
merge_worktree() {
    local worktree_name=$1
    local worktree_path="$WORKTREE_BASE/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    # Get the branch name from worktree
    cd "$worktree_path"
    local branch_name=$(git branch --show-current)
    
    echo -e "${BLUE}Merging branch: $branch_name${NC}"
    
    # Switch to main project
    cd "$MAIN_PROJECT"
    
    # Ensure we're on main branch and up to date
    git checkout main
    git pull origin main
    
    # Fetch the worktree branch
    git fetch origin "$branch_name"
    
    # Merge the branch
    git merge "origin/$branch_name" --no-ff -m "Merge branch '$branch_name' from worktree"
    
    echo -e "${GREEN}✓ Branch merged successfully${NC}"
    echo -e "${YELLOW}Remember to push: git push origin main${NC}"
}

# Function to check differences between worktree and main
check_diff() {
    local worktree_name=$1
    local worktree_path="$WORKTREE_BASE/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Checking differences between worktree and main${NC}"
    
    # Key directories to check
    local dirs_to_check=(
        "todo-viewer"
        ".claude/scripts"
        ".claude/commands"
        ".claude/hooks"
    )
    
    for dir in "${dirs_to_check[@]}"; do
        if [ -d "$worktree_path/$dir" ] && [ -d "$MAIN_PROJECT/$dir" ]; then
            echo -e "\n${YELLOW}Differences in $dir:${NC}"
            diff -rq "$worktree_path/$dir" "$MAIN_PROJECT/$dir" 2>/dev/null | grep -v "Only in.*\.git" || echo "  No differences"
        fi
    done
}

# Function to setup port for worktree server
setup_worktree_port() {
    local worktree_name=$1
    local port=${2:-8081}
    local worktree_path="$WORKTREE_BASE/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    local server_file="$worktree_path/todo-viewer/server.js"
    
    if [ -f "$server_file" ]; then
        # Update the port in server.js
        sed -i "s/const PORT = .*/const PORT = process.env.PORT || $port;/" "$server_file"
        echo -e "${GREEN}✓ Updated server port to $port${NC}"
    else
        echo -e "${YELLOW}Warning: server.js not found in worktree${NC}"
    fi
}

# Function to list all worktrees
list_worktrees() {
    echo -e "${BLUE}Available worktrees:${NC}"
    if [ -d "$WORKTREE_BASE" ]; then
        for worktree in "$WORKTREE_BASE"/*; do
            if [ -d "$worktree" ]; then
                local name=$(basename "$worktree")
                cd "$worktree" 2>/dev/null && {
                    local branch=$(git branch --show-current)
                    local status=$(git status --porcelain | wc -l)
                    echo -e "  ${GREEN}$name${NC} (branch: $branch, uncommitted: $status)"
                }
            fi
        done
    else
        echo -e "${YELLOW}No worktrees found${NC}"
    fi
}

# Function to create PR from worktree
create_pr() {
    local worktree_name=$1
    local worktree_path="$WORKTREE_BASE/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    cd "$worktree_path"
    local branch_name=$(git branch --show-current)
    
    # Push the branch if needed
    git push -u origin "$branch_name"
    
    # Extract issue number from branch name (e.g., 155-todo-github-sync -> 155)
    local issue_num=$(echo "$branch_name" | grep -oE '^[0-9]+')
    
    if [ -n "$issue_num" ]; then
        # Create PR that closes the issue
        gh pr create --title "Implement features from Issue #$issue_num" \
                     --body "Closes #$issue_num" \
                     --base main
    else
        # Create PR without issue reference
        gh pr create --title "Changes from worktree: $worktree_name" \
                     --body "Changes implemented in worktree branch" \
                     --base main
    fi
    
    echo -e "${GREEN}✓ Pull request created${NC}"
}

# Main command handler
case "${1:-help}" in
    sync)
        sync_files "${2:-$(basename $(pwd))}"
        ;;
    merge)
        merge_worktree "${2:-$(basename $(pwd))}"
        ;;
    diff)
        check_diff "${2:-$(basename $(pwd))}"
        ;;
    port)
        setup_worktree_port "${2:-$(basename $(pwd))}" "${3:-8081}"
        ;;
    list)
        list_worktrees
        ;;
    pr)
        create_pr "${2:-$(basename $(pwd))}"
        ;;
    help|--help|-h)
        echo "Worktree Sync Tool - Smooth integration between worktrees and main branch"
        echo ""
        echo "Usage: $0 [command] [worktree-name] [options]"
        echo ""
        echo "Commands:"
        echo "  sync [name]  - Sync files from worktree to main (default: current dir name)"
        echo "  merge [name] - Merge worktree branch into main"
        echo "  diff [name]  - Check differences between worktree and main"
        echo "  port [name] [port] - Setup server port for worktree (default: 8081)"
        echo "  list         - List all available worktrees"
        echo "  pr [name]    - Create pull request from worktree"
        echo "  help         - Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 sync 155-todo-github-sync"
        echo "  $0 merge 155-todo-github-sync"
        echo "  $0 port 155-todo-github-sync 8082"
        echo "  $0 pr 155-todo-github-sync"
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        $0 help
        exit 1
        ;;
esac