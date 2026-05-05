# Project Structure

## Maven setup

### Single-module POM skeleton

```xml
<project>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.x.x</version>  <!-- or 4.x -->
    </parent>

    <groupId>com.yourorg</groupId>
    <artifactId>your-service</artifactId>
    <version>1.0.0-SNAPSHOT</version>

    <properties>
        <java.version>21</java.version>  <!-- or 25 for cutting edge -->
    </properties>

    <dependencies>
        <!-- Core -->
        <dependency>spring-boot-starter-web</dependency>
        <dependency>spring-boot-starter-data-jpa</dependency>

        <!-- Messaging -->
        <dependency>spring-boot-starter-kafka</dependency>
        <dependency>kafka-avro-serializer</dependency>
        <dependency>avro</dependency>

        <!-- Database (adjust for your DB) -->
        <dependency>spring-boot-starter-flyway</dependency>
        <dependency>postgresql / ojdbc11</dependency>

        <!-- Null safety -->
        <dependency>jspecify</dependency>

        <!-- Builder generation (optional) -->
        <dependency>bob-annotations</dependency>  <!-- or Lombok -->

        <!-- Testing -->
        <dependency>spring-boot-starter-test</dependency>
        <dependency>spring-kafka-test</dependency>
        <dependency>testcontainers-postgresql / testcontainers-oracle-free</dependency>
        <dependency>testcontainers-kafka</dependency>
        <dependency>spring-boot-testcontainers</dependency>
        <dependency>archunit</dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Code formatting — fails build on violations -->
            <plugin>com.spotify.fmt:fmt-maven-plugin</plugin>

            <!-- Null safety + static analysis at compile time -->
            <plugin>maven-compiler-plugin with Error Prone + NullAway</plugin>

            <!-- Avro IDL compilation -->
            <plugin>org.apache.avro:avro-maven-plugin</plugin>

            <!-- Living documentation -->
            <plugin>org.asciidoctor:asciidoctor-maven-plugin</plugin>

            <!-- Code coverage -->
            <plugin>jacoco-maven-plugin (under coverage profile)</plugin>

            <!-- Git metadata in actuator /info -->
            <plugin>git-commit-id-maven-plugin</plugin>
        </plugins>
    </build>

    <profiles>
        <profile>
            <id>coverage</id>
            <!-- activates JaCoCo -->
        </profile>
    </profiles>
</project>
```

---

## Main source layout

