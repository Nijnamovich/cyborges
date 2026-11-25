# Protocol: Design Trade-off Analysis

Structured comparison of design options that ends in a decision record. Name the
drivers, compare at least two real options plus "do nothing", assess reversibility and
cost, probe sensitivity, emit an ADR, and escalate genuine ties.

> This protocol produces one ADR. It does not choose architecture by itself and it does
> not replace the design loop — it is the instrument that loop uses at its trade-off
> stage ([`system-design-review.md`](./system-design-review.md)).

## When to apply

Apply when at least one is true:

- Two or more viable options exist and the choice changes the shape of the system.
- The choice is load-bearing (auth, schema or data migration, breaking change, public
  contract) or hard to reverse.
- A boundary or pattern decision must be made (where a responsibility lives, which
  documented pattern applies).
- A build-versus-buy, datastore, transport, or deployment-unit choice is open.

Do not apply to a reversible, low-cost detail with one obviously adequate answer — write
the one-line rationale in the design document and move on. Do not apply to a pure
preference: a preference is recorded as an opinion, not scored.

## Decision record shape

Every analysis emits exactly one ADR via [`adr-template.md`](./adr-template.md). The
template owns the section order and front matter; the table below states what each field
must contain and is not a substitute for reading it.

| Field | Must contain | Fails when |
|---|---|---|
| `status` | `proposed`, `accepted`, `rejected`, `superseded`, or `deprecated`, with date | A record with no lifecycle state, or one marked accepted before the decision is made |
| Context | The problem, the forces at play, and the scope of the decision in a short paragraph | The context restates the chosen solution |
| Drivers | The 3–6 criteria used to compare, each with a direction (higher or lower is better) | Drivers invented after scoring, or a driver nobody could measure or judge |
| Options | At least two viable options plus "do nothing / status quo", each with a one-paragraph description | A single option, or options that differ only in naming |
| Decision | The chosen option, in one sentence, and the margin by which it won | "It depends", or a decision with no stated winner |
| Consequences | What becomes easier, what becomes harder, what is now harder to reverse, and the follow-ups the choice creates | Only positive consequences |
| Links | The design document, the estimate, the review, and any superseded ADR | A record that cannot be traced from the design |

One decision per record. A record that decides three things cannot be superseded cleanly.

## Option comparison

**Drivers (choose 3–6, no more).** Typical set: latency, cost, operability (deploy,
observe, on-call load), reversibility, team fit (existing skills and patterns),
compliance and data residency. Pick the ones that can actually change the outcome and
state why the others were excluded.

**Options.** At least two viable options, plus:

- **Do nothing / status quo** — always present, always scored. It is often the correct
  answer when the current cost is acceptable, and it is the baseline every other option
  must beat. Omitting it inflates every comparison.

**Scoring.** Use one scale for the whole record and state it once:

| Scale | Use when |
|---|---|
| `High` / `Med` / `Low` | The driver is judged, not measured (team fit, operability) |
| `1–5` | The driver has an ordinal gradient and reviewers benefit from finer ranking |

For the `1–5` scale, state what the endpoints mean (e.g. `5` = best on this driver,
`1` = worst) and never mix scales inside one record. Mixed units, invented decimal
precision, or weighted totals that hide the raw scores are defects — show the raw matrix
and, if weights are used, show them as a separate stated row.

| Driver (direction) | Option A | Option B | Do nothing |
|---|---|---|---|
| Latency (lower better) | 4 | 3 | 2 |
| Operability (higher better) | 3 | 5 | 5 |
| Reversibility (higher better) | 2 | 4 | 5 |
| Rough annual cost (lower better) | 3 | 2 | 5 |

Scores are judgements, not measurements. Where a score rests on an estimate, cite the
estimate ([`capacity-estimate-template.md`](./capacity-estimate-template.md)); where it
rests on a benchmark or a document, link it. A score with no basis is an opinion wearing
a number.

**Sensitivity.** Before deciding, ask which single driver, if it moved by one step, would
change the winner. If the answer is "any of three", the comparison is not separating the
options — gather evidence or escalate ([§ Escalation to analista](#escalation-to-analista)).
Record the sensitivity result in the ADR's consequences or context.

## Reversibility and cost

Classify every option before choosing:

| Class | Meaning | Consequence |
|---|---|---|
| **Two-way door** | Can be undone in one delivery cycle at acceptable cost, with no data loss and no contract break | Decide quickly; prefer it on a tie |
| **One-way door** | Undoing requires a migration, a contract break, or a data-repair campaign | Needs the full comparison, an ADR, and often a human check |

For each option name three costs:

- **Migration cost** — work to get there: code, data backfill, dual-write window,
  coordination, downtime.
- **Run cost** — steady state: infrastructure, licences, operational load, on-call.
- **Exit cost** — work to leave later: data export, contract unwinding, retraining,
  rewrite of the parts that leak the choice.

**Tie-break rule:** when scores tie within noise on the load-bearing drivers, prefer the
**reversible** option. A reversible wrong choice is cheap; a one-way-door wrong choice is
not. Never break a tie with a driver that was not scored.

## Escalation to analista

Escalate instead of choosing when:

- Two options score within noise on the load-bearing drivers and sensitivity shows the
  winner flips on a plausible change.
- The decision is a genuine tie after the reversibility tie-break.
- The comparison exposes a disagreement about facts rather than preferences.

The escalation goes to `analista` for an independent verdict. Do **not** average scores,
do not silently add a driver until one option wins, and do not let the author of an
option also be its judge. The record keeps the options open and notes that the verdict is
pending.

A **load-bearing** decision returned with `confidence < 0.5` does not proceed on the
author's say-so: the orchestrator's `## Confidence Gate` surfaces it as
`STATUS: NEEDS_HUMAN`. Reversibility does not weaken that rule for one-way doors.

## Anti-patterns

- **Scoring after the decision** — the matrix is reverse-engineered to justify a choice
  already made.
- **Inventing precision** — weighted totals to two decimals over judgements, or
  `3.7` where the scale is `High/Med/Low`.
- **Ignoring do-nothing** — no baseline, so every option looks like an improvement.
- **Comparing incomparable scopes** — option A includes migration and option B does not.
- **An ADR that records the winner but not the rejected options** — the rejected list is
  the record's value; without it the decision cannot be revisited.
- **Averaging a tie** — splitting the difference between two designs produces a third
  design nobody evaluated.
- **One-way door on vibes** — an irreversible choice decided without the full comparison
  or a human check.
- **Re-scoring until the preferred option wins** — changing drivers or scale mid-record.

## Cross-references

- [`adr-template.md`](./adr-template.md) — the record every analysis emits; owns field
  order and lifecycle.
- [`system-design-review.md`](./system-design-review.md) — the design loop whose
  trade-off stage invokes this protocol.
- [`design-doc-template.md`](./design-doc-template.md) — where the ADR link and the
  design narrative live.
- [`system-design-primitives.md`](./system-design-primitives.md) — anchors for the
  latency and throughput judgements that feed driver scores.
- [`capacity-estimate-template.md`](./capacity-estimate-template.md) — the estimate
  behind any cost or scale score.
- [`prompt-pipeline.md`](./prompt-pipeline.md) — owns scope reduction and the hot-spot
  test that decides whether a choice is load-bearing.
- [`orchestrate.md`](./orchestrate.md) — seat cadence and how an escalated verdict is
  routed back into delivery.
- [`security-review.md`](./security-review.md) — owns security-class constraints that
  enter the comparison as drivers, never as a protocol restated here.
