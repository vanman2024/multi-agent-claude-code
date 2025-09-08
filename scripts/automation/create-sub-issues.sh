#!/bin/bash

# Helper script to create sub-issues for a parent issue
# Uses GitHub's GraphQL API to properly link parent/child relationships

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Function to get issue node ID
get_issue_node_id() {
    local issue_number=$1
    gh api graphql -f query="
    {
      repository(owner: \"vanman2024\", name: \"multi-agent-claude-code\") {
        issue(number: $issue_number) {
          id
        }
      }
    }" --jq '.data.repository.issue.id'
}

# Function to create and link a sub-issue
create_sub_issue() {
    local parent_number=$1
    local title=$2
    local body=$3
    local labels=$4
    
    echo -e "${BLUE}Creating sub-issue: $title${NC}"
    
    # Create the issue first
    local new_issue_url=$(gh issue create \
        --title "$title" \
        --body "$body" \
        --label "$labels" \
        --assignee @me \
        2>/dev/null)
    
    # Extract issue number from URL
    local new_issue_number=$(echo "$new_issue_url" | grep -oE '[0-9]+$')
    
    if [ -n "$new_issue_number" ]; then
        echo -e "${GREEN}✓ Created issue #$new_issue_number${NC}"
        
        # Get node IDs
        local parent_node_id=$(get_issue_node_id "$parent_number")
        local sub_node_id=$(get_issue_node_id "$new_issue_number")
        
        # Link as sub-issue
        echo -e "${YELLOW}Linking to parent issue #$parent_number...${NC}"
        
        gh api graphql -f query="
        mutation {
          addSubIssue(input: {
            issueId: \"$parent_node_id\"
            subIssueId: \"$sub_node_id\"
          }) {
            issue {
              number
            }
          }
        }" 2>/dev/null && echo -e "${GREEN}✓ Linked as sub-issue${NC}" || echo -e "${YELLOW}⚠ May already be linked${NC}"
        
        echo "$new_issue_number"
    else
        echo -e "${RED}✗ Failed to create issue${NC}"
        return 1
    fi
}

# Main function for interactive sub-issue creation
main() {
    local parent_issue="${1:-}"
    
    if [ -z "$parent_issue" ]; then
        read -p "Enter parent issue number: " parent_issue
    fi
    
    # Verify parent issue exists
    if ! gh issue view "$parent_issue" &>/dev/null; then
        echo -e "${RED}Error: Issue #$parent_issue not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Creating sub-issues for #$parent_issue${NC}"
    echo
    
    # Ask if user wants to create multiple sub-issues
    read -p "Do you want to create multiple sub-issues? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Enter sub-issues (empty line to finish):"
        echo
        
        local count=1
        while true; do
            echo "Sub-issue $count:"
            read -p "  Title (empty to finish): " title
            
            if [ -z "$title" ]; then
                break
            fi
            
            read -p "  Brief description: " description
            read -p "  Labels (comma-separated): " labels
            
            # Create the sub-issue
            local body="## Parent Issue
#$parent_issue

## Description
$description

## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests added
- [ ] Documentation updated"
            
            create_sub_issue "$parent_issue" "$title" "$body" "$labels"
            echo
            
            count=$((count + 1))
        done
    else
        # Single sub-issue creation
        read -p "Sub-issue title: " title
        read -p "Description: " description
        read -p "Labels (comma-separated): " labels
        
        local body="## Parent Issue
#$parent_issue

## Description
$description

## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests added
- [ ] Documentation updated"
        
        create_sub_issue "$parent_issue" "$title" "$body" "$labels"
    fi
    
    echo
    echo -e "${GREEN}Done! View parent issue: gh issue view $parent_issue${NC}"
}

# Export functions for use in other scripts
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi