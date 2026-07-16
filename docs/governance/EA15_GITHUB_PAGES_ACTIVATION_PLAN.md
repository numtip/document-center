# EA-15 — GitHub Pages Activation Plan

**Date**: 2026-07-16  
**Version target**: 1.0.3

---

## Discovery Summary

| Item | Current state |
|------|---------------|
| Deployment | GitHub Actions → `gh-pages` branch |
| Workflow | `.github/workflows/pages.yml` |
| Build command | `npm run build` → `tsx scripts/build-preview.ts` |
| Published branch | `gh-pages` (orphan, force) |
| Static technology | Plain HTML/CSS/JS (no framework) |
| Previous root | 3-record Document Center demo (`preview/` copied to `dist/`) |
| Base path | `/document-center/` (project Pages URL) |
| Node | 20 (workflow) |

## Target IA

| Route | Purpose |
|-------|---------|
| `/` | Canonical Repository landing (NEW) |
| `/preview/` | 3-record UI demo (preserved) |
| `/architecture/` | Architecture overview |
| `/standards/` | Principles & standards |
| `/adr/` | ADR index |
| `/roadmap/` | Enterprise roadmap |
| `/release/` | v1.0.x release baseline |
| `/operations/` | READ-MOSTLY operations summary |
| `/404.html` | Friendly fallback |

## Build Changes

1. New `site/` source for canonical portal
2. `scripts/build-preview.ts` builds portal + copies `preview/` → `dist/preview/`
3. `scripts/validate-pages.ts` validates routes, links, version, preview_mode
4. Workflow adds validate step before deploy

## Constraints

- No SharePoint/Registry/production data exposure
- No ADR or baseline modifications
- Preserve `preview_mode: true` on demo data
- Base path `/document-center/` compatible relative paths

## Verdict criteria

`EA15_CANONICAL_PAGES_LIVE` when live root shows canonical landing, not demo.
