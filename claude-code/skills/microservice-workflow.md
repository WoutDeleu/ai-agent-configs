Implement the user story below using the hexagonal microservice workflow defined in CLAUDE.md and CLAUDE.project.md.

Follow each stage in strict order. Do not skip stages. Do not write code before GATE-1 is approved. Do not run tests before GATE-4 is approved.

At each gate, stop completely and wait for the user to type `approve` or `proceed` before continuing. Do not interpret any other response as approval — treat it as feedback and revise accordingly.

---

## Stage 1 — Plan

Read the user story. Before proposing anything, check whether any part of it is ambiguous, contradictory, or missing acceptance criteria. If so, ask for clarification now.

Once the story is clear, produce a structured implementation plan:

**Affected layers**
List each layer that will change (domain, application, incoming adapter, outgoing adapter) and why.

**Files to create**
| File path | What it contains |
|-----------|-----------------|
| ... | ... |

**Files to modify**
| File path | What changes and why |
|-----------|---------------------|
| ... | ... |

**Domain changes**
List any new or modified entities, value objects, aggregates, or domain events.

**Port changes**
List any new or modified use case interfaces (incoming ports) and repository/publisher interfaces (outgoing ports).

**Event changes**
List any new Kafka topics, new event types, or changes to existing event schemas.

**Open questions**
List anything you need the user to decide before development can start.

---

> **--- GATE-1: Plan ---**
> Review the plan above.
> Type `approve` to proceed to documentation review, or provide feedback to revise the plan.

---

## Stage 2 — Documentation

Read the documentation files listed in CLAUDE.project.md.

For each documentation file that must change:

1. State the current content relevant to this story.
2. State the proposed change (use a diff-style format: `- old line` / `+ new line`).
3. State why the change is needed.

If the proposed implementation differs from what the documentation currently describes, call this out explicitly:

> **Documentation conflict**: The current documentation states X, but this user story requires Y. Please confirm which should take precedence before I proceed.

If no documentation changes are needed, state this explicitly.

---

> **--- GATE-2: Documentation ---**
> Review all documentation changes above.
> Type `approve` to apply the changes and proceed to development, or provide feedback.
> If no documentation changes are needed and you confirmed above, type `approve` to proceed directly to development.

Apply approved documentation changes now, then proceed to Stage 3.

---

## Stage 3 — Development

Implement in this strict order. Announce each sub-stage before starting it.

### 3a. Incoming ports

Define use case interfaces and their command/result models. No implementations yet.

For each use case interface:
- Show the full interface definition.
- Show the command object (input model).
- Show the result object (output model).
- Explain what the use case is responsible for.

### 3b. Domain

Add or modify domain objects. For each change:
- Show the full class definition.
- Explain invariants enforced.
- Show any domain events that will be emitted.

Verify: no infrastructure imports. No Spring, JPA, Kafka, or HTTP dependencies.

### 3c. Use case implementations

Implement each use case interface. For each implementation:
- Show the full class.
- Explain the orchestration logic.
- Identify which outgoing ports are called and in what order.
- Show where domain events are emitted.

### 3d. Outgoing ports and adapters

Define outgoing port interfaces, then implement each adapter:
- Repository adapters: show JPA entity, mapper, and repository implementation.
- Event publisher adapters: show Kafka producer, Avro schema if applicable.
- HTTP client adapters: show WebClient configuration and request/response mapping.

### 3e. Incoming adapters

Implement the adapter that drives the use case:
- REST controllers: show endpoint, request/response models, and mapping logic.
- Messaging listeners: show consumer, deserialization, idempotency check, and use case call.

After all code is written, present a summary:

**Development summary**
| File | Action | Key responsibility |
|------|--------|--------------------|
| ... | created/modified | ... |

---

> **--- GATE-3: Development ---**
> Review the development summary above. Confirm all files look correct.
> Type `approve` to proceed to writing tests, or provide feedback.

---

## Stage 4 — Tests

Write tests in this order. Announce each layer before starting it.

### 4a. Domain unit tests

For each entity, value object, and aggregate changed:
- Test happy-path behavior.
- Test each invariant (what happens when it is violated).
- Test domain event emission (assert event is returned or published).
- No mocks. No Spring context.

### 4b. Use case tests

For each use case implementation:
- Mock all outgoing ports using Mockito (or the project's preferred mock library).
- Test the happy path.
- Test each error condition (missing entity, port throws exception, etc.).
- Verify correct interactions with mocked ports (argument capture if needed).
- Verify domain events are passed to the event publisher port.

### 4c. Adapter tests

**Persistence** (one test class per repository adapter):
- Use Testcontainers (PostgreSQL) or the project's embedded DB.
- Test save, find, and any custom query methods.
- Test that the mapper correctly converts between JPA entity and domain object.

**Kafka producer** (one test class per publisher adapter):
- Use embedded Kafka or Testcontainers Kafka.
- Test that the correct topic is targeted.
- Test that the message payload matches the domain event fields.

**Kafka consumer** (one test class per listener):
- Publish a test message to the topic.
- Verify the correct use case is called with the correct command.
- Verify idempotency: publishing the same message ID twice calls the use case only once.

**HTTP clients** (one test class per client):
- Use WireMock to stub downstream services.
- Test happy path response mapping.
- Test 4xx and 5xx error handling.

### 4d. Integration tests

For each user story scenario (happy path + at least one failure path):
- Start the full application with Testcontainers (DB + Kafka + any required HTTP stubs).
- Drive the system through the incoming adapter (HTTP request or published Kafka message).
- Assert outcomes:
  - Response / acknowledgment received.
  - Database state is correct.
  - Expected Kafka messages were produced.
  - Expected downstream HTTP calls were made.

After all tests are written, present a summary:

**Test summary**
| Test class | Layer | Cases covered |
|-----------|-------|---------------|
| ... | domain / use-case / adapter / integration | ... |

**Coverage statement**: Briefly state what is and is not covered, and why.

---

> **--- GATE-4: Tests ---**
> Review the test summary above.
> Type `approve` to run the full test suite, or provide feedback to add or modify tests.

Run the test suite now. Report results for each layer. If any test fails, fix it before reporting completion.

---

## Stage 5 — Architecture validation

Check every item. Report pass or fail for each. Fix failures immediately.

- [ ] No domain class imports a framework or infrastructure package (Spring, JPA, Kafka, HTTP).
- [ ] No adapter class directly imports or instantiates another adapter class.
- [ ] Every new use case is accessed only via its incoming port interface.
- [ ] Every new outgoing adapter implements a defined port interface.
- [ ] All new class and method names use the ubiquitous language established in the domain model.
- [ ] No primitive obsession: domain IDs and monetary values are value objects, not raw UUIDs or BigDecimals.
- [ ] Every domain event has at least one test asserting it is emitted under the correct condition.
- [ ] All Kafka consumers implement idempotency (per CLAUDE.project.md rules, if applicable).
- [ ] `@Transactional` (or equivalent) is only applied inside use case implementations.
- [ ] Documentation files updated in Stage 2 reflect the final implementation.

---

## Completion

Once Stage 5 passes, produce a final summary:

**Story complete**

| Stage | Status |
|-------|--------|
| Plan | Approved |
| Documentation | Approved (N changes) |
| Development | N files created, N modified |
| Tests | N test cases across N classes, all passing |
| Architecture validation | All checks passed |

List any follow-up tasks, tech debt, or decisions deferred during this story.
