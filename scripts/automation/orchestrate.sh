#!/bin/bash

# Multi-Agent Orchestration Script
# This makes Claude and Copilot work together

echo "🎯 Multi-Agent Orchestration System"
echo "===================================="

# Function to assess task complexity
assess_task() {
    local title="$1"
    local body="$2"
    
    # Keywords that indicate Copilot should handle
    if echo "$title $body" | grep -iE "(crud|endpoint|test|component|fix bug|add button|update ui)" > /dev/null; then
        echo "copilot"
    # Keywords that indicate Claude should handle
    elif echo "$title $body" | grep -iE "(architect|design|security|complex|optimize|refactor system)" > /dev/null; then
        echo "claude"
    else
        echo "review"
    fi
}

# Check current workload
echo -e "\n📊 Current Workload:"
echo "-------------------"
COPILOT_COUNT=$(gh issue list --assignee copilot --state open --json number --jq '. | length')
CLAUDE_COUNT=$(gh issue list --assignee @me --state open --json number --jq '. | length')

echo "🤖 Copilot: $COPILOT_COUNT active tasks"
echo "🧠 Claude: $CLAUDE_COUNT active tasks"

# Get unassigned issues
echo -e "\n📋 Analyzing Unassigned Issues:"
echo "-------------------------------"

gh issue list --no-assignee --state open --json number,title,body --jq '.[]' | while read -r issue; do
    NUMBER=$(echo "$issue" | jq -r '.number')
    TITLE=$(echo "$issue" | jq -r '.title')
    BODY=$(echo "$issue" | jq -r '.body // ""')
    
    ASSIGNEE=$(assess_task "$TITLE" "$BODY")
    
    if [ "$ASSIGNEE" = "copilot" ] && [ "$COPILOT_COUNT" -lt 5 ]; then
        echo "→ Assigning #$NUMBER to Copilot: $TITLE"
        gh issue edit "$NUMBER" --add-assignee copilot --add-label "copilot-assigned"
        ((COPILOT_COUNT++))
    elif [ "$ASSIGNEE" = "claude" ]; then
        echo "→ Marking #$NUMBER for Claude: $TITLE"
        gh issue edit "$NUMBER" --add-label "claude-assigned,needs-architecture"
    else
        echo "⚠ Issue #$NUMBER needs manual review: $TITLE"
    fi
done

# Show active PRs
echo -e "\n🔄 Active Pull Requests:"
echo "------------------------"
gh pr list --json number,title,author,isDraft --jq '.[] | "PR #\(.number): \(.title) by \(.author.login) \(if .isDraft then "[DRAFT]" else "" end)"'

# Create status file for both agents to read
cat > .github/AGENT-STATUS.json << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "copilot": {
    "active_tasks": $COPILOT_COUNT,
    "can_accept_more": $([ $COPILOT_COUNT -lt 5 ] && echo "true" || echo "false")
  },
  "claude": {
    "active_tasks": $CLAUDE_COUNT,
    "working_on": "$(git branch --show-current)"
  },
  "ready_for_assignment": $(gh issue list --no-assignee --state open --json number --jq '. | length')
}
EOF

echo -e "\n✅ Orchestration complete! Status saved to .github/AGENT-STATUS.json"