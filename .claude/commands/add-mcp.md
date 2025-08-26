---
allowed-tools: Bash(*), Read(*)
description: Add essential MCP servers to your project
---

# Add MCP Servers Command

## Instructions for Assistant

This command helps users add the essential MCP servers needed for the Multi-Agent Development Framework.

### Available Servers

1. **github** - Official GitHub MCP server (HTTP endpoint from GitHub Copilot)
2. **playwright** - Browser automation and testing
3. **postman** - API testing and collections  
4. **supabase** - Database and authentication
5. **filesystem** - File system access
6. **all** - Add all recommended servers (github, playwright, postman, supabase)

### Process

1. **Check what's already installed:**
```bash
claude mcp list
```

2. **Add requested servers based on user input:**

#### GitHub MCP Server (REQUIRED - HTTP Transport)
```bash
# Get GitHub token from gh CLI
GITHUB_TOKEN=$(gh auth token)

# Add the GitHub MCP server with authentication
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"
```
Note: This is the OFFICIAL GitHub Copilot MCP endpoint. Requires GitHub CLI (`gh`) to be authenticated.

#### Playwright MCP Server (for frontend-tester agent)
```bash
claude mcp add playwright -- npx @modelcontextprotocol/server-playwright
```
Note: No API key required.

#### Postman MCP Server (for backend-tester agent)  
```bash
# Requires POSTMAN_API_KEY environment variable
claude mcp add postman -- npx @modelcontextprotocol/server-postman
```
Note: Requires POSTMAN_API_KEY in environment.

#### Supabase MCP Server (for database)
```bash
# For local Supabase project
claude mcp add supabase -- npx @modelcontextprotocol/server-supabase

# OR for hosted HTTP version (if available)
# claude mcp add --transport http supabase https://your-supabase-mcp.com -H "Authorization: Bearer YOUR_KEY"
```
Note: Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables.

#### Filesystem MCP Server (optional)
```bash
claude mcp add filesystem -- npx @modelcontextprotocol/server-filesystem /path/to/project
```

3. **Verify installation:**
```bash
claude mcp list
```

4. **Set up required environment variables:**
```bash
# Check if .env exists
if [ ! -f .env ]; then
  echo "Creating .env file..."
  cat > .env << 'EOF'
# Postman (required for postman MCP)
POSTMAN_API_KEY=

# Supabase (required for supabase MCP)
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

# Add your values above
EOF
  echo "✅ Created .env file. Please add your API keys."
else
  echo "✅ .env file already exists"
fi
```

## Usage Examples

### User: "add github mcp"
Add the GitHub MCP server using HTTP transport and gh CLI token.

### User: "add all mcp servers"
Add github, playwright, postman, and supabase servers.

### User: "setup mcp for frontend development"
Add github and playwright servers.

### User: "setup mcp for backend api"
Add github, postman, and supabase servers.

## Important Notes

- **GitHub MCP** uses HTTP transport with the official GitHub Copilot API endpoint
- **Playwright** doesn't require any API keys
- **Postman** requires POSTMAN_API_KEY
- **Supabase** can be local (stdio) or hosted (HTTP)
- Restart Claude Code after adding servers: exit and run `claude` again
- Configuration is stored in `.claude/mcp_servers.json`

## Quick Install Script

For users who want all servers at once:

```bash
#!/bin/bash
# Quick setup all MCP servers

echo "🔧 Setting up MCP servers..."

# Check gh CLI is authenticated
if ! gh auth status &>/dev/null; then
  echo "❌ GitHub CLI not authenticated. Run: gh auth login"
  exit 1
fi

# GitHub (HTTP transport with gh token)
echo "Adding GitHub MCP..."
GITHUB_TOKEN=$(gh auth token)
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"

# Playwright (no key required)
echo "Adding Playwright MCP..."
claude mcp add playwright -- npx @modelcontextprotocol/server-playwright

# Postman (requires API key)
echo "Adding Postman MCP..."
if [ -z "$POSTMAN_API_KEY" ]; then
  echo "⚠️  POSTMAN_API_KEY not set. Add to .env file"
fi
claude mcp add postman -- npx @modelcontextprotocol/server-postman

# Supabase (requires URL and key)
echo "Adding Supabase MCP..."
if [ -z "$SUPABASE_URL" ]; then
  echo "⚠️  SUPABASE_URL not set. Add to .env file"
fi
claude mcp add supabase -- npx @modelcontextprotocol/server-supabase

echo "✅ MCP servers configured!"
echo "📝 Remember to set API keys in your .env file"
echo "🔄 Restart Claude Code for changes to take effect"

claude mcp list
```

## About Hosted MCP Servers

For custom MCP servers (like your Supabase HTTP server), they can be hosted on:
- **DigitalOcean App Platform** - Deploy as a Python/Node app
- **Vercel Functions** - For serverless MCP endpoints
- **Any cloud provider** - As long as it has a public HTTPS endpoint

Example for hosted custom server:
```bash
# If you have a custom MCP server deployed
claude mcp add --transport http custom-server https://your-mcp-server.digitalocean.app -H "Authorization: Bearer YOUR_API_KEY"
```

The key management for hosted servers can be:
1. **User provides their own key** - Most secure
2. **Shared key for template** - Less secure but easier
3. **No auth for read-only operations** - Simplest for public data