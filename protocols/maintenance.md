# Protocol: Maintenance

Periodic, on-demand maintenance audit of a **target project repository** — not of the
agent-system install. Seven named phases, each owned by a seat, each with a fixed
status vocabulary, ending in one consolidated report. **Read-only by default: this
protocol reports and proposes; it never mutates anything without explicit,
per-item human authorization.**

> This protocol never targets the agent-system repository itself (the install
> resolved from the `agent-system` reference in `opencode.json`). Retargeting it
> there requires an explicit operator instruction, and even then it must not create
> a global `docs/`.

## 1. Scope and mode

- **In scope:** the repository the session is working in — code comments, dependency
  manifests, linter configuration, `docs/`, local branches, and repository hygiene.
- **Out of scope:** builds, dev servers, test suites, deployments, and anything that
  writes to the working tree, the index, the lockfile, refs, or a registry.
- **Mode:** `read-only` is the only mode this protocol defines. Remediation is a
  *normal change cycle* (a fresh prompt through
  [`prompt-pipeline.md`](./prompt-pipeline.md)), executed by `coder` / `documenter`
  against the authorized items of the report.
- **Invocation path:** the run enters through the normal turn — `interpreter` (Step 0,
  [`dispatch.md`](./dispatch.md)) → `delivery` routes the non-trivial run →
  `orchestrator` (Phase 2 scope + seat assignment) → the phase seats → consolidated
  report → `delivery`. A maintenance run never bypasses Step 0. Every child return
  passes through [`subagent-return-check.md`](./subagent-return-check.md).

## 2. Language rule — English only (mandatory)

> **RULE — ENGLISH ONLY.** Every artefact **this protocol produces** is written in
> **English**: the consolidated report, every finding and rationale, every proposed
> commit message, every proposed branch name, and every code comment named in a
> candidate list. This is a standing human requirement of the agent system, not a
> per-project style choice. A non-English artefact from this protocol is a defect to
> fix, not a preference to debate.
>
> **Project documentation content is the one exception, and it is not governed here:**
> doc content follows `docs/project.md` → `doc_language`
> ([`agents/documenter.md`](../agents/documenter.md) → Rules). The report proposes such
> edits in English; the edit itself is written in the project's doc language.
> **Code comments are always in ENGLISH** — that is also its own checklist item in
> Phase 1 (§8), so a non-English comment is reported as a minimization candidate with
> that class.

## 3. Non-negotiables

1. **Read-only default; never unattended mutation.** No dependency install, update,
   bump, or lockfile regeneration; no `--fix` / `format` / `--write`; no comment edits
   or deletions; no `git branch -D`, no remote branch deletion, no tag or release
   changes; no `git fetch --prune`, `gc`, `prune`, `reset`, `checkout --`, `clean`, or
   stash manipulation; no doc rewrites or file moves.
2. **Authorization starts a new cycle, never a mutation inside this run.** Nothing in
   this protocol writes, deletes, or installs. An authorized follow-up is executed as a
   fresh change cycle ([`prompt-pipeline.md`](./prompt-pipeline.md)) by
   `coder` / `documenter` against that one item; approval of one item never covers the
   next, and this run ends at the report regardless of approvals.
3. **No-running-while-busy guard.** If the working tree is dirty, or another session,
   agent handoff, or watcher is active in the repository, the run reports `blocked`
   and **stops** — it does not race edits (§4).
4. **Fail-closed discovery.** Unknown tooling is `not_applicable` or `blocked`, never
   `pass`. Never install a tool to make a check runnable. Never read absence as
   cleanliness: no linter is not a clean lint; no docs script is not matching docs.
5. **Evidence or silence.** Every row carries the command that produced it and a short
   output excerpt. A command that did not run is never reported as run
   ([`subagent-return-check.md`](./subagent-return-check.md) → "Receipt ≠ completion").
6. **No network assumptions.** Registry-dependent checks are optional; offline or
   unauthenticated → `blocked`. Never send credentials or tokens to a registry.
7. **Report-only for secrets.** A secret-like finding reports the `path:line` and the
   pattern class only — never the value, never a masked variant long enough to
   reconstruct it, and never a live test against the issuing service.
