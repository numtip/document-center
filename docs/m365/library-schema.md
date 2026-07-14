# Library Schema — RAE Document Center

**Phase:** M365-3 — SharePoint Foundation  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-13  
**Applies to:** All 6 Document Libraries on the RAE Document Center site  
**Source data:** `migration/sharepoint-migration-manifest.csv` (772 rows)

---

## 1. Schema Design Principles

1. **Single schema across all 6 libraries** — same column set, consistent naming
2. **Manifest fields are the source** — every manifest column maps to a SharePoint column (see `migration-field-map.csv`)
3. **Owner = TBD is valid** — until individual owners are confirmed post-migration
4. **Metadata-only records do not use dummy files** — they live in Microsoft Lists Registry (Phase M365-4)
5. **Duplicate records are not re-uploaded** — tracked via `DuplicateOf` field pointing to primary `DocumentID`
6. **SharePoint is Source of Truth** — registry JSON exported from here (Phase M365-8)

---

## 2. Column Definitions

All columns are site columns applied as a Content Type (see `content-types.md`) to every library.

### 2.1 Core Identification

| Column Name | SharePoint Type | Internal Name | Required | Indexed | Default | Allowed Values |
|---|---|---|---|---|---|---|
| `DocumentID` | Single line of text | `RAE_DocumentID` | Yes | Yes (unique) | _(auto-assigned)_ | Pattern: `RAE-NNNNN` |
| `Title` | Single line of text | `Title` | Yes | Yes | _(from manifest `Title` or filename)_ | Free text; max 255 chars |
| `Category` | Single line of text | `RAE_Category` | Yes | Yes | _(inherited from library)_ | Taxonomy slug: see §2.6 |
| `Subcategory` | Single line of text | `RAE_Subcategory` | Yes | Yes | _(folder name)_ | Free text; from legacy subcategory |

> **Note:** `Title` column is the built-in SharePoint column. 616 of 772 manifest rows have empty `Title`; during upload the title will be derived from `link_text` → `original_filename` → `LocalRelativePath` stem (priority order).

### 2.2 Ownership and Lifecycle

| Column Name | SharePoint Type | Internal Name | Required | Indexed | Default | Allowed Values |
|---|---|---|---|---|---|---|
| `Owner` | Single line of text | `RAE_Owner` | Yes | Yes | `TBD` | Email or role name; `TBD` valid during migration |
| `DocumentStatus` | Choice | `RAE_DocumentStatus` | Yes | Yes | `LegacyImported` | See §2.7 |
| `Version` | Single line of text | `RAE_Version` | No | No | `1.0` | Semantic: `{major}.{minor}` (e.g. `1.0`, `2.1`) |
| `UpdatedDate` | Date and Time (date only) | `RAE_UpdatedDate` | No | No | _(upload date)_ | `YYYY-MM-DD`; must not be future |

### 2.3 Access Control and Discovery

| Column Name | SharePoint Type | Internal Name | Required | Indexed | Default | Allowed Values |
|---|---|---|---|---|---|---|
| `PublicVisibility` | Choice | `RAE_PublicVisibility` | Yes | Yes | `PendingReview` | See §2.8 |
| `Tags` | Managed Metadata (Term Set: RAE-Tags) | `RAE_Tags` | No | Yes | _(empty)_ | Lowercase terms in `RAE-Tags` term set |

> **`PublicVisibility = PendingReview`** is valid and expected for all 772 legacy-imported documents. It signals that visibility has not been reviewed post-migration. No document is public until a Category Owner changes this to `Public` or `Internal`.

### 2.4 Migration Traceability

| Column Name | SharePoint Type | Internal Name | Required | Indexed | Default | Allowed Values |
|---|---|---|---|---|---|---|
| `LegacySourceURL` | Hyperlink or Picture | `RAE_LegacySourceURL` | No | No | _(from manifest `SourceURL`)_ | URL string; may be dead link |
| `MigrationStatus` | Choice | `RAE_MigrationStatus` | Yes | Yes | `Ready` | See §2.9 |
| `SHA256` | Single line of text | `RAE_SHA256` | No | No | _(from manifest `SHA256`)_ | 64-char hex; empty for metadata-only |
| `DuplicateOf` | Single line of text | `RAE_DuplicateOf` | No | No | _(from manifest `DuplicateOf`)_ | `DocumentID` or filename of primary; empty if not duplicate |

### 2.5 Notes

| Column Name | SharePoint Type | Internal Name | Required | Indexed | Default | Allowed Values |
|---|---|---|---|---|---|---|
| `Notes` | Multiple lines of text (plain text) | `RAE_Notes` | No | No | _(empty)_ | Free text; max 1000 chars |

