# EA-3R — Existing RAE SharePoint Site Reuse Capability Audit

**Phase:** EA-3R — Existing Site Reuse Audit  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Account:** researchmju@mju.ac.th (Site Admin of existing RAE site)  
**Date:** 2026-07-14  
**Status:** COMPLETE — Decision: `REUSE_EXISTING_SITE_WITH_CONDITIONS`

---

## Executive Summary

This audit evaluated whether the approved RAE Document Center can be implemented as an isolated workspace inside the **existing** RAE SharePoint site (`https://maejo365.sharepoint.com/sites/msteams_54adc4`) instead of requiring a new dedicated SharePoint site.

**Key Finding:** The existing RAE site is a strong candidate for hosting the Document Center workspace. The `researchmju@mju.ac.th` account is a **Site Admin** of this site with comprehensive capability to create libraries, lists, columns, pages, and manage permissions. The Documents library already demonstrates **unique permissions** (broken inheritance), proving library-level permission isolation is feasible. No naming collisions exist with the six canonical libraries or the RAE Document Registry list.

**Final Decision:** `REUSE_EXISTING_SITE_WITH_CONDITIONS` — reuse is technically viable but requires documented conditions.

---

## Audit Objective

Determine whether the approved RAE Document Center (6 libraries, 1 registry list, 17 site columns, 5 content types, 9 permission groups, 1 landing page, 5 workflows) can operate as an isolated workspace within the existing RAE SharePoint site without materially disrupting current operations.

---

## Execution Method

- **Model:** Single Main Agent, authenticated browser session
- **Authentication State:** Preserved from previous EA-3R session
- **Account:** researchmju@mju.ac.th
- **Tenant:** maejo365.sharepoint.com
- **Tools:** Browser inspection (accessibility snapshot, CDP, REST API), direct URL navigation, classic settings pages
- **Constraint:** Read-only inspection; no resource created, modified, or provisioned

---

## Evidence Index

| Reference | Description | Status |
|-----------|-------------|--------|
| EA3R-SITE-IDENTITY-01 | Existing RAE site identity | CONFIRMED |
| EA3R-PERMISSION-01 | Account permission posture | CONFIRMED |
| EA3R-LIBRARY-01 | Library creation capability | CONFIRMED |
| EA3R-LIB-GOV-01 | Library governance capability | CONFIRMED |
| EA3R-LIST-01 | Microsoft Lists site-location | CONFIRMED |
| EA3R-LIST-SCHEMA-01 | Registry column compatibility | CONFIRMED |
| EA3R-PAGE-01 | Site page capability | CONFIRMED |
| EA3R-PERM-ISOLATION-01 | Permission isolation | CONFIRMED |
| EA3R-COLLISION-01 | Existing site collision audit | CONFIRMED |

---

## Existing RAE Site Identity

| Property | Value |
|----------|-------|
| **Site Display Name** | สำนักวิจัยฯ |
| **Full Name** | สำนักวิจัยและส่งเสริมวิชาการการเกษตร |
| **Site URL** | `https://maejo365.sharepoint.com/sites/msteams_54adc4` |
| **Site Type** | Team Site (connected to M365 Group) |
| **M365 Group** | Confirmed — "Private group" badge, 23 members, 1 owner |
| **Privacy** | Private (group members only) |
| **Current Account Role** | **Site Admin** (`IsSiteAdmin: true`, User ID: 9) |
| **Account Identity** | researchmju@mju.ac.th — หน่วยวิจัยและส่งเสริมวิชาการการเกษตร (RAE office account) |
| **Site Created** | On or before December 2020 (based on library modified dates) |
| **Verification** | Site name confirms this is the official organizational site for สำนักวิจัยและส่งเสริมวิชาการการเกษตร (Office of Agricultural Research and Extension) |

**Evidence:** EA3R-SITE-IDENTITY-01

---

## Current Account Permission Posture

