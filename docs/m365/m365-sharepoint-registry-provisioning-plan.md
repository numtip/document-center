# SharePoint + Registry Provisioning Plan — RAE Document Center

**Phase:** EA-3P — Pro

---

## Architecture Implementation Exception — Existing Site Boundary (EA-3R / EA-3S)

Per **EA-3R** reuse audit and **EA-3S** readiness closure, the deployment boundary is changed from a dedicated new site to the **existing RAE SharePoint site**.

| Parameter | Original Design | Approved Exception |
|-----------|-----------------|-------------------|
| Site URL | `/sites/RAEDocumentCenter` | `/sites/msteams_54adc4` |
| Site Type | New Team Site + M365 Group | Existing Team Site + M365 Group |
| Account Role | Regular user (admin-dependent) | **Site Admin** (self-service capable) |
| Group Creation | New M365 Group required | Existing M365 Group reused (23 members) |
| Permission Groups | 9 new RAE-DC-* groups | 9 new RAE-DC-* groups (Site Admin can create) |
| Libraries | 6 new (PLANNED) | 6 new (unchanged) |
| Registry | New list (PLANNED) | New list (unchanged) |
| Content Types | 5 new (PLANNED) | 5 new (unchanged) |
| Site Columns | 17 new (PLANNED) | 17 new (unchanged) |

**Exception document:** `docs/m365/m365-existing-site-implementation-exception.md`  
**Readiness closure:** `docs/m365/m365-existing-site-reuse-readiness-closure.md`

---

visioning Preflight (Updated per EA-3R/EA-3S Exception)  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Account:** researchmju@mju.ac.th (Jumpon Sriudomsuwan) — Site Admin of existing RAE site  
**Date:** 2026-07-14  
**Status:** PROVISIONING_READY — EXISTING_SITE_APPROVED (see EA-3S readiness closure)

---

## Executive Summary

This document defines the provisioning plan for the RAE Document Center and RAE Document Registry Microsoft List. All preflight checks have been completed. The plan originally assumed a dedicated new SharePoint site, but per the **EA-3R reuse audit** and **EA-3S readiness closure**, the approved deployment boundary is the **existing RAE SharePoint site** (`https://maejo365.sharepoint.com/sites/msteams_54adc4`). An `ARCHITECTURE_IMPLEMENTATION_EXCEPTION` has been approved for this boundary change.

The account used for verification (`researchmju@mju.ac.th`) is a **Site Admin** of the existing RAE site with full self-service capability for libraries, lists, columns, content types, pages, and permission groups. This significantly reduces MJU tenant admin dependency.

The plan defines exact parameters for library provisioning, content type creation, column creation, Microsoft List creation, permission configuration, and internal name capture within the existing site boundary. No production resource has been created or modified.

**Preflight Verdict:** `PROVISIONING_READY` — Deployment boundary: existing RAE site (`/sites/msteams_54adc4`)

---

## Confirmed Tenant Preconditions

| Check | Status | Evidence |
|-------|--------|----------|
| SharePoint Online | ✅ CONFIRMED | SPO-001: Tenant hostname maejo365.sharepoint.com accessible |
| Microsoft Lists | ✅ CONFIRMED | LST-001: Lists app visible and accessible |
| Tenant Admin Access | ❌ NOT AVAILABLE | researchmju@mju.ac.th is regular user; admin center returns error |
| Self-Service Site Creation | ❌ NOT AVAILABLE | No "Create site" button visible on SharePoint start page |
| External/Anonymous Sharing | ✅ CONFIRMED ENABLED | SPO-013/014/015: Anyone links enabled by default |
| Power Automate (Standard) | ✅ CONFIRMED | Batch 2: 3 cloud flow types; SharePoint, Approvals, Teams connectors Standard |
| HTTP Connector | ⚠️ PREMIUM | Premium tier; avoided by architecture (GitHub Actions alternative) |
| DLP Policies | ⚪ NOT_VERIFIED | No admin center access; no warnings observed in UI |

---

## Existing Site — Deployment Parameters

### Site Identity

