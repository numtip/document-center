# Canonical Repository Capability Audit — RAE Document Center

**Project:** RAE Document Center
**Canonical Repository:** `https://github.com/numtip/document-center`
**Branch audited:** `main` @ `885337daec17828c668dc3805ce7d6c6a83c1a7d`
**Auditor:** Co-Work A (Repository Reality Auditor)
**Date:** 2026-07-12

---

## Scope and Method

This audit inspects **only real, committed files present in the canonical `numtip/document-center` GitHub repository** at the commit above. Every classification in this document is backed by a file path that was directly read or a command that was directly executed in this repository during the audit.

**No second project was referenced or assumed as evidence.** Specifically:

- **No second project (`RAE-M365-Platform`) was referenced or assumed as evidence in this audit.** Only files present in `numtip/document-center` were inspected.
- Historical handoff claims embedded in some in-repo documents (e.g. "26 metadata fields," "10 domains," "21 site columns," `G:\ProjectAI\RAE-M365-Platform` as a "recovery source") are **not treated as evidence of anything** in this audit. Where those claims appear inside real committed files (`PROJECT_BASELINE.md`, `docs/architecture/EA_RECOVERY_GAP_MATRIX.md`, `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md`, `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md`), they are noted below strictly as **unverified assertions written into the repository**, not as proof that the referenced external artifacts exist. That external path does not exist on this machine and was not searched for or assumed present.
- Every row in the capability table below cites a real file path in this repository as evidence. Where a document describes a proposed/future capability, it is classified `PROPOSED` or `DOCUMENTED_ONLY`, never `IMPLEMENTED`.

---

## Capability Table

