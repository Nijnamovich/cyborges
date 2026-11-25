# Catalog: System Design Primitives

> Concepts distilled from liquidslr/system-design-notes, which summarizes "System Design Interview" by Alex Xu (Vol 1, Vol 2 2nd ed). No text, diagrams, or code from the source is reproduced. Chapter links are provided for reference only.

## How to use this catalog

This catalog is an **offline fallback**. Use it when the external
`system-design-notes` reference cannot be fetched during a review or design
task; the fetch-and-verify rules live in
[`external-knowledge-ingestion.md`](./external-knowledge-ingestion.md), and when
the reference is reachable its chapter content outranks this summary.

Each chapter is one entry holding a concept plus the contract it implies —
never a retelling of the source. Read the entry, then state the decision and
its failure mode in your own design document; cite the chapter link only as a
pointer for a human who wants the long form. Do not quote this catalog as if it
were the book, and do not treat a missing entry as permission to improvise
requirements.

Pick the cluster that matches the question: scale reasoning, a reusable
distributed component, a high-fan-out product surface, or a money/state
workflow. Membership is fixed, one entry per chapter, and cross-cluster
dependencies (for example a feed built on a message queue) are expected.

## Method and scale foundations

### 01 — Scaling

- **Problem:** One machine saturates before demand stops growing, so capacity has to grow without rewriting the system.
- **Contract:** Throughput and storage scale with added nodes while no single node remains a hard bottleneck.
- **Use:** Stateless request tiers, read replicas, and partitioned storage. **Do not use:** Workflows whose correctness depends on one serialized actor.
- **Common failure mode:** Adding nodes to a tier that shares one database moves the bottleneck rather than removing it, so throughput stays flat.

### 02 — Back-of-the-envelope Estimation

- **Problem:** Architectural choices need magnitudes before any prototype or load test exists.
- **Contract:** Every capacity claim is an explicit arithmetic chain from traffic and payload assumptions to QPS, storage, bandwidth, and node count.
- **Use:** Scoping, shard sizing, and cost ceilings. **Do not use:** As evidence of measured behaviour.
- **Common failure mode:** An unstated peak-to-average multiplier or a unit slip turns a defensible estimate into an answer off by orders of magnitude.

### 03 — System Design Framework

- **Problem:** Open-ended design prompts invite structureless answers that skip constraints and hide tradeoffs.
- **Contract:** A fixed sequence — requirements, estimates, API, data model, high-level design, deep dives — records each decision together with the alternative it rejected.
- **Use:** Design reviews and interview-style walkthroughs. **Do not use:** As a substitute for domain research.
- **Common failure mode:** Skipping scope and non-functional requirements produces a generic diagram that satisfies no concrete constraint.

## Distributed building blocks

### 04 — Rate Limiter

- **Problem:** Clients can exceed a fair or safe request volume, whether by bug, retry storm, or abuse.
- **Contract:** Admitted request rate stays under a configured limit per key with bounded burst; token bucket absorbs bursts, sliding-window counters smooth the long-run rate.
- **Use:** Protecting shared backends, per-tenant quotas, abuse control. **Do not use:** As an authorization mechanism.
- **Common failure mode:** Per-instance counters behind a load balancer multiply the effective limit, and fixed windows admit double the burst at each boundary.

### 05 — Consistent Hashing

- **Problem:** Modulo hashing remaps almost every key whenever the node set changes, forcing a full cache or data migration.
- **Contract:** Adding or removing a node moves only about 1/N of keys, and a given key resolves to the same node for the same ring state.
- **Use:** Cache placement and shard assignment where resizing must be cheap. **Do not use:** When keys need strict range ordering.
- **Common failure mode:** Too few virtual nodes leave an uneven ring, so one node takes a disproportionate share and rebalancing moves a hot spot rather than spreading it.

### 06 — Key-Value Store

