# Agents — Java Hexagonal Microservice

Project-specific agent templates. Copy to your project's `.claude/agents/`, then fill in every `{{placeholder}}` before use.

## Placeholders

| Placeholder | Example | Description |
|-------------|---------|-------------|
| `{{root_package}}` | `com.volvocars.order_service` | Root Java package of the service |
| `{{bounded_contexts}}` | `order, payment, shipment` | Comma-separated list of bounded contexts |
| `{{external_systems}}` | `sap, kafka-bridge` | Comma-separated list of external systems with adapters |
| `{{formatter_command}}` | `mvn fmt:format` | Command that formats the code (run after each file) |
| `{{builder_library}}` | `bob-annotations` / `Lombok` | Builder library used in the project |
| `{{doc_path}}` | `docs/asciidoc` | Root path for project documentation |
| `{{domain_doc_file}}` | `docs/asciidoc/_sections/domain_model.adoc` | Domain model documentation file |
| `{{event_doc_file}}` | `docs/asciidoc/_sections/event_flows.adoc` | Event flow documentation file |
| `{{diagrams_path}}` | `docs/asciidoc/diagrams` | Directory containing Mermaid diagram files |
| `{{model_fast}}` | `claude-haiku-4-5-20251001` | Model for read-only agents (search, planning, analysis) |
| `{{model_capable}}` | `claude-sonnet-4-6` | Model for code/doc-writing agents |

## Installation

```bash
# 1. Copy agents to your project
cp workflows/java-hexagonal-microservice/agents/*.md /your-project/.claude/agents/

# 2. Fill in all placeholders (search-and-replace in your editor)
#    Every {{placeholder}} must be replaced before the agents are used.

# 3. Verify — no placeholder should remain
grep -r "{{" /your-project/.claude/agents/
```

## Agents

| Agent | Role | Writes files? | Model tier |
|-------|------|---------------|------------|
| [`planner`](planner.md) | Proposes implementation plan — read-only | No | `{{model_fast}}` |
| [`domain-analyst`](domain-analyst.md) | Checks domain model impact, proposes diagram changes — read-only | No | `{{model_fast}}` |
| [`code-explorer`](code-explorer.md) | Searches and locates existing code, patterns, and conventions — read-only | No | `{{model_fast}}` |
| [`story-writer`](story-writer.md) | Generates structured GitHub issues | No | `{{model_fast}}` |
| [`developer`](developer.md) | Implements production code following hexagonal architecture | Yes | `{{model_capable}}` |
| [`test-writer`](test-writer.md) | Writes tests following the project test strategy | Yes | `{{model_capable}}` |
| [`doc-writer`](doc-writer.md) | Updates README and project documentation | Yes | `{{model_capable}}` |

These agents work together as part of the `/microservice`, `/implement`, `/user-story`, and `/document` skill flows.
