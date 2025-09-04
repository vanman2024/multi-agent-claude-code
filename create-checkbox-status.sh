#!/bin/bash

# Get the latest commit SHA
SHA=$(git rev-parse HEAD)
REPO="vanman2024/multi-agent-claude-code"

# Check issue #134 for unchecked boxes
ISSUE_BODY=$(gh issue view 134 --json body -q '.body')
UNCHECKED=$(echo "$ISSUE_BODY" | grep -c "\- \[ \]" || true)
UNCHECKED=${UNCHECKED:-0}
CHECKED=$(echo "$ISSUE_BODY" | grep -ci "\- \[x\]" || true)
CHECKED=${CHECKED:-0}
TOTAL=$((UNCHECKED + CHECKED))

echo "Issue #134 status:"
echo "Checked: $CHECKED"
echo "Unchecked: $UNCHECKED"
echo "Total: $TOTAL"

if [ $UNCHECKED -gt 0 ]; then
  echo "Creating FAILURE status - $UNCHECKED unchecked boxes"
  gh api \
    repos/$REPO/statuses/$SHA \
    --method POST \
    --field state="failure" \
    --field context="Issue Checkboxes" \
    --field description="$UNCHECKED unchecked boxes in issue #134" \
    --field target_url="https://github.com/$REPO/issues/134"
else
  echo "Creating SUCCESS status - all boxes checked"
  gh api \
    repos/$REPO/statuses/$SHA \
    --method POST \
    --field state="success" \
    --field context="Issue Checkboxes" \
    --field description="All $TOTAL requirements complete" \
    --field target_url="https://github.com/$REPO/issues/134"
fi

echo "Status created for commit $SHA"