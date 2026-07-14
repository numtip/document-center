# Permissions Matrix — RAE Document Center

**Phase:** M365-3 — SharePoint Foundation  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-13  
**Predecessor:** `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` (adapted to SharePoint Online)

---

## 1. Design Principles

Carried forward from `ONEDRIVE_PERMISSION_POLICY.md`:

1. **Least privilege** — Grant minimum access for each role
2. **Owner accountability** — Every library has a Category Owner
3. **Separation of duties** — Content owners manage documents; Platform Admin manages site structure
4. **No anonymous write access** — Upload requires authenticated M365 account
5. **Links are intentional** — `storage_url` (view-only) created deliberately per registry entry

Additional SharePoint principles:

6. **No permission inheritance breaks** at item level (only at library level)
7. **`PublicVisibility = PendingReview`** — no anonymous link until promoted to `Public`
8. **Migration phase exception** — Upload bot account has `Contribute` across all libraries during initial import; revoked after migration completes

---

## 2. Role Definitions

| Role | Description | M365 Equivalent |
|------|-------------|-----------------|
| **Platform Admin** | Site collection admin; manages structure, groups, governance | Site Collection Administrator |
| **Category Owner** | Owns 1–2 libraries; approves uploads, manages metadata, reviews visibility | SharePoint Group: `RAE-DC-{Library}-Owners` |
| **Document Owner** | Responsible for a specific document (`Owner` field) | Individual user; no special group |
| **Contributor** | Upload to `_Inbox` folder; cannot move or delete | SharePoint Group: `RAE-DC-Contributors` |
| **Reader** | View and download documents | SharePoint Group: `RAE-DC-Readers` |
| **Archive Manager** | Manages `_Archive` folder moves and obsolete records | SharePoint Group: `RAE-DC-ArchiveManagers` |
| **Migration Bot** | Service account for automated bulk import | SharePoint Group: `RAE-DC-MigrationBot` (temporary) |
| **Anonymous (External)** | No-account access via view-only share link | SharePoint anonymous link (per document only) |

---

## 3. SharePoint Permission Levels

| Permission Level | SharePoint Level | Capabilities |
|-----------------|-----------------|--------------|
| `Full Control` | Full Control | All operations including site settings |
| `Edit` | Edit | Add, edit, delete items and documents |
| `Contribute` | Contribute | Add and edit items; cannot delete |
| `Read` | Read | View and download only |
| `View Only` | View Only | View in browser only; no download for some types |
| `No Access` | (not granted) | Cannot see or open |

---

## 4. Site-Level Permissions

| Group / Principal | Permission Level | Notes |
|---|---|---|
| Platform Admin | Full Control | Site Collection Administrator |
| `RAE-DC-{Library}-Owners` (all 6) | Full Control on own library | Category owner scope (see §5) |
| `RAE-DC-Contributors` | Contribute on `_Inbox` folders only | Cannot access main library folders directly |
| `RAE-DC-Readers` | Read | All libraries read access |
| `RAE-DC-ArchiveManagers` | Edit on `_Archive` folders | Cannot touch live documents |
| `RAE-DC-MigrationBot` | Contribute on all libraries | **Temporary** — revoke after migration |
| All authenticated org users | Read (default) | Via org-wide site permissions |
| External / anonymous | No Access (default) | Granted only per-document via share link |

---

## 5. Library-Level Permissions

Each library has its own Category Owner group with scoped access:

| Library | Category Owner Group | Thai Name | Suggested Owner Role |
|---------|---------------------|-----------|---------------------|
| Administration | `RAE-DC-Admin-Owners` | งานบริหารและธุรการ | Administration unit lead |
| FinanceProcurement | `RAE-DC-Finance-Owners` | งานคลังและพัสดุ | Inventory & supplies lead |
| PlanningPolicy | `RAE-DC-Policy-Owners` | งานนโยบายและแผน | Policy & planning lead |
| AcademicServices | `RAE-DC-Academic-Owners` | งานบริการวิชาการ | Academic services lead |
| Research | `RAE-DC-Research-Owners` | งานวิจัย | Research unit lead |
| SOPManuals | `RAE-DC-Manuals-Owners` | คู่มือปฏิบัติงาน | Operations / training lead |

> Individual named owners are **TBD** — to be confirmed before go-live. See `docs/document-center/OWNER_CONFIRMATION_CHECKLIST.csv`.

### 5.1 Library Permission Matrix

| Action | Platform Admin | Category Owner (own lib) | Contributor | Reader | Archive Mgr | Migration Bot |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| View all documents | ✅ | ✅ | ✅ (Inbox only) | ✅ | ✅ | ✅ |
| Upload to `_Inbox` | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Upload to subcategory folder | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Edit metadata on any doc | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Edit own document metadata | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Change `DocumentStatus` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Change `PublicVisibility` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Move to `_Archive` | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Delete document | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create share link | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Manage library settings | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create/delete folders | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 6. Folder-Level Permissions