| Property | Value |
|----------|-------|
| Site URL | `https://maejo365.sharepoint.com/sites/msteams_54adc4` |
| Display Name | สำนักวิจัยฯ (สำนักวิจัยและส่งเสริมวิชาการการเกษตร) |
| Type | Private Team Site (M365 Group connected) |
| Site Admin | researchmju@mju.ac.th (IsSiteAdmin = true) |

> A new site is NOT required. The existing RAE site is the approved deployment boundary per ARCHITECTURE_IMPLEMENTATION_EXCEPTION.

### Site Type Decision

| Parameter | Approved Design | Tenant UI Observation | Recommendation |
|-----------|-----------------|----------------------|----------------|
| Site Type | SharePoint Team Site (with hub site capability) | Existing sites are Team Sites with M365 Group association; Communication site creation not verified | **Team Site (with M365 Group)** — aligns with approved design and existing tenant pattern |
| Team Site Available | — | CONFIRMED (multiple Team Sites exist) | ✅ |
| Communication Site | — | NOT VERIFIED (no "Create site" available) | Not required for this project |
| Hub Site Capability | Required | Requires admin to enable hub feature | Admin must register RAE Document Center as hub site post-creation |

### Site Name

**Approved Name:** `RAE Document Center`  
**Thai Display:** ศูนย์เอกสารสำนักวิจัยฯ

### Primary Language

| Parameter | Approved Design | Tenant UI | Recommendation |
|-----------|-----------------|-----------|----------------|
| Language | Thai (th-TH) | Existing sites use Thai UI | **Thai (th-TH)** — aligns with institutional language |
| Time Zone | (UTC+07:00) Bangkok | — | Bangkok time zone confirmed |

### Privacy

| Setting | Recommendation |
|---------|---------------|
| Privacy | **Private** — Only members can access site content |
| Justification | RAE documents include sensitive institutional data; private team site provides controlled access |
| Future adjustment | Can be changed to Public if institutional knowledge base requirement emerges |

### M365 Group Association

| Decision | Value |
|----------|-------|
| Create new M365 Group? | **NO** — Existing M365 Group reused per ARCHITECTURE_IMPLEMENTATION_EXCEPTION (EA-3R/EA-3S) |
| Group name | Existing M365 Group: สมาชิก สำนักวิจัยฯ (`msteams_54adc4@maejo365.onmicrosoft.com`) |
| Group privacy | **Private** — Existing group is already private |
| Group owners | Existing M365 Group owner is "เจ้าของ สำนักวิจัยฯ" managed via Azure AD. Category Owner assignment is a separate governance dependency |
| Auto-create Teams team | **No** — Not required for this architecture; can be enabled later if needed |

### Owner Requirements

| Role | Requirement | Status |
|------|-------------|--------|
| Primary Site Owner | M365 user account with Full Control | **OWNER_CONFIRMATION_REQUIRED** — named individual unknown |
| Additional Owners | Can be added from existing MJU users | Tenant supports Person/Group selection (confirmed from existing site: Jumpon, Prinya, Monthon visible) |
| Category Owner Groups | 6 SharePoint groups (RAE-DC-{Library}-Owners) | **GROUPS_NOT_CREATED** — must be provisioned after site creation |

---

## Site URL Decision

### Evaluated Patterns

| Pattern | Example | Evaluation |
|---------|---------|------------|
| `/sites/RAEDocumentCenter` | `maejo365.sharepoint.com/sites/RAEDocumentCenter` | Clear, concise, no hyphens; matches institutional pattern |
| `/sites/RAE-DocumentCenter` | `maejo365.sharepoint.com/sites/RAE-DocumentCenter` | Hyphenated; readable but longer |
| `/sites/RAEDocuments` | `maejo365.sharepoint.com/sites/RAEDocuments` | Shorter but ambiguous (implies multiple documents, not a center) |
| `/teams/RAEDocumentCenter` | `maejo365.sharepoint.com/teams/RAEDocumentCenter` | `/teams/` managed path; depends on tenant configuration |
| `/sites/rae-document-center` | `maejo365.sharepoint.com/sites/rae-document-center` | Lowercase with hyphens; consistent with modern URL conventions |

