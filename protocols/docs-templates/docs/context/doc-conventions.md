---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{Canonical format, frontmatter contract, and freshness rules for every documentation page.}}
tags: [{{docs}}, {{conventions}}]
---

# Documentation Conventions

Canonical format for every page under `docs/`. Apply it when creating or editing documentation.

## Frontmatter

Every page except a top-level template README starts with:

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
| `last_updated` | ISO 8601 date (`YYYY-MM-DD`); the date the content last changed, not the file's copy date. |
| `status` | Exactly one of `draft` (not yet trustworthy), `active` (current), `deprecated` (kept for history, superseded). |
| `description` | One line, no trailing period required, states the page's single topic. |
| `tags` | Flow list of lowercase lookup tags; mirror them in `../tag-index.md`. |

## Structure

- Exactly one H1 per page, matching the page's purpose.
- H2 sections; maximum 3 nesting levels (H1 → H2 → H3).
- Tables and checklists over narrative prose.
- Code blocks and real project examples where they make a contract concrete.
- Frontmatter first, then H1, then sections — no content before the frontmatter.

## Writing rules

- Concise technical prose. State the contract, not the history of the decision.
- Contracts, tables, and checklists over narrative explanation.
- Reference another doc by relative link instead of repeating its content.
- English unless `docs/project.md` → `doc_language` says otherwise; code, identifiers, and agent-system files stay English.
- Status markers in headings or list items: `(WIP)`, `(TODO)`, `(DEPRECATED)`.
- No images, no emoji, no decorative markup.

## Status and freshness

| Age since `last_updated` | Action |
|---|---|
| ≤ 30 days | Current. No action. |
| > 30 days | Stale warning: re-read against the code and update or confirm. |
| > 90 days | Flag for review or removal; deprecate or refresh. |

- A `draft` page older than 90 days is a removal candidate unless someone owns it.
- Exempt: per-session cache contents.
- Updating `last_updated` is allowed only after the content is confirmed valid.

## Link integrity

- Every relative markdown link must resolve to an existing file or anchor.
- Check links whenever a doc is created, renamed, or removed.
- A broken link in a routing document (`docs/project.md` Slices, `docs/context/README.md`, `docs/tag-index.md`, `docs/protocols/README.md`) is **critical** — fix or flag it immediately.
- Do not link outside the project to files that only exist in the agent-system install; name them instead.
