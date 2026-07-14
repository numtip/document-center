# M365-3 Design Readiness Report — RAE Document Center

**Phase:** M365-3 — SharePoint Foundation  
**Status:** Design Complete (pre-implementation)  
**Report Date:** 2026-07-13  
**Author:** RAE Digital Transformation  
**Blueprint ref:** `docs/document-center/M365 FoundationBlueprint.MD` §Phase M365-3

---

## 1. Executive Summary

Phase M365-3 SharePoint Libraries Design is **complete**. All 6 document libraries have been designed with a consistent schema derived from the actual migration manifest (772 rows). The design respects the existing blueprint, taxonomy, naming standard, and permission policy without redesigning from scratch.

| Item | Status |
|------|--------|
| Site Design | ✅ Complete |
| Library Schema (6 libraries) | ✅ Complete |
| Content Types (4 types) | ✅ Complete |
| Permissions Matrix | ✅ Complete |
| Migration Field Map | ✅ Complete |
| Manifest Coverage (772 rows) | ✅ 100% mapped |
| Metadata-only handling | ✅ No dummy files |
| Duplicate handling | ✅ No re-upload |
| Owner=TBD support | ✅ Allowed |
| PendingReview support | ✅ Default for all imports |

---

## 2. Documents Created

| File | Purpose | Lines |
|------|---------|-------|
| `docs/m365/sharepoint-site-design.md` | Site, libraries, folder structure, versioning, retention | ~230 |
| `docs/m365/library-schema.md` | 15-column schema, allowed values, views, validation rules | ~270 |
| `docs/m365/content-types.md` | 4 content types, hierarchy, field defaults, term set | ~215 |
| `docs/m365/permissions-matrix.md` | Roles, site/library/folder/document permissions, audit | ~195 |
| `docs/m365/migration-field-map.csv` | 19-row field mapping: manifest → SharePoint column | CSV |
| `docs/m365/m365-3-readiness-report.md` | This report | — |

---

## 3. Schema Summary

### 3.1 Site

| Property | Value |
|----------|-------|
| Site Name | RAE Document Center |
| Site Type | SharePoint Team Site |
| Suggested URL | `https://[tenant].sharepoint.com/sites/RAE-DocumentCenter` |
| Language | Thai (th-TH) |
| External sharing | Disabled by default |

### 3.2 Libraries

| Library | Taxonomy ID | Thai Name | Total Rows | Files | Metadata-Only |
|---------|-------------|-----------|-----------|-------|---------------|
| Administration | `admin` | งานบริหารและธุรการ | 42 | 9 | 33 |
| FinanceProcurement | `finance-procurement` | งานคลังและพัสดุ | 35 | 20 | 15 |
| PlanningPolicy | `policy-planning` | งานนโยบาย แผนและประกันคุณภาพ | 57 | 10 | 47 |
| AcademicServices | `academic-service` | งานบริการวิชาการ | 47 | 43 | 4 |
| Research | `research` | งานวิจัย | 576 | 530 (+45 dup) | 1 |
| SOPManuals | `manuals` | คู่มือปฏิบัติงาน | 15 | 15 | 0 |
| **Total** | | | **772** | **627** | **100** |

### 3.3 Columns (15 total)

| # | Column | Type | Required | Default |
|---|--------|------|----------|---------|
| 1 | `DocumentID` | Text | Yes | auto |
| 2 | `Title` | Text (built-in) | Yes | derived |
| 3 | `Category` | Text | Yes | taxonomy slug |
| 4 | `Subcategory` | Text | Yes | folder name |
| 5 | `Owner` | Text | Yes | `TBD` |
| 6 | `DocumentStatus` | Choice | Yes | `LegacyImported` |
| 7 | `Version` | Text | No | `1.0` |
| 8 | `UpdatedDate` | Date | No | upload date |
| 9 | `Tags` | Managed Metadata | No | _(empty)_ |
| 10 | `PublicVisibility` | Choice | Yes | `PendingReview` |
| 11 | `LegacySourceURL` | Hyperlink | No | from manifest |
| 12 | `MigrationStatus` | Choice | Yes | `Ready` |
| 13 | `SHA256` | Text | No | from manifest |
| 14 | `DuplicateOf` | Text | No | from manifest |
| 15 | `Notes` | Multi-text | No | _(empty)_ |

### 3.4 Content Types

| Content Type | Record Count | File? | Notes |
|---|---|---|---|
| `RAE Legacy Document` | 627 | Yes | All migrated physical files |
| `RAE Duplicate Reference` | 45 | No | Link record; no file upload |
| `RAE Active Document` | 0 now | Yes | New documents post-migration |
| `RAE Metadata Record` | 100 | No | Microsoft Lists only; no dummy files |

---

## 4. Manifest Coverage Verification

Confirming all 772 manifest rows are covered by the schema:

