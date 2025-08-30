#!/bin/bash
# Setup local development environment
# Usage: ./scripts/development/setup-local-env.sh

echo "=== Setting Up Local Development Environment ==="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
command -v git >/dev/null 2>&1 || { echo "✗ git is required"; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "✗ GitHub CLI (gh) is required"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "✗ jq is required"; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "⚠ Claude Code CLI not found (optional)"; }

echo "✓ Prerequisites checked"
echo ""

# Setup directories
echo "Creating project directories..."
mkdir -p .claude/{hooks,logs,commands}
mkdir -p scripts/{automation,development,testing,utilities}
mkdir -p tests/{hooks,slash-commands,subagents,github-workflows,integration}
echo "✓ Directories created"
echo ""

# Make scripts executable
echo "Setting script permissions..."
find .claude/hooks -name "*.sh" -o -name "*.py" | xargs chmod +x 2>/dev/null
find scripts -name "*.sh" | xargs chmod +x 2>/dev/null
find tests -name "*.sh" | xargs chmod +x 2>/dev/null
echo "✓ Scripts made executable"
echo ""

# Check GitHub auth
echo "Checking GitHub authentication..."
if gh auth status >/dev/null 2>&1; then
    echo "✓ GitHub authenticated"
else
    echo "✗ Not authenticated with GitHub"
    echo "  Run: gh auth login"
fi
echo ""

# Check Claude Code hooks
echo "Checking Claude Code hooks..."
if [ -f .claude/settings.json ]; then
    HOOK_COUNT=$(jq '.hooks | to_entries | length' .claude/settings.json 2>/dev/null)
    echo "✓ Found $HOOK_COUNT hook categories"
else
    echo "⚠ No Claude Code settings found"
fi
echo ""

# Git configuration
echo "Git repository status:"
git status --short
echo ""

# Environment variables
echo "Environment setup:"
echo "export CLAUDE_PROJECT_DIR='$(pwd)'"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Run: export CLAUDE_PROJECT_DIR='$(pwd)'"
echo "2. Reload Claude Code hooks with /hooks command"
echo "3. Run tests: ./scripts/testing/run-all-tests.sh"
echo "4. Start developing!"