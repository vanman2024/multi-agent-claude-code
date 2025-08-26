# Hosting Custom MCP Servers

## Why Host Custom MCP Servers?

Just like GitHub hosts their MCP at `api.githubcopilot.com/mcp`, you can host custom MCP servers for:

1. **Team Sharing** - One server, multiple users
2. **Proprietary Tools** - Your own internal APIs
3. **Persistent State** - Servers that remember things
4. **No Local Setup** - Users don't install anything

## Example: Hosting on DigitalOcean

### 1. Deploy Your MCP Server

Let's say you built a custom Supabase MCP server:

```python
# Your custom MCP server (Python/FastAPI example)
# Located at: /servers/supabase-mcp/app.py
```

Deploy to DigitalOcean App Platform:

```bash
# Create app.yaml for DigitalOcean
name: supabase-mcp
region: nyc
services:
- environment_slug: python
  github:
    branch: main
    deploy_on_push: true
    repo: yourusername/mcp-servers
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
  name: supabase-mcp
  routes:
  - path: /
  source_dir: /servers/supabase-mcp
```

### 2. Your Server Gets a URL

Once deployed:
```
https://supabase-mcp-xxxxx.ondigitalocean.app
```

### 3. Users Add It Like GitHub's

```bash
# Just like GitHub's:
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $TOKEN"

# Your custom server:
claude mcp add --transport http supabase https://supabase-mcp-xxxxx.ondigitalocean.app -H "Authorization: Bearer $API_KEY"
```

## Authentication Strategies

### Option 1: Shared Template Key (Easiest, Less Secure)
```bash
# You provide one key for all template users
TEMPLATE_MCP_KEY="template_key_abc123"
claude mcp add --transport http custom https://your-mcp.ondigitalocean.app -H "Authorization: Bearer $TEMPLATE_MCP_KEY"
```

### Option 2: User's Own Keys (Most Secure)
```bash
# Users provide their own Supabase credentials
claude mcp add --transport http custom https://your-mcp.ondigitalocean.app \
  -H "Authorization: Bearer $USER_SUPABASE_KEY" \
  -H "X-Supabase-URL: $USER_SUPABASE_URL"
```

### Option 3: Free Tier with Limits
```bash
# No auth for basic operations, auth for advanced
claude mcp add --transport http custom https://your-mcp.ondigitalocean.app
```

## Cost Considerations

### DigitalOcean App Platform
- **Basic**: $5/month (1 vCPU, 512MB RAM)
- **Enough for**: ~100 concurrent users
- **Auto-scaling**: Available if needed

### Alternatives
- **Vercel Functions**: Free tier, serverless
- **Railway**: $5/month, easy deploys
- **Fly.io**: Free tier available
- **AWS Lambda**: Pay per request

## Example: Custom MCP Servers Worth Hosting

### 1. Team Database Manager
```python
# Shared Supabase access for your team
@app.post("/mcp/tools/query")
async def execute_query(request: Request):
    # Use team's shared Supabase credentials
    # Apply row-level security
    # Log all queries for audit
```

### 2. Company API Gateway
```python
# Access multiple internal services
@app.post("/mcp/tools/internal_api")
async def internal_api(request: Request):
    # Route to internal services
    # Handle authentication
    # Apply rate limiting
```

### 3. Specialized Tools
```python
# Custom business logic
@app.post("/mcp/tools/calculate_pricing")
async def calculate_pricing(request: Request):
    # Your proprietary pricing algorithm
    # Access private data
    # Return results
```

## Current Template Approach

For the Multi-Agent template, we're NOT hosting custom servers because:

1. **GitHub MCP** - Already hosted by GitHub
2. **Playwright** - MUST be local (browser control)
3. **Postman** - Local is simpler
4. **Supabase** - Official package works fine locally

## When You Should Host

Host custom MCP servers when:

✅ **Multiple users need the same server**
```bash
# Team of 10 developers all using:
claude mcp add --transport http team-tools https://mcp.yourcompany.com
```

✅ **Server needs cloud resources**
```bash
# Accessing private VPC databases
# Using cloud-only APIs
# Requiring high compute
```

✅ **You want to hide complexity**
```bash
# Users just add one URL
# No local setup needed
# No dependency management
```

## Quick Hosting Guide

### 1. Build MCP Server
```python
# Follow MCP protocol
from fastapi import FastAPI
app = FastAPI()

@app.post("/mcp/tools")
async def list_tools():
    return {"tools": [...]}

@app.post("/mcp/tools/{tool_name}")
async def execute_tool(tool_name: str):
    # Tool logic
```

### 2. Deploy to DigitalOcean
```bash
doctl apps create --spec app.yaml
```

### 3. Share with Users
```markdown
## Add Our Custom MCP Server

\```bash
claude mcp add --transport http custom https://mcp-custom.ondigitalocean.app
\```
```

## The Bottom Line

- **Local MCP servers** = Free, run on user's machine
- **Hosted MCP servers** = $5+/month, accessible anywhere
- **GitHub's approach** = Host it, make it available to all
- **Your approach** = Depends on your needs

For most templates: **Local is fine**
For team tools: **Hosting makes sense**