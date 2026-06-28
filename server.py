"""
Web Search MCP Server - Streamable HTTP MCP Server
"""
import json, os
from mcp.server import FastMCP
from mcp_billing import billing
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class AgenticMarketMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        secret = os.getenv("AGENTICMARKET_SECRET")
        if secret:
            header_val = request.headers.get("x-agenticmarket-secret")
            if header_val != secret:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)

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


# Health check endpoint for Render
from starlette.routing import Route


async def health_check(request):
    return JSONResponse({"status": "ok"})


# ASGI app for Render / uvicorn with health check + AgenticMarket middleware
starlette_app = fastmcp.streamable_http_app()
starlette_app.add_middleware(AgenticMarketMiddleware)
starlette_app.router.routes.insert(0, Route("/health", endpoint=health_check, methods=["GET"]))

if __name__ == "__main__":
    fastmcp.run(transport="streamable-http")