| Check | Expected | Design Status |
|-------|----------|---------------|
| All rows have `TargetLibrary` | 772 | ✅ All 6 libraries defined |
| All rows have valid `DocumentStatus` | 772 | ✅ `LegacyImported` default |
| All rows have `PublicVisibility` | 772 | ✅ `PendingReview` default |
| All rows have `Owner` | 772 | ✅ `TBD` is valid |
| Metadata-only rows (100): no dummy files | 100 | ✅ `RAE Metadata Record` in Lists only |
| Duplicate rows (45): no re-upload | 45 | ✅ `RAE Duplicate Reference` CT; no file |
| Ready rows (627): SHA-256 verified | 627 | ✅ All SHAs verified (mismatch=0) |
| `DuplicateOf` populated for all 45 dups | 45 | ✅ All 45 have DuplicateOf value |
| Unknown `TargetLibrary` | 0 | ✅ None |
| Unknown `Category/Subcategory` | 0 | ✅ All 23 subcategories mapped |

---

## 5. Field Mapping Completeness

From `migration-field-map.csv` (19 rows):

| Manifest Field | SP Column | Status |
|---|---|---|
| `DocumentID` | `RAE_DocumentID` | ✅ Direct |
| `Title` | `Title` (built-in) | ✅ With derivation fallback |
| `Category` | `RAE_Category` | ✅ With taxonomy slug mapping |
| `Subcategory` | `RAE_Subcategory` | ✅ Direct |
| `Owner` | `RAE_Owner` | ✅ TBD allowed |
| `Status` | `RAE_DocumentStatus` | ✅ `LegacyImported` default |
| `PublicVisibility` | `RAE_PublicVisibility` | ✅ `PendingReview` default |
| `SourceURL` | `RAE_LegacySourceURL` | ✅ Hyperlink |
| `LocalRelativePath` | _(upload tooling only)_ | ✅ Not stored in SP |
| `SHA256` | `RAE_SHA256` | ✅ Verification hash |
| `DuplicateOf` | `RAE_DuplicateOf` | ✅ Reference to primary |
| `MigrationStatus` | `RAE_MigrationStatus` | ✅ Direct |
| `Notes` | `RAE_Notes` | ✅ Direct |
| `Version` | `RAE_Version` | ✅ Default 1.0 |
| `UpdatedDate` | `RAE_UpdatedDate` | ✅ Upload date default |
| `Tags` | `RAE_Tags` | ✅ Empty at import |
| `link_text` (audit) | `Title` fallback | ✅ Derivation rule defined |
| `original_filename` (audit) | `Title` fallback | ✅ Derivation rule defined |
| `mapping_status` (audit) | (informational) | ✅ Not stored in SP |

**No missing fields.**

---

## 6. Special Case Handling

### 6.1 Owner = TBD

- ✅ Column allows `TBD` as a valid string value
- ✅ Default value set to `TBD` for all migrated documents
- ✅ Power Automate (Phase M365-5) will send reminder to Category Owners monthly
- ✅ View "Pending Owner Assignment" shows all `Owner = TBD` rows
- 🔲 Named owners to be confirmed before portal launch (Phase M365-8)

### 6.2 PublicVisibility = PendingReview

- ✅ `PendingReview` is a defined allowed value
- ✅ All 772 import rows default to `PendingReview`
- ✅ No share link created; no portal exposure
- ✅ Category Owner must explicitly change to `Public` or `Internal` before portal
- ✅ "Public Documents" view is empty until owners act

### 6.3 Metadata-Only (100 records)

- ✅ No dummy/empty files created — design explicitly forbids this
- ✅ Records stored in `RAE Document Registry` Microsoft List (Phase M365-4) as `RAE Metadata Record` items
- ✅ `SHA256` is empty for these records
- ✅ `LocalRelativePath` is empty in manifest
- ✅ Notes column preserves failure reason (404 / 403 / login required / connection error)
- ✅ `DocumentStatus = MetadataOnly` is a defined choice value

### 6.4 Duplicate-Linked (45 records)

- ✅ No re-upload of the same file
- ✅ `RAE Duplicate Reference` content type used (item-only, no file)
- ✅ `DuplicateOf` field populated for all 45 rows (verified in QA)
- ✅ `SHA256` populated (same as primary) for traceability
- ✅ `MigrationStatus = Duplicate (linked)` is a defined choice value

### 6.5 Website Is Not File Storage

- ✅ SharePoint is Source of Truth
- ✅ Portal (Phase M365-8) reads from Registry Export JSON only
- ✅ No files served from VPS or static site
- ✅ Download links point to SharePoint view-only share links
- ✅ Portal has no upload, edit, or admin capability

---

## 7. Assumptions

