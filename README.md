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

**Starting a new project?** See [docs/new-project-setup.md](docs/new-project-setup.md) for a step-by-step guide on bootstrapping Claude Code in any project using configs from this repo.

## Skills

Skills are Claude Code slash commands. Copy them to `~/.claude/skills/` (global) or `.claude/skills/` (project-local).

| Skill | Command | Purpose |
|-------|---------|---------|
| [`contribute`](skills/contribute.md) | `/contribute` | Contribute a new skill, workflow, config, or prompt to this repo via a gated PR workflow |
| [`sync-ai-configs`](skills/sync-ai-configs.md) | `/sync-ai-configs` | Sync CLAUDE.md shared content to Copilot, Cursor, and Windsurf config files |
| [`cleanup`](skills/cleanup.md) | `/cleanup` | Pre-PR cleanup: remove dead code, debug artifacts, check docs and test coverage |
| [`microservice`](skills/microservice.md) | `/microservice` | Orchestrator for the Java hexagonal microservice flows |
| [`user-story`](skills/user-story.md) | `/user-story` | Generate a structured GitHub issue from a feature description |
| [`implement`](skills/implement.md) | `/implement` | Implement a user story: plan → domain analysis → docs → code → tests |
| [`document`](skills/document.md) | `/document` | Update README and AsciiDoc docs without changing code |

## Agents

Specialized agents with focused roles and restricted toolsets. Copy to `.claude/agents/` (project-local) or `~/.claude/agents/` (global). See [`agents/README.md`](agents/README.md).

| Agent | Role |
|-------|------|
| [`story-writer`](agents/story-writer.md) | Writes GitHub issues matching repo style |
| [`planner`](agents/planner.md) | Plans implementation — read-only, no file writes |
| [`domain-analyst`](agents/domain-analyst.md) | Checks domain model impact, proposes UML/event changes — read-only |
| [`developer`](agents/developer.md) | Implements production code following hexagonal architecture |
| [`test-writer`](agents/test-writer.md) | Writes tests following the project test strategy |
| [`doc-writer`](agents/doc-writer.md) | Updates README and AsciiDoc documentation |

## Workflows

Workflows are end-to-end operating procedures for AI agents — reference docs that the skills and agents load at runtime.

| Workflow | Purpose |
|----------|---------|
| [`java-hexagonal-microservice`](workflows/java-hexagonal-microservice/) | Architecture, conventions, testing, tooling, and project structure reference |

## Contributing

- Keep configs generic and reusable — avoid hardcoded project-specific values.
- Use `.example` suffixes for files containing secrets (e.g. `config.example.json`).
- Document every non-obvious setting inline or in the section `README.md`.