Within each library, folder permissions narrow what each role can access:

| Folder | Platform Admin | Category Owner | Contributor | Reader | Archive Mgr | Migration Bot |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| Root (library level) | Full Control | Edit | Read | Read | Read | Contribute |
| `{subcategory}/` | Full Control | Edit | Read | Read | Read | Contribute |
| `_Inbox/` | Full Control | Edit | Contribute | No Access | No Access | Contribute |
| `_Review/` | Full Control | Edit | No Access | No Access | Edit | Contribute |
| `_Archive/` | Full Control | Read | No Access | No Access | Edit | No Access |

---

## 7. Document-Level Access Control

For individual documents:

| `PublicVisibility` | Authenticated org users | External (anonymous) | Action Required |
|---|---|---|---|
| `PendingReview` | Read (library permission) | No Access | No action until reviewed |
| `Internal` | Read (org-wide) | No Access | Category Owner creates org-scoped link |
| `Public` | Read | Read via share link | Category Owner creates anonymous view-only link; add to `LegacySourceURL` or `storage_url` |
| `Restricted` | No Access (default) | No Access | Platform Admin grants explicit permission |

### 7.1 Share Link Policy (from `ONEDRIVE_PERMISSION_POLICY.md`)

| Setting | Requirement |
|---------|-------------|
| Link type | **View only** (no edit) |
| Scope | "People in organization" for `Internal`; "Anyone with link" only for `Public` |
| Expiration | No expiration for stable `Current` documents; annual review |
| Regeneration | Update `LegacySourceURL` in SharePoint column if link is regenerated |
| `PendingReview` | **No share links created** until visibility confirmed |

---

## 8. Migration Phase Permissions

Temporary during initial bulk import:

| Period | Action |
|--------|--------|
| **Pre-migration** | Create `RAE-DC-MigrationBot` service account; add to all library Contribute groups |
| **During migration** | MigrationBot uploads 627 files + sets metadata; no delete permission |
| **Post-migration** | Remove `RAE-DC-MigrationBot` from all library groups; disable service account |
| **Timeline** | Revoke within 7 days of migration completion |

---

## 9. Microsoft Lists Permissions (Phase M365-4)

For the `RAE Document Registry` list (100 metadata-only records + full registry):

| Role | Permission |
|------|-----------|
| Platform Admin | Full Control |
| Category Owners | Edit (own category rows) |
| Contributors | No Access (list is managed only) |
| Readers | Read |
| External | No Access |

---

## 10. Audit and Governance

| Audit Item | Frequency | Owner |
|---|---|---|
| Category owner group membership review | Quarterly | Platform Admin |
| Overly broad share links audit | Quarterly | Platform Admin |
| `PendingReview` documents pending visibility decision | Monthly | Category Owners |
| `_Inbox` folder clearance check | Monthly | Category Owners |
| Migration Bot account status | Once (post-migration) | Platform Admin |
| `Owner = TBD` resolution progress | Monthly | Platform Admin → Category Owners |

> Audit process mirrors `ONEDRIVE_PERMISSION_POLICY.md §Audit Checklist` adapted for SharePoint Online.

---

## 11. Group and Account Setup Checklist

Before site creation:

- [ ] Create M365 group `RAE-DC-Admin-Owners`; add Administration unit lead
- [ ] Create M365 group `RAE-DC-Finance-Owners`; add Finance unit lead
- [ ] Create M365 group `RAE-DC-Policy-Owners`; add Policy unit lead
- [ ] Create M365 group `RAE-DC-Academic-Owners`; add Academic Services lead
- [ ] Create M365 group `RAE-DC-Research-Owners`; add Research unit lead
- [ ] Create M365 group `RAE-DC-Manuals-Owners`; add Operations lead
- [ ] Create M365 group `RAE-DC-Contributors` (upload staff)
- [ ] Create M365 group `RAE-DC-Readers` (all RAE staff)
- [ ] Create M365 group `RAE-DC-ArchiveManagers`
- [ ] Create `RAE-DC-MigrationBot` service account (temporary)
- [ ] Confirm named individuals with HR/Admin for each owner role
- [ ] Document assignments in `OWNER_CONFIRMATION_CHECKLIST.csv`

---

## Related Documents

| Document | Path |
|----------|------|
| OneDrive Permission Policy (predecessor) | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` |
| Site Design | `docs/m365/sharepoint-site-design.md` |
| Library Schema | `docs/m365/library-schema.md` |
| Content Types | `docs/m365/content-types.md` |
| Owner Confirmation Checklist | `docs/document-center/OWNER_CONFIRMATION_CHECKLIST.csv` |
