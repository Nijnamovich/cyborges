---
last_updated: {{YYYY-MM-DD}}
status: active
description: {{Project metadata, stack, commands, domain entities, and the Slices routing table.}}
tags: [{{project}}, {{metadata}}]
---

# Project: {{PROJECT_NAME}}

Canonical entry point for {{PROJECT_NAME}}. Every change routes through the Slices table below to its primary doc and primary agent.

## Metadata

| Field | Value |
|---|---|
| Project name | {{PROJECT_NAME}} |
| Repo | {{REPO_URL_OR_PATH}} |
| Owner | {{OWNER}} |
| Default branch | {{DEFAULT_BRANCH}} |

## Stack and versions

| Layer | Tech | Version |
|---|---|---|
| {{LAYER}} | {{TECH}} | {{VERSION}} |
| {{LAYER}} | {{TECH}} | {{VERSION}} |

## Commands

Plan for all five rows; delete a row only when the project has no such action.

| Action | Command | Run from |
|---|---|---|
| Install | `{{INSTALL_COMMAND}}` | {{INSTALL_DIR}} |
| Build | `{{BUILD_COMMAND}}` | {{BUILD_DIR}} |
| Test | `{{TEST_COMMAND}}` | {{TEST_DIR}} |
| Lint | `{{LINT_COMMAND}}` | {{LINT_DIR}} |
| Typecheck | `{{TYPECHECK_COMMAND}}` | {{TYPECHECK_DIR}} |

Run commands from the affected package directory, never the repository root, unless the project documents otherwise.

## doc_language

| Field | Value |
|---|---|
| `doc_language` | `{{DOC_LANGUAGE}}` (default `en`) |

Documentation content follows this value. Code, identifiers, file names, and agent-system files stay English.

## Domain entities

| Entity | Meaning | Key fields |
|---|---|---|
| {{ENTITY}} | {{MEANING}} | {{KEY_FIELDS}} |

## Slices

| Area | Paths | Primary doc | Primary agent |
|---|---|---|---|
| {{AREA}} | `{{PATH}}` | `context/{{PRIMARY_DOC}}.md` | `{{PRIMARY_AGENT}}` |
| {{AREA}} | `{{PATH}}` | `context/{{PRIMARY_DOC}}.md` | `{{PRIMARY_AGENT}}` |

New rows change routing and require human approval. Keep all four registries in sync when a row is added, renamed, or removed.

## Glossary

| Term | Meaning |
|---|---|
| {{TERM}} | {{MEANING}} |