- **Problem:** Low-latency get and put must survive a data set larger than one node and failures of individual nodes.
- **Contract:** Reads and writes resolve through partitioning plus replication plus quorum, so R + W > N yields read-your-write consistency on a key.
- **Use:** Session state, feature flags, and metadata lookups. **Do not use:** Multi-key transactions or ordered range scans.
- **Common failure mode:** Ignoring quorum overlap across a partition serves stale values, and lagging repair with resurrected tombstones brings deleted keys back.

### 07 — Unique-Id Generator

- **Problem:** A central sequence does not survive distribution, and coordination per id adds a round trip to every write.
- **Contract:** Ids are unique across nodes without coordination, roughly time-ordered, and fit a 64-bit key; a Snowflake-style layout packs timestamp, node/worker bits, and a per-millisecond sequence.
- **Use:** Primary keys and event identifiers. **Do not use:** As secrets, or where strict gapless ordering is required.
- **Common failure mode:** Clock rollback reissues ids from the past and collides with existing rows; worker-id reuse after rescheduling is the other classic collision.

### 08 — URL Shortener

- **Problem:** Long URLs are unwieldy in messages, print, and character-limited channels.
- **Contract:** A short token maps to exactly one target, and resolution is a single lookup served mostly from cache; ids come from base62 encoding or a counter/key-generation service.
- **Use:** Link sharing and click attribution. **Do not use:** As durable archival of the destination.
- **Common failure mode:** Sequential tokens expose volume and permit enumeration; a redirect path with no cache or negative cache turns every hit into a database read.

### 09 — Web Crawler

- **Problem:** The web is unbounded, adversarial, and sensitive to how fast a single host is hit.
- **Contract:** Each URL is fetched at most according to policy, duplicates are suppressed after normalization, and per-host politeness limits are respected.
- **Use:** Index building and freshness monitoring. **Do not use:** As an unbounded scraper of private or disallowed content.
- **Common failure mode:** Normalization gaps (fragments, casing, query order) explode the frontier with duplicates, while spider traps and missing per-host backoff get the crawler blocked.

### 10 — Notification System

- **Problem:** Many channels and many recipients must each receive a message once, without spam or duplicate sends.
- **Contract:** Each event produces one delivery per user per enabled channel, governed by preferences, with retries that do not duplicate.
- **Use:** Transactional and campaign messaging. **Do not use:** Real-time bidirectional control traffic.
- **Common failure mode:** Retry without an idempotency key double-sends, and write-time fan-out collapses the queue when a single event targets millions of users.

### 19 — Distributed Message Queue

- **Problem:** Producers and consumers scale and fail independently, so a direct call couples their availability and rate.
- **Contract:** Published messages are retained durably, delivered at least once, and ordered per partition key; consumer groups split partitions and expose lag for backpressure.
- **Use:** Asynchronous work, event pipelines, load leveling. **Do not use:** As a drop-in replacement for synchronous RPC.
- **Common failure mode:** Unbounded lag with no backpressure fills disks, and group rebalancing mid-batch redelivers work that non-idempotent handlers apply twice.

### 20 — Metrics Monitoring and Alerting System

- **Problem:** Thousands of time series must be ingested cheaply and evaluated continuously for conditions worth waking someone.
- **Contract:** Each series is queryable by name plus labels over a retention window, and alert rules evaluate on a defined interval with a sustained-for condition.
- **Use:** SLO tracking, saturation and error-rate signals. **Do not use:** Per-user audit trails.
- **Common failure mode:** High-cardinality labels such as user or request id blow up the index, and alerting on raw spikes without a for-window produces pager storms.

## Product-scale patterns (high fan-out and real time)

### 11 — News Feed System

- **Problem:** Rendering a merged timeline at read time is expensive once each user follows many authors.
- **Contract:** A user's feed is available within a bounded latency and reflects followed authors within an agreed staleness bound.
- **Use:** Social timelines and activity streams. **Do not use:** When strict global ordering is required.
- **Common failure mode:** Pure push explodes writes for high-follower accounts while pure pull is slow for heavy readers; the hybrid must age out inactive users or it keeps doing both.

