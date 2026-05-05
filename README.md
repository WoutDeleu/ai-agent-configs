# AI Agent Configs

A centralized repository of configuration files, prompts, and settings for AI agents and LLM-powered tools.

## Structure

```
ai-agent-configs/
├── claude-code/          # Claude Code CLI configurations
│   ├── settings/         # settings.json templates
│   ├── hooks/            # Hook scripts (pre/post tool call, etc.)
│   └── skills/           # Reusable Claude Code skills
├── llm-configs/          # LLM API configurations
│   ├── claude/           # Anthropic Claude
│   ├── openai/           # OpenAI
│   └── gemini/           # Google Gemini
├── agent-frameworks/     # Agent orchestration framework configs
│   └── langgraph/
├── mcp-servers/          # Model Context Protocol server definitions
│   └── servers/
├── prompts/              # Reusable prompt library
│   ├── system/           # System prompts
│   └── user/             # User prompt templates
└── workflows/            # End-to-end AI agent workflows
    └── hexagonal-microservice/  # Hexagonal arch + DDD microservice workflow
```

## Usage

Clone this repo and symlink or copy the configs you need into your project:

```bash
git clone <repo-url> ai-agent-configs
```

Each subdirectory has its own `README.md` with usage instructions.

## Workflows

Workflows are end-to-end operating procedures for AI agents — combining CLAUDE.md base configs, project-specific overrides, and Claude Code skills into a complete development loop.

| Workflow | Skill | Purpose |
|----------|-------|---------|
| [`hexagonal-microservice`](workflows/hexagonal-microservice/) | `/microservice-workflow` | Implement user stories in hexagonal + DDD microservices with approval gates |

See each workflow's `README.md` for setup instructions.

## Contributing

- Keep configs generic and reusable — avoid hardcoded project-specific values.
- Use `.example` suffixes for files containing secrets (e.g. `config.example.json`).
- Document every non-obvious setting inline or in the section `README.md`.
