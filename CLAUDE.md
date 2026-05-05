# CLAUDE.md

This repository is a centralized, version-controlled base for AI agent configurations.
It is populated by AI agents using the `/contribute` skill and reviewed by a human before merging.

## Purpose

Reusable configs for:
- Claude Code (settings, hooks, skills)
- LLM API parameters and model references
- Agent frameworks (LangGraph)
- MCP server definitions
- Prompts and workflow templates

## Contribution workflow

All changes to this repo go through the `/contribute` skill:

1. User describes what they want (new skill, config, workflow, prompt, MCP server, etc.)
2. Agent analyzes validity and fit → **GATE-1**
3. Agent proposes an implementation plan → **GATE-2**
4. Agent implements on a feature branch
5. Agent runs a critical self-review and fixes any issues
6. Agent opens a PR via `gh pr create`
7. User reviews and merges on GitHub

Never commit directly to `main`. Always use a feature branch.

## Conventions

| Rule | Detail |
|------|--------|
| Secrets | Never commit real credentials. Files with secrets use `.example` suffix. |
| Placeholders | Variable values in templates use `{{double_brace}}` syntax. |
| Documentation | Every new directory gets a `README.md`. New items in existing directories are documented in the parent `README.md`. |
| Branch names | `feat/<type>/<name>` — e.g. `feat/skill/langgraph-debug`, `feat/mcp/postgres` |
| Commit style | `<type>(<scope>): <description>` — e.g. `feat(skills): add langgraph debugging skill` |
| Reusability | All content must be generic. No hardcoded project names, paths, or team-specific values. |

## Repo structure

```
ai-agent-configs/
├── claude-code/
│   ├── settings/         # settings.json templates
│   ├── hooks/            # Hook scripts
│   └── skills/           # Claude Code slash command skills
├── llm-configs/
│   ├── claude/           # Anthropic Claude configs and model reference
│   ├── openai/
│   └── gemini/
├── agent-frameworks/
│   └── langgraph/        # LangGraph config templates
├── mcp-servers/
│   └── servers/          # MCP server definitions (.json)
├── prompts/
│   ├── system/           # System prompts
│   └── user/             # User prompt templates
└── workflows/
    └── hexagonal-microservice/  # Hexagonal arch + DDD microservice workflow
```

## GitHub

Remote: https://github.com/WoutDeleu/ai-agent-configs
PRs are created with `gh pr create`. The user does a final review on GitHub before merging.
