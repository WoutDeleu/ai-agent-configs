# MCP Servers

Model Context Protocol (MCP) server definitions for Claude Code and other MCP clients.

## What is MCP?

MCP lets you expose tools, resources, and prompts from external services to an LLM host (like Claude Code). Each server is a process the host spawns and communicates with over stdio or HTTP/SSE.

## Structure

```
servers/
└── <server-name>.json   # Server definition
```

## Adding a server to Claude Code

Add the server definition to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my-org/mcp-server"],
      "env": {
        "API_KEY": "YOUR_KEY"
      }
    }
  }
}
```

Or use the CLI:

```bash
claude mcp add my-server npx -- -y @my-org/mcp-server
```

## Server definitions in this directory

See `servers/` for individual server configs.
