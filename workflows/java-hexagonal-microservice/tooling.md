# Tooling

## Maven plugins

### Google Java Format — formatting enforced at build time

```xml
<plugin>
    <groupId>com.spotify.fmt</groupId>
    <artifactId>fmt-maven-plugin</artifactId>
    <version>2.29</version>
    <executions>
        <execution>
            <phase>validate</phase>
            <goals><goal>check</goal></goals>
        </execution>
    </executions>
</plugin>
```

- Run `mvn fmt:format` to format in place.
- The `check` goal fails the build on violations — no manual enforcement needed.
- IntelliJ plugin: `google-java-format`.

### Error Prone + NullAway — static analysis at compile time

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.14.1</version>
    <configuration>
        <annotationProcessorPaths>
            <path>
                <groupId>com.uber.nullaway</groupId>
                <artifactId>nullaway</artifactId>
                <version>0.13.1</version>
            </path>
            <path>
                <groupId>com.google.errorprone</groupId>
                <artifactId>error_prone_core</artifactId>
                <version>2.47.0</version>
            </path>
        </annotationProcessorPaths>
        <compilerArgs>
            <arg>-Xplugin:ErrorProne
                -Xep:NullAway:ERROR
                -XepOpt:NullAway:AnnotatedPackages=com.yourorg
                -XepOpt:NullAway:ExcludedFieldAnnotations=org.springframework.beans.factory.annotation.Value
            </arg>
        </compilerArgs>
    </configuration>
</plugin>
```

### Avro IDL compilation

```xml
<plugin>
    <groupId>org.apache.avro</groupId>
    <artifactId>avro-maven-plugin</artifactId>
    <version>1.12.0</version>
    <executions>
        <execution>
            <phase>generate-sources</phase>
            <goals><goal>idl-protocol</goal></goals>
            <configuration>
                <sourceDirectory>${project.basedir}/src/main/avro</sourceDirectory>
                <outputDirectory>${project.build.directory}/generated-sources/avro</outputDirectory>
            </configuration>
        </execution>
    </executions>
</plugin>
```

Place `.avdl` (Avro IDL) files in `src/main/avro/`. Generated classes land in `target/generated-sources/avro/`. Exclude generated sources from NullAway.

### Living documentation (AsciiDoc)

```xml
<plugin>
    <groupId>org.asciidoctor</groupId>
    <artifactId>asciidoctor-maven-plugin</artifactId>
    <version>3.2.0</version>
    <executions>
        <execution>
            <id>output-html</id>
            <phase>generate-resources</phase>
            <goals><goal>process-asciidoc</goal></goals>
            <configuration>
                <backend>html5</backend>
                <outputDirectory>${project.build.directory}/generated-docs/html</outputDirectory>
            </configuration>
        </execution>
        <execution>
            <id>output-pdf</id>
            <phase>generate-resources</phase>
            <goals><goal>process-asciidoc</goal></goals>
            <configuration>
                <backend>pdf</backend>
                <outputDirectory>${project.build.directory}/generated-docs/pdf</outputDirectory>
            </configuration>
        </execution>
    </executions>
</plugin>

<!-- Copy generated docs into the JAR static resources so they're served at runtime -->
<plugin>
    <artifactId>maven-resources-plugin</artifactId>
    <executions>
        <execution>
            <id>copy-docs</id>
            <phase>prepare-package</phase>
            <goals><goal>copy-resources</goal></goals>
            <configuration>
                <outputDirectory>${project.build.outputDirectory}/static/docs</outputDirectory>
                <resources>
                    <resource>
                        <directory>${project.build.directory}/generated-docs/html</directory>
                    </resource>
                </resources>
            </configuration>
        </execution>
    </executions>
