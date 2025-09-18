#!/bin/bash
# Git Commit Helper Script
#
# PURPOSE: Generates standardized commit messages following project conventions
# USAGE: ./git-commit-helper.sh [--help]
# PART OF: Git workflow automation
# CONNECTS TO: Development workflow, used by all agents for consistent commits
#
# This script helps create commit messages that follow the project's conventional
# commit format with proper agent attribution and task references.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Git Commit Helper${NC}"
echo "===================="

# Check git status
echo -e "\n${YELLOW}Current git status:${NC}"
git status --short

# Check if there are changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✓ Working directory is clean${NC}"
    exit 0
fi

# Function to create semantic commit
semantic_commit() {
    echo -e "\n${YELLOW}Choose commit type:${NC}"
    echo "1) feat     - New feature"
    echo "2) fix      - Bug fix"
    echo "3) docs     - Documentation only"
    echo "4) style    - Code style (formatting, etc)"
    echo "5) refactor - Code refactoring"
    echo "6) test     - Adding tests"
    echo "7) chore    - Maintenance tasks"
    echo "8) perf     - Performance improvements"
    
    read -p "Select type (1-8): " type_choice
    
    case $type_choice in
        1) type="feat" ;;
        2) type="fix" ;;
        3) type="docs" ;;
        4) type="style" ;;
        5) type="refactor" ;;
        6) type="test" ;;
        7) type="chore" ;;
        8) type="perf" ;;
        *) echo -e "${RED}Invalid choice${NC}"; exit 1 ;;
    esac
    
    read -p "Enter commit scope (optional, e.g., 'api', 'cli'): " scope
    read -p "Enter commit description: " description
    
    if [ -n "$scope" ]; then
        message="${type}(${scope}): ${description}"
    else
        message="${type}: ${description}"
    fi
    
    echo -e "\n${YELLOW}Commit message:${NC} $message"
    read -p "Add extended description? (y/n): " add_body
    
    if [ "$add_body" = "y" ]; then
        echo "Enter extended description (press Ctrl+D when done):"
        body=$(cat)
        full_message="${message}

${body}

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
    else
        full_message="${message}

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
    fi
    
    echo -e "\n${YELLOW}Files to commit:${NC}"
    git status --short
    
    read -p "Proceed with commit? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        git add -A
        git commit -m "$full_message"
        echo -e "${GREEN}✓ Commit successful${NC}"
    else
        echo -e "${YELLOW}Commit cancelled${NC}"
    fi
}

# Function for quick commit
quick_commit() {
    read -p "Enter commit message: " message
    echo -e "\n${YELLOW}Files to commit:${NC}"
    git status --short
    
    read -p "Proceed with commit? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        git add -A
        git commit -m "${message}

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
        echo -e "${GREEN}✓ Commit successful${NC}"
    else
        echo -e "${YELLOW}Commit cancelled${NC}"
    fi
}

# Main menu
echo -e "\n${YELLOW}Choose commit style:${NC}"
echo "1) Semantic commit (recommended)"
echo "2) Quick commit"
echo "3) Exit"

read -p "Select option (1-3): " choice

case $choice in
    1) semantic_commit ;;
    2) quick_commit ;;
    3) exit 0 ;;
    *) echo -e "${RED}Invalid choice${NC}"; exit 1 ;;
esac

# Show latest commits
echo -e "\n${YELLOW}Latest commits:${NC}"
git log --oneline -5