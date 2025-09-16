"""
Inline Snapshot Testing Examples

Demonstrates inline snapshot testing with FastMCP patterns.
Inline snapshots capture the expected output directly in the test code.
"""

import pytest
from inline_snapshot import snapshot
from typing import Dict, Any
import json


@pytest.mark.mcp
class TestInlineSnapshots:
    """Demonstrate inline snapshot testing patterns."""
    
    def test_tool_schema_snapshot(self):
        """Test tool schema generation with inline snapshots."""
        # Generate a tool schema
        def create_tool_schema(name: str, params: Dict) -> Dict:
            return {
                "name": name,
                "description": f"Tool for {name}",
                "inputSchema": {
                    "type": "object",
                    "properties": params,
                    "required": list(params.keys())
                }
            }
        
        schema = create_tool_schema("search", {
            "query": {"type": "string", "description": "Search query"},
            "limit": {"type": "integer", "default": 10}
        })
        
        # Snapshot will be auto-filled on first run
        assert schema == snapshot({
            "name": "search",
            "description": "Tool for search",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query", "limit"]
            }
        })
    
    def test_mcp_response_snapshot(self):
        """Test MCP response format with inline snapshots."""
        def create_mcp_response(method: str, result: Any) -> Dict:
            return {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "result": result
            }
        
        response = create_mcp_response("tools/list", {
            "tools": [
                {"name": "add", "description": "Add numbers"},
                {"name": "subtract", "description": "Subtract numbers"}
            ]
        })
        
        assert response == snapshot({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "result": {
                "tools": [
                    {"name": "add", "description": "Add numbers"},
                    {"name": "subtract", "description": "Subtract numbers"}
                ]
            }
        })
    
    @pytest.mark.asyncio
    async def test_fastmcp_tool_registration_snapshot(self, fastmcp_test_server):
        """Test FastMCP tool registration with snapshots."""
        tools = fastmcp_test_server.list_tools()
        
        # Convert to serializable format
        tool_data = []
        for tool in tools:
            tool_data.append({
                "name": tool.name,
                "description": tool.description,
                "schema": tool.inputSchema
            })
        
        # Snapshot captures the exact structure
        assert tool_data == snapshot([
            {
                "name": "echo",
                "description": "Echo the message back.",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "add",
                "description": "Add two numbers.",
                "schema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            }
        ])
    
    def test_cli_output_snapshot(self):
        """Test CLI output formatting with snapshots."""
        def format_cli_output(tools: list) -> str:
            lines = ["Available Tools:"]
            for tool in tools:
                lines.append(f"  - {tool['name']}: {tool['description']}")
            return "\n".join(lines)
        
        output = format_cli_output([
            {"name": "search", "description": "Search for content"},
            {"name": "calculate", "description": "Perform calculations"}
        ])
        
        assert output == snapshot("""Available Tools:
  - search: Search for content
  - calculate: Perform calculations""")
    
    def test_error_response_snapshot(self):
        """Test error response format with snapshots."""
        def create_error_response(code: int, message: str) -> Dict:
            return {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": code,
                    "message": message,
                    "data": None
                }
            }
        
        error = create_error_response(-32601, "Method not found")
        
        assert error == snapshot({
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32601,
                "message": "Method not found",
                "data": None
            }
        })
    
    def test_complex_nested_snapshot(self):
        """Test complex nested data structures with snapshots."""
        def create_server_info() -> Dict:
            return {
                "name": "TestServer",
                "version": "1.0.0",
                "capabilities": {
                    "tools": {
                        "enabled": True,
                        "count": 5,
                        "categories": ["math", "text", "data"]
                    },
                    "resources": {
                        "enabled": True,
                        "protocols": ["file://", "http://", "config://"]
                    },
                    "auth": {
                        "required": False,
                        "methods": ["bearer", "api-key"]
                    }
                },
                "metadata": {
                    "author": "Test Author",
                    "license": "MIT",
                    "repository": "github.com/test/repo"
                }
            }
        
        info = create_server_info()
        
        # Snapshot captures entire nested structure
        assert info == snapshot({
            "name": "TestServer",
            "version": "1.0.0",
            "capabilities": {
                "tools": {
                    "enabled": True,
                    "count": 5,
                    "categories": ["math", "text", "data"]
                },
                "resources": {
                    "enabled": True,
                    "protocols": ["file://", "http://", "config://"]
                },
                "auth": {
                    "required": False,
                    "methods": ["bearer", "api-key"]
                }
            },
            "metadata": {
                "author": "Test Author",
                "license": "MIT",
                "repository": "github.com/test/repo"
            }
        })


@pytest.mark.mcp
@pytest.mark.cli
class TestCLIOutputSnapshots:
    """Test CLI output formatting with snapshots."""
    
    def test_table_output_snapshot(self):
        """Test table-formatted output with snapshots."""
        def create_table_output(data: list) -> str:
            lines = []
            lines.append("┌─────────┬──────────────┬────────┐")
            lines.append("│ Name    │ Description  │ Status │")
            lines.append("├─────────┼──────────────┼────────┤")
            for row in data:
                lines.append(f"│ {row['name']:<7} │ {row['desc']:<12} │ {row['status']:<6} │")
            lines.append("└─────────┴──────────────┴────────┘")
            return "\n".join(lines)
        
        output = create_table_output([
            {"name": "add", "desc": "Add numbers", "status": "active"},
            {"name": "sub", "desc": "Subtract", "status": "active"}
        ])
        
        # Snapshot captures exact formatting
        assert output == snapshot("""┌─────────┬──────────────┬────────┐
│ Name    │ Description  │ Status │
├─────────┼──────────────┼────────┤
│ add     │ Add numbers  │ active │
│ sub     │ Subtract     │ active │
└─────────┴──────────────┴────────┘""")
    
    def test_json_output_snapshot(self):
        """Test JSON-formatted output with snapshots."""
        data = {
            "server": "TestMCP",
            "status": "running",
            "tools": ["add", "multiply", "search"],
            "uptime": "2h 15m"
        }
        
        formatted = json.dumps(data, indent=2)
        
        assert formatted == snapshot("""{
  "server": "TestMCP",
  "status": "running",
  "tools": [
    "add",
    "multiply",
    "search"
  ],
  "uptime": "2h 15m"
}""")


# Usage Notes for Inline Snapshots:
# 
# 1. First Run: Leave snapshot() empty or with expected structure
# 2. Run tests with: pytest --inline-snapshot=create
# 3. Snapshots are auto-filled with actual values
# 4. Review the generated snapshots
# 5. Future runs: pytest (snapshots are now assertions)
# 6. Update snapshots: pytest --inline-snapshot=update
# 
# Benefits:
# - Expected values are visible in the test code
# - No separate snapshot files to manage
# - Easy to review in code reviews
# - Works with any serializable data structure