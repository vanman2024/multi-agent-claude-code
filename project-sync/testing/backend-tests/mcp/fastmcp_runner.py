"""
FastMCP Server Runner

Implements the FastMCP CLI patterns for running MCP servers in tests.
Follows the same entrypoint detection and execution patterns as `fastmcp run`.
"""

import importlib.util
import inspect
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional, Union, Dict, Callable
from contextlib import asynccontextmanager
import subprocess


class FastMCPRunner:
    """
    Runner for FastMCP servers following CLI patterns.
    
    Supports:
    - Inferred server instances (mcp, server, app)
    - Explicit server entrypoints (server.py:custom_name)
    - Factory functions (server.py:create_server)
    - FastMCP configuration files (fastmcp.json)
    - Remote server proxies (URLs)
    """
    
    def __init__(self, transport: str = "stdio"):
        self.transport = transport
        self.host = "127.0.0.1"
        self.port = 8000
        self.path = "/mcp/" if transport == "http" else "/sse/"
        
    def load_server(self, entrypoint: str) -> Any:
        """
        Load a FastMCP server from various entrypoint formats.
        
        Args:
            entrypoint: Can be:
                - "server.py" - Infers server instance
                - "server.py:custom_name" - Explicit entrypoint
                - "server.py:create_server" - Factory function
                - "fastmcp.json" - Configuration file
                - "https://example.com/mcp" - Remote proxy
        """
        if entrypoint.startswith(("http://", "https://")):
            return self._create_proxy_server(entrypoint)
        
        if entrypoint.endswith(".json"):
            return self._load_from_config(entrypoint)
            
        # Parse file:entrypoint format
        if ":" in entrypoint:
            file_path, entry_name = entrypoint.split(":", 1)
        else:
            file_path = entrypoint
            entry_name = None
            
        # Load the module
        module = self._load_module(file_path)
        
        if entry_name:
            # Explicit entrypoint
            obj = getattr(module, entry_name, None)
            if obj is None:
                raise ValueError(f"No '{entry_name}' found in {file_path}")
                
            # Check if it's a factory function
            if callable(obj) and not self._is_server_instance(obj):
                return self._call_factory(obj)
            return obj
        else:
            # Inferred entrypoint - look for mcp, server, or app
            for name in ["mcp", "server", "app"]:
                obj = getattr(module, name, None)
                if obj and self._is_server_instance(obj):
                    return obj
                    
            raise ValueError(
                f"No FastMCP server instance found in {file_path}. "
                "Looking for variables named 'mcp', 'server', or 'app'"
            )
    
    def _load_module(self, file_path: str):
        """Load a Python module from file path."""
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if not spec or not spec.loader:
            raise ImportError(f"Cannot load module from {file_path}")
            
        module = importlib.util.module_from_spec(spec)
        
        # Add parent directory to path for imports
        sys.path.insert(0, str(path.parent))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.remove(str(path.parent))
            
        return module
    
    def _is_server_instance(self, obj: Any) -> bool:
        """Check if object is a FastMCP server instance."""
        # Check for FastMCP type or duck-type checking
        return (
            hasattr(obj, "list_tools") and 
            hasattr(obj, "list_resources") and
            hasattr(obj, "list_prompts")
        ) or (
            obj.__class__.__name__ == "FastMCP"
        )
    
    def _call_factory(self, factory: Callable) -> Any:
        """Call a factory function to create server."""
        sig = inspect.signature(factory)
        
        # Factory should take no arguments
        if len(sig.parameters) > 0:
            raise ValueError("Factory function should not require arguments")
            
        # Call sync or async factory
        if inspect.iscoroutinefunction(factory):
            return asyncio.run(factory())
        else:
            return factory()
    
    def _create_proxy_server(self, url: str) -> Any:
        """Create a proxy server for remote MCP server."""
        # Implementation for proxy server
        # This would create a local FastMCP server that forwards to remote
        from fastmcp import FastMCP
        
        proxy = FastMCP(f"Proxy to {url}")
        # Add proxy implementation
        return proxy
    
    def _load_from_config(self, config_path: str) -> Any:
        """Load server from fastmcp.json configuration."""
        with open(config_path) as f:
            config = json.load(f)
            
        # Handle FastMCP configuration format
        if "server" in config:
            # Standard FastMCP config
            server_config = config["server"]
            entrypoint = server_config.get("entrypoint", "server.py")
            
            # Load dependencies if specified
            if "dependencies" in config:
                self._setup_dependencies(config["dependencies"])
                
            return self.load_server(entrypoint)
        elif "mcpServers" in config:
            # MCP standard config - run all servers
            servers = []
            for server_name, server_config in config["mcpServers"].items():
                # Handle MCP server config
                command = server_config["command"]
                args = server_config.get("args", [])
                servers.append(self._run_mcp_server(command, args))
            return servers
        else:
            raise ValueError("Invalid configuration format")
    
    def _setup_dependencies(self, dependencies: list):
        """Setup dependencies using uv."""
        for dep in dependencies:
            subprocess.run(["uv", "pip", "install", dep], check=True)
    
    def _run_mcp_server(self, command: str, args: list) -> subprocess.Popen:
        """Run an MCP server command."""
        full_command = [command] + args
        return subprocess.Popen(
            full_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    async def run_server(self, entrypoint: str, **kwargs):
        """
        Run a FastMCP server.
        
        This mimics the behavior of `fastmcp run`.
        """
        server = self.load_server(entrypoint)
        
        # Apply transport settings
        if hasattr(server, "run"):
            # FastMCP server with run method
            if self.transport == "stdio":
                await server.run()
            elif self.transport == "http":
                await server.run_http(
                    host=kwargs.get("host", self.host),
                    port=kwargs.get("port", self.port)
                )
            elif self.transport == "sse":
                await server.run_sse(
                    host=kwargs.get("host", self.host),
                    port=kwargs.get("port", self.port),
                    path=kwargs.get("path", self.path)
                )
        else:
            # Handle other server types
            return server


class FastMCPDevServer:
    """
    Development server runner that mimics `fastmcp dev`.
    Always runs via subprocess with MCP Inspector.
    """
    
    def __init__(self, inspector_version: str = "latest"):
        self.inspector_version = inspector_version
        self.ui_port = 5173
        self.server_port = 8000
        
    async def run_with_inspector(
        self, 
        entrypoint: str,
        with_packages: Optional[list] = None,
        with_editable: Optional[str] = None,
        python_version: Optional[str] = None
    ):
        """
        Run server with MCP Inspector for testing.
        
        This mimics `fastmcp dev` behavior.
        """
        # Build uv run command
        cmd = ["uv", "run"]
        
        if python_version:
            cmd.extend(["--python", python_version])
            
        if with_packages:
            for package in with_packages:
                cmd.extend(["--with", package])
                
        if with_editable:
            cmd.extend(["--with-editable", with_editable])
            
        # Add fastmcp run command
        cmd.extend(["fastmcp", "run", entrypoint])
        
        # Start inspector UI
        inspector_process = await self._start_inspector()
        
        try:
            # Run server via subprocess
            server_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for both to be ready
            await self._wait_for_ready(server_process, inspector_process)
            
            return server_process, inspector_process
            
        except Exception as e:
            if inspector_process:
                inspector_process.terminate()
            raise e
    
    async def _start_inspector(self) -> subprocess.Popen:
        """Start MCP Inspector UI."""
        # Implementation for starting inspector
        cmd = [
            "npx", 
            f"@modelcontextprotocol/inspector@{self.inspector_version}",
            "--port", str(self.ui_port),
            "--server-port", str(self.server_port)
        ]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    async def _wait_for_ready(self, server_proc, inspector_proc):
        """Wait for server and inspector to be ready."""
        # Simple wait - in practice would check for actual readiness
        await asyncio.sleep(2)


class FastMCPInstaller:
    """
    Server installer that mimics `fastmcp install`.
    """
    
    def install_claude_code(
        self,
        entrypoint: str,
        server_name: Optional[str] = None,
        with_packages: Optional[list] = None,
        with_editable: Optional[str] = None,
        env_vars: Optional[dict] = None
    ) -> dict:
        """
        Generate Claude Code installation config.
        
        Returns the configuration dict that would be installed.
        """
        config = {
            "command": "uv",
            "args": ["run", "--with", "fastmcp"]
        }
        
        if with_packages:
            for package in with_packages:
                config["args"].extend(["--with", package])
                
        if with_editable:
            config["args"].extend(["--with-editable", with_editable])
            
        config["args"].extend(["fastmcp", "run", entrypoint])
        
        if env_vars:
            config["env"] = env_vars
            
        return {server_name or Path(entrypoint).stem: config}
    
    def install_claude_desktop(self, entrypoint: str, **kwargs) -> dict:
        """Generate Claude Desktop installation config."""
        # Similar to claude_code but with desktop-specific settings
        return self.install_claude_code(entrypoint, **kwargs)
    
    def install_cursor(self, entrypoint: str, **kwargs) -> str:
        """Generate Cursor deeplink for installation."""
        config = self.install_claude_code(entrypoint, **kwargs)
        
        # Create deeplink URL
        import urllib.parse
        deeplink = f"cursor://install-mcp-server?config={urllib.parse.quote(json.dumps(config))}"
        return deeplink
    
    def install_mcp_json(self, entrypoint: str, **kwargs) -> str:
        """Generate standard MCP JSON configuration."""
        config = self.install_claude_code(entrypoint, **kwargs)
        return json.dumps(config, indent=2)


@asynccontextmanager
async def fastmcp_test_server(
    entrypoint: str,
    transport: str = "stdio",
    **kwargs
):
    """
    Context manager for running FastMCP server in tests.
    
    Usage:
        async with fastmcp_test_server("server.py") as server:
            # Test server functionality
            pass
    """
    runner = FastMCPRunner(transport=transport)
    
    if transport == "stdio":
        # For stdio, just load the server
        server = runner.load_server(entrypoint)
        yield server
    else:
        # For HTTP/SSE, run in subprocess
        process = None
        try:
            cmd = [
                "fastmcp", "run", entrypoint,
                "--transport", transport,
                "--host", kwargs.get("host", "127.0.0.1"),
                "--port", str(kwargs.get("port", 8000))
            ]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            await asyncio.sleep(1)
            
            yield process
            
        finally:
            if process:
                process.terminate()
                process.wait(timeout=5)


# Utility functions for testing
def create_test_server(name: str = "TestServer") -> str:
    """Create a test server file and return its path."""
    content = f'''
from fastmcp import FastMCP

mcp = FastMCP("{name}")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.resource("config://test")
def get_config() -> dict:
    """Get test configuration."""
    return {{"env": "test", "version": "1.0.0"}}
'''
    
    path = Path(f"test_server_{name.lower()}.py")
    path.write_text(content)
    return str(path)


def create_factory_server(name: str = "FactoryServer") -> str:
    """Create a test server with factory function."""
    content = f'''
from fastmcp import FastMCP

async def create_server() -> FastMCP:
    """Factory function to create server."""
    mcp = FastMCP("{name}")
    
    @mcp.tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    # Setup code that runs when server is created
    print("Server initialized via factory")
    
    return mcp
'''
    
    path = Path(f"test_factory_{name.lower()}.py")
    path.write_text(content)
    return str(path)


def create_fastmcp_config(
    name: str = "ConfigServer",
    entrypoint: str = "server.py",
    dependencies: Optional[list] = None
) -> str:
    """Create a fastmcp.json configuration file."""
    config = {
        "server": {
            "name": name,
            "entrypoint": entrypoint,
            "transport": "stdio"
        },
        "dependencies": dependencies or ["fastmcp"],
        "environment": {
            "DEBUG": "true",
            "ENV": "test"
        }
    }
    
    path = Path("fastmcp.json")
    path.write_text(json.dumps(config, indent=2))
    return str(path)