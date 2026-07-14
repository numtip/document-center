# EA Forward Implementation Baseline — RAE Document Center

**Version:** 1.0  
**Status:** Approved  
**Authority:** EA-3F Canonical Baseline Correction  
**Date:** 2026-07-12  
**Canonical repository:** `numtip/document-center` (GitHub)

---

## Purpose

Define the canonical current state of the RAE Document Center using repository evidence only — no external sources, no unverified claims, no historical recovery assumptions. This baseline is the sole starting point for all forward architecture work.

---

## Canonical Source-of-Truth Boundaries

| Layer | Canonical Source | Authority |
|-------|-----------------|-----------|
| Code, schemas, validated exports | `numtip/document-center` (GitHub) | Single source of truth |
| Operational governance | M365 (target — not yet provisioned) | Future target |
| Document file storage | OneDrive (current) / SharePoint Online (target) | Current = OneDrive; Target = SharePoint |
| Authoritative metadata registry | Microsoft Lists (target — not yet provisioned) | Future target |
| Presentation / discovery | Next.js Portal / GitHub Pages preview | Presentation layer only |
| Code/schema governance | GitHub | Pull requests, ADRs, validations |

---

## Implemented Capabilities

These capabilities have real, working implementations in the canonical repository. Evidence is from `CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md` (Co-Work A).

| # | Capability | Evidence |
|---|------------|----------|
| 1 | Taxonomy system (6 flat categories, v1.0.0) | `docs/document-center/taxonomy.json` — locked, consumed by validators |
| 2 | Document registry schema (13 fields) | `docs/document-center/REGISTRY_DATA_MODEL.md` — locked data model |
| 3 | DocumentID standard (`RAE-DC-{NNNN}`) | `docs/document-center/DOCUMENT_NAMING_STANDARD.md` — enforced by validators |
| 4 | Migration matrix validation | `npm run validate:matrix` — 42 rows, 0 errors |
| 5 | Registry validation | `npm run validate:registry` — 40 documents, 0 errors |
| 6 | Registry generation scripts | CSV→JSON draft, OneDrive prep-map generation, audit/remediated generation |
| 7 | GitHub Pages preview pipeline | Guarded static-export build, deployed via `gh-pages` |
| 8 | Document registry instances (example/draft/audit/remediated) | Real JSON instances with validated data |

---

## Documented-Only Capabilities

These capabilities have detailed specification documents but no implementation.

| # | Capability | Evidence |
|---|------------|----------|
| 1 | OneDrive storage model | `PHASE3_ONEDRIVE_STORAGE_GUIDE.md` — explicitly labeled "Documentation only (no implementation)" |
| 2 | Permission / governance model | `ONEDRIVE_PERMISSION_POLICY.md` — 6-role model, manually applied, not enforced by code |
| 3 | UI/frontend blueprint | `UI_BLUEPRINT.md` — locked design spec for future Next.js implementation |
| 4 | Git canonical governance | `GIT_CANONICAL_VERSION_POLICY.md` + `REPOSITORY_CONVERGENCE_MODEL.md` — documented, followed by convention |
| 5 | M365 Foundation Blueprint | `M365 FoundationBlueprint.MD` — 9-phase plan, explicitly self-labeled `Status: Proposed` |

---

## Legacy Capability

| Capability | Status | Note |
|------------|--------|------|
| OneDrive document storage | **LEGACY** | Current active storage architecture. This is the live operational model, not a proposed target. SharePoint Online is the target replacement. |

---

## Missing Capabilities

These capabilities are **absent** from the canonical repository. They were never built — there is nothing to recover.

| # | Capability | Evidence of Absence |
|---|------------|-------------------|
| 1 | SharePoint Online site/library/content-type/column/view definitions | No SharePoint schema files exist; only a proposal in M365 Blueprint Phase M365-3 |
| 2 | Microsoft Lists schema | No Lists schema exists; only a 10-field bullet list in M365 Blueprint Phase M365-4 |
| 3 | Power Automate workflow definitions | No flow definitions exist; only a diagram-level description in M365 Blueprint Phase M365-5 |
| 4 | PnP provisioning scripts / IaC | Zero `.ps1` files or provisioning templates repository-wide |
| 5 | M365 tenant capability audit | `M365_LICENSE_AUDIT.md` (named deliverable from Blueprint Phase M365-1) does not exist |
| 6 | Hierarchical taxonomy (10 domains / 30 categories / 62 subcategories / 11 document types) | Only flat 6-category `taxonomy.json` exists |
| 7 | Extended metadata registry (26 fields) | Only 13-field `REGISTRY_DATA_MODEL.md` exists |
| 8 | M365-wide permission model | `ONEDRIVE_PERMISSION_POLICY.md` covers OneDrive only; no SharePoint/AD group mapping |
| 9 | Public export policy | No formal policy document exists |
| 10 | AI source eligibility policy | No policy document exists |
| 11 | Memory OS / AI agent context | No `.cursor/`, `CORE.md`, `AGENTS.md`, or `SKILL.md` files exist |

