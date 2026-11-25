---
last_updated: {{YYYY-MM-DD}}
status: draft
description: {{Layer map, module boundaries, dependency rules, and data flow for the project.}}
tags: [architecture, {{tag}}]
---

# Architecture

Target architecture for {{PROJECT_NAME}}. Document the intended structure, not a legacy anti-pattern. Replace each placeholder with verified facts before setting `status: active`.

## Layer map

| Layer | Responsibility | Paths |
|---|---|---|
| {{LAYER}} | {{RESPONSIBILITY}} | `{{PATH}}` |

- Which layers exist, top to bottom?
- Which layer owns entry points, orchestration, domain logic, and persistence?

## Module boundaries

| Module | Owns | Public surface | Must not import |
|---|---|---|---|
| {{MODULE}} | {{OWNS}} | {{PUBLIC_SURFACE}} | {{FORBIDDEN_IMPORTS}} |

- Where is the boundary enforced (package layout, lint rule, review)?
- Which modules are allowed to know about each other?

## Dependency rules

- Allowed direction: {{ALLOWED_DIRECTION}}.
- Forbidden edges: {{FORBIDDEN_EDGES}}.
- Cross-cutting code enters through {{MECHANISM}} (injection, adapter, event bus), never by direct import.

## Data flow

1. {{ENTRY_POINT}} receives {{INPUT}}.
2. {{LAYER}} validates and maps it to {{DOMAIN_TYPE}}.
3. {{LAYER}} persists or dispatches via {{MECHANISM}}.
4. {{OUTPUT}} returns to the caller.

- Note transaction boundaries and failure paths here.

## Cross-cutting concerns

| Concern | Approach | Reference |
|---|---|---|
| Auth / permissions | {{APPROACH}} | {{DOC}} |
| Logging / observability | {{APPROACH}} | {{DOC}} |
| Error handling | {{APPROACH}} | {{DOC}} |
| Configuration | {{APPROACH}} | {{DOC}} |

## ADR links

Architecture decisions that shaped this page are recorded in [`../adr/README.md`](../adr/README.md). Link each relevant ADR from the section it explains.
