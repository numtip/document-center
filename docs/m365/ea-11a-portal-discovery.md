# EA-11A — Portal Discovery

**Date**: 2026-07-16  
**Repository**: `G:\ProjectAI\document-center`  
**Migration baseline**: 627 SharePoint files · 627 Registry rows · EA-10 commit `a787f30`

---

## Candidate Portals

| Portal Name | URL | Deployment Type | Repository Source | Status |
|-------------|-----|-----------------|-------------------|--------|
| **RAE Document Center (SharePoint)** | `https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx` | SharePoint Modern Site Page + List web part | Provisioned EA-3I; integrated EA-7B/7C | **PRODUCTION (operational)** |
| **RAE Document Registry (SharePoint List)** | `https://maejo365.sharepoint.com/sites/msteams_54adc4/Lists/RAE%20Document%20Registry/AllItems.aspx` | SharePoint List view | `_registry_upsert.py` / EA-8 sync | **PRODUCTION (metadata layer)** |
| **Six Document Libraries** | `…/Administration`, `FinanceProcurement`, `PlanningPolicy`, `AcademicServices`, `Research`, `SOPManuals` | SharePoint document libraries | EA-6–EA-10 migration | **PRODUCTION (file storage)** |
| **SharePoint Native Search** | `https://maejo365.sharepoint.com/sites/msteams_54adc4/_layouts/15/search.aspx` | SharePoint search | EA-7B Quick Links / hero chips | **PRODUCTION (search entry)** |
| **GitHub Pages Preview** | `https://numtip.github.io/document-center/` | Static site (`gh-pages` branch) | `preview/` + `.github/workflows/pages.yml` | **PREVIEW (demo only)** |
| **Next.js Document Center** | Not deployed from this repo | Next.js (planned) | External: `github.com/numtip/rae-nextjs-main` | **STAGING / PLANNED** |
| **Registry draft JSON (authoring)** | N/A (not a portal) | Git metadata file | `docs/document-center/document-registry.draft.json` | **ARCHIVED / authoring** |

---

## Classification

| Endpoint | Role |
|----------|------|
| SharePoint Site Page + Registry + Libraries | **PRODUCTION** — where migrated corpus lives and is browsed today |
| GitHub Pages | **PREVIEW** — UI mock with 3 sample records; README explicitly excludes production |
| Next.js (`rae-nextjs-main`) | **STAGING / PLANNED** — documented target public portal; consumes future Registry export JSON |
| Registry draft in Git | **ARCHIVED / authoring** — not user-facing |

---

## Evidence Sources

- `README.md` — “Production UI implemented in rae-nextjs-main”; Pages = preview/demo only
- `docs/m365/ea-3i-provisioning-report.md` — `RAE-Document-Center.aspx` provisioned
- `docs/m365/ea-7b-operational-document-center-report.md` — Registry List web part, 6-library Quick Links
- `docs/m365/ea-7c-operational-ux-completion-report.md` — UX completion on same page
- `.migration/rae-wtms/ea-11/ea-11-final-summary.json` — 627/627/627 reconciliation
- `scripts/build-preview.ts` — blocks non-demo URLs from Pages build

---

## Where the 627-Document Corpus Is Exposed

| Layer | Exposed? | Count |
|-------|----------|------:|
| SharePoint libraries (files) | Yes | 627 DocumentIDs |
| RAE Document Registry (List) | Yes | 627 rows |
| SharePoint DC landing page (Registry web part) | Yes | Live Registry view |
| GitHub Pages | No | 3 sample records |
| Next.js portal | Not verified / not in repo | Unknown |

**Conclusion**: The migrated corpus is exposed on **SharePoint** (libraries + Registry + Document Center page). GitHub Pages is **not** the production portal.
