# cyborges — published page build (`gh-pages`)

Static build of **AgentWizard**, the single-page app that documents the cyborges agent
system. Published at <https://nijnamovich.github.io/cyborges/>.

- Source: `Daver-Ui/agent-wizard` @ `d1462a4` (public), plus two local commits that add the
  CyBorges intro hero and the full protocol set (see [`PROVENANCE.md`](PROVENANCE.md)).
- The agent system itself (`agents/`, `protocols/`, `code-lang/`, `scripts/`,
  `opencode.json`) lives on `main`, not on this branch.
- Provenance, source commits, toolchain and file hashes: [`PROVENANCE.md`](PROVENANCE.md).

This branch holds **build output only**. It is a **build from source**, produced with
`ng build --configuration production --base-href /cyborges/` — not a byte-exact capture of
any previously deployed artifact. Do not edit by hand — regenerate from the source repo.

Layout:

| Path | Purpose |
|---|---|
| `index.html` | SPA shell |
| `404.html` | copy of `index.html`, so deep links resolve |
| `main-*.js`, `chunk-*.js` | application bundles |
| `styles-*.css` | global stylesheet |
| `assets/` | hero image (AVIF / WebP / PNG) |
| `favicon.ico`, `.nojekyll` | site metadata |
