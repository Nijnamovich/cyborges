---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{Registry and numbering rules for architecture decision records.}}
tags: [{{adr}}, {{decisions}}]
---

# Architecture Decision Records

Registry of accepted architecture decisions for {{PROJECT_NAME}}. One decision per file; the registry below is the index.

## What this is

- An ADR records **why** a structural decision was made, the alternatives rejected, and the consequences accepted.
- ADRs are immutable history: correct a later change with a new ADR, not by rewriting the old one.
- ADRs are produced by the global `design-tradeoff-analysis` protocol and instantiated from the global `adr-template` (named, not linked: an instantiated project cannot resolve the agent-system install's own protocol path).
- Link each ADR from the context doc it explains, for example [`../context/architecture.md`](../context/architecture.md).

## Numbering

| Rule | Value |
|---|---|
| File name | `NNNN-short-title.md` |
| Number | Zero-padded, four digits, starting at `0001` |
| Order | Monotonic: the next number is the highest existing number plus one |
| Reuse | Never; a deleted decision keeps its number retired |

## Registry

| ADR | Title | Status | Date |
|---|---|---|---|
| `{{NNNN}}-{{short-title}}.md` | {{TITLE}} | {{proposed|accepted|superseded|deprecated}} | {{YYYY-MM-DD}} |

## Template

Copy the global `adr-template` structure when instantiated into this project:

1. **Title** — `NNNN. Short decision title`.
2. **Status** — proposed, accepted, superseded, or deprecated; link the superseding ADR when applicable.
3. **Context** — the forces and constraints that made a decision necessary.
4. **Decision** — the choice, stated in one paragraph.
5. **Alternatives considered** — each rejected option and why.
6. **Consequences** — what becomes easier, what becomes harder, and what must be revisited.

**Superseding:** to replace a decision, write a new ADR that references the old one, set the old ADR's status to `superseded` with a link to the new file, and update both rows in the registry. Never renumber or delete the old record.
