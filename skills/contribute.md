Analyze and implement the contribution to the ai-agent-configs repository described below.

This repository is a centralized, reusable base for AI agent configurations. Contributions must be generic and reusable — not tied to a specific project. Follow each stage in strict order. Do not write any files before GATE-2 is approved.

---

## Stage 1 — Analyze

First, identify the contribution type:
- **Skill** — a new Claude Code slash command (`skills/`)
- **Workflow** — a multi-stage agent workflow with approval gates (`workflows/`)
- **Config / template** — LLM API config, settings template (`llm-configs/`)
- **MCP server** — a new MCP server definition (`mcp-servers/servers/`)
- **Prompt** — a system or user prompt template (`prompts/`)
- **Framework config** — agent framework template (`agent-frameworks/`)

Then evaluate against these criteria:

**Valid?**
Does the request make sense as described? Is it complete enough to implement? If anything is ambiguous or missing, ask now before proceeding.

**Already exists?**
Check the repo for similar content. If something equivalent exists, say so and propose extending it rather than duplicating.

**Reusable?**
Would this be useful across multiple projects, or is it too specific to one codebase? If it's too specific, flag this and suggest how to make it more generic (e.g. using `{{placeholders}}`).

**Worth adding?**
Does it add meaningful value to the repo? Is the effort proportionate to the benefit?

Present the analysis clearly: contribution type, evaluation result, and a recommendation (proceed / modify scope / decline with reason).

---

> **--- GATE-1: Analysis ---**
> Present the analysis above and wait.
> Type `approve` to proceed to planning, or provide feedback to adjust the scope.

---

## Stage 2 — Plan

Produce a concrete implementation plan:

**Files to create**
| File path | Contents |
|-----------|----------|
| ... | ... |

**Files to modify**
| File path | What changes |
|-----------|-------------|
| ... | ... |

**Naming decisions**
List any names (files, directories, placeholders) that could reasonably go multiple ways, and state which you chose and why.

**Conventions to apply**
List the repo conventions that are relevant to this contribution (from CLAUDE.md).

---

> **--- GATE-2: Plan ---**
> Present the plan above and wait.
> Type `approve` to begin implementation, or provide feedback to revise.

---

## Stage 3 — Execute

Create a feature branch before touching any files:

```bash
git checkout -b feat/<type>/<name>
# examples:
#   feat/skill/langgraph-debug
#   feat/workflow/rag-pipeline
#   feat/mcp/postgres
#   feat/prompt/chain-of-thought
```

Implement every file from the approved plan. Follow all conventions from CLAUDE.md:
- Secrets and API keys use `.example` suffix — never commit real values.
- Variable placeholders use `{{double_brace}}` syntax.
- Every new directory gets a `README.md` or is documented in its parent's `README.md`.
- Prompts are plain Markdown.
- Top-level `README.md` is updated if a new top-level section is introduced.

---

## Stage 4 — Critical review

Review the implementation against this checklist. Fix every failure before continuing. Report the result of each item.

- [ ] **Reusability**: no hardcoded project-specific values; variables use `{{placeholders}}`
- [ ] **Secrets**: no API keys, tokens, or passwords — sensitive files have `.example` suffix
- [ ] **Documentation**: every new file is documented (inline or in a README)
- [ ] **Naming**: filenames and directory names follow existing conventions in this repo
- [ ] **Consistency**: style, format, and depth are consistent with existing content in the same category
- [ ] **README coverage**: parent README updated if new content was added alongside existing items
- [ ] **Top-level README**: updated if a new top-level section was introduced
- [ ] **No dead ends**: every `README.md` that references other files actually links to files that exist

Report: `PASS` or `FAIL — <what was wrong and what was fixed>` for each item.

---

## Stage 5 — PR and notify

Commit all changes on the feature branch, then create a pull request:

```bash
git add <specific files>
git commit -m "<type>(<scope>): <short description>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

gh pr create \
  --title "<type>(<scope>): <short description>" \
  --body "$(cat <<'EOF'
## What
<one sentence>

## Type
- [x] <contribution type>

## Why
<why this belongs in a base config repo>

## Checklist
- [x] No hardcoded project-specific values
- [x] No secrets committed
- [x] Documentation complete
- [x] Naming follows conventions
- [x] Consistent with existing content
- [x] READMEs updated where needed
EOF
)"
```

After the PR is created, report the PR URL and ask the user to review it on GitHub.
