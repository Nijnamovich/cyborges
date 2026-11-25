# Protocol: UI Design

Creation-time design criteria for front-end work. Applied when a page, screen, view, or a
coherent set of UI states is **designed or created** — before or alongside the code. It is
not a review protocol: auditing a built UI is the review seats' job, and no step here ever
produces an accessibility certificate.

> Adapted from a human-supplied review specification (`ui-design-reviewer`), inverted from
> *evaluate an existing UI* to *design a new one*. The measurable rules and the evidence
> discipline are preserved; each rule is restated as a design-time decision plus a checkable
> acceptance condition.

## 1. Scope and seats

**In scope**

- Designing a new page, screen, or view; a substantial redesign of one; a dashboard, form,
  wizard, table, dialog, navigation area, empty state, or equivalent UI surface.
- Deciding visual hierarchy, content density, interaction model, and responsive behavior
  for such a surface.

**Out of scope**

- CSS mechanics — tokens, layout primitives, focus styling, container queries, motion:
  [`code-lang/css/standards.md`](../code-lang/css/standards.md) owns those and wins (§3).
- Accessibility certification, and any claim that a designed UI *passes* WCAG (§5.10).
- Implementing a component when no design decision is left to make.

**Seats**

- **`architect`** produces the **design brief** (§4) — purpose, hierarchy, content, states,
  layout, interaction model, accessibility plan, and acceptance conditions — and returns it
  as `decisions[]` entries in `ArchitectOutput`. It does not edit files.
- **`coder`** (`language=angular|css`) implements the brief and self-checks its acceptance
  conditions before returning (§7). When a UI-bearing change arrives with no brief, `coder`
  derives the brief fields itself **only for a non-substantial change**, records that
  assumption in its summary, and re-routes a substantial redesign to `architect`.
- No seat negotiates these criteria away. A project overrides them only through its
  documented design system and project rules (§3).

**Route a task here when** it says create, design, redesign, or add a page, screen, view,
dashboard, form, wizard, table, navigation area, or empty state — or asks to "make it look
like X".

## 2. Guiding principles

1. **Function before decoration.** Every visual element must help the user understand,
   decide, or act.
2. **Clarity before density.** Show what the current task needs; remove visual noise.
3. **Consistency before variety.** Same purpose → same appearance and behavior.
4. **State always visible.** The user can tell what is selected, available, busy, loading,
   or disabled.
5. **Predictability.** A control communicates what it does and behaves as expected.
6. **Accessibility from design.** The interface must be perceivable, understandable, and
   operable by people with different abilities — decided at design time, not patched later.
7. **Evidence before opinion.** A claim names what is established, where, and how; anything
   else is recorded as unverified (§6).
8. **Personal taste is not a usability problem.** A preference with no task impact is an
   opinion, not a design defect, and never an acceptance failure.
9. **References borrow traits, not atmospheres.** A concrete reference ("a 1970s graduate
   lecture handout") communicates intent faster than an adjective list, but it also imports
   traits nobody asked for: name the traits meant to be borrowed and the ones explicitly
   not.

## 3. Precedence

Resolve conflicts in this order; a higher rule wins.

1. **The project's design system** documented in `docs/context/` (tokens, component library,
   brand, platform conventions) wins over this protocol. Where the project system is silent,
   this protocol applies.
2. **[`code-lang/css/standards.md`](../code-lang/css/standards.md) wins on styling
   mechanics.** This protocol states *what must be true*, never *how to write the CSS*;
   where it cites a mechanical value (e.g. the 44px target baseline, reduced-motion
   handling) that file remains the authoring authority.
3. **Accessibility floor:** WCAG 2.2 AA as referenced in §5.4 and §5.10. A stricter project
   rule wins.
4. When a platform convention conflicts with a domain below, record the conflict in the
   brief's open questions instead of silently choosing a side.

## 4. The design brief (architect output, before code)

A compact brief, one screen at a time. Every field is mandatory unless marked otherwise; an
empty field is a declared gap, not an omission.