### Recommendation

**`/sites/RAEDocumentCenter`**

Rationale:
1. **Clarity** — "RAE Document Center" matches the approved site name exactly (PascalCase concatenation)
2. **Institutional naming** — Existing sites use `/sites/` prefix (e.g., `/sites/msteams_54adc4`, `/sites/GreenOffice236`)
3. **Future maintainability** — No hyphens to cause URL encoding issues; stable
4. **Registry/Export architecture** — Short, clean URL for use in registry StorageURL and JSON export
5. **URL stability** — SharePoint manages URL redirection; site can be renamed later without breaking `/sites/` path

**Full URL:** `https://maejo365.sharepoint.com/sites/RAEDocumentCenter`

### Alternatives

| Priority | URL | Rationale |
|----------|-----|-----------|
| 1 (Recommended) | `/sites/RAEDocumentCenter` | Best clarity and maintainability |
| 2 | `/sites/rae-document-center` | Consistent with modern lowercasing conventions |
| 3 | `/teams/RAEDocumentCenter` | If tenant restricts `/sites/` managed path |

> **Note:** Final URL must be validated by tenant admin during creation. SharePoint will confirm availability.

---

## M365 Group Association Decision

| Aspect | Decision |
|--------|----------|
| Create M365 Group | **YES** — Team Site template creates one automatically |
| Group Email Alias | `RAEDocumentCenter` (derived from site URL) |
| Group Privacy | **Private** — only approved members |
| Owner Assignment | **REQUIRES ADMIN** — MJU admin must set initial owner |
| Teams Integration | **NOT REQUIRED** — Do not auto-create Teams team |
| Group Naming Policy | Subject to MJU tenant policy (if configured) |

---

## Owner Requirements

### Confirmed Capabilities

| Capability | Evidence |
|------------|----------|
| Individual MJU users selectable | CONFIRMED — existing site shows Jumpon, Prinya, Monthon as identifiable users |
| M365 Groups selectable | CONFIRMED — site shows "23 members" group |
| SharePoint groups selectable | PRESUMED — standard SharePoint behavior |
| Person/Group column type | CONFIRMED — standard SharePoint/Lists column type |

### Identified Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| Named Category Owners unknown | Cannot create owner groups | **BLOCKER** — Requires institutional confirmation of 6 Category Owners |
| RAE-DC-{Library}-Owners groups not created | Permission model cannot be applied | Must be created after site provisioning |
| Primary Site Owner not designated | Site cannot be created | Admin must assign initial owner |

---

## Library Provisioning Order

1. **Administration** — `admin` taxonomy
2. **FinanceProcurement** — `finance-procurement` taxonomy
3. **PlanningPolicy** — `policy-planning` taxonomy
4. **AcademicServices** — `academic-service` taxonomy
5. **Research** — `research` taxonomy (largest: 576 rows)
6. **SOPManuals** — `manuals` taxonomy

---

## Library Parameter Matrix

| Library | Display Name (Thai) | Recommended Internal Name | Content Type | Required Columns | Versioning | Default Visibility | Migration Dependency |
|---------|---------------------|--------------------------|--------------|------------------|------------|-------------------|---------------------|
| **Administration** | งานบริหารและธุรการ | `Administration` | RAE Legacy Document | DocumentID, Title, Category, Owner, DocumentStatus, PublicVisibility, MigrationStatus | Major+Minor (Keep all, 10 drafts) | PendingReview | 9 files |
| **FinanceProcurement** | งานคลังและพัสดุ | `FinanceProcurement` | RAE Legacy Document | Same as above | Major+Minor | PendingReview | 20 files |
| **PlanningPolicy** | งานนโยบาย แผนและประกันคุณภาพ | `PlanningPolicy` | RAE Legacy Document | Same as above | Major+Minor | PendingReview | 10 files |
| **AcademicServices** | งานบริการวิชาการ | `AcademicServices` | RAE Legacy Document | Same as above | Major+Minor | PendingReview | 43 files |
| **Research** | งานวิจัย | `Research` | RAE Legacy Document | Same as above | Major+Minor | PendingReview | 530+45 files |
| **SOPManuals** | คู่มือปฏิบัติงาน | `SOPManuals` | RAE Legacy Document | Same as above | Major+Minor | PendingReview | 15 files |

