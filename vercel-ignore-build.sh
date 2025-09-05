#!/bin/bash

# This script determines whether Vercel should build a deployment
# Exit codes: 0 = build, 1 = skip build

echo "🔍 Checking build conditions for commit: $VERCEL_GIT_COMMIT_SHA"

# Always build main branch
if [[ "$VERCEL_GIT_COMMIT_REF" == "main" ]]; then
  echo "✅ Building: main branch always builds"
  exit 0
fi

# For PRs, check if issue checkboxes are complete
if [[ -n "$VERCEL_GIT_PULL_REQUEST_ID" ]]; then
  echo "📋 Pull Request #$VERCEL_GIT_PULL_REQUEST_ID detected"
  
  # Skip build for Copilot PRs (they need human review first)
  if [[ "$VERCEL_GIT_COMMIT_REF" == copilot/* ]]; then
    echo "🤖 Copilot PR detected - skipping automatic deployment"
    echo "❌ Copilot PRs require human review before deployment"
    exit 1
  fi
  
  # Check GitHub API for checkbox status (requires GITHUB_TOKEN in Vercel env)
  if [[ -n "$GITHUB_TOKEN" ]]; then
    echo "🔍 Checking issue checkbox status..."
    
    # Get the PR status checks
    STATUS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
      "https://api.github.com/repos/$VERCEL_GIT_REPO_OWNER/$VERCEL_GIT_REPO_SLUG/commits/$VERCEL_GIT_COMMIT_SHA/status" \
      | grep -o '"state":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    # Check for checkbox completion status
    CHECKBOX_STATUS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
      "https://api.github.com/repos/$VERCEL_GIT_REPO_OWNER/$VERCEL_GIT_REPO_SLUG/commits/$VERCEL_GIT_COMMIT_SHA/statuses" \
      | grep -B2 -A2 "Issue Checkboxes" | grep '"state"' | cut -d'"' -f4)
    
    if [[ "$CHECKBOX_STATUS" == "success" ]]; then
      echo "✅ Issue checkboxes complete - proceeding with build"
      exit 0
    elif [[ "$CHECKBOX_STATUS" == "pending" ]]; then
      echo "⏳ Issue checkboxes still pending - skipping build"
      exit 1
    elif [[ "$CHECKBOX_STATUS" == "failure" ]]; then
      echo "❌ Issue checkboxes failed - skipping build"
      exit 1
    else
      echo "⚠️ Could not determine checkbox status - skipping build for safety"
      exit 1
    fi
  else
    echo "⚠️ No GITHUB_TOKEN available - cannot check checkbox status"
    echo "💡 Add GITHUB_TOKEN to Vercel environment variables"
    # Skip build if we can't verify checkboxes
    exit 1
  fi
fi

# For non-PR branches, skip build
echo "⏭️ Skipping build for feature branch (not a PR)"
exit 1