| # | Capability | Classification | Evidence (file path + brief description) |
|---|-------------|-----------------|--------------------------------------------|
| 1 | Taxonomy (category system) | **IMPLEMENTED** | `docs/document-center/taxonomy.json` — real, locked v1.0.0 taxonomy with **6 flat categories** (`admin`, `finance-procurement`, `research`, `academic-service`, `policy-planning`, `manuals`). Schema documented in `docs/document-center/REGISTRY_DATA_MODEL.md`. Actively consumed by `scripts/validate-document-registry.ts` and `scripts/validate-document-migration-matrix.ts`, both of which ran successfully against it during this audit. |
| 2 | Document registry / metadata schema | **IMPLEMENTED** | `docs/document-center/REGISTRY_DATA_MODEL.md` locks a 13-field document schema (`id, title, category, owner, file_type, status, updated_date, onedrive_path, storage_url, tags, version, visibility, note`). Real instances exist: `document-registry.example.json` (8 sample docs), `document-registry.draft.json` (40 docs, Phase 5A.6), `document-registry.audit.json`, `document-registry.remediated.json`. Validated successfully by `scripts/validate-document-registry.ts` during this audit (40/40 documents, 0 errors). |
| 3 | DocumentID standard | **IMPLEMENTED** | `docs/document-center/DOCUMENT_NAMING_STANDARD.md` defines the `RAE-DC-{NNNN}` format, versioning rules, and filename conventions. Duplicate-ID rejection is actively enforced in code by `scripts/validate-document-registry.ts` and `scripts/validate-document-migration-matrix.ts` (both checked and passed during this audit). No automated ID-*assignment* tool exists — IDs are assigned manually per the documented procedure. |
| 4 | Migration matrix tooling | **IMPLEMENTED** | `scripts/validate-document-migration-matrix.ts` — ran successfully during this audit against `docs/document-center/migration-matrix.v2.csv` (42 rows: 30 keep, 5 merge, 4 review, 2 drop, 1 rewrite; 0 errors). Wired into `package.json` as `npm run validate:matrix`. |
| 5 | Registry validation tooling | **IMPLEMENTED** | `scripts/validate-document-registry.ts` and `scripts/validate-remediated-registry.ts` both exist as working TypeScript/tsx scripts. `validate-document-registry.ts` ran successfully during this audit (40 documents, 0 errors) via `npm run validate:registry`. `validate-remediated-registry.ts` exists but is **not** wired into any `package.json` script — it must be invoked directly with `tsx`. |
| 6 | Registry generation tooling | **IMPLEMENTED** | Four working generator scripts exist in `scripts/`: `generate-registry-draft.ts` (CSV→JSON draft, wired as `npm run generate:registry`), `generate-onedrive-prep-map.ts` (wired as `npm run generate:prep-map`), `generate-audit-registry.ts` and `generate-remediated-registry.ts` (both exist and are complete, but **not** wired into `package.json` scripts — direct `tsx` invocation required). |
| 7 | GitHub Pages preview (public export) | **IMPLEMENTED** | `preview/` directory contains a real static site (`index.html`, `app.js`, `styles.css`, `data/public-registry.sample.json`, `data/taxonomy.sample.json`). `scripts/build-preview.ts` (wired as `npm run build`) validates that only `visibility=public` + `status=current` + demo `example.sharepoint.com` links ship, then builds to `dist/`. `.github/workflows/pages.yml` deploys `dist/` to the `gh-pages` branch on push to `main`. Build was not re-run in this audit beyond `validate:all`, but the script and workflow are real and self-consistent. |
| 8 | OneDrive storage model | **LEGACY** | This is the **current, active** storage architecture (not SharePoint). `README.md`: "Document files live in OneDrive; they are never stored in Git." `PROJECT_BASELINE.md`: "Architecture Status: OneDrive-based metadata registry with proposed M365 Foundation blueprint (not yet implemented)." Fully specified in `docs/document-center/PHASE3_ONEDRIVE_STORAGE_GUIDE.md` (explicitly labeled "Status: Documentation only (no implementation)"), `docs/document-center/DOCUMENT_NAMING_STANDARD.md`, and `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md`. No code provisions OneDrive folders; this is a manual, documentation-governed process that is nonetheless the live/intended architecture today. |
| 9 | SharePoint Online implementation | **MISSING** | No SharePoint site, library schema, content type, column, or view definition file exists anywhere in the repository (confirmed via directory search of `docs/`). The only SharePoint content is the *proposal* in `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-3, listing 6 target libraries and 9 metadata columns) — explicitly `Status: Proposed`. |
| 10 | Microsoft Lists implementation | **MISSING** | No Microsoft Lists schema, export, or provisioning file exists. Only a proposal exists: `docs/document-center/M365 FoundationBlueprint.MD` Phase M365-4 ("Microsoft Lists Registry," `RAE Document Registry` list, 10 proposed fields) — `Status: Proposed`, no implementation. |
| 11 | Power Automate workflows | **MISSING** | No flow definitions, exported `.zip`/JSON flow packages, or Power Automate configuration exist. Only a proposal exists: `docs/document-center/M365 FoundationBlueprint.MD` Phase M365-5 describes 3 conceptual workflows (Upload, Approval, Archive Control) at the diagram level only. |
| 12 | PnP provisioning scripts/IaC | **MISSING** | Confirmed via repository-wide file search: zero `.ps1` files, zero PnP cmdlet references, zero provisioning templates of any kind exist in the repository. `docs/architecture/EA_RECOVERY_GAP_MATRIX.md` (a real committed file) independently reaches the same conclusion: "No .ps1 files, no PnP-related scripts, no provisioning automation of any kind exist in GitHub." |
| 13 | M365 tenant capability audit | **MISSING** | No completed tenant audit, license inventory, or capability-checklist deliverable exists. `docs/document-center/M365 FoundationBlueprint.MD` Phase M365-1 only lists a 9-item checklist template (SharePoint Online, Microsoft Lists, Power Automate, Teams Approvals, Forms, Power BI, Graph API, Azure App Registration, Copilot) and names an undelivered artifact (`M365_LICENSE_AUDIT.md`) that does not exist in the repository. |
| 14 | Permission/governance model | **DOCUMENTED_ONLY** | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` is a complete, detailed policy: 6 roles (Platform Admin, Category Owner, Document Owner, Contributor, Reader, Archive Manager), folder-level permission matrix, share-link policy, quarterly audit checklist. This governs OneDrive access only — there is no SharePoint permission-group implementation, and no code in the repository enforces any of these roles; it is a policy document to be applied manually by humans. |
| 15 | UI/frontend blueprint (Next.js) | **DOCUMENTED_ONLY** (within this repo) | `docs/document-center/UI_BLUEPRINT.md` is an extensive, locked design spec (routes, page layouts, document card spec, search/filter behavior, badges, accessibility, performance budgets) explicitly for a future Next.js implementation — `Status: Blueprint locked for Phase 4B implementation`. No Next.js code, `package.json` Next.js dependency, or `/app`/`/pages` directory exists in this repository. `README.md` asserts "Production UI Implemented in [`rae-nextjs-main`]" — this is a claim about a *different, external* GitHub repository that was not inspected as part of this audit and is not evidence of anything inside `numtip/document-center`. The only working frontend code physically in this repository is the plain HTML/CSS/vanilla-JS GitHub Pages preview (`preview/app.js`), which is not Next.js and not the blueprinted UI. |
| 16 | Memory OS / AI agent context | **MISSING** | Repository-wide search for `.cursor/`, `CORE.md`, `AGENTS.md`, `SKILL.md`, and `*memory*` file patterns returned zero results. No AI agent context, rules, or "Memory OS" artifacts of any kind exist in this repository. |
| 17 | Git canonical governance | **DOCUMENTED_ONLY** (actively followed by convention) | `docs/governance/GIT_CANONICAL_VERSION_POLICY.md` (12 frozen rules: GitHub is canonical, no force-push to `main`, ADR required for architecture changes, secrets never in Git, etc.) and `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md` (branch/workstation model, divergence-handling procedures, mandatory `rtk` command prefix). Both are real, detailed policy documents. No code in the repository enforces these rules (e.g., no branch-protection config file, no CI check that blocks force-push); enforcement depends on GitHub repository settings (not inspectable from file contents) and human/process discipline. The existence of multiple correctly-named feature branches/worktrees (`cowork/git-centralization`, `cowork/ea-recovery-map`) is circumstantial evidence the convention is being actively followed in practice. |
| 18 | EA/M365 gap analysis (recovery docs) | **CONFLICTING** | `docs/architecture/EA_RECOVERY_GAP_MATRIX.md` and `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md` (both dated 2026-07-12, authored by "Co-Work B") are real committed files that **themselves assert the existence of** an external source `G:\ProjectAI\RAE-M365-Platform` containing 22+ claimed artifacts (10 taxonomy domains, 30 categories, 62 subcategories, 26 metadata fields, 21 site columns, PnP scripts, etc.), and `PROJECT_BASELINE.md` labels that same path "Active" as a "recovery source." This is a direct conflict with the confirmed fact (per current task context) that `G:\ProjectAI\RAE-M365-Platform` does not exist anywhere. The gap-matrix and manifest documents are internally well-reasoned (they correctly compare claims against real repo files and mark most items `MISSING`/`PARTIAL`), but their entire premise rests on an external source that has not been verified to exist. Treat the *comparisons against real repo files* in these documents as reliable; treat any *claim about `RAE-M365-Platform` contents* as unverified. |

