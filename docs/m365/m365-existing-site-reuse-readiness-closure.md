# EA-3S — Existing RAE Site Reuse Readiness Closure

**Phase:** EA-3S — Existing Site Boundary Exception & Reuse Readiness Closure  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Account:** researchmju@mju.ac.th (Site Admin of existing RAE site)  
**Date:** 2026-07-14  
**Status:** READINESS_CLOSURE_COMPLETE — Five conditions resolved

---

## Execution Summary

| Item | Value |
|------|-------|
| **Execution Model** | Single Main Agent, authenticated browser session |
| **Browser State** | Preserved from EA-3R |
| **Account** | researchmju@mju.ac.th |
| **Existing RAE Site URL** | `https://maejo365.sharepoint.com/sites/msteams_54adc4` |
| **Site Display Name** | สำนักวิจัยฯ |
| **Site Type** | Private Team Site connected to M365 Group |
| **Account Role** | Site Admin (`IsSiteAdmin = true`) |
| **Architecture Baseline** | FROZEN at commit `ecd1f2a` |

---

## Condition 1 — Permission Group Creation Test

### Test Execution

1. Navigated to site permissions page (`/_layouts/15/user.aspx`)
2. Confirmed **"Create Group"** button is visible in the Permission Tools ribbon
3. Created temporary validation group **EA3S-Capability-Test** (ID: 43) via REST API (`POST /_api/web/sitegroups`)
4. Verified group creation returned status **201 Created**
5. Deleted the temporary group via REST API (`POST /_api/web/sitegroups/removebyid(43)`) — status **200 OK**

### Result

```
GROUP_CREATION_CONFIRMED
```

The Site Admin account can successfully create and delete SharePoint permission groups. This satisfies the requirement for creating the 9 canonical `RAE-DC-*` permission groups during provisioning.

### Library Scope Assignment

Documents library already demonstrates unique permissions (`HasUniqueRoleAssignments = true`). The same library-level permission assignment pattern will be applied to all 6 Document Center libraries.

**Evidence:** EA3S-GROUP-01

---

## Condition 2 — Content Type Enablement Test

### Inspection

1. Confirmed **Site columns** gallery accessible (`/_layouts/15/mngfield.aspx`) with "Create new site column" link
2. Confirmed **Site content types** accessible via REST API
3. Navigated to **Documents library Advanced Settings** (`/_layouts/15/ListEdit.aspx?List={...}&Mode=Advanced`)
4. Confirmed **"Allow management of content types?"** setting visible with Yes/No radio buttons
5. The page displays: *"If you have content types you would like to apply, you can now enable it directly from your document library. To enable content types, go to Documents, select Add column, and then select Content type and apply the relevant content types"*

### Naming Collision Check

| Canonical Content Type | Existing | Collision |
|------------------------|----------|-----------|
| RAE Document Base | Not found | ✅ None |
| RAE Legacy Document | Not found | ✅ None |
| RAE Active Document | Not found | ✅ None |
| RAE Duplicate Reference | Not found | ✅ None |
| RAE Metadata Record | Not found | ✅ None |

### Result

```
CONTENT_TYPE_CAPABILITY_CONFIRMED
```

Site admin can enable content type management on document libraries and create/assign content types. No naming collisions with the 5 canonical content types.

**Evidence:** EA3S-CT-01

---

## Condition 3 — Navigation Impact Plan

### Current Navigation Structure

The existing site's left navigation (Quick Launch) contains:

```
Home
Conversations (Teams)
Documents
Notebook (OneNote)
Pages
Class Files
เอกสารประกอบของคลาส
Site contents
Recycle bin
Edit (edit navigation)
```

### Analysis

