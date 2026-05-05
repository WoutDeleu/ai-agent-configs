# Testing Strategy

## Test directory layout

```
src/test/java/com/yourorg/<service>/
├── core/
│   ├── <bounded_context_a>/
│   │   ├── domain/               # Entity and value object unit tests + Mother objects
│   │   └── usecase/              # Use case tests (pure unit, no Spring)
│   └── <bounded_context_b>/
│       └── ...
├── adapters/
│   ├── database/
│   │   ├── adapter/              # JPA repository integration tests
│   │   ├── config/               # InMemoryRepository, cleanup extensions
│   │   ├── dlt/                  # Dead letter adapter tests + Mother objects
│   │   └── entity/               # JPA entity mapping tests
│   └── <external_system>/
│       ├── <feature>/
│       │   ├── adapter/          # Kafka consumer slice tests
│       │   └── entity/           # DTO deserialization tests + Mother objects
│       └── outbox/               # Outbox adapter tests
├── infrastructure/
│   ├── annotations/              # Custom test meta-annotations
│   ├── config/                   # TestClassOrderer, shared test config
│   ├── kafka/                    # KafkaAdminTestClient, KafkaSetupAndCleanupExtension
│   ├── outbox/                   # OutboxGateway JUnit 5 extensions
│   ├── testcontainers/           # Shared container configs (Oracle/PG + Kafka)
│   └── util/                     # KafkaTestUtils, test helpers
└── integration/                  # Full end-to-end tests
    ├── <Feature>IntegrationTest.java
    └── ...
```

---

## Test categories and custom slice annotations

Define custom meta-annotations in `infrastructure/annotations/` (test source only). This keeps test setup DRY and makes the intent of each test class obvious.

### `@UsecaseTest`

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@ExtendWith(CleanUpInMemoryRepositories.class)
public @interface UsecaseTest {}
```

- No Spring context.
- Uses `InMemoryRepository` implementations instead of JPA.
- Fastest tests in the suite.

### `@DataJpaTest`

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import(DatabaseConfig.class)
@ServiceConnection  // Spring Boot 3+ Testcontainers auto-wiring
public @interface DataJpaTest {}
```

- Starts only the JPA slice.
- Uses Testcontainers (PostgreSQL or Oracle) — no H2.
- Does NOT start Kafka or the full application context.

### `@KafkaConsumerTest` (one per external system)

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@SpringJUnitConfig(classes = {MaximoConsumerConfig.class, MaximoConsumerErrorHandlerConfig.class})
@EmbeddedKafka(...)   // or Testcontainers Kafka
@ActiveProfiles("<system>-kafka-test")
public @interface MaximoKafkaTest {}
```

- Starts only the Kafka consumer beans + their config.
- Use cases are mocked with Mockito.
- Does NOT start JPA or the full application context.

### `@IntegrationTest`

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("integration-test")
@ExtendWith({
    CleanUpDatabaseExtension.class,
    MaximoTransactionalOutboxGatewayExtension.class,
    S4mTransactionalOutboxGatewayExtension.class
})
public @interface IntegrationTest {}
```

- Full application context.
- Testcontainers for all infrastructure (DB + Kafka).
- JUnit 5 extensions handle DB cleanup and outbox flushing.

---

## Object Mother pattern

Create a Mother class for every domain object and every Kafka DTO. Mothers produce **valid, fully-populated instances with random values by default**. Tests override only the fields relevant to the scenario.

### Why random values?

Hardcoding `"0000000001"` everywhere means your tests only ever exercise that one value. Random defaults:
- Surface bugs that only appear for certain inputs (edge lengths, character sets, boundary values).
- Prevent tests from accidentally passing because they share the same hardcoded constant.
- Make it obvious when a test is asserting on a specific value vs. just needing *any* valid value.

If a test fails on a random value, log the seed or the generated value so it can be reproduced.

### Random value utilities

