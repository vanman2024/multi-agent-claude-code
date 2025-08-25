---
allowed-tools: Read(*), Bash(*), Write(*)
description: Global MCP server setup - add essential MCP servers to any project
---

# Global MCP Server Setup

## Instructions for Assistant

This command adds MCP servers to ANY project using the global configuration at:
`/home/gotime2022/Projects/mcp-kernel-new/.claude/project_configs/seedmcp.json`

The assistant should:

1. **Read the global config** at `/home/gotime2022/Projects/mcp-kernel-new/.claude/project_configs/seedmcp.json`

2. **Determine which servers to add** based on user request:
   - `all` - Add all servers from seedmcp.json config
   - `github` - GitHub Copilot MCP API 
   - `supabase` - Supabase HTTP server (port 8013)
   - `filesystem` - Filesystem HTTP server (port 8006)
   - `memory` - Memory HTTP server (port 8007)
   - `sequential` - Sequential thinking HTTP server (port 8016)
   - Or specific server names from the config

3. **Essential Servers Configuration (from seedmcp.json):**

   **Official GitHub Server (HTTP - GitHub Copilot API):**
   ```bash
   # First, get the GitHub token using gh CLI
   GITHUB_TOKEN=$(gh auth token)
   
   # Add the GitHub MCP server with authentication
   claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"
   ```
   Note: Requires GitHub CLI (`gh`) to be authenticated. If not, run `gh auth login` first.

   **Supabase HTTP Server (Your Custom):**
   ```bash
   claude mcp add --transport http supabase http://localhost:8013
   ```
   Note: Make sure the HTTP server is running

   **Official Filesystem Server (STDIO):**
   ```bash
   claude mcp add filesystem "npx" "-y" "@modelcontextprotocol/server-filesystem" "/home/gotime2022"
   ```

   **PostgreSQL Server (if needed):**
   ```bash
   claude mcp add postgres "npx" "-y" "@modelcontextprotocol/server-postgres" "postgresql://localhost/mydb"
   ```

3. **Setup Process:**
   
   a. First check if servers are already added:
   ```bash
   claude mcp list
   ```

   b. Ensure GitHub CLI is authenticated:
   ```bash
   # Check if gh is authenticated
   gh auth status
   
   # If not authenticated, login
   gh auth login
   ```

   c. Add requested servers using appropriate commands above with token from gh CLI

   d. Verify installation:
   ```bash
   claude mcp list
   ```

4. **Starting HTTP Servers (if using custom ones):**
   
   For Supabase HTTP server:
   ```bash
   # Navigate to server directory
   cd /home/gotime2022/Projects/mcp-kernel-new/servers/http/supabase-http-mcp
   
   # Start the server
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python src/supabase_server.py &
   ```

5. **CLI Tools Alternative:**
   
   Instead of MCP servers, you can use CLI tools directly:
   - **GitHub CLI**: `gh` command (already installed)
   - **Vercel CLI**: `vercel` command
   - **DigitalOcean CLI**: `doctl` command
   - **Supabase CLI**: `supabase` command

   Example installations:
   ```bash
   # Vercel CLI
   npm i -g vercel
   
   # Supabase CLI
   npm i -g supabase
   
   # DigitalOcean CLI
   snap install doctl
   ```

## Common Usage Examples:

1. **Add essential servers for web development:**
   ```
   User: Add github and supabase servers
   Assistant: Adds official GitHub server and Supabase HTTP server
   ```

2. **Add all recommended servers:**
   ```
   User: Add all MCP servers
   Assistant: Adds GitHub, Supabase, and Filesystem
   ```

3. **Project-specific setup:**
   ```
   User: Setup MCP for a Next.js project
   Assistant: Adds GitHub, Filesystem, and possibly Vercel-related servers
   ```

## Notes:
- Official MCP servers (stdio) are preferred over HTTP versions when available
- HTTP servers require separate processes to be running
- CLI tools can often replace MCP servers for deployment tasks
- Always verify with `claude mcp list` after adding