```
src/
├── main/
│   ├── java/com/yourorg/<service>/
│   │   │
│   │   ├── core/                               # Hexagonal core (domain + ports + use cases)
│   │   │   ├── <bounded_context_a>/
│   │   │   │   ├── domain/                     # Entities, VOs, domain events, domain exceptions
│   │   │   │   │   ├── <Entity>.java
│   │   │   │   │   ├── <ValueObject>.java      # Java record
│   │   │   │   │   ├── <DomainEvent>.java      # Java record
│   │   │   │   │   └── <DomainException>.java
│   │   │   │   ├── port/                       # Port interfaces
│   │   │   │   │   ├── <Feature>InboundPort.java
│   │   │   │   │   └── <Feature>OutboundPort.java
│   │   │   │   └── usecase/                    # Use case implementations
│   │   │   │       ├── <Action><Entity>.java   # e.g. UpsertItem.java
│   │   │   │       └── orchestrator/
│   │   │   │           └── <Orchestrator>.java
│   │   │   └── <bounded_context_b>/
│   │   │       └── ...
│   │   │
│   │   ├── adapters/                           # All port implementations
│   │   │   ├── <external_system_a>/            # e.g. maximo/, s4m/, sap/
│   │   │   │   ├── config/                     # Kafka / HTTP client config beans
│   │   │   │   ├── <feature>/
│   │   │   │   │   ├── adapter/                # Implements inbound or outbound port
│   │   │   │   │   ├── entity/                 # Kafka DTOs, Avro records, HTTP models
│   │   │   │   │   └── exceptions/
│   │   │   │   └── outbox/                     # Outbox adapter for this system
│   │   │   └── database/
│   │   │       ├── adapter/                    # JPA repository port implementations
│   │   │       ├── config/
│   │   │       ├── dlt/                        # Dead Letter Table adapter + entity
│   │   │       └── entity/                     # JPA entity classes
│   │   │
│   │   └── infrastructure/                     # Cross-cutting technical concerns
│   │       ├── annotations/                    # Custom stereotype annotations
│   │       ├── dlt/                            # Dead-letter interfaces
│   │       ├── exceptions/                     # Base exception classes
│   │       ├── json/                           # Jackson serializers/deserializers for VOs
│   │       ├── kafka/                          # Topics registry, utilities
│   │       ├── micrometer/                     # Custom metrics
│   │       ├── secure/                         # SecureString
│   │       ├── stereotype/                     # @Usecase, @KafkaConsumer, etc.
│   │       ├── util/                           # Shared utilities
│   │       └── web/docs/                       # DocumentationController (optional)
│   │
│   ├── avro/                                   # Avro IDL (.avdl) and schema (.avsc) files
│   │   └── <entity>.avdl
│   │
│   └── resources/
│       ├── application.yml                     # Base config (no secrets)
│       ├── application-cluster.yml             # Production config (secrets via env vars)
│       ├── application-local.yml               # Local dev overrides
│       ├── application-local.yml.example       # Committed safe template for local config
│       ├── db/migration/                       # Flyway SQL migrations
│       │   └── V1__init.sql
│       └── static/docs/                        # Built AsciiDoc output (generated at build time)
│
├── docs/asciidoc/                              # Living documentation source
│   ├── <ServiceName>.adoc                      # Main document (includes all sections)
│   ├── _sections/                              # Modular doc sections
│   │   ├── overview.adoc
│   │   ├── architecture.adoc
│   │   ├── domain_model.adoc
│   │   ├── event_flows.adoc
│   │   └── ...
│   ├── _adr/                                   # Architecture Decision Records
│   │   ├── ADR-001-<title>.adoc
│   │   └── ...
│   ├── diagrams/                               # Mermaid diagram files
│   │   └── <diagram>.mermaid
│   └── snippets/                               # JSON/YAML payload examples embedded in docs
│
└── test/
    └── (see testing.md)
```

---

## application.yml structure

```yaml
spring:
  datasource:
    url: ${DATASOURCE_URL:jdbc:postgresql://localhost:5432/mydb}
    username: ${DATASOURCE_USER:myuser}
    password: ${DATASOURCE_PASSWORD:mypassword}
  jpa:
    open-in-view: false               # always disable
    hibernate:
      ddl-auto: validate
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP:localhost:9092}
  flyway:
    locations: classpath:db/migration

management:
  server:
    port: 8889
  endpoints:
    web:
      exposure:
        include: health,info,loggers,metrics

# Per external-system Kafka config block (repeat for each system)
<system>:
  kafka:
    properties:
      consumer:
        bootstrap-servers: ${<SYSTEM>_KAFKA_BOOTSTRAP}
        group-id: ${<SYSTEM>_KAFKA_GROUP_ID}
      producer:
        bootstrap-servers: ${<SYSTEM>_KAFKA_BOOTSTRAP}
    topics:
      <feature>: ${<SYSTEM>_TOPIC_<FEATURE>}
```

---

## Kubernetes deployment structure (Kustomize)

```
kustomize/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── qa/
    │   ├── kustomization.yaml
    │   └── externalsecret.yaml   # HashiCorp Vault or AWS Secrets Manager
    └── prod/
        ├── kustomization.yaml
        └── externalsecret.yaml
```

---

## Root files

```
<service-root>/
├── compose.yml                 # Local dev Docker Compose (DB + Kafka + Schema Registry + UI)
├── .sdkmanrc                   # Pin Java version (e.g. java=21.0.5-tem)
├── mvnw / mvnw.cmd             # Maven wrapper
├── pom.xml
├── README.md
├── CLAUDE.md                   # Claude Code context (see hexagonal-microservice workflow)
├── CLAUDE.project.md           # Project-specific overrides
└── whiteboard.excalidraw       # Optional: architecture whiteboard (Excalidraw)
```
