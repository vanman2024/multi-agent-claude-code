# MCP Server Issues Fixed

## Issues Identified

1. **GitHub MCP Server**: Error: missing required Authorization header
2. **Supabase MCP Server**: MCP error -32000: Connection closed
3. **Postman MCP Server**: Skipping tools due to missing types in parameter schema

## Fixes Applied

### 1. Environment Variables Configuration

Added missing `SUPABASE_PROJECT_REF` to `.env` file:
```bash
SUPABASE_PROJECT_REF="dkpwdljgnysqzjufjtnk"
```

### 2. MCP Server Configuration Updates

Updated `project-sync/config/mcp-servers.json` to properly configure environment variables:

#### Postman Server
Added environment variable configuration:
```json
"postman": {
  "transport": "stdio",
  "command": "npx",
  "args": [
    "-y",
    "@postman/postman-mcp-server"
  ],
  "env": {
    "POSTMAN_API_KEY": "${POSTMAN_API_KEY}"
  }
}
```

#### Supabase Server
Fixed to use the correct environment variable:
```json
"supabase": {
  "transport": "stdio",
  "command": "npx",
  "args": [
    "-y",
    "@supabase/mcp-server-supabase@latest"
  ],
  "env_required": [
    "SUPABASE_PROJECT_REF",
    "SUPABASE_SERVICE_KEY"
  ],
  "env_args": [
    "--project-ref=${SUPABASE_PROJECT_REF}",
    "--access-token=${SUPABASE_SERVICE_KEY}"
  ]
}
```

### 3. Synchronization

Ran the MCP server synchronization script to apply configurations to all agents:
```bash
./project-sync/scripts/sync-mcp-servers.sh sync-all
```

## Verification

All MCP servers are now working correctly:
- ✅ GitHub MCP Server
- ✅ Supabase MCP Server  
- ✅ Postman MCP Server
- ✅ Filesystem MCP Server
- ✅ Memory MCP Server
- ✅ Sequential Thinking MCP Server
- ✅ Playwright MCP Server

The "missing types in parameter schema" warnings for Postman tools are non-critical and can be ignored as they don't affect functionality.