### 12 — Chat System

- **Problem:** Two participants may sit behind different gateways with intermittent connectivity and multiple devices.
- **Contract:** Messages are ordered per conversation, persisted before acknowledgement, and delivery/read receipts are observable to the sender.
- **Use:** One-to-one and group messaging. **Do not use:** As a durable audit log without a retention policy.
- **Common failure mode:** Treating an open TCP connection as presence, or fanning out to devices without per-conversation sequence numbers, yields false online states and out-of-order duplicates.

### 13 — Search Autocomplete

- **Problem:** Prefix suggestions must return in single-digit milliseconds over a vocabulary far larger than memory-friendly lists.
- **Contract:** Top-k completions for a prefix come from a prefix index — typically a trie or precomputed prefix table — with bounded staleness and stable ranking.
- **Use:** Search boxes and command palettes. **Do not use:** As full-text search.
- **Common failure mode:** Rebuilding the trie on every write, or blending unbounded personalization and trending terms, makes the index a hot spot that misses the latency budget.

### 14 — Youtube

- **Problem:** Uploads are large and heterogeneous, and playback is global and bandwidth-constrained.
- **Contract:** An uploaded asset becomes playable at several bitrates within a bounded processing time and is served from edge caches via adaptive bitrate.
- **Use:** Large-scale video delivery. **Do not use:** For tiny assets where transcoding overhead dominates.
- **Common failure mode:** A transcode pipeline that fails midway without a resumable state machine orphans uploads, and long-tail cache misses push egress back to origin.

### 16 — Proximity Service

- **Problem:** "What is near me" must be answered over millions of points without scanning them.
- **Contract:** A radius query returns every candidate within distance d, with no false negatives, in time bounded by the spatial index rather than data size.
- **Use:** Store locators and point-of-interest search. **Do not use:** Continuous location tracking.
- **Common failure mode:** Prefix-only geohash search misses neighbours across cell boundaries, while an unindexed or unbounded result set degrades to a full scan.

### 17 — Nearby Friends

- **Problem:** Location is high-frequency, ephemeral, and privacy-sensitive, so storing every ping forever is both costly and wrong.
- **Contract:** A user sees friends inside a radius as of a bounded TTL, and positions never outlive their expiry.
- **Use:** Opt-in social proximity features. **Do not use:** Safety-critical tracking.
- **Common failure mode:** Fan-out on every location update amplifies writes, and expired entries left in the index produce phantom friends who are no longer there.

### 18 — Google Maps

- **Problem:** Global map rendering and routing must be fast, consistent across zoom levels, and tolerant of stale or partial data.
- **Contract:** Tiles are addressable by (zoom, x, y) and served from a precomputed pyramid, while routes minimise a cost function over a versioned road graph.
- **Use:** Map display and navigation. **Do not use:** As the authority for live dispatch decisions.
- **Common failure mode:** Pre-rendering every zoom wastes storage, and traffic data fused without versioning yields routes that are optimal in the graph yet wrong on the road.

## Correctness-first patterns (money, ledgers, stateful pipelines)

### 15 — Google Drive

- **Problem:** Files must be stored once, versioned, and synchronised across clients that go offline for long periods.
- **Contract:** Content is chunked and immutable per version, metadata is authoritative, and concurrent edits resolve deterministically with a replayable change cursor.
- **Use:** File sync and collaboration. **Do not use:** As a low-latency database for small records.
- **Common failure mode:** Whole-file last-writer-wins silently discards edits, and a non-monotonic sync cursor replays or skips changes after a long offline period.

### 21 — Ad Click Event Aggregation

- **Problem:** Click events arrive late, duplicated, and heavily skewed toward a few campaigns.
- **Contract:** Per-ad per-window aggregates reconcile to a billing-grade total with bounded error and no double counting.
- **Use:** Billing and campaign reporting. **Do not use:** Real-time bidding decisions.
- **Common failure mode:** Hot campaign keys overwhelm one aggregator shard, and late or duplicated events without event-time windows and dedupe inflate recorded spend.

