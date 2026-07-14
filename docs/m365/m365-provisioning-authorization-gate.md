# Provisioning Authorization Gate — RAE Document Center

**Phase:** EA-3P — Provisioning Preflight (Updated per EA-3R/EA-3S Exception)  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Date:** 2026-07-14  
**Status:** EXISTING SITE APPROVED — Actions 1-2: `REUSE_EXISTING_SITE` | Actions 3-11: `NOT_AUTHORIZED`

---

## Purpose

This document lists every production action that requires explicit user authorization before execution. No action listed here may be performed without documented approval.

**Authorization flow:**

```
User provides explicit authorization in chat
    ↓
Action status changes from NOT_AUTHORIZED to AUTHORIZED
    ↓
Action is executed with documented evidence
    ↓
Action status changes to COMPLETED
    ↓
Evidence is recorded in provisioning manifest
```

---

## Authorization Register

### Action 1 — Create SharePoint Site (EXISTING SITE REUSE)

| Field | Value |
|-------|-------|
| **Production Change** | ~~Create RAE Document Center SharePoint Team Site at `/sites/RAEDocumentCenter`~~ **NOT REQUIRED** — Existing RAE site at `/sites/msteams_54adc4` is the approved deployment boundary per `ARCHITECTURE_IMPLEMENTATION_EXCEPTION` (EA-3R/EA-3S) |
| **Impact** | No site creation needed. Existing site is a Private Team Site connected to M365 Group with 23 members |
| **Reversible** | N/A — no site creation action required |
| **Rollback Method** | N/A — the site already exists; the fallback dedicated-site path is the Admin Provisioning Request Package |
| **Required Role** | Site Admin (researchmju@mju.ac.th) — already verified as `IsSiteAdmin = true` |
| **Evidence Required Before Action** | EA-3S readiness closure confirmed: `EXISTING_SITE_READY_FOR_PROVISIONING` |
| **Authorization Status** | **REUSE_EXISTING_SITE — NO CREATION REQUIRED** |

### Action 2 — Create M365 Group (EXISTING GROUP REUSE)

| Field | Value |
|-------|-------|
| **Production Change** | ~~Auto-created with Team Site (Action 1). M365 Group named "RAE Document Center" with email alias RAEDocumentCenter~~ **NOT REQUIRED** — Existing M365 Group for the RAE site is reused per `ARCHITECTURE_IMPLEMENTATION_EXCEPTION` (EA-3R/EA-3S) |
| **Impact** | No group creation needed. Existing M365 Group has 23 members managed through Azure AD |
| **Reversible** | N/A — no group creation action required |
| **Rollback Method** | N/A — group already exists |
| **Required Role** | N/A — group exists; Site Admin has full site management capability |
| **Evidence Required Before Action** | EA-3S condition C4 confirmed: `OWNERSHIP_CLEAR` |
| **Authorization Status** | **REUSE_EXISTING_GROUP — NO CREATION REQUIRED** |

### Action 3 — Create Document Libraries

| Field | Value |
|-------|-------|
| **Production Change** | Create 6 document libraries: Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals |
| **Impact** | Creates empty libraries with default SharePoint settings. No files uploaded |
| **Reversible** | ✅ Yes — Libraries can be deleted if empty |
| **Rollback Method** | Site Contents → Library settings → Delete this document library |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | Site is accessible; Content Types ready |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 4 — Create Content Types

| Field | Value |
|-------|-------|
| **Production Change** | Create 5 site-level content types: RAE Document Base, RAE Legacy Document, RAE Active Document, RAE Duplicate Reference, RAE Metadata Record |
| **Impact** | Adds content types to site collection. Libraries can use these CTs for metadata schema |
| **Reversible** | ✅ Yes — CTs can be deleted if no items use them |
| **Rollback Method** | Site Settings → Site content types → Delete content type |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | Site columns created (Action 5) |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 5 — Create Site Columns

| Field | Value |
|-------|-------|
| **Production Change** | Create 17 site-level columns (15 standard + 3 for Active Document CT) |
| **Impact** | Adds columns to site collection column gallery. Each column has specific type, required, indexed settings |
| **Reversible** | ✅ Yes — Columns can be deleted if not referenced by any content type |
| **Rollback Method** | Site Settings → Site columns → Delete column |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | Site is provisioned; internal name capture strategy ready |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 6 — Create Term Set (Managed Metadata)

| Field | Value |
|-------|-------|
| **Production Change** | Create `RAE-Tags` term set in SharePoint Term Store under `RAE Document Center` group |
| **Impact** | Enables Managed Metadata column for Tags field. Requires Term Store admin access |
| **Reversible** | ✅ Yes — Term set can be deleted if not in use |
| **Rollback Method** | Term Store Management → Term set → Delete |
| **Required Role** | Term Store Administrator |
| **Evidence Required Before Action** | Term Store admin access confirmed; Tags fallback strategy ready for initial provisioning |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 7 — Create Microsoft List

