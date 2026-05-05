Synchronize AI tool configuration files in the current project from the canonical `CLAUDE.md`.

Many AI coding tools (GitHub Copilot, Cursor, Windsurf) read their own instruction files, but all want the same core content: project context, stack, and conventions. This skill extracts the shared content from `CLAUDE.md` and writes or updates each tool's config file, keeping them in sync without manual duplication.

---

## Step 1 — Read CLAUDE.md

Read the project's `CLAUDE.md`. Identify two sections:

**Shared content** — generic project information any AI tool benefits from:
- Project description and purpose
- Tech stack
- Code conventions (naming, folder structure, test strategy)
- Architecture decisions
- What the AI should and should not do autonomously

**Claude-specific content** — skip this when generating other tool configs:
- Hooks and permissions
- Skill invocations (`/skill-name`)
- References to `.claude/` directories
- Claude Code-specific syntax

---

## Step 2 — Detect which tools are in use

Check for existing config files or tool-specific directories:

| Tool | Config file |
|------|-------------|
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursorrules` or `.cursor/rules/*.md` |
| Windsurf | `.windsurfrules` |

For each detected file: update it.
For each undetected file: do **not** create it unless the user explicitly asks. Only sync tools already present in the project.

If no tool config files exist, report this and ask the user which tools they want to add before proceeding.

---

## Step 3 — Generate updated content

For each tool config file being updated or created, produce:

```markdown
# {{Tool name}} Instructions

> Auto-generated from CLAUDE.md — do not edit directly. Run `/sync-ai-configs` to update.

{{shared content extracted from CLAUDE.md}}
```

Rules for content extraction:
- Keep all headings, bullet points, and tables from the shared sections.
- Rewrite any Claude-specific phrasing in neutral terms (e.g. "Claude should not" → "Do not").
- Remove any section that references Claude Code features (hooks, skills, permissions).
- Preserve `{{placeholders}}` as-is if present.

---

## Step 4 — Write and report

Write each file. Then report:

```
Synced AI tool configs from CLAUDE.md:

✓ .github/copilot-instructions.md  (updated)
✓ .cursorrules                      (updated)
✗ .windsurfrules                    (not found — skipped)

Shared sections included: Project context, Stack, Conventions, Architecture
Skipped (Claude-specific): Hooks, Permissions, Skills
```

If the shared content in CLAUDE.md is too thin to be useful (under ~5 meaningful lines), warn the user and suggest expanding CLAUDE.md before syncing.
