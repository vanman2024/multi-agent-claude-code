import pytest

fastmcp = pytest.importorskip("fastmcp", reason="fastmcp not installed; skip MCP tests")
Client = fastmcp.Client
FastMCP = fastmcp.FastMCP


@pytest.mark.mcp
async def test_mcp_tool_schema_generation():
    """Validate input schema for a sample tool."""
    mcp = FastMCP("SchemaServer")

    @mcp.tool
    def calculate_tax(amount: float, rate: float = 0.1) -> dict:
        return {"amount": amount, "tax": amount * rate, "total": amount * (1 + rate)}

    tools = mcp.list_tools()
    assert tools, "No tools from server"
    schema = tools[0].inputSchema
    assert isinstance(schema, dict)
    assert schema.get("type") == "object"
    props = schema.get("properties", {})
    assert "amount" in props and props["amount"].get("type") in ("number", "integer")
    assert "rate" in props and props["rate"].get("type") in ("number", "integer")

