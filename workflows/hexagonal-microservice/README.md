# Hexagonal Microservice Workflow

An AI-agent workflow for implementing user stories in microservices built on hexagonal architecture and domain-driven design.

## How to use

### 1. Copy the base config into your project

```bash
cp base.md /your-project/CLAUDE.md
```

### 2. Create a project-specific override

```bash
cp project-override.example.md /your-project/CLAUDE.project.md
```

Fill in the concrete technology stack, folder structure, and naming conventions. Claude will read both files; the override takes precedence for any section it defines.

### 3. Install the skill

```bash
cp ../../claude-code/skills/microservice-workflow.md ~/.claude/skills/
# or project-local:
cp ../../claude-code/skills/microservice-workflow.md /your-project/.claude/skills/
```

### 4. Run the workflow

In Claude Code, give Claude a user story and invoke the skill:

```
/microservice-workflow

User story:
As a customer, I want to receive an order confirmation email after placing an order,
so that I have a record of my purchase.
```

Claude will walk through each stage and stop for your approval before proceeding.

## Approval gates

| Gate | Triggered after |
|------|----------------|
| **GATE-1: Plan approved** | Implementation plan is presented |
| **GATE-2: Docs approved** | Domain model / event flow changes are documented |
| **GATE-3: Dev approved** | Full development plan is confirmed before writing code |
| **GATE-4: Tests approved** | Tests are written and ready to run |

Claude will not proceed past a gate until you explicitly type `approve` or `proceed`.

## Files

| File | Purpose |
|------|---------|
| `base.md` | Core CLAUDE.md — architecture principles, workflow, approval protocol |
| `project-override.example.md` | Template for project-specific tech stack and conventions |
