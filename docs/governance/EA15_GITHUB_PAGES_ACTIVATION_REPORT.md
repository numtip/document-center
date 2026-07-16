# EA-15 — GitHub Pages Activation Report

**Date**: 2026-07-16  
**Version**: 1.0.3  
**Tag**: `document-center-v1.0.3`

---

## Previous Pages State

| Item | Before EA-15 |
|------|--------------|
| Root URL | 3-record Document Center demo |
| Data source | `preview/data/public-registry.sample.json` |
| Build | Copied `preview/` → `dist/` root |
| Classification | Misleading — demo at root |

## New Information Architecture

| Route | Content |
|-------|---------|
| `/` | Canonical Repository landing (bilingual) |
| `/preview/` | 3-record UI demo (preserved) |
| `/architecture/` | Architecture overview |
| `/standards/` | Principles & standards |
| `/adr/` | ADR index (001–009) |
| `/roadmap/` | Enterprise platform roadmap |
| `/release/` | Version baseline |
| `/operations/` | READ-MOSTLY policy summary |
| `/404.html` | Friendly fallback |

## Deployment

| Item | Value |
|------|-------|
| Source | GitHub Actions workflow |
| Workflow | `.github/workflows/pages.yml` |
| Build | `npm run build` → `dist/` |
| Validate | `npm run validate:pages` |
| Branch | `gh-pages` (orphan) |
| Base path | `/document-center/` |

## Build Result

| Check | Result |
|-------|--------|
| `npm run build` | PASS |
| `npm run validate:pages` | PASS |
| `npm run validate:all` | PASS |
| `npm run lint` | PASS |

## Link Validation

Internal routes and preview_mode validated in build script. GitHub doc links use `github.com/numtip/document-center/blob/main/...`.

## Live Verification

| Check | Result |
|-------|--------|
| Root canonical landing | _pending deploy_ |
| Preview at `/preview/` | _pending deploy_ |
| Version 1.0.3 displayed | _pending deploy_ |
| Production CTA correct | _pending deploy_ |

## Final Verdict

_Pending workflow completion and live verification._
