#!/bin/bash

# Todo Management Script - Fixes the session-based todo problem
# Uses a single project-based todo file instead of session files

PROJECT_PATH="${1:-/home/gotime2022/Projects/multi-agent-claude-code}"
PROJECT_NAME=$(basename "$PROJECT_PATH")
TODO_DIR="$HOME/.claude/todos"
PROJECT_TODO_FILE="$TODO_DIR/PROJECT-${PROJECT_NAME}.json"
SESSION_PATTERN="*-agent-*.json"

# Ensure todo directory exists
mkdir -p "$TODO_DIR"

# Function to consolidate all todos into project file
consolidate_todos() {
    echo "Consolidating todos from all sessions..."
    
    # Create temporary file for consolidated todos
    TEMP_FILE=$(mktemp)
    echo "[]" > "$TEMP_FILE"
    
    # Find all non-empty session files and merge them
    for file in $TODO_DIR/$SESSION_PATTERN; do
        if [ -f "$file" ] && [ -s "$file" ]; then
            # Check if file is not just "[]"
            content=$(cat "$file")
            if [ "$content" != "[]" ] && [ "$content" != "[ ]" ]; then
                echo "Processing: $(basename $file)"
                # Merge with existing todos
                jq -s '.[0] + .[1]' "$TEMP_FILE" "$file" > "${TEMP_FILE}.new"
                mv "${TEMP_FILE}.new" "$TEMP_FILE"
            fi
        fi
    done
    
    # Remove duplicates based on content and timestamp
    jq 'unique_by(.content + .timestamp)' "$TEMP_FILE" > "$PROJECT_TODO_FILE"
    
    rm -f "$TEMP_FILE"
    echo "Consolidated $(jq length "$PROJECT_TODO_FILE") todos into $PROJECT_TODO_FILE"
}

# Function to clean up empty session files
cleanup_empty_sessions() {
    echo "Cleaning up empty session files..."
    count=0
    for file in $TODO_DIR/$SESSION_PATTERN; do
        if [ -f "$file" ]; then
            content=$(cat "$file")
            if [ "$content" = "[]" ] || [ "$content" = "[ ]" ] || [ ! -s "$file" ]; then
                rm -f "$file"
                ((count++))
            fi
        fi
    done
    echo "Removed $count empty session files"
}

# Function to update todo status
update_todo() {
    local content="$1"
    local new_status="$2"
    
    if [ ! -f "$PROJECT_TODO_FILE" ]; then
        echo "No project todo file found"
        return 1
    fi
    
    # Update the status of matching todo
    jq --arg content "$content" --arg status "$new_status" \
        'map(if .content == $content then .status = $status else . end)' \
        "$PROJECT_TODO_FILE" > "${PROJECT_TODO_FILE}.tmp"
    
    mv "${PROJECT_TODO_FILE}.tmp" "$PROJECT_TODO_FILE"
    echo "Updated todo status: $content -> $new_status"
}

# Function to add new todo
add_todo() {
    local content="$1"
    local status="${2:-pending}"
    
    # Initialize file if it doesn't exist
    if [ ! -f "$PROJECT_TODO_FILE" ]; then
        echo "[]" > "$PROJECT_TODO_FILE"
    fi
    
    # Create new todo object
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
    local date=$(date -u +"%Y-%m-%d")
    
    jq --arg content "$content" \
       --arg status "$status" \
       --arg timestamp "$timestamp" \
       --arg date "$date" \
       --arg project "$PROJECT_NAME" \
       --arg path "$PROJECT_PATH" \
       '. + [{
           content: $content,
           status: $status,
           timestamp: $timestamp,
           date: $date,
           projectName: $project,
           projectPath: $path
       }]' "$PROJECT_TODO_FILE" > "${PROJECT_TODO_FILE}.tmp"
    
    mv "${PROJECT_TODO_FILE}.tmp" "$PROJECT_TODO_FILE"
    echo "Added new todo: $content"
}

# Function to get current session file (for compatibility)
get_session_file() {
    # Find the most recent session file
    ls -t $TODO_DIR/*-agent-*.json 2>/dev/null | head -1
}

# Function to sync session file with project file
sync_session_to_project() {
    local session_file=$(get_session_file)
    if [ -f "$session_file" ]; then
        # Copy project todos to session file for TodoWrite compatibility
        cp "$PROJECT_TODO_FILE" "$session_file"
        echo "Synced project todos to session: $(basename $session_file)"
    fi
}

# Main command processing
case "${2:-consolidate}" in
    consolidate)
        consolidate_todos
        cleanup_empty_sessions
        ;;
    add)
        add_todo "$3" "${4:-pending}"
        sync_session_to_project
        ;;
    update)
        update_todo "$3" "$4"
        sync_session_to_project
        ;;
    complete)
        update_todo "$3" "completed"
        sync_session_to_project
        ;;
    cleanup)
        cleanup_empty_sessions
        ;;
    sync)
        sync_session_to_project
        ;;
    stats)
        if [ -f "$PROJECT_TODO_FILE" ]; then
            echo "Project todos: $(jq length "$PROJECT_TODO_FILE")"
            echo "Pending: $(jq '[.[] | select(.status == "pending")] | length' "$PROJECT_TODO_FILE")"
            echo "In Progress: $(jq '[.[] | select(.status == "in_progress")] | length' "$PROJECT_TODO_FILE")"
            echo "Completed: $(jq '[.[] | select(.status == "completed")] | length' "$PROJECT_TODO_FILE")"
        else
            echo "No project todo file found"
        fi
        ;;
    *)
        echo "Usage: $0 [project-path] [command] [args]"
        echo "Commands:"
        echo "  consolidate - Merge all session todos into project file (default)"
        echo "  add <content> [status] - Add new todo"
        echo "  update <content> <status> - Update todo status"
        echo "  complete <content> - Mark todo as completed"
        echo "  cleanup - Remove empty session files"
        echo "  sync - Sync project file to current session"
        echo "  stats - Show todo statistics"
        ;;
esac