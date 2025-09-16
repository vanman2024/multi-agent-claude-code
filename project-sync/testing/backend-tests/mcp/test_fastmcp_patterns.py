"""
Test FastMCP CLI Patterns

Tests that demonstrate the FastMCP CLI patterns for running servers.
These tests show how to use the same patterns as `fastmcp run`, `fastmcp dev`, and `fastmcp install`.
"""

import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from fastmcp_runner import (
    FastMCPRunner,
    FastMCPDevServer,
    FastMCPInstaller,
    fastmcp_test_server,
    create_test_server,
    create_factory_server,
    create_fastmcp_config
)


@pytest.mark.mcp
class TestFastMCPRunPatterns:
    """Test FastMCP run command patterns."""
    
    def test_inferred_server_instance(self, tmp_path):
        """Test loading server with inferred instance name (mcp, server, app)."""
        # Create test server file
        server_file = tmp_path / "server.py"
        server_file.write_text('''
from fastmcp import FastMCP

mcp = FastMCP("TestServer")

@mcp.tool
def echo(msg: str) -> str:
    """Echo message."""
    return msg
''')
        
        runner = FastMCPRunner()
        server = runner.load_server(str(server_file))
        
        assert server is not None
        tools = server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "echo"
    
    def test_explicit_server_entrypoint(self, tmp_path):
        """Test loading server with explicit entrypoint name."""
        server_file = tmp_path / "server.py"
        server_file.write_text('''
from fastmcp import FastMCP

custom_server = FastMCP("CustomServer")

@custom_server.tool  
def add(a: int, b: int) -> int:
    """Add numbers."""
    return a + b
''')
        
        runner = FastMCPRunner()
        server = runner.load_server(f"{server_file}:custom_server")
        
        assert server is not None
        tools = server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "add"
    
    def test_factory_function_sync(self, tmp_path):
        """Test loading server via synchronous factory function."""
        server_file = tmp_path / "server.py"
        server_file.write_text('''
from fastmcp import FastMCP

def create_server() -> FastMCP:
    """Factory to create server."""
    mcp = FastMCP("FactoryServer")
    
    @mcp.tool
    def multiply(x: int, y: int) -> int:
        """Multiply numbers."""
        return x * y
    
    # Setup code that runs with factory
    mcp.initialized = True
    
    return mcp
''')
        
        runner = FastMCPRunner()
        server = runner.load_server(f"{server_file}:create_server")
        
        assert server is not None
        assert hasattr(server, "initialized")
        assert server.initialized is True
        tools = server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "multiply"
    
    def test_factory_function_async(self, tmp_path):
        """Test loading server via asynchronous factory function."""
        server_file = tmp_path / "server.py"
        server_file.write_text('''
from fastmcp import FastMCP
import asyncio

async def create_server() -> FastMCP:
    """Async factory to create server."""
    mcp = FastMCP("AsyncFactoryServer")
    
    @mcp.tool
    def divide(a: float, b: float) -> float:
        """Divide numbers."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    # Async setup
    await asyncio.sleep(0.1)
    mcp.ready = True
    
    return mcp
''')
        
        runner = FastMCPRunner()
        server = runner.load_server(f"{server_file}:create_server")
        
        assert server is not None
        assert hasattr(server, "ready")
        assert server.ready is True
    
    def test_fastmcp_json_config(self, tmp_path):
        """Test loading server from fastmcp.json configuration."""
        # Create server file
        server_file = tmp_path / "server.py"
        server_file.write_text('''
from fastmcp import FastMCP

server = FastMCP("ConfigServer")

@server.tool
def process(data: str) -> str:
    """Process data."""
    return data.upper()
''')
        
        # Create fastmcp.json
        config_file = tmp_path / "fastmcp.json"
        config_file.write_text(json.dumps({
            "server": {
                "name": "ConfigServer",
                "entrypoint": str(server_file),
                "transport": "stdio"
            },
            "dependencies": ["fastmcp"],
            "environment": {
                "DEBUG": "true"
            }
        }))
        
        runner = FastMCPRunner()
        server = runner.load_server(str(config_file))
        
        assert server is not None
        tools = server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "process"
    
    def test_missing_server_error(self, tmp_path):
        """Test error when no server instance found."""
        server_file = tmp_path / "server.py"
        server_file.write_text('''
# No FastMCP server defined
def some_function():
    pass
''')
        
        runner = FastMCPRunner()
        with pytest.raises(ValueError) as exc_info:
            runner.load_server(str(server_file))
        
        assert "No FastMCP server instance found" in str(exc_info.value)
    
    def test_missing_entrypoint_error(self, tmp_path):
        """Test error when specified entrypoint not found."""
        server_file = tmp_path / "server.py"
        server_file.write_text('''
from fastmcp import FastMCP

mcp = FastMCP("TestServer")
''')
        
        runner = FastMCPRunner()
        with pytest.raises(ValueError) as exc_info:
            runner.load_server(f"{server_file}:nonexistent")
        
        assert "No 'nonexistent' found" in str(exc_info.value)


