"""
FastMCP Server Tests

Following FastMCP testing patterns for MCP server implementation.
Tests run in-memory for speed and determinism.
"""

import pytest
from typing import Dict, Any
from fastmcp import FastMCP
from fastmcp.client import Client
from inline_snapshot import snapshot


@pytest.mark.mcp
class TestFastMCPServer:
    """Test FastMCP server implementation."""
    
    @pytest.fixture
    def basic_server(self):
        """Create a basic FastMCP server with tools."""
        server = FastMCP("TestServer")
        
        @server.tool
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b
        
        @server.tool
        def divide(a: float, b: float) -> float:
            """Divide two numbers."""
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b
        
        return server
    
    @pytest.mark.asyncio
    async def test_tool_registration(self, basic_server):
        """Test that tools are properly registered with the server."""
        tools = basic_server.list_tools()
        assert len(tools) == 2
        assert tools[0].name == "add"
        assert tools[1].name == "divide"
    
    @pytest.mark.asyncio
    async def test_tool_execution(self, basic_server):
        """Test tool execution through in-memory transport."""
        async with Client(basic_server) as client:
            result = await client.call_tool("add", {"a": 5, "b": 3})
            assert result.content[0].text == "8"
    
    @pytest.mark.asyncio
    async def test_tool_error_handling(self, basic_server):
        """Test that tool errors are properly handled."""
        async with Client(basic_server) as client:
            with pytest.raises(Exception) as exc_info:
                await client.call_tool("divide", {"a": 10, "b": 0})
            assert "Cannot divide by zero" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_tool_schema_generation(self):
        """Test that tool schemas are generated correctly using inline snapshots."""
        mcp = FastMCP("test-server")
        
        @mcp.tool
        def calculate_tax(amount: float, rate: float = 0.1) -> dict:
            """Calculate tax on an amount."""
            return {
                "amount": amount,
                "tax": amount * rate,
                "total": amount * (1 + rate)
            }
        
        tools = mcp.list_tools()
        schema = tools[0].inputSchema
        
        # Use inline snapshot for schema validation
        assert schema == snapshot({
            "type": "object",
            "properties": {
                "amount": {"type": "number"},
                "rate": {"type": "number", "default": 0.1}
            },
            "required": ["amount"]
        })


@pytest.mark.mcp
class TestFastMCPResources:
    """Test FastMCP resource handling."""
    
    @pytest.fixture
    def resource_server(self):
        """Create server with resources."""
        server = FastMCP("ResourceServer")
        
        @server.resource("config://settings")
        def get_settings() -> dict:
            """Get application settings."""
            return {
                "theme": "dark",
                "language": "en",
                "notifications": True
            }
        
        @server.resource("data://users/{user_id}")
        def get_user(user_id: str) -> dict:
            """Get user data."""
            users = {
                "123": {"id": "123", "name": "Alice"},
                "456": {"id": "456", "name": "Bob"}
            }
            return users.get(user_id, {})
        
        return server
    
    @pytest.mark.asyncio
    async def test_resource_listing(self, resource_server):
        """Test resource listing."""
        async with Client(resource_server) as client:
            resources = await client.list_resources()
            assert len(resources) == 2
            assert any(r.uri == "config://settings" for r in resources)
    
    @pytest.mark.asyncio
    async def test_resource_reading(self, resource_server):
        """Test reading resource content."""
        async with Client(resource_server) as client:
            result = await client.read_resource("config://settings")
            assert result.content[0].type == "text"
            data = result.content[0].data
            assert data["theme"] == "dark"
            assert data["notifications"] is True
    
    @pytest.mark.asyncio
    async def test_parametric_resource(self, resource_server):
        """Test resource with parameters."""
        async with Client(resource_server) as client:
            result = await client.read_resource("data://users/123")
            assert result.content[0].data["name"] == "Alice"


