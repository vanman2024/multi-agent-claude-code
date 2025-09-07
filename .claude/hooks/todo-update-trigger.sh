#!/bin/bash

# Real-time Todo Update Hook
# Triggers whenever TodoWrite is used to notify the web viewer

EVENT_NAME="$1"
shift
ARGS="$@"

# Only trigger on TodoWrite tool usage
if [[ "$EVENT_NAME" == "ToolUse" ]]; then
    TOOL_NAME="$1"
    
    if [[ "$TOOL_NAME" == "TodoWrite" ]]; then
        # Touch a marker file that the web app can watch
        MARKER_FILE="/tmp/claude-todos-updated-$(date +%s)"
        touch "$MARKER_FILE"
        
        # Clean up old markers (older than 1 minute)
        find /tmp -name "claude-todos-updated-*" -mmin +1 -delete 2>/dev/null
        
        # If the todo viewer server is running, trigger a refresh
        if lsof -i:8080 &>/dev/null; then
            # Send a simple HTTP request to trigger refresh (optional)
            curl -s -X POST http://localhost:8080/api/refresh &>/dev/null || true
        fi
        
        echo "📝 Todo list updated - web viewer will refresh automatically"
    fi
fi