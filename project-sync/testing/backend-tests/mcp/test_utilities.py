"""
FastMCP Test Utilities

Common utilities for testing MCP servers and clients following FastMCP patterns.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager
import subprocess
import time
import os
from pathlib import Path


class MCPTestClient:
    """Test client for MCP server interactions."""
    
    def __init__(self, server_url: str = "stdio://./mcp-server"):
        self.server_url = server_url
        self.request_id = 0
        
    def _next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id
        
    async def send_request(self, method: str, params: Optional[Dict] = None) -> Dict:
        """Send JSON-RPC request to server."""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._next_id()
        }
        if params:
            request["params"] = params
            
        # In real implementation, would send via transport
        # This is a mock response for testing
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {}
        }
        
    async def list_tools(self) -> List[Dict]:
        """List available tools."""
        response = await self.send_request("tools/list")
        return response.get("result", {}).get("tools", [])
        
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        """Call a tool with arguments."""
        return await self.send_request(
            "tools/call",
            {"name": name, "arguments": arguments}
        )
        
    async def list_resources(self) -> List[Dict]:
        """List available resources."""
        response = await self.send_request("resources/list")
        return response.get("result", {}).get("resources", [])
        
    async def read_resource(self, uri: str) -> Dict:
        """Read a resource by URI."""
        return await self.send_request(
            "resources/read",
            {"uri": uri}
        )


class InMemoryTransport:
    """In-memory transport for testing without network/stdio."""
    
    def __init__(self, server):
        self.server = server
        self.messages = []
        
    async def send(self, message: Dict) -> Optional[Dict]:
        """Send message to server and get response."""
        self.messages.append(message)
        
        # Simulate server processing
        if hasattr(self.server, 'handle_request'):
            return await self.server.handle_request(message)
        return None
        
    def get_messages(self) -> List[Dict]:
        """Get all sent messages for verification."""
        return self.messages.copy()


@asynccontextmanager
async def run_mcp_server(server_cmd: str, timeout: int = 5):
    """Run MCP server in subprocess for integration testing."""
    process = None
    try:
        process = subprocess.Popen(
            server_cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give server time to start
        await asyncio.sleep(0.5)
        
        # Check if server started successfully
        if process.poll() is not None:
            stderr = process.stderr.read()
            raise RuntimeError(f"Server failed to start: {stderr}")
            
        yield process
        
    finally:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()


def validate_jsonrpc_response(response: Dict) -> bool:
    """Validate JSON-RPC 2.0 response format."""
    if not isinstance(response, dict):
        return False
        
    # Must have jsonrpc version
    if response.get("jsonrpc") != "2.0":
        return False
        
    # Must have either result or error (not both)
    has_result = "result" in response
    has_error = "error" in response
    
    if has_result == has_error:  # Both or neither
        return False
        
    # If error, must have code and message
    if has_error:
        error = response["error"]
        if not isinstance(error, dict):
            return False
        if "code" not in error or "message" not in error:
            return False
            
    # Must have id (unless it's a notification response)
    if "id" not in response and not is_notification_response(response):
        return False
        
    return True


def is_notification_response(response: Any) -> bool:
    """Check if response is for a notification (no response expected)."""
    return response is None


def create_test_tool_schema(
    name: str,
    description: str,
    parameters: Dict[str, Any]
) -> Dict:
    """Create a tool schema for testing."""
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": parameters,
            "required": list(parameters.keys())
        }
    }


def create_test_resource(
    uri: str,
    name: str,
    description: str,
    mimeType: str = "text/plain"
) -> Dict:
    """Create a resource descriptor for testing."""
    return {
        "uri": uri,
        "name": name,
        "description": description,
        "mimeType": mimeType
    }


class MockFastMCPServer:
    """Mock FastMCP server for testing."""
    
    def __init__(self, name: str = "TestServer"):
        self.name = name
        self.tools = {}
        self.resources = {}
        self.prompts = {}
        
    def tool(self, func):
        """Decorator to register a tool."""
        self.tools[func.__name__] = func
        return func
        
    def resource(self, uri: str):
        """Decorator to register a resource."""
        def decorator(func):
            self.resources[uri] = func
            return func
        return decorator
        
    def prompt(self, func):
        """Decorator to register a prompt."""
        self.prompts[func.__name__] = func
        return func
        
    def list_tools(self):
        """List registered tools."""
        from types import SimpleNamespace
        tools = []
        for name, func in self.tools.items():
            tool = SimpleNamespace()
            tool.name = name
            tool.description = func.__doc__ or ""
            tool.inputSchema = self._generate_schema(func)
            tools.append(tool)
        return tools
        
    def _generate_schema(self, func):
        """Generate input schema from function signature."""
        import inspect
        sig = inspect.signature(func)
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_type = "string"  # Default type
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == dict:
                    param_type = "object"
                    
            properties[param_name] = {"type": param_type}
            
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
            else:
                properties[param_name]["default"] = param.default
                
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }


async def wait_for_server(url: str, timeout: int = 10) -> bool:
    """Wait for server to become available."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            # Try to connect to server
            # Implementation depends on transport type
            return True
        except:
            await asyncio.sleep(0.5)
    return False


def compare_schemas(expected: Dict, actual: Dict) -> bool:
    """Compare two JSON schemas for testing."""
    # Simple comparison - can be made more sophisticated
    return json.dumps(expected, sort_keys=True) == json.dumps(actual, sort_keys=True)


# Test data generators
def generate_test_request(method: str, params: Dict = None) -> Dict:
    """Generate a test JSON-RPC request."""
    import random
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "id": random.randint(1, 10000)
    }
    if params:
        request["params"] = params
    return request


def generate_test_response(request_id: int, result: Any = None, error: Dict = None) -> Dict:
    """Generate a test JSON-RPC response."""
    response = {
        "jsonrpc": "2.0",
        "id": request_id
    }
    if error:
        response["error"] = error
    else:
        response["result"] = result if result is not None else {}
    return response