# Protocol: System Design Review

The operating loop `architect` runs for a non-UI system, service, or component design, a
scale or capacity question, or a boundary and pattern decision. The loop produces
decisions, a design document, and an ADR — never code.

> This protocol is the loop, not the artefact library. Templates, estimation scaffolds,
> and the trade-off instrument are separate files and are linked, not restated. UI,
> security, and scope reduction stay with their owning protocols.

## When to apply

| Trigger | Example |
|---|---|
| New service or component design | "design an ingestion pipeline for tenant events" |
| Scale or capacity question | "will this hold 10k tenants and 5 years of history?" |
| Boundary or pattern decision | "where does billing end and accounts begin?" |
| Any design with no UI surface | queue, worker, API, storage layout, sync job |

**Out of scope — route, do not absorb:**

| Task | Route to |
|---|---|
| A page, screen, form, or other UI surface | [`ui-design.md`](./ui-design.md) |
| Security certification or threat modelling | [`security-review.md`](./security-review.md), [`owasp-analysis.md`](./owasp-analysis.md) |
| Writing or editing the implementation | `coder` (`language=angular\|go\|css`) |
| Critique of an existing design, second opinion, or tie-break | `analista` |
| Unknowns that need evidence before any design is possible | [`broad-investigation-template.md`](./broad-investigation-template.md) first |

A task that is partly UI runs both protocols: this loop owns the system decisions, and
[`ui-design.md`](./ui-design.md) owns the design brief for the surface.

## The design loop (Scope → Estimation → High-Level Design → Deep Dive → Trade-offs → Wrap-up)

Six stages, in order. Each stage has an exit condition; a stage that cannot meet it is a
declared gap carried forward, not skipped silently.

### 1. Scope

State the problem in one sentence, then the requirement set:

- **Functional requirements** — what the system must do, as observable behavior.
- **Non-functional requirements** — latency, throughput, availability, durability,
  consistency, retention, compliance. Each with a target and a tolerance.
- **Non-goals** — what this design deliberately does not solve, and why not.
- **Constraints** — budget, team size and skills, existing stack, deadlines, data
  residency, contractual limits.
- **Inputs** — the documents, code paths, and measurements the rest of the loop will
  rely on.

Scope reduction is not re-derived here: [`prompt-pipeline.md`](./prompt-pipeline.md) →
Phase 2 owns it, including the explicit out-of-scope list this stage consumes.

**Exit:** a third party can state what will be built and what will not, without reading
the rest of the design.

### 2. Estimation

Size the load and the data envelope before choosing components:

- Peak and average request rate, read/write split.
- Records per unit time, record size, retention, growth per year.
- Working set versus cold storage.
- Ingress and egress bandwidth at peak.
- The single largest cost driver (storage, compute, network, or operations).

Follow [`capacity-estimate-template.md`](./capacity-estimate-template.md) for the
worksheet and [`system-design-primitives.md`](./system-design-primitives.md) for the
reference numbers. Arithmetic rules are in the next section.

**Exit:** every quantity that drives a component choice is estimated, labeled, and
traceable to a stated assumption. "Unknown" is an allowed value only with the reason and
what would settle it.

### 3. High-Level Design

- **Components** — each with one responsibility, in one table.
- **Boundaries** — what each component owns, what it must not own, and which data has a
  single source of truth.
- **Data flow** — synchronous versus asynchronous paths, ordering, retries, and the
  direction of every dependency.
- **Interfaces** — protocol and shape at each boundary, versioning stance.
- **Deployment units** — what scales together, what fails together.

Use [`design-doc-template.md`](./design-doc-template.md) as the document skeleton. Keep
this stage deliberately shallow: a component that needs more than two lines of
justification belongs in the deep dive.

**Exit:** dependencies point one way at each boundary, and every requirement in the scope
maps to at least one component.

### 4. Deep Dive

Pick only the **one or two riskiest components** — the ones that can invalidate the whole
design: the hot path, the consistency boundary, the migration, the piece with no proven
precedent. For each:

- Data model or state machine, at the level needed to spot the hard part.
- API or contract sketch.
- Failure behavior: dependency down, partial write, duplicate delivery, overload.
- Capacity check against the estimation stage.
- The open question that remains.

Everything else stays at high-level depth. A deep dive on a component nobody is worried
about is gold-plating.

**Exit:** the riskiest parts have a stated behavior under failure, and the design either
survives it or says what changes.

### 5. Trade-offs

For every load-bearing choice (datastore, boundary, sync versus async, build versus buy):

- At least two viable options **plus** an explicit "do nothing / status quo".
- Named drivers, a scored comparison, and a reversibility classification.
- An emitted ADR.

Run [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md); emit the record via
[`adr-template.md`](./adr-template.md). A design that records only the winner is
incomplete — the rejected options and why they lost are part of the output.

**Exit:** every load-bearing choice has a decision record with consequences.

### 6. Wrap-up

- **Open questions** — each with an owner and what would settle it.
- **Rollout** — phases, flags, backfill or dual-write window, ordering constraints.
- **Rollback** — the concrete path back, and what data it cannot undo.
- **Acceptance** — the checklist below, each item `met`, `not-met`, or `open`.
- **Handoff** — `architect` returns `decisions[]` and `files_to_touch[]`; implementation
  stays with `coder`.

**Exit:** the acceptance checklist has no unaddressed `not-met` item on a critical path.

## Back-of-envelope discipline

Estimates exist to eliminate options, not to predict the future.

1. **Order of magnitude only.** One significant figure. If a decision depends on a 20%
   difference, the estimate is the wrong instrument.
