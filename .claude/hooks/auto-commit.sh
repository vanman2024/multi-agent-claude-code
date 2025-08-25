#!/bin/bash
# Hook: Auto-commit changes after file edits
# Event: PostToolUse (Edit|Write|MultiEdit)
# Purpose: Creates atomic commits as you work locally

# Read the tool input to get file information
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Only proceed if we have a file path
if [ -n "$FILE_PATH" ]; then
  # Check if there are changes to commit
  if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    # Get issue number from branch
    BRANCH=$(git branch --show-current 2>/dev/null)
    ISSUE=$(echo "$BRANCH" | grep -oE '[0-9]+' | head -1)
    
    # Stage the specific file
    git add "$FILE_PATH" 2>/dev/null
    
    # Create descriptive commit message
    FILE_NAME=$(basename "$FILE_PATH")
    if [ -n "$ISSUE" ]; then
      COMMIT_MSG="Update $FILE_NAME for issue #$ISSUE"
    else
      COMMIT_MSG="Update $FILE_NAME"
    fi
    
    # Commit the changes
    git commit -m "$COMMIT_MSG" --no-verify 2>/dev/null
    
    if [ $? -eq 0 ]; then
      echo "✓ Auto-committed: $COMMIT_MSG"
    fi
  fi
fi

# Always exit 0 to not block Claude's workflow
exit 0