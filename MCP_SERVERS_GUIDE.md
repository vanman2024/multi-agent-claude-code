# MCP Servers Guide for Claude Code

## Overview

Claude Code can connect to hundreds of external tools and data sources through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), an open-source standard for AI-tool integrations.

## Quick Start Commands

```bash
# Add a local stdio server
claude mcp add <name> -- <command> [args...]

# Add a remote SSE server
claude mcp add --transport sse <name> <url>

# Add a remote HTTP server
claude mcp add --transport http <name> <url>

# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get <server-name>

# Remove a server
claude mcp remove <server-name>

# Check server status (within Claude Code)
/mcp
```

## Popular MCP Servers

### Development & Testing Tools

| Server | Description | Command |
|--------|-------------|---------|
| **Sentry** | Monitor errors, debug production issues | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **Socket** | Security analysis for dependencies | `claude mcp add --transport http socket https://mcp.socket.dev/` |
| **Hugging Face** | Access Hugging Face Hub and Gradio AI Applications | `claude mcp add --transport http huggingface https://huggingface.co/mcp` |
| **Jam** | Debug with AI agents using Jam recordings | `claude mcp add --transport http jam https://mcp.jam.dev/mcp` |

### Project Management & Documentation

| Server | Description | Command |
|--------|-------------|---------|
| **Asana** | Interact with your Asana workspace | `claude mcp add --transport sse asana https://mcp.asana.com/sse` |
| **Atlassian** | Manage Jira tickets and Confluence docs | `claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse` |
| **Linear** | Issue tracking and project management | `claude mcp add --transport sse linear https://mcp.linear.app/sse` |
| **Notion** | Read docs, update pages, manage tasks | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Monday** | Manage monday.com boards | `claude mcp add --transport sse monday https://mcp.monday.com/sse` |
| **Box** | Enterprise content management | `claude mcp add --transport http box https://mcp.box.com/` |
| **Fireflies** | Extract insights from meeting transcripts | `claude mcp add --transport http fireflies https://api.fireflies.ai/mcp` |
| **Intercom** | Access customer conversations and tickets | `claude mcp add --transport sse intercom https://mcp.intercom.com/sse` |
| **ClickUp** | Task management (requires API key) | `claude mcp add clickup --env CLICKUP_API_KEY=YOUR_KEY --env CLICKUP_TEAM_ID=YOUR_ID -- npx -y @hauptsache.net/clickup-mcp` |

### Databases & Data Management

| Server | Description | Command |
|--------|-------------|---------|
| **Airtable** | Read/write records, manage bases | `claude mcp add airtable --env AIRTABLE_API_KEY=YOUR_KEY -- npx -y airtable-mcp-server` |
| **HubSpot** | Access and manage CRM data | `claude mcp add --transport http hubspot https://mcp.hubspot.com/anthropic` |
| **Daloopa** | Financial data from SEC filings | `claude mcp add --transport http daloopa https://mcp.daloopa.com/server/mcp` |

### Payments & Commerce

| Server | Description | Command |
|--------|-------------|---------|
| **Stripe** | Payment processing and subscriptions | `claude mcp add --transport http stripe https://mcp.stripe.com` |
| **Square** | Payments, inventory, orders | `claude mcp add --transport sse square https://mcp.squareup.com/sse` |
| **PayPal** | Payment processing and transactions | `claude mcp add --transport sse paypal https://mcp.paypal.com/sse` |
| **Plaid** | Banking data and account linking | `claude mcp add --transport sse plaid https://api.dashboard.plaid.com/mcp/sse` |

### Design & Media

| Server | Description | Command |
|--------|-------------|---------|
| **Figma** | Access designs, export assets (requires Figma Desktop) | `claude mcp add --transport http figma-dev-mode-mcp-server http://127.0.0.1:3845/mcp` |
| **Canva** | Browse and generate designs | `claude mcp add --transport http canva https://mcp.canva.com/mcp` |
| **invideo** | Video creation capabilities | `claude mcp add --transport sse invideo https://mcp.invideo.io/sse` |

### Infrastructure & DevOps

| Server | Description | Command |
|--------|-------------|---------|
| **Vercel** | Manage projects and deployments | `claude mcp add --transport http vercel https://mcp.vercel.com/` |
| **Netlify** | Deploy and manage websites | `claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp` |
| **Cloudflare** | Build applications, analyze traffic | See [Cloudflare docs](https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/) |
| **Stytch** | Configure authentication services | `claude mcp add --transport http stytch http://mcp.stytch.dev/mcp` |

### Automation & Integration

| Server | Description | Command |
|--------|-------------|---------|
| **Zapier** | Connect to 8,000+ apps | Generate URL at [mcp.zapier.com](https://mcp.zapier.com) |
| **Workato** | Workflow automation | See [Workato docs](https://docs.workato.com/mcp.html) |

## Installation Scopes

### Local Scope (Default)
- Private to you, only in current project
- `claude mcp add my-server -- command`

### Project Scope
- Shared with team via `.mcp.json`
- `claude mcp add shared-server --scope project -- command`

### User Scope
- Available across all your projects
- `claude mcp add my-tool --scope user -- command`

## Authentication

Many cloud services require OAuth authentication:

1. Add the server: `claude mcp add --transport http service https://service.com/mcp`
2. In Claude Code, run: `/mcp`
3. Select "Authenticate" and follow browser prompts

## Environment Variables

For servers requiring API keys:

```bash
# Single environment variable
claude mcp add myserver --env API_KEY=your-key -- command

# Multiple environment variables
claude mcp add myserver \
  --env API_KEY=key \
  --env API_SECRET=secret \
  -- command
```

## Using MCP Resources

Reference MCP resources with @ mentions:

```
> Can you analyze @github:issue://123 and suggest a fix?
> Please review @docs:file://api/authentication
> Compare @postgres:schema://users with @docs:file://database/user-model
```

## MCP Prompts as Slash Commands

MCP servers can expose prompts as slash commands:

```
> /mcp__github__list_prs
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug in login flow" high
```

## Advanced Configuration

### Import from Claude Desktop

```bash
# Import servers from Claude Desktop
claude mcp add-from-claude-desktop
```

### Add from JSON Configuration

```bash
claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"]}'
```

### Use Claude Code as an MCP Server

```bash
# Start Claude as a stdio MCP server
claude mcp serve
```

## Project Configuration (.mcp.json)

Create a `.mcp.json` file in your project root for team-shared servers:

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {
        "API_KEY": "${API_KEY:-default_value}"
      }
    }
  }
}
```

Supports environment variable expansion:
- `${VAR}` - Uses environment variable VAR
- `${VAR:-default}` - Uses VAR if set, otherwise uses default

## Windows-Specific Notes

On native Windows (not WSL), use `cmd /c` wrapper for npx commands:

```bash
claude mcp add my-server -- cmd /c npx -y @some/package
```

## Troubleshooting

- **Connection closed**: Check server URL/command is correct
- **Authentication failed**: Use `/mcp` to re-authenticate
- **Server not responding**: Increase timeout with `MCP_TIMEOUT=10000 claude`
- **Permission denied**: Check file permissions for stdio servers

## Security Notes

⚠️ **Important**: 
- Only install MCP servers from trusted sources
- Be careful with servers that fetch untrusted content (prompt injection risk)
- Never commit API keys or secrets to version control
- Use environment variables for sensitive configuration

## Learn More

- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [Find more MCP servers on GitHub](https://github.com/modelcontextprotocol/servers)
- [Build your own MCP server](https://modelcontextprotocol.io/quickstart/server)