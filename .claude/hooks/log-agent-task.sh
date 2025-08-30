#!/bin/bash
# Hook: Log agent task invocations
# Event: PreToolUse (Task)
# Purpose: Track and coordinate agent operations

# Read the hook input
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')

# Only process Task tool calls
if [ "$TOOL_NAME" != "Task" ]; then
  exit 0
fi

# Extract agent details
AGENT_TYPE=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // "unknown"')
DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // ""')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create log directory if it doesn't exist
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$(dirname "$SCRIPT_DIR")/logs"
mkdir -p "$LOG_DIR"

# Log to file
LOG_FILE="$LOG_DIR/agent-tasks.jsonl"
echo "{\"timestamp\":\"$TIMESTAMP\",\"session_id\":\"$SESSION_ID\",\"agent_type\":\"$AGENT_TYPE\",\"description\":\"$DESCRIPTION\"}" >> "$LOG_FILE"

# Also log to a human-readable format
READABLE_LOG="$LOG_DIR/agent-tasks.log"
echo "[$TIMESTAMP] Agent: $AGENT_TYPE - $DESCRIPTION" >> "$READABLE_LOG"

# Output success message (visible in transcript mode)
echo "📝 Logged agent task: $AGENT_TYPE - $DESCRIPTION"

# Allow the operation to proceed
exit 0