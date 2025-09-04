#!/bin/bash

# This script tells Vercel whether to build or skip deployment
# Exit 0 = skip build, Exit 1 = proceed with build
# Configure in Vercel: Project Settings → Git → Ignored Build Step Command

echo "🔍 Checking if deployment should proceed..."

# Get the PR number from Vercel environment
if [ -z "$VERCEL_GIT_PULL_REQUEST_ID" ]; then
  echo "✅ Not a PR - proceeding with deployment"
  exit 1  # Proceed with build
fi

echo "📋 PR #$VERCEL_GIT_PULL_REQUEST_ID detected"

# Use GitHub API to check the PR
PR_DATA=$(curl -s "https://api.github.com/repos/$VERCEL_GIT_REPO_OWNER/$VERCEL_GIT_REPO_SLUG/pulls/$VERCEL_GIT_PULL_REQUEST_ID")

# Extract linked issue from PR body
ISSUE_NUMBER=$(echo "$PR_DATA" | grep -oP '(?:Closes|Fixes|Resolves)\s+#\K\d+' | head -1)

if [ -z "$ISSUE_NUMBER" ]; then
  echo "⚠️  No linked issue found - proceeding with deployment"
  exit 1  # Proceed with build
fi

echo "🔗 Found linked issue #$ISSUE_NUMBER"

# Get issue data
ISSUE_DATA=$(curl -s "https://api.github.com/repos/$VERCEL_GIT_REPO_OWNER/$VERCEL_GIT_REPO_SLUG/issues/$ISSUE_NUMBER")

# Count checkboxes
UNCHECKED=$(echo "$ISSUE_DATA" | grep -o '\- \[ \]' | wc -l)
CHECKED=$(echo "$ISSUE_DATA" | grep -o '\- \[x\]' | wc -l)
TOTAL=$((UNCHECKED + CHECKED))

echo "📊 Issue #$ISSUE_NUMBER status:"
echo "   Checked: $CHECKED"
echo "   Unchecked: $UNCHECKED"
echo "   Total: $TOTAL"

if [ $UNCHECKED -gt 0 ]; then
  echo "❌ BLOCKING DEPLOYMENT: $UNCHECKED unchecked requirements in issue #$ISSUE_NUMBER"
  echo "   Complete all checkboxes before deployment"
  exit 0  # Skip build
else
  echo "✅ All requirements complete - proceeding with deployment"
  exit 1  # Proceed with build
fi