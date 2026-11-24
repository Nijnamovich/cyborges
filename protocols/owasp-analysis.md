# Protocol: OWASP Application Analysis

## 1. Scope and mode

Application analysis against the **OWASP** body of knowledge: enumerate the
application's attack surface, map it to the OWASP framework that matches its
shape, and turn each applicable check into evidence-backed findings.

This protocol **extends** [`security-review.md`](./security-review.md); it does
not replace it. `security-review.md` owns the boundary gate, verdicts, severity
anchors, coverage ledger and output mapping — this file only adds the OWASP
category taxonomy and the surface-to-framework selection. Mode is guidance by
default and a full audit only on an explicit human or project request; the mode
stays a recorded OUTPUT of Phase 2 (Reduce), never a turn-entry classification
step.

## 2. Non-negotiables

The authority is [`security-review.md`](./security-review.md) §2; the summary
below is subordinate to it.

- **Source-read-only — never execute target code.** This repo has no sandbox and
  the reviewer inherits the global `shell: allow` permission; never run the
  target's builds, tests, scripts, binaries or package managers.
- **No finding without `path:line`; no severity without demonstrated impact.** A
  possible bug is a candidate, not a finding.
- **Never stop mid-phase**, and **"no finding" is a valid result.**

Additional to this protocol:

- **The framework edition is pinned, never implied.** State the OWASP release in
  the report header, including the date the edition was checked, and never mix
  editions silently. Baseline here is **OWASP Top 10:2021**, current at this
  protocol's authoring (2026-11); re-pin it and bump that date when OWASP
  publishes the next release.
- **A category is not a finding.** Passing a checklist row is evidence, not a
  verdict; the boundary gate still decides.

## 3. Surface → framework selection

Pick the framework(s) that match what the application actually exposes, and
record the choice in the coverage ledger.

| Application shape | Primary framework | Add when |
|---|---|---|
| Web app / SPA + HTTP backend | OWASP Top 10 (web) | Auth-heavy → ASVS L2 |
| REST / GraphQL / gRPC API | OWASP API Security Top 10 | Object-level authz → BOLA / BOPLA checks |
| Mobile client (iOS / Android) | OWASP MASVS | Server side still gets Top 10 |
| Service-to-service / agent / MCP | Top 10 (web) | Supply chain → A06 / A08; trust → [`security-review.md`](./security-review.md) §8 |
| Library / SDK | OWASP Top 10 (consumer-facing surface only) | ASVS L1 optionally, as an app-side floor |

If the shape is ambiguous, analyze the union of the candidate frameworks and
say so; never narrow the surface silently.

## 4. OWASP Top 10 (web) — analysis matrix

Baseline: **OWASP Top 10:2021** (see §2 for the re-pin rule).

| ID | Category | What to inspect | Evidence that closes the row |
|---|---|---|---|
| A01 | Broken Access Control | Route / handler authorization, IDOR, forced browsing, tenant scoping, CORS¹ | Observed missing check at `path:line`, or an explicit deny path |
| A02 | Cryptographic Failures | In-repo password hashing, key storage, weak or rolled crypto; TLS served by a deployment or provider is out of repo scope → `blocked` | Sink or config at `path:line` |
| A03 | Injection | SQL / NoSQL / OS / LDAP / template, deserialization, XSS sinks | Untrusted input reaching an interpreter at `path:line` |
| A04 | Insecure Design | Threat-model gaps, missing rate limits, business-logic abuse | Reachable abuse path with a real consequence |
| A05 | Security Misconfiguration | Default credentials, debug on, verbose errors, permissive CORS / headers, exposed admin | Config file at `path:line` |
| A06 | Vulnerable & Outdated Components | Dependency manifests, lockfiles, pinned versions, known CVEs | Manifest at `path:line` + affected range **only when a locally available advisory source proves it**; otherwise `blocked` (no severity). Never cite a CVE from memory. |
| A07 | Identification & Auth Failures | Session handling, MFA, credential recovery, token validation | Auth-flow weakness at `path:line` |
| A08 | Software & Data Integrity Failures | CI/CD trust, unsigned artifacts, insecure deserialization, update channels | Pipeline / integrity gap at `path:line` |
| A09 | Logging & Monitoring Failures | Auth and security events logged, alerting, audit trail | Missing log site, or PII in logs, at `path:line` |
| A10 | SSRF | Server-side fetches of user-controlled URLs, allowlists, metadata endpoints | Fetch sink with a user-controlled target at `path:line` |

