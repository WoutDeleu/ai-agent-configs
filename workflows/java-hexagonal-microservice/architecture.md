# Architecture

## Layer overview

```
┌──────────────────────────────────────────────────────────────────┐
│                          Adapters                                │
│                                                                  │
│  Inbound adapters                   Outbound adapters           │
│  (Kafka consumers, REST)            (Kafka producers, JPA,      │
│                                      HTTP clients, Outbox)      │
│       │                                       ▲                 │
└───────┼───────────────────────────────────────┼─────────────────┘
        │                                       │
┌───────▼───────────────────────────────────────┼─────────────────┐
│                          Ports                                   │
│                                                                  │
│  Inbound ports                      Outbound ports              │
│  (use case interfaces)              (repository, publisher       │
│                                      interfaces)                │
│       │                                       ▲                 │
└───────┼───────────────────────────────────────┼─────────────────┘
        │                                       │
┌───────▼───────────────────────────────────────┼─────────────────┐
│                      Application layer                           │
│                   (Use case implementations)                     │
│                                                                  │
│       Use cases call outbound ports; never call adapters.        │
└──────────────────────────┬───────────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                         Domain                                   │
│        Entities · Value objects · Aggregates · Events            │
│                                                                  │
│        Zero dependencies on Spring, JPA, Kafka, or HTTP.        │
└──────────────────────────────────────────────────────────────────┘
```

## Invariants

- Domain classes have **zero infrastructure imports**. No Spring, JPA, Kafka, HTTP.
- Ports are interfaces. Adapters are implementations. The domain defines what it needs; adapters fulfill it.
- Use cases orchestrate. Domain objects enforce. Business rules live in entities and value objects.
- Adapters depend on ports. Adapters never directly depend on other adapters.
- Use cases are accessed only through their port interface — never instantiated directly.

---

## Package layout per bounded context

```
core/
└── <bounded_context>/
    ├── domain/         # Entities, value objects, domain events, domain exceptions
    ├── port/           # Inbound and outbound port interfaces
    └── usecase/        # Use case implementations
        └── orchestrator/  # Higher-order use cases that compose others (optional)

adapters/
├── <external_system_a>/
│   ├── config/         # Kafka consumer/producer configuration
│   ├── <feature>/
│   │   ├── adapter/    # Port implementations
│   │   ├── entity/     # Kafka DTOs, Avro-generated classes, HTTP request/response models
│   │   └── exceptions/ # Adapter-specific exceptions
│   └── outbox/         # Outbox adapter for this system
└── <external_system_b>/
    └── ...

infrastructure/
├── annotations/        # Custom stereotype meta-annotations
├── dlt/                # Dead-letter interfaces
├── exceptions/         # Base exception classes
├── json/               # Jackson serializers/deserializers for value objects
├── kafka/              # Topics registry, Kafka utilities
├── micrometer/         # Custom metrics
├── stereotype/         # @Usecase, @KafkaConsumer, @KafkaProducer etc.
└── util/               # Shared utilities
```

---

## Inbound ports

Inbound ports are use case interfaces. Name them `<Action><Entity>UseCase` or `<Action><Entity>Port`.

```java
// core/<bounded_context>/port/ItemOnboardingInboundPort.java
public interface ItemOnboardingInboundPort {
    void consume(ConsumerRecord<String, JsonNode> record, Acknowledgment acknowledgment);
}
```

The Kafka consumer adapter implements this:

```java
// adapters/<system>/onboarding/adapter/SystemItemOnboardingInbound.java
@KafkaConsumer
class SystemItemOnboardingInbound implements ItemOnboardingInboundPort {
    // ...
}
```

---

## Use cases

Use cases are the heart of the application. They:
- Are annotated with `@Usecase` (a custom stereotype that implies `@Transactional` + `@Component`)
- Expose a single `execute(Command)` method
- Orchestrate calls to outbound ports
- Never call other use cases directly
- Never call adapters directly

```java
// core/item/usecase/UpsertItem.java
@Usecase
class UpsertItem implements UpsertItemUseCase {

    private final ItemRepositoryPort itemRepository;
    private final ItemOnboardingOutboundPort outboundPort;

    @Override
    public void execute(UpsertItemCommand command) {
        Item item = itemRepository.getByItemNr(command.itemNr())
            .orElse(Item.newItem(command.itemNr()));
        item.applyUpdate(command);
        itemRepository.upsert(item);
        outboundPort.publishEvent(EventType.ITEM_UPSERTED, item);
    }
}
```

Orchestrator use cases compose other use cases:

```java
// core/item/usecase/orchestrator/DetermineEventType.java
@Usecase
class DetermineEventType implements DetermineEventTypeUseCase {
    // decides whether to upsert, delete, or skip based on current DB state
}
```

---

## Outbound ports

Outbound ports are what the domain calls. They define what is needed without knowing how it is provided.

```java
// core/item/port/ItemRepositoryPort.java
public interface ItemRepositoryPort {
    void upsert(Item item);
    Optional<Item> getByItemNr(ItemNr itemNr);
    List<Item> getAll();
    boolean doesNotExist(ItemNr itemNr);
    void deleteByItemNr(ItemNr itemNr);
}

// core/item/port/ItemOnboardingOutboundPort.java
public interface ItemOnboardingOutboundPort {
    void publishEvent(EventType eventType, Object payload);
}
```

