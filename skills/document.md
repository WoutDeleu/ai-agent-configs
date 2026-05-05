Update documentation for the Java hexagonal microservice without changing any implementation code.

Use this when:
- A design decision was made and needs to be recorded (ADR)
- Domain model documentation drifted from the implementation
- Event flows changed and diagrams need updating
- A new bounded context or feature needs to be documented

**Input:** A description of what changed, what needs documenting, or which section is out of date.

---

## Step 1 — Understand the scope

Read the input and classify the documentation work:

| Type | Location | When |
|------|----------|------|
| Domain model update | `docs/asciidoc/_sections/domain_model.adoc` | New entity, VO, aggregate, or domain event |
| Event flow update | `docs/asciidoc/_sections/event_flows.adoc` | New or changed Kafka topic, flow, or integration |
| Architecture update | `docs/asciidoc/_sections/architecture.adoc` | Structural change, new adapter, new pattern |
| ADR | `docs/asciidoc/_adr/ADR-NNN-<title>.adoc` | A significant design decision was made |
| README update | `README.md` | Public API, getting started, or setup changed |
| Overview update | `docs/asciidoc/_sections/overview.adoc` | Project purpose or scope changed |

Read the relevant existing files before proposing changes. Understand what is already there.

---

## Step 2 — Propose changes (doc-writer agent)

Use the `doc-writer` agent. For each file that needs updating, show:

1. **Current content** (the relevant section)
2. **Proposed change** in diff style:
   ```
   - old line
   + new line
   ```
3. **Why** this change is needed

For Mermaid diagrams (`docs/asciidoc/diagrams/`), show the full updated diagram, not just a diff.

For ADRs, use the standard template:

```asciidoc
= ADR-NNN: <Title>
:date: {{YYYY-MM-DD}}
:status: Accepted

== Context

Why was this decision needed?

== Decision

What was decided?

== Consequences

What becomes easier or harder as a result?
```

Number ADRs sequentially. Check existing ADRs for the next available number.

---

> **--- GATE: Documentation proposal ---**
> Present all proposed changes above.
> Wait for `approve` or feedback before writing any files.

---

## Step 3 — Apply changes

On approval, use the `doc-writer` agent to write all files.

After writing:

- Run a quick consistency check: does any prose reference a class name or topic name that no longer matches the implementation?
- If the AsciiDoc build can be verified locally (`mvn generate-resources` or `asciidoctor`), run it and confirm no errors.

---

## Step 4 — Commit

```bash
git add docs/ README.md
git commit -m "docs(<scope>): <short description>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Report what was updated and on which branch. Ask if a PR should be opened or if this commit should be squashed into a feature branch.
