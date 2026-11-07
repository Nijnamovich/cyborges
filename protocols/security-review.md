# Protocol: Security Review

> Attribution: procedural inspiration from Cloudflare's security-review skill (MIT; no code copied), boundary/severity discipline informed by QwenLM/Qwen-Live-Harness (Apache-2.0; prose disciplines only), minimalism ideas from IagoLast/files (no text copied). See `## Credits` in `readme.md`.
## 1. Scope and mode
Security review is **guidance by default** and a **full audit only on an explicit human or project request**. The mode is a recorded OUTPUT of Phase 2 (Reduce) — never a new classification step at turn entry. The interpreter-first gate and the "never classify before Step 0" rule are unchanged; a full audit is a checklist scope, not a different pipeline.
## 2. Non-negotiables
- **Source-read-only — NEVER execute target code.** This repo has no sandbox and the reviewer inherits the global `shell: allow` permission. Read, grep, and reason; never run the target's builds, tests, scripts, binaries, or package managers.
- **No finding without `path:line`; no severity without demonstrated impact.** A possible bug is a candidate, not a finding.
- **Never stop mid-phase**, and **"no finding" is a valid result.**
## 3. Boundary gate
A finding must answer all six, in order:

1. **Lower-trust principal** — who acts with less trust than the system?
2. **Accepted input or action** — what exactly do they control?
3. **Intended control** — which check or permission is supposed to stop them?
4. **Crossed boundary** — where does that control fail?
5. **Affected principal or resource** — whose data or capability is exposed?
6. **Concrete result** — what is observed, or observable by the owner?

**Reject** any candidate that is: a missing best practice with no control bypass; guessed deployment behavior; a generic parser crash without boundary crossing; same-principal self-impact; defense-in-depth advice with no boundary violation; or a re-report of a prior finding.
## 4. Verdicts
- **confirmed** — the boundary gate is satisfied and impact is demonstrated.
- **needs_validation** — a named fact remains unresolved; state the exact fact and give **no severity**.
- **rejected** — name the gate question that failed.
## 5. Severity
Severity = likelihood × impact, with five anchors:

| Anchor | Meaning |
|---|---|
| critical | Unauthenticated code execution, full data-store access, or takeover of arbitrary accounts. |
| high | Auth bypass, cross-tenant read/write, stored script execution, authenticated code execution, or unauthenticated remote stop of a shared service. |
| medium | A control is weakened for an action with limited blast radius. |
| low | Hardening gap with no demonstrated bypass. |
| info | Observation only. |

**Discriminator:** does it fully defeat an explicit control for an action with real consequences, or only weaken it? Overall severity cannot exceed the demonstrated impact.
## 6. Mapping to ReviewerOutput
- Security severity maps to `critical` | `warning` | `info` in `issues[].severity`.
- Return `verdict: block` only for a demonstrated boundary violation.
- Carry confirmed / needs_validation / rejected in the issue or summary prose.
- **No schema change**: `agents/reviewer.schema.json` is untouched.
## 7. Coverage ledger
| Status | Meaning |
|---|---|
| covered | Checked; result recorded. |
| candidate | Suspicious; not yet verified. |
| not_applicable | The class cannot occur here. |
| out_of_scope | Deliberately excluded. |
| blocked | Could not check; say why. |

**The ledger is the coverage claim.** A partial or scoped review must say so; silence is not coverage.
## 8. Attack classes
| Class | Ask |
|---|---|
| Access control / authz | Can a principal act on another's resource? |
| Injection / input | Does untrusted input reach an interpreter, query, or shell? |
| Secrets / crypto | Is a secret exposed, or crypto misused? |
| Resource exhaustion | Can input make cost unbounded? |
| Supply chain / release | Can an attacker influence what ships or runs? |
| Business logic / state | Can a valid sequence produce an invalid state? |
| Data lifecycle / privacy | Is data retained, logged, or exposed beyond intent? |
| Agent / MCP / model trust | Can fetched content or a tool become instructions? |

## 9. Obvious things to grep
- Hardcoded secrets, tokens, keys, and connection strings.
- `eval`, `exec`, `child_process`, or shell templates built from input.
- Missing authorization on a route or handler.
- SQL / NoSQL string concatenation.
- Permissions widened (`allow` / `*`) without a matching need.
- Logs that print tokens, headers, or personal data.
## 10. Anti-patterns
- A checklist deviation reported as a vulnerability.
- Defense-in-depth advice with no boundary violation.
- Executing in a live or shared environment.
- Guessing deployment behavior instead of reading configuration.
- Assigning severity to an unverified candidate.
- Reporting before verification is complete.
## Cross-references
[`agents/reviewer.md`](../agents/reviewer.md) · [`broad-investigation-template.md`](./broad-investigation-template.md) · [`subagent-return-check.md`](./subagent-return-check.md) · [`orchestrate.md`](./orchestrate.md)