| Field | Value |
|-------|-------|
| **Production Change** | Create RAE Document Registry Microsoft List on RAE Document Center site |
| **Impact** | Creates empty list with default view. Foundation for EA-4 registry implementation |
| **Reversible** | ✅ Yes — List can be deleted if empty |
| **Rollback Method** | Site Contents → List settings → Delete this list |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | Site is provisioned; List columns ready to create (Action 8) |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 8 — Create Registry Columns

| Field | Value |
|-------|-------|
| **Production Change** | Create 22 columns on RAE Document Registry list per `registry-list-schema.md` |
| **Impact** | Defines the full registry schema. Includes Choice, Text, Person/Group, Hyperlink, Date, Multi-text, Number types |
| **Reversible** | ✅ Yes — Columns can be deleted if no items exist |
| **Rollback Method** | List settings → Column → Delete |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | List created (Action 7); internal name capture ready |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 9 — Configure Permissions

| Field | Value |
|-------|-------|
| **Production Change** | Break permission inheritance on all 6 libraries. Create 9 SharePoint groups. Apply library-level and folder-level permissions |
| **Impact** | Changes access control from site-level inheritance to custom library-level permissions. Affects all users accessing the site |
| **Reversible** | ✅ Partially — Permissions can be reset to inherit, but group membership changes must be reversed manually |
| **Rollback Method** | Library settings → Permissions → Delete unique permissions → Inherit permissions from parent |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | Named Category Owners confirmed; groups created with correct members |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 10 — Configure Versioning

| Field | Value |
|-------|-------|
| **Production Change** | Enable major+minor versioning on all 6 libraries. Set draft security to "Only authors and approvers" |
| **Impact** | Increases storage usage over time (major versions kept indefinitely). Controls draft visibility |
| **Reversible** | ✅ Yes — Versioning settings can be changed at any time |
| **Rollback Method** | Library settings → Versioning settings → Restore defaults |
| **Required Role** | Site owner (Full Control) |
| **Evidence Required Before Action** | Libraries created (Action 3) |
| **Authorization Status** | **NOT_AUTHORIZED** |

### Action 11 — Configure Public Sharing

| Field | Value |
|-------|-------|
| **Production Change** | Disable default external sharing on the site. Set sharing policy to "Only per-document view-only links for Public documents" |
| **Impact** | Restricts anonymous access to only explicitly shared documents with PublicVisibility=Public |
| **Reversible** | ✅ Yes — Sharing settings can be changed at site level |
| **Rollback Method** | Site settings → Sharing → Enable broader sharing |
| **Required Role** | SharePoint admin (tenant-level sharing settings) or site owner (site-level) |
| **Evidence Required Before Action** | Tenant-level sharing policy confirmed; external sharing confirmed enabled (SPO-015) |
| **Authorization Status** | **NOT_AUTHORIZED** |

---

## Authorization Summary

| # | Action | Status | Dependencies | Owner |
|---|--------|--------|--------------|-------|
| 1 | Create SharePoint Site | ❌ NOT_AUTHORIZED | Owner identity, URL decision | Tenant Admin |
| 2 | Create M365 Group | ❌ NOT_AUTHORIZED | Auto-created with site | Tenant Admin |
| 3 | Create Document Libraries | ❌ NOT_AUTHORIZED | Site created | Platform Admin |
| 4 | Create Content Types | ❌ NOT_AUTHORIZED | Site columns created | Platform Admin |
| 5 | Create Site Columns | ❌ NOT_AUTHORIZED | Site created, library created | Platform Admin |
| 6 | Create Term Set | ❌ NOT_AUTHORIZED | Term Store admin access | Term Store Admin |
| 7 | Create Microsoft List | ❌ NOT_AUTHORIZED | Site created | Platform Admin |
| 8 | Create Registry Columns | ❌ NOT_AUTHORIZED | List created | Platform Admin |
| 9 | Configure Permissions | ❌ NOT_AUTHORIZED | Category Owners named, groups created | Platform Admin |
| 10 | Configure Versioning | ❌ NOT_AUTHORIZED | Libraries created | Platform Admin |
| 11 | Configure Public Sharing | ❌ NOT_AUTHORIZED | Tenant sharing confirmed | Site Owner / Admin |

---

## Authorization Protocol

### How to Authorize

1. User reviews this gate document
2. User states "I authorize Action X" in chat (or the batch)
3. Authorization status changes to **AUTHORIZED**
4. Action is executed with documented evidence
5. Status updates to **COMPLETED** with evidence reference

### What Authorization Means

- The user confirms the action matches the approved EA-3/EA-4 design
- The user accepts the operational impact described in the "Impact" field
- The user acknowledges the rollback method is available
- The user understands this is a production infrastructure action

### What Authorization Does NOT Mean

- It does not override tenant admin requirements
- It does not waive security review or compliance checks
- It does not authorize unapproved deviation from EA-3/EA-4 design

---

*End of Authorization Gate Document — Generated 2026-07-14*
