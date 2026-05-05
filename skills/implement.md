Implement a user story in the Java hexagonal microservice. Follows a strict two-workflow sequence with human approval gates before advancing to each phase.

**Input:** A GitHub issue number (`#42`) or inline user story text.

---

## Prerequisites

Before starting, verify these architecture reference files are readable:
- `.claude/architecture/architecture.md`
- `.claude/architecture/conventions.md`
- `.claude/architecture/testing.md`
- `.claude/architecture/project-structure.md`

If missing, stop and ask the user to copy them from `workflows/java-hexagonal-microservice/` in the ai-agent-configs repo.

---

# Workflow 1 — Analysis & Documentation

## Step 1 — Load the user story

If given an issue number, fetch it:

```bash
gh issue view <number> --json title,body
```

Read the full acceptance criteria and proposed implementation. If anything is ambiguous or contradicts the architecture docs, raise it now before proposing a plan.

---

## Step 2 — Implementation plan (planner agent)

Use the `planner` agent. Produce a structured plan:

**Affected layers**
List each layer that changes (domain, port, use case, inbound adapter, outbound adapter) and why.

**Files to create**
| File path | Layer | What it contains |
|-----------|-------|-----------------|
| ... | ... | ... |

**Files to modify**
| File path | What changes |
|-----------|-------------|
| ... | ... |

**Domain impact**
List new or modified: entities, value objects, aggregates, domain events, domain exceptions.

**Port changes**
List new or modified: inbound ports (use case interfaces), outbound ports (repository/publisher interfaces).

**Event changes**
List new Kafka topics, new event types, or changes to existing schemas.

**Open questions**
Anything needing a decision before development starts.

---

> **--- GATE-1: Plan ---**
> Present the full plan above. Wait for `approve` or feedback.
> No files are written until GATE-1 passes.

---

## Step 3 — Domain model analysis (domain-analyst agent)

Use the `domain-analyst` agent. Compare the approved plan against existing documentation:

- Read `docs/asciidoc/_sections/domain_model.adoc` (or equivalent)
- Read `docs/asciidoc/_sections/event_flows.adoc` (or equivalent)
- Read existing Mermaid diagrams in `docs/asciidoc/diagrams/`

**Does the domain model need to change?**

If **no**: state this explicitly and proceed directly to GATE-2 (approve without changes).

If **yes**: produce specific proposals:

- New or modified entities/value objects/aggregates — describe the change in plain language
- New or modified domain events — list name, fields, and emitting use case
- UML class diagram changes — show as a Mermaid `classDiagram` diff (before/after)
- Event flow changes — show as a Mermaid `sequenceDiagram` diff (before/after)

---

> **--- GATE-2: Documentation changes ---**
> Present all proposed doc changes above.
> Wait for `approve` or feedback.
> If no domain changes are needed, type `approve` to proceed.

---

## Step 4 — Update documentation (doc-writer agent)

Use the `doc-writer` agent. Apply approved changes now, before any code is written:

- Update `docs/asciidoc/_sections/domain_model.adoc`
- Update `docs/asciidoc/_sections/event_flows.adoc`
- Update Mermaid diagrams in `docs/asciidoc/diagrams/`
- Update `README.md` if the public API or behavior description changes

Confirm each file updated and show a brief summary of what changed.

---

# Workflow 2 — Development & Testing

## Step 5 — Implement incoming port (developer agent)

Use the `developer` agent. Implement in strict order — **do not move to the next step until the current one is complete**.

### 5a. Inbound port interface

Define the use case interface in `core/<bounded-context>/port/`:

```java
public interface <Action><Entity>UseCase {
    <Result> execute(<Action><Entity>Command command);
}
```

Define the command and result records.

### 5b. Use case implementation

Implement the use case in `core/<bounded-context>/usecase/`:

- Annotate with `@Usecase`
- Inject only outbound port interfaces — never adapters
- Orchestrate: load from repository, apply domain logic, persist, publish event via outbound port
- Emit domain events through the outbound port (never directly to Kafka)

### 5c. Outbound port and adapter

Define outbound port interface(s) in `core/<bounded-context>/port/`:

```java
public interface <Feature>OutboundPort { ... }
```

Implement adapters in `adapters/<system>/<feature>/adapter/`:
- Repository adapter: JPA entity, mapper, Spring Data repo, port implementation
- Event publisher adapter: outbox adapter (writes to DB outbox table — never calls Kafka directly)
- HTTP client adapter (if applicable): WebClient config, request/response mapping

---

> **--- GATE-3: Implementation review ---**
> Present a summary table of all files created and modified.
> Wait for `approve` or feedback before writing any tests.

---

## Step 6 — Tests (test-writer agent)

Use the `test-writer` agent. Write tests in this strict order.

### 6a. Domain unit tests

For each new or changed entity, value object, or aggregate:

- `@Test void <scenario>()` — happy path
- `@Test void <scenario>_whenInvariantViolated_throws()` — one test per invariant
- `@Test void <scenario>_emitsDomainEvent()` — if domain events are emitted
- No Spring context, no mocks, no infrastructure imports
- Use `InMemoryRepository` for any persistence needs
- Use Object Mother pattern with `random()` as default

### 6b. Use case tests (`@UsecaseTest`)

For each use case:

- Mock all outbound ports with `InMemoryRepository` or Mockito
- Test happy path end-to-end through the use case
- Test each error condition (entity not found, port throws, invariant violated)
- Verify domain events are passed to the outbound port
- Use Object Mothers — `random()` by default

### 6c. Kafka consumer tests (if Kafka is involved)

For each new Kafka listener:

- Use `@KafkaConsumerTest` slice annotation
- Publish a test message → verify correct use case is called with correct command
- Test idempotency: same message ID twice → use case called once
- Test malformed/invalid message → DLT entry written, offset committed

### 6d. Data API tests (if a new REST endpoint or data query is added)

- `@DataJpaTest` for new repository methods
- Test save, find, and custom query methods against a real Testcontainers DB
- Test mapper correctness: domain object → JPA entity → domain object round-trip

### 6e. Integration tests (if new exceptions or new flows are introduced)

For each acceptance criterion in the user story:

- `@IntegrationTest` — full application context, Testcontainers for DB + Kafka
- Drive through the inbound adapter (Kafka message or HTTP request)
- Assert: response/acknowledgment, DB state, produced Kafka messages, external HTTP calls
- Must cover: happy path, at least one failure path, idempotency (if applicable)

### 6f. Gold standard test suite

If the project has a gold standard / smoke test suite:

- Add the new happy-path flow as a scenario
- Confirm the suite still passes end-to-end

---

> **--- GATE-4: Full review ---**
> Present a complete test summary:
> - Test class name | Layer | Cases covered
>
> State what is and is not covered, and why.
> Wait for `approve` before committing or opening a PR.

---

## Step 7 — Commit and PR

On final approval:

```bash
git add <specific files>
git commit -m "feat(<bounded-context>): <short description>

Implements #<issue-number>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

gh pr create \
  --title "feat(<bounded-context>): <short description>" \
  --body "Closes #<issue-number>

## Changes
<summary of what was implemented>

## Test coverage
<summary of tests added>"
```

Report the PR URL and ask the user to review on GitHub.
