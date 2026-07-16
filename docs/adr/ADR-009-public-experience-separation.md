# ADR-009: Public Experience Separation

**Status**: Accepted  
**Date**: 2026-07-16 (retroactive)  
**Phase**: EA-11A

---

## Context

Multiple URLs existed: SharePoint Document Center, GitHub Pages preview, archived JSON in Git, and planned Next.js portal. Stakeholders could confuse preview/demo environments with production, leading to incorrect bookmarks and support requests.

## Decision

**Explicitly separate** three experience tiers:

| Tier | URL | Records | Role |
|------|-----|--------:|------|
| **Production** | SharePoint Document Center | 627 | Operational portal (authenticated) |
| **Preview** | `numtip.github.io/document-center/` | 3 | UI demo (`preview_mode: true`) |
| **Planned public** | `rae-nextjs-main` | 627 (future export) | Public portal via Registry JSON |

GitHub Pages **must remain preview only**. Build guard validates only demo `example.sharepoint.com` URLs ship to Pages.

## Consequences

**Positive**:

- No production data exposed on public GitHub Pages
- Clear communication to users and dependent projects
- Preview useful for UI blueprint validation
- Export contract defines future public portal boundary

**Negative**:

- Two URLs to communicate (production vs preview)
- GitHub Pages not useful for real document access
- Next.js portal still requires export pipeline build

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| GitHub Pages as production | Public exposure of internal docs; no ACL |
| SharePoint only (no preview) | No public UI development sandbox |
| Export 627 records to GitHub Pages | Internal/restricted docs would leak |
| Single Next.js portal immediately | Export pipeline not built; blocks v1.0 freeze |