### Versioning Configuration (All Libraries)

| Setting | Value |
|---------|-------|
| Versioning enabled | Yes |
| Version type | Major and minor |
| Major version limit | Keep all |
| Minor (draft) version limit | 10 |
| Require check out | No |
| Draft item security | Only authors and approvers |

---

## Content Type Provisioning Order

1. Create **site columns** (all 15 from `library-schema.md`)
2. Create **RAE Document Base** (abstract parent CT)
3. Create **RAE Legacy Document** (inherits from Base; used for 627 files)
4. Create **RAE Active Document** (inherits from Base; for post-migration new docs)
5. Create **RAE Duplicate Reference** (inherits from Base; for 45 duplicates)
6. Create **RAE Metadata Record** (Item-based CT for Microsoft Lists; 100 records)
7. Apply CTs to all 6 libraries
8. Apply RAE Metadata Record to RAE Document Registry list

---

## Column Provisioning Order

SharePoint Site Columns (created in order for dependency resolution):

| Sequence | Column | Type | Required | Indexed | Notes |
|----------|--------|------|----------|---------|-------|
| 1 | DocumentID (RAE_DocumentID) | Single line of text | Yes | Yes | Pattern: RAE-NNNNN |
| 2 | Category (RAE_Category) | Single line of text | Yes | Yes | Taxonomy slug |
| 3 | Subcategory (RAE_Subcategory) | Single line of text | Yes | Yes | Free text |
| 4 | Owner (RAE_Owner) | Single line of text | Yes | Yes | Default: TBD |
| 5 | DocumentStatus (RAE_DocumentStatus) | Choice | Yes | Yes | 6 values |
| 6 | Version (RAE_Version) | Single line of text | No | No | Default: 1.0 |
| 7 | UpdatedDate (RAE_UpdatedDate) | Date and Time | No | No | Date only |
| 8 | Tags (RAE_Tags) | Managed Metadata | No | Yes | SEE MANAGED METADATA DECISION |
| 9 | PublicVisibility (RAE_PublicVisibility) | Choice | Yes | Yes | 4 values |
| 10 | LegacySourceURL (RAE_LegacySourceURL) | Hyperlink or Picture | No | No | |
| 11 | MigrationStatus (RAE_MigrationStatus) | Choice | Yes | Yes | 4 values |
| 12 | SHA256 (RAE_SHA256) | Single line of text | No | No | |
| 13 | DuplicateOf (RAE_DuplicateOf) | Single line of text | No | No | |
| 14 | Notes (RAE_Notes) | Multiple lines of text | No | No | |
| 15 | ApprovalStatus (RAE_ApprovalStatus) | Choice | No | No | For RAE Active Document only |
| 16 | ReviewedBy (RAE_ReviewedBy) | Person or Group | No | No | For RAE Active Document only |
| 17 | ReviewDate (RAE_ReviewDate) | Date and Time | No | No | For RAE Active Document only |

---

## Managed Metadata Decision

### Assessment

| Check | Status | Evidence |
|-------|--------|----------|
| Managed Metadata column creation | ❌ NOT_VERIFIED | Term Store requires admin access; no UI evidence available |
| RAE-Tags term set availability | ❌ NOT_VERIFIED | Term Set must be created by Term Store admin |
| Term Store access | ❌ ADMIN_DEPENDENT | Only SharePoint admins and Term Store admins can access |
| Term Store admin dependency | ✅ CONFIRMED | MJU tenant admin required |

### Classification

**`ADMIN_REQUIRED`** — Managed Metadata / Term Store is not accessible through the current user account. Tenant admin involvement is required to:
1. Create the `RAE-Tags` term set in the Term Store
2. Grant Term Store admin access to the designated RAE platform admin (if applicable)

### Fallback Decision