8. **One run, one report.** Phases are independent: a phase that is `blocked` or
   `not_applicable` records that status and the run continues. Only a precondition
   failure (§4) stops the run.

## 4. Preconditions and the busy guard

Run these gates in order **before Phase 1**. Any gate failing at steps 1–4 ends the run
with `blocked` and a one-line reason; gate 5 never stops the run — it degrades
individual checks. Nothing else executes after a failing gate.

**Owner:** `orchestrator` runs gates 1–5 immediately after Phase 2 (shell allowed,
`edit` denied). A failing gate produces no phase dispatch: the agent-snapshot returns
`STATUS: NEEDS_HUMAN` (a fact only the human holds) or `STUCK` (unresolvable), and the
report is the single-section refusal defined in §14.

| # | Gate | How to establish it | Failure |
|---|---|---|---|
| 1 | Target confirmed | `git rev-parse --show-toplevel`; the path is the session project and is not the agent-system install | `blocked` |
| 2 | Tree clean | `git status --porcelain` returns empty | `blocked` — "dirty tree: <n> entries" |
| 3 | Nobody else working | no `.git/index.lock`, no running watcher/dev server reported by the operator, no in-flight handoff in this repository | `blocked` — "concurrent work detected" |
| 4 | Mode declared | the run is announced as `read-only` in the report header | `blocked` |
| 5 | Tool inventory probed | record which of git, the package manager, the linters, and the doc scripts exist (§9–§13) | proceeds — with `not_applicable`/`blocked` per check |

- **Dirty tree is a stop, not a warning.** Uncommitted work from another session is
  indistinguishable from work this protocol might be blamed for. The sanctioned
  escape is operator-driven: a clean dedicated checkout (a separate clone or a
  worktree the *operator* creates) and a rerun there — the protocol never creates one.
- **Stale refs are declared, never refreshed.** `git fetch` mutates refs, so the
  inventory in §12 describes refs as they exist locally. Record the age of the local
  `origin/<default>` tip so the reader can judge staleness.
- **One question round, upstream only.** A precondition that needs a fact only the
  human holds is a `STATUS: NEEDS_HUMAN` stop, not a question from this protocol: the
  orchestrator returns the concrete fact it needs, `delivery` resolves it in the single
  batched round already owned by [`prompt-pipeline.md`](./prompt-pipeline.md) → Reflex
  checks and `agents/delivery.md` → Session Preflight, and the run stays `blocked` until
  it is answered. The orchestrator itself is denied `question`.

## 5. Cadence and trigger

The protocol is **started manually, "every so often"** — by a human, through the normal
pipeline. There is **no cron, scheduler, watcher, or self-trigger**, and no agent may
start a run because a timer or a prior report said so.

Concrete triggers:

- Before a release or a tag.
- On a roughly monthly rhythm, if the project wants one (the rhythm is a human habit,
  not an automation).
- After a large merge campaign, a long-lived branch lands, or a refactor closes.
- When the repository has been idle for a while and nobody remembers its state.
- Before a handover, onboarding, or archive/deprecation decision.
- After a dependency security advisory, or when CI has been red or flaky.
- When the default branch and the local branch list have visibly diverged.

A run is a **point-in-time snapshot**, not a trend. Comparing runs requires the reports
to be stored somewhere the operator authorized (§14, persistence).

## 6. Status, severity, and evidence

### Status enum (per check)

| Status | Meaning |
|---|---|
| `pass` | The check ran and found nothing; evidence recorded. |
| `fail` | The check ran and found something; findings listed with counts. |
| `not_applicable` | The check cannot apply here, **established by inspection** (no linter, no lockfile, no tags), not by a failed attempt. |
| `blocked` | The check could not run: missing or unrunnable tool, offline, detached HEAD, permissions, unparseable config. (A dirty tree is a run-level stop — §4 — never a per-check status.) |
| `unknown` | The check ran but the result is inconclusive (heuristic detection, squash-merge attribution, no tool for unused-dependency detection). |

