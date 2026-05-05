# Setting Up a New Project with AI Agent Configs

This guide explains how to wire up Claude Code efficiently in any new project using the configs from this repo.

---

## Step 1 — Create the `.claude/` folder

```bash
mkdir -p .claude/skills
```

## Step 2 — Copy a settings template

Pick the template that fits your workflow:

| Template | When to use |
|----------|-------------|
| `claude-code/settings/base.json` | Default — balanced permissions, no auto-approve |
| `claude-code/settings/permissive.json` | Active development — auto-approves common commands to reduce prompts |

```bash
cp /path/to/ai-agent-configs/claude-code/settings/base.json .claude/settings.json
```

Edit `.claude/settings.json` to add any project-specific permission rules or hooks.

## Step 3 — Write a CLAUDE.md

`CLAUDE.md` is the single most impactful thing you can do. Claude reads it at startup and uses it as persistent context for every session.

Run `/init` inside Claude Code to generate a draft from the existing codebase, then edit it to include:

- What the project is and does
- Tech stack and architecture decisions
- Code conventions (naming, folder structure, test strategy)
- Branch and commit style
- What Claude should and should not do autonomously

**Minimum viable CLAUDE.md:**

```markdown
# <Project name>

<One paragraph: what this is and who it's for.>

## Stack
- <Language / runtime>
- <Framework>
- <Database / external services>

## Conventions
- Branch names: `feat/<name>`, `fix/<name>`
- Commits: `<type>(<scope>): <description>`
- Tests: <where they live, how to run them>

## What Claude should not do
- Never commit directly to `main`
- Never push without explicit instruction
```

## Step 4 — Copy relevant skills

Skills are slash commands Claude can invoke. Copy only what applies to the project.

```bash
# Contribution workflow (for projects that feed back into ai-agent-configs)
cp /path/to/ai-agent-configs/claude-code/skills/contribute.md .claude/skills/

# Hexagonal microservice workflow (for Java/DDD backend projects)
cp /path/to/ai-agent-configs/claude-code/skills/microservice-workflow.md .claude/skills/
```

Global skills (available in all projects):

```bash
cp /path/to/ai-agent-configs/claude-code/skills/*.md ~/.claude/skills/
```

## Step 5 — Add relevant MCP servers

Global MCP servers (configured once, available everywhere):

```bash
# GitHub — read repos, issues, PRs
claude mcp add github --scope user \
  -e GITHUB_PERSONAL_ACCESS_TOKEN={{your_token}} \
  -- npx -y @modelcontextprotocol/server-github

# Brave Search — web search
claude mcp add brave-search --scope user \
  -e BRAVE_API_KEY={{your_key}} \
  -- npx -y @modelcontextprotocol/server-brave-search

# Filesystem — explicit file access (useful for dotfile/config projects)
claude mcp add filesystem --scope user \
  -- npx -y @modelcontextprotocol/server-filesystem /path/to/allow
```

MCP server definitions (command + args) are stored in `mcp-servers/servers/` for reference.

## Step 6 — Copy a workflow (if applicable)

For structured, multi-stage development workflows, copy the relevant workflow docs into `.claude/`:

```bash
# Java hexagonal microservice architecture reference
cp -r /path/to/ai-agent-configs/workflows/java-hexagonal-microservice .claude/architecture
```

Reference the docs from `CLAUDE.md`:

```markdown
## Architecture
See `.claude/architecture/` for structure, conventions, and testing rules.
```

---

## Quick reference by project type

### Personal Linux setup (dotfiles)

- `CLAUDE.md` — target machines, package manager, what is managed
- `base.json` settings
- Filesystem MCP (to read/write config files outside the project root)
- No workflow needed

### Customer website + backend

- `CLAUDE.md` — client context, stack, deploy targets, conventions
- `permissive.json` settings (speeds up development)
- GitHub MCP (PR management, issue tracking)
- If hexagonal Java backend: copy `java-hexagonal-microservice` workflow + `microservice-workflow` skill

### General software project

- `CLAUDE.md` — stack, conventions, test strategy
- `base.json` settings
- GitHub MCP
- Brave Search MCP (for researching libraries and docs)

---

## Keeping this repo in sync

When you discover a useful config, skill, or workflow in a project, bring it back here via the contribution workflow:

```bash
# In the ai-agent-configs repo
/contribute
```

This ensures the base stays up to date and future projects benefit.