---

## Conflicting Artifacts Resolved

| Conflict | Resolution |
|----------|-----------|
| "Known Archives for Recovery" in `PROJECT_BASELINE.md` claiming `G:\ProjectAI\RAE-M365-Platform` as Active recovery source | Removed. No external recovery source exists. Repository is sole source of project history. |
| `REPOSITORY_CONVERGENCE_MODEL.md` including RAE-M365-Platform as a model node and §6 as Recovery Source Status | Removed. Model now shows only canonical GitHub + feature branches + HOME/WORK checkouts. |
| `EA_RECOVERY_GAP_MATRIX.md` framed as recovery from WORK PC | Reframed as forward implementation priority. Decision changed from `RECOVERY_REQUIRED_BEFORE_EA_3F` to `FORWARD_IMPLEMENTATION_REQUIRED_BEFORE_EA_3F`. |
| `EA_LEGACY_RECOVERY_MANIFEST.md` structured for import from nonexistent source | Restructured as forward implementation manifest with `BUILD_NEW` / `EXTEND_EXISTING` / `NEEDS_ADR` classifications. |
| `EA_WORK_PC_RECOVERY_RUNBOOK.md` entire premise based on false assumption | Retired in place. Body replaced with historical note and cross-reference to audit evidence. |

---

## Forward Architecture Position Statements

These statements are binding for all forward EA work.

### OneDrive Model

**Current OneDrive model is legacy architecture.** It is the live, operational storage model today but is explicitly designated as legacy. Forward architecture must target SharePoint Online as the replacement without disrupting current operational documents. Migration compatibility must be preserved.

### SharePoint Online

**SharePoint Online is target architecture, not recovered architecture.** No SharePoint artifacts existed in any external source that could have been imported. All SharePoint site designs, library schemas, content types, columns, views, and permission groups must be designed and authored directly against the canonical repository. This is forward design work, not recovery.

### Microsoft Lists

**Microsoft Lists is the target authoritative metadata registry.** The current JSON-based document registry (`REGISTRY_DATA_MODEL.md`, `document-registry.draft.json`) is the real, validated predecessor. Microsoft Lists will become the authoritative source of record. The JSON registry serves as the schema template and migration baseline. No Lists schema has been created yet — this is forward implementation.

### GitHub Governance

**GitHub remains code/schema/export governance.** The canonical repository governs:
- Validation scripts and tooling
- Taxonomy and registry schema definitions
- Architecture Decision Records
- Validated static exports (public registry JSON)
- CI/CD pipelines (Pages preview, validation)
- Governance policies and runbooks

GitHub does not store:
- Real document files (OneDrive / SharePoint)
- M365 credentials or authentication artifacts
- Operational M365 configuration not represented as code

### Presentation / Discovery Layer

**Next.js / public preview remains presentation and discovery layer only.** The GitHub Pages preview is the current working implementation. The future Next.js portal (documented in `UI_BLUEPRINT.md`) will:
- Search, browse, filter, and download documents
- Display public metadata only
- Never store master files
- Never manage approval workflows
- Never maintain authoritative metadata

The website is not file storage. The website is not a workflow system.

---

## Pre-Integration Architecture Constraint

**Scheduled registry export JSON is the preferred first integration phase.** The M365 Blueprint Phase M365-8 identifies two integration options — Graph API (Option A) and Scheduled Registry Export JSON (Option B) — and prefers Option B for static hosting simplicity. The first integration phase between GitHub governance and M365 operations should use a scheduled JSON export from Microsoft Lists to GitHub, validated by the existing `build-preview.ts` pipeline.

This does not preclude Graph API integration in a later phase. It establishes the minimal viable integration path.

---

## Related Documents

- [Canonical Repository Capability Audit](./CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md) — full evidence-based capability audit
- [Invalid Recovery Assumption Review](./INVALID_RECOVERY_ASSUMPTION_REVIEW.md) — catalog of the false assumption and corrections
- [Canonical Architecture Correction Plan](./CANONICAL_ARCHITECTURE_CORRECTION_PLAN.md) — correction plan governing this baseline
- [Forward Implementation Manifest](./EA_LEGACY_RECOVERY_MANIFEST.md) — per-item implementation classification
- [Gap Matrix (Forward Implementation View)](./EA_RECOVERY_GAP_MATRIX.md) — prioritized gap analysis
