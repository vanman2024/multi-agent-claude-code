import pytest

fastmcp = pytest.importorskip("fastmcp", reason="fastmcp not installed; skip MCP tests")
Client = fastmcp.Client
FastMCP = fastmcp.FastMCP


@pytest.mark.mcp
async def test_mcp_client_ping():
    """In-memory: client can ping server."""
    server = FastMCP("PingServer")
    async with Client(server) as client:
        ok = await client.ping()
        assert ok is True

