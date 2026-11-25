---
last_updated: {{YYYY-MM-DD}}
status: {{draft|active|deprecated}}
description: {{Registry of project-local protocols and their distinction from the global agent protocols.}}
tags: [{{protocols}}, {{registry}}]
---

# Project Protocols

Registry of **project-local** protocols: procedures that belong to {{PROJECT_NAME}} and are written for its own contributors and agents.

## What this is

- A project-local protocol is a project-specific procedure: release steps, environment setup, review checklists, data-handling rules.
- Files live next to this README as `{{protocol-name}}.md` and follow [`../context/doc-conventions.md`](../context/doc-conventions.md).
- This registry is one of the four files kept in sync on Create, Rename, or Delete of a doc.

## Relationship to the global protocols

| Kind | Location | Scope | Owner |
|---|---|---|---|
| Project-local protocol | `docs/protocols/` (this directory) | {{PROJECT_NAME}} only | Project maintainers |
| Global agent protocol | `protocols/` in the agent-system install | Every project the agent system operates on | Agent-system maintainers |

The two are separate namespaces. Do not copy global agent protocols into this directory, and do not edit the global `protocols/` from a project. Reference a global protocol by name and path relative to the agent-system install when a project procedure depends on it.

## Registry

| Protocol | Purpose | Owner | last_updated |
|---|---|---|---|
| {{PROTOCOL}}.md | {{PURPOSE}} | {{OWNER}} | {{YYYY-MM-DD}} |

Add one row per project-local protocol file. Remove the row when the protocol is deleted; list a kept-but-superseded protocol with `(DEPRECATED)` in its purpose.