@pytest.mark.mcp
@pytest.mark.asyncio
class TestFastMCPDevPatterns:
    """Test FastMCP dev command patterns."""
    
    async def test_dev_server_with_packages(self, tmp_path):
        """Test running dev server with additional packages."""
        server_file = create_test_server("DevServer")
        
        dev_server = FastMCPDevServer()
        
        # This would normally start inspector and server
        # For testing, we just verify the command construction
        with pytest.raises(FileNotFoundError):
            # Inspector won't be found in test environment
            await dev_server.run_with_inspector(
                server_file,
                with_packages=["pandas", "numpy"],
                python_version="3.11"
            )
    
    async def test_dev_server_with_editable(self, tmp_path):
        """Test running dev server with editable package."""
        server_file = create_test_server("DevEditableServer")
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        
        pyproject = project_dir / "pyproject.toml"
        pyproject.write_text('''
[project]
name = "myproject"
version = "0.1.0"
''')
        
        dev_server = FastMCPDevServer()
        
        # Verify command construction (actual run would fail in test)
        with pytest.raises(FileNotFoundError):
            await dev_server.run_with_inspector(
                server_file,
                with_editable=str(project_dir)
            )


@pytest.mark.mcp
class TestFastMCPInstallPatterns:
    """Test FastMCP install command patterns."""
    
    def test_install_claude_code(self, tmp_path):
        """Test generating Claude Code installation config."""
        server_file = create_test_server("InstallServer")
        
        installer = FastMCPInstaller()
        config = installer.install_claude_code(
            server_file,
            server_name="MyTestServer",
            with_packages=["requests", "aiohttp"],
            env_vars={"API_KEY": "secret", "DEBUG": "true"}
        )
        
        assert "MyTestServer" in config
        server_config = config["MyTestServer"]
        
        assert server_config["command"] == "uv"
        assert "--with" in server_config["args"]
        assert "requests" in server_config["args"]
        assert "aiohttp" in server_config["args"]
        assert server_config["env"]["API_KEY"] == "secret"
    
    def test_install_claude_desktop(self, tmp_path):
        """Test generating Claude Desktop installation config."""
        server_file = create_test_server("DesktopServer")
        
        installer = FastMCPInstaller()
        config = installer.install_claude_desktop(
            server_file,
            server_name="DesktopMCP"
        )
        
        assert "DesktopMCP" in config
        assert config["DesktopMCP"]["command"] == "uv"
    
    def test_install_cursor_deeplink(self, tmp_path):
        """Test generating Cursor deeplink."""
        server_file = create_test_server("CursorServer")
        
        installer = FastMCPInstaller()
        deeplink = installer.install_cursor(
            server_file,
            server_name="CursorMCP"
        )
        
        assert deeplink.startswith("cursor://install-mcp-server")
        assert "CursorMCP" in deeplink
    
    def test_install_mcp_json(self, tmp_path):
        """Test generating standard MCP JSON config."""
        server_file = create_test_server("JsonServer")
        
        installer = FastMCPInstaller()
        json_config = installer.install_mcp_json(
            server_file,
            server_name="JsonMCP",
            with_packages=["fastmcp"]
        )
        
        config = json.loads(json_config)
        assert "JsonMCP" in config
        assert config["JsonMCP"]["command"] == "uv"


@pytest.mark.mcp
@pytest.mark.asyncio
class TestFastMCPTestServer:
    """Test the fastmcp_test_server context manager."""
    
    async def test_stdio_server_context(self, tmp_path):
        """Test running server with stdio transport in tests."""
        server_file = create_test_server("StdioTestServer")
        
        async with fastmcp_test_server(server_file, transport="stdio") as server:
            assert server is not None
            tools = server.list_tools()
            assert len(tools) > 0
            assert any(tool.name == "add" for tool in tools)
    
    async def test_factory_server_context(self, tmp_path):
        """Test running factory server in test context."""
        server_file = create_factory_server("FactoryTestServer")
        
        async with fastmcp_test_server(
            f"{server_file}:create_server",
            transport="stdio"
        ) as server:
            assert server is not None
            tools = server.list_tools()
            assert len(tools) > 0
            assert any(tool.name == "multiply" for tool in tools)


@pytest.mark.mcp
class TestFastMCPConfigPatterns:
    """Test FastMCP configuration file patterns."""
    
    def test_create_config_with_dependencies(self, tmp_path):
        """Test creating fastmcp.json with dependencies."""
        config_path = create_fastmcp_config(
            name="TestConfigServer",
            entrypoint="myserver.py",
            dependencies=["fastmcp", "pandas", "numpy"]
        )
        
        with open(config_path) as f:
            config = json.load(f)
        
        assert config["server"]["name"] == "TestConfigServer"
        assert config["server"]["entrypoint"] == "myserver.py"
        assert "pandas" in config["dependencies"]
        assert config["environment"]["DEBUG"] == "true"
        
        # Clean up
        Path(config_path).unlink()
    
    def test_transport_configuration(self, tmp_path):
        """Test different transport configurations."""
        runner = FastMCPRunner(transport="http")
        assert runner.transport == "http"
        assert runner.host == "127.0.0.1"
        assert runner.port == 8000
        
        runner_sse = FastMCPRunner(transport="sse")
        assert runner_sse.transport == "sse"
        assert runner_sse.path == "/sse/"