```java
// infrastructure/util/RandomTestValues.java (test source)
public final class RandomTestValues {
    private static final ThreadLocalRandom RNG = ThreadLocalRandom.current();

    public static String digits(int length) {
        return RNG.ints(length, 0, 10)
            .mapToObj(Integer::toString)
            .collect(Collectors.joining());
    }

    public static int positiveInt(int max) { return RNG.nextInt(1, max + 1); }
    public static int positiveInt() { return positiveInt(1000); }

    public static BigDecimal positiveBigDecimal() {
        return BigDecimal.valueOf(RNG.nextDouble(0.01, 9999.99))
            .setScale(2, RoundingMode.HALF_UP);
    }

    public static String uuid() { return UUID.randomUUID().toString(); }

    public static <T> T oneOf(T... values) {
        return values[RNG.nextInt(values.length)];
    }
}
```

### Mother examples

```java
// core/item/domain/ItemNrMother.java
public class ItemNrMother {
    // Default: random valid ItemNr — use this when the specific value doesn't matter
    public static ItemNr random() {
        return ItemNr.of(RandomTestValues.digits(10));
    }

    // Named scenarios: use these when the specific value matters to the test
    public static ItemNr known() { return ItemNr.of("0000000001"); }
}

// core/stockmovement/domain/QuantityMother.java
public class QuantityMother {
    public static Quantity random()       { return new Quantity(RandomTestValues.positiveInt()); }
    public static Quantity zero()         { return new Quantity(0); }
    public static Quantity large()        { return new Quantity(Integer.MAX_VALUE); }
    public static Quantity of(int value)  { return new Quantity(value); }
}

// core/item/domain/ItemMother.java
public class ItemMother {
    // Default: fully random, fully valid — use for tests where item content is irrelevant
    public static Item random() {
        return new Item(ItemNrMother.random(), List.of(ReplenishmentLocationMother.random()));
    }

    // Named scenarios: use when the specific shape matters
    public static Item withOneLocation() {
        return new Item(ItemNrMother.random(), List.of(ReplenishmentLocationMother.random()));
    }

    public static Item withNoLocations() {
        return new Item(ItemNrMother.random(), List.of());
    }

    public static Item withLocations(int count) {
        var locations = IntStream.range(0, count)
            .mapToObj(_ -> ReplenishmentLocationMother.random())
            .toList();
        return new Item(ItemNrMother.random(), locations);
    }
}

// adapters/maximo/onboarding/entity/ItemKafkaEntityMother.java
public class ItemKafkaEntityMother {
    public static ItemKafkaEntity random() {
        return new ItemKafkaEntity(
            RandomTestValues.digits(10),   // itemNumber
            RandomTestValues.uuid(),        // transactionId
            RandomTestValues.oneOf("ACTIVE", "PLANNING", "ABSOLUTE")
        );
    }

    public static ItemKafkaEntity withStatus(String status) {
        var base = random();
        base.setStatus(status);
        return base;
    }
}
```

### Rules

- **Default factory method is always `random()`**, not `valid()` or `default()`. If a test needs a specific value, use a named method that makes the intent explicit.
- One Mother class per domain concept.
- Named scenario methods describe the scenario, not the fields: `withNoLocations()` not `withReplenishmentLocations(List.of())`.
- Only use fixed values when the test explicitly asserts on that value — otherwise, use `random()`.
- Mothers live in the same package as the class they build, in the test source tree.

---

## In-memory repository pattern

For use case tests (`@UsecaseTest`), implement every outbound repository port with an in-memory version backed by a `HashMap`.

```java
// adapters/database/config/InMemoryItemRepository.java (test source)
public class InMemoryItemRepository implements ItemRepositoryPort {
    private final Map<ItemNr, Item> store = new HashMap<>();

    @Override
    public void upsert(Item item) { store.put(item.itemNr(), item); }

    @Override
    public Optional<Item> getByItemNr(ItemNr itemNr) {
        return Optional.ofNullable(store.get(itemNr));
    }

    @Override
    public void clear() { store.clear(); }
}
```

The `CleanUpInMemoryRepositories` JUnit 5 extension calls `clear()` on all in-memory repos before each test.

---

## JUnit 5 extensions

Encapsulate test infrastructure concerns as `@ExtendWith` extensions rather than `@BeforeEach` / `@AfterEach` boilerplate.

