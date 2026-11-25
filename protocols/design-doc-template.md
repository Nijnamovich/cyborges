# Template: Design Doc

Fill-in scaffold for the durable design document described in [`system-design-review.md`](./system-design-review.md). Replace every `[bracket]` with project-specific content; keep the heading order.

## Purpose

The design doc is the durable artifact of [`system-design-review.md`](./system-design-review.md) — filled once per substantial design, kept for the life of the feature, and amended by link rather than rewritten. A design is substantial when it introduces a new service, datastore, public contract, or cross-team dependency, or changes an existing one's failure or scale characteristics.

## How to use

1. **Copy** this file to the target project's docs tree (for example `docs/design/<slug>.md`) and **rename** it to the design slug, not to `design.md`.
2. **Retain** the doc after delivery; it is the reference for reviewers, operators, and future ADRs. Supersede it with a new doc plus a link, never delete it.
3. **Delete inapplicable sections** instead of leaving placeholders — an empty `### Cache` or a bare `[TBD]` reads as unfinished work.
4. **Numbers over adjectives.** Every target, limit, and estimate carries a unit; "fast", "large", and "scalable" are not requirements.
5. **Point, do not restate.** Security lives in [`security-review.md`](./security-review.md), UI in [`ui-design.md`](./ui-design.md), scope reduction in [`prompt-pipeline.md`](./prompt-pipeline.md); link them.

## Template

### Problem and scope