| Field | Must state | Fails when |
|---|---|---|
| Purpose & primary task | One sentence: what the user accomplishes here, concrete enough that a third party can name the visual consequence it implies. | The screen has two primary tasks or none; the sentence is an adjective list with no derivable visual consequence. |
| Users & entry context | Who arrives, from where, on which device class. | It assumes a single happy-path entry. |
| Visual hierarchy | The primary action, the secondary tier, what is subordinate; for any cited reference, the trait being borrowed (density, type scale, contrast, rhythm). | Two elements compete as the primary focus, or a cited reference names no borrowed trait. |
| Content & disclosure | Content inventory; what is always visible; what sits behind progressive disclosure. | Necessary capability is hidden to look minimal. |
| Design-system usage | Tokens and components reused, with one actual in-repo source path per distinct source file — or the package/import specifier when the system is an external dependency — plus a section `#anchor` when the target doc has one; an unresolvable path is a declared gap; each new variant with its functional reason. | A one-off pattern appears with no recorded gap, or a cited source path is invented or dead. |
| States | Every applicable state from §5.7, with its message or affordance. | Only the happy path is designed. |
| Layout & responsive targets | Grid/structure, spacing scale, named viewport or container sizes and what reflows at each. | It names no sizes, or claims "responsive" without saying what changes. |
| Interaction & affordances | Interaction model, hit areas, destructive-action guards, non-drag alternatives. | An interaction is assumed to work because the mock suggests it. |
| Accessibility plan | Semantic structure, keyboard path, focus order, accessible names, non-color cues. | The plan is "it will be accessible". |
| Acceptance conditions | The checkable conditions from §5, each with its status vocabulary (§7). | Conditions are unmeasurable adjectives. |
| Open questions & conflicts | Each unresolved conflict (§3) with the side taken provisionally and who resolves it. | A conflict is silently resolved, or no owner is named. |
| Pending checks | What design cannot settle, and what would settle it (§6). | A pending item is silently reported as met. |

## 5. Design domains and acceptance conditions

### 5.1 Visual hierarchy

Design: one primary action; the current location or section stated; primary, secondary, and
tertiary action tiers; related information grouped; size, weight, spacing, and contrast used
to rank; secondary information visually subordinate to the primary task.

Accept when: from the design alone, a reader can name the screen, the primary task, and the
primary action without reading every label; no two elements compete as the primary focus;
every secondary action is visually distinguishable from the primary one.

### 5.2 Simplicity and cognitive load

Design: only the decisions needed now are visible; advanced options behind progressive
disclosure; sensible defaults for the common case; no repeated or irrelevant information;
fields appear when the user needs them; the flow has as few steps as the task allows.

Accept when: each screen carries one primary task; every visible control is needed for the
current step or is behind disclosure; simplification removes effort **without** hiding a
capability — disclose, do not delete.

### 5.3 Consistency and design system

Design: reuse the existing tokens and components; same purpose → same look and behavior;
every difference has a functional reason; every interactive component has defined hover,
focus, active, selected, disabled, loading, and error states; terminology matches the product.

Accept when: every new visual variant cites the token or component it reuses, or records a
design-system gap in the brief; no ad-hoc component is introduced without that record;
labels and terms match existing screens.

### 5.4 Color, contrast, and legibility

Design: color carries function (state, emphasis, meaning), not decoration; accent color used
sparingly; foreground/background pairs named explicitly; no meaning conveyed by color alone.

Accept — **WCAG 2.2 AA, measurable:**

- Normal text: contrast ratio **at least 4.5:1**.
- Large text: contrast ratio **at least 3:1**.
- UI components and graphical objects required for understanding: **at least 3:1** against
  adjacent colors.

If the design carries no measured color values, do **not** assert that contrast passes or
fails numerically — record `contrast: pending measurement` in the brief's pending checks.
Every color-encoded meaning has a second cue (icon, text, pattern, or position).

### 5.5 Typography and content

Design: legible at real screen sizes; a small fixed type scale; comfortable line length for
prose; action-oriented labels; error text that says what happened and how to fix it; help
text next to the element it explains; a placeholder is never the only field name.

