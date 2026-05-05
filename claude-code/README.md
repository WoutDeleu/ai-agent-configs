# Claude Code Configs

Configuration templates for the Claude Code CLI.

## Contents

| Directory  | Purpose |
|------------|---------|
| `settings/` | `settings.json` templates for project and global Claude Code settings |
| `hooks/`    | Shell scripts triggered by Claude Code hook events |
| `skills/`   | Reusable slash-command skill definitions (`.md` files) |

## Settings

Copy a template from `settings/` into your project's `.claude/settings.json`:

```bash
cp settings/base.json /your-project/.claude/settings.json
```

## Hooks

Hooks are shell scripts that Claude Code executes on events like `PreToolUse`, `PostToolUse`, `Stop`, etc. Place them in your project's `.claude/hooks/` directory and reference them in `settings.json`.

## Skills

Skills are Markdown files that define reusable slash commands. Drop them into `~/.claude/skills/` (global) or `.claude/skills/` (project-local).
