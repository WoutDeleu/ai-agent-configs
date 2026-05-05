# Agents

Specialized Claude Code agents. Each agent has a focused role, a restricted toolset, and a system prompt that enforces its boundaries.

Copy agents to `.claude/agents/` in your project (project-local) or `~/.claude/agents/` (global).

## Java hexagonal microservice agents

These agents work together as part of the `/microservice`, `/user-story`, `/implement`, and `/document` flows.

| Agent | Role | Tools |
|-------|------|-------|
| [`story-writer`](story-writer.md) | Generates GitHub issues matching the repo's style | Bash, Read |
| [`planner`](planner.md) | Proposes implementation plans — read-only, no file writes | Bash, Read |
| [`domain-analyst`](domain-analyst.md) | Checks domain model impact and proposes UML/event flow changes — read-only | Bash, Read |
| [`developer`](developer.md) | Implements production code following hexagonal architecture | Bash, Read, Write, Edit |
| [`test-writer`](test-writer.md) | Writes tests following the project's test strategy | Bash, Read, Write, Edit |
| [`doc-writer`](doc-writer.md) | Updates README and AsciiDoc documentation | Bash, Read, Write, Edit |

## Installation

```bash
# Project-local (recommended — keeps agents scoped to the microservice)
cp /path/to/ai-agent-configs/agents/*.md .claude/agents/
```
