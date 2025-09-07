# MCP Servers Setup Guide

MCP (Model Context Protocol) servers give Claude Code additional capabilities. This template requires these essential servers for full functionality.

## Required MCP Servers

### 1. GitHub MCP Server (HTTP Transport)
Provides full GitHub API access for issues, PRs, discussions, and repository management.

```bash
# Get GitHub token from gh CLI
GITHUB_TOKEN=$(gh auth token)

# Add the GitHub MCP server with HTTP transport and authentication
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"

# Or with your personal access token directly:
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer YOUR_GITHUB_PAT"
```

Note: This uses HTTP transport with Bearer token authentication. The endpoint may return 500 on health checks but works for MCP protocol commands.

### 2. Playwright MCP Server
Enables browser automation and testing for frontend development.

```bash
# First, install Playwright browsers (Chromium, Firefox, WebKit)
npx playwright install

# If you get permission errors, you may need:
npx playwright install-deps  # Install system dependencies

# Then add Playwright MCP server
claude mcp add playwright -- npx @modelcontextprotocol/server-playwright
```

Note: Playwright requires browser binaries. The first command downloads Chromium, Firefox, and WebKit.

### 3. Postman MCP Server
Enables API testing and collection management.

```bash
# Install Postman MCP server
claude mcp add postman -- npx @modelcontextprotocol/server-postman
```

### 4. Supabase MCP Server
Database and authentication management (if using Supabase).

```bash
# Install Supabase MCP server
claude mcp add supabase -- npx @modelcontextprotocol/server-supabase
```

### 5. Memory MCP Server
Persistent memory storage for context between Claude sessions.

```bash
# Install Memory MCP server
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory
```

Note: Memory server provides persistent storage between sessions. No API key required.

## Quick Setup Script

Create this script to add all servers at once:

```bash
#!/bin/bash
# setup-mcp-servers.sh

echo "Setting up MCP servers for Multi-Agent Development..."

# Check gh CLI is authenticated
if ! gh auth status &>/dev/null; then
  echo "❌ GitHub CLI not authenticated. Run: gh auth login"
  exit 1
fi

# GitHub MCP (HTTP transport with gh token)
echo "Adding GitHub MCP server..."
GITHUB_TOKEN=$(gh auth token)
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"

# Playwright for browser testing (no key required)
echo "Installing Playwright browsers..."
npx playwright install
echo "Adding Playwright MCP server..."
claude mcp add playwright -- npx @modelcontextprotocol/server-playwright

# Postman for API testing (requires POSTMAN_API_KEY in environment)
echo "Adding Postman MCP server..."
# Note: Set POSTMAN_API_KEY environment variable first:
# export POSTMAN_API_KEY="your-postman-api-key"
claude mcp add postman -- npx @modelcontextprotocol/server-postman

# Supabase for database (requires SUPABASE_URL and key)
echo "Adding Supabase MCP server..."
claude mcp add supabase -- npx @modelcontextprotocol/server-supabase

# Memory for persistent storage (no key required)
echo "Adding Memory MCP server..."
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory

echo "✅ MCP servers configured!"
echo "Run 'claude mcp list' to verify installation"
```

## Required CLI Tools

These CLI tools must be installed for the agents to work properly:

### 1. GitHub CLI (`gh`)
```bash
# macOS
brew install gh

# Linux/WSL
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

### 2. Newman (Postman CLI)
```bash
# Install globally via npm
npm install -g newman

# Verify installation
newman --version
```

### 3. Vercel CLI
```bash
# Install globally
npm install -g vercel

# Login
vercel login
```

### 4. Playwright (for testing)
```bash
# Install in your project
npm init playwright@latest

# Or globally
npm install -g playwright
playwright install  # Install browsers
```

## Verification

After installation, verify everything is working:

```bash
# Check MCP servers
claude mcp list

# Check CLI tools
gh --version
newman --version
vercel --version
playwright --version
```

## Using the /add-mcp Command

Once the template is set up, you can add additional MCP servers using:

```bash
# In Claude Code
/add-mcp
```

This will guide you through adding servers like:
- `github` - GitHub API access (required for this template)
- `playwright` - Browser automation and testing
- `postman` - API testing and collections
- `supabase` - Database and authentication
- `filesystem` - File system access
- `memory` - Persistent memory storage between sessions
- `slack` - Slack integration (optional)
- `notion` - Notion workspace (optional)
- And many more...

## MCP Server Configuration

MCP servers are configured per-project by default. Configuration is stored in:
- Project: `.claude/mcp_servers.json`
- User: `~/.config/claude/mcp_servers.json`

## Troubleshooting

### MCP server not working
1. Check server is running: `claude mcp list`
2. **If MCP won't add to a project**: Run `claude init` first to reinitialize Claude
3. Restart Claude Code: Exit and run `claude` again
4. Check authentication: Some servers need API keys

### MCP server shows "incompatible auth server" error
If you get this error when adding an MCP server to a project:
```bash
# Fix: Reinitialize Claude in the project
cd /your/project/directory
claude init

# Then try adding the MCP server again
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $(gh auth token)"
```

### CLI tool not found
1. Ensure tool is in PATH
2. Restart terminal after installation
3. Check installation with `which [tool-name]`

### Authentication issues
1. Re-authenticate: `gh auth login`, `vercel login`, etc.
2. Check API keys are set in environment
3. Verify tokens have correct permissions

## Environment Variables for MCP

Add to your `.env` file:
```bash
# GitHub
GITHUB_TOKEN=ghp_xxxx

# Postman
POSTMAN_API_KEY=PMAK-xxxx

# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_ANON_KEY=xxxx

# DigitalOcean
DIGITALOCEAN_ACCESS_TOKEN=dop_xxxx

# Vercel
VERCEL_TOKEN=xxxx
```

These environment variables will be used by both MCP servers and CLI tools.