**For initial provisioning:** Use **Single line of text** column type for Tags instead of Managed Metadata.

This is a **temporary fallback** only. The canonical schema (EA-3/EA-4) specifies `Tags` as Managed Metadata for the SharePoint libraries. The fallback allows provisioning to proceed without blocking on Term Store admin access.

| Aspect | Fallback Impact |
|--------|-----------------|
| EA-3 Schema Compliance | ✅ Not violated — text column is a permitted initial implementation; Managed Metadata is the target state |
| EA-4 Registry Schema | ✅ No impact — registry already uses text-based Tags (semicolon-separated) per `registry-list-schema.md` |
| Data Migration | ✅ No impact — Tags are not part of migration critical path (no legacy tags to migrate) |
| Future Conversion | Text → Managed Metadata conversion requires creating a new column, migrating data, and removing old column. Power Automate can automate this. |

**Target state:** Convert to Managed Metadata `RAE-Tags` term set once Term Store access is available.

---

## Microsoft Lists Parameters

### List Creation Parameters

| Parameter | Value | Evidence |
|-----------|-------|----------|
| List Name | RAE Document Registry | Approved design |
| List Description | Authoritative operational registry for RAE documents | — |
| Platform | Microsoft Lists (custom list) | CONFIRMED AVAILABLE |
| Save Location | RAE Document Center SharePoint site | Requires site creation first |
| Blank list creation | ✅ AVAILABLE | Standard Lists feature |
| SharePoint site location support | ✅ CONFIRMED | Lists can be attached to any SharePoint site |

### Registry Column Compatibility

| Registry Column | Lists Type | Required | Indexed | Supported in Tenant |
|----------------|------------|----------|---------|---------------------|
| DocumentID | Single line of text | Yes | Yes (Unique) | ✅ Standard |
| Title | Single line of text | Yes | Yes | ✅ Standard |
| Description | Multiple lines of text | No | No | ✅ Standard |
| Category | Choice | Yes | Yes | ✅ Standard |
| Subcategory | Single line of text | No | Yes | ✅ Standard |
| Tags | Single line of text | No | No | ✅ Standard (semicolon-separated) |
| Audience | Choice (multi-select) | No | No | ✅ Standard |
| Owner | Person or Group | Yes | Yes | ✅ CONFIRMED |
| Department | Single line of text | No | No | ✅ Standard |
| Status | Choice | Yes | Yes | ✅ Standard (7 canonical values) |
| Visibility | Choice | Yes | Yes | ✅ Standard (4 canonical values) |
| UpdatedDate | Date and Time | Yes | Yes | ✅ Standard |
| ReviewDate | Date and Time | No | Yes | ✅ Standard |
| PublishedDate | Date and Time | No | Yes | ✅ Standard |
| StorageURL | Hyperlink | Yes* | No | ✅ Standard |
| LegacySourceURL | Hyperlink | No | No | ✅ Standard |
| RelatedDocuments | Single line of text | No | No | ✅ Standard |
| DuplicateOf | Single line of text | No | No | ✅ Standard |
| SourceSystem | Choice | Yes | Yes | ✅ Standard (5 values) |
| Version | Single line of text | No | No | ✅ Standard |
| Notes | Multiple lines of text | No | No | ✅ Standard |
| RecordVersion | Number | No | No | ✅ Standard (DEFERRED) |

### Indexing

Microsoft Lists supports indexing. Index strategy from `registry-list-schema.md` §5 (11 indexed columns) is within supported limits.

### Validation Rules

Minimal validation is applied at Lists level:
- Required field enforcement (native Lists behavior)
- Choice column value restriction (native)
- Unique constraint on DocumentID

Advanced validation rules from `registry-validation-rules.md` are enforced by Power Automate (EA-5), not at Lists schema level.

> **Note:** Microsoft Lists does NOT support Managed Metadata columns. The registry `Tags` field uses text (semicolon-separated) as designed in `registry-list-schema.md`. This is architecturally correct and does not need change.

---

## Registry Column Provisioning Order

Provision order for Microsoft List columns (sequence matters for dependency resolution):

