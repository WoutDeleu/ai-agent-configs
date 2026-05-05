# LLM Configs

API parameters and model configuration templates for each LLM provider.

## Structure

| Directory | Provider |
|-----------|----------|
| `claude/` | Anthropic Claude |
| `openai/` | OpenAI GPT |
| `gemini/` | Google Gemini |

## File conventions

- `config.example.json` — parameter template; copy into your project and fill in your values
- `models.json` — reference list of available models with context windows and capabilities

---

## Per-project API keys

Each project gets its own copy of the config, which means each project can use a **different API key**. This is useful for:

- Separating billing across projects or teams
- Using restricted keys (e.g. lower rate limits) for dev/staging environments
- Rotating or revoking a key for one project without affecting others

### Setup for a new project

```bash
# Copy the template for your provider into your project
cp llm-configs/claude/config.example.json /your-project/config.json

# Fill in your key and adjust parameters
# Never commit config.json — it is already covered by .gitignore
```

If your project uses environment variables instead of a JSON file, copy the values into a `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_MAX_TOKENS=8096
```

`.env` files are also covered by `.gitignore`.

### Keeping secrets out of version control

The `.gitignore` at the root of this repo excludes:

```
.env
.env.*        # .env.dev, .env.prod, etc.
*.secret
*.key
```

Only the `.example` files are committed. They document the shape of the config without containing real credentials. Never put a real API key in an `.example` file.

### Multiple environments (dev / staging / prod)

Use suffixed files for environment-specific configs and load the right one at runtime:

```
your-project/
├── config.dev.json       # dev key, lower rate limits, verbose logging
├── config.staging.json   # staging key
├── config.prod.json      # production key
└── config.example.json   # committed template (no real key)
```

Or with environment variables:

```
.env.dev
.env.staging
.env.prod
.env.example   # committed template
```

---

## Using `models.json`

`models.json` is a reference you can use in two ways:

**1. Human reference** — look up model IDs, context windows, and capabilities without visiting the provider's docs.

**2. Programmatic validation** — load it at startup to check that the configured model ID is valid:

```python
import json

with open("llm-configs/claude/models.json") as f:
    catalog = json.load(f)

known_ids = {m["id"] for m in catalog["models"]}
assert config["default_model"] in known_ids, f"Unknown model: {config['default_model']}"
```
