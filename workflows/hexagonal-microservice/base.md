# CLAUDE.md — Hexagonal Microservice Base

This file defines the AI agent's operating principles for this codebase.
A project-specific `CLAUDE.project.md` may extend or override any section below.

---

## Architecture

This project follows **hexagonal architecture** (ports and adapters) combined with **domain-driven design**.

### Layers

```
┌─────────────────────────────────────────────────┐
│                   Adapters                       │
│  ┌──────────────┐          ┌──────────────────┐  │
│  │   Incoming   │          │    Outgoing      │  │
│  │  (REST, gRPC,│          │  (DB, Kafka,     │  │
│  │  Messaging)  │          │   HTTP clients)  │  │
│  └──────┬───────┘          └────────┬─────────┘  │
│         │                           │             │
│  ┌──────▼───────────────────────────▼─────────┐  │
│  │              Ports (interfaces)             │  │
│  │  Incoming ports = use case interfaces       │  │
│  │  Outgoing ports = repository/service ifaces │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │                             │
│  ┌──────────────────▼──────────────────────────┐  │
│  │              Domain                          │  │
│  │  Entities · Value objects · Aggregates       │  │
│  │  Domain events · Domain services             │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Invariants

- **Domain has zero infrastructure dependencies.** No Spring, JPA, Kafka, or HTTP imports inside the domain layer.
- **Ports are interfaces, adapters are implementations.** The domain defines what it needs; adapters fulfill it.
- **Use cases orchestrate, domain objects enforce.** Business rules live in entities and value objects, not in use cases.
- **Adapters depend on ports, never on each other.** Cross-adapter communication goes through the domain.

---

## Domain-Driven Design

- Identify and name **bounded contexts** before writing code.
- Use **ubiquitous language** from the domain in all names (classes, methods, variables, tests).
- Model **aggregates** with clear consistency boundaries. Aggregates reference other aggregates by ID only.
- Emit **domain events** to communicate state changes across bounded contexts.
- Distinguish **entities** (identity-based) from **value objects** (value-based, immutable).

---

## Clean Code Standards

- One reason to change per class (SRP).
- Method length: prefer under 20 lines. Extract if a block needs a comment explaining what it does.
- No primitive obsession — wrap domain concepts in value objects.
- No magic strings or numbers — use named constants or enums.
- No `null` in domain objects — use `Optional` or a typed absence value.
- Test names describe behavior, not implementation: `should_emit_order_confirmed_event_when_payment_succeeds`.

---

## Workflow

The agent implements user stories through five sequential stages.
**The agent must not proceed past a gate without explicit human approval.**

### Stage 1 — Plan

1. Read the user story carefully.
2. Identify all affected layers: which incoming adapter, which use case(s), which outgoing ports, which domain objects.
3. List every file that will be created or modified, with a one-line description of each change.
4. Flag any ambiguities in the user story and ask for clarification before presenting the plan.
5. Present the plan in structured Markdown.

> **GATE-1**: Present the plan and wait. Do not write any code or modify any files until the user explicitly approves.

---

### Stage 2 — Documentation

1. Review existing domain model documentation, event catalogs, and flow diagrams.
2. Identify any changes required by this user story.
3. For each change, state: what it was, what it becomes, and why.
4. If the implementation requires deviating from existing documentation, flag this explicitly and request input before proceeding.
5. Update documentation files only after approval.

> **GATE-2**: Present all documentation changes and wait. Do not start development until the user explicitly approves.
> If no documentation changes are needed, state this clearly and ask whether to proceed directly to GATE-3.

---

### Stage 3 — Development

Implement in this strict order:

#### 3a. Incoming ports (use case interfaces)

- Define the use case interface in the application layer.
- Define input and output model objects (commands, queries, results).
- No implementation yet — interfaces only.

#### 3b. Domain

- Add or modify entities, value objects, and aggregates.
- Add domain events if state changes need to be communicated.
- Implement domain logic and invariants inside domain objects.

#### 3c. Use case implementations

- Implement the use case interface.
- Orchestrate calls to outgoing ports.
- Emit domain events via the event publisher port.

#### 3d. Outgoing ports and adapters

- Define outgoing port interfaces (repositories, external service clients, event publishers).
- Implement adapters (JPA repositories, Kafka producers, HTTP clients, etc.).

#### 3e. Incoming adapters

- Implement the adapter that drives the use case (REST controller, message listener, etc.).
- Map between external models and input/output models.

> **GATE-3**: Before writing any code, confirm the implementation plan with the user. After all code is written, present a summary of every changed file before moving to testing.

---

### Stage 4 — Tests

Write tests in this order:

#### 4a. Domain unit tests

- Test entities and value objects in isolation.
- No mocks. Pure input/output.
- Cover invariants, edge cases, and domain event emission.

#### 4b. Use case tests

- Test use case implementations with mocked outgoing ports.
- Verify orchestration logic: correct ports called, correct arguments, correct events emitted.
- One test class per use case.

#### 4c. Adapter tests

- **Persistence**: use an in-memory or embedded database. Test repository implementations against real SQL/queries.
- **Kafka / messaging**: use an embedded broker or testcontainers. Test that the correct messages are produced and consumed.
- **HTTP clients**: use WireMock or equivalent. Test request/response mapping and error handling.

#### 4d. Integration tests

- Spin up the full application context (testcontainers for all infrastructure).
- Drive the system through incoming adapters (HTTP, messaging).
- Assert outcomes via outgoing adapters (DB state, emitted events, downstream calls).
- Cover the happy path and at least one failure path per use case.

> **GATE-4**: After tests are written, present a summary of test coverage (files, cases, what each verifies). Wait for approval before executing the test suite.

---

### Stage 5 — Architecture Validation

After tests pass, verify:

- [ ] No domain class imports infrastructure packages.
- [ ] No adapter class imports another adapter class directly.
- [ ] All new use cases are accessed only through their port interface.
- [ ] All new outgoing adapters implement a port interface.
- [ ] Naming follows ubiquitous language established in Stage 2.
- [ ] No raw strings or primitives where value objects should be used.
- [ ] Every domain event has at least one test verifying it is emitted.

Report the result of each check explicitly. Fix any violations before declaring the story done.

---

## Approval gate protocol

The agent uses these exact prompts at each gate:

```
--- GATE-N: <name> ---
[summary of what was produced]

Type `approve` to proceed to the next stage, or provide feedback to revise.
```

The agent will not interpret silence, "ok", "yes", or "looks good" as approval.
Only the word `approve` (case-insensitive) or `proceed` advances the workflow.

---

## File organization (generic)

Adapt these patterns to the project-specific structure defined in `CLAUDE.project.md`.

```
src/
└── <bounded-context>/
    ├── domain/
    │   ├── model/          # Entities, aggregates, value objects
    │   ├── event/          # Domain events
    │   └── service/        # Domain services (stateless logic shared across use cases)
    ├── application/
    │   ├── port/
    │   │   ├── in/         # Incoming port interfaces (use cases)
    │   │   └── out/        # Outgoing port interfaces (repositories, publishers)
    │   └── service/        # Use case implementations
    └── adapter/
        ├── in/             # Incoming adapters (REST, messaging listeners)
        └── out/            # Outgoing adapters (JPA, Kafka, HTTP clients)
```

---

## What the agent must never do

- Write code before GATE-1 is approved.
- Skip a stage or gate, even if the user story seems trivial.
- Put business logic in an adapter.
- Put infrastructure code in the domain.
- Create a use case that calls another use case directly.
- Modify documentation without noting the change and receiving approval.
- Run the full test suite before GATE-4 is approved.
