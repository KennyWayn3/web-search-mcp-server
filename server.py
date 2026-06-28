"""
Web Search MCP Server - Streamable HTTP MCP Server
"""
import json, os
from mcp.server import FastMCP
from mcp_billing import billing

fastmcp = FastMCP(
    "Web Search MCP Server",
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)


@fastmcp.tool()
def web_search(query: str) -> str:
    """Search the web
    query (str): Query
    """
    allowed, msg, remaining = billing.check_and_deduct("web-search", "web_search")
    if not allowed:
        return json.dumps({"error": msg, "payment_required": True, "remaining": remaining})
    return json.dumps({"tool": "web_search", "params": {"query": query}, "credits_remaining": remaining})


@fastmcp.tool()
def extract_content(url: str) -> str:
    """Extract content from URL
    url (str): URL
    """
    allowed, msg, remaining = billing.check_and_deduct("web-search", "extract_content")
    if not allowed:
        return json.dumps({"error": msg, "payment_required": True, "remaining": remaining})
    return json.dumps({"tool": "extract_content", "params": {"url": url}, "credits_remaining": remaining})


# ASGI app for Render / uvicorn
starlette_app = fastmcp.streamable_http_app()

if __name__ == "__main__":
    fastmcp.run(transport="streamable-http")