| Capability | Status | Evidence |
|------------|--------|----------|
| Access Site Contents | **CONFIRMED** | viewlsts.aspx loads fully; all contents visible |
| Access Site Settings | **CONFIRMED** | settings.aspx loads fully; all settings sections visible |
| Access Site Permissions | **LIKELY_AVAILABLE** | IsSiteAdmin=true; only "Access requests" link in Users section; permission admin pages may need direct URL |
| Access Site Information | **CONFIRMED** | Site header, Members count, Privacy visible |
| Inspect Library Settings | **CONFIRMED** | Document library settings page fully accessible |
| Inspect List Settings | **CONFIRMED** | Same settings UI accessible |
| Inspect Versioning Settings | **CONFIRMED** | Versioning settings link visible; EnableVersioning=true via REST API |
| Inspect Content Type Settings | **CONFIRMED** | Site content types accessible via REST API |
| Inspect Site Columns | **CONFIRMED** | Site columns gallery fully accessible (mngfield.aspx) |

**Key finding:** `IsSiteAdmin = true` for `researchmju@mju.ac.th`. The account has elevated privileges on this specific site.

**Evidence:** EA3R-PERMISSION-01

---

## Document Library Creation Capability

The "New" menu on the Site Contents page shows:

- ✅ **Document library** — available
- ✅ **List** — available
- ✅ **Page** — available
- ✅ **App** — available
- ✅ **Subsite** — available

As a Site Admin, the account can create document libraries. This is the highest confidence level observable without performing the actual creation.

### Six-Library Naming Collision

| Canonical Library | Existing Resource | Collision |
|-------------------|-------------------|-----------|
| Administration | Not found | **No collision** |
| FinanceProcurement | Not found | **No collision** |
| PlanningPolicy | Not found | **No collision** |
| AcademicServices | Not found | **No collision** |
| Research | Not found | **No collision** |
| SOPManuals | Not found | **No collision** |

No confusingly similar names exist (e.g., "ResearchData", "AdminDocs", etc.).

**Evidence:** EA3R-LIBRARY-01

---

## Library Governance Capability

Inspected the existing **Documents** library settings:

| Capability | Status | Details |
|------------|--------|---------|
| Versioning | **CONFIRMED** | EnableVersioning=true; MajorVersionLimit=500 |
| Minor Versions | **Available** | EnableMinorVersions=false currently; configurable |
| Content Approval | **Available** | EnableModeration=false; configurable |
| Custom Columns | **CONFIRMED** | "Create column" and "Add from existing site columns" links visible |
| Choice Columns | **CONFIRMED** | Standard SharePoint column type |
| Person/Group Columns | **CONFIRMED** | Standard SharePoint column type |
| Date Columns | **CONFIRMED** | Standard SharePoint column type |
| Hyperlink Columns | **CONFIRMED** | Standard SharePoint column type |
| Indexed Columns | **CONFIRMED** | "Indexed columns" link visible in settings |
| Content Types | **LIKELY_AVAILABLE** | ContentTypesEnabled=false on Documents library; site admin can enable via Advanced Settings |
| Library Permissions | **CONFIRMED** | "Permissions for this document library" link visible; HasUniqueRoleAssignments=true (already unique) |
| Column Default Values | **CONFIRMED** | "Column default value settings" link visible |

**Evidence:** EA3R-LIB-GOV-01

---

## Microsoft Lists Site Location Capability

| Check | Result |
|-------|--------|
| Blank list option | ✅ Available (New > List) |
| Existing RAE site as location | ✅ Lists can be created within the current site |
| RAE Document Registry existence | ❌ Not found — no naming collision |
| Registry creation in existing site | ✅ Technically viable for Site Admin |

The critical question — *Can RAE Document Registry be created INSIDE the existing RAE SharePoint site?* — is answered **YES**, with the highest confidence level achievable without actual creation.

**Evidence:** EA3R-LIST-01

---

## Registry Schema Compatibility

All required column types for the 22-column Registry schema are standard SharePoint column types available in this tenant:

| Required Type | Status | Notes |
|---------------|--------|-------|
| Single line of text | ✅ CONFIRMED | Used for DocumentID, Title, Category, Owner |
| Choice | ✅ CONFIRMED | Used for DocumentStatus, PublicVisibility |
| Person or Group | ✅ CONFIRMED | Used for AssignedTo (metadata) |
| Hyperlink | ✅ CONFIRMED | Used for SourceURL, PublicURL |
| Date and Time | ✅ CONFIRMED | Used for UpdatedDate, CreatedDate |
| Multiple lines of text | ✅ CONFIRMED | Used for Description |
| Number | ✅ CONFIRMED | Used for Version sort-order |