@pytest.mark.mcp
class TestFastMCPAuthentication:
    """Test FastMCP authentication patterns."""
    
    @pytest.fixture
    def auth_server(self):
        """Create server with authentication."""
        from fastmcp.auth import BearerTokenProvider, BearerAuth
        
        server = FastMCP("AuthServer")
        server.auth = BearerTokenProvider({
            "secret-token-123": "alice",
            "secret-token-456": "bob"
        })
        
        @server.tool
        def protected_action(action: str) -> str:
            """Perform protected action."""
            context = server.get_context()
            user = context.auth.user if context.auth else "anonymous"
            return f"{user} performed {action}"
        
        return server
    
    @pytest.mark.asyncio
    async def test_authenticated_request(self, auth_server):
        """Test authenticated tool access."""
        from fastmcp.auth import BearerAuth
        
        async with Client(auth_server, auth=BearerAuth("secret-token-123")) as client:
            result = await client.call_tool("protected_action", {"action": "read"})
            assert result.content[0].text == "alice performed read"
    
    @pytest.mark.asyncio
    async def test_unauthenticated_rejection(self, auth_server):
        """Test that unauthenticated requests are rejected."""
        async with Client(auth_server) as client:
            with pytest.raises(Exception) as exc_info:
                await client.call_tool("protected_action", {"action": "write"})
            assert "authentication" in str(exc_info.value).lower()


@pytest.mark.mcp
class TestFastMCPPrompts:
    """Test FastMCP prompt handling."""
    
    @pytest.fixture
    def prompt_server(self):
        """Create server with prompts."""
        server = FastMCP("PromptServer")
        
        @server.prompt
        def code_review(language: str = "python") -> str:
            """Generate code review prompt."""
            return f"""You are reviewing {language} code.
            Focus on:
            - Code quality and best practices
            - Performance considerations
            - Security vulnerabilities
            - Test coverage"""
        
        @server.prompt
        def test_generator(component: str) -> str:
            """Generate test cases for a component."""
            return f"Generate comprehensive tests for {component}"
        
        return server
    
    @pytest.mark.asyncio
    async def test_prompt_listing(self, prompt_server):
        """Test listing available prompts."""
        async with Client(prompt_server) as client:
            prompts = await client.list_prompts()
            assert len(prompts) == 2
            assert any(p.name == "code_review" for p in prompts)
    
    @pytest.mark.asyncio
    async def test_prompt_execution(self, prompt_server):
        """Test prompt execution with parameters."""
        async with Client(prompt_server) as client:
            result = await client.get_prompt("code_review", {"language": "typescript"})
            assert "typescript" in result.messages[0].content.text
            assert "security" in result.messages[0].content.text.lower()


@pytest.mark.mcp
@pytest.mark.integration
class TestFastMCPNetworkTransport:
    """Test network transports (marked as integration)."""
    
    @pytest.mark.asyncio
    @pytest.mark.client_process
    async def test_http_transport(self):
        """Test HTTP/SSE transport with real server."""
        from fastmcp.utilities.tests import run_server_in_process
        from fastmcp.client.transports import StreamableHttpTransport
        
        def run_server(host: str, port: int) -> None:
            """Server function to run in subprocess."""
            server = FastMCP("HTTPTestServer")
            
            @server.tool
            def echo(message: str) -> str:
                return message
            
            server.run(host=host, port=port)
        
        with run_server_in_process(run_server, transport="http") as url:
            async with Client(
                transport=StreamableHttpTransport(f"{url}/mcp")
            ) as client:
                result = await client.ping()
                assert result is True
                
                echo_result = await client.call_tool("echo", {"message": "test"})
                assert echo_result.content[0].text == "test"
    
    @pytest.mark.asyncio
    @pytest.mark.client_process
    async def test_stdio_transport(self):
        """Test STDIO transport with subprocess."""
        async with Client("python examples/echo_server.py") as client:
            result = await client.call_tool("echo", {"message": "hello"})
            assert result.content[0].text == "hello"