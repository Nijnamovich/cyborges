# cyborges — published page build (`gh-pages`)

Static build of **AgentWizard**, the single-page app that documents the cyborges agent
system. Published at <https://nijnamovich.github.io/cyborges/>.

- Source: `Daver-Ui/agent-wizard` @ `d1462a4` (public) — deployed at
  <https://daver-ui.github.io/agent-wizard/>.
- The agent system itself (`agents/`, `protocols/`, `code-lang/`, `scripts/`,
  `opencode.json`) lives on `main`, not on this branch.
- Provenance, source commit and file hashes: [`PROVENANCE.md`](PROVENANCE.md).

This branch holds **build output only**. Everything except `index.html` is byte-identical
to the deployed artifact; `index.html` differs only by its `<base href>`
(`/agent-wizard/` → `/cyborges/`). Do not edit by hand — regenerate from the source repo.
