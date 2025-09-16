# FastMCP CLI Guide: Complete Command Reference

## Overview

FastMCP provides a powerful command-line interface (CLI) that makes it easy to run, develop, install, and manage your MCP servers. This guide covers all FastMCP CLI commands with practical examples and best practices.

## Installation

The FastMCP CLI is automatically installed when you install FastMCP:

```bash
pip install fastmcp
# or
uv add fastmcp
```

## Core Commands

### `fastmcp run` - Run MCP Servers

The `fastmcp run` command is your primary tool for running MCP servers. It supports multiple entrypoints and transport protocols.

#### Basic Usage

```bash
# Run a server directly
fastmcp run server.py

# Run with specific transport
fastmcp run server.py --transport http --port 8000

# Run with custom Python version
fastmcp run server.py --python 3.11
```

#### Entrypoint Types

**1. Inferred Server Instance**
```python
# server.py
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def hello() -> str:
    return "Hello World!"
```

```bash
fastmcp run server.py  # Looks for 'mcp', 'server', or 'app' variables
```

**2. Explicit Server Entrypoint**
```python
# server.py
from fastmcp import FastMCP

my_custom_server = FastMCP("CustomServer")

@my_custom_server.tool
def custom_tool() -> str:
    return "Custom response"
```

```bash
fastmcp run server.py:my_custom_server
```

**3. Factory Function (Recommended)**
```python
# server.py
from fastmcp import FastMCP

async def create_server() -> FastMCP:
    mcp = FastMCP("MyServer")

    # Setup code that runs with fastmcp run
    @mcp.tool
    async def dynamic_tool() -> str:
        return "Dynamic tool response"

    # Pre-run setup
    tool = await mcp.get_tool("dynamic_tool")
    # Custom setup logic here

    return mcp
```

```bash
fastmcp run server.py:create_server
```

**4. Remote Server Proxy**
```bash
# Proxy a remote server locally
fastmcp run https://example.com/mcp-server
```

**5. Configuration Files**

*FastMCP Configuration (fastmcp.json):*
```bash
# Auto-detect fastmcp.json in current directory
fastmcp run

# Explicit configuration file
fastmcp run my-config.fastmcp.json

# Override config with CLI options
fastmcp run fastmcp.json --port 8080
```

*MCP Configuration (mcp.json):*
```bash
fastmcp run mcp.json
```

#### Transport Options

```bash
# STDIO (default for local development)
fastmcp run server.py --transport stdio

# HTTP with custom host/port
fastmcp run server.py --transport http --host 0.0.0.0 --port 8000

# SSE (Server-Sent Events)
fastmcp run server.py --transport sse --port 8001
```

#### Dependency Management

```bash
# Use local environment (you manage dependencies)
fastmcp run server.py

# Install additional packages
fastmcp run server.py --with pandas --with requests

# Use requirements file
fastmcp run server.py --with-requirements requirements.txt

# Run in specific project directory
fastmcp run server.py --project /path/to/project

# Skip environment setup (when already in uv environment)
fastmcp run server.py --skip-env
```

### `fastmcp dev` - Development with MCP Inspector

The `dev` command runs your server with the MCP Inspector for testing and debugging.

#### Basic Development Workflow

```bash
# Start development server with inspector
fastmcp dev server.py

# With fastmcp.json configuration
fastmcp dev  # Auto-detects fastmcp.json

# With custom configuration
fastmcp dev dev-config.fastmcp.json
```

#### Development Options

```bash
# Install in editable mode
fastmcp dev server.py --with-editable .

# Add development dependencies
fastmcp dev server.py --with pytest --with black

# Specify Python version
fastmcp dev server.py --python 3.11

# Use requirements file
fastmcp dev server.py --with-requirements requirements-dev.txt

# Run in project directory
fastmcp dev server.py --project /path/to/project
```

#### MCP Inspector Tips

1. **STDIO Transport**: Select "STDIO" from the transport dropdown after the inspector launches
2. **HTTP/SSE Testing**: Start server manually with HTTP transport, then connect inspector separately
3. **Environment Isolation**: The dev command always uses uv subprocess (never local environment)

### `fastmcp install` - Install Servers in MCP Clients

Install your MCP server in various MCP-compatible client applications.

#### Supported Clients

```bash
# Claude Code
fastmcp install claude-code server.py

# Claude Desktop
fastmcp install claude-desktop server.py

# Cursor
fastmcp install cursor server.py

# Generate MCP JSON configuration
fastmcp install mcp-json server.py
```

#### Installation with Dependencies

```bash
# Basic installation with dependencies
fastmcp install claude-desktop server.py --with pandas --with requests

# Editable installation (for development)
fastmcp install claude-code server.py --with-editable .

# With environment variables
fastmcp install cursor server.py --env API_KEY=secret --env DEBUG=true

# Load from .env file
fastmcp install claude-desktop server.py --env-file .env

# Custom server name
fastmcp install claude-code server.py --server-name "My Analysis Server"
```

#### MCP JSON Generation

```bash
# Generate and display JSON configuration
fastmcp install mcp-json server.py --with pandas

# Copy to clipboard
fastmcp install mcp-json server.py --copy

# Save to file
fastmcp install mcp-json server.py > server-config.json
```

### `fastmcp inspect` - Server Inspection & Analysis

Inspect your MCP server to view metadata, tools, prompts, and resources.

#### Inspection Commands