---

## Domain model

### Value objects

All domain identifiers and wrapped concepts are value objects. Use **Java records** with validation in the compact constructor.

```java
// core/item/domain/ItemNr.java
public record ItemNr(String value) {
    public ItemNr {
        Objects.requireNonNull(value, "ItemNr must not be null");
        if (value.length() != 10 || !value.matches("\\d+")) {
            throw new InvalidItemNrException(value);
        }
    }

    public static ItemNr of(String value) {
        return new ItemNr(value);
    }
}
```

Rules:
- Validation runs in the compact constructor — no invalid value objects can be constructed.
- Static factory method `of(raw)` for ergonomics.
- Raw accessor via generated `value()` — never expose primitives beyond the domain boundary.
- No `null` inside domain objects. Use `Optional` or `@Nullable` (JSpecify) where absence is valid.

### Entities and aggregates

```java
// core/item/domain/Item.java
public class Item extends ItemStructure {

    private final List<ReplenishmentLocation> replenishmentLocations;

    public Item(ItemNr itemNr, List<ReplenishmentLocation> replenishmentLocations) {
        super(itemNr);
        this.replenishmentLocations = List.copyOf(replenishmentLocations); // defensive copy
    }

    // Business rule: vending machine IDs must be unique within an item
    public void addReplenishmentLocation(ReplenishmentLocation location) {
        if (replenishmentLocations.stream()
                .anyMatch(l -> l.vendingMachineId().equals(location.vendingMachineId()))) {
            throw new DuplicateVendingMachineException(location.vendingMachineId());
        }
        // ...
    }
}
```

### Domain events

Domain events are records. They carry the data needed by listeners; no behavior.

```java
// core/item/domain/ItemOnboardingEvent.java
public record ItemOnboardingEvent(ItemStructure item, EventType eventType) {}
```

### SecureString

Wrap any secret or credential value in a `SecureString` type whose `toString()` returns `"<REDACTED>"`:

```java
public record SecureString(char[] value) {
    @Override
    public String toString() { return "<REDACTED>"; }
}
```

---

## Notable architectural patterns

### Kafka bridge layer (dual-cluster relay)

When integrating two Kafka clusters with different message key structures, introduce a bridge adapter that reads raw events from the external cluster, extracts a meaningful domain key, and re-publishes to internal bridge topics. This restores partition-based ordering for downstream consumers.

```
External Kafka cluster
  └── raw-topic (key: messageId)
         │
         ▼
    Bridge adapter (re-keys by domain ID, e.g. itemNr)
         │
         ▼
Internal bridge topics (key: itemNr)
         │
         ▼
Domain consumer adapter
```

The bridge is a separate Kafka listener container with its own transaction manager.

### Type-safe event dispatcher

Instead of a large `switch` in one producer class, define a `SubclassProducer<T>` interface, let Spring inject all implementations, and build an `EnumMap` keyed by event type at startup:

```java
@Component
class KafkaProducerDispatcher {
    private final EnumMap<EventType, SubclassProducer<?>> producers;

    KafkaProducerDispatcher(List<SubclassProducer<?>> producers) {
        this.producers = new EnumMap<>(EventType.class);
        producers.forEach(p -> this.producers.put(p.eventType(), p));
    }

    void dispatch(OutboxEvent event) {
        producers.get(event.eventType()).publish(event);
    }
}
```

### Chain of Responsibility for event dispatching

When one Kafka consumer must handle multiple event types, inject a `List<EventHandler>` (Spring wires all beans implementing the interface) and iterate:

```java
@KafkaConsumer
class SystemInbound implements InboundPort {
    private final List<EventHandler> handlers;

    public void consume(ConsumerRecord<?, ?> record, Acknowledgment ack) {
        handlers.stream()
            .filter(h -> h.canHandle(record))
            .findFirst()
            .orElseThrow(UnknownEventTypeException::new)
            .handle(record);
        ack.acknowledge();
    }
}
```

### Transactional Outbox (mandatory for Kafka + DB atomicity)

Never call a Kafka producer directly from a use case. Write events to an outbox table in the same transaction as the DB write. A background poller (or an outbox library) publishes to Kafka and marks records as published.

```
Use case
  │
  ├─ writes domain state → DB (Oracle)          ┐
  └─ writes outbox event → outbox table          ┤ same transaction
                                                 ┘
Outbox poller (separate thread)
  ├─ reads unpublished events from outbox table
  ├─ publishes to Kafka
  └─ marks events as published
```

This guarantees exactly-once semantics without distributed transactions.

### Outbound port decoupled from Kafka producer

The use case calls an `OutboundPort`, which is implemented by an `OutboxAdapter` (writes to DB outbox), not the Kafka producer. The Kafka producer reads from the outbox independently. This means the domain is never aware Kafka exists.

### Jackson serialization stays outside the domain

Each value object has a corresponding `@JacksonComponent` serializer/deserializer in `infrastructure/json/`. This keeps all Jackson annotations and dependencies out of the domain layer.