---

## Summary Counts

| Classification | Count |
|-----------------|-------|
| IMPLEMENTED | 7 |
| DOCUMENTED_ONLY | 3 |
| LEGACY | 1 |
| MISSING | 6 |
| CONFLICTING | 1 |
| PROPOSED | 0 (folded into MISSING/DOCUMENTED_ONLY rows above — the M365 Blueprint's phases are the "proposed" content driving items 9–13) |
| **Total capability areas** | **18** |

Note on PROPOSED: no capability area was *purely* forward-looking with zero missing/documented evidence, so each proposal-backed area was classified by what's real today (`MISSING` for the M365/SharePoint/Lists/PowerAutomate/PnP/tenant-audit areas that only exist as text in `M365 FoundationBlueprint.MD`). The blueprint document itself is explicitly self-labeled `Status: Proposed` and is the sole source for items 9–13.

---

## Ready for Immediate Use (IMPLEMENTED)

These capability areas have real, working tooling in the repository today and can be used immediately without further build-out:

1. **Taxonomy system** — `taxonomy.json` is a valid, locked, machine-readable category list consumed by validators.
2. **Document registry schema + sample data** — `REGISTRY_DATA_MODEL.md` + `document-registry.example.json`/`document-registry.draft.json` are ready to drive a UI or further tooling.
3. **DocumentID uniqueness enforcement** — duplicate-ID checks work today via the validator scripts.
4. **Migration matrix validation** — `npm run validate:matrix` runs clean against the current 42-row CSV.
5. **Registry validation** — `npm run validate:registry` runs clean against the current 40-document draft registry.
6. **Registry generation scripts** — CSV→JSON draft generation (`npm run generate:registry`) and OneDrive prep-map generation (`npm run generate:prep-map`) both work; two additional generator scripts (`generate-audit-registry.ts`, `generate-remediated-registry.ts`) work but need manual `tsx` invocation since they aren't wired into `package.json`.
7. **GitHub Pages preview pipeline** — `build-preview.ts` + `.github/workflows/pages.yml` form a working, guarded static-export pipeline (blocks non-public/non-demo data from shipping).

`npm --prefix . install` followed by `npm run validate:all` was executed during this audit and passed with **zero errors** against the current repository state.

---

## Missing and Would Block SharePoint/M365 Work Today

If SharePoint/M365 implementation work started today, these gaps would immediately block it:

1. **No SharePoint site/library/content-type/column/view definitions exist** — Phase M365-3 of the Blueprint names deliverables (`sharepoint-site-design.md`, `library-schema.md`) that were never created. Nothing to provision from.
2. **No Microsoft Lists schema** — Phase M365-4's `RAE Document Registry` list (`registry-list-schema.md`) does not exist; only a 10-field bullet list in the Blueprint.
3. **No Power Automate flow definitions** — Phase M365-5's three workflows (Upload, Approval, Archive Control) are diagram-level only; no flow logic, connectors, or triggers are specified in enough detail to build from, let alone implemented.
4. **No PnP or any other provisioning/IaC scripts** — confirmed zero `.ps1` files or provisioning templates repository-wide. Any SharePoint site would have to be provisioned entirely from scratch (manually or by writing new IaC).
5. **No completed M365 tenant capability audit** — the Blueprint's own Phase M365-1 deliverable (`M365_LICENSE_AUDIT.md`) was never produced. It is unknown from repository evidence whether the target tenant even has the licenses (SharePoint Online, Power Automate, Lists, Teams Approvals, Power BI, Graph API app registration access, Copilot) that the rest of the Blueprint depends on.
6. **Taxonomy is a flat 6-category list, not the hierarchical model referenced in the EA gap-matrix docs** — `taxonomy.json` v1.0.0 has no domain/subcategory/document-type layers. If SharePoint content types and site columns were to be modeled after a richer taxonomy, that taxonomy does not yet exist as a real file (the "10 domains / 30 categories / 62 subcategories" figures appear only as *unverified claims* inside `EA_RECOVERY_GAP_MATRIX.md`, not as an actual taxonomy file).
7. **Registry schema (13 fields) has no SharePoint/Lists column-type mapping** — `REGISTRY_DATA_MODEL.md` defines string/array/boolean-level fields for a flat JSON registry; none are mapped to SharePoint column types (choice, person, managed metadata, etc.), content types, or list relationships.
8. **No M365-wide permission model** — `ONEDRIVE_PERMISSION_POLICY.md` covers OneDrive only; there is no SharePoint permission-group design, no AD/Entra group mapping, and no Power Automate/Teams governance-channel setup.
9. **No Memory OS / AI agent context in-repo** — any AI-assisted M365 build-out would start with zero persisted project context inside this repository.

---

*No second project (RAE-M365-Platform) was referenced or assumed as evidence in this audit. Only files present in numtip/document-center were inspected.*
