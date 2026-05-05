Generate a structured user story from a natural language feature description and post it as a GitHub issue.

The input is a free-form description of a feature or requirement. The output is a GitHub issue matching the style and structure of existing issues in the repository.

---

## Step 1 — Read existing issues for style

Fetch the last 10 open issues to understand the established format, label vocabulary, and tone:

```bash
gh issue list --limit 10 --json number,title,labels,body
```

Identify:
- Title format (e.g. `feat: <description>`, `fix: <description>`)
- Body section structure (Overview, User story, Acceptance criteria, Proposed implementation, Out of scope, Labels applied)
- Labels used and their meaning
- Whether epics reference child stories or tasks

---

## Step 2 — Read project context

Check for open epics that the new story might belong to:

```bash
gh issue list --label epic --json number,title,body
```

Also read `CLAUDE.md` and `.claude/architecture/architecture.md` (if present) to understand the domain language and bounded contexts. Use the ubiquitous language from the domain model when writing the story.

---

## Step 3 — Generate the story proposal

Using the `story-writer` agent, produce a complete issue proposal:

**Title:** `feat: <short imperative description>`

**Body:**

```markdown
## Overview

<One paragraph: what this feature is, why it is needed, and what problem it solves.>

## User story

> As a <role>, I want <goal> so that <benefit>.

## Acceptance criteria

- [ ] <Criterion 1 — observable, testable>
- [ ] <Criterion 2>
- [ ] <...>

## Proposed implementation

1. <Step 1 — high level>
2. <Step 2>
3. <...>

## Out of scope (v1)

- <What is explicitly not included in this story>

## Labels applied

`<label>` — <explanation>
```

Rules for the proposal:
- Acceptance criteria must be observable and testable — not implementation steps.
- Use the domain's ubiquitous language. Do not use generic terms if the domain has specific ones.
- If the story belongs to an open epic, reference it in the Overview: "Part of #N — <epic title>."
- Proposed implementation is high-level only — no code, no class names.
- Labels must come from the existing label vocabulary (fetched in Step 1).

---

> **--- GATE: Story proposal ---**
> Present the full issue title and body above.
> Wait for the user to type `approve`, or provide feedback to revise.
> Do not create any GitHub issue until approved.

---

## Step 4 — Create the issue

On approval, create the issue:

```bash
gh issue create \
  --title "<title>" \
  --body "<body>" \
  --label "<label>"
```

If the story belongs to an epic, link it as a sub-issue:

```bash
gh api repos/{owner}/{repo}/issues/{epic-number}/sub_issues \
  --method POST \
  --field sub_issue_id=<new-issue-number>
```

Report the created issue URL and number. Ask if the issue should also be added to a GitHub Project:

```bash
gh project item-add {{project-number}} --owner {{owner}} --url <issue-url>
```

Use `{{project-number}}` and `{{owner}}` as placeholders — fill from CLAUDE.md or ask the user.
