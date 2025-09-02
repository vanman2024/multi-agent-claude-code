#!/bin/bash

# Gemini Status Check Script
# This script verifies if Gemini AI is properly configured and working

set -e

echo "🔍 Checking Gemini AI Status..."
echo "================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

# Check GitHub CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found - install from https://cli.github.com"
    exit 1
fi

echo "✅ Git repository detected"
echo "✅ GitHub CLI available"

# Check if required workflow files exist
WORKFLOW_DIR=".github/workflows"
REQUIRED_WORKFLOWS=(
    "gemini-dispatch.yml"
    "gemini-review.yml"
    "gemini-triage.yml"
    "gemini-invoke.yml"
)

echo ""
echo "🔧 Checking Gemini workflows..."

missing_workflows=()
for workflow in "${REQUIRED_WORKFLOWS[@]}"; do
    if [[ -f "$WORKFLOW_DIR/$workflow" ]]; then
        echo "✅ $workflow found"
    else
        echo "❌ $workflow missing"
        missing_workflows+=("$workflow")
    fi
done

if [[ ${#missing_workflows[@]} -gt 0 ]]; then
    echo ""
    echo "❌ Missing required workflow files:"
    for workflow in "${missing_workflows[@]}"; do
        echo "   - $workflow"
    done
    echo "   Run setup to add missing workflows"
    exit 1
fi

# Check GitHub secrets
echo ""
echo "🔐 Checking GitHub secrets..."

# Try to list secrets (may fail if not authenticated)
if secrets_output=$(gh secret list 2>/dev/null); then
    if echo "$secrets_output" | grep -q "GEMINI_API_KEY"; then
        echo "✅ GEMINI_API_KEY secret is configured"
    else
        echo "❌ GEMINI_API_KEY secret is missing"
        echo "   Set it with: gh secret set GEMINI_API_KEY --body 'your-api-key'"
        exit 1
    fi
else
    echo "⚠️  Could not check secrets (authentication issue)"
    echo "   Make sure you're authenticated: gh auth login"
fi

# Check recent workflow runs
echo ""
echo "📊 Checking recent Gemini workflow runs..."

if run_output=$(gh run list --workflow=gemini-dispatch.yml --limit=3 2>/dev/null); then
    if [[ -n "$run_output" ]]; then
        echo "✅ Recent Gemini dispatch runs found:"
        echo "$run_output" | head -4  # Include header + 3 runs
    else
        echo "⚠️  No recent Gemini workflow runs found"
        echo "   This might be normal if no issues/PRs were recently created"
    fi
else
    echo "⚠️  Could not check workflow runs"
    echo "   Make sure repository exists on GitHub and you have access"
fi

# Check repository permissions
echo ""
echo "🔑 Checking repository permissions..."
if repo_info=$(gh repo view --json owner,name,permissions 2>/dev/null); then
    repo_name=$(echo "$repo_info" | jq -r '.owner.login + "/" + .name')
    echo "✅ Repository: $repo_name"
    
    # Check if Actions have write permissions (this is indirect)
    settings_url="https://github.com/$repo_name/settings/actions"
    echo "   ℹ️  Verify Actions have 'Read and write permissions' at:"
    echo "   $settings_url"
else
    echo "⚠️  Could not check repository info"
fi

echo ""
echo "🎯 Quick Test Instructions:"
echo "1. Create a new issue in your repository"
echo "2. Wait 30-60 seconds"
echo "3. Check if the issue gets automatically labeled"
echo "4. Or comment '@gemini-cli /triage' in any existing issue"

echo ""
echo "📖 For more help:"
echo "- Setup: docs/GEMINI_SETUP.md"
echo "- Usage: docs/GEMINI_USER_GUIDE.md"
echo "- Troubleshooting: docs/GEMINI_TROUBLESHOOTING.md"

echo ""
echo "✨ Gemini status check complete!"