| Extension | Purpose |
|-----------|---------|
| `CleanUpDatabaseExtension` | `@BeforeEach`: truncates all tables via JDBC |
| `CleanUpInMemoryRepositories` | `@BeforeEach`: clears all in-memory repos |
| `KafkaSetupAndCleanupExtension` | `@BeforeEach` / `@AfterEach`: creates/deletes Kafka topics |
| `TransactionalOutboxGatewayExtension` | Programmatically triggers outbox polling between test steps |

Compose extensions in the custom meta-annotations so tests declare intent, not infrastructure.

---

## Integration tests

### Philosophy: no mocks, real infrastructure

Integration tests must mirror production as closely as possible. The goal is high confidence that a passing test means working software — not just working test doubles.

**Default rule: if real infrastructure can run in a container, use it. Do not mock it.**

| Concern | Approach |
|---------|----------|
| Database | Testcontainers — same DB engine as production (PostgreSQL, Oracle). Never H2. |
| Kafka | Testcontainers Kafka (or embedded Kafka for speed). Real broker, real topics, real partitions. |
| Schema Registry | Testcontainers or Apicurio in-memory — real schema validation. |
| Internal services (same repo/bounded context) | No mocks — let them run. |
| External HTTP services (partner systems, third-party APIs) | WireMock — acceptable exception (see below). Configure to replay realistic response shapes and latency. |
| Clock / time | Use the real system clock. Do not mock `Clock` unless the test is specifically about time-dependent behavior. |
| Transactions | Real transaction manager, real commit/rollback. Never mock `@Transactional`. |

**Acceptable exceptions — when a mock or stub is justified:**

- **External HTTP services you do not own**: use WireMock, but configure it with real response shapes captured from the actual service. Verify that the expected requests were made. Never use `any()` matchers for requests in WireMock stubs — match real fields.
- **Services that are prohibitively expensive or impossible to containerize**: document why mocking was necessary with a comment and a ticket to revisit.

**Never acceptable in integration tests:**

- Mocking the repository layer — defeats the purpose of testing persistence.
- Mocking Kafka producers or consumers — defeats the purpose of testing the messaging path.
- Using `@MockBean` for anything that has a real Testcontainer-backed implementation.
- Hardcoding sleep durations — use Awaitility.

### Structure

```java
@IntegrationTest
class ItemOnboardingIntegrationTest {

    @Autowired MaximoItemTestProducer producer;   // sends real Kafka messages to the test broker
    @Autowired KafkaS4mTestConsumer consumer;     // receives real Kafka messages from the test broker
    @Autowired SpringDataItemRepository repo;     // queries the real Testcontainers DB
    @Autowired WireMockServer wireMock;           // stubs external HTTP partner (if any)

    @Test
    void should_persist_item_and_publish_catalog_event_when_item_is_upserted() {
        var payload = ItemKafkaEntityMother.random();  // random by default

        producer.sendItemUpserted(payload);

        // Assert Kafka output — real broker, real consumer
        await().atMost(10, SECONDS).untilAsserted(() -> {
            var events = consumer.pollCatalogTopic();
            assertThat(events).hasSize(1);
            assertThat(events.get(0).getItemNr()).isEqualTo(payload.getItemNumber());
        });

        // Assert DB state — real database, no mocks
        var savedItem = repo.findByItemNr(payload.getItemNumber());
        assertThat(savedItem).isPresent();
        assertThat(savedItem.get().status()).isEqualTo(Status.of(payload.getStatus()));
    }

    @Test
    void should_write_to_dead_letter_table_when_message_is_malformed() {
        // Publish a message that will fail deserialization or validation
        producer.sendRaw(Topics.MAXIMO_ITEM_BRIDGE, "bad-key", "{not valid json}");

        // Assert the DLT entry — real DB, no mocks
        await().atMost(10, SECONDS).untilAsserted(() -> {
            var dltEntries = dltRepo.findAll();
            assertThat(dltEntries).hasSize(1);
            assertThat(dltEntries.get(0).source()).isEqualTo(MessageSource.MAXIMO);
        });

        // Assert no catalog event was published
        await().during(2, SECONDS).atMost(3, SECONDS).untilAsserted(() ->
            assertThat(consumer.pollCatalogTopic()).isEmpty()
        );
    }
}
```

