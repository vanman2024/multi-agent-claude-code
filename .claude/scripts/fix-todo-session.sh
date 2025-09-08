#!/bin/bash

# Script to fix todo session tracking by ensuring current session is registered with project

set -e

# Get current directory project hash
CURRENT_PATH=$(pwd)
PROJECT_HASH=$(echo "$CURRENT_PATH" | sed 's/\//-/g')
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_HASH"

# Create project directory if it doesn't exist
mkdir -p "$PROJECT_DIR"

# Find the most recent todo file (current session)
LATEST_TODO=$(find ~/.claude/todos -name "*.json" -type f -mmin -10 2>/dev/null | xargs ls -t 2>/dev/null | head -1)

if [ -n "$LATEST_TODO" ]; then
    SESSION_ID=$(basename "$LATEST_TODO" .json | sed 's/-agent-.*//')
    echo "Found active session: $SESSION_ID"
    
    # Create session file if it doesn't exist
    SESSION_FILE="$PROJECT_DIR/${SESSION_ID}.jsonl"
    if [ ! -f "$SESSION_FILE" ]; then
        echo "Registering session with project..."
        echo "{\"timestamp\": \"$(date -Iseconds)\", \"session_id\": \"$SESSION_ID\", \"path\": \"$CURRENT_PATH\"}" > "$SESSION_FILE"
        echo "Session registered successfully"
    else
        echo "Session already registered"
    fi
    
    # Also ensure the agent variant is linked
    AGENT_SESSION="${SESSION_ID}-agent-${SESSION_ID}"
    if [ -f "$HOME/.claude/todos/${AGENT_SESSION}.json" ]; then
        AGENT_FILE="$PROJECT_DIR/${AGENT_SESSION}.jsonl"
        if [ ! -f "$AGENT_FILE" ]; then
            echo "{\"timestamp\": \"$(date -Iseconds)\", \"session_id\": \"$AGENT_SESSION\", \"path\": \"$CURRENT_PATH\"}" > "$AGENT_FILE"
        fi
    fi
else
    echo "No active todo session found"
fi

# Count todos after fix
echo ""
echo "Current todo counts for this project:"
python3 -c "
import json
import glob
import os

project_dir = '$PROJECT_DIR'
sessions = glob.glob(f'{project_dir}/*.jsonl')

todos_by_status = {'completed': 0, 'in_progress': 0, 'pending': 0}
total = 0

for session_file in sessions:
    session_id = os.path.basename(session_file).replace('.jsonl', '')
    
    for pattern in [session_id, f'{session_id}-agent-{session_id}']:
        todo_file = os.path.expanduser(f'~/.claude/todos/{pattern}.json')
        if os.path.exists(todo_file):
            try:
                with open(todo_file) as f:
                    data = json.load(f)
                    if data and isinstance(data, list):
                        for todo in data:
                            status = todo.get('status', 'pending')
                            todos_by_status[status] = todos_by_status.get(status, 0) + 1
                            total += 1
                break
            except:
                pass

print(f'Completed: {todos_by_status[\"completed\"]}')
print(f'In Progress: {todos_by_status[\"in_progress\"]}')  
print(f'Pending: {todos_by_status[\"pending\"]}')
print(f'Total: {total}')
"