**Rollup** of a phase = worst of its checks, ordered `blocked` > `unknown` > `fail` >
`not_applicable` > `pass`. Rationale: `blocked` and `unknown` are *gaps in knowledge*
and are ranked above `fail`, because a known problem is actionable while an unnoticed
one is not. `unknown` is never rendered as `pass`, and `not_applicable` is never
rendered as `pass`.

### Severity anchors (for the findings table)

| Anchor | Meaning | Examples |
|---|---|---|
| critical | A demonstrated, reachable harm: secret exposure proven by the security gate, a dependency vulnerability with a reachable exploitation path, or a demonstrated data-loss hazard. | critical advisory in a shipped dependency. |
| high | A documented workflow does not work, or a repository state that blocks safe delivery. | documented build command fails; default branch unresolvable; a branch holding unpushed work proposed for deletion. |
| medium | Drift and hygiene with a real cost. | lockfile/manifest drift; failing lint in check mode; stale non-English comments in a maintained module. |
| low | Minimization and tidiness. | redundant comments, oversized files, `TODO` without a ticket. |
| info | Observation only. | an existing script is undocumented. |

**Security findings follow [`security-review.md`](./security-review.md).** Its boundary
gate and severity anchors supersede this table for anything security-class: a
secret-like pattern match without demonstrated exposure is `needs_validation` at
`info`, never `critical`.

**Mapping to `ReviewerOutput`** (Phases 5–6 return it, and its `issues[].severity` enum
is `critical | warning | info`): `critical` → `critical`, `high` / `medium` →
`warning`, `low` / `info` → `info`. The five-anchor severity is carried in the issue
`message` and in the consolidated table, which is the table of record.

### Evidence

Every row: `check | command | exit code | output excerpt (≤2 lines)`. No claim without a
registered command, and no severity without a concrete consequence.

## 7. Phase map

| # | Phase | Primary seat | Secondary | Return shape |
|---|---|---|---|---|
| 1 | Code comment minimization | `documenter` | — | `DocumenterOutput` — `files_changed: []`, candidates in `follow_up[]` |
| 2 | Dependency review | `explorer` (manifests) | `tester` (tool inventory + commands) | `ExplorerOutput` + `TesterOutput` |
| 3 | Linter and formatter review | `tester` | — | `TesterOutput` — one entry per command |
| 4 | Docs vs. test/format scripts | `documenter` | `tester` | `DocumenterOutput` + `TesterOutput` |
| 5 | Merged local branch inventory | `reviewer` | — | `ReviewerOutput` — table in `summary`, risky tips in `issues[]` |
| 6 | Additional checks | `explorer` / `reviewer` / `tester` | `external-scout` (external facts only) | the owning seat's schema |
| 7 | Consolidated report | `orchestrator` | `delivery` | prose report (no `output_schema` by design) |

- No new agent. **No schema change is required *provided* phase rows reuse the fields
  below**; adding an evidence field to a schema would be a schema change and is out of
  scope here (it would need its own authorized change). Rows that do not map cleanly
  live in the seat's free-text field (`summary`, or `failures[]` items shaped
  `"<check>: <status> — <command> → <excerpt>"`), and §14's template is the table of
  record.
- Seats keep their own posture; the read-only constraint is a protocol rule layered on
  top, not a permission change.
- Phase sub-checks run **independently and in parallel where safe** (all are read-only).
  A blocked phase never cancels the others.

## 8. Phase 1 — Code comment minimization

**Seat:** `documenter`. **Goal:** decide whether the comments are still necessary and
can be reduced to a minimum — by reporting candidates, never by deleting them.

**Procedure**

1. Enumerate source files by extension, excluding `node_modules/`, vendored
   third-party trees, build output, lockfiles, minified assets, and anything marked
   `DO NOT EDIT` / `@generated`.
2. Classify every comment block into *keep* or *candidate* using the keep-list and the
   candidate classes below. When a comment is both, classify as *keep* and note the
   overlap.
3. Record each candidate as `file:line`, a ≤1-line excerpt, its class, and the reason.
4. Count: files scanned, comment blocks inspected, candidates per class.

