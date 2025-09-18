#!/bin/bash
# Sync Project Template - Complete Development Environment Setup
# Syncs all development tools, configurations, and AI agent coordination to your project
#
# Usage:
#   ./sync-project-template.sh                    # Full-stack project (backend + frontend testing)
#   ./sync-project-template.sh --backend-only     # Backend-only project (Python/pytest)
#   ./sync-project-template.sh --frontend-only    # Frontend-only project (Playwright/TypeScript)
#   ./sync-project-template.sh --no-testing       # Skip all testing templates

set -e

echo "🚀 Syncing complete development template to project..."
echo ""

# Get current directory
PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_DIR")

echo "📁 Project: $PROJECT_NAME"
echo "📍 Location: $PROJECT_DIR"
echo ""

# Check if already set up
if [ -f "devops/ops/ops" ] && [ -f "pyproject.toml" ]; then
  echo "⚠️  Project template already synced!"
  echo ""
  echo "To re-sync or update, run:"
  echo "  node $(dirname "$0")/setup/sync-project.js"
  exit 0
fi

# Run the project sync
echo "🚀 Running project sync..."
if [ -f "$(dirname "$0")/setup/sync-project.js" ]; then
  node "$(dirname "$0")/setup/sync-project.js" "$PROJECT_DIR" "$@"
else
  echo "❌ Project sync script not found!"
  echo "Make sure you're running this from the template directory"
  exit 1
fi

# DevOps setup is now integrated into sync-project.js
echo "✅ DevOps system setup integrated into main sync process"

echo ""
echo "✅ Project template sync complete!"
echo ""
echo "📋 What was configured:"
echo "  • AI Agent coordination (Claude, Copilot, Qwen, Gemini, Codex)"
echo "  • Complete DevOps system (devops/ops/, devops/deploy/, devops/ci/)"
echo "  • Testing architecture (testing/backend/ + testing/frontend/ as appropriate)"
echo "  • Development environment setup (.env.example, gitignore, agent config)"
echo "  • Project-specific configuration and documentation"
echo "  • VS Code settings with file icons and extensions"
echo "  • Docker development environment (Python/Node.js)"
echo "  • GitHub workflows for CI/CD"
echo "  • Testing standards and configurations"
echo "  • MCP server configurations with FastMCP patterns"
echo "  • MCP testing framework (backend-tests/mcp/ with FastMCP runner)"
echo "  • Development hooks and tools"
echo "  • Environment variable templates"
echo ""
echo "🎯 Next steps:"
echo "  1. Copy .env.example to .env and fill in your API keys"
echo "  2. Run './scripts/ops status' to check your automation setup"
echo "  3. Start using @symbol coordination with ops CLI:"
echo "     - @claude for complex development tasks (always use 'ops qa')"
echo "     - @copilot for simple implementation tasks (Complexity ≤2, Size XS-S)"
echo "     - @qwen for performance optimization (2000 requests/day)"
echo "     - @gemini for research and documentation"
echo "     - @codex for interactive prototyping"
echo ""
echo "🔗 MCP Server Testing (if using Python):"
echo "  • Install FastMCP: pip install fastmcp"
echo "  • Run MCP tests: pytest backend-tests/mcp -v -m mcp"
echo "  • Check backend-tests/mcp/fastmcp_runner.py for FastMCP patterns"
echo ""
echo "📖 Learn more:"
echo "  • Check AGENTS.md for detailed agent coordination info"  
echo "  • Read VERSIONING.md for release and versioning documentation"
echo "  • See backend-tests/README.md for MCP testing documentation"
