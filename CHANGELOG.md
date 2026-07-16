# Changelog

All notable changes to the RAE Document Center project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-07-16

### Added

- Canonical GitHub Pages portal at site root
- Routes: `/`, `/preview/`, `/architecture/`, `/standards/`, `/adr/`, `/roadmap/`, `/release/`, `/operations/`, `404.html`
- Bilingual canonical landing page (Thai/English)
- `scripts/validate-pages.ts` for route and labelling validation
- EA-15 activation plan and report

### Changed

- GitHub Pages root: canonical repository portal (replaces 3-record demo at root)
- UI demo preserved at `/preview/` with preview banner
- Workflow validates pages before deploy
- No production, SharePoint, Registry, or ADR changes

## [1.0.2] - 2026-07-16

### Added

- Enterprise governance package under `docs/governance/`
- RAE Enterprise Platform Roadmap and dependency graph
- Canonical Repository Certificate
- Consumer Implementation Guide (Research, Learning, Green Office, Next.js, AI)
- Architecture Lifecycle (v1.x–v4.x roadmap)
- Repository Operation Policy (READ-MOSTLY mode)
- Project Bootstrap Template for new RAE projects
- System of Records declaration
- Architecture Principles (7 normative principles)

### Changed

- README updated for enterprise governance freeze (v1.0.2)
- Repository enters READ-MOSTLY mode
- No production implementation, SharePoint, Registry, or ADR changes

## [1.0.1] - 2026-07-16

### Added

- Canonical repository governance under `docs/canonical/`
- Architecture Decision Records ADR-001 through ADR-009 in `docs/adr/`
- Canonical Repository Charter, Repository Governance, Reference Standards
- Repository Map, Project Index, Dependent Projects registry
- Project Memory Freeze v1 and Change Control Policy
- Master README rewritten as RAE Enterprise Canonical Repository

### Changed

- Repository elevated from implementation project to canonical enterprise reference
- No production code or SharePoint/Registry data changes

## [1.0.0] - 2026-07-16

### Added

- Production freeze package under `docs/release/`
- Architecture baseline v1.0 (`ARCHITECTURE_BASELINE_v1.0.md`)
- Production acceptance certificate (627/627/627 verified)
- Operation runbook v1.0
- Project closeout report
- EA-11A production portal discovery documentation
- Git tag `document-center-v1.0.0`

### Completed

- Full WTMS corpus migration: **627 documents** to SharePoint (EA-10)
- Final reconciliation and portal QA (EA-11)
- Registry automation with idempotent sync (EA-8)
- SharePoint Document Center operational portal (EA-7B/7C)

### Documented

- Production URL: SharePoint Document Center on Maejo365
- Preview URL: GitHub Pages with **3 demo records** (`preview_mode: true`)
- Deferred governance scope (owners, groups, workflows)

### Fixed

- REST library scan pagination for 500+ item libraries (EA-10)
- Registry reconciliation via artifact-based corpus verify (EA-11)

### Security

- No secrets committed in release scope
- Browser profiles remain gitignored (`.browser-profile/`)

---

## Pre-1.0 History

Migration phases EA-3 through EA-11 are documented in `docs/m365/ea-*-*.md`.

[1.0.3]: https://github.com/numtip/document-center/releases/tag/document-center-v1.0.3
[1.0.2]: https://github.com/numtip/document-center/releases/tag/document-center-v1.0.2
[1.0.1]: https://github.com/numtip/document-center/releases/tag/document-center-v1.0.1
[1.0.0]: https://github.com/numtip/document-center/releases/tag/document-center-v1.0.0