**Keep-list:** authoritative in
[`agents/documenter.md`](../agents/documenter.md) → `## Comment pruning` →
`### What always stays` — read it there, do not restate it.

**Candidate classes** (nothing else qualifies):

| Candidate class | Why it goes |
|---|---|
| Restates the next line ("increment the counter") | The code already says *what*. |
| Changelog chatter ("added X on 2024-03-01", "fix by JR") | Version control owns history. |
| Commented-out code | Git owns it; it rots and misleads. |
| Stale comment — contradicts the code beside it | Worse than no comment: it teaches the wrong model. |
| Section banner that duplicates the directory or type structure | Structure is visible. |
| Prose duplicated from `docs/` | Two copies, one of which is unversioned. |
| **Non-English comment** (Phase 1 checklist item per §2) | The language rule: all code comments are in ENGLISH. |

**Return:** `DocumenterOutput` with `files_changed: []`, `files_added: []`,
`files_removed: []`, `summary` = the counts, `confidence` (required by the schema), and
one `follow_up[]` entry per candidate:
`"<path>:<line> — <class> — <rationale> — proposed: delete|rewrite|move to docs"`.
`prune_verification: "not_required"` — this phase prunes nothing.

**Boundary:** the pruning contract — keep-list, knowledge-first rule, comment-only
invariant, `verified | reverted | not_required | blocked` — belongs to
[`agents/documenter.md`](../agents/documenter.md) → `## Comment pruning`, and pruning
runs only in a change cycle with human authorization. **This phase deletes nothing.**

**Status:** `fail` when candidates exist, `pass` when none do, `not_applicable` when the
repo has no hand-maintained source (docs-only, generated-only), `blocked` when the source
set cannot be enumerated (submodules not checked out, unreadable tree).

## 9. Phase 2 — Dependency review

**Seat:** `explorer` for discovery, `tester` for command execution. **Goal:** outdated,
unused, duplicated, and unmaintained dependencies; lockfile-vs-manifest drift; known
vulnerabilities — where a tool exists.

**Procedure**

1. **Discover tooling — never assume a package manager.**
   - **Manifests (`explorer`, read-only):** record the manifests and lockfiles actually
     present (`package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`,
     `pyproject.toml`, `requirements*.txt`, `poetry.lock`, `uv.lock`, `go.mod`/`go.sum`,
     `Cargo.toml`/`Cargo.lock`, `pom.xml`/`build.gradle*`,
     `*.csproj`/`packages.lock.json`, `composer.json`/`composer.lock`,
     `Gemfile`/`Gemfile.lock`, and equivalents) → `ExplorerOutput.files_found`;
     `summary` = one line.
   - **Tool inventory (`tester`):** `explorer` has `bash: deny` and cannot probe `PATH`.
     `tester` runs `<tool> --version` for each candidate (`npm`, `pnpm`, `yarn`, `bun`,
     `uv`, `poetry`, `pip-audit`, `go`, `govulncheck`, `cargo`, `cargo-audit`,
     `osv-scanner`, `dotnet`, `composer`, `bundle-audit`) and records exit/absence.
2. **Run only non-mutating forms** — `outdated`, `ls`, `list`, `audit`/report modes,
   `--json` where available. Any form that installs, resolves-and-writes, or edits the
   lockfile is out of scope: use a documented dry-run flag if one exists, otherwise
   report `blocked` with the reason.
3. **Checks and their status semantics:**

| Check | Status rules |
|---|---|
| Outdated | `fail` with counts by major/minor/patch; `not_applicable` if no manifest; `blocked` if the registry is unreachable. |
| Unused | `fail` with the list; `unknown` if the manager has no unused-detection and no static tool can attribute usage confidently. |
| Duplicated (multiple resolved versions) | `fail` with the resolved versions; `unknown` if the lockfile cannot be resolved without installing. |
| Unmaintained (archived, no release in a long window) | `fail` with the evidence; `blocked` when it needs registry metadata and the network is unavailable. |
| Lockfile vs. manifest drift | `fail` when a manifest range has no matching lock entry, or the lockfile is absent while a manifest is committed; `not_applicable` with no lockfile policy. |
| Known vulnerabilities | `fail` with counts by severity and the advisory ids; `not_applicable` when no audit tool is present; `blocked` when offline. |

