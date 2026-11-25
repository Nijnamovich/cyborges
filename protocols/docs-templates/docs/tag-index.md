---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{Fast tag-to-doc lookup across docs/context/.}}
tags: [{{index}}, {{tags}}]
---

# Tag Index

Fast lookup from a tag to the context doc and section that defines it. Derived from the docs; [`context/README.md`](./context/README.md) remains the authoritative index.

## Tag index

| Tag | Doc | Section |
|---|---|---|
| `{{TAG}}` | `context/{{DOC}}.md` | {{SECTION}} |

Seed the table from the `tags` frontmatter of every file listed in [`context/README.md`](./context/README.md). Add one row per doc-section pair a reader would plausibly search for.

## How to use

1. Search this table for the tag, then open the named doc and section.
2. When a context doc gains, loses, or renames a tag, update this table in the same change.
3. Do not treat this page as the index of record: if it disagrees with [`context/README.md`](./context/README.md), the context index wins and this table is corrected.
4. Keep tags lowercase and stable; one tag may point to several docs.
