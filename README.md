# Web Search MCP Server - MCP Server

MCP server providing web search and content extraction for AI agents

## Installation

### pip
```bash
pip install web-search-mcp-server
```

### uvx (recommended)
```bash
uvx web-search-mcp-server
```

## Usage

Add to your Claude Desktop config:
```json
{"mcpServers": {"web-search-mcp-server": {"command": "uvx", "args": ["web-search-mcp-server"]}}}
```

## Available Tools
- **web_search**: Search the web
- **extract_content**: Extract content from URL

## License
MIT
