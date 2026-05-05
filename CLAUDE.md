# CLAUDE.md

This repository stores base configurations for AI agents and LLM tooling.

## Purpose

Centralized, version-controlled configs for:
- Claude Code (settings, hooks, skills)
- LLM API parameters and system prompts
- Agent frameworks (LangChain, CrewAI, LangGraph)
- MCP server definitions

## Conventions

- Config files that contain secrets use an `.example` suffix — never commit real credentials.
- Each top-level directory has its own `README.md` explaining its contents.
- Prompts are written in Markdown; wrap variable placeholders in `{{double_braces}}`.

## Common tasks

- **Add a new skill**: drop a `.md` file into `claude-code/skills/` following the existing skill format.
- **Add an MCP server**: add a JSON definition to `mcp-servers/servers/` and update `mcp-servers/README.md`.
- **Add a system prompt**: place it in `prompts/system/` with a descriptive filename.