---

## 3. Column Summary Table

| # | Column | Type | Required | Indexed | Default | Source Manifest Field |
|---|--------|------|----------|---------|---------|----------------------|
| 1 | `DocumentID` | Text | Yes | Yes | auto | `DocumentID` |
| 2 | `Title` | Text (built-in) | Yes | Yes | filename stem | `Title` → `link_text` → filename |
| 3 | `Category` | Text | Yes | Yes | library default | `Category` |
| 4 | `Subcategory` | Text | Yes | Yes | folder name | `Subcategory` |
| 5 | `Owner` | Text | Yes | Yes | `TBD` | `Owner` |
| 6 | `DocumentStatus` | Choice | Yes | Yes | `LegacyImported` | `Status` |
| 7 | `Version` | Text | No | No | `1.0` | _(not in v1 manifest)_ |
| 8 | `UpdatedDate` | Date | No | No | upload date | _(not in v1 manifest)_ |
| 9 | `Tags` | Managed Metadata | No | Yes | _(empty)_ | _(not in v1 manifest)_ |
| 10 | `PublicVisibility` | Choice | Yes | Yes | `PendingReview` | `PublicVisibility` |
| 11 | `LegacySourceURL` | Hyperlink | No | No | from manifest | `SourceURL` |
| 12 | `MigrationStatus` | Choice | Yes | Yes | `Ready` | `MigrationStatus` |
| 13 | `SHA256` | Text | No | No | from manifest | `SHA256` |
| 14 | `DuplicateOf` | Text | No | No | from manifest | `DuplicateOf` |
| 15 | `Notes` | Multi-text | No | No | _(empty)_ | `Notes` |

**Total: 15 columns** (14 custom + 1 built-in Title)

---

## 4. Allowed Values

### 4.1 `Category` — Taxonomy Slugs (from `taxonomy.json`)

| Slug | Thai Name | Library |
|------|-----------|---------|
| `admin` | งานบริหารและธุรการ | Administration |
| `finance-procurement` | งานคลังและพัสดุ | FinanceProcurement |
| `policy-planning` | งานนโยบาย แผนและประกันคุณภาพ | PlanningPolicy |
| `academic-service` | งานบริการวิชาการ | AcademicServices |
| `research` | งานวิจัย | Research |
| `manuals` | คู่มือปฏิบัติงาน | SOPManuals |

### 4.2 `DocumentStatus` Allowed Values

| Value | Meaning | Listed in Search | Registry Status |
|-------|---------|-----------------|-----------------|
| `LegacyImported` | Imported from WTMS; pending review | Yes | Default for all migrated docs |
| `Current` | Active, reviewed, published | Yes | Post-review state |
| `Obsolete` | Superseded but retained | Conditional | De-emphasized |
| `Archived` | Moved to `_Archive` folder | No | Not shown in default views |
| `Draft` | Work in progress | No | Internal only |
| `MetadataOnly` | No physical file; metadata record only | Conditional | Maps to 100 metadata-only records |

> `MetadataOnly` status in SharePoint is for completeness; actual metadata-only records live in Microsoft Lists (Phase M365-4). If a stub item is created, it uses this status with empty file attachment.

### 4.3 `PublicVisibility` Allowed Values

| Value | Meaning | Portal Behavior |
|-------|---------|-----------------|
| `PendingReview` | Not yet reviewed for public access | **Excluded** from portal export |
| `Public` | Accessible to all site visitors | **Included** in portal export; anonymous view link OK |
| `Internal` | Visible to org users only | **Included** in portal (authenticated); org-scoped link |
| `Restricted` | Access by exception only | **Excluded** from portal; manual access request |

### 4.4 `MigrationStatus` Allowed Values

| Value | Count | Meaning |
|-------|-------|---------|
| `Ready` | 627 | Physical file verified; SHA-256 validated; ready to upload |
| `Duplicate (linked)` | 45 | Same file as primary; links to `DuplicateOf`; no re-upload |
| `Metadata Only` | 100 | No original file (404/403/login-required); metadata record only |
| `Pending Review` | 0 | Unreadable or unverified file |

---

## 5. Library-Specific Column Defaults

Each library has column default values that auto-populate `Category` and `DocumentStatus`:

| Library | `Category` default | `DocumentStatus` default | `PublicVisibility` default |
|---------|-------------------|--------------------------|---------------------------|
| Administration | `admin` | `LegacyImported` | `PendingReview` |
| FinanceProcurement | `finance-procurement` | `LegacyImported` | `PendingReview` |
| PlanningPolicy | `policy-planning` | `LegacyImported` | `PendingReview` |
| AcademicServices | `academic-service` | `LegacyImported` | `PendingReview` |
| Research | `research` | `LegacyImported` | `PendingReview` |
| SOPManuals | `manuals` | `LegacyImported` | `PendingReview` |