| # | Assumption | Impact if Wrong |
|---|-----------|-----------------|
| A1 | SharePoint Online license is available (Phase M365-1 not yet complete) | Cannot create site or libraries |
| A2 | Tenant URL format is `[mju].sharepoint.com` | Site URL changes; adjust `LegacySourceURL` references |
| A3 | Thai character filenames are supported in SharePoint (they are in SPO) | Folder/file naming constraints |
| A4 | Microsoft Purview is available for retention labels | Retention must be manual if unavailable |
| A5 | Power Automate is available for notification flows (Phase M365-5) | Owner assignment reminders manual |
| A6 | Named Category Owners will be confirmed post-migration | All `Owner = TBD` records remain stale |
| A7 | Microsoft Lists is available for RAE Document Registry (Phase M365-4) | Metadata-only records need alternative storage |
| A8 | 627 files (~3–5 GB estimated) fit within SharePoint storage quota | Request quota increase if needed |
| A9 | Legacy WTMS URLs in `LegacySourceURL` are dead/inaccessible | Acceptable; preserved for traceability only |

---

## 8. Blockers

| # | Blocker | Phase | Resolution |
|---|---------|-------|------------|
| B1 | M365 license audit not yet complete (Phase M365-1) | Pre-M365-3 | Complete M365-1 before implementation |
| B2 | Named Category Owners not confirmed | Post-migration | Use `OWNER_CONFIRMATION_CHECKLIST.csv`; set TBD for now |
| B3 | Tenant admin credentials / app registration needed for bulk upload | Implementation | Coordinate with IT; service account setup |
| B4 | 102 legacy `.doc` files may not preview in SharePoint | Implementation | Plan DOCX conversion post-upload |
| B5 | 616 of 772 Title fields are empty | Implementation | Derivation rule (link_text → filename) needed in upload script |

---

## 9. Dependencies for Implementation

| Dependency | Phase | Status |
|---|---|---|
| SharePoint Online site created | M365-3 impl | 🔲 Pending license confirm |
| M365 groups created for 6 libraries | M365-3 impl | 🔲 Pending owner confirmation |
| Migration Bot service account | M365-3 impl | 🔲 Pending IT coordination |
| Staging files validated at `G:\ProjectAI\document-center\.migration\rae-wtms\files\` | ✅ Complete | SHA-256 verified 627/627 |
| `sharepoint-migration-manifest.csv` finalized | ✅ Complete | 772 rows, QA PASS |
| Microsoft Lists setup (for 100 metadata-only) | M365-4 | 🔲 Next phase |
| Power Automate flows (owner assignment reminders) | M365-5 | 🔲 Future phase |

---

## 10. Next Steps (Phase M365-3 → Implementation)

1. **Complete Phase M365-1** — Confirm SharePoint Online and Microsoft Lists availability
2. **Create M365 groups** — 6 owner groups + contributors + readers (see `permissions-matrix.md` §11)
3. **Create SharePoint site** — `RAE-DocumentCenter`; apply settings from `sharepoint-site-design.md`
4. **Create site columns** — All 15 columns as site-level columns
5. **Create content types** — Hierarchy from `content-types.md`
6. **Create 6 libraries** — Apply content types and column defaults from `library-schema.md`
7. **Create folder structure** — 23 subcategory folders across 6 libraries
8. **Set permissions** — Apply `permissions-matrix.md` to site, libraries, folders
9. **Configure versioning and retention** — As specified in `sharepoint-site-design.md §5-6`
10. **Run bulk import script** — Upload 627 files using `sharepoint-migration-manifest.csv`
11. **Register metadata-only in Lists** — Phase M365-4
12. **Revoke Migration Bot account** — Within 7 days of import completion

---

## 11. QA Checklist

| Check | Result |
|-------|--------|
| All 6 libraries defined | ✅ PASS |
| Schema covers all 15 required columns | ✅ PASS |
| All 772 manifest rows map to schema | ✅ PASS |
| No missing manifest fields | ✅ PASS |
| Owner=TBD supported | ✅ PASS |
| PendingReview supported and default | ✅ PASS |
| Metadata-only: no dummy files in design | ✅ PASS |
| Duplicates: no re-upload in design | ✅ PASS |
| Website not used as file storage | ✅ PASS |
| SharePoint is Source of Truth | ✅ PASS |
| Content types cover all 772+100 records | ✅ PASS |
| Permissions respect least-privilege | ✅ PASS |
| Field map covers all manifest columns | ✅ PASS |
| 23 subcategories mapped to folders | ✅ PASS |
| Retention policy defined per library | ✅ PASS |
| No site/tenant created (design-only phase) | ✅ PASS |
| No untracked/unrelated files touched | ✅ PASS |

---

## **M365-3 Design QA: PASS**

---

## Related Documents

| Document | Path |
|----------|------|
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
| Site Design | `docs/m365/sharepoint-site-design.md` |
| Library Schema | `docs/m365/library-schema.md` |
| Content Types | `docs/m365/content-types.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Migration Field Map | `docs/m365/migration-field-map.csv` |
| Migration Manifest | `migration/sharepoint-migration-manifest.csv` |
| Migration Readiness | `migration/migration-readiness-report.md` |
| QA Report | `migration/qa_report.json` |
| Taxonomy | `docs/document-center/taxonomy.json` |
| Registry Data Model | `docs/document-center/REGISTRY_DATA_MODEL.md` |
