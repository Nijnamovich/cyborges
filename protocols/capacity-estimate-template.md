# Template: Capacity Estimate

Fill-in back-of-the-envelope worksheet. Assumptions first, arithmetic second, ranges in the report — order-of-magnitude only.

## Purpose

This is the capacity worksheet used by [`system-design-review.md`](./system-design-review.md): it turns a design's inputs into peak QPS, storage growth, bandwidth, cache size, and fan-out so scale errors surface before implementation. It is not a benchmark and not a forecast; it is a set of estimates whose assumptions must be visible.

## Inputs and assumptions

Every number is either **sourced** or **labelled an assumption**. An unsourced number is a defect.

| Input | Value | Source | Confidence |
|---|---|---|---|
| Daily active users (DAU) | [value] | [product metric / assumption] | [high / medium / low] |
| Actions per user per day | [value] | [analytics / assumption] | [—] |
| Read : write ratio | [value] | [traffic sample / assumption] | [—] |
| Peak factor | [value] | [observed diurnal ratio / assumption] | [—] |
| Request payload size | [value] | [schema / sample] | [—] |
| Response payload size | [value] | [schema / sample] | [—] |
| Bytes per stored row | [value] | [schema estimate] | [—] |
| Retention | [value] | [policy / requirement] | [—] |
| Replication factor | [value] | [topology] | [—] |
| Hot-data fraction | [value] | [access sample / assumption] | [—] |
| Fan-out (followers, consumers, subscribers) | [value] | [product model / assumption] | [—] |

- State units in every row; derive nothing in this table.
- Confidence is `high` only for measured production values.

## Estimation worksheet

### Traffic

- `avg QPS = DAU × actions/user/day ÷ 86,400`
- `peak QPS = avg QPS × peak factor`
- `read QPS = peak QPS × read ratio`, `write QPS = peak QPS × write ratio`
- **Micro-example:** 2M DAU × 10 actions ÷ 86,400 ≈ **231 QPS** average; ×3 peak ≈ **700 QPS**; at 9:1 reads ≈ 630 read QPS and 70 write QPS.

### Storage

- `rows/day = DAU × writes/user/day`
- `raw bytes/day = rows/day × bytes/row`
- `stored = raw bytes/day × retention days × replication factor × index overhead`
- **Micro-example:** 2M × 5 writes = 10M rows/day × 1 KB = **10 GB/day**; ×365 days × 3 replicas ≈ **11 TB/year** before index overhead (~1.3× ≈ 14 TB).

### Bandwidth

- `ingress bytes/s = write QPS × request bytes`
- `egress bytes/s = read QPS × response bytes`
- `monthly egress = egress bytes/s × ~2.6M s/month`
- **Micro-example:** 70 write QPS × 10 KB ≈ **0.7 MB/s ingress**; 630 read QPS × 50 KB ≈ **31 MB/s egress** (~250 Mbps), which is what drives egress cost.

### Cache

- `working set = hot fraction × total dataset`
- `cache memory = working set × per-entry overhead` (typically 1.3–2×)
- `database QPS after cache = read QPS × (1 − hit-ratio target)`
- **Micro-example:** 14 TB total × 5% hot = **700 GB** working set; ×1.5 overhead ≈ **1 TB** RAM; at 90% hit ratio, 630 read QPS falls to ~63 QPS at the database.

### Fan-out

- `fan-out writes/s = source writes/s × fan-out`
- `read amplification = reads × per-request fan-out`
- `delivery capacity = fan-out writes/s × peak factor`
- **Micro-example:** 1,000 posts/s × 500 followers = **500k deliveries/s** at peak 3× → 1.5M/s; this usually breaks the design, so compare push-on-write against pull-on-read before choosing.

## Sanity constants

Approximate values for mental arithmetic — not exact, and not a substitute for the worksheet.

| Constant | Value | Use |
|---|---|---|
| Seconds per day | 86,400 | daily volume → average QPS |
| 1M per day | ≈ 12 QPS | quick daily-to-QPS check |
| 1 KB × 1M | = 1 GB | payload sizing |
| 1 MB/s | ≈ 8 Mbps | bandwidth sanity |
| 1M seconds | ≈ 11.6 days | window arithmetic |
| Typical peak factor | 2–5× | average → peak |
| Typical index and overhead | 1.2–2× | raw bytes → stored bytes |
| Seconds per month | ≈ 2.6M | egress and cost math |

## Sensitivity and reporting

- **Elasticity:** change each input by ±2× and record which one moves the result across a design threshold (a shard, a tier, a queue). That input is the one to measure first.
- **Ranges:** report low / expected / high, not one number; a single figure hides the uncertainty the worksheet exists to expose.
- **Labelling:** every reported figure is `measured` (production or benchmark), `estimated` (derived here), or `assumed` (chosen arbitrarily). Mixed provenance in one sentence is a defect.
- **Precision:** round prose to one significant figure; keep exact values in the worksheet.
- **Contradiction check:** if an estimate differs from a measured number by more than 10×, stop and find the error before the design proceeds.

## Cross-references

- [`system-design-review.md`](./system-design-review.md) — consumes this worksheet at the estimation gate.
- [`design-doc-template.md`](./design-doc-template.md) — the design doc's Estimation section links this file.
- [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md) — options are scored partly on the cost and scale figures produced here.
- [`system-design-primitives.md`](./system-design-primitives.md) — the building blocks whose limits these estimates are checked against.
- [`prompt-pipeline.md`](./prompt-pipeline.md) — scope reduction that keeps an estimate to the inputs that matter.
