# AgenticMarket Submission: Web Search MCP Server

## Step 1: Sign up & get API key
1. Go to https://agenticmarket.dev and sign up with GitHub
2. Go to https://agenticmarket.dev/dashboard/api-keys
3. Generate an API key (format: `am_live_xxxxxxxxxxxx`)
4. Save it — you'll need it later to test

## Step 2: Submit server at https://agenticmarket.dev/dashboard/submit

### Form fields to fill in:

| Field | Value |
|---|---|
| **Name** | `web-search` (lowercase, no spaces — permanent) |
| **Short description** | Real-time web search and content extraction for AI agents. Performs web searches via SerpAPI and extracts webpage content into clean text. |
| **Long description** | See markdown below |
| **MCP server URL** | `https://mcp-web-search-elgl.onrender.com/mcp` (permanent — contact support to change) |
| **Category** | Web Scraping |
| **Price per call** | `3` (cents = $0.03 — this is the minimum) |
| **Visibility** | Listed |
| **Free trial calls** | `50` |

### Long description (paste this):

```markdown
# Web Search MCP Server

A real-time web search and content extraction MCP server for AI agents and LLM-powered applications.

## Tools

### `web_search`
Performs a web search using SerpAPI and returns structured results (titles, URLs, snippets).

**Parameters:**
- `query` (string, required) — The search query

### `extract_content`
Extracts and cleans webpage content from a given URL. Strips navigation, ads, and boilerplate.

**Parameters:**
- `url` (string, required) — The URL to extract content from

## Usage

### Direct MCP client config
```json
{
  "mcpServers": {
    "web-search": {
      "url": "https://mcp-web-search-elgl.onrender.com/mcp",
      "headers": {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

### Set license key (for billing)
```
set MCP_LICENSE_KEY=your-key
```

## Pricing
- Free tier: 50 calls/day with no license key
- Pay-per-use: $0.01/call ($20 for 2,000 calls)
- Unlimited: $19/month
- Also available on AgenticMarket (billed per call by AgenticMarket)

## Links
- GitHub: https://github.com/KennyWayn3/web-search-mcp-server
- PyPI: https://pypi.org/project/web-search-mcp-server/
- Gumroad: https://stinkmaster37.gumroad.com/l/ushdqa
```

## Step 3: After submission — Add proxy secret to server

Once submitted (even in Pending state), your dashboard will show a **proxy secret**.

1. Copy the proxy secret (format: `am_server_xxxxxxxxxxxx`)
2. Set it on Render as an environment variable:

```
Go to https://dashboard.render.com/web/srv-... (your web search service)
→ Environment → Add Environment Variable
Name: AGENTICMARKET_SECRET
Value: am_server_xxxxxxxxxxxx
```

The server already has the middleware in place to validate `x-agenticmarket-secret` on every request.

## Step 4: Verify it works

```bash
# Test with correct secret
curl -s -X POST "https://mcp-web-search-elgl.onrender.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-agenticmarket-secret: am_server_xxxxxxxxxxxx" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Test without secret (should get 401)
curl -s -X POST "https://mcp-web-search-elgl.onrender.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Notes
- **Name cannot be changed after publish** — choose carefully
- **URL cannot be changed after publish** — contact support if it changes
- **Price can only be changed by publishing a new listing**
- The min price is $0.03/call (3 cents)
- You can still sell directly via Gumroad too — they coexist
