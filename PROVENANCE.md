# CyBorges — published build provenance

This branch carries the static build served at <https://nijnamovich.github.io/cyborges/>.

**This is a build from source, not a byte-exact capture of the upstream deployment.**
The artifacts below were produced with the upstream toolchain from the commit described
here, so they are reproducible from the sources listed under "Source" — they are not
copies of a previously published deployment.

## Source

- Repository: `Daver-Ui/agent-wizard` (public)
- Base commit: `d1462a4e24ad3252e3a10078ac7e877e07d4c652` — *"ci: deploy static Angular SPA
  to GitHub Pages"*
- Local changes built on top of that base (not pushed upstream):

  | Commit | Subject |
  |---|---|
  | `df86f4804ba2a0e39b40753a49baa3dd2265e05a` | `feat(ui): CyBorges intro hero, stage-grouped agents, full protocol set` |
  | `53ccf18c1eceb6aaf6251296597a9001844e01f3` | `fix(protocols): size protocol cards to their content` |

## Toolchain

| Tool | Version |
|---|---|
| Angular | 22.1.3 |
| Angular CLI / `@angular/build` | 22.1.5 |
| Node.js | 26.12.1 |
| npm | 12.0.2 |
| OS | linux x64 |

## Build

```sh
npx ng build --configuration production --base-href /cyborges/
cp dist/agent-wizard/browser/index.html dist/agent-wizard/browser/404.html
```

- Build timestamp: `2026-10-27T00:11:45Z`
- Output bundle: `dist/agent-wizard/browser/` (13 files, 1 674 677 bytes)
- `404.html` is a copy of `index.html`, so deep links resolve to the SPA shell.
- `.nojekyll` is present so GitHub Pages serves the tree verbatim.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `index.html` | 55 459 | `9df10d9bd0b3c4e1f9b48c3e73691cb2143043c3b8540e8b2c2839f7b0b04aa4` |
| `404.html` | 55 459 | `9df10d9bd0b3c4e1f9b48c3e73691cb2143043c3b8540e8b2c2839f7b0b04aa4` |
| `main-5TQRNGKX.js` | 423 498 | `e9dd039d4da376f5900ec7dfd6c6d808aa9eb23837fb3fa2f51d990b3af0fd46` |
| `chunk-CbVe9y2i.js` | 448 820 | `ad61a7a4066d202552b7bfe28e5002bc231ce47e4fa0490e51e5d72042e29b9e` |
| `chunk-D1Er4EtG.js` | 67 853 | `874771653f06f112388e0ae698fefd788b8f8c075bcd43b902d7a4a585e086c3` |
| `chunk-BoU4aeH3.js` | 16 885 | `fdb176b510660c7f82f2ae77f3f1ae0b7fad5865b4706834b28c85620ed73773` |
| `styles-RD3AWLMQ.css` | 104 408 | `afdf76b41f71f728447ea28938214fe3fa3406eded08cd5a51f37c4d5c838f22` |
| `favicon.ico` | 15 086 | `f9102be80297c0529207607be5277b4f90bca89d65988fa1771b91c7894e815f` |
| `assets/cyborges-borges-standing.avif` | 82 578 | `a52705abaed52ce473751db103dd1d35471962a8b3946245fcaed92133330307` |
| `assets/cyborges-borges-standing.webp` | 143 080 | `cddfe797736cb690aa961599b83ccb45db1e644af022da784f85911321ecadc9` |
| `assets/cyborges-borges-standing.png` | 261 551 | `31cecbf0628addbe52a357ebc7b1d4158125ceda8ab07c263c16014b59e1f8d2` |

The hero image is served as AVIF (`<link rel="preload">` + `<source type="image/avif">`),
with WebP and PNG fallbacks, at an intrinsic size of 900 × 1350.

## Notes

- The lazy chunk `chunk-CbVe9y2i.js` carries the Pipeline view; `chunk-D1Er4EtG.js` the
  in-app source browser; `chunk-BoU4aeH3.js` the diagram agent viewer.
- No analytics, no cookies, no external script origins. The page links out to
  `opencode.ai`, `github.com/Nijnamovich/cyborges` and
  `github.com/Nijnamovich/documentation-onrails`.
- The site contains no email addresses, no local filesystem paths and no browser data.