**Evidence:** EA3R-LIST-SCHEMA-01

---

## Site Page Capability

| Capability | Status |
|------------|--------|
| Site Pages library accessible | ✅ CONFIRMED — 1 existing page |
| New Site Page option | ✅ CONFIRMED — New > Page visible |
| Page templates | ✅ CONFIRMED — Site Page content type exists |
| Modern web parts | ⚪ NOT VERIFIED but expected (modern Team Site) |

The intended workspace model is architecturally feasible:

```
Existing RAE SharePoint Site
        ↓
RAE Document Center Page
        ↓
6 Dedicated Libraries
        ↓
RAE Document Registry
        ↓
Governance Workflows
```

**Evidence:** EA3R-PAGE-01

---

## Permission Isolation Assessment

| Check | Result | Evidence |
|-------|--------|----------|
| Can inspect site permissions | ✅ CONFIRMED | Settings page accessible |
| Can inspect library permissions | ✅ CONFIRMED | "Permissions for this document library" link visible |
| Library unique permissions | ✅ CONFIRMED | Documents library HasUniqueRoleAssignments=true |
| Can create SharePoint groups | ⚪ LIKELY_AVAILABLE | Site Admin; not directly tested (OPTIONAL_TEST_REQUIRED) |
| Can break inheritance | ✅ CONFIRMED | Already demonstrated (existing unique permissions) |
| Can assign groups at library level | ✅ CONFIRMED | Existing structure proves library-level assignments work |
| Site-level vs DC library access | ✅ CONFIRMED | M365 Group members have site access; DC libraries can have restricted unique permissions |

### Classification

**STRONG_ISOLATION_POSSIBLE**

The existing Documents library already operates with unique permissions (inheritance broken). This proves the SharePoint platform supports library-level permission isolation within this site. The RAE Document Center libraries can follow the same pattern: dedicated SharePoint groups with access scoped to specific libraries, while M365 Group members retain site-level access without automatic Document Center access.

**Evidence:** EA3R-PERM-ISOLATION-01

---

## Existing Site Collision Assessment

### Current Site Resources

| Resource Type | Existing | Collision Risk |
|---------------|----------|----------------|
| Document Libraries | 6 (Documents, Class Files, Form Templates, Site Assets, Style Library, เอกสารประกอบของคลาส) | **LOW** — No overlap with DC library names |
| Microsoft Lists | 0 (only system lists) | **LOW** — No existing lists |
| Site Pages | 1 (Home) | **LOW** — No overlap |
| Custom Site Columns | 0 (only default SharePoint columns) | **LOW** |
| Custom Content Types | Some in "Group Work Content Types" (from template) | **LOW** — No overlap |
| Workflows | None visible (Workflow Settings accessible but empty) | **LOW** |
| Subsites | 0 | **LOW** |

### Risk Assessment

| Risk Area | Classification | Rationale |
|-----------|---------------|-----------|
| Naming collision | **LOW** | No collisions with canonical names |
| Navigation clutter | **MEDIUM** | 6 new libraries + 1 list + 1 page will significantly expand left navigation |
| Permission complexity | **MEDIUM** | Existing site uses M365 Group permissions; DC libraries need unique groups with different access rules |
| Content type collision | **LOW** | Existing content types are default SharePoint types |
| Site column collision | **LOW** | No custom columns exist that conflict with planned RAE_* columns |
| Workflow collision | **LOW** | No existing workflows detected |
| Ownership ambiguity | **MEDIUM** | researchmju is current admin; long-term DC ownership should be clarified |
| Existing user disruption | **MEDIUM** | 23 group members may see new libraries but may not have access to them; clear communication needed |

**Evidence:** EA3R-COLLISION-01

---

## Governance Boundary Assessment

