#!/bin/bash

# Safe Worktree Creation Script
# This ensures worktrees ALWAYS start from latest main

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to create safe worktree
create_safe_worktree() {
    local issue_number=$1
    
    if [ -z "$issue_number" ]; then
        echo -e "${RED}Error: Please provide an issue number${NC}"
        echo "Usage: $0 create <issue-number>"
        exit 1
    fi
    
    echo -e "${BLUE}Creating SAFE worktree for issue #$issue_number${NC}"
    
    # 1. First, ensure main is up to date
    echo -e "${YELLOW}Step 1: Updating main branch...${NC}"
    git checkout main
    git pull origin main
    
    # 2. Create the branch from CURRENT main (not from issue creation point)
    local branch_name="${issue_number}-worktree"
    echo -e "${YELLOW}Step 2: Creating branch from latest main...${NC}"
    git checkout -b "$branch_name"
    
    # 3. Push the branch
    echo -e "${YELLOW}Step 3: Pushing branch...${NC}"
    git push -u origin "$branch_name"
    
    # 4. Create worktree
    local worktree_path="/home/gotime2022/Projects/worktrees/$branch_name"
    echo -e "${YELLOW}Step 4: Creating worktree at $worktree_path...${NC}"
    git worktree add "$worktree_path" "$branch_name"
    
    # 5. Setup the worktree
    cd "$worktree_path"
    
    # 6. Ensure package.json exists for auto-reload
    if [ -f "todo-viewer/server.js" ] && [ ! -f "todo-viewer/package.json" ]; then
        echo -e "${YELLOW}Step 5: Setting up auto-reload...${NC}"
        cp /home/gotime2022/Projects/multi-agent-claude-code/todo-viewer/package.json todo-viewer/ 2>/dev/null || true
    fi
    
    # 7. Set correct port (ALWAYS 8081 for worktrees)
    local port=8081  # All worktrees use 8081
    echo -e "${YELLOW}Step 6: Setting port to $port (standard worktree port)...${NC}"
    if [ -f "todo-viewer/server.js" ]; then
        sed -i "s/const PORT = .*/const PORT = process.env.PORT || $port;/" todo-viewer/server.js
    fi
    
    echo -e "${GREEN}✅ SAFE worktree created successfully!${NC}"
    echo -e "${GREEN}Location: $worktree_path${NC}"
    echo -e "${GREEN}Branch: $branch_name${NC}"
    echo -e "${GREEN}Port: $port${NC}"
    echo ""
    echo -e "${BLUE}To start working:${NC}"
    echo "  cd $worktree_path"
    echo "  cd todo-viewer && npm run dev:$port"
    echo ""
    echo -e "${YELLOW}⚠️  This worktree has the LATEST code from main${NC}"
}

# Function to verify worktree is up to date
verify_worktree() {
    local worktree_name=$1
    local worktree_path="/home/gotime2022/Projects/worktrees/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    cd "$worktree_path"
    
    # Check if behind main
    git fetch origin main
    local behind=$(git rev-list --count HEAD..origin/main)
    
    if [ "$behind" -gt 0 ]; then
        echo -e "${RED}⚠️  WARNING: Worktree is $behind commits behind main!${NC}"
        echo -e "${YELLOW}Run: git merge origin/main${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Worktree is up to date with main${NC}"
        return 0
    fi
}

# Function to safely merge main
safe_merge_main() {
    local worktree_name=$1
    local worktree_path="/home/gotime2022/Projects/worktrees/$worktree_name"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED}Error: Worktree $worktree_name not found${NC}"
        exit 1
    fi
    
    cd "$worktree_path"
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${RED}Error: You have uncommitted changes${NC}"
        echo -e "${YELLOW}Please commit or stash your changes first${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Safely merging main into worktree...${NC}"
    git fetch origin main
    git merge origin/main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully merged main${NC}"
    else
        echo -e "${RED}⚠️  Merge conflicts detected. Please resolve them.${NC}"
    fi
}

# Main command handler
case "${1:-help}" in
    create)
        create_safe_worktree "$2"
        ;;
    verify)
        verify_worktree "${2:-$(basename $(pwd))}"
        ;;
    merge)
        safe_merge_main "${2:-$(basename $(pwd))}"
        ;;
    help|--help|-h)
        echo "Safe Worktree Tool - Prevents common worktree issues"
        echo ""
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  create <issue-num>  - Create worktree from LATEST main (not issue creation point)"
        echo "  verify [name]       - Check if worktree is up to date with main"
        echo "  merge [name]        - Safely merge main into worktree"
        echo "  help                - Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 create 156       # Creates worktree for issue 156 from LATEST main"
        echo "  $0 verify           # Check current worktree status"
        echo "  $0 merge            # Merge latest main into current worktree"
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        $0 help
        exit 1
        ;;
esac