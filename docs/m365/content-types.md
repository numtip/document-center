# Content Types — RAE Document Center

**Phase:** M365-3 — SharePoint Foundation  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-13  
**Applies to:** RAE Document Center SharePoint site

---

## 1. Overview

SharePoint Content Types define the metadata template, document template, and workflow behavior for items in a library. Content Types inherit from a parent hierarchy and are managed at the Site Collection level so all 6 libraries share them.

### 1.1 Design Goals

| Goal | Approach |
|------|----------|
| Consistent schema across 6 libraries | Single shared Content Type hierarchy |
| Support legacy-imported documents | `RAE Legacy Document` CT with migration fields |
| Support metadata-only records | `RAE Metadata Record` CT (no file template) — for Microsoft Lists use |
| Support future active documents | `RAE Active Document` CT with approval workflow hook |
| Enable Phase M365-5 automation | Workflow association field on each CT |
| Align with existing registry model | Fields map to `REGISTRY_DATA_MODEL.md` field names |

---

## 2. Content Type Hierarchy

```
Document (built-in, SharePoint base)
└── RAE Document Base (site CT — abstract)
    ├── RAE Legacy Document         ← All 672 migrated files
    ├── RAE Active Document         ← New documents post-migration
    └── RAE Duplicate Reference     ← 45 duplicate link records

Item (built-in, SharePoint base)
└── RAE Metadata Record             ← 100 metadata-only records (Microsoft Lists)
```

---

## 3. RAE Document Base (Abstract Parent)

**Content Type ID:** `0x010100[site-GUID]01`  
**Parent:** `Document` (built-in)  
**Description:** Abstract base; not used directly in libraries. Defines all shared columns.  
**Document template:** None (abstract)

### 3.1 Columns Inherited by All RAE Document CTs

| Column | Internal Name | Required | Inherits From |
|--------|--------------|----------|---------------|
| `DocumentID` | `RAE_DocumentID` | Yes | Base |
| `Title` | `Title` | Yes | Document (built-in) |
| `Category` | `RAE_Category` | Yes | Base |
| `Subcategory` | `RAE_Subcategory` | Yes | Base |
| `Owner` | `RAE_Owner` | Yes | Base |
| `DocumentStatus` | `RAE_DocumentStatus` | Yes | Base |
| `Version` | `RAE_Version` | No | Base |
| `UpdatedDate` | `RAE_UpdatedDate` | No | Base |
| `Tags` | `RAE_Tags` | No | Base |
| `PublicVisibility` | `RAE_PublicVisibility` | Yes | Base |
| `LegacySourceURL` | `RAE_LegacySourceURL` | No | Base |
| `MigrationStatus` | `RAE_MigrationStatus` | Yes | Base |
| `SHA256` | `RAE_SHA256` | No | Base |
| `DuplicateOf` | `RAE_DuplicateOf` | No | Base |
| `Notes` | `RAE_Notes` | No | Base |

---

## 4. RAE Legacy Document

**Content Type ID:** `0x010100[site-GUID]0101`  
**Parent:** `RAE Document Base`  
**Used in:** All 6 Document Libraries  
**Applies to:** 627 physical files from WTMS migration  
**Document template:** None (file uploaded as-is from archive)

### 4.1 Field Defaults for This CT

| Column | Default Value | Notes |
|--------|---------------|-------|
| `DocumentStatus` | `LegacyImported` | Set at import; owner updates to `Current` after review |
| `PublicVisibility` | `PendingReview` | Must be reviewed before portal exposure |
| `MigrationStatus` | `Ready` | Pre-verified by SHA-256 check |
| `Owner` | `TBD` | Category owner updates post-import |
| `Version` | `1.0` | Starting version; increment on content update |

### 4.2 Workflow Hook (Phase M365-5)

| Trigger | Action |
|---------|--------|
| Document uploaded with this CT | Power Automate: notify Category Owner for metadata review |
| `Owner` field updated from `TBD` | Power Automate: log owner assignment to audit list |
| `DocumentStatus` changed to `Current` | Power Automate: prompt `PublicVisibility` review |

### 4.3 Validation Rules

| Rule | Column | Constraint |
|------|--------|------------|
| DocumentID required | `DocumentID` | Cannot be empty; pattern `RAE-NNNNN` |
| Owner TBD is acceptable | `Owner` | Allows `TBD`; governance reminder via Power Automate |
| SHA256 must match on upload | `SHA256` | Upload script validates before file creation |
| MigrationStatus = Ready | `MigrationStatus` | Default for this CT; change blocked until SHA verified |

---

## 5. RAE Active Document

**Content Type ID:** `0x010100[site-GUID]0102`  
**Parent:** `RAE Document Base`  
**Used in:** All 6 Document Libraries  
**Applies to:** New documents created after migration; reviewed legacy documents promoted to `Current`  
**Document template:** Blank (library assigns per subcategory if needed)

### 5.1 Field Defaults for This CT

| Column | Default Value | Notes |
|--------|---------------|-------|
| `DocumentStatus` | `Draft` | Starts as draft; promoted via approval |
| `PublicVisibility` | `Internal` | Default to org-only |
| `MigrationStatus` | `N/A` | Not a migrated document |
| `Owner` | _(current user email)_ | Auto-populated from user profile |
| `Version` | `1.0` | Initial version |

### 5.2 Approval Workflow (Phase M365-5)

```
Draft → [Category Owner Review] → Approved (Current) → [Document Owner] → Published
                                ↓
                           Rejected (back to Draft + Notes)
```

### 5.3 Additional Columns (Active only)

| Column | Type | Purpose |
|--------|------|---------|
| `ApprovalStatus` | Choice | `Draft`, `InReview`, `Approved`, `Rejected` |
| `ReviewedBy` | Person or Group | Reviewer identity |
| `ReviewDate` | Date | When review occurred |

> These columns are exclusive to `RAE Active Document` and are **not** part of the Base CT. They enable Phase M365-5 approval automation.

---

## 6. RAE Duplicate Reference

**Content Type ID:** `0x010100[site-GUID]0103`  
**Parent:** `RAE Document Base`  
**Used in:** All 6 Document Libraries (for tracking purposes only)  
**Applies to:** 45 duplicate-linked records from WTMS migration  
**Document template:** None — no file uploaded; item-only record in library  
**Note:** This is a list item (not a file) that records the legacy URL alias. The physical file is under the primary document's `DocumentID`.

### 6.1 Field Defaults for This CT

| Column | Default Value | Notes |
|--------|---------------|-------|
| `DocumentStatus` | `LegacyImported` | Matches primary |
| `MigrationStatus` | `Duplicate (linked)` | Fixed; not editable post-migration |
| `DuplicateOf` | _(from manifest)_ | Must reference primary `DocumentID` |
| `SHA256` | _(same as primary)_ | Same file; populated for traceability |

### 6.2 Behavior Rules

- `DuplicateOf` must be populated and reference a valid `DocumentID` in any library
- No new file is associated with this item type
- `PublicVisibility` inherits from the primary document (via Power Automate sync, Phase M365-5)
- Cannot be promoted to `RAE Active Document`; must be deleted if legacy URL is decommissioned

---

## 7. RAE Metadata Record (Microsoft Lists)

**Content Type ID:** `0x0100[site-GUID]0200` (List Item base)  
**Parent:** `Item` (built-in)  
**Used in:** `RAE Document Registry` Microsoft List (Phase M365-4)  
**Applies to:** 100 metadata-only records (no physical file)  
**Purpose:** Preserve knowledge that these documents existed in legacy WTMS, even though originals are inaccessible (404/403/login-required)

### 7.1 Columns

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| `DocumentID` | Text | Yes | `RAE-NNNNN` format |
| `Title` | Text | Yes | Document title from legacy site |
| `Category` | Choice | Yes | Taxonomy slug |
| `Subcategory` | Text | Yes | Legacy subcategory |
| `Owner` | Text | Yes | `TBD` during migration |
| `DocumentStatus` | Choice | Yes | `MetadataOnly` |
| `PublicVisibility` | Choice | Yes | `PendingReview` |
| `LegacySourceURL` | Hyperlink | No | Original URL (may be dead) |
| `MigrationStatus` | Choice | Yes | `Metadata Only` |
| `SHA256` | Text | No | Empty — no file |
| `Notes` | Multi-text | No | Reason: `404 / 403 / login required / connection error` |

### 7.2 Rules

| Rule | Enforcement |
|------|-------------|
| No file attachment | List item only; no file template |
| `SHA256` must be empty | Validation formula |
| `DocumentStatus` must be `MetadataOnly` | Locked; not changeable to `Current` |
| `Notes` must explain reason | Required if `MigrationStatus = Metadata Only` |

### 7.3 Why Not in Document Libraries?

SharePoint Document Libraries require a file for each item. Creating a 0-byte placeholder violates the principle:

> **"Metadata Only ไม่มีการสร้างไฟล์ปลอม"** (No dummy files for metadata-only records)

Microsoft Lists is the correct container for file-free metadata records.

---

## 8. Content Type Application Summary

| Content Type | Libraries | Microsoft Lists | Record Count |
|---|---|---|---|
| `RAE Legacy Document` | All 6 | No | 627 |
| `RAE Duplicate Reference` | All 6 | No | 45 |
| `RAE Active Document` | All 6 | No | 0 (post-migration new docs) |
| `RAE Metadata Record` | No | RAE Document Registry | 100 |
| **Total** | | | **772** |

---

## 9. Term Set: RAE-Tags

Managed Metadata term set for the `Tags` column. Populated post-migration by Category Owners.

**Term Set Name:** `RAE-Tags`  
**Term Store Group:** `RAE Document Center`  
**Open/Closed:** Open (Category Owners can add terms)

### Seed Terms (to be confirmed by owners)

| Term | Applicable Libraries |
|------|---------------------|
| `administration` | Administration |
| `finance` | FinanceProcurement |
| `procurement` | FinanceProcurement |
| `research` | Research, SOPManuals |
| `research-fund` | Research |
| `research-report` | Research |
| `academic-service` | AcademicServices |
| `policy` | PlanningPolicy |
| `planning` | PlanningPolicy |
| `quality-assurance` | PlanningPolicy |
| `sop` | SOPManuals |
| `form` | AcademicServices, Research |
| `announcement` | Research |
| `legacy-import` | All | (auto-tagged during migration) |

---

## 10. Implementation Order

1. Create site columns (all 15 columns as site-level columns)
2. Create `RAE Document Base` Content Type; add all 15 columns
3. Create `RAE Legacy Document` inheriting from Base; set defaults
4. Create `RAE Active Document` inheriting from Base; add approval columns
5. Create `RAE Duplicate Reference` inheriting from Base; set MigrationStatus default
6. Create `RAE Metadata Record` as List Item CT
7. Apply `RAE Legacy Document` and `RAE Duplicate Reference` to all 6 libraries
8. Apply `RAE Metadata Record` to `RAE Document Registry` list (Phase M365-4)
9. Create Term Set `RAE-Tags`

---

## Related Documents

| Document | Path |
|----------|------|
| Site Design | `docs/m365/sharepoint-site-design.md` |
| Library Schema | `docs/m365/library-schema.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Registry Data Model | `docs/document-center/REGISTRY_DATA_MODEL.md` |
| Migration Field Map | `docs/m365/migration-field-map.csv` |
