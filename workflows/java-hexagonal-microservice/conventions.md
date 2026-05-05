# Naming Conventions

## Class naming by layer

| Layer | Pattern | Examples |
|-------|---------|---------|
| Use case interface | `<Action><Entity>UseCase` | `UpsertItemUseCase`, `GetPackageQuantityUseCase` |
| Use case implementation | `<Action><Entity>` | `UpsertItem`, `GetPackageQuantity` |
| Orchestrator use case | descriptive noun phrase | `DetermineTypeOfItemStructureUpsertedEvent` |
| Command (use case input) | `<Action><Entity>Command` | `UpsertItemCommand`, `ProcessStockMovementCommand` |
| Result (use case output) | `<Action><Entity>Result` | `UpsertItemResult` |
| Inbound port | `<Feature>InboundPort` | `ItemOnboardingInboundPort` |
| Outbound port | `<Feature>OutboundPort` | `ItemOnboardingOutboundPort`, `ItemRepositoryPort` |
| Inbound adapter (Kafka) | `<System><Feature>Inbound` | `MaximoItemOnboardingInbound`, `S4mStockMovementKafkaConsumer` |
| Outbound adapter (Kafka) | `<System><Feature>KafkaProducer` | `S4mOnboardingKafkaProducer`, `MaximoStockMovementKafkaProducer` |
| Outbox adapter | `<System><Feature>OutboxAdapter` | `S4mOnboardingOutboxAdapter` |
| JPA entity | `<DomainClass>Entity` | `ItemEntity`, `ItemStructureEntity` |
| JPA Spring Data repo | `SpringData<Entity>Repository` | `SpringDataItemRepository` |
| JPA port impl | `<Entity>JpaRepository` | `ItemJpaRepository` |
| Kafka DTO | `<DomainConcept>KafkaEntity` / `<DomainConcept>KafkaEvent` | `ItemKafkaEntity`, `ImageUpsertedKafkaEvent` |
| Outbox event | `<System>Outbox<Feature>Event` | `S4mOnboardingOutboxEvent` |
| Factory | `<Output>Factory` | `CatalogUpsertedFactory` |
| Exception (domain) | `<Concept>Exception` | `InvalidItemNrException`, `ItemNotFoundException` |
| Exception (adapter) | `<System><Feature>Exception` | `MaximoBridgePublishException`, `ItemKafkaConsumerException` |
| Dead Letter adapter | `DeadLetterTableAdapter` | — |
| Config class | `<System><Concern>Config` | `MaximoConsumerConfig`, `S4mSchemaRegistryConfig` |
| Metrics bean | `<Concept>Metrics` | `DltMetrics`, `SslBundleCertificateMetrics` |

## Method naming

| Context | Pattern | Examples |
|---------|---------|---------|
| Use case entry point | `execute(Command)` | `execute(UpsertItemCommand command)` |
| Inbound port (Kafka) | `consume(record, ack)` | `consume(ConsumerRecord<?, ?>, Acknowledgment)` |
| Outbound port (events) | `publishEvent(type, payload)` | — |
| Repository port (write) | `upsert(entity)` | — |
| Repository port (read) | `getBy<Key>`, `getAll`, `findBy<Key>` | `getByItemNr`, `getAll` |
| Repository port (check) | `doesNotExist(<id>)` | — |
| Repository port (delete) | `deleteBy<Key>` | `deleteByItemNr` |
| Value object factory | `of(raw)` | `ItemNr.of("0000000001")` |
| Event handler routing | `canHandle(record)` | — |

## Package naming

- Use lowercase. If the artifact name forces underscores (hyphenated artifact IDs become underscored package roots), keep that convention throughout the package tree.
- Sub-package segments: lowercase nouns, no abbreviations.
  - `kafka_bridge` not `kafkabridge`, `rule_engine` not `ruleengine`
- Bounded context names become package segments: `core.item`, `core.stockmovement`, `core.rule_engine`.

## Test naming

| Test type | Pattern | Examples |
|-----------|---------|---------|
| Unit test | `<ClassUnderTest>Test` | `ItemNrTest`, `UpsertItemTest` |
| Integration test | `<Feature>IntegrationTest` | `ItemOnboardingIntegrationTest` |
| Object Mother | `<DomainClass>Mother` | `ItemMother`, `ItemNrMother`, `StockMovementMother` |
| Test Kafka producer | `<System><Feature>TestProducer` | `MaximoItemTestProducer` |
| Test Kafka consumer | `<System><Feature>TestConsumer` | `KafkaS4mTestConsumer` |
| Data contract samples | `DataContractSamplesTest` | — |

---

## Custom stereotype annotations

Define meta-annotations in `infrastructure/stereotype/` to encode architectural roles. Stereotypes serve two purposes: they act as Spring `@Component` aliases and they make the architectural role visible in the code.

```java
// @Usecase — automatically transactional; marks an application service
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Component
@DatabaseTransactional   // your own @Transactional alias with the right transaction manager
public @interface Usecase {
    boolean readOnly() default false;
}

// @KafkaConsumer — marks an inbound adapter
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Component
public @interface KafkaConsumer {}

// @KafkaConsumerHandler — marks one handler in a Chain of Responsibility
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Component
public @interface KafkaConsumerHandler {}

// @S4mKafkaProducer / @MaximoKafkaProducer — binds to a specific transaction manager
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Component
@Transactional(transactionManager = "s4mKafkaTransactionManager")
public @interface S4mKafkaProducer {}

// @DatabaseTransactional — alias for @Transactional bound to the DB transaction manager
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Transactional(transactionManager = "transactionManager")
public @interface DatabaseTransactional {}
```

**Rule:** `@Transactional` with a specific `transactionManager` should only appear on custom stereotype annotations or use case implementations — never on adapters or infrastructure classes.

---

## Null safety

Use [JSpecify](https://jspecify.dev/) annotations enforced by [NullAway](https://github.com/uber/NullAway) in `ERROR` mode.

```java
// Mark nullable return values explicitly
public @Nullable Size size() { return size; }

// Mark nullable parameters explicitly
public void setSize(@Nullable Size size) { this.size = size; }

// Everything else is implicitly non-null — NullAway enforces this at compile time
public ItemNr itemNr() { return itemNr; }  // never null
```

NullAway configuration in `pom.xml`:
```xml
<compilerArgs>
    <arg>-Xplugin:ErrorProne
        -Xep:NullAway:ERROR
        -XepOpt:NullAway:AnnotatedPackages=com.yourorg
        -XepOpt:NullAway:ExcludedFieldAnnotations=org.springframework.beans.factory.annotation.Value
    </arg>
</compilerArgs>
```

---

## Code formatting

Enforce [Google Java Format](https://github.com/google/google-java-format) at the `validate` Maven phase — build fails on unformatted code:

```xml
<plugin>
    <groupId>com.spotify.fmt</groupId>
    <artifactId>fmt-maven-plugin</artifactId>
    <version>2.29</version>
    <executions>
        <execution>
            <goals><goal>check</goal></goals>
        </execution>
    </executions>
</plugin>
```

Developers format on save: IntelliJ plugin `google-java-format` or `mvn fmt:format` before committing.

---

## Commit style

```
<type>(<scope>): <short description>

feat(item): add image upsert use case
fix(maximo): handle null image mime type in bridge
docs(adr): add ADR-015 for outbox pattern decision
test(stock-movement): add integration test for transfer movement type
refactor(item): extract ReplenishmentLocation to value object
```