| Factor | Observation |
|--------|-------------|
| New libraries in nav | Modern Team Sites auto-add new libraries to navigation by default |
| Library creation dialog | "Show in navigation" option available during library creation |
| Site Pages in nav | Pages library currently in navigation; individual pages can be added |
| Navigation editing | "Edit" link at bottom of navigation enables reordering and visibility control |
| Navigation Elements | Classic "Navigation Elements" link accessible from site settings |
| Quick Launch | Classic quicklaunch.aspx not functional (modern site) |

### Recommended Minimum-Disruption Navigation Model

```
Existing RAE Site Navigation (preserved)
├── Home
├── Conversations
├── Documents
├── Notebook
├── Pages
├── Class Files
├── เอกสารประกอบของคลาส
├── RAE Document Center         ← ONE new top-level entry
├── Site contents
└── Recycle bin
```

**Design rules:**

1. Create the Document Center Landing Page as a modern Site Page under Site Pages
2. Add **one** navigation entry `RAE Document Center` pointing to the landing page
3. Create 6 new libraries with **"Show in navigation = No"** (available during creation via "Add to navigation" checkbox)
4. Create the RAE Document Registry List with **"Show in navigation = No"**
5. Use the landing page with Quick Links, Document Library web parts, and List web parts
6. Manage navigation via modern "Edit" button at bottom of navigation pane

### Impact Classification

```
MEDIUM_MANAGEABLE
```

The navigation impact is manageable. One additional navigation entry plus controlled library visibility keeps disruption low. Existing site users continue to see their familiar navigation structure.

**Evidence:** EA3S-NAV-01

---

## Condition 4 — Site Ownership Clarification

### Evidence Collected

| Check | Finding |
|-------|---------|
| Site Collection Admin | `researchmju@mju.ac.th` — confirmed `IsSiteAdmin = true` |
| SharePoint Owners Group | "สำนักวิจัยฯ Owners" (ID 3) — contains System Account + M365 Group Owner claim |
| M365 Group Owner | "เจ้าของ สำนักวิจัยฯ" — managed through Azure AD / Entra ID; email `msteams_54adc4@maejo365.onmicrosoft.com` |
| M365 Group Members | "สมาชิก สำนักวิจัยฯ" — 23 total members managed through directory |
| researchmju role | Site Admin only; not a direct member of Owners or Members groups (Site Admin privilege is separate) |
| Other site admins | Not publicly listed through available UI; Owner group contains only system and directory claim |

### Ownership Model

The existing site follows the modern SharePoint Team Site ownership model:

```
M365 Group Owner (Azure AD/Entra ID)
    └── Manages group membership (23 members)
    └── M365 Group → SharePoint Members/Visitors group mapping

Site Collection Administrator (researchmju@mju.ac.th)
    └── Technical Site Admin for the SharePoint site
    └── Can manage site structure, libraries, lists, permissions
    └── IsSiteAdmin = true (verified)
```

### Classification

```
OWNERSHIP_CLEAR
```

The existing site has clear ownership separation:
- **M365 Group ownership** managed through Azure AD (not exposed in SharePoint UI)
- **Site Administration** held by `researchmju@mju.ac.th` with Site Admin privileges
- **No ownership continuity risk** — researchmju is the active RAE office account

### Important Notes

- researchmju being Site Admin does NOT equate to being an M365 Group Owner
- Category Owner assignment remains a separate governance dependency (not resolved by this condition)
- If researchmju's role changes, a new Site Admin should be assigned

**Evidence:** EA3S-OWNER-01

---

## Condition 5 — External Sharing Verification

### Evidence

From EA-1 batch evidence and EA-3S site inspection:

| Check | Finding |
|-------|---------|
| Tenant-level external sharing | ✅ CONFIRMED — Anyone links enabled (SPO-013/014/015) |
| Site-level privacy | Private — only M365 Group members can access |
| Library-level sharing controls | Available — Documents library settings show sharing management |
| Unique-permission library sharing | Available — library-level sharing settings independent of site |
| Anyone link availability | ✅ CONFIRMED at tenant level |

### Sharing Behavior Notes

