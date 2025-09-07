#!/bin/bash

# Script to organize and view todos by project WITHOUT modifying the ~/.claude/todos folder
# This creates a read-only view of todos organized by their projects

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to create a project-todo mapping cache
create_todo_project_map() {
    local cache_file="$HOME/.claude/todo-project-map.json"
    local temp_file="/tmp/todo-project-map-$$.json"
    
    echo -e "${YELLOW}Building project-todo mapping...${NC}"
    
    echo "{" > "$temp_file"
    echo '  "generated": "'$(date -Iseconds)'",' >> "$temp_file"
    echo '  "mappings": {' >> "$temp_file"
    
    local first_project=true
    
    # Iterate through all projects
    for project_dir in "$HOME/.claude/projects"/*; do
        if [ -d "$project_dir" ]; then
            local project_name=$(basename "$project_dir")
            local readable_path=$(echo "$project_name" | sed 's/^-/\//' | sed 's/-/\//g')
            
            if [ "$first_project" = false ]; then
                echo "," >> "$temp_file"
            fi
            first_project=false
            
            echo -n '    "'$project_name'": {' >> "$temp_file"
            echo -n '"path": "'$readable_path'", "todos": [' >> "$temp_file"
            
            local first_todo=true
            
            # Find all session IDs for this project
            for session_file in "$project_dir"/*.jsonl; do
                if [ -f "$session_file" ]; then
                    local session_id=$(basename "$session_file" .jsonl)
                    
                    # Check for matching todo files (both patterns)
                    for pattern in "$session_id" "$session_id-agent-$session_id"; do
                        local todo_file="$HOME/.claude/todos/${pattern}.json"
                        
                        if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                            local content=$(cat "$todo_file")
                            if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                                if [ "$first_todo" = false ]; then
                                    echo -n ", " >> "$temp_file"
                                fi
                                first_todo=false
                                
                                echo -n '"'$pattern'"' >> "$temp_file"
                            fi
                        fi
                    done
                fi
            done
            
            echo -n ']}' >> "$temp_file"
        fi
    done
    
    echo "" >> "$temp_file"
    echo '  }' >> "$temp_file"
    echo '}' >> "$temp_file"
    
    mv "$temp_file" "$cache_file"
    echo -e "${GREEN}Mapping created: $cache_file${NC}"
}

# Function to show todos for current project only
show_current_project_todos() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    if [ ! -d "$project_dir" ]; then
        echo -e "${YELLOW}No project history found for current directory${NC}"
        echo "Path: $current_path"
        return 1
    fi
    
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}Project Todos: ${NC}$current_path"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
    
    local todos_found=0
    local total_todos=0
    
    # Get recent session IDs (last 20)
    for session_file in $(ls -t "$project_dir"/*.jsonl 2>/dev/null | head -20); do
        local session_id=$(basename "$session_file" .jsonl)
        
        # Check both todo file patterns
        for pattern in "$session_id" "$session_id-agent-$session_id"; do
            local todo_file="$HOME/.claude/todos/${pattern}.json"
            
            if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                local content=$(cat "$todo_file")
                if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                    todos_found=$((todos_found + 1))
                    
                    # Get session date
                    local session_date=$(stat -c %y "$session_file" | cut -d' ' -f1)
                    local session_time=$(stat -c %y "$session_file" | cut -d' ' -f2 | cut -d'.' -f1)
                    
                    echo -e "${GREEN}📋 Session: ${session_id:0:8}...${NC}"
                    echo -e "   Date: $session_date $session_time"
                    
                    # Parse todos with jq if available
                    if command -v jq &> /dev/null; then
                        local todo_count=$(cat "$todo_file" | jq -r '. | length' 2>/dev/null || echo 0)
                        total_todos=$((total_todos + todo_count))
                        
                        cat "$todo_file" | jq -r '.[] | 
                            if .status == "completed" then 
                                "   ✅ [\(.status)] \(.content)"
                            elif .status == "in_progress" then
                                "   🔄 [\(.status)] \(.content)"
                            else
                                "   ⏳ [\(.status)] \(.content)"
                            end' 2>/dev/null || echo "   [Error parsing todos]"
                    else
                        # Fallback without jq
                        echo "   $(grep -o '"content":"[^"]*"' "$todo_file" | sed 's/"content":"//g' | sed 's/"//g' | head -5)"
                    fi
                    echo ""
                fi
            fi
        done
    done
    
    echo -e "${BLUE}───────────────────────────────────────────────────────${NC}"
    if [ $todos_found -eq 0 ]; then
        echo -e "${YELLOW}No todos found for this project${NC}"
    else
        echo -e "${GREEN}Summary: $todos_found sessions with $total_todos total todos${NC}"
    fi
}

# Function to show summary of all projects with todo counts
show_all_projects_summary() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}All Projects Todo Summary${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
    
    local total_projects=0
    local total_todos_global=0
    
    for project_dir in "$HOME/.claude/projects"/*; do
        if [ -d "$project_dir" ]; then
            local project_name=$(basename "$project_dir")
            local readable_path=$(echo "$project_name" | sed 's/^-/\//' | sed 's/-/\//g')
            
            local session_count=0
            local todo_count=0
            
            # Count sessions with todos
            for session_file in "$project_dir"/*.jsonl; do
                if [ -f "$session_file" ]; then
                    local session_id=$(basename "$session_file" .jsonl)
                    
                    for pattern in "$session_id" "$session_id-agent-$session_id"; do
                        local todo_file="$HOME/.claude/todos/${pattern}.json"
                        
                        if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                            local content=$(cat "$todo_file")
                            if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                                session_count=$((session_count + 1))
                                
                                if command -v jq &> /dev/null; then
                                    local count=$(cat "$todo_file" | jq -r '. | length' 2>/dev/null || echo 0)
                                    todo_count=$((todo_count + count))
                                fi
                                break
                            fi
                        fi
                    done
                fi
            done
            
            if [ $session_count -gt 0 ]; then
                total_projects=$((total_projects + 1))
                total_todos_global=$((total_todos_global + todo_count))
                
                # Truncate long paths
                if [ ${#readable_path} -gt 50 ]; then
                    readable_path="...${readable_path: -47}"
                fi
                
                printf "${GREEN}%-52s${NC} %3d sessions, %4d todos\n" "$readable_path" "$session_count" "$todo_count"
            fi
        fi
    done
    
    echo ""
    echo -e "${BLUE}───────────────────────────────────────────────────────${NC}"
    echo -e "${CYAN}Total: $total_projects projects with $total_todos_global todos${NC}"
}

# Function to export todos for a project to markdown
export_project_todos() {
    local export_dir="$HOME/.claude/todo-exports"
    mkdir -p "$export_dir"
    
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    if [ ! -d "$project_dir" ]; then
        echo -e "${RED}No project found for current directory${NC}"
        return 1
    fi
    
    local export_file="$export_dir/${project_hash}-todos-$(date +%Y%m%d-%H%M%S).md"
    
    echo "# Todo Export for $current_path" > "$export_file"
    echo "Generated: $(date)" >> "$export_file"
    echo "" >> "$export_file"
    
    for session_file in $(ls -t "$project_dir"/*.jsonl 2>/dev/null); do
        local session_id=$(basename "$session_file" .jsonl)
        
        for pattern in "$session_id" "$session_id-agent-$session_id"; do
            local todo_file="$HOME/.claude/todos/${pattern}.json"
            
            if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                local content=$(cat "$todo_file")
                if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                    echo "## Session: $session_id" >> "$export_file"
                    echo "Date: $(stat -c %y "$session_file" | cut -d'.' -f1)" >> "$export_file"
                    echo "" >> "$export_file"
                    
                    if command -v jq &> /dev/null; then
                        cat "$todo_file" | jq -r '.[] | "- [\(if .status == "completed" then "x" else " " end)] \(.content)"' >> "$export_file"
                    fi
                    echo "" >> "$export_file"
                fi
            fi
        done
    done
    
    echo -e "${GREEN}Exported to: $export_file${NC}"
}

# Main menu
main() {
    case "${1:-current}" in
        current)
            show_current_project_todos
            ;;
        summary)
            show_all_projects_summary
            ;;
        map)
            create_todo_project_map
            ;;
        export)
            export_project_todos
            ;;
        help|--help|-h)
            echo "Todo Organization Tool - View todos by project WITHOUT modifying ~/.claude/todos/"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  current   - Show todos for current project (default)"
            echo "  summary   - Show summary of all projects with todo counts"
            echo "  map       - Create a project-todo mapping cache"
            echo "  export    - Export current project's todos to markdown"
            echo "  help      - Show this help message"
            echo ""
            echo "This tool provides a read-only view of todos organized by project."
            echo "It NEVER modifies the ~/.claude/todos/ folder."
            ;;
        *)
            echo "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"