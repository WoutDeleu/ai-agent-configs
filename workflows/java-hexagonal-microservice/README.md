# Java Hexagonal Microservice — Architecture Reference

A reusable reference for structuring Java microservices using hexagonal architecture (ports and adapters), domain-driven design, and clean code principles.

Derived from a production Volvo manufacturing application. All Volvo-specific artifacts (internal libraries, naming, topics) are clearly marked — the architecture and patterns are fully generic.

## Files

| File | Contents |
|------|----------|
| [`architecture.md`](architecture.md) | Hexagonal layers, port/adapter patterns, domain model, notable design patterns |
| [`project-structure.md`](project-structure.md) | Maven setup, package hierarchy, folder layout for main and test sources |
| [`conventions.md`](conventions.md) | Class, method, package, and test naming conventions; stereotype annotations; null safety |
| [`testing.md`](testing.md) | Test categories, custom slice annotations, Object Mother pattern, JUnit 5 extensions |
| [`tooling.md`](tooling.md) | Maven plugins, Docker Compose local stack, GitHub Actions, Kubernetes, living docs |

## Quick start for a new project

1. Use [`project-structure.md`](project-structure.md) to set up your Maven POM and package layout.
2. Use [`architecture.md`](architecture.md) to design your ports, use cases, and adapters.
3. Copy naming patterns from [`conventions.md`](conventions.md).
4. Set up your test infrastructure using [`testing.md`](testing.md).
5. Configure tooling from [`tooling.md`](tooling.md).

## What this covers

- Spring Boot (4.x / 3.x compatible patterns)
- Java records as value objects and domain events
- Dual-cluster Kafka with transactional outbox
- Oracle JPA with Testcontainers
- Avro + Schema Registry
- AsciiDoc living documentation served at runtime
- Null safety enforced at compile time (NullAway + JSpecify)
- Google Java Format enforced at build time