4. **Instantiate severity** per §6 — a critical advisory in a dependency that ships to
   production outranks a dev-only one; say which is which.

**Return:** two children. `ExplorerOutput` (`files_found` = manifests/lockfiles,
`summary` = one line for the tool list). `TesterOutput` with `tests_run` = **integer**
count of checks executed, `tests_passed` = **integer** count that returned a clean
status, `failures[]` = one string per non-clean check shaped
`"<check>: <status> — <command> → <excerpt>"`, plus `confidence` (required by the
schema). Command/exit evidence for *clean* checks is assembled by the orchestrator in
Appendix C from the dispatch payload — `TesterOutput` has no evidence field. If no
manifest exists, the `tester` child is not dispatched and the phase is
`not_applicable`.

## 10. Phase 3 — Linter and formatter review

**Seat:** `tester`. **Goal:** report what the project's own linters say, without
changing a single byte.

**Seat contract:** `tester` declares a narrow linter parameter (`linter=eslint|biome`
only). Pass `linter=eslint` / `linter=biome` when the project configures them; for every
other toolchain (ruff, golangci-lint, clippy, stylelint, markdownlint, vale, textlint,
cspell) hand the **exact command line** as ordinary command execution. Never pass a test
framework — this phase runs no tests. If `tester`'s contract cannot express the tool,
report the check `blocked` rather than improvising.

**Procedure**

1. **Discover configuration:** `eslint.config.*` / `.eslintrc*`, `biome.json`,
   `.prettierrc*`, `ruff.toml` / `[tool.ruff]`, `.golangci.yml`, `gofmt`/`go vet`,
   `clippy`, `.stylelintrc*`, `.markdownlint*`, plus `lint` / `format:check` entries in
   the manifest scripts or the project's `docs/project.md` → Common Commands.
2. **Run check mode only:** `--check`, `--dry-run`, `--no-fix`, or the project's
   `lint` / `format:check` script **when it does not write**. Never `--fix`, never a
   bare `format`, never `--write`.
3. Run from the affected package directory, per
   [`orchestrate.md`](./orchestrate.md) → thinking rule 6 (`do-not-run-tests-from-root`).
4. Record: the exact command, the exit code, counts by severity (errors/warnings), the
   worst rules (top 5 by count, rule id → count → one example `file:line`), and the
   worst files (top 10 by findings).
5. Distinguish *configured* from *default*: a tool run without the project's config is
   a different check, and must say so.

**Status:** `fail` when there are errors (or warnings above a project-declared gate),
`pass` when clean, `not_applicable` when **no linter or formatter is configured** —
never `pass` — and `blocked` when the tool is configured but not installed, or its
config cannot be parsed.

## 11. Phase 4 — Documentation vs. the project's test/format scripts

**Seat:** `documenter` (content truth), `tester` (script execution). **Goal:** verify
that the documentation matches reality, and that the docs pass the project's own
formatting/doc-check script.

**Pass A — content truth (`documenter`, read-only).** For every factual claim in
`docs/project.md`, `docs/context/*.md`, a project-root `AGENTS.md` when one exists, and
`README*`: does it still hold?

| Claim kind | Verified by |
|---|---|
| A documented command | The script entry exists in the manifest / Makefile / task runner, is spelled identically, and the docs name the same working directory the script targets. Execution truth (does it actually run) belongs to `tester` — never claim it from a read. |
| A documented path | `glob`/`list` resolves it. |
| A documented version (framework, runtime, tool) | Matches the manifest and the lockfile. |
| A documented package/workspace layout | Matches the directories present. |

Report each claim as `claim | doc location | verified by | status`. A documented
command that no longer exists, or a documented path that moved, is `fail` (high
severity when it is the primary build/run command). An existing script that is
undocumented is `info` (low), never `fail`.

