# Prompts

A library of reusable system prompts and user prompt templates.

## Structure

| Directory | Purpose |
|-----------|---------|
| `system/` | System prompts — define agent persona, constraints, and behavior |
| `user/`   | User-facing prompt templates with `{{variable}}` placeholders |

## Conventions

- Variables use `{{double_brace}}` syntax.
- One prompt per file; filename describes the use case.
- System prompts are plain Markdown.
- Keep prompts focused — one responsibility per file.