```bash
# Show text summary
fastmcp inspect server.py

# Output FastMCP JSON format
fastmcp inspect server.py --format fastmcp

# Output MCP protocol format
fastmcp inspect server.py --format mcp

# Save to file (requires format)
fastmcp inspect server.py --format fastmcp -o server-manifest.json
```

#### Output Formats

**FastMCP Format** (`--format fastmcp`):
- Includes FastMCP-specific metadata
- Tool tags and enabled status
- Output schemas and annotations
- Snake_case field names
- Best for: Complete server introspection

**MCP Protocol Format** (`--format mcp`):
- Standard MCP protocol fields only
- Matches client.list_tools() output
- CamelCase field names
- Best for: Client compatibility debugging

### `fastmcp project prepare` - Environment Preparation

Create persistent uv project directories for faster server startup.

```bash
# Prepare environment from fastmcp.json
fastmcp project prepare fastmcp.json --output-dir ./env

# Use prepared environment
fastmcp run fastmcp.json --project ./env
```

### `fastmcp version` - Version Information

```bash
# Display version info
fastmcp version

# Copy to clipboard
fastmcp version --copy
```

## Advanced Usage Patterns

### Development Workflow

```bash
# 1. Create server with factory function
# 2. Test with dev command
fastmcp dev server.py:create_server

# 3. Inspect server capabilities
fastmcp inspect server.py:create_server --format fastmcp

# 4. Install in your preferred client
fastmcp install claude-code server.py:create_server --with pandas

# 5. Run in production
fastmcp run server.py:create_server --transport http --port 8000
```

### Configuration Management

```json
// fastmcp.json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "API_KEY": "${API_KEY}",
        "DEBUG": "false"
      }
    }
  },
  "dependencies": ["pandas", "requests"],
  "python": "3.11"
}
```

```bash
# Use configuration
fastmcp run fastmcp.json
fastmcp dev fastmcp.json
fastmcp install claude-desktop fastmcp.json
```

### Environment Management

```bash
# Prepare reusable environment
fastmcp project prepare fastmcp.json --output-dir ./prod-env

# Use prepared environment for faster startup
fastmcp run fastmcp.json --project ./prod-env --port 8000

# Development with hot reload
fastmcp dev server.py --with-editable . --with pytest
```

### Remote Server Integration

```bash
# Proxy remote server locally
fastmcp run https://api.example.com/mcp

# Test remote server with inspector
# 1. Start proxy: fastmcp run https://api.example.com/mcp --port 3000
# 2. Open inspector and connect to localhost:3000
```

## Best Practices

### 1. Use Factory Functions
```python
# ✅ Recommended: Factory function allows setup code
async def create_server() -> FastMCP:
    mcp = FastMCP("MyServer")
    # Setup code here
    return mcp

# ❌ Avoid: __main__ block is ignored by fastmcp run
if __name__ == "__main__":
    # This won't run with fastmcp run
    pass
```

### 2. Environment Isolation
```bash
# Development: Use dev command for isolation
fastmcp dev server.py --with pytest --with black

# Production: Use prepared environments
fastmcp project prepare fastmcp.json --output-dir ./env
fastmcp run fastmcp.json --project ./env
```

### 3. Configuration Files
```bash
# Use fastmcp.json for complex setups
fastmcp run fastmcp.json  # Auto-detects configuration
fastmcp dev fastmcp.json  # Uses configured dependencies
fastmcp install claude-desktop fastmcp.json  # Handles all setup
```

### 4. Transport Selection
```bash
# Development: STDIO with dev command
fastmcp dev server.py

# Local testing: HTTP transport
fastmcp run server.py --transport http --port 8000

# Production: HTTP or SSE
fastmcp run server.py --transport http --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Common Issues

**"No server instance found"**
```bash
# Check variable names (must be 'mcp', 'server', or 'app')
fastmcp run server.py  # Looks for these specific names

# Use explicit entrypoint
fastmcp run server.py:my_server
```

**"Dependencies not found"**
```bash
# Install dependencies explicitly
fastmcp run server.py --with pandas --with requests

# Use requirements file
fastmcp run server.py --with-requirements requirements.txt

# Use fastmcp.json for complex dependency management
fastmcp run fastmcp.json
```

**"Port already in use"**
```bash
# Specify different port
fastmcp run server.py --port 8001

# Find available port
lsof -i :8000  # Check what's using port 8000
```

**"Inspector not connecting"**
```bash
# For STDIO: Select "STDIO" in inspector dropdown
# For HTTP: Start server separately, connect inspector to server URL
fastmcp run server.py --transport http --port 8000
# Then connect inspector to http://localhost:8000
```

## Integration Examples

### With Claude Code
```bash
# Install server
fastmcp install claude-code server.py --with pandas

# Server appears in Claude Code's MCP server list
# Use @mention to interact with your server
```

### With Claude Desktop
```bash
# Install server
fastmcp install claude-desktop server.py --with requests

# Server is added to Claude Desktop's configuration
# Available in all Claude Desktop conversations
```

### With Cursor
```bash
# Install server
fastmcp install cursor server.py --with numpy

# Cursor opens confirmation dialog
# Server becomes available in Cursor's MCP integration
```

### CI/CD Integration
```bash
# Prepare environment once
fastmcp project prepare fastmcp.json --output-dir ./env

# Run tests in CI
fastmcp run fastmcp.json --project ./env --port 8000

# Health check
curl http://localhost:8000/health
```

This comprehensive guide covers all FastMCP CLI commands and usage patterns. For more advanced features, refer to the official FastMCP documentation.