**Pass B — docs check script (`tester`).** Discover, in this order, the project's own
documentation check: `format:check`, `lint:md`, `prettier --check "**/*.md"`,
`markdownlint` / `markdownlint-cli2`, `vale`, `textlint`, `cspell` over docs. Run it in
check mode, from the documented directory, and report **pass/fail per script** with the
exact command and an output summary (files checked, files failing, first 3 messages).

- No docs check script present → `not_applicable`, **never** `pass` — "the docs format
  themselves cleanly" is unproven, not proven.
- Script present but not runnable (missing dependency, wrong interpreter) → `blocked`
  with the error.

**Return:** `DocumenterOutput` with `files_changed: []`, `files_added: []`,
`files_removed: []`, `summary` = the claim tally, `follow_up[]` = one entry per claim
mismatch, and `confidence`; plus a `TesterOutput` for Pass B. Nothing is edited: fixing
the docs is a follow-up requiring authorization.

## 12. Phase 5 — Local branches safe to remove because they are already merged

**Seat:** `reviewer`. **Goal:** a read-only inventory. **Nothing is deleted; deletion
requires per-branch human authorization.**

**Procedure**

1. **Establish the context; fail closed.**
   - Not a git work tree → `blocked`.
   - **Detached HEAD** → `blocked` for this phase (no current branch to reason from).
   - Resolve the default branch offline: `git symbolic-ref refs/remotes/origin/HEAD` →
     `git rev-parse --abbrev-ref origin/HEAD` → the project's declared default from
     `docs/project.md` **only if it names one** → `blocked`. No remote is not by itself
     a block; an unresolved default branch is.
   - Prefer `origin/<default>` when it exists; otherwise the local `<default>` — and
     record which one was used, plus the tip date of `origin/<default>` (§4: refs are
     not refreshed).
2. **Inventory.**
   - `git branch --merged <default>` → candidates whose tip is an ancestor.
   - `git branch --no-merged <default>` → everything else.
   - Per branch: `git log -1 --format='%cI %an %s' <branch>` and
     `git rev-list --left-right --count <default>...<branch>`.
   - Branch-with-gone-upstream: `git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads`.
3. **Account for squash and rebase merges.** `--merged` misses them;
   `git cherry <default> <branch>` marks patch-equivalent commits with `-` and unique
   ones with `+`, but a squash merge rewrites the patch entirely, so `git cherry` also
   reports `+` there.
   - `merged-into-default: yes` — only when `--merged` lists the branch.
   - `merged-into-default: unknown` — not listed, but patch-equivalence, a merged PR
     reference (`gh pr list --state merged`, if present), or a `--grep`-able merge
     commit suggests it landed.
   - `merged-into-default: no` — `git cherry` shows unique commits with no merge
     evidence.
   - **A squash/rebase-detected branch is never `safe-to-delete`.** It is `unknown`,
     always.
4. **Emit the table:** `branch | last commit (date, author, subject ≤50 chars) |
   merged into default (yes/no/unknown) | unique commits | recommendation`.
   `recommendation` ∈ `safe-to-delete` | `review-then-delete` | `keep` | `unknown`.
   Any branch whose unique commits are also absent from every remote ref is
   `keep` (unpushed work), regardless of merge appearance.

**Return:** `ReviewerOutput` — the table in `summary`, `verdict: "approve"` (this phase
is advisory), `issues[]` only for a real hazard: an unpushed tip that looks deletable, a
branch containing a secret-like file, or a diverging branch that a report line might
tempt someone to delete.

**Guardrail:** report only. No `git branch -D`, no `git push --delete`, no `git gc`,
no reflog rewrite. Each deletion needs its own human authorization, quoted per branch.

## 13. Phase 6 — Additional checks

A **fixed set** (each check carries its own status) plus a clearly-marked optional
extension slot. Seat is named per check; every check is read-only.

