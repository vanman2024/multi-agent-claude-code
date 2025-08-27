#!/bin/bash
# Hook: Verify GitHub is synced before asking @claude to test
# Event: UserPromptSubmit
# Purpose: Warn if local changes haven't been pushed before mentioning @claude

# Read the prompt
INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""')

# Check if prompt mentions @claude or testing
if ! echo "$PROMPT" | grep -qiE "@claude|test|verify|review"; then
  # Not asking for testing, pass through
  exit 0
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  exit 0
fi

# Check for unpushed commits
UNPUSHED=$(git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null | wc -l)
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)

if [ "$UNPUSHED" -gt 0 ] || [ "$UNCOMMITTED" -gt 0 ]; then
  WARNING_MSG="⚠️ LOCAL CHANGES NOT SYNCED TO GITHUB ⚠️

You have:
- $UNCOMMITTED uncommitted changes
- $UNPUSHED unpushed commits

@claude can only see what's in GitHub. Your local changes are invisible to the bot.

Options:
1. Let auto-sync handle it (if enabled)
2. Manually push: git add . && git commit -m 'sync' && git push
3. Run: /sync-to-github to force sync

The GitHub @claude bot will test OLD code unless you sync first!"

  # Output warning as context
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "$WARNING_MSG"
  }
}
EOF
fi

exit 0