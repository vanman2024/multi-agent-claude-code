#!/bin/bash

# Hook to automatically register todo sessions with the current project
# This ensures todos are properly tracked and visible in the dashboard

# Get current directory project hash
CURRENT_PATH=$(pwd)
PROJECT_HASH=$(echo "$CURRENT_PATH" | sed 's/\//-/g')
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_HASH"

# Create project directory if it doesn't exist
mkdir -p "$PROJECT_DIR"

# Function to register a session
register_session() {
    local todo_file="$1"
    if [ -f "$todo_file" ]; then
        local session_id=$(basename "$todo_file" .json | sed 's/-agent-.*//')
        local full_session=$(basename "$todo_file" .json)
        local session_file="$PROJECT_DIR/${full_session}.jsonl"
        
        if [ ! -f "$session_file" ]; then
            echo "{\"timestamp\": \"$(date -Iseconds)\", \"session_id\": \"$full_session\", \"path\": \"$CURRENT_PATH\"}" > "$session_file"
            return 0
        fi
    fi
    return 1
}

# Check for recent todo files (last 5 minutes)
REGISTERED=0
for todo_file in $(find ~/.claude/todos -name "*.json" -type f -mmin -5 2>/dev/null); do
    if register_session "$todo_file"; then
        REGISTERED=$((REGISTERED + 1))
    fi
done

if [ $REGISTERED -gt 0 ]; then
    echo "✅ Registered $REGISTERED new todo session(s) with project"
fi