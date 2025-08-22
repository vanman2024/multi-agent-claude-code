# Claude Code Documentation

## Working with MCP Servers

MCP (Model Context Protocol) servers allow Claude to interact with external tools and services. Here's how to manage them:

### Managing MCP Servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

### Adding MCP Servers

To add a new MCP server, use:
```bash
claude mcp add <server-name> <server-url>
```

### Troubleshooting

If a server shows as "Failed to connect", you can:
1. Check the server status with `/mcp` within Claude Code
2. Remove and re-add the server if needed
3. Verify the server URL is correct and accessible