</plugin>
```

Serve the docs at runtime with a minimal controller:

```java
@Controller
class DocumentationController {
    @GetMapping("/docs")
    public String docs() { return "forward:/docs/index.html"; }
}
```

Documentation is versioned alongside code and always matches the deployed artifact.

### JaCoCo (under `coverage` Maven profile)

```xml
<profile>
    <id>coverage</id>
    <build>
        <plugins>
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>0.8.14</version>
                <executions>
                    <execution><goals><goal>prepare-agent</goal></goals></execution>
                    <execution>
                        <id>report</id>
                        <phase>verify</phase>
                        <goals><goal>report</goal></goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</profile>
```

Run with: `mvn verify -Pcoverage`

### Git commit ID in actuator `/info`

```xml
<plugin>
    <groupId>io.github.git-commit-id</groupId>
    <artifactId>git-commit-id-maven-plugin</artifactId>
    <executions>
        <execution>
            <goals><goal>revision</goal></goals>
        </execution>
    </executions>
</plugin>
```

---

## Docker Compose — local development stack

```yaml
# compose.yml
services:
  db:
    image: postgres:17-alpine         # or gvenzl/oracle-free:23-slim-faststart for Oracle
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    ports: ["5432:5432"]

  kafka:
    image: confluentinc/cp-kafka:7.x  # KRaft mode — no ZooKeeper
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      CLUSTER_ID: "<random-base64>"
    ports: ["9092:9092"]

  schema-registry:
    image: apicurio/apicurio-registry:3.x   # or confluentinc/cp-schema-registry
    environment:
      REGISTRY_AUTH_ANONYMOUS_READ_ACCESS_ENABLED: "true"
    ports: ["8081:8080"]
    depends_on: [kafka]

  kafka-ui:
    image: docker.redpanda.com/redpandadata/console:latest
    environment:
      CONFIG_FILEPATH: /tmp/config.yml
    volumes:
      - ./kafka-ui-config.yml:/tmp/config.yml
    ports: ["8083:8080"]
    depends_on: [kafka, schema-registry]

  observability:
    image: grafana/otel-lgtm   # Grafana + Loki + Tempo + Mimir in one container
    ports: ["3000:3000", "4317:4317", "4318:4318"]
```

---

## GitHub Actions pipeline

Structure workflows as a main trigger + reusable sub-workflows:

```
.github/workflows/
├── ci-test.yml                              # Push → test
├── ci-release.yml                           # workflow_dispatch → version bump + build + release
├── ci-release-snapshot.yml                  # workflow_dispatch → snapshot release
├── cd-deploy.yml                            # workflow_dispatch / tag → deploy
├── _subworkflow_test.yml                    # Reusable: Maven test
├── _subworkflow_release.yml                 # Reusable: Paketo buildpack + container push
└── _subworkflow_deploy.yml                  # Reusable: kubectl apply -k kustomize/overlays/...
```

### Container build (Paketo buildpacks — no Dockerfile needed)

```yaml
# In the release sub-workflow
- name: Build and push image
  run: |
    mvn spring-boot:build-image \
      -Dspring-boot.build-image.imageName=<registry>/<image>:<version> \
      -Dspring-boot.build-image.publish=true
```

Paketo buildpacks produce a minimal, hardened image without a Dockerfile. The Spring Boot Maven plugin handles everything.

---

## SDK version pinning

Pin the Java version for all developers with SDKman:

```bash
# .sdkmanrc
java=21.0.5-tem
```

When a developer `cd`s into the project, SDKman auto-switches to the pinned JDK.

---

## ADR (Architecture Decision Records)

Store ADRs in `src/docs/asciidoc/_adr/`. Each ADR is an AsciiDoc file:

```
ADR-NNN-<kebab-case-title>.adoc
```

Template:
```asciidoc
= ADR-NNN: <Title>
:date: YYYY-MM-DD
:status: Accepted | Superseded by ADR-XXX | Deprecated

== Context

Why was this decision needed?

== Decision

What was decided?

== Consequences

What does this mean going forward? What becomes easier? What becomes harder?
```

ADRs are included in the main documentation and served at runtime alongside the rest of the living docs.
