# Agents

Agents are project-specific. They are not stored here as ready-to-use files because they contain paths, package names, tooling commands, and bounded context names that differ for every project.

## How to get agents for your project

Each workflow provides a set of agent templates tailored to its architecture. Find the one that matches your project type:

| Workflow | Agent templates |
|----------|----------------|
| [Java hexagonal microservice](../workflows/java-hexagonal-microservice/agents/) | planner, domain-analyst, developer, test-writer, doc-writer, story-writer |

## How to use the templates

```bash
# 1. Copy the agent templates for your workflow into your project
cp workflows/java-hexagonal-microservice/agents/*.md /your-project/.claude/agents/

# 2. Open each file and replace every {{placeholder}} with your project's values
#    See the workflow's agents/README.md for the full placeholder reference

# 3. Verify no placeholder remains before using the agents
grep -r "{{" /your-project/.claude/agents/
```

Agents live in `.claude/agents/` inside each project — not globally. This keeps them scoped to the project they were configured for.
