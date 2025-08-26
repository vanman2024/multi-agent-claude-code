# MCP Server Architecture - Local vs Hosted

## Understanding MCP Server Types

### What's Actually Happening

When you use MCP servers, there are different architectures at play:

## 1. LOCAL MCP Servers (stdio transport)
These run on YOUR machine as local processes:

```bash
# These spawn a local Node.js process on your machine
claude mcp add playwright -- npx @modelcontextprotocol/server-playwright
claude mcp add postman -- npx @modelcontextprotocol/server-postman  
claude mcp add supabase -- npx @modelcontextprotocol/server-supabase
```

**How it works:**
- Claude Code spawns a Node.js process locally
- Communicates via stdio (standard input/output)
- Requires dependencies installed locally (npm packages)
- Stops when Claude Code stops

## 2. REMOTE API Endpoints (HTTP transport)
These connect to existing cloud services:

```bash
# Connects to GitHub's servers
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $TOKEN"
```

**How it works:**
- Claude Code makes HTTPS requests to remote servers
- No local process needed
- Authentication via headers
- Always available (doesn't depend on local setup)

## 3. CUSTOM Hosted MCP Servers (HTTP transport)
Your own MCP servers deployed to the cloud:

```bash
# Example: Your Supabase MCP deployed to DigitalOcean
claude mcp add --transport http supabase https://mcp-supabase.digitalocean.app -H "Authorization: Bearer $KEY"
```

**How it works:**
- You deploy an MCP server to cloud (DigitalOcean, Vercel, etc.)
- Provides HTTP endpoints following MCP protocol
- Can be shared across multiple users
- Requires authentication strategy

## Current Template Setup

For the Multi-Agent template, we use:

| Server | Type | Why |
|--------|------|-----|
| **GitHub** | Remote API (GitHub's servers) | Official GitHub Copilot endpoint |
| **Playwright** | Local (stdio) | Needs access to local browsers |
| **Postman** | Local (stdio) | Uses local Newman CLI |
| **Supabase** | Local (stdio) | Official Supabase package works well |

## Why Not Everything Hosted?

1. **Playwright** - Must be local because it controls browsers on YOUR machine
2. **Postman** - Could be hosted, but local is simpler for API testing
3. **Supabase** - The official local package is sufficient

## When to Use Hosted MCP Servers

Consider hosting when:
- Multiple users need the same server
- Server needs persistent state
- Server accesses cloud-only resources
- You want to hide API keys from users

## The Confusion Cleared

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Code                         │
└─────────────┬───────────────────────┬───────────────────┘
              │                       │
              │                       │
    ┌─────────▼──────────┐  ┌────────▼──────────┐
    │   Local Process     │  │   HTTP Request    │
    │   (stdio)           │  │   (HTTPS)         │
    └─────────┬──────────┘  └────────┬──────────┘
              │                       │
              │                       │
    ┌─────────▼──────────┐  ┌────────▼──────────┐
    │ • Playwright       │  │ • GitHub API      │
    │ • Postman          │  │ • Custom servers  │
    │ • Supabase         │  │   on cloud        │
    │ • Filesystem       │  │                   │
    └────────────────────┘  └───────────────────┘
      Runs on your PC          Runs in cloud
```

## Practical Impact

### For Template Users

1. **Clone template**
2. **Add MCP servers** - Mix of local and remote:
   - GitHub → Remote (GitHub's servers)
   - Others → Local (run on their machine)
3. **Everything works** - No need to deploy anything

### For Advanced Users

Could deploy custom MCP servers for:
- Shared team resources
- Complex integrations
- Proprietary tools

## Key Takeaway

**You DON'T need to host MCP servers for this template to work.**

The template uses:
- **GitHub's hosted endpoint** (already in cloud)
- **Local npm packages** for everything else (run on user's machine)

This keeps it simple and free for users!