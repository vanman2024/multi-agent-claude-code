#!/bin/bash

# Todo Reminder Hook - Reminds Claude to use TodoWrite tool
# This hook triggers on various events to encourage todo usage

EVENT_NAME="$1"
shift
ARGS="$@"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if todos are stale
check_todo_staleness() {
    local TODO_DIR="$HOME/.claude/todos"
    local CURRENT_SESSION_FILE=$(ls -t "$TODO_DIR"/*.json 2>/dev/null | head -1)
    
    if [[ -z "$CURRENT_SESSION_FILE" ]]; then
        echo "true"  # No todos = stale
        return
    fi
    
    # Check if last todo update was more than 30 minutes ago
    local LAST_MODIFIED=$(stat -c %Y "$CURRENT_SESSION_FILE" 2>/dev/null || stat -f %m "$CURRENT_SESSION_FILE" 2>/dev/null)
    local CURRENT_TIME=$(date +%s)
    local TIME_DIFF=$((CURRENT_TIME - LAST_MODIFIED))
    
    if [[ $TIME_DIFF -gt 1800 ]]; then  # 30 minutes
        echo "true"
    else
        echo "false"
    fi
}

# Function to suggest todo usage based on context
suggest_todo_usage() {
    local CONTEXT="$1"
    
    case "$CONTEXT" in
        "task_start")
            echo -e "${YELLOW}💡 Reminder: Use TodoWrite to track this task!${NC}"
            echo "This helps maintain a clear overview of progress."
            ;;
        "multi_step")
            echo -e "${YELLOW}📝 This looks like a multi-step task.${NC}"
            echo "Consider using TodoWrite to break it down into subtasks."
            ;;
        "stale")
            echo -e "${YELLOW}⏰ Your todo list might be outdated.${NC}"
            echo "Consider updating it with TodoWrite to reflect current work."
            ;;
        "complex")
            echo -e "${YELLOW}🎯 Complex task detected!${NC}"
            echo "TodoWrite can help organize the steps needed."
            ;;
    esac
}

# Main hook logic based on event
case "$EVENT_NAME" in
    "ToolUse")
        TOOL_NAME="$1"
        # Check if multiple tools are being used (indicates complex task)
        if [[ "$TOOL_NAME" == "Task" ]] || [[ "$TOOL_NAME" == "MultiEdit" ]]; then
            suggest_todo_usage "complex"
        fi
        ;;
        
    "CommandRun")
        COMMAND="$1"
        # Check for work-related commands
        if [[ "$COMMAND" == *"/work"* ]] || [[ "$COMMAND" == *"/create-issue"* ]]; then
            suggest_todo_usage "task_start"
        fi
        ;;
        
    "SessionStart")
        # Check if todos are stale at session start
        if [[ $(check_todo_staleness) == "true" ]]; then
            suggest_todo_usage "stale"
        fi
        
        # Show todo viewer hint
        echo -e "${BLUE}💻 Tip: Use /todo-viewer to see todos in a beautiful web interface!${NC}"
        ;;
        
    "UserPrompt")
        MESSAGE="$1"
        # Detect multi-step tasks from keywords
        if echo "$MESSAGE" | grep -qiE "implement|build|create|develop|fix.*and|then|after|steps"; then
            suggest_todo_usage "multi_step"
        fi
        ;;
esac

# Track tool usage statistics (for analysis)
STATS_FILE="$HOME/.claude/todo-usage-stats.json"
if [[ ! -f "$STATS_FILE" ]]; then
    echo '{"reminders_shown": 0, "last_reminder": null}' > "$STATS_FILE"
fi

# Update statistics
if [[ -n "$CONTEXT" ]]; then
    jq --arg time "$(date -Iseconds)" '.reminders_shown += 1 | .last_reminder = $time' "$STATS_FILE" > "${STATS_FILE}.tmp" && mv "${STATS_FILE}.tmp" "$STATS_FILE"
fi