#!/bin/bash

# Todo Archive System - Maintains persistent todo history
# This script archives todos before they're lost and restores them on demand

PROJECT_PATH="${1:-/home/gotime2022/Projects/multi-agent-claude-code}"
PROJECT_NAME=$(basename "$PROJECT_PATH")
TODO_DIR="$HOME/.claude/todos"
PROJECT_HASH=$(echo "$PROJECT_PATH" | sed 's/\//-/g')
ARCHIVE_DIR="$HOME/.claude/projects/$PROJECT_HASH/todo-archive"
ARCHIVE_FILE="$ARCHIVE_DIR/master-todos.json"

# Ensure directories exist
mkdir -p "$ARCHIVE_DIR"

# Function to archive current todos (merge with existing archive)
archive_todos() {
    echo "Archiving todos..."
    
    # Initialize archive if it doesn't exist
    if [ ! -f "$ARCHIVE_FILE" ]; then
        echo "[]" > "$ARCHIVE_FILE"
    fi
    
    # Collect all todos from all session files for this project
    TEMP_ALL=$(mktemp)
    echo "[]" > "$TEMP_ALL"
    
    # Get all session IDs for this project
    for session_file in "$HOME/.claude/projects/$PROJECT_HASH"/*.jsonl; do
        if [ -f "$session_file" ]; then
            SESSION_ID=$(basename "$session_file" .jsonl)
            TODO_FILE="$TODO_DIR/${SESSION_ID}.json"
            
            if [ -f "$TODO_FILE" ] && [ -s "$TODO_FILE" ]; then
                # Merge this session's todos
                jq -s '.[0] + .[1]' "$TEMP_ALL" "$TODO_FILE" > "${TEMP_ALL}.new"
                mv "${TEMP_ALL}.new" "$TEMP_ALL"
            fi
        fi
    done
    
    # Merge with existing archive, keeping unique todos by content
    jq -s '[.[0] + .[1] | group_by(.content) | .[] | 
            if length == 1 then .[0] 
            else (.[0] as $base | 
                  .[] | select(.status == "completed") // $base) 
            end] | sort_by(.timestamp // "2025-01-01")' \
        "$ARCHIVE_FILE" "$TEMP_ALL" > "${ARCHIVE_FILE}.tmp"
    
    mv "${ARCHIVE_FILE}.tmp" "$ARCHIVE_FILE"
    
    TODO_COUNT=$(jq length "$ARCHIVE_FILE")
    COMPLETED=$(jq '[.[] | select(.status == "completed")] | length' "$ARCHIVE_FILE")
    PENDING=$(jq '[.[] | select(.status == "pending")] | length' "$ARCHIVE_FILE")
    
    echo "✅ Archived $TODO_COUNT todos ($COMPLETED completed, $PENDING pending)"
    
    rm -f "$TEMP_ALL"
}

# Function to restore todos to current session
restore_todos() {
    echo "Restoring todos from archive..."
    
    if [ ! -f "$ARCHIVE_FILE" ]; then
        echo "No archive found"
        return 1
    fi
    
    # Find current session file
    CURRENT_SESSION=$(ls -t "$TODO_DIR"/*.json 2>/dev/null | head -1)
    
    if [ -z "$CURRENT_SESSION" ]; then
        echo "No current session found"
        return 1
    fi
    
    # Only restore if current session is empty or very small
    CURRENT_COUNT=$(jq 'length' "$CURRENT_SESSION" 2>/dev/null || echo 0)
    
    if [ "$CURRENT_COUNT" -lt 3 ]; then
        # Restore non-completed todos plus recent completed ones
        jq '[.[] | select(.status != "completed" or 
            (.timestamp // "2025-01-01" | . >= "'$(date -d '7 days ago' -Iseconds)'"))]' \
            "$ARCHIVE_FILE" > "$CURRENT_SESSION"
        
        RESTORED=$(jq length "$CURRENT_SESSION")
        echo "✅ Restored $RESTORED todos to current session"
    else
        echo "Current session has $CURRENT_COUNT todos, skipping restore"
    fi
}

# Function to show archive stats
show_stats() {
    if [ -f "$ARCHIVE_FILE" ]; then
        echo "📊 Todo Archive Statistics:"
        echo "Total: $(jq length "$ARCHIVE_FILE")"
        echo "Completed: $(jq '[.[] | select(.status == "completed")] | length' "$ARCHIVE_FILE")"
        echo "In Progress: $(jq '[.[] | select(.status == "in_progress")] | length' "$ARCHIVE_FILE")"
        echo "Pending: $(jq '[.[] | select(.status == "pending")] | length' "$ARCHIVE_FILE")"
        echo ""
        echo "Recent todos:"
        jq -r '.[-5:] | reverse | .[] | 
            "  [\(.status[0:1] | ascii_upcase)] \(.content[0:50])"' "$ARCHIVE_FILE" 2>/dev/null
    else
        echo "No archive found"
    fi
}

# Function to hop (archive then restore)
hop_todos() {
    echo "🔄 Hopping todos (archive + restore)..."
    archive_todos
    restore_todos
}

# Main command processing
case "${2:-hop}" in
    archive)
        archive_todos
        ;;
    restore)
        restore_todos
        ;;
    stats)
        show_stats
        ;;
    hop)
        hop_todos
        ;;
    auto)
        # Auto mode: archive if todos exist, restore if empty
        CURRENT_SESSION=$(ls -t "$TODO_DIR"/*.json 2>/dev/null | head -1)
        if [ -f "$CURRENT_SESSION" ]; then
            COUNT=$(jq 'length' "$CURRENT_SESSION" 2>/dev/null || echo 0)
            if [ "$COUNT" -gt 0 ]; then
                archive_todos
            else
                restore_todos
            fi
        fi
        ;;
    *)
        echo "Usage: $0 [project-path] [archive|restore|stats|hop|auto]"
        echo "  archive - Save current todos to persistent archive"
        echo "  restore - Restore todos from archive to current session"
        echo "  stats   - Show archive statistics"
        echo "  hop     - Archive then restore (default)"
        echo "  auto    - Smart mode: archive if full, restore if empty"
        ;;
esac