### 22 — Hotel Reservation System

- **Problem:** Many users race for the same room over overlapping date ranges.
- **Contract:** A confirmed booking never pushes a room-night past its inventory, and the client learns success or failure atomically.
- **Use:** Inventory-constrained booking. **Do not use:** High-volume catalog browsing reads.
- **Common failure mode:** Check-then-write without a conditional or locked update oversells, and cached availability without invalidation shows rooms that are already gone.

### 23 — Distributed Email Service

- **Problem:** Delivery crosses untrusted peers that retry, delay, and occasionally lie.
- **Contract:** A message is accepted once by message id, queued durably, retried per recipient, and filtered before inbox placement.
- **Use:** Store-and-forward messaging. **Do not use:** As a real-time channel.
- **Common failure mode:** Retry loops without an idempotency check create duplicate deliveries, and synchronous spam scanning on ingest makes the queue back up precisely during an attack.

### 24 — S3-like Object Storage

- **Problem:** Large immutable objects must be durable and cheap at a scale where disks fail routinely.
- **Contract:** An object is readable after a successful put, and durability survives node and disk loss within the stated SLA via replication or erasure coding.
- **Use:** Backups, media, and data lakes. **Do not use:** Workloads needing in-place random writes.
- **Common failure mode:** Metadata and blob stores diverge, leaving listings that point at missing data, while small objects waste space and IOPS without packing.

### 25 — Real-time Gaming Leaderboard

- **Problem:** Ranking millions of players by a fast-changing score must stay responsive to both top-k reads and single-player rank lookups.
- **Contract:** Top-k and a player's rank are queryable within a bounded latency after each score update, with deterministic tie-breaking.
- **Use:** Competition boards and rankings. **Do not use:** Financial settlement or payouts.
- **Common failure mode:** A single sorted set becomes a write hot spot, and rebuilding ranks from raw events on read is too slow; snapshots without event replay lose tie-break consistency.

### 26 — Payment System

- **Problem:** Money movement must never double-apply when clients, services, or networks retry.
- **Contract:** Each payment intent produces exactly one ledger effect, enforced by an idempotency key plus an explicit state machine.
- **Use:** Charges, refunds, and payouts. **Do not use:** Best-effort fire-and-forget flows.
- **Common failure mode:** A downstream charge succeeds while the local write fails, so a retry bills twice without idempotency; out-of-order transitions corrupt state.

### 27 — Digital Wallet

- **Problem:** Stored balances must be provable, internally consistent, and auditable under concurrent debits.
- **Contract:** Every balance change is one side of a balanced double-entry posting, and the balance equals the sum of its ledger entries.
- **Use:** Stored value and internal transfers. **Do not use:** Raw high-frequency throughput without batching.
- **Common failure mode:** Mutating a balance row directly destroys auditability, and concurrent debits without serializable or locked semantics allow negative balances.

### 28 — Stock Exchange

- **Problem:** Price discovery must stay deterministic and fair under burst load from many participants.
- **Contract:** Each inbound order is sequenced once, matched by a deterministic engine over a price-time priority book, and market data reflects that same total order.
- **Use:** Electronic order books and matching. **Do not use:** Eventually consistent stores for matching state.
- **Common failure mode:** Non-deterministic matching diverges on replay after failover, and missing admission control lets one participant flood the book and starve everyone else.

## Cross-references and attribution

- [`system-design-review.md`](./system-design-review.md) — runs the review that consumes these primitives as checkpoints.
- [`design-tradeoff-analysis.md`](./design-tradeoff-analysis.md) — turns each contract and failure mode here into a weighed tradeoff.
- [`external-knowledge-ingestion.md`](./external-knowledge-ingestion.md) — defines when this offline fallback is used and how external facts are verified.
- [`capacity-estimate-template.md`](./capacity-estimate-template.md) — structures the arithmetic required by chapter 02.
- [`design-doc-template.md`](./design-doc-template.md) — the document shape that cites primitives by chapter number.