### WireMock for external HTTP — do it realistically

When an external HTTP service must be stubbed:

```java
// Capture real response shapes — don't invent them
wireMock.stubFor(
    post(urlEqualTo("/inventory/reserve"))
        .withRequestBody(matchingJsonPath("$.itemNr"))      // match real fields, not any()
        .withRequestBody(matchingJsonPath("$.quantity"))
        .willReturn(aResponse()
            .withStatus(200)
            .withHeader("Content-Type", "application/json")
            .withBodyFile("wiremock/inventory-reserve-response.json")  // real shape, from actual service
            .withFixedDelay(50))   // realistic latency
);

// After the test — verify the call was actually made
wireMock.verify(postRequestedFor(urlEqualTo("/inventory/reserve"))
    .withRequestBody(matchingJsonPath("$.itemNr", equalTo(payload.getItemNumber()))));
```

Store WireMock response bodies in `src/test/resources/__files/wiremock/`. Use real response shapes captured from the actual partner service.

### What every integration test must cover

1. **Happy path** — drive a realistic payload through the full stack (inbound adapter → use case → outbound adapter). Assert DB state, produced Kafka messages, and any external HTTP calls made.
2. **Failure / error path** — malformed input, missing precondition, or downstream error. Assert that the system degrades correctly: DLT entry written, offset committed, no partial state left in the DB.
3. **Idempotency** (where applicable) — publish the same message twice. Assert the outcome is the same as publishing once.

---

## Kafka test infrastructure

```java
// Shared test Kafka producer
@Component
class MaximoItemTestProducer {
    private final KafkaTemplate<String, JsonNode> template;

    void sendItemUpserted(ItemKafkaEntity payload) {
        template.send(Topics.MAXIMO_ITEM_BRIDGE, payload.getItemNumber(), toJson(payload));
    }
}

// Shared test Kafka consumer
@Component
class KafkaS4mTestConsumer {
    private final BlockingQueue<GenericRecord> catalogRecords = new LinkedBlockingQueue<>();

    @KafkaListener(topics = "${s4m.kafka.topics.catalog}")
    void consume(ConsumerRecord<String, GenericRecord> record) {
        catalogRecords.add(record.value());
    }

    List<GenericRecord> pollCatalogTopic() {
        // drain the queue
    }
}
```

Use [Awaitility](https://github.com/awaitility/awaitility) for all async assertions — never `Thread.sleep()`.

---

## Test Kafka fixtures

Store canonical JSON payload files in `src/test/resources/kafka_samples/`:

```
kafka_samples/
├── <system>-init/              # Seed data for container startup
│   ├── item.json
│   └── user.json
└── <system>-test/              # Scenario-specific fixtures
    ├── item-upsert.json
    ├── item-delete.json
    └── item-image-upsert.json
```

Load fixtures in Mother classes:

```java
public class MaximoConsumerRecordMother {
    public static ConsumerRecord<String, JsonNode> itemUpsert() {
        var json = loadJson("kafka_samples/maximo-test/item-upsert.json");
        return new ConsumerRecord<>(Topics.MAXIMO_ITEM_BRIDGE, 0, 0L, "0000000001", json);
    }
}
```

---

## Data contract samples

For each Avro schema produced by the service, add a test that constructs a canonical record and serializes it. This test does not assert behavior — it generates payload examples for integration partners and documentation.

```java
@Test
void generate_catalog_upserted_sample() {
    var record = CatalogUpsertedFactory.create(ItemMother.withOneLocation());
    var json = avroToJson(record);
    // log or write to file — no assertion needed
}
```

---

## Maven Surefire configuration

Limit Spring context cache size to avoid OOM when running many integration tests:

```
src/test/resources/spring.properties:
spring.test.context.cache.maxSize=1
```

Wire the Mockito Java agent for open/inline mocks:

```xml
<plugin>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>
            -javaagent:${settings.localRepository}/org/mockito/mockito-core/.../mockito-core-...jar
            ${surefire-argline}
        </argLine>
    </configuration>
</plugin>
```
