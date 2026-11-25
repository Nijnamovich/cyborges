# Docs Template — Instantiation Contract

A copyable `docs/` skeleton for a target project. Copy this tree into the project repository, replace every `{{PLACEHOLDER}}`, and the documentation routing paths cited by the agent-system become real on first instantiation.

## What this is

- A **project-local** `docs/` skeleton: the canonical documentation root for one target repository.
- **Not** the global `protocols/` directory. Agent-system protocols live in the install's `protocols/` and stay read-only; this skeleton only provides project documents.
- The directory layout mirrors what the documenter seat expects (`docs/project.md`, `docs/context/`, `docs/tag-index.md`, `docs/protocols/`) and extends it with `docs/adr/`.

## Copy order

Copy in dependency order so each layer can link to the previous one:

1. `docs/README.md` and `docs/project.md` — entry point and project metadata, stack, commands, Slices.
2. `docs/context/README.md` and `docs/context/doc-conventions.md` — context index and the canonical doc format.
3. `docs/context/architecture.md` — fill from the project's real layering; leave `draft` until verified.
4. `docs/protocols/README.md`, `docs/adr/README.md`, and `docs/tag-index.md` — the remaining registries.

Replace every `{{PLACEHOLDER}}` with a project value. Delete rows or sections that do not apply; do not leave empty scaffolding behind.

## Registry files that must stay in sync

All four registries are included so the documenter loop closes on first instantiation. On Create, Rename, or Delete of any doc, update all of them that are affected:

| Registry | Owns |
|---|---|
| `docs/project.md` → Slices table | Which area routes to which primary doc and primary agent |
| `docs/context/README.md` | The authoritative index of every context doc |
| `docs/tag-index.md` | Fast tag-to-doc lookup across context docs |
| `docs/protocols/README.md` | The registry of project-local protocols |

## Frontmatter contract

Every page in the copied tree except this top-level README carries this block:

```markdown
---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{one line}}
tags: [{{tag}}, {{tag}}]
---
```

| Field | Rule |
|---|---|
| `last_updated` | ISO date (`YYYY-MM-DD`); update whenever content changes. |
| `status` | Exactly one of `draft`, `active`, `deprecated`. |
| `description` | One line, describes the page's single topic. |
| `tags` | Flow list of lowercase lookup tags. |

## doc_language

Documentation content follows the project's configured `doc_language` in `docs/project.md`. Code, identifiers, file names, and all agent-system files stay in English regardless of that setting.

## Why this repo has no docs/

The global install must never ship a global `docs/` — see the Path contract golden rule in `readme.md` ("never create a global `docs/`") and thinking rule 1 in `protocols/orchestrate.md` ("never create a global `docs/`"). A root `docs/` here would collapse the distinction between project documents and agent-system assets.

This skeleton therefore lives under `protocols/docs-templates/` precisely so it is copyable without violating that rule. It is a template, not a live documentation tree: the agent-system install does not read it as project context.

## Cross-references

- [`./docs/README.md`](./docs/README.md) — docs root entry point.
- [`./docs/project.md`](./docs/project.md) — project metadata, stack, commands, Slices.
- [`./docs/context/README.md`](./docs/context/README.md) — context index.
- [`./docs/tag-index.md`](./docs/tag-index.md) — tag lookup.
- [`./docs/protocols/README.md`](./docs/protocols/README.md) — project-local protocol registry.
- [`./docs/adr/README.md`](./docs/adr/README.md) — architecture decision records.
- [`../maintenance.md`](../maintenance.md) — maintenance audit of the instantiated tree.
