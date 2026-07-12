# Canonical Architecture Correction Plan

**Project:** RAE Document Center
**Canonical repository:** `https://github.com/numtip/document-center`
**Authority:** Sonnet-5 QC Commander, 2026-07-12
**Basis:** [`CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md`](./CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md) (Co-Work A) + [`INVALID_RECOVERY_ASSUMPTION_REVIEW.md`](./INVALID_RECOVERY_ASSUMPTION_REVIEW.md) (Co-Work B)

---

## Context

A prior task incorrectly assumed a second project, `RAE-M365-Platform`, existed at `G:\ProjectAI\RAE-M365-Platform` as a historical recovery source. This assumption is **confirmed false** — no such path exists on any accessible machine. There is, and has only ever been, **one canonical project**: `numtip/document-center` on GitHub.

This plan is **not a recovery plan**. It defines how to move the project **forward** from the real, verified state of the canonical repository.

---

## 1. Recovery Documents Requiring Correction

| Document | Correction Required |
|----------|---------------------|
| `PROJECT_BASELINE.md` | Remove "Known Archives for Recovery" section and its blockquote. Replace with: "No external recovery sources exist. This repository is the sole source of project history." |
| `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md` | Remove the `RAE-M365-Platform` diagram node (§1), the hierarchy table row (§2), and §6 "Recovery Source Status" in its entirety. Renumber trailing sections. Rewrite the "no active project development outside Git" sentence as unconditional (never depended on a recovery step). |
| `docs/architecture/EA_RECOVERY_GAP_MATRIX.md` | Remove the "WORK PC source (claimed)" header. Rename "Recovery Priority" column to "Implementation Priority." Change `RECOVERY_REQUIRED_BEFORE_EA_3F` decision label to `FORWARD_IMPLEMENTATION_REQUIRED_BEFORE_EA_3F`. Replace "Recommended path" step 1 (recover from runbook) with a forward-design step. Reword speculative "WORK PC may have..." notes as forward design options. |
| `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md` | Remove "Recovery source" / "Canonical target (WORK PC checkout)" header framing. Delete the fabricated "Likely File/Path Pattern" column entirely. Remap "Import Classification" vocabulary to forward-implementation actions: `IMPORT_AS_AUTHORITATIVE` → `BUILD_NEW`, `MERGE_WITH_EXISTING` → `EXTEND_EXISTING`, `REQUIRES_ADR_REVIEW` → `NEEDS_ADR`. Drop `RETAIN_AS_HISTORICAL` / `DO_NOT_IMPORT_DUPLICATE` (both presuppose a discoverable source). Re-derive the "Recovery Item Count" as an "Items requiring forward implementation" count. |

## 2. Documents Remaining as Historical Audit Evidence

| Document | Disposition |
|----------|-------------|
| `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md` | **STALE_ASSUMPTION** — no salvageable content once the recovery premise is removed. Retire in place: replace body with a short pointer noting the assumption was investigated and found false, linking to `INVALID_RECOVERY_ASSUMPTION_REVIEW.md`. Original content remains recoverable via Git history (commits `d9f5c37`, `729b5ad`, `64eed3f`) — not deleted from history, only retired from active guidance. |
| `docs/architecture/CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md` | Retain as-is — this is the factual, evidence-based capability audit that supersedes any handoff claims. |
| `docs/architecture/INVALID_RECOVERY_ASSUMPTION_REVIEW.md` | Retain as-is — permanent record of the false assumption, its impact, and the corrections it necessitated. |

## 3. Invalid RAE-M365-Platform References Requiring Removal

All 45 line-level references across the 5 documents cataloged in `INVALID_RECOVERY_ASSUMPTION_REVIEW.md` must be removed or reframed per the table in §1 above. No new references to `RAE-M365-Platform`, `G:\ProjectAI\RAE-M365-Platform`, or `recovery/ea-m365-baseline` are permitted anywhere in the repository going forward.

## 4. Current Repository Artifacts That Are Reusable

Per the Capability Audit, these are real, working, and usable today without further build-out:

1. **Taxonomy system** — `docs/document-center/taxonomy.json` (6 flat categories, locked v1.0.0)
2. **Document registry schema + sample data** — `REGISTRY_DATA_MODEL.md` (13 fields) + example/draft registries
3. **DocumentID uniqueness enforcement** — `RAE-DC-{NNNN}` format, validated by scripts
4. **Migration matrix validation** — `npm run validate:matrix` (42 rows, 0 errors)
5. **Registry validation** — `npm run validate:registry` (40 docs, 0 errors)
6. **Registry generation scripts** — CSV→JSON draft + OneDrive prep-map generation
7. **GitHub Pages preview pipeline** — guarded static-export build, deployed via `gh-pages`

## 5. M365 Capabilities That Are Only Proposed

Per the Capability Audit (`MISSING`, backed solely by the self-labeled `Status: Proposed` M365 Foundation Blueprint):

- SharePoint Online site/library/content-type/column/view definitions
- Microsoft Lists schema
- Power Automate flow definitions
- PnP provisioning scripts / IaC
- Completed M365 tenant capability audit (`M365_LICENSE_AUDIT.md` was never produced)

## 6. EA Capabilities That Are Genuinely Missing

These gaps are **real** (confirmed by direct file inspection, not by unverified handoff claims) and cannot be closed by import since no external source exists:

- Hierarchical taxonomy (10 domains / 30 categories / 62 subcategories / 11 document types) — only a flat 6-category list exists
- Extended metadata registry (26 fields claimed vs. 13 real fields) — no evidence of the extended set anywhere in Git
- SharePoint site columns (21), content types (11), views (8), permission groups (6) — zero exist
- PnP PowerShell provisioning scripts — zero exist
- M365 admin questions / tenant capability checklist / integration decision matrix — zero exist as completed deliverables
- Public export policy, AI source eligibility policy — zero exist
- Memory OS / AI agent context — zero exist in this repository

**These gaps are not "missing recoverable files" — they are "never-built artifacts."** The only path to closing them is designing and authoring them directly against the canonical repository.

## 7. Can EA-3F Start From the Current Canonical Repository?

**No.** EA-3F (SharePoint Provisioning Readiness Gate) requires, at minimum, a SharePoint site design, library/content-type/column schema, and a mature taxonomy to provision against. None of these exist as real, implementable artifacts in the canonical repository today — only a proposed 9-phase blueprint at the concept level.

## 8. Is a Controlled Forward Implementation Phase Required First?

**Yes.** Before EA-3F can begin, the canonical repository needs a forward-implementation phase that:

1. Corrects the 5 stale governance/recovery documents per §1 above
2. Designs (not recovers) the missing SharePoint foundation artifacts (site design, library schema, content types, columns, views, permission groups)
3. Resolves via ADR: whether to adopt a hierarchical taxonomy v2, extend the registry schema, and choose a provisioning tooling approach (PnP vs. the existing TypeScript/tsx validation stack)
4. Produces the M365 tenant capability audit as a real, completed artifact (not a checklist template)
5. Authors the missing governance policies (public export, AI source eligibility)

This is forward design-and-build work, not recovery — there is nothing to recover.

---

## Summary

| Question | Answer |
|----------|--------|
| Does RAE-M365-Platform exist? | **NO** |
| Is there a historical recovery source? | **NO** |
| Are the EA-3A–3E gaps real? | **YES** — confirmed by direct GitHub file inspection |
| Can the gaps be closed by import? | **NO** — nothing to import from |
| Is EA-3F ready to start today? | **NO** |
| Is a forward-implementation phase required first? | **YES** |
