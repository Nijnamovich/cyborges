# Template: ADR

Fill-in scaffold for an Architecture Decision Record. One decision per file; the value is in the reasoning and the history, not the length.

## Purpose

An ADR is the durable record emitted by [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md): it captures what was decided, against which criteria, and what it costs. Write one ADR per decision — bundling two decisions makes both hard to supersede. An ADR is not a design doc; it records a choice, not a system.

## Naming and location

| Rule | Convention |
|---|---|
| Filename | `NNNN-short-title.md` — `NNNN` zero-padded and monotonic within a project's ADR set, never reused |
| Title | Lower-case kebab, ≤5 words, names the decision (`0007-use-postgres-for-orders.md`), not the topic |
| Location | The project's `docs/adr/` when the project has a `docs/` tree; keep the numbering local to that project |
| Granularity | One decision per ADR; a related but separable choice gets its own number |
| Status home | The `Status` section inside the file, never the filename |

This repository ships a copyable skeleton at [`docs-templates/docs/adr/README.md`](./docs-templates/docs/adr/README.md). Do **not** create a root `docs/` in this repository — it holds agent-system assets, not project documentation.

## Template

### Status

`proposed | accepted | superseded by NNNN | deprecated` — plus the date of the last status change. Accepted ADRs keep their status until an explicit supersede or deprecation.

### Context

- [Forces at play: constraints, existing system, team, deadlines, regulations, operational reality]
- [What changed to make this decision necessary now]
- Neutral statement of the situation — no decision yet, no advocacy.

### Drivers

- [Named criterion the options are judged against — e.g. latency, cost, operability, team familiarity, reversibility, compliance]
- [Weight or ranking, if the tradeoff analysis used one]
- Reuse the exact criteria and scores from [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md) so the record and the analysis agree.

### Options

| Option | Summary | Pros | Cons | Score |
|---|---|---|---|---|
| [A] | [one line] | [—] | [—] | [from analysis] |
| [B] | [one line] | [—] | [—] | [from analysis] |
| Do nothing | [state what happens if deferred] | [—] | [—] | [baseline] |

- At least two real alternatives plus the do-nothing baseline; a single-option ADR is a memo, not a decision record.

### Decision

- **We will** [chosen option in one active-voice sentence].
- **Because** [decisive driver scores and the constraint that ruled others out].
- **We will not** [the rejected direction, so future readers do not reintroduce it by accident].

### Consequences

- **Positive:** [what improves, with the metric or capability]
- **Negative:** [accepted cost, new failure mode, operational burden, lock-in]
- **Follow-ups:** [work this decision creates — owner and issue]
- **Reversibility:** [two-way or one-way door; the cost and trigger for reversing]

### Links

- Design doc: `<path to the design doc>`
- Tradeoff analysis: `<path to the analysis>`
- Related ADRs: `NNNN-short-title.md`, `NNNN-short-title.md`
- Pull requests, issues, incidents: [links]
- Source material: [chapter, note, or reference — attributed, never copied]

## Superseding an ADR

1. **Never edit an accepted ADR's Decision, Context, or Drivers in place.** History is the point; a rewritten record is a falsified one.
2. Write a **new ADR** with the next `NNNN`, status `accepted`, and a Context section that explains what changed since the original.
3. Change only the **Status** line of the old ADR to `superseded by NNNN`, and add the new ADR to its Links.
4. **Keep both files.** Do not delete or renumber; links from PRs, issues, and other ADRs must keep resolving.
5. Typo fixes and formatting are fine at any time; any change of meaning is a new ADR.

## Cross-references

- [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md) — produces the decision this ADR records.
- [`system-design-review.md`](./system-design-review.md) — requires an ADR for each consequential decision.
- [`design-doc-template.md`](./design-doc-template.md) — the design doc that links these ADRs from Alternatives and decisions.
- [`docs-templates/docs/adr/README.md`](./docs-templates/docs/adr/README.md) — copyable ADR skeleton and index.
- [`prompt-pipeline.md`](./prompt-pipeline.md) — how the decision becomes an authorized change cycle.
- [`orchestrate.md`](./orchestrate.md) — seat cadence around design review and decision recording.