¹ **CORS is dual-listed by OWASP.** Primary ID is **A05** (misconfiguration);
cite **A01** only when the demonstrated consequence is object-level access to
another principal's resource. File it once, under the primary ID.

Each row's status goes into the ledger as `covered` / `candidate` /
`not_applicable` / `out_of_scope` / `blocked` — ledger semantics are
[`security-review.md`](./security-review.md) §7.

## 5. Companion standards (use when applicable)

Each companion is **pinned** like the Top 10 (§2); name the edition in the
report header.

- **OWASP ASVS** — verification requirements by assurance level (v5.0 current;
  v4.0.3 still common — pin whichever the project targets). Map each applicable
  requirement to a ledger status and cite the ASVS chapter in the finding prose.
  Never claim a level is met without a row per requirement.
- **OWASP API Security Top 10:2023** — for API surfaces. API1:2023 (BOLA,
  object-level authz) and API3:2023 (BOPLA, property-level) are the most frequent
  object-level findings; check them before the rest.
- **OWASP MASVS** — pin the edition. v2.0 categories: STORAGE / CRYPTO / AUTH /
  NETWORK / PLATFORM / CODE / RESILIENCE / PRIVACY (v1.4 used a different set;
  say which you are using).
- **OWASP WSTG / Cheat Sheets** — test *ideas* only; never execute a live test
  (source-read-only stands).
- **OWASP Dependency-Check / CycloneDX SBOM** — evidence source for A06.
  Reading a generated SBOM is allowed; generating one requires running the
  target (forbidden here — mark the row `blocked`).

## 6. Turning a category into a finding

1. Locate the surface element (route, sink, config, manifest) and record
   `path:line`.
2. Apply the boundary gate from [`security-review.md`](./security-review.md) §3.
3. Assign a verdict (`confirmed` / `needs_validation` / `rejected`) per §4 —
   **not** by checklist compliance.
4. Assign severity via the §5 anchors only when the gate is satisfied.
5. Map to `ReviewerOutput` per §6, and cite the OWASP ID (e.g. `A03`) in the
   issue message so findings stay deduplicable.

A checklist row that is "present" but has no demonstrated boundary violation is
`covered`, not `confirmed`.

## 7. Coverage ledger (OWASP variant)

Seed one ledger row per applicable category **before** analysis; update status
as you go. The ledger is the coverage claim: a partial analysis must say which
categories were not reviewed. Statuses and meaning are exactly
[`security-review.md`](./security-review.md) §7.

The report header must state: framework + edition (and check date), application
shapes analysed, and every `not_applicable` / `out_of_scope` category with a
one-line reason.

## 8. Anti-patterns

1. Checklist compliance reported as a vulnerability — or as a clean bill of
   health.
2. Mixing OWASP editions without pinning one.
3. Running a web Top 10 against an API surface (or vice versa) without saying so.
4. Running scanners, Dependency-Check, or WSTG active tests against the target —
   forbidden; mark the row `blocked`.
5. Assigning a Top 10 ID to a finding the boundary gate rejected.
6. Claiming an ASVS level without per-requirement rows.
7. Silent surface narrowing (skipping MASVS on a mobile app, or skipping the API
   Top 10 on an API).
8. Re-reporting one root cause under several OWASP IDs — dedupe, cite the
   primary ID.
9. Citing a CVE or advisory from memory instead of a locally available source.

## Cross-references

[`security-review.md`](./security-review.md) ·
[`agents/reviewer.md`](../agents/reviewer.md) ·
[`agents/orchestrator.md`](../agents/orchestrator.md) ·
[`broad-investigation-template.md`](./broad-investigation-template.md) ·
[`subagent-return-check.md`](./subagent-return-check.md) ·
[OWASP Top 10](https://owasp.org/Top10/)