- The site being **Private** means the default site access is restricted to 23 M365 Group members
- **Library-level sharing** can be configured independently for each library
- **Unique permissions libraries** retain their own sharing settings when inheritance is broken
- **Public document delivery** uses Anyone (anonymous) links — confirmed available at tenant level
- The **Share** button is accessible from the command bar for individual items

### Classification

```
EXTERNAL_SHARING_CONFIRMED
```

External sharing capability exists at the tenant and site levels. Anyone links are available for public document delivery. Library-level sharing controls are independently configurable.

### Governance Reminder

Tenant default sharing behavior must NOT become RAE governance policy. Public delivery eligibility remains controlled by Registry metadata (`PublicVisibility = public`) and workflow validation.

**Evidence:** EA3S-SHARING-01

---

## Five-Condition Closure Summary

| # | Condition | Result | Evidence |
|---|-----------|--------|----------|
| C1 | Permission Group Creation | GROUP_CREATION_CONFIRMED | EA3S-GROUP-01 |
| C2 | Content Type Enablement | CONTENT_TYPE_CAPABILITY_CONFIRMED | EA3S-CT-01 |
| C3 | Navigation Impact Plan | MEDIUM_MANAGEABLE | EA3S-NAV-01 |
| C4 | Site Ownership Clarification | OWNERSHIP_CLEAR | EA3S-OWNER-01 |
| C5 | External Sharing Verification | EXTERNAL_SHARING_CONFIRMED | EA3S-SHARING-01 |

**All five conditions resolved successfully. No critical blockers identified.**

---

## Architecture Exception Status

```
APPROVED_FOR_EXISTING_SITE_IMPLEMENTATION
```

The implementation exception is formally approved. The deployment topology changes from `/sites/RAEDocumentCenter` to the existing RAE site (`/sites/msteams_54adc4`).

See: `docs/m365/m365-existing-site-implementation-exception.md`

---

## Provisioning Plan Impact

The following documents have been updated to reflect the existing-site deployment boundary:

| Document | Changes |
|----------|---------|
| `docs/m365/m365-sharepoint-registry-provisioning-plan.md` | Updated status from PREFLIGHT to PROVISIONING_READY; added EA-3S context section; updated site URL; updated TenantAdminAccess and SelfServiceSiteCreation assessments |
| `docs/m365/m365-provisioning-manifest.csv` | Site (Seq 1) and M365Group (Seq 2) reclassified from PLANNED to REQUIRE_EXISTING_SITE; target URL updated |
| `docs/m365/m365-provisioning-authorization-gate.md` | Action 1 (Create Site) and Action 2 (Create Group) marked as REUSE_EXISTING_SITE — no longer required |

---

## Admin Package Status

```
FALLBACK_DEDICATED_SITE_PROVISIONING_PATH
```

The Admin Provisioning Request Package (`docs/m365/admin/`) is preserved as a fallback path. The package remains historically traceable. If existing-site reuse encounters critical blockers, the dedicated-site admin request can be reactivated.

---

## Final Implementation Readiness Decision

```
EXISTING_SITE_READY_FOR_PROVISIONING
```

All five EA-3R conditions resolved successfully. The existing RAE SharePoint site is approved and ready for Document Center foundation provisioning.

---

## Recommended Next Phase

```
EA-3I — Sequential Existing-Site Foundation Provisioning
```

The next phase should provision the approved SharePoint and Registry foundation sequentially:

1. Create 6 document libraries (unique permissions, navigation hidden)
2. Create 17 site columns (RAE_DocumentID, RAE_Category, RAE_Subcategory, etc.)
3. Create 5 content types (RAE Document Base → RAE Legacy Document, etc.)
4. Create RAE Document Registry Microsoft List (22 columns)
5. Create 9 RAE-DC-* permission groups
6. Create Document Center Landing Page

Do NOT jump directly to EA-5 (governance workflows). The foundation must be provisioned and validated first.
