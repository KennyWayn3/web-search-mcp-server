"""
Web Search MCP Server - MCP Server
"""
import json
from mcp.server import FastMCP

app = FastMCP("Web Search MCP Server")


@app.tool()
def web_search(query: str) -> str:
    """Search the web
    query (str): Query
    """
    return json.dumps({"tool": "web_search", "params": {"query": query}})

@app.tool()
def extract_content(url: str) -> str:
    """Extract content from URL
    url (str): URL
    """
    return json.dumps({"tool": "extract_content", "params": {"url": url}})

if __name__ == "__main__":
    app.run(transport="stdio")