| Sequence | Column | Type | Required | Notes |
|----------|--------|------|----------|-------|
| 1 | DocumentID | Text | Yes | Unique; set before all other fields |
| 2 | Title | Text | Yes | |
| 3 | Description | Multi-text | No | |
| 4 | Category | Choice | Yes | 6 values from taxonomy |
| 5 | Subcategory | Text | No | |
| 6 | Tags | Text | No | Semicolon-separated |
| 7 | Audience | Choice (multi) | No | 6 values |
| 8 | Owner | Person/Group | Yes | |
| 9 | Department | Text | No | |
| 10 | Status | Choice | Yes | 7 canonical values: draft, review, approved, published, current, obsolete, archived |
| 11 | Visibility | Choice | Yes | 4 canonical values: public, internal, restricted, private |
| 12 | UpdatedDate | Date | Yes | Date only |
| 13 | ReviewDate | Date | No | |
| 14 | PublishedDate | Date | No | |
| 15 | StorageURL | Hyperlink | Yes* | Conditional |
| 16 | LegacySourceURL | Hyperlink | No | |
| 17 | RelatedDocuments | Text | No | |
| 18 | DuplicateOf | Text | No | |
| 19 | SourceSystem | Choice | Yes | 5 values |
| 20 | Version | Text | No | |
| 21 | Notes | Multi-text | No | |
| 22 | RecordVersion | Number | No | DEFERRED |

---

## Internal Name Capture Strategy

### Problem Statement

SharePoint and Microsoft Lists generate internal names for columns based on display names at creation time. These internal names are required for:
- Power Automate flows (EA-5) referencing columns in expressions
- REST API calls (EA-7/EA-8)
- Export Contract column mapping (`registry-export-contract.md`)
- Field mapping between SharePoint and Registry (`sharepoint-registry-field-map.csv`)

Internal names CANNOT be reliably determined from display names alone. SharePoint appends suffix numbers (e.g., `FieldName`, `FieldName0`, `FieldName1`) when collisions occur.

### Strategy

**Phase 1 — Pre-Provisioning (THIS DOCUMENT):**
Define the recommended/projected internal names based on display names.

**Phase 2 — Provisioning Execution:**
Follow the deterministic capture order:

```
Create column (via UI or PnP)
    ↓
Capture generated internal name (via URL parameter inspection or REST API)
    ↓
Record mapping (in internal name evidence file)
    ↓
Validate type matches schema
    ↓
Proceed to next field
```

### Capture Method

After each column creation:
1. **REST API:** `GET /_api/web/fields/getbytitle('{DisplayName}')` — returns `InternalName` in response
2. **URL Inspection:** SharePoint column settings page URL contains internal name as query parameter
3. **PnP PowerShell:** `Get-PnPField -Identity "{DisplayName}"` — returns full field schema including `InternalName`

### Recommended Internal Names (Projected)

Based on approved `library-schema.md` and `registry-list-schema.md`:

#### SharePoint Site Columns

| Display Name | Recommended Internal Name | Notes |
|-------------|--------------------------|-------|
| DocumentID | `RAE_DocumentID` | Prefix ensures uniqueness |
| Category | `RAE_Category` | |
| Subcategory | `RAE_Subcategory` | |
| Owner | `RAE_Owner` | |
| DocumentStatus | `RAE_DocumentStatus` | |
| Version | `RAE_Version` | |
| UpdatedDate | `RAE_UpdatedDate` | |
| Tags | `RAE_Tags` | Fallback: text column |
| PublicVisibility | `RAE_PublicVisibility` | |
| LegacySourceURL | `RAE_LegacySourceURL` | |
| MigrationStatus | `RAE_MigrationStatus` | |
| SHA256 | `RAE_SHA256` | |
| DuplicateOf | `RAE_DuplicateOf` | |
| Notes | `RAE_Notes` | |
| ApprovalStatus | `RAE_ApprovalStatus` | Active Document only |
| ReviewedBy | `RAE_ReviewedBy` | Active Document only |
| ReviewDate | `RAE_ReviewDate` | Active Document only |

#### Microsoft List Columns (RAE Document Registry)

