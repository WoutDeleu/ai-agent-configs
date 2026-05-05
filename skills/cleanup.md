Run a pre-PR cleanup pass on the current feature branch. This skill reviews the changes on the branch, fixes common issues, and produces a readiness summary before a pull request is opened.

Run this after development is complete and before opening a PR.

---

## Step 1 — Understand the diff

```bash
git diff main...HEAD --stat
git diff main...HEAD
```

Read the full diff. Note which files changed and what the intended behavior change is. If the branch name or recent commits make the intent unclear, state what you inferred before continuing.

---

## Step 2 — Dead code and debug artifacts

Scan changed files for:

- Commented-out code blocks (not explanatory comments — actual disabled code)
- `console.log`, `System.out.println`, `print(`, `debugger`, `TODO`, `FIXME`, `HACK`, `XXX`
- Unused imports in changed files
- Unused variables or functions introduced in this branch

For each finding: remove it or flag it with a clear explanation if it should be kept.

---

## Step 3 — Documentation drift

For each changed file, check whether:

- Public API signatures changed without updating their doc comment
- A README or CLAUDE.md references behavior that no longer matches the implementation
- New public functions or classes lack any documentation

Fix obvious drift. For larger doc updates (architecture docs, READMEs), list what needs updating and propose the change — do not rewrite large docs silently.

---

## Step 4 — Test coverage check

Check whether the changed behavior has test coverage:

- Are there new or updated tests in the diff?
- If not, does existing test coverage plausibly cover the change?

If coverage looks absent for non-trivial logic, flag it explicitly. Do not write tests automatically — list what is missing and ask whether to add them.

---

## Step 5 — Secret and safety scan

Check the diff for:

- Hardcoded credentials, tokens, or API keys
- Absolute paths specific to a developer's machine
- Environment-specific config values that should be in `.env` or a config file

If found, flag immediately and do not proceed until resolved.

---

## Step 6 — Readiness summary

Produce a concise summary:

```
Cleanup complete — branch: {{branch-name}}

Files changed: N
Commits: N

Cleaned:
- Removed N commented-out code blocks
- Removed N debug statements
- Removed N unused imports

Flagged (needs decision):
- [ ] {{file}}: {{issue}}
- [ ] {{file}}: {{issue}}

Documentation: {{up to date | N items need updating}}
Test coverage: {{adequate | N gaps identified}}
Secrets: {{none found | ⚠ N issues — fix before PR}}

Recommendation: {{ready to open PR | fix flagged items first}}
```

If everything is clean, say so clearly and suggest running `/contribute` or `gh pr create` next.
