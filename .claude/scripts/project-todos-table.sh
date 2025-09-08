#!/bin/bash

# Enhanced script to display todos in a table format with better visualization
# Shows ALL todos (completed, in-progress, pending) across all sessions

set -e

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Box drawing characters
BOX_TOP_LEFT='╔'
BOX_TOP_RIGHT='╗'
BOX_BOTTOM_LEFT='╚'
BOX_BOTTOM_RIGHT='╝'
BOX_HORIZONTAL='═'
BOX_VERTICAL='║'
BOX_CROSS='╬'
BOX_T_DOWN='╦'
BOX_T_UP='╩'
BOX_T_RIGHT='╠'
BOX_T_LEFT='╣'

# Function to draw a line
draw_line() {
    local width=${1:-80}
    printf "${BOX_HORIZONTAL}%.0s" $(seq 1 $width)
}

# Function to display todos as a formatted table
show_project_todos_table() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    if [ ! -d "$project_dir" ]; then
        echo -e "${YELLOW}No project history found for current directory${NC}"
        return 1
    fi
    
    # Header
    echo
    echo -e "${BOLD}${BLUE}${BOX_TOP_LEFT}$(draw_line 78)${BOX_TOP_RIGHT}${NC}"
    printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} %-76s ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" "📊 PROJECT TODO TRACKER"
    printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${DIM}%-76s${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" "${current_path}"
    echo -e "${BOLD}${BLUE}${BOX_T_RIGHT}$(draw_line 78)${BOX_T_LEFT}${NC}"
    
    # Stats counters
    local total_completed=0
    local total_in_progress=0
    local total_pending=0
    local total_todos=0
    local session_count=0
    
    # Collect all todos first for statistics
    local temp_file="/tmp/todos-$$"
    > "$temp_file"
    
    for session_file in $(ls -t "$project_dir"/*.jsonl 2>/dev/null); do
        local session_id=$(basename "$session_file" .jsonl)
        
        for pattern in "$session_id" "$session_id-agent-$session_id"; do
            local todo_file="$HOME/.claude/todos/${pattern}.json"
            
            if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                local content=$(cat "$todo_file")
                if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                    session_count=$((session_count + 1))
                    local session_date=$(stat -c %y "$session_file" | cut -d' ' -f1)
                    
                    if command -v jq &> /dev/null; then
                        # Save todos with session info
                        cat "$todo_file" | jq -r --arg sid "$session_id" --arg sdate "$session_date" \
                            '.[] | "\($sdate)|\($sid)|\(.status)|\(.content)"' >> "$temp_file"
                    fi
                    break
                fi
            fi
        done
    done
    
    # Count by status
    total_completed=$(grep -c "|completed|" "$temp_file" 2>/dev/null || echo 0)
    total_in_progress=$(grep -c "|in_progress|" "$temp_file" 2>/dev/null || echo 0)
    total_pending=$(grep -c "|pending|" "$temp_file" 2>/dev/null || echo 0)
    total_todos=$((total_completed + total_in_progress + total_pending))
    
    # Display statistics bar
    printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} " 
    printf "${GREEN}✅ Completed: %-8d${NC} " "$total_completed"
    printf "${YELLOW}🔄 In Progress: %-8d${NC} " "$total_in_progress"
    printf "${CYAN}⏳ Pending: %-8d${NC}  " "$total_pending"
    printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n"
    
    echo -e "${BOLD}${BLUE}${BOX_T_RIGHT}$(draw_line 78)${BOX_T_LEFT}${NC}"
    
    # Table header
    printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${BOLD}%-12s %-8s %-55s${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" \
        "DATE" "STATUS" "TASK"
    echo -e "${BOLD}${BLUE}${BOX_T_RIGHT}$(draw_line 78)${BOX_T_LEFT}${NC}"
    
    # Display todos grouped by status
    if [ $total_in_progress -gt 0 ]; then
        echo -e "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${BOLD}${YELLOW}IN PROGRESS                                                                  ${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}"
        grep "|in_progress|" "$temp_file" | while IFS='|' read -r date sid status content; do
            # Truncate content if too long
            if [ ${#content} -gt 53 ]; then
                content="${content:0:50}..."
            fi
            printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${DIM}%-12s${NC} ${YELLOW}%-8s${NC} %-55s ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" \
                "$date" "🔄" "$content"
        done
    fi
    
    if [ $total_pending -gt 0 ]; then
        if [ $total_in_progress -gt 0 ]; then
            echo -e "${BOLD}${BLUE}${BOX_T_RIGHT}$(draw_line 78)${BOX_T_LEFT}${NC}"
        fi
        echo -e "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${BOLD}${CYAN}PENDING                                                                      ${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}"
        grep "|pending|" "$temp_file" | while IFS='|' read -r date sid status content; do
            if [ ${#content} -gt 53 ]; then
                content="${content:0:50}..."
            fi
            printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${DIM}%-12s${NC} ${CYAN}%-8s${NC} %-55s ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" \
                "$date" "⏳" "$content"
        done
    fi
    
    if [ $total_completed -gt 0 ]; then
        if [ $((total_in_progress + total_pending)) -gt 0 ]; then
            echo -e "${BOLD}${BLUE}${BOX_T_RIGHT}$(draw_line 78)${BOX_T_LEFT}${NC}"
        fi
        echo -e "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${BOLD}${GREEN}COMPLETED                                                                    ${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}"
        grep "|completed|" "$temp_file" | tail -10 | while IFS='|' read -r date sid status content; do
            if [ ${#content} -gt 53 ]; then
                content="${content:0:50}..."
            fi
            printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${DIM}%-12s${NC} ${GREEN}%-8s${NC} ${DIM}%-55s${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" \
                "$date" "✅" "$content"
        done
        local completed_hidden=$((total_completed - 10))
        if [ $completed_hidden -gt 0 ]; then
            printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${DIM}%-76s${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" \
                "... and $completed_hidden more completed tasks"
        fi
    fi
    
    # Footer
    echo -e "${BOLD}${BLUE}${BOX_T_RIGHT}$(draw_line 78)${BOX_T_LEFT}${NC}"
    printf "${BOLD}${BLUE}${BOX_VERTICAL}${NC} ${BOLD}%-76s${NC} ${BOLD}${BLUE}${BOX_VERTICAL}${NC}\n" \
        "SUMMARY: $session_count sessions | $total_todos total tasks"
    echo -e "${BOLD}${BLUE}${BOX_BOTTOM_LEFT}$(draw_line 78)${BOX_BOTTOM_RIGHT}${NC}"
    echo
    
    # Clean up
    rm -f "$temp_file"
}

# Function to show markdown export suitable for GitHub
show_markdown_export() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    echo "# 📊 Project Todo Report"
    echo
    echo "**Project:** \`$current_path\`"
    echo "**Generated:** $(date '+%Y-%m-%d %H:%M:%S')"
    echo
    
    # Collect statistics
    local total_completed=0
    local total_in_progress=0
    local total_pending=0
    
    local temp_file="/tmp/todos-md-$$"
    > "$temp_file"
    
    for session_file in $(ls -t "$project_dir"/*.jsonl 2>/dev/null); do
        local session_id=$(basename "$session_file" .jsonl)
        
        for pattern in "$session_id" "$session_id-agent-$session_id"; do
            local todo_file="$HOME/.claude/todos/${pattern}.json"
            
            if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                local content=$(cat "$todo_file")
                if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                    if command -v jq &> /dev/null; then
                        cat "$todo_file" | jq -r '.[] | "\(.status)|\(.content)"' >> "$temp_file"
                    fi
                    break
                fi
            fi
        done
    done
    
    total_completed=$(grep -c "^completed|" "$temp_file" 2>/dev/null || echo 0)
    total_in_progress=$(grep -c "^in_progress|" "$temp_file" 2>/dev/null || echo 0)
    total_pending=$(grep -c "^pending|" "$temp_file" 2>/dev/null || echo 0)
    
    echo "## 📈 Statistics"
    echo
    echo "| Status | Count | Percentage |"
    echo "|--------|-------|------------|"
    local total=$((total_completed + total_in_progress + total_pending))
    if [ $total -gt 0 ]; then
        echo "| ✅ Completed | $total_completed | $((total_completed * 100 / total))% |"
        echo "| 🔄 In Progress | $total_in_progress | $((total_in_progress * 100 / total))% |"
        echo "| ⏳ Pending | $total_pending | $((total_pending * 100 / total))% |"
        echo "| **Total** | **$total** | **100%** |"
    fi
    echo
    
    echo "## 🔄 In Progress Tasks"
    echo
    if [ $total_in_progress -gt 0 ]; then
        grep "^in_progress|" "$temp_file" | while IFS='|' read -r status content; do
            echo "- [ ] $content"
        done
    else
        echo "*No tasks in progress*"
    fi
    echo
    
    echo "## ⏳ Pending Tasks"
    echo
    if [ $total_pending -gt 0 ]; then
        grep "^pending|" "$temp_file" | while IFS='|' read -r status content; do
            echo "- [ ] $content"
        done
    else
        echo "*No pending tasks*"
    fi
    echo
    
    echo "## ✅ Recently Completed"
    echo
    if [ $total_completed -gt 0 ]; then
        grep "^completed|" "$temp_file" | tail -10 | while IFS='|' read -r status content; do
            echo "- [x] $content"
        done
        if [ $total_completed -gt 10 ]; then
            echo
            echo "*...and $((total_completed - 10)) more completed tasks*"
        fi
    else
        echo "*No completed tasks*"
    fi
    
    rm -f "$temp_file"
}

# Function to output JSON format
show_json_export() {
    local current_path=$(pwd)
    local project_hash=$(echo "$current_path" | sed 's/\//-/g')
    local project_dir="$HOME/.claude/projects/$project_hash"
    
    local todos_json="[]"
    local session_count=0
    
    if [ -d "$project_dir" ]; then
        local temp_file="/tmp/todos-json-$$"
        > "$temp_file"
        
        for session_file in $(ls -t "$project_dir"/*.jsonl 2>/dev/null); do
            local session_id=$(basename "$session_file" .jsonl)
            
            for pattern in "$session_id" "$session_id-agent-$session_id"; do
                local todo_file="$HOME/.claude/todos/${pattern}.json"
                
                if [ -f "$todo_file" ] && [ -s "$todo_file" ]; then
                    local content=$(cat "$todo_file")
                    if [ "$content" != "[]" ] && [ "$content" != "null" ]; then
                        session_count=$((session_count + 1))
                        local session_date=$(stat -c %y "$session_file" | cut -d' ' -f1)
                        
                        if command -v jq &> /dev/null; then
                            # Add session info to each todo
                            cat "$todo_file" | jq --arg sid "$session_id" --arg sdate "$session_date" \
                                '[.[] | . + {session: $sid, date: $sdate}]' >> "$temp_file"
                        fi
                        break
                    fi
                fi
            done
        done
        
        # Combine all todos into single array
        if [ -s "$temp_file" ]; then
            todos_json=$(cat "$temp_file" | jq -s 'add')
        fi
        rm -f "$temp_file"
    fi
    
    # Output JSON
    echo "{\"todos\": $todos_json, \"sessions\": $session_count, \"project\": \"$current_path\"}"
}

# Main function
main() {
    case "${1:-table}" in
        table|current)
            show_project_todos_table
            ;;
        markdown|export)
            show_markdown_export
            ;;
        json)
            show_json_export
            ;;
        help|--help|-h)
            echo "Project Todos Table View"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  table     - Show todos in table format (default)"
            echo "  markdown  - Export as markdown for GitHub"
            echo "  json      - Export as JSON for API consumption"
            echo "  help      - Show this help"
            ;;
        *)
            show_project_todos_table
            ;;
    esac
}

main "$@"