- **Problem:** [what hurts today, for whom, and the evidence — incident, ticket, metric, user report]
- **Goals:** [3–5 outcome statements, each measurable]
- **Non-goals:** [explicitly out of scope for this design]
- **Constraints:** [deadline, budget, team size, compliance, systems that cannot change]
- **Current vs target scale:** [today's numbers and the 12-month target; detail in Estimation]

### Requirements

| ID | Type | Requirement | Target |
|---|---|---|---|
| R1 | Functional | [user-visible capability] | [acceptance condition] |
| R2 | Functional | [user-visible capability] | [acceptance condition] |
| N1 | Non-functional | [latency] | [p95 ≤ _ ms at _ QPS] |
| N2 | Non-functional | [throughput] | [peak _ QPS sustained] |
| N3 | Non-functional | [availability / durability] | [99._% ; RPO _ , RTO _ ] |
| N4 | Non-functional | [cost] | [ceiling per month or per request] |

- Functional requirements describe observable behavior, one row per capability.
- Non-functional requirements are numeric and testable; no "fast", "scalable", or "highly available" without a number.
- Mark any requirement that is a hard constraint (regulatory, contractual) versus a preference.

### Estimation

- Fill the capacity worksheet at [`capacity-estimate-template.md`](./capacity-estimate-template.md) and link the filled copy here.
- Carry forward only the figures that drive design: peak QPS, storage growth per year, egress, and fan-out.
- State whether each figure is measured, estimated, or assumed, and its confidence.
- Name the assumption most likely to invalidate the design if it is wrong.

### High-level design

- **Components:** [named box — one-line responsibility — owner]
- **Boundaries:** [what each component owns, what it must not reach into, trust boundaries]
- **Data flow:** [numbered steps for the primary path; mark synchronous vs asynchronous hops]
- **Text sketch:** [box-and-arrow in text or a small ASCII block; no image assets]
- **Dependencies:** [existing services, external providers, shared schemas]
- **Deployment shape:** [regions, environments, tenancy, stateful components]

Keep each component to one line. Anything that needs a paragraph belongs in a deep dive.

### Data model and API

| Entity | Key fields | Primary key | Relationships | Retention |
|---|---|---|---|---|
| [name] | [fields] | [key] | [parent/child, cardinality] | [duration] |

| Endpoint or event | Method / direction | Purpose | Request | Response | Error paths |
|---|---|---|---|---|---|
| [`/v1/...`] | [GET / POST / emitted / consumed] | [one line] | [shape or schema link] | [shape] | [codes and meanings] |

- Name the storage engine and the partition or shard key, with the reason.
- State idempotency, pagination, versioning, and ordering guarantees per contract.
- Access control is owned by [`security-review.md`](./security-review.md); reference its findings, do not restate the rules.

### Deep dives

Pick the **1–2 riskiest components only** — the ones where a wrong choice is expensive to reverse or hard to detect.

- **Component:** [name]
- **Why risky:** [novelty, load, consistency, concurrency, dependency, migration]
- **Design:** [mechanism, invariants, ordering and concurrency model]
- **Failure behavior:** [what happens when it is slow, partitioned, or restarted]
- **Evidence:** [spike, benchmark, prototype, or prior art — and its result]

Everything not riskiest stays a one-liner in High-level design.

### Failure modes and operations

| Failure mode | Detection | Impact | Mitigation | Recovery |
|---|---|---|---|---|
| [dependency down] | [signal] | [user-visible effect] | [fallback, shed, retry] | [steps, owner] |
| [saturation] | [signal] | [effect] | [limit, scale, queue] | [steps] |
| [data corruption or loss] | [signal] | [effect] | [checks, backups] | [restore, RPO/RTO] |

- **SLOs:** [SLI — target — window] for each user-facing path.
- **Dashboards:** [3–5 signals that would explain an incident]
- **Alerts:** [symptom-based; paging vs ticket; owner]
- **Operability:** runbooks, deploy and rollback procedure, backup and restore drill, on-call rotation.

### Alternatives and decisions

| Option | Summary | Pros | Cons | Verdict |
|---|---|---|---|---|
| [A] | [one line] | [—] | [—] | [chosen / rejected, why] |
| [B] | [one line] | [—] | [—] | [chosen / rejected, why] |
| Do nothing | [what happens if deferred] | [—] | [—] | [baseline] |

- Score options with the criteria from [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md); link the analysis rather than repeating the matrix.
- One consequential decision gets one ADR written from [`adr-template.md`](./adr-template.md); list the ADR paths here.
- Mark each decision as a two-way or one-way door, and the cost to reverse.

### Rollout and open questions

- **Rollout:** [phases, feature flags, percentage ramp, backfill or migration order, rollback trigger]
- **Compatibility:** [clients, schema, events, deprecation window]
- **Open questions:** [table below — no question without an owner]

| Question | Owner | Needed by | Blocking? |
|---|---|---|---|
| [question] | [name or seat] | [date or milestone] | [yes/no] |

- **Sign-off:** [reviewers, date, link to the review record]

## Acceptance

- [ ] Problem and scope stated with evidence; non-goals listed explicitly.
- [ ] Every assumption listed with the consequence if it is wrong.
- [ ] Every non-functional requirement has a number, a unit, and a measurement point.
- [ ] A load estimate exists for every quantity that drives a choice, with arithmetic and an estimate label; the worksheet is linked.
- [ ] At least two viable options plus a do-nothing baseline, compared against named drivers.
- [ ] Failure modes named — dependency down, partial failure, overload, data loss, duplicate processing — each with the designed response.
- [ ] High-level design names every component, its boundary, and the primary data flow.
- [ ] Data model and API are sketched well enough to expose the hard part; keys, contracts, and error paths are present.
- [ ] Deep dives cover the 1–2 riskiest components; everything else stays a one-liner.
- [ ] SLOs, dashboards, and alerts are defined.
- [ ] Rollout and rollback stated, including what rollback cannot undo.
- [ ] Each consequential decision links an ADR emitted via [`adr-template.md`](./adr-template.md), with consequences filled.
- [ ] Every open question has an owner and what settles it; no blocking question is left unowned.
- [ ] No placeholders remain; inapplicable sections were deleted.
- [ ] No UI, security, or capacity guarantee is claimed outside its owning protocol.
- [ ] Reviewed under [`system-design-review.md`](./system-design-review.md) with reviewers and date recorded.

## Cross-references

- [`system-design-review.md`](./system-design-review.md) — the review procedure that consumes this doc and owns the acceptance gate.
- [`capacity-estimate-template.md`](./capacity-estimate-template.md) — the worksheet linked from Estimation.
- [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md) — the scoring method linked from Alternatives.
- [`adr-template.md`](./adr-template.md) — one ADR per consequential decision.
- [`system-design-primitives.md`](./system-design-primitives.md) — the vocabulary and building blocks the design is composed from.
- [`prompt-pipeline.md`](./prompt-pipeline.md) — scope reduction before a design is commissioned.
- [`security-review.md`](./security-review.md) — security findings and threat modeling; linked, never restated.
- [`ui-design.md`](./ui-design.md) — UI-specific design; this doc links to it for user-facing surfaces.
