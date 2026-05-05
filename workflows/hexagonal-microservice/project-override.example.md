# CLAUDE.project.md — Project-Specific Override

Copy this file into your project root as `CLAUDE.project.md` and fill in each section.
Claude reads this alongside `CLAUDE.md`. Anything defined here overrides the base.

---

## Project overview

**Service name**: `order-service`
**Bounded context**: Order Management
**Owned by**: [team name]
**Description**: Manages the full lifecycle of customer orders from placement through fulfillment.

---

## Technology stack

| Concern | Technology |
|---------|-----------|
| Language | Kotlin 1.9 / Java 21 |
| Framework | Spring Boot 3.x |
| Persistence | PostgreSQL via Spring Data JPA |
| Messaging | Apache Kafka (Confluent Schema Registry) |
| HTTP clients | Spring WebClient |
| Testing | JUnit 5, Mockito, Testcontainers, WireMock |
| Build | Gradle (Kotlin DSL) |

---

## Folder structure

```
src/
└── main/kotlin/com/example/order/
    ├── domain/
    │   ├── model/          # e.g. Order.kt, OrderItem.kt, OrderId.kt
    │   ├── event/          # e.g. OrderPlacedEvent.kt, OrderConfirmedEvent.kt
    │   └── service/        # e.g. OrderPricingService.kt
    ├── application/
    │   ├── port/
    │   │   ├── in/         # e.g. PlaceOrderUseCase.kt, ConfirmOrderUseCase.kt
    │   │   └── out/        # e.g. OrderRepository.kt, OrderEventPublisher.kt
    │   └── service/        # e.g. PlaceOrderService.kt
    └── adapter/
        ├── in/
        │   ├── rest/       # e.g. OrderController.kt, OrderRequest.kt
        │   └── messaging/  # e.g. PaymentEventListener.kt
        └── out/
            ├── persistence/  # e.g. OrderJpaRepository.kt, OrderMapper.kt
            ├── messaging/    # e.g. KafkaOrderEventPublisher.kt
            └── http/         # e.g. InventoryServiceClient.kt

src/
└── test/kotlin/com/example/order/
    ├── domain/             # Unit tests for domain objects
    ├── application/        # Use case tests (mocked ports)
    ├── adapter/
    │   ├── in/             # Controller / listener tests (MockMvc, embedded Kafka)
    │   └── out/            # Repository tests (Testcontainers PG), Kafka producer tests
    └── integration/        # Full-stack integration tests
```

---

## Naming conventions

| Concept | Convention | Example |
|---------|-----------|---------|
| Use case interface | `<Action><Entity>UseCase` | `PlaceOrderUseCase` |
| Use case implementation | `<Action><Entity>Service` | `PlaceOrderService` |
| Incoming port command | `<Action><Entity>Command` | `PlaceOrderCommand` |
| Incoming port result | `<Action><Entity>Result` | `PlaceOrderResult` |
| Outgoing port (repository) | `<Entity>Repository` | `OrderRepository` |
| Outgoing port (publisher) | `<Entity>EventPublisher` | `OrderEventPublisher` |
| Domain event | `<Entity><PastTense>Event` | `OrderPlacedEvent` |
| REST controller | `<Entity>Controller` | `OrderController` |
| REST request model | `<Action><Entity>Request` | `PlaceOrderRequest` |
| REST response model | `<Entity>Response` | `OrderResponse` |
| JPA entity | `<Entity>Jpa` | `OrderJpa` |
| JPA repository | `<Entity>JpaRepository` | `OrderJpaRepository` |
| Mapper | `<Entity>Mapper` | `OrderMapper` |
| Kafka producer adapter | `Kafka<Entity>EventPublisher` | `KafkaOrderEventPublisher` |
| Kafka listener | `<Source>EventListener` | `PaymentEventListener` |
| Test class | `<ClassName>Test` | `PlaceOrderServiceTest` |
| Integration test | `<Flow>IntegrationTest` | `PlaceOrderIntegrationTest` |

---

## Domain model

Document your current domain model here so the agent can detect when a user story requires changes.

### Aggregates

- **Order** (root: `OrderId`)
  - `customerId: CustomerId`
  - `items: List<OrderItem>`
  - `status: OrderStatus` — `PENDING | CONFIRMED | SHIPPED | DELIVERED | CANCELLED`
  - `placedAt: Instant`

### Value objects

- `OrderId(value: UUID)`
- `CustomerId(value: UUID)`
- `Money(amount: BigDecimal, currency: Currency)`
- `OrderItem(productId: ProductId, quantity: Int, unitPrice: Money)`

### Domain events

| Event | Trigger |
|-------|---------|
| `OrderPlacedEvent` | New order created |
| `OrderConfirmedEvent` | Payment confirmed |
| `OrderCancelledEvent` | Order cancelled |

---

## Event catalog

### Produced (published by this service)

| Topic | Event type | Schema | Trigger |
|-------|-----------|--------|---------|
| `orders.placed` | `OrderPlacedEvent` | Avro v1 | Order placed |
| `orders.confirmed` | `OrderConfirmedEvent` | Avro v1 | Payment confirmed |

### Consumed (subscribed by this service)

| Topic | Event type | Produced by | Action |
|-------|-----------|-------------|--------|
| `payments.succeeded` | `PaymentSucceededEvent` | payment-service | Confirm order |
| `payments.failed` | `PaymentFailedEvent` | payment-service | Cancel order |

---

## External dependencies

| Service | Purpose | Client location |
|---------|---------|-----------------|
| `inventory-service` | Stock reservation | `adapter/out/http/InventoryServiceClient.kt` |
| `notification-service` | Send emails/SMS | `adapter/out/http/NotificationServiceClient.kt` |

---

## Architecture rules (project-specific additions)

- All Kafka consumers must be idempotent — check for duplicate message IDs before processing.
- JPA entities (`*Jpa`) are only used inside `adapter/out/persistence/`. They must not leak into the domain or application layers.
- Avro schemas live in `src/main/avro/`. Never hand-write Kafka message POJOs — always generate from schema.
- `@Transactional` belongs only in use case implementations, not in adapters.

---

## Documentation files

| File | Purpose |
|------|---------|
| `docs/domain-model.md` | Current domain model (source of truth) |
| `docs/event-catalog.md` | All produced and consumed events |
| `docs/api.yaml` | OpenAPI spec |
| `docs/adr/` | Architecture decision records |

The agent must update the relevant documentation file as part of Stage 2 and call out every change.