| Display Name | Recommended Internal Name | Notes |
|-------------|--------------------------|-------|
| Document ID | `RAE_DocumentID` | Lists defaults to `_{GUID}` pattern; recommended prefix |
| Title | `RAE_Title` | |
| Description | `RAE_Description` | |
| Category | `RAE_Category` | |
| Subcategory | `RAE_Subcategory` | |
| Tags | `RAE_Tags` | |
| Audience | `RAE_Audience` | |
| Owner | `RAE_Owner` | Person/Group |
| Department | `RAE_Department` | |
| Status | `RAE_Status` | |
| Visibility | `RAE_Visibility` | |
| Updated Date | `RAE_UpdatedDate` | |
| Review Date | `RAE_ReviewDate` | |
| Published Date | `RAE_PublishedDate` | |
| Storage URL | `RAE_StorageURL` | |
| Legacy Source URL | `RAE_LegacySourceURL` | |
| Related Documents | `RAE_RelatedDocuments` | |
| Duplicate Of | `RAE_DuplicateOf` | |
| Source System | `RAE_SourceSystem` | |
| Version | `RAE_Version` | |
| Notes | `RAE_Notes` | |
| Record Version | `RAE_RecordVersion` | DEFERRED |

### Internal Name Evidence File

After provisioning, internal names will be recorded in:

**`docs/m365/m365-internal-name-registry.csv`**

Format:

```csv
ResourceType,ParentResource,DisplayName,RecommendedInternalName,ActualInternalName,GeneratedGUID,Match,Notes
SiteColumn,RAE Document Center,DocumentID,RAE_DocumentID,,,PENDING,Verify after creation
ListColumn,RAE Document Registry,Document ID,RAE_DocumentID,,,PENDING,Verify after creation
```

---

## Permission Validation Plan

### Steps (Post-Provisioning)

1. Verify default site permissions (site owner = creator = tenant admin)
2. Create 6 Category Owner SharePoint groups: `RAE-DC-{Library}-Owners`
3. Create `RAE-DC-Contributors` group
4. Create `RAE-DC-Readers` group
5. Create `RAE-DC-ArchiveManagers` group
6. Break permission inheritance on each library
7. Apply library-specific permissions per `permissions-matrix.md`
8. Create `_Inbox`, `_Review`, `_Archive` folders with scoped permissions
9. Verify library-level permission enforcement
10. Verify folder-level permission scoping

### Pre-requisite

Named Category Owners must be confirmed and added to their respective `RAE-DC-{Library}-Owners` groups.

---

## Public Sharing Validation Plan

### Steps (Post-Provisioning)

1. Verify tenant-level external sharing policy (admin task)
2. Confirm "Anyone" links are enabled at site level (or scope down if restricted)
3. Create sample view-only sharing link for a test document
4. Verify anonymous access renders document without authentication
5. Document the exact sharing link format and expiration behavior

### Current State

External/Anonymous sharing is **CONFIRMED ENABLED** at tenant level (SPO-015). Site-level configuration will be set during provisioning to match approved design:
- Default: Disabled
- Enable per-document via view-only link for Public visibility documents only

---

## Rollback / Cleanup Plan

| Scenario | Rollback Action | Reversible? |
|----------|-----------------|-------------|
| Site creation fails | Delete site from SharePoint admin center | ✅ Yes (within 30 days) |
| Library misconfigured | Delete library and recreate | ✅ Yes (if empty) |
| Content type error | Delete and recreate CT | ✅ Yes (if no items use it) |
| Column error | Delete site column | ✅ Yes (if not referenced) |
| List misconfigured | Delete list and recreate | ✅ Yes (if empty) |
| Permission error | Reset to parent permission inheritance | ✅ Yes |
| Sharing misconfiguration | Disable external sharing at site level | ✅ Yes |
| Term Set error | Delete and recreate term set | ✅ Yes (if no columns use it) |

**General principle:** Provision in this order to minimize rollback impact: Site → Libraries → CTs → Columns → List → Permissions → Sharing. Validate at each step before proceeding.

---