Accept when: every form control has a visible, persistent label (icon-only controls satisfy
§5.6's accessible-name requirement instead); every error message names the
problem and the next step; no essential text is set at a size or weight that fails §5.4 at
the named viewport; no ambiguous generic label ("OK", "Accept") stands where a specific
action word is available.

### 5.6 Affordances and interaction

Design: interactive elements look interactive; icons are recognizable and carry an
accessible name; hit and touch targets are comfortably usable (at least 44px, or the
project's larger floor); drag and drop signals origin, target, and result and has a
non-drag alternative; destructive actions are guarded; errors are prevented by design.

Accept when: every interactive element is distinguishable from static content without
hover; every icon-only control has an accessible name; every destructive action has a guard
(confirmation, undo, or a reversible step); no required interaction is drag-only.

### 5.7 Feedback and system states

Design every applicable state from this inventory, not just the happy path: initial or
empty, hover, focus, selected, loading or processing, success, error, disabled, no results,
and offline when relevant.

Accept when: the brief lists each applicable state with its message or affordance;
operations that are not immediate show a loading indicator; an important or destructive
action is confirmed; double submission is prevented; persistence or loss of unsaved changes
is communicated; every error state is actionable.

**Evidence rule:** a state that was not designed or not observed is `unverified` — never
reported as absent, and never assumed unnecessary.

### 5.8 Layout, alignment, and spacing

Design: a recognizable grid or structure; a consistent spacing scale; proximity groups
related elements and separates unrelated groups; density matched to the task; no overflow,
overlap, or avoidable scrolling; balanced use of the available space.

Accept when: all elements align to the declared grid and spacing scale; spacing within a
group is smaller than spacing between groups; no design frame shows clipping, overlap, or a
scrollbar the content does not need.

### 5.9 Responsive design

Design: name the viewport or container sizes the product must support; state reflow and
content priority at each; navigation and panels adapt; tables, grids, dialogs, and side
panels have defined narrow behavior; touch targets hold on touch sizes.

Accept when: the brief names the supported sizes and what changes at each; no supported size
requires horizontal scrolling to read; nothing is cut off or overlapped at a named size;
the brief defines narrow behavior for every named size instead of inheriting the desktop
layout.

**Evidence rule:** sizes not examined are listed as `unverified` — a desktop design does not
imply a working narrow layout.

### 5.10 Accessibility

Design against WCAG 2.2 AA: sufficient contrast (§5.4), full keyboard operation, a visible
focus indicator, logical focus order, accessible names and labels, correct heading hierarchy
and semantic structure, alternative text for informative images, no meaning by color, sound,
or motion alone, adequate touch targets, respect for reduced-motion preferences, and a
structure a screen reader can traverse.

Accept when: the brief states the semantic structure (landmarks and headings), the keyboard
path through the page, and the accessible name of every control; focus order matches visual
order; no functionality is mouse- or gesture-only.

**Boundary (mandatory): a visual or design pass cannot certify accessibility.** Separate the
design decisions from the checks that need a keyboard, a screen reader, the DOM, or automated
tooling, and list the latter as pending checks with what would verify them.

### 5.11 Usability heuristics for the designed flow

Apply these to the flow, not just the frame: visibility of system state; match to the real
world; user control and freedom; consistency and standards; error prevention; recognition
over recall; flexibility and efficiency; minimalist design; helpful error recovery.

Accept when: the brief records where the user can cancel, go back, or undo, and where the
design could show what it currently asks the user to remember.

## 6. Evidence discipline at design time

- Assert only what is established. No contrast number without measured values → `contrast:
  pending measurement`. When the project exposes token values for a named foreground/background
  pair, contrast is measured with a named tool by the seat that can run one instead of left
  pending; `contrast: pending measurement` is the fallback only when no token values are
  available or no seat can run a tool. No unobserved state reported as absent → `unverified`.
  No responsive claim from a single-size design → list the unverified sizes. No accessibility
  compliance claim from a design → §5.10 boundary.
- Every pending check names three things: what is unverified, why design cannot settle it,
  and what would settle it (tool, device, keyboard, screen reader, or runtime state).
- A preference is recorded as a design opinion, clearly separate from the acceptance
  conditions. It is never escalated to a defect by repetition.

## 7. Acceptance and handoff

Every acceptance condition carries one status: `met`, `pending-check`, `not-met`, or
`not_applicable`. `unverified` and `contrast: pending measurement` are **not** statuses — they
are the reason recorded *inside* a `pending-check`; use that single form throughout.

- `not-met` on a **critical** condition blocks handoff. Critical at design time means: it
  blocks the primary task, risks data loss, or creates a serious access barrier.
- `pending-check` never counts as met, and is carried into implementation, not dropped.
- The brief travels with the implementation. `coder` self-checks every condition and reports
  the `met` / `pending-check` list compactly in `CoderOutput.summary`.
- Reviewing a delivered page belongs to the review seats. This protocol supplies the
  criteria; it does not issue the verdict.

## 8. Anti-patterns

1. Treating a personal preference as a usability problem.
2. Redesigning because a visual trend is fashionable.
3. Demanding identical screens instead of coherent ones.
4. Adding a control without stating the need it resolves.
5. Calling minimalism the hiding of necessary functions.
6. Specifying interactions nobody will verify, or inventing behavior that was not designed.
7. Claiming WCAG compliance from a design pass.
8. Rebuilding a whole UI when a targeted change resolves the problem.
9. Changing decisions that already work, without a reason.
10. Choosing the clever solution over the simplest one consistent with the product.

## 9. Cross-references

- [`code-lang/css/standards.md`](../code-lang/css/standards.md) — styling mechanics; wins on
  *how* the CSS is written (§3).
- [`agents/architect.md`](../agents/architect.md) — produces the design brief.
- [`agents/coder.md`](../agents/coder.md) — implements the brief and self-checks it.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — the accessibility reference behind §5.4 and
  §5.10.
- [`orchestrate.md`](./orchestrate.md) → thinking rule 1 — read the project's `docs/` before
  designing; the project's design system is the source of truth (§3).
