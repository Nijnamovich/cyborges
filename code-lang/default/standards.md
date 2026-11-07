# Design Standards

Language-agnostic architectural baseline.

## Minimalism invariants

- Add only the layers the behavior needs. Do not create empty controllers, services, or folders.
- Promote code to a shared location only after two real consumers need it.
- Do not introduce an interface only because a dependency exists.
- Avoid speculative extensibility.

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

A test earns its place only by passing both:

1. **Can it fail?** Name one realistic bug it would catch.
2. **Can it survive?** Rename an internal method, split the unit, swap the storage library.

Avoid **mirror tests**: the assertions are a second copy of the implementation.

Use this exact test-name structure: `should <expected behavior> when <known context>`. Keep the complete formula in the `test` or `it` description even when nested `describe` blocks already establish context.