| Check | Seat | Method | Status rules |
|---|---|---|---|
| Stale `TODO` / `FIXME` / `HACK` / `XXX` with age | `reviewer` (`explorer` may supply marker locations) | `grep` the markers, then `git blame -L<line>,<line> -- <path>` for the commit date; bucket ≤90d / 90d–1y / >1y | `fail` with the oldest 10 and their age bucket; `pass` if none |
| Dead / unreferenced files | `explorer` | no inbound import, manifest entry, or doc link; label each finding Verified / Likely / Inferred per [`broad-investigation-template.md`](./broad-investigation-template.md) | `unknown` when only heuristics support it; `fail` for Verified cases only |
| Broken links and stale versions inside docs | `documenter` | resolve every relative markdown link; compare documented versions with manifests; flag `last_updated` older than 30 days (stale) / 90 days (review) | `fail` per broken link or wrong version |
| `.gitignore` hygiene and committed generated artifacts | `reviewer` | build output, `node_modules`, `.env`, editor/OS noise, large binaries tracked in the index | `fail` with the tracked paths |
| Oversized files | `tester` | top-10 by line count and byte size; flag files over 900 lines as a hot spot candidate. This is a maintenance convention, not [`prompt-pipeline.md`](./prompt-pipeline.md)'s `>900` figure, which counts lines *touched* by a refactor | `fail` with the list; `not_applicable` for a docs-only repo |
| Secret-like filenames and patterns | `reviewer` | filenames (`.env`, `*.pem`, `*.key`, `id_rsa*`), patterns (private-key headers, cloud access-key prefixes, common token prefixes, high-entropy strings) — report `path:line` and class only. **Mechanism:** match contents with `grep` (permitted independently of the `read` secret denies) and never `read` a `.env` path; report `glob` matches for denied filenames | `fail` only per [`security-review.md`](./security-review.md) §3–§5 (boundary gate satisfied); a pattern match without demonstrated exposure is `needs_validation` at `info`, never `critical`; `pass` if none; `blocked` when neither `grep` nor a scan tool covers the set |
| Stale tags / releases and outdated CI action versions | `reviewer` | `git tag --sort=-creatordate`; `uses: <action>@<ref>` majors in CI workflow files | `fail` with the list; `blocked` when checking the current major needs the network |
| License check | `reviewer` | `licensee`, `reuse`, `pip-licenses`, `go-licenses` — only if already installed | `not_applicable` when no tool exists |
| README still describes the project | `documenter` | install / run / stack / badge claims vs. the repository | `fail` when a primary claim is wrong |

### 6.x Optional extension slot (opt-in)

Marked **optional**; nothing here runs unless the operator opts in, and a declined slot
is listed in the report's "checks not run" appendix with the reason.

- Exactly one extension check per run, unless the operator names more.
- It must be read-only, carry its own status from §6, and produce evidence like any
  fixed check.
- Candidates: accessibility audit, performance budget, i18n coverage, database
  migration drift, API-spec drift, dead feature flags, test-coverage trend.
- A slot may **not** be used to justify an install, a network login, or any mutation.

## 14. Phase 7 — Consolidated report

**Seat:** `orchestrator` assembles; `delivery` presents. One report per run, sections in
fixed order, one row per check. The report is returned **in the session** — persisting
it into the target repository (e.g. `docs/maintenance/<date>.md`) is a mutation and
needs per-item authorization.

**Assembly rules**

1. Header first: repository, commit sha (`git rev-parse --short HEAD`), date, trigger,
   operator, mode, precondition verdict.
2. Phase summary in phase order, never severity order.
3. Findings ranked by severity; ties broken by phase order. Every finding cites its
   phase, location, and evidence.
4. Follow-ups split in two: **human authorization required** (anything that would
   change the repository) and **read-only informational** (reads, re-checks, decisions).
   The first group is what a later change cycle consumes; the protocol executes
   neither.
5. Appendices: comment candidates, branch inventory, commands executed, and checks not
   run with their status and reason.
6. Contradictions are surfaced, not smoothed: a `fail` with no evidence, or a `pass`
   with no command, invalidates the section — redo that check **once**, labeled
   `evidence-retry` ([`orchestrate.md`](./orchestrate.md) → `## Outcome feedback
   (bounded)`, the single permitted re-iteration and the second launch-dedup carve-out).
   If the second attempt still lacks evidence, mark the check `unknown` and list it in
   Appendix D. Never a third attempt.

### Report template

