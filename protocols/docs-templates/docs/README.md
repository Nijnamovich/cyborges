---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{Entry point and map of the project documentation tree.}}
tags: [{{docs}}, {{index}}]
---

# Documentation

Canonical documentation root for {{PROJECT_NAME}}. One topic per file; registries route readers to the right page.

## What lives here

| Path | Contents |
|---|---|
| [`project.md`](./project.md) | Project metadata, stack, commands, domain entities, Slices table. |
| [`context/`](./context/README.md) | Strategic docs: architecture, conventions, rules, design system. |
| [`tag-index.md`](./tag-index.md) | Fast tag-to-doc lookup over context docs. |
| [`protocols/`](./protocols/README.md) | Project-local procedures and their registry. |
| [`adr/`](./adr/README.md) | Architecture decision records. |

## Start here

1. Read [`project.md`](./project.md) for metadata, commands, and the Slices table that routes every change.
2. Read [`context/README.md`](./context/README.md) to find the relevant context doc.
3. Read the primary doc named by the matching Slices row before changing that area.
4. Follow [`context/doc-conventions.md`](./context/doc-conventions.md) when writing or editing any page.

## Conventions

- Every page carries the frontmatter contract defined in [`context/doc-conventions.md`](./context/doc-conventions.md).
- Registries are updated in the same change that adds, renames, or removes a doc: `project.md` Slices, `context/README.md`, `tag-index.md`, `protocols/README.md`.
- Documentation content is written in the project's `doc_language`; code and identifiers stay English.
- Status markers: `(WIP)`, `(TODO)`, `(DEPRECATED)` complement the frontmatter `status`.
