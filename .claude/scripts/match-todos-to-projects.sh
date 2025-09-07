#!/bin/bash

# Script to match todos with their corresponding projects using session IDs
# This leverages the existing connection between project conversation logs and todo files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to get project path hash from current directory
get_project_hash() {
    pwd | sed 's/\//-/g'
}

# Function to extract todos for a specific project
get_project_todos() {
    local project_path="$1"
    local show_all="${2:-false}"
    
    # Convert project path to hash format used in .claude/projects
    local project_hash=$(echo "$project_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    if [ ! -d "$project_dir" ]; then
        echo "No project history found for: $project_path"
        return 1
    fi
    
    echo -e "${BLUE}Project: ${NC}$project_path"
    echo -e "${BLUE}Session logs found: ${NC}$(ls -1 "$project_dir"/*.jsonl 2>/dev/null | wc -l)"
    echo ""
    
    # Get all session IDs from this project (sorted by modification time)
    local session_ids=$(ls -t "$project_dir"/*.jsonl 2>/dev/null | xargs -r basename -s .jsonl)
    
    if [ -z "$session_ids" ]; then
        echo "No sessions found for this project"
        return 1
    fi
    
    local todos_found=0
    local sessions_checked=0
    
    # Check each session for matching todos
    for session_id in $session_ids; do
        sessions_checked=$((sessions_checked + 1))
        
        # Stop after checking recent sessions unless show_all is true
        if [ "$show_all" != "true" ] && [ $sessions_checked -gt 10 ]; then
            break
        fi
        
        # Look for matching todo files (both patterns)
        local todo_file1="$HOME/.claude/todos/${session_id}.json"
        local todo_file2="$HOME/.claude/todos/${session_id}-agent-${session_id}.json"
        
        local todo_file=""
        if [ -f "$todo_file1" ]; then
            todo_file="$todo_file1"
        elif [ -f "$todo_file2" ]; then
            todo_file="$todo_file2"
        fi
        
        if [ -n "$todo_file" ] && [ -s "$todo_file" ]; then
            # Check if the todo file has actual content (not just empty array)
            local content=$(cat "$todo_file")
            if [ "$content" != "[]" ] && [ "$content" != "null" ] && [ -n "$content" ]; then
                todos_found=$((todos_found + 1))
                
                # Get session date from file modification time
                local session_date=$(stat -c %y "$project_dir/${session_id}.jsonl" | cut -d' ' -f1)
                
                echo -e "${GREEN}📋 Session ${session_id:0:8}... (${session_date})${NC}"
                
                # Parse and display todos with jq if available
                if command -v jq &> /dev/null; then
                    cat "$todo_file" | jq -r '.[] | "   [\(.status)] \(.content)"' 2>/dev/null || echo "   [Error parsing todos]"
                else
                    # Fallback without jq - basic grep
                    echo "   $(grep -o '"content":"[^"]*"' "$todo_file" | sed 's/"content":"//g' | sed 's/"//g' | head -3)"
                    if [ $(grep -c '"content"' "$todo_file") -gt 3 ]; then
                        echo "   ... and more"
                    fi
                fi
                echo ""
            fi
        fi
    done
    
    if [ $todos_found -eq 0 ]; then
        echo -e "${YELLOW}No todos found for this project${NC}"
        echo "(Checked $sessions_checked recent sessions)"
    else
        echo -e "${GREEN}Found $todos_found sessions with todos${NC}"
    fi
}

# Function to show todos across all projects
show_all_projects_todos() {
    echo -e "${BLUE}=== Todos Across All Projects ===${NC}\n"
    
    local projects_dir="$HOME/.claude/projects"
    
    if [ ! -d "$projects_dir" ]; then
        echo "No projects found"
        return 1
    fi
    
    # Get all project directories
    for project_hash_dir in "$projects_dir"/*; do
        if [ -d "$project_hash_dir" ]; then
            # Convert hash back to path (basic conversion, may not be perfect)
            local project_name=$(basename "$project_hash_dir" | sed 's/^-/\//' | sed 's/-/\//g')
            
            echo "----------------------------------------"
            get_project_todos "$project_name" false
            echo ""
        fi
    done
}

# Function to clean orphaned todos
clean_orphaned_todos() {
    echo -e "${YELLOW}Cleaning orphaned todos...${NC}\n"
    
    local todos_dir="$HOME/.claude/todos"
    local projects_dir="$HOME/.claude/projects"
    
    local total_todos=$(ls -1 "$todos_dir"/*.json 2>/dev/null | wc -l)
    local orphaned_count=0
    local kept_count=0
    
    echo "Total todo files: $total_todos"
    echo "Checking for orphaned files..."
    
    for todo_file in "$todos_dir"/*.json; do
        if [ -f "$todo_file" ]; then
            # Extract session ID from filename
            local filename=$(basename "$todo_file")
            local session_id=""
            
            # Handle both naming patterns
            if [[ "$filename" =~ ^([a-f0-9-]+)-agent-.*\.json$ ]]; then
                session_id="${BASH_REMATCH[1]}"
            elif [[ "$filename" =~ ^([a-f0-9-]+)\.json$ ]]; then
                session_id="${BASH_REMATCH[1]}"
            fi
            
            if [ -n "$session_id" ]; then
                # Check if this session exists in any project
                local found=false
                for project_dir in "$projects_dir"/*; do
                    if [ -f "$project_dir/${session_id}.jsonl" ]; then
                        found=true
                        break
                    fi
                done
                
                if [ "$found" = false ]; then
                    echo "  Removing orphaned todo: ${filename:0:50}..."
                    rm "$todo_file"
                    orphaned_count=$((orphaned_count + 1))
                else
                    kept_count=$((kept_count + 1))
                fi
            fi
        fi
    done
    
    echo ""
    echo -e "${GREEN}Cleanup complete!${NC}"
    echo "  Removed: $orphaned_count orphaned todos"
    echo "  Kept: $kept_count active todos"
}

# Main script logic
main() {
    case "${1:-current}" in
        current)
            # Show todos for current project
            get_project_todos "$(pwd)"
            ;;
        all)
            # Show todos for all projects
            show_all_projects_todos
            ;;
        clean)
            # Clean orphaned todos
            clean_orphaned_todos
            ;;
        help|--help|-h)
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  current   - Show todos for current project (default)"
            echo "  all       - Show todos for all projects"
            echo "  clean     - Remove orphaned todos not linked to any project"
            echo "  help      - Show this help message"
            echo ""
            echo "This script matches todo files to projects using session IDs,"
            echo "leveraging the existing connection in Claude Code's storage."
            ;;
        *)
            echo "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"