# CrewAI Web Search MCP

MCP server providing web search and content extraction for AI agents.

## Tools

### `web_search`
Search the web using a query string.
- **`query`** (string, required): Search query

### `extract_content`
Extract text content from a URL.
- **`url`** (string, required): URL to extract content from

## Quick Start (local)

```bash
pip install -r requirements.txt
export MCP_BILLING_API=https://mcp-billing-api.onrender.com
uvicorn server:starlette_app --host 0.0.0.0 --port 8000
```

## Usage with Claude Desktop / MCP clients

```json
{
  "mcpServers": {
    "crewai-web-search-mcp": {
      "url": "https://mcp-web-search.onrender.com/"
    }
  }
}
```

## Deployed endpoint

`https://mcp-web-search.onrender.com/` — Streamable HTTP transport at root path. Health check at `/health`.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `MCP_BILLING_API` | Yes | Billing API endpoint |
| `MCP_LICENSE_KEY` | Yes | License key for billing |
| `AGENTICMARKET_SECRET` | No | Secret for AgenticMarket authentication |

## License

MIT