2. **State every assumption next to the number** it drives. An unlabeled number is a
   rumour.
3. **Compute the three base quantities:** request rate, storage, bandwidth. Everything
   else derives from them.
4. **Show the arithmetic.** A reader must be able to redo it with a calculator.
5. **Label estimates as estimates** — never let an estimate read as a measurement.
6. **Sanity-check against an anchor:** one machine, one disk, one network link, one
   managed-service quota. If the result is orders of magnitude off an anchor, the
   assumption is wrong, not the anchor.
7. **Carry uncertainty explicitly** — "between 1k and 5k QPS, because peak factor is
   unmeasured" beats a false single value.

| Quantity | Formula | Note |
|---|---|---|
| Average read QPS | reads per day ÷ 86,400 | reads per day = users × reads per user |
| Peak QPS | average × peak factor | peak factor 2–5, stated explicitly |
| Writes per day | users × write actions per user | split by record type when they differ |
| Storage per year | writes per day × bytes per record × 365 × replication | include index and WAL overhead as a stated multiplier |
| Bandwidth | QPS × payload bytes × 8 | bits per second; apply per direction |
| Working set | hot fraction × total record bytes | the part that must stay in memory or fast storage |

**Worked example (illustrative, not a measurement).** 1M daily users, 20 reads per user
per day: 20M reads/day ÷ 86,400 ≈ 231 average QPS; at a stated 4× peak ≈ 930 QPS, call it
about 1k. One write per 100 users per day: 10k writes/day ≈ 0.12 average write QPS, about
0.5 at peak. At 2 KB per record: 10k × 2 KB = 20 MB/day × 365 ≈ 7.3 GB/year, ×3 replicas
≈ 22 GB/year. At 5 KB per read response: 1k QPS × 5 KB × 8 ≈ 40 Mbps egress.

Those numbers say "one modest database and one application instance", which is the entire
point: the estimate's job is to rule out sharding and a data lake, not to size a cluster
to the rack.

Use [`capacity-estimate-template.md`](./capacity-estimate-template.md) for the worksheet
and [`system-design-primitives.md`](./system-design-primitives.md) for order-of-magnitude
anchors (latency, throughput, storage density).

## Acceptance conditions for a design

A design is ready to hand off only when every item is checkable and answered. Mark each
`met`, `not-met`, or `open`.

- [ ] Problem and scope stated; non-goals listed explicitly.
- [ ] Assumptions listed, each with the consequence if it is wrong.
- [ ] Load estimate present for every quantity that drives a choice, with arithmetic and
      an estimate label.
- [ ] At least two viable options plus "do nothing" compared against named drivers
      ([`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md)).
- [ ] Failure modes named — dependency down, partial failure, overload, data loss,
      duplicate processing — each with the designed response.
- [ ] Data model and API sketched well enough to expose the hard part.
- [ ] Rollout and rollback stated, including what rollback cannot undo.
- [ ] Open questions explicit, each with an owner and what settles it.
- [ ] ADR emitted via [`adr-template.md`](./adr-template.md), with consequences filled.
- [ ] No UI acceptance, no security certificate, and no capacity guarantee claimed
      outside the owning protocol.

An `open` item on a critical path blocks handoff. A `not-met` item is fixed or the design
returns to the loop — it is never relabeled as a follow-up to avoid the fix.

## Anti-patterns

- **Designing before requirements exist** — components chosen first, rationale invented
  after.
- **Hand-waving numbers** — "it will scale", "storage is cheap", with no arithmetic and
  no assumption.
- **A single-option "comparison"** — two columns that differ only in name, or no
  do-nothing baseline.
- **Cargo-culting a product's architecture** — copying a hyperscaler topology for a
  workload three orders of magnitude smaller.
- **Ignoring failure modes** — the happy path only, with retries assumed to be free and
  duplicates assumed not to happen.
- **Designing the whole system at deep-dive depth** — gold-plating every component
  instead of the risky two.
- **Restating other protocols** — repeating UI rules, security thresholds, or scope
  reduction here instead of linking them.
- **Treating the estimate as a guarantee** — quoting an order-of-magnitude figure as a
  capacity commitment.

## Cross-references

- [`design-doc-template.md`](./design-doc-template.md) — the document skeleton for the
  high-level design and deep dive.
- [`capacity-estimate-template.md`](./capacity-estimate-template.md) — the estimation
  worksheet the second stage fills in.
- [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md) — the option comparison
  and reversibility instrument used by the trade-offs stage.
- [`system-design-primitives.md`](./system-design-primitives.md) — order-of-magnitude
  anchors for latency, throughput, and storage.
- [`adr-template.md`](./adr-template.md) — the decision record each load-bearing choice
  emits.
- [`prompt-pipeline.md`](./prompt-pipeline.md) — owns scope reduction and the hot-spot
  test that feeds the loop's scope stage.
- [`orchestrate.md`](./orchestrate.md) — owns seat cadence, delegation, and when the loop
  runs inside a larger delivery.
- [`ui-design.md`](./ui-design.md) — owns every UI surface; this protocol stops at the
  system boundary.
- [`security-review.md`](./security-review.md) — owns security findings and the boundary
  gate; a security-class concern leaves this loop and is routed there.
- [`owasp-analysis.md`](./owasp-analysis.md) — owns the threat-model analysis behind a
  security certification; this protocol never issues one.
- [`broad-investigation-template.md`](./broad-investigation-template.md) — used before
  the loop when the inputs themselves are unknown.