---

## 6. Default Views per Library

### 6.1 All Documents (default view)

Columns shown: `DocumentID`, `Title`, `Subcategory`, `Owner`, `DocumentStatus`, `PublicVisibility`, `MigrationStatus`  
Filter: `DocumentStatus != Archived`  
Sort: `Subcategory` ASC, `Title` ASC  
Group by: `Subcategory`

### 6.2 Migration Review View

Columns shown: `DocumentID`, `Title`, `Subcategory`, `MigrationStatus`, `DuplicateOf`, `SHA256`, `LegacySourceURL`, `Notes`  
Filter: `MigrationStatus = Ready OR Duplicate (linked)`  
Purpose: Post-migration verification by category owners

### 6.3 Pending Owner Assignment

Columns shown: `DocumentID`, `Title`, `Category`, `Subcategory`, `Owner`, `DocumentStatus`, `UpdatedDate`  
Filter: `Owner = TBD`  
Purpose: Identify documents needing owner assignment

### 6.4 Public Documents

Columns shown: `DocumentID`, `Title`, `Subcategory`, `Version`, `UpdatedDate`, `LegacySourceURL`  
Filter: `PublicVisibility = Public AND DocumentStatus = Current`  
Purpose: Documents ready for portal export

### 6.5 Archive View

Columns shown: `DocumentID`, `Title`, `DocumentStatus`, `UpdatedDate`, `Notes`  
Filter: `DocumentStatus = Archived OR DocumentStatus = Obsolete`  
Purpose: Historical record management

---

## 7. File Type Composition (from manifest analysis)

| File Type | Count | % of files | Notes |
|-----------|-------|-----------|-------|
| PDF | 423 | 67.5% | Most common; many scanned |
| DOCX | 134 | 21.4% | Modern Word format |
| DOC | 102 | 16.3% | Legacy Word; plan conversion |
| XLSX | 10 | 1.6% | Excel workbooks |
| PPTX | 2 | 0.3% | PowerPoint presentations |
| JPG | 1 | 0.2% | Image file; in `_Review` |
| _(none — metadata only)_ | 100 | — | No file; Microsoft List only |

> **Migration note:** DOC files (102) may need conversion to DOCX post-upload for full SharePoint preview. Legacy DOC format has limited preview support.

---

## 8. Column Index Strategy

Indexed columns enable efficient filtered views and search refiners. Indexing consumes list threshold budget (5000-item limit applies to non-indexed queries).

| Column | Index Type | Reason |
|--------|------------|--------|
| `DocumentID` | Unique | Primary identifier; lookup |
| `Title` | Non-unique | Default SharePoint index |
| `Category` | Non-unique | Primary navigation refiner |
| `Subcategory` | Non-unique | Folder-level grouping |
| `Owner` | Non-unique | Owner assignment views |
| `DocumentStatus` | Non-unique | Lifecycle filtering |
| `PublicVisibility` | Non-unique | Portal export filtering |
| `MigrationStatus` | Non-unique | Migration verification |
| `Tags` | Non-unique | Search refinement |

> Research library has 576 rows — no single subfolder exceeds 5000 items, so list threshold is not a concern for this migration batch.

---

## 9. Validation Rules

| Rule | Enforcement |
|------|-------------|
| `DocumentID` must be unique across all 6 libraries | Column validation formula + Power Automate check (Phase M365-5) |
| `Owner = TBD` is allowed; must be resolved within 90 days of migration | Governance reminder (Phase M365-5) |
| `PublicVisibility = PendingReview` documents excluded from portal | Registry export filter (Phase M365-8) |
| Metadata-only: `SHA256` and `LocalRelativePath` must be empty | Migration upload script validation |
| Duplicate: `DuplicateOf` must reference an existing `DocumentID` | Manual check during upload; automated in Phase M365-5 |
| File upload: SHA-256 of uploaded file must match manifest `SHA256` | Upload validation script (migration tooling) |

---

## Related Documents

| Document | Path |
|----------|------|
| Site Design | `docs/m365/sharepoint-site-design.md` |
| Content Types | `docs/m365/content-types.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Migration Field Map | `docs/m365/migration-field-map.csv` |
| Registry Data Model | `docs/document-center/REGISTRY_DATA_MODEL.md` |
| Taxonomy | `docs/document-center/taxonomy.json` |
| Migration Manifest | `migration/sharepoint-migration-manifest.csv` |
