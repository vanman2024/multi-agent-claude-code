"""MCP transport tests - test real network/stdio transports with subprocess."""
import os
import sys
import pytest
import asyncio
import subprocess
import time
from typing import Optional

# Skip these tests unless explicitly enabled
pytestmark = [
    pytest.mark.mcp,
    pytest.mark.client_process,
    pytest.mark.skipif(
        not os.getenv("RUN_MCP_TRANSPORT"),
        reason="Set RUN_MCP_TRANSPORT=1 to run transport tests"
    )
]

# Try to import fastmcp, skip all tests if not available
fastmcp = pytest.importorskip("fastmcp", reason="fastmcp required for MCP transport tests")


class MCPServerProcess:
    """Context manager for running MCP server in subprocess."""
    
    def __init__(self, script_content: str, transport: str = "stdio"):
        self.script_content = script_content
        self.transport = transport
        self.process: Optional[subprocess.Popen] = None
        self.port = 8765  # Default port for HTTP transport
    
    def __enter__(self):
        """Start the server process."""
        # Write server script to temp file
        import tempfile
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        )
        self.temp_file.write(self.script_content)
        self.temp_file.flush()
        
        if self.transport == "stdio":
            # Start STDIO server
            self.process = subprocess.Popen(
                [sys.executable, self.temp_file.name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        elif self.transport == "http":
            # Start HTTP server
            self.process = subprocess.Popen(
                [sys.executable, self.temp_file.name, "--port", str(self.port)],
                stderr=subprocess.PIPE,
                text=True
            )
            # Wait for server to start
            time.sleep(2)
            return f"http://localhost:{self.port}"
        
        return self.process
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the server process."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        # Clean up temp file
        if hasattr(self, 'temp_file'):
            os.unlink(self.temp_file.name)


# Simple test server script
TEST_SERVER_SCRIPT = '''
import sys
import asyncio
from fastmcp import FastMCP

server = FastMCP("TestTransportServer")

@server.tool
def echo(message: str) -> str:
    """Echo the message back."""
    return f"Echo: {message}"

@server.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    
    if "--port" in sys.argv:
        # HTTP mode
        asyncio.run(server.run_http(port=args.port))
    else:
        # STDIO mode
        asyncio.run(server.run_stdio())
'''


@pytest.mark.asyncio
async def test_stdio_transport():
    """Test STDIO transport with subprocess."""
    with MCPServerProcess(TEST_SERVER_SCRIPT, transport="stdio") as process:
        # Import here to avoid issues if not installed
        from fastmcp import Client
        
        # Connect via STDIO transport
        async with Client(
            [sys.executable, process.args[0]],  # Command to run
            transport="stdio"
        ) as client:
            # Test basic connectivity
            assert await client.ping() is True
            
            # Test tool listing
            tools = await client.list_tools()
            assert len(tools) == 2
            assert any(t.name == "echo" for t in tools)
            assert any(t.name == "add" for t in tools)
            
            # Test tool execution
            result = await client.call_tool("echo", {"message": "Hello"})
            assert "Echo: Hello" in str(result)


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("RUN_HTTP_TRANSPORT"),
    reason="Set RUN_HTTP_TRANSPORT=1 for HTTP transport tests"
)
async def test_http_transport():
    """Test HTTP transport with subprocess."""
    with MCPServerProcess(TEST_SERVER_SCRIPT, transport="http") as url:
        from fastmcp import Client
        
        # Connect via HTTP transport
        async with Client(url, transport="http") as client:
            # Test basic connectivity
            assert await client.ping() is True
            
            # Test tool listing
            tools = await client.list_tools()
            assert len(tools) == 2
            
            # Test tool execution
            result = await client.call_tool("add", {"a": 5, "b": 3})
            assert result == 8 or "8" in str(result)


@pytest.mark.asyncio
async def test_transport_error_handling():
    """Test that transport errors are handled gracefully."""
    from fastmcp import Client
    
    # Try to connect to non-existent server
    with pytest.raises(Exception) as exc_info:
        async with Client("http://localhost:99999", transport="http") as client:
            await client.ping()
    
    # Should get connection error
    assert "connect" in str(exc_info.value).lower() or "refused" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_transport_timeout():
    """Test transport timeout handling."""
    # Create a server that delays response
    SLOW_SERVER = '''
import asyncio
from fastmcp import FastMCP

server = FastMCP("SlowServer")

@server.tool
async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "Done"

if __name__ == "__main__":
    asyncio.run(server.run_stdio())
'''
    
    with MCPServerProcess(SLOW_SERVER, transport="stdio") as process:
        from fastmcp import Client
        
        async with Client(
            [sys.executable, process.args[0]],
            transport="stdio",
            timeout=2  # 2 second timeout
        ) as client:
            # Should timeout
            with pytest.raises(asyncio.TimeoutError):
                await client.call_tool("slow_operation", {})


@pytest.mark.asyncio
async def test_large_payload_transport():
    """Test transport with large payloads."""
    LARGE_PAYLOAD_SERVER = '''
from fastmcp import FastMCP

server = FastMCP("LargePayloadServer")

@server.tool
def process_data(data: list) -> dict:
    """Process large data array."""
    return {
        "count": len(data),
        "first": data[0] if data else None,
        "last": data[-1] if data else None
    }

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run_stdio())
'''
    
    with MCPServerProcess(LARGE_PAYLOAD_SERVER, transport="stdio") as process:
        from fastmcp import Client
        
        async with Client(
            [sys.executable, process.args[0]],
            transport="stdio"
        ) as client:
            # Send large payload
            large_data = list(range(10000))
            result = await client.call_tool(
                "process_data",
                {"data": large_data}
            )
            
            # Verify result
            result_dict = result if isinstance(result, dict) else result.model_dump()
            assert result_dict["count"] == 10000
            assert result_dict["first"] == 0
            assert result_dict["last"] == 9999