## Provisioning Evidence Requirements

| Evidence | Method | Record Location |
|----------|--------|-----------------|
| Site created | Screenshot of site home page | `docs/m365/evidence/provisioning/` |
| Site URL | Record from browser URL | `m365-provisioning-manifest.csv` |
| Library created | Screenshot of library in site contents | Evidence directory |
| Content type applied | Screenshot of library content type settings | Evidence directory |
| Column internal name | REST API or PnP output | `m365-internal-name-registry.csv` |
| List created | Screenshot of list view | Evidence directory |
| Permissions applied | Screenshot of permission settings | Evidence directory |
| Versioning configured | Screenshot of library versioning settings | Evidence directory |
| Sharing disabled | Screenshot of site sharing settings | Evidence directory |

---

## Post-Provision Validation

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| All 6 libraries exist | Site Contents inspection | 6 libraries visible with correct names |
| Content types on each library | Library settings | RAE Legacy Document available |
| All columns present | Column listing | All 15 site columns present |
| DocumentID unique | Column settings | Unique constraint enabled |
| Indexed columns configured | Column listing | All indexed columns show index icon |
| List created | Lists app | RAE Document Registry visible |
| List columns match schema | List settings | All 22 columns present with correct types |
| Status values | Choice column edit | Exactly 7 canonical values |
| Visibility values | Choice column edit | Exactly 4 canonical values |
| Owner values | Person/Group column | Person or Group selection enabled |
| Permission groups | Site permissions | All groups created with correct permission levels |
| Folder structure | Library navigation | _Inbox, _Review, _Archive present in each library |

---

## EA-5 Handoff Requirements

Before EA-5 can begin:

| Prerequisite | Responsible | Target State |
|--------------|-------------|--------------|
| RAE Document Center site created | Tenant Admin | Site URL accessible |
| 6 libraries provisioned | Platform Admin | Libraries with correct schema |
| Content types applied | Platform Admin | CTs assigned to all libraries |
| Site columns created | Platform Admin | Columns with captured internal names |
| Internal name registry completed | Platform Admin | `m365-internal-name-registry.csv` populated |
| RAE Document Registry list created | Platform Admin | List with 22 columns |
| Registry column internal names captured | Platform Admin | Names recorded |
| Permission groups created | Platform Admin | All groups with correct members |
| Term Store accessible | Tenant Admin | RAE-Tags term set created |
| Owner groups populated | Category Owners | Named individuals assigned |
| Test data available | Platform Admin | 5-10 sample documents uploaded |

---

## Blockers

| Blocker | Impact | Severity | Resolution | Owner |
|---------|--------|----------|------------|-------|
| **B1: No SharePoint admin / site creation access** | Cannot create site, cannot provision resources | 🔴 HIGH | MJU tenant admin must create site or grant site creation permission | Tenant Admin |
| **B2: Named Category Owners unknown** | Cannot create owner groups, cannot assign permissions | 🔴 HIGH | HR/Admin must confirm 6 Category Owner identities | Institutional |
| **B3: Managed Metadata / Term Store admin-dependent** | Tags column cannot use Managed Metadata | 🟡 MEDIUM | Tenant admin creates RAE-Tags term set; fallback: text column for initial provisioning | Tenant Admin |
| **B4: No tenant admin for Term Store** | Term Store operations blocked | 🟡 MEDIUM | Deferred; text fallback unblocks provisioning | Tenant Admin |
| **B5: DLP policy unverified** | Risk of cross-connector flow blocks (EA-5) | 🟡 MEDIUM | Test with scaffold flow after provisioning; admin verification recommended | Platform Admin |
| **B6: Owner groups not created** | Permission model cannot be fully implemented | 🔴 HIGH | Create after site is provisioned | Platform Admin |

---

## Explicit User Authorization Gate

**Before any production provisioning action, the user must provide explicit authorization.**

See `docs/m365/m365-provisioning-authorization-gate.md` for the full list of actions requiring authorization.

**Current authorization status:** `NOT_AUTHORIZED` for all actions.

---

*End of Provisioning Plan — Generated 2026-07-14*
