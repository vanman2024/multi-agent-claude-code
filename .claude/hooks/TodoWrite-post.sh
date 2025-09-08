#!/bin/bash
# Hook: TodoWrite-post
# Purpose: Simple workaround - if TodoWrite clears all todos, restore them

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
TODO_DIR="$HOME/.claude/todos"
TEMP_BACKUP="/tmp/todo-last-state.json"

# Find the current session's todo file (most recently modified)
CURRENT_TODO=$(find "$TODO_DIR" -name "*.json" -type f -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -f "$CURRENT_TODO" ]; then
    # Read current content
    FILE_CONTENT=$(cat "$CURRENT_TODO")
    
    # If file was just cleared but we have a backup
    if [ "$FILE_CONTENT" = "[]" ] && [ -f "$TEMP_BACKUP" ]; then
        # Check if backup had any todos at all
        BACKUP_COUNT=$(jq 'length' "$TEMP_BACKUP" 2>/dev/null || echo 0)
        
        if [ "$BACKUP_COUNT" -gt 0 ]; then
            # Mark all todos in backup as completed (since TodoWrite cleared them, they must all be done)
            jq 'map(.status = "completed")' "$TEMP_BACKUP" > "$CURRENT_TODO"
            echo "✅ Restored $(jq 'length' "$CURRENT_TODO") completed todos (TodoWrite bug workaround)" >&2
        fi
    fi
    
    # Save current state for next time (only if not empty)
    if [ "$FILE_CONTENT" != "[]" ] && [ "$FILE_CONTENT" != "" ]; then
        echo "$FILE_CONTENT" > "$TEMP_BACKUP"
    fi
fi

# Register session
bash "$(dirname "$0")/register-session.sh" 2>/dev/null

exit 0