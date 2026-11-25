---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{Authoritative index of every document under docs/context/.}}
tags: [{{context}}, {{index}}]
---

# Context Index

Authoritative registry of the strategic docs in `docs/context/`. One topic per file; every file is listed here.

## Index

| Doc | Status | Owner | Tags | last_updated |
|---|---|---|---|---|
| [`architecture.md`](./architecture.md) | draft | {{OWNER}} | architecture | {{YYYY-MM-DD}} |
| [`doc-conventions.md`](./doc-conventions.md) | active | {{OWNER}} | docs, conventions | {{YYYY-MM-DD}} |

## Rules

- One topic per file. Split a page when it starts covering unrelated subjects.
- Register every new context doc in this table in the same change that creates it.
- Update `last_updated` in both the doc's frontmatter and this table whenever its content changes.
- This table is the authoritative index; `../tag-index.md` is only a derived fast lookup.
