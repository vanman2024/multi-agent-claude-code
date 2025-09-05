#!/bin/bash

# This script determines whether Vercel should build a deployment
# Exit codes: 0 = build, 1 = skip build

# Always build main branch
if [[ "$VERCEL_GIT_COMMIT_REF" == "main" ]]; then
  echo "✅ Building: main branch always builds"
  exit 0
fi

# Check if this is a PR from our repo
if [[ -n "$VERCEL_GIT_PULL_REQUEST_ID" ]]; then
  echo "✅ Building: Pull request #$VERCEL_GIT_PULL_REQUEST_ID"
  exit 0
fi

# Build all other branches (feature branches, etc.)
echo "✅ Building: Branch $VERCEL_GIT_COMMIT_REF"
exit 0