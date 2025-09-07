#!/bin/bash

# Create an index file that links todos to projects WITHOUT moving or modifying anything
# This creates a project-specific index in the project folder that points to todos

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to create todo index for current project
create_project_todo_index() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    if [ ! -d "$project_dir" ]; then
        echo -e "${YELLOW}No project history found${NC}"
        return 1
    fi
    
    # Create index file in project directory (not in todos!)
    local index_file="$project_dir/todo-index.json"
    local temp_index="/tmp/todo-index-$$.json"
    
    echo "{" > "$temp_index"
    echo '  "project": "'$current_path'",' >> "$temp_index"
    echo '  "generated": "'$(date -Iseconds)'",' >> "$temp_index"
    echo '  "todo_mappings": [' >> "$temp_index"
    
    local first=true
    local todo_count=0
    
    # Find all session files and their matching todos
    for session_file in "$project_dir"/*.jsonl; do
        if [ -f "$session_file" ]; then
            local session_id=$(basename "$session_file" .jsonl)
            
            # Check for matching todo files
            for pattern in "$session_id" "$session_id-agent-$session_id"; do
                local todo_file="$HOME/.claude/todos/${pattern}.json"
                
                if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                    local content=$(cat "$todo_file")
                    if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                        if [ "$first" = false ]; then
                            echo "," >> "$temp_index"
                        fi
                        first=false
                        
                        echo -n '    {' >> "$temp_index"
                        echo -n '"session_id": "'$session_id'",' >> "$temp_index"
                        echo -n '"todo_file": "'$pattern'.json",' >> "$temp_index"
                        echo -n '"session_date": "'$(stat -c %y "$session_file" | cut -d'.' -f1)'",' >> "$temp_index"
                        
                        if command -v jq &> /dev/null; then
                            local count=$(cat "$todo_file" | jq '. | length')
                            echo -n '"todo_count": '$count >> "$temp_index"
                            todo_count=$((todo_count + count))
                        else
                            echo -n '"todo_count": 0' >> "$temp_index"
                        fi
                        
                        echo -n '}' >> "$temp_index"
                    fi
                fi
            done
        fi
    done
    
    echo "" >> "$temp_index"
    echo '  ],' >> "$temp_index"
    echo '  "total_todos": '$todo_count >> "$temp_index"
    echo '}' >> "$temp_index"
    
    # Save the index
    mv "$temp_index" "$index_file"
    
    echo -e "${GREEN}✅ Created todo index: $index_file${NC}"
    echo -e "${BLUE}📊 Indexed $todo_count todos from $(grep -c session_id "$index_file") sessions${NC}"
    echo
    echo "This index file links todos to this project WITHOUT:"
    echo "- Moving any files from ~/.claude/todos/"
    echo "- Modifying any existing structures"
    echo "- Creating new folders"
    echo
    echo "The todos remain in their original location and can still be accessed by Claude Code."
}

# Function to read project todo index
read_project_todo_index() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local index_file="$HOME/.claude/projects/$project_hash/todo-index.json"
    
    if [ ! -f "$index_file" ]; then
        echo -e "${YELLOW}No todo index found. Run with 'create' first.${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📋 Todo Index for: $current_path${NC}"
    echo
    
    if command -v jq &> /dev/null; then
        # Parse and display the index
        local total=$(jq -r '.total_todos' "$index_file")
        local sessions=$(jq -r '.todo_mappings | length' "$index_file")
        
        echo "Total Todos: $total across $sessions sessions"
        echo
        echo "Linked Todo Files:"
        jq -r '.todo_mappings[] | "  - \(.todo_file) (\(.todo_count) todos) - \(.session_date)"' "$index_file"
        echo
        echo "All todos remain in: ~/.claude/todos/"
    else
        cat "$index_file"
    fi
}

# Function to verify todos still exist
verify_todo_links() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local index_file="$HOME/.claude/projects/$project_hash/todo-index.json"
    
    if [ ! -f "$index_file" ]; then
        echo -e "${YELLOW}No todo index found${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Verifying todo links...${NC}"
    
    local valid=0
    local missing=0
    
    if command -v jq &> /dev/null; then
        while read -r todo_file; do
            if [ -f "$HOME/.claude/todos/$todo_file" ]; then
                valid=$((valid + 1))
                echo -e "  ${GREEN}✓${NC} $todo_file"
            else
                missing=$((missing + 1))
                echo -e "  ${RED}✗${NC} $todo_file (missing)"
            fi
        done < <(jq -r '.todo_mappings[].todo_file' "$index_file")
    fi
    
    echo
    echo "Valid links: $valid"
    echo "Missing: $missing"
}

# Main
case "${1:-create}" in
    create)
        create_project_todo_index
        ;;
    read)
        read_project_todo_index
        ;;
    verify)
        verify_todo_links
        ;;
    help|--help|-h)
        echo "Todo Index Creator - Links todos to projects without moving files"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  create  - Create an index linking todos to current project"
        echo "  read    - Display the todo index for current project"
        echo "  verify  - Check if linked todo files still exist"
        echo "  help    - Show this help"
        echo ""
        echo "This creates an index in the project folder that points to todos"
        echo "WITHOUT moving or modifying the original ~/.claude/todos/ folder."
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use '$0 help' for usage"
        exit 1
        ;;
esac