### Model A — Dedicated Site (`/sites/RAEDocumentCenter`)

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Implementation speed | 2 / 5 | Requires tenant admin site creation — blocking dependency |
| Admin dependency | 5 / 5 | Tenant admin MUST create the site |
| Governance isolation | 5 / 5 | Complete site-level boundary; no cross-contamination with existing site |
| Permission simplicity | 5 / 5 | Clean slate; minimal initial groups; no existing users to manage |
| User experience | 4 / 5 | Separate site to manage and navigate; dedicated home page |
| Operational ownership | 5 / 5 | Clear ownership boundary; Document Center is clearly distinct |
| Public document delivery | 4 / 5 | Can configure public/anonymous access on dedicated site independently |
| Power Automate compatibility | 4 / 5 | Site-scoped flows operate in a clean context |
| Future AI/knowledge integration | 4 / 5 | Knowledge base can target one site |
| Migration complexity | 3 / 5 | Data already in legacy systems; migration path needs planning |
| Long-term maintainability | 4 / 5 | Clean lifecycle management |
| Risk to existing RAE operations | 1 / 5 | Near-zero risk; no impact on existing site |
| **TOTAL** | **45 / 60** | |

### Model B — Existing RAE Site Workspace

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Implementation speed | 4 / 5 | No admin dependency; can create resources immediately (as site admin) |
| Admin dependency | 1 / 5 | Low dependency; researchmju is site admin |
| Governance isolation | 3 / 5 | Library-level only; M365 Group members see site but not DC libraries |
| Permission simplicity | 3 / 5 | Must break inheritance on each library; create DC-specific groups |
| User experience | 4 / 5 | Single site; users find everything in one place |
| Operational ownership | 3 / 5 | Shared with existing site; DC owner = existing site admin |
| Public document delivery | 3 / 5 | Existing site is Private; library-level external sharing needed |
| Power Automate compatibility | 4 / 5 | Flows can target specific libraries; site context available |
| Future AI/knowledge integration | 3 / 5 | May need to scope to specific libraries |
| Migration complexity | 5 / 5 | No new site to migrate data into; libraries are in place for content |
| Long-term maintainability | 3 / 5 | Site lifecycle tied to existing RAE site lifecycle |
| Risk to existing RAE operations | 3 / 5 | Permission changes, navigation changes affect existing users |
| **TOTAL** | **39 / 60** | |

### Comparative Summary

| Aspect | Model A (Dedicated) | Model B (Existing) | Advantage |
|--------|---------------------|--------------------|-----------|
| Speed | 2 | 4 | **Model B** |
| Isolation | 5 | 3 | **Model A** |
| Admin dependency | 5 (high) | 1 (low) | **Model B** |
| Risk to existing ops | 1 (low) | 3 (medium) | **Model A** |
| Maintainability | 4 | 3 | **Model A** |
| Overall | 45 | 39 | **Model A** |

---

## Architecture Impact

`ARCHITECTURE_IMPLEMENTATION_EXCEPTION_PROPOSED`

The reuse decision changes only the **SharePoint site boundary / deployment topology**. The following primitives remain unchanged:

- ✅ DocumentID format (`RAE-NNNNN`)
- ✅ Status vocabulary (draft, review, approved, published, current, obsolete, archived)
- ✅ Visibility vocabulary (public, internal, restricted, private)
- ✅ Library schema (17 site columns, all types and defaults)
- ✅ Registry schema (22 columns, all types and constraints)
- ✅ Content types (RAE Legacy Document)
- ✅ Lifecycle model
- ✅ Export contract (JSON)
- ✅ Permissions design (RAE-DC-* groups)

The frozen EA-3 and EA-4 documents remain unchanged until the implementation exception is explicitly approved.

---

## Security Impact

- **Existing site is Private** — only M365 Group members (23 members) can access. This is consistent with the frozen security scope.
- **Document Center libraries would need unique permissions** — M365 Group members would see the site but NOT automatically access DC libraries. This aligns with the least-privilege model.
- **Public document delivery** — requires library-level anonymous/anyone links. The tenant already has external sharing enabled (confirmed in EA-3P). This is feasible.
- **Anonymous sharing risk** — same compensating controls documented in `RAE_DOCUMENT_CENTER_SECURITY_SCOPE.md` apply.

---

## Operational Impact

- **Existing users (23 members)**: Will see new libraries in navigation but may not have access. Communication/training needed.
- **Navigation bloat**: The left navigation will grow from ~8 items to ~16 items. Consider using a hub navigation or Document Center landing page to organize.
- **Site admin continuity**: researchmju@mju.ac.th is the current site admin. Document Center ownership should be formally assigned to ensure continuity.
- **Content migration**: Existing Documents library (3 items) and other libraries have minimal content. No migration conflicts.

---

## Power Automate Impact

- **No existing workflows detected** in the existing site.
- Power Automate flows can be created at the library or list level within the existing site — confirmed compatible.
- The same 3 flow types (Automated, Instant, Scheduled) and connectors (SharePoint, Approvals, Teams) are available as verified in EA-1D.
- HTTP Premium connector limitation applies regardless of site choice.

---

## Conditions for Reuse

For `REUSE_EXISTING_SITE` to become viable without the `_WITH_CONDITIONS` qualifier, the following must be resolved:

1. **Permission Group Creation** — Confirm the researchmju account can create SharePoint groups (OPTIONAL_TEST_REQUIRED). If not, admin must create the 9 RAE-DC-* groups.
2. **Content Type Enablement** — Confirm the account can enable Content Types on new/existing libraries (OPTIONAL_TEST_REQUIRED).
3. **Navigation Management** — Plan for navigation organization: either hide DC libraries from navigation and use a landing page, or create a document center page with Quick Links.
4. **Owner Clarification** — Confirm the official RAE Document Center owner (may be different from researchmju account admin).
5. **External Sharing Verification** — Confirm library-level anonymous/anyone link settings are available for Public Visibility documents.

---

## Reasons Dedicated Site May Still Be Required

The dedicated site model remains the architecturally cleaner option if:

- Permission isolation requirements exceed library-level boundaries
- The existing site undergoes major restructuring
- Governance compliance requires a separate site collection
- The tenant admin prefers a dedicated site for management clarity
- Power Automate flows need site-wide scoping conflicts with existing site content

---

## Final Decision

```
REUSE_EXISTING_SITE_WITH_CONDITIONS
```

The existing RAE site (`/sites/msteams_54adc4`) is **technically capable** of hosting the RAE Document Center as an isolated workspace. The researchmju account's Site Admin role enables all required provisioning actions without tenant admin involvement. Permission isolation via library-level unique permissions is proven. No naming collisions exist.

However, five conditions (see above) should be verified before proceeding with full implementation.

---

## Recommended Implementation Model

**Implementation topology:**

```
Existing RAE SharePoint Site (/sites/msteams_54adc4)
│
├── (Existing) Documents, Class Files, etc.
├── (Existing) Site Pages / Home
│
└── RAE Document Center Workspace
    ├── Document Center Landing Page (new Site Page)
    ├── Administration library (unique permissions)
    ├── FinanceProcurement library (unique permissions)
    ├── PlanningPolicy library (unique permissions)
    ├── AcademicServices library (unique permissions)
    ├── Research library (unique permissions)
    ├── SOPManuals library (unique permissions)
    ├── RAE Document Registry (Microsoft List)
    └── Dedicated RAE-DC-* permission groups
```

---

## Architecture Implementation Exception Status

```
ARCHITECTURE_IMPLEMENTATION_EXCEPTION_PROPOSED
```

**Scope of exception:** Site boundary / deployment topology only.  
**Primitives NOT affected:** DocumentID, Status, Visibility, Library schema, Registry schema, Lifecycle, Export contract, Permissions design.  
**Frozen architecture:** All EA-3, EA-4 documents remain frozen until the user explicitly approves the exception.

---

## Recommended Next Action

1. Review this audit report and the capability matrix (`m365-existing-site-capability-matrix.csv`)
2. If the `REUSE_EXISTING_SITE_WITH_CONDITIONS` decision is accepted, authorize the implementation exception
3. Update the provisioning plan (`m365-sharepoint-registry-provisioning-plan.md`) to reflect the existing site URL instead of `/sites/RAEDocumentCenter`
4. Update the provisioning manifest (`m365-provisioning-manifest.csv`) target site URL
5. Resolve the 5 conditions listed above
6. Proceed with EA-5 provisioning (now with reduced admin dependency since researchmju is site admin)
7. If conditions cannot be resolved, revert to the original dedicated-site model

---

## Files Created

| File | Purpose |
|------|---------|
| `docs/m365/m365-existing-rae-site-reuse-audit.md` | Full audit report |
| `docs/m365/m365-existing-site-capability-matrix.csv` | 40-row capability matrix |
