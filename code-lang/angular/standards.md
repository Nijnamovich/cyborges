# Angular Standards

Companion: [Design standards](../default/standards.md).

- Prefer the `angular-cli` MCP `get_best_practices` and `search_documentation`
  tools for Angular decisions; angular.dev is the canonical documentation source.
  Check guidance and API signatures against the installed version; current
  documentation is not a migration mandate.
- Use strict TypeScript and precise contracts. Prefer inference where clear and
  `unknown` with narrowing at uncertain boundaries; avoid `any` or casts that
  conceal mismatches.
- Prefer standalone APIs, OnPush, and signal-based component APIs when supported
  and consistent with project conventions. Do not convert working
  NgModule, injection, forms, or state patterns merely to modernize syntax.
- Use `computed` for signal-derived values and, where supported, `linkedSignal`
  for writable state dependent on a source. Reserve effects for side effects,
  not state propagation; timers are not a reactive synchronization mechanism.
- Choose Observable, signal interop, and resource APIs deliberately. Manage
  subscription lifetimes, cancellation, and stale responses. Guard resource
  value reads and represent loading, error, empty, and success states explicitly;
  defaults and retained values can affect which state should render.
- Keep templates declarative and accessible; track repeated items by stable
  identity. Preserve Angular sanitization and do not bypass it for untrusted data.
- Provide the router base explicitly with `APP_BASE_HREF` and keep asset URLs
  independent of `<base>` (`deployUrl`, or absolute URLs including the
  deployment path); the router must not depend on an authored `<base>` element.
- Under a CSP with `base-uri 'none'`, every `<base>` is inert. Remove the element
  and the `baseHref` build option that would re-emit it, rather than relaxing the
  directive to `'self'`; verify the built `index.html` and that deep links resolve.
- Test observable component behavior and async transitions with the installed
  testing stack and supported scheduling utilities, not copied flush sequences.

## References

- [Angular style guide](https://angular.dev/style-guide)
- [Signals](https://angular.dev/guide/signals) and
  [linkedSignal](https://angular.dev/guide/signals/linked-signal)
- [RxJS interop](https://angular.dev/ecosystem/rxjs-interop) and
  [rxResource API](https://angular.dev/api/core/rxjs-interop/rxResource)
- [Router base href](https://angular.dev/guide/routing/router-reference#base-href)
  and [deploy URL](https://angular.dev/tools/cli/deployment#--deploy-url)
- [Security](https://angular.dev/best-practices/security) and
  [testing](https://angular.dev/guide/testing)
- [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [RxJS guide](https://rxjs.dev/guide/overview)
