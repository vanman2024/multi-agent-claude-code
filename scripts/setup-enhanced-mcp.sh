#!/bin/bash
set -euo pipefail

# Setup Enhanced MCP Servers for Multi-Agent Development Framework
# This script sets up the new AI-powered MCP servers with file access capabilities

echo "🚀 Setting up Enhanced MCP Servers for Multi-Agent Development Framework"
echo ""

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
  echo "❌ Node.js not found. Please install Node.js 18+ first."
  exit 1
fi

if ! command_exists npm; then
  echo "❌ npm not found. Please install npm first."
  exit 1
fi

if ! command_exists claude; then
  echo "❌ Claude Code CLI not found. Please install Claude Code first."
  exit 1
fi

if ! command_exists gh; then
  echo "❌ GitHub CLI not found. Please install GitHub CLI first."
  exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install
echo "✅ Dependencies installed"
echo ""

# Make MCP server files executable
echo "🔧 Setting up MCP server permissions..."
chmod +x scripts/mcp-servers/*.js
echo "✅ Permissions set"
echo ""

# Check if .env file exists, create if not
if [ ! -f .env ]; then
  echo "📝 Creating .env file from template..."
  cp .env.example .env
  echo "✅ .env file created. Please configure your API keys:"
  echo "   - TOGETHER_AI_API_KEY (get from: https://api.together.xyz/)"
  echo "   - GOOGLE_API_KEY (get from: https://makersuite.google.com/app/apikey)"
  echo "   - HUGGINGFACE_API_TOKEN (get from: https://huggingface.co/settings/tokens)"
  echo ""
else
  echo "✅ .env file already exists"
fi

# Function to add MCP server with error handling
add_mcp_server() {
  local name="$1"
  local command="$2"
  local description="$3"
  local env_var="$4"
  
  echo "🔧 Adding $description..."
  
  if [ -n "$env_var" ] && [ -z "${!env_var:-}" ]; then
    echo "⚠️  $env_var not set. Skipping $name (you can add it later)"
    return 0
  fi
  
  if claude mcp add "$name" -- $command; then
    echo "✅ $description added successfully"
  else
    echo "❌ Failed to add $description"
    return 1
  fi
}

# Add enhanced MCP servers
echo "🤖 Adding Enhanced AI MCP Servers..."
echo ""

# Load environment variables if .env exists
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Add Together AI MCP Server
add_mcp_server "together-ai" \
  "node $(pwd)/scripts/mcp-servers/together-ai-mcp-server.js" \
  "Together AI MCP Server (Complex Code Generation)" \
  "TOGETHER_AI_API_KEY"

# Add Gemini MCP Server
add_mcp_server "gemini-pro" \
  "node $(pwd)/scripts/mcp-servers/gemini-mcp-server.js" \
  "Gemini 1.5 Pro MCP Server (Testing & Documentation)" \
  "GOOGLE_API_KEY"

# Add HuggingFace MCP Server
add_mcp_server "huggingface" \
  "node $(pwd)/scripts/mcp-servers/huggingface-mcp-server.js" \
  "HuggingFace Inference MCP Server (Specialized Models)" \
  "HUGGINGFACE_API_TOKEN"

echo ""
echo "🎉 Enhanced MCP Servers setup complete!"
echo ""

# Display current MCP servers
echo "📊 Current MCP Servers:"
claude mcp list || echo "Run 'claude mcp list' to see configured servers"
echo ""

# Final instructions
echo "📚 Next Steps:"
echo "1. Configure API keys in .env file if you haven't already"
echo "2. Restart Claude Code for changes to take effect"
echo "3. Use '/mcp-delegate' command for task delegation"
echo "4. Use '/add-mcp ai-enhanced' to add servers individually"
echo ""

echo "🔗 API Key Links:"
echo "- Together AI: https://api.together.xyz/"
echo "- Google Gemini: https://makersuite.google.com/app/apikey"
echo "- HuggingFace: https://huggingface.co/settings/tokens"
echo ""

echo "📖 Documentation:"
echo "- PROJECT_CONTEXT.md - Current project state"
echo "- docs/AI_TASK_ALLOCATION.md - Agent specialization guide"
echo "- .claude/commands/mcp-delegate.md - Task delegation commands"
echo ""

echo "✨ Multi-Agent Development Framework is ready!"