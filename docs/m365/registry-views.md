# RAE Document Registry — Microsoft Lists Views

**Phase:** M365-4 — Microsoft Lists Registry Design  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-14  
**Applies to:** `RAE Document Registry` Microsoft List

---

## 1. Design Principles

1. **Views enable governance operations** — Every view serves a governance purpose, not just visual appeal.
2. **Minimize view maintenance** — Use filters and groupings that work with the data as-is, not manually maintained.
3. **Fixed set of views** — 10 views defined. No ad-hoc views created without governance approval.
4. **Operational Action** — Each view includes a defined action for the viewer to take.
5. **Audience** — Not all views are for all roles. Category Owners, Platform Admin, and Power Automate each have appropriate views.

---

## 2. View Definitions

### 2.1 All Documents

| Property | Value |
|----------|-------|
| **Purpose** | Complete list of all registry records |
| **Audience** | Platform Admin, Category Owners |
| **Columns** | Document ID, Title, Category, Owner, Status, Visibility, UpdatedDate, Storage URL, SourceSystem |
| **Filters** | None (all records visible) |
| **Sort** | UpdatedDate DESC |
| **Grouping** | Category |
| **Operational Action** | Review overall registry health |

### 2.2 Public Documents

| Property | Value |
|----------|-------|
| **Purpose** | Documents eligible for public portal export |
| **Audience** | Platform Admin |
| **Columns** | Document ID, Title, Category, Owner, Version, UpdatedDate, PublishedDate, Storage URL |
| **Filters** | Status = Current OR Published OR Approved AND Visibility = Public AND StorageURL is not empty |
| **Sort** | UpdatedDate DESC |
| **Grouping** | Category |
| **Operational Action** | Verify public export set; identify documents needing StorageURL updates |

### 2.3 Missing Metadata

| Property | Value |
|----------|-------|
| **Purpose** | Documents with incomplete required metadata |
| **Audience** | Category Owners, Platform Admin |
| **Columns** | Document ID, Title, Category, Owner, Status, Visibility, Storage URL, Notes |
| **Filters** | DocumentID is empty OR Title is empty OR Owner is empty OR Status is empty OR Visibility is empty OR (SourceSystem = WTMS Migration AND StorageURL is empty AND Status != archived AND Status != obsolete) |
| **Sort** | Category ASC |
| **Grouping** | Category |
| **Operational Action** | Assign missing metadata; CORE fields must be populated before export readiness |

### 2.4 Pending Review

| Property | Value |
|----------|-------|
| **Purpose** | Documents whose visibility or lifecycle review is pending |
| **Audience** | Category Owners |
| **Columns** | Document ID, Title, Category, Owner, Status, Visibility, UpdatedDate, LegacySourceURL |
| **Filters** | Status = review OR Visibility is empty |
| **Sort** | UpdatedDate ASC (oldest first) |
| **Grouping** | Category |
| **Operational Action** | Review each document; transition Status to approved/published/current/obsolete; set Visibility to public/internal/restricted/private |

### 2.5 Expiring Review

| Property | Value |
|----------|-------|
| **Purpose** | Documents whose governance review date is approaching or past due |
| **Audience** | Category Owners, Platform Admin |
| **Columns** | Document ID, Title, Category, Owner, Status, UpdatedDate, ReviewDate |
| **Filters** | ReviewDate is not empty AND ReviewDate <= [Today + 90 days] |
| **Sort** | ReviewDate ASC (soonest first) |
| **Grouping** | Category |
| **Operational Action** | Review document; reset ReviewDate to next review date or mark as reviewed |

### 2.6 Obsolete / Archive Candidates

| Property | Value |
|----------|-------|
| **Purpose** | Documents ready for lifecycle transition to Obsolete or Archived |
| **Audience** | Category Owners, Archive Manager |
| **Columns** | Document ID, Title, Category, Owner, Status, Visibility, UpdatedDate, ReviewDate, Notes |
| **Filters** | Status = draft AND UpdatedDate <= [Today - 365 days] OR Status = obsolete OR Status = archived |
| **Sort** | UpdatedDate ASC |
| **Grouping** | Category |
| **Operational Action** | Review old drafts older than 1 year; confirm obsolete/archived status |

### 2.7 By Owner

| Property | Value |
|----------|-------|
| **Purpose** | Documents grouped by responsible owner for accountability |
| **Audience** | Category Owners, Platform Admin |
| **Columns** | Document ID, Title, Category, Status, Visibility, UpdatedDate, ReviewDate |
| **Filters** | (none) |
| **Sort** | Owner ASC, Status ASC |
| **Grouping** | Owner |
| **Operational Action** | Verify owner assignments; identify orphan records |

### 2.8 By Category

| Property | Value |
|----------|-------|
| **Purpose** | Registry health summary per taxonomy category |
| **Audience** | Category Owners, Platform Admin |
| **Columns** | Document ID, Title, Owner, Status, Visibility, UpdatedDate |
| **Filters** | (none) |
| **Sort** | Title ASC |
| **Grouping** | Category |
| **Operational Action** | Per-category governance review |

### 2.9 Synchronization Errors

| Property | Value |
|----------|-------|
| **Purpose** | Records with potential synchronization issues between SharePoint and Registry |
| **Audience** | Platform Admin |
| **Columns** | Document ID, Title, Category, Owner, Status, Visibility, SourceSystem, Notes |
| **Filters** | (Manual — no automated sync error detection without Power Automate in this phase) |
| **Sort** | Category ASC |
| **Grouping** | (none) |
| **Operational Action** | **DEFERRED** — Automated sync error detection requires Phase M365-5 (Power Automate) or Phase M365-7 (Migration Pilot) |
| **Notes** | In EA-4, this view is a placeholder. Manual reconciliation is the only option until Power Automate is implemented. Column visibility is configured for sync fields. |

### 2.10 Migration Records

| Property | Value |
|----------|-------|
| **Purpose** | View all records originating from WTMS migration |
| **Audience** | Platform Admin |
| **Columns** | Document ID, Title, Category, Owner, Status, Visibility, SourceSystem, LegacySourceURL, DuplicateOf, Notes |
| **Filters** | SourceSystem = WTMS Migration |
| **Sort** | DocumentID ASC |
| **Grouping** | SourceSystem |
| **Operational Action** | Verify migration completeness; track post-migration metadata updates |

---

## 3. View Summary

| # | View Name | Purpose | Audience | Primary Filter |
|---|-----------|---------|----------|----------------|
| 1 | All Documents | Complete registry view | Admin, Owners | None |
| 2 | Public Documents | Portal export candidates | Admin | Status=Current/Published/Approved, Visibility=Public |
| 3 | Missing Metadata | Incomplete required fields | Owners, Admin | Empty CORE fields |
| 4 | Pending Review | Unreviewed documents | Owners | Status=review or Visibility empty |
| 5 | Expiring Review | Approaching review date | Owners, Admin | ReviewDate <= Today+90 |
| 6 | Obsolete/Archive | Old drafts, obsolete, archived | Owners, Archive Mgr | draft older than 1yr or obsolete/archived |
| 7 | By Owner | Owner accountability | Owners, Admin | Grouped by Owner |
| 8 | By Category | Category health | Owners, Admin | Grouped by Category |
| 9 | Synchronization Errors | Sync issues (placeholder) | Admin | Manual only; deferred |
| 10 | Migration Records | WTMS migration trace | Admin | SourceSystem=WTMS Migration |

---

## 4. View Permissions

| View | Platform Admin | Category Owner | Reader |
|------|:-------------:|:--------------:|:------:|
| All Documents | ✅ | ✅ | ❌ |
| Public Documents | ✅ | ✅ | ✅ |
| Missing Metadata | ✅ | ✅ | ❌ |
| Pending Review | ✅ | ✅ | ❌ |
| Expiring Review | ✅ | ✅ | ❌ |
| Obsolete / Archive | ✅ | ✅ | ❌ |
| By Owner | ✅ | ✅ | ❌ |
| By Category | ✅ | ✅ | ✅ |
| Synchronization Errors | ✅ | ❌ | ❌ |
| Migration Records | ✅ | ✅ | ❌ |

> Reader access is restricted to the "Public Documents" and "By Category" views. Other views expose governance metadata.

---

## 5. Implementation Notes

- Create views in the order listed (most-used first for default visibility)
- Person column-based grouping ("By Owner") requires Person/Group column type
- Date-based filters ("Expiring Review" and "Obsolete / Archive") use relative date formulas where supported
- "Synchronization Errors" view should be created as a placeholder shell. Populate with automated data in Phase M365-5
- Views cannot be permission-scoped at the view level in Microsoft Lists; manage via List-level permissions as defined in `permissions-matrix.md` §9

---

## Related Documents

| Document | Path |
|----------|------|
| Registry Schema | `docs/m365/registry-list-schema.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Validation Rules | `docs/m365/registry-validation-rules.md` |
| Lifecycle Model | `docs/m365/registry-lifecycle-model.md` |
