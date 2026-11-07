# Design Standards

Language-agnostic architectural baseline.

## Minimalism invariants

- Introduce only the layers and abstractions the behavior actually needs; a diagram is not a requirement.
- Promote code to a shared module after the second real consumer, not before.
- No speculative extensibility: no hooks, options, or indirection for imagined futures.

## Boundaries and state

- Separate business decisions, application coordination, and delivery details.
  Keep domain rules independent of framework, transport, and persistence choices.
- Use explicit boundaries and adapters where external details need isolation;
  dependencies should point toward the rules they serve.
- Make contracts, ownership, and meaningful state transitions explicit.
- Prefer composition and cohesive units. Introduce layers or interfaces for real
  boundaries, not to reproduce an architectural diagram.
- Keep correctness-critical decisions deterministic; treat external engines,
  including model-backed services, as replaceable infrastructure.

## Testing

A test earns its place by answering two questions:

- **Can it fail?** If no realistic change could make it fail, it is not a test.
- **Can it survive?** If it would pass through a regression in the behavior it
  names, it is not a test.

Avoid the **mirror test**: assertions that are a second copy of the
implementation (restating each internal step). Test observable behavior and
contracts, not the current internal sequence.
