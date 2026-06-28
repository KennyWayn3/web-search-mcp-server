# CrewAI Web Search MCP

MCP server providing web search and content extraction for AI agents

## Installation

### pip
```bash
pip install crewai-web-search-mcp
```

### uvx (recommended)
```bash
uvx crewai-web-search-mcp
```

## Usage

Add to your Claude Desktop config:
```json
{"mcpServers": {"crewai-web-search-mcp": {"command": "uvx", "args": ["crewai-web-search-mcp"]}}}
```

## Available Tools
- **web_search**: Search the web
- **extract_content**: Extract content from URL

## License
MIT

[![PyPI](https://img.shields.io/pypi/v/crewai-web-search-mcp)](https://pypi.org/project/crewai-web-search-mcp/) [![GitHub](https://img.shields.io/github/stars/KennyWayn3/web-search-mcp-server)](https://github.com/KennyWayn3/web-search-mcp-server)