```markdown
# Maintenance report — <repo> @ <short-sha> — <YYYY-MM-DD>

Trigger: <release | monthly | post-merge | idle | handover | advisory | other>
Operator: <human>   Mode: read-only
Preconditions: tree clean <yes/no> · concurrent work <none/detected> · default branch <name / unresolved>
Refs as of: local `origin/<default>` tip <date> (refs not refreshed)

## Phase summary

| Phase | Status | Checks | Failures | Notes |
|---|---|---|---|---|
| 1 Comment minimization | <status> | <n> | <n> | <one line> |
| 2 Dependency review | <status> | <n> | <n> | <one line> |
| 3 Linter review | <status> | <n> | <n> | <one line> |
| 4 Docs vs. scripts | <status> | <n> | <n> | <one line> |
| 5 Branch inventory | <status> | <n> | <n> | <one line> |
| 6 Additional checks | <status> | <n> | <n> | <one line> |

## Findings (severity-ranked)

| # | Severity | Phase | Location | Finding | Evidence (command → excerpt) |
|---|---|---|---|---|---|
| 1 | <critical..info> | <n> | <path:line / branch> | <what is wrong> | `<cmd>` → <2 lines> |

## Follow-ups — human authorization required

| # | Action | Phase | Why | Risk if applied |
|---|---|---|---|---|
| 1 | <bump X to Y / delete branch Z / prune comments in F> | <n> | <finding #> | <blast radius> |

## Follow-ups — read-only informational

- <re-check after release; confirm intent with owner; keep as-is>

## Appendix A — Comment candidates

| file:line | Class | Rationale | Proposed |
|---|---|---|---|

## Appendix B — Branch inventory

| Branch | Last commit | Merged into default | Unique commits | Recommendation |
|---|---|---|---|---|

## Appendix C — Commands executed

| Command | Exit | Excerpt |
|---|---|---|

## Appendix D — Checks not run

| Check | Status | Reason |
|---|---|---|
```

**Status of the report itself:** the worst phase rollup under §6. An
all-`not_applicable` report is `pass` only with the explicit line "nothing was
verifiable in this repository" — it is never presented as a clean repository.
`blocked` when a precondition stopped the run (the report is then a one-section refusal
with the gate and its evidence).

## 15. Anti-patterns

1. Running a mutating command "because it was obviously safe" — installs, `--fix`,
   formatters, lockfile refreshes, branch deletion.
2. Reporting `pass` because a tool was absent, or `not_applicable` because a command
   failed.
3. Reading absence as cleanliness: no linter, no docs script, no audit tool, no
   `TODO` found because the search was too narrow.
4. Refreshing refs (`git fetch --prune`) to make the branch inventory "accurate" —
   that mutates, and it also hides how stale the picture was.
5. Marking a squash-merged branch `safe-to-delete` on the strength of `--merged`.
6. Echoing a secret value, or a reconstructible fragment of it, into the report.
7. Editing a comment, a doc, or a `.gitignore` mid-audit "since we were there".
8. A phase silently skipped because an earlier phase was `blocked`.
9. Trend claims from a single snapshot.
10. Presenting a finding without the command that produced it, or a severity without a
    consequence.

## 16. Cross-references

- [`agents/documenter.md`](../agents/documenter.md) → `## Comment pruning` — the
  keep-list, knowledge-first rule, comment-only invariant, and pruning status.
- [`agents/reviewer.md`](../agents/reviewer.md) — the judgement seat used by Phases 5
  and 6.
- [`broad-investigation-template.md`](./broad-investigation-template.md) — evidence
  quality labels (Verified / Likely / Inferred) used by Phase 6.
- [`orchestrate.md`](./orchestrate.md) → thinking rule 6 — run project commands from
  the package directory, never the repo root.
- [`security-review.md`](./security-review.md) — boundary gate and severity anchors;
  the secret-scan findings of Phase 6 reuse its `path:line` and
  no-severity-without-impact discipline.
- [`subagent-return-check.md`](./subagent-return-check.md) — return validation and the
  "receipt ≠ completion" rule for every phase return.
- [`prompt-pipeline.md`](./prompt-pipeline.md) — the normal change cycle that executes
  an authorized follow-up.
