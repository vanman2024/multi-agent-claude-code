#!/bin/bash
# Hook: Automatically sync changes to GitHub for @claude visibility
# Event: PostToolUse (Edit|Write|MultiEdit)
# Purpose: Ensures GitHub @claude bot always sees latest code

# Read the tool input
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')

# Only process file modification tools
if ! echo "$TOOL_NAME" | grep -qE "Edit|Write|MultiEdit"; then
  exit 0
fi

# Get the modified file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""')

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  exit 0
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Skip if on main/master branch (don't auto-push to protected branches)
if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
  echo "⚠️  On protected branch $CURRENT_BRANCH - skipping auto-sync"
  exit 0
fi

# Check if file is tracked by git
if ! git ls-files --error-unmatch "$FILE_PATH" > /dev/null 2>&1; then
  # New file - add it
  git add "$FILE_PATH" 2>/dev/null || exit 0
fi

# Check if there are changes to commit
if git diff --cached --quiet && git diff --quiet "$FILE_PATH"; then
  exit 0  # No changes
fi

# Stage the file
git add "$FILE_PATH"

# Create commit message
COMMIT_MSG="sync: auto-commit $(basename "$FILE_PATH") changes

Auto-synced to GitHub for @claude visibility
Session: ${SESSION_ID:0:8}"

# Commit the change
git commit -m "$COMMIT_MSG" --no-verify > /dev/null 2>&1

# Push to GitHub (without triggering CI if possible)
if git push origin "$CURRENT_BRANCH" --no-verify > /dev/null 2>&1; then
  echo "🔄 Synced to GitHub: $(basename "$FILE_PATH")"
  echo "   Branch: $CURRENT_BRANCH"
  echo "   @claude can now see latest changes"
else
  echo "⚠️  Auto-sync pending (will sync on next manual push)"
fi

exit 0