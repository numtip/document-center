# Reference Standards

**Version**: 1.0.1  
**Effective**: 2026-07-16  
**Status**: NORMATIVE — future projects must reference these standards

---

## 1. Metadata

| Field | Standard | Source |
|-------|----------|--------|
| DocumentID | `RAE-NNNNN` (5-digit zero-padded) | Manifest; immutable |
| Title | Thai/English as authored in manifest | Manifest |
| Category1 | Subcategory slug from taxonomy | Manifest |
| Owner | `TBD` until governance activation | Placeholder (EA-6C deferred) |
| DocumentStatus | `LegacyImported` for migrated corpus | SharePoint column |
| PublicVisibility | `PendingReview` for migrated corpus | SharePoint column |
| LegacySourceURL | Original WTMS URL | Manifest |
| Source System | `WTMS` for migrated documents | Registry |

**Rule**: Metadata is applied at upload time via ValidateUpdateListItem; Registry sync propagates to List.

---

## 2. Registry

| Property | Standard |
|----------|----------|
| List name | `RAE Document Registry` |
| Idempotency key | DocumentID |
| Upsert mode | AUTO_UPSERT |
| Sync tool | `_ea8_registry_sync.py --sync-all` |
| Critical fields | DocumentID, Title, Category, Storage URL, Status, Visibility, Source System |

Export contract: `docs/m365/registry-export-contract.md`

---

## 3. Document IDs

| Rule | Value |
|------|-------|
| Format | `RAE-` + 5 digits (`RAE-00001` … `RAE-99999`) |
| Uniqueness | One DocumentID per logical document across all libraries |
| Filename | `{DocumentID}{extension}` in SharePoint |
| Collision | Zero tolerance — stop and escalate |

Preview demo IDs (`RAE-DC-0001`) are **not** production format.

---

## 4. Status Values

| Layer | Allowed values (v1.0) |
|-------|----------------------|
| Manifest MigrationStatus | `Ready` (migrated corpus) |
| SharePoint DocumentStatus | `LegacyImported` |
| Registry Status | `draft` |
| Migration UploadStatus | `UPLOADED_OK` / `OK` |
| Migration RegistryStatus | `AUTO_UPSERT` |

Future governance may introduce: `current`, `archived`, `superseded`. Requires ADR.

---

## 5. Visibility

| Layer | v1.0 value |
|-------|------------|
| SharePoint PublicVisibility | `PendingReview` |
| Registry Visibility | `internal` |
| GitHub Pages preview | `public` (demo records only) |
| Export eligibility | `visibility=public` + `status=current` (future) |

Tenant anonymous access: not enabled (AUTH_REQUIRED).

---

## 6. Naming

| Asset | Convention |
|-------|------------|
| SharePoint file | `{DocumentID}{ext}` |
| Library | PascalCase English (`Research`, `SOPManuals`) |
| Category slug | kebab-case (`finance-procurement`, `policy-planning`) |
| ADR file | `ADR-NNN-short-title.md` |
| Phase report | `ea-NN-description-report.md` |
| Script prefix | `_eaNN_` for phase-specific tools |

---

## 7. Libraries

| Library | Category slug | Role |
|---------|---------------|------|
| Administration | `admin` | Admin documents |
| FinanceProcurement | `finance-procurement` | Finance & procurement |
| PlanningPolicy | `policy-planning` | Policy & planning |
| AcademicServices | `academic-service` | Academic services |
| Research | `research` | Research documents |
| SOPManuals | `manuals` | SOPs & manuals |

**Frozen at v1.0**: No additional libraries without ADR and acceptance update.

---

## 8. Taxonomy

Authoritative taxonomy: `docs/document-center/taxonomy.json`

| Level | Description |
|-------|-------------|
| Category | Top-level grouping (maps to library) |
| Subcategory | Category1 metadata value |
| Tags | Optional; applied at export/preview |

Future projects must not invent parallel taxonomies without ADR.

---

## 9. Search

| Environment | Search mechanism |
|-------------|------------------|
| SharePoint production | Native site/library search |
| Registry admin | List views and filters |
| GitHub Pages preview | Client-side filter on 3 demo records |
| Future Next.js | Fuse.js fuzzy search (planned — not implemented) |

Search indexing lag (`PENDING_INDEX`) is acceptable if direct Storage URL resolves.

---

## 10. Portal Integration

| Portal | URL | Data source | Role |
|--------|-----|-------------|------|
| Production | SharePoint Document Center page | Registry List web part | Operational |
| Registry admin | Registry AllItems.aspx | SharePoint List | Metadata admin |
| Preview | `numtip.github.io/document-center/` | `public-registry.sample.json` | UI demo (3 records) |
| Future public | `rae-nextjs-main` | Registry export JSON | Public portal |

**Rule**: Portals consume metadata; SharePoint libraries hold files. See [ADR-002](../adr/ADR-002-website-presentation-layer.md).

---

## Compliance

Projects deviating from these standards must:

1. Submit an ADR explaining the deviation
2. Reference this document and the baseline
3. Obtain architecture approval before implementation
