# Hooks

Claude Code hooks are shell scripts executed on lifecycle events.

## Available events

| Event | Trigger |
|-------|---------|
| `PreToolUse` | Before any tool call |
| `PostToolUse` | After any tool call |
| `Stop` | When Claude stops generating |
| `Notification` | On push notifications |

## Wiring a hook in settings.json

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/on-stop.sh" }
        ]
      }
    ]
  }
}
```

## Scripts in this directory

Add hook scripts here. Name them clearly, e.g. `pre-bash.sh`, `on-stop.sh`.
