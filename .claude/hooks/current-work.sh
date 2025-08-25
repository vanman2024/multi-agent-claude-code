#!/bin/bash
# Hook: Inject current issue context into every prompt
# Event: UserPromptSubmit
# Purpose: Ensures Claude always knows what issue is being worked on

# Get current branch and extract issue number
BRANCH=$(git branch --show-current 2>/dev/null)
ISSUE=$(echo "$BRANCH" | grep -oE '[0-9]+' | head -1)

if [ -n "$ISSUE" ]; then
  # Get issue details from GitHub
  ISSUE_DATA=$(gh issue view "$ISSUE" --json title,body,labels,assignees 2>/dev/null)
  
  if [ $? -eq 0 ]; then
    # Output context that will be injected into the prompt
    echo "📋 Currently working on Issue #$ISSUE"
    echo "$ISSUE_DATA" | jq -r '"Title: " + .title'
    echo "$ISSUE_DATA" | jq -r '"Labels: " + ([.labels[].name] | join(", "))'
    echo "$ISSUE_DATA" | jq -r '"Assignees: " + ([.assignees[].login] | join(", "))'
    echo "Branch: $BRANCH"
    echo "---"
  fi
fi

# Always exit 0 to not block the prompt
exit 0