# SharePoint Site Design — RAE Document Center

**Phase:** M365-3 — SharePoint Foundation  
**Blueprint ref:** `docs/document-center/M365 FoundationBlueprint.MD` §Phase M365-3  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-13  
**Author:** RAE Digital Transformation

---

## 1. Design Principles

From `M365 FoundationBlueprint.MD`:

> **Build Less. Govern More.**  
> Website should not become a document management system.  
> Microsoft 365 should become the document management platform.  
> SharePoint is the Source of Truth.

| Principle | Implication |
|-----------|-------------|
| No files on VPS | All documents live in SharePoint; portal links out |
| No manual registry maintenance | Metadata managed inside M365 columns |
| Website stateless | Portal reads Registry Export JSON (Phase M365-8) |
| Governance enforced by platform | SharePoint groups + column defaults + Power Automate (M365-5) |
| Metadata-only records | Stored in Microsoft Lists Registry (M365-4), **not** as dummy files in libraries |

---

## 2. Site Specification

| Property | Value |
|----------|-------|
| **Site Name** | RAE Document Center |
| **Site Type** | SharePoint Team Site (with hub site capability) |
| **Suggested URL** | `https://[tenant].sharepoint.com/sites/RAE-DocumentCenter` |
| **Language (primary)** | Thai (th-TH) |
| **Time Zone** | (UTC+07:00) Bangkok, Hanoi, Jakarta |
| **Storage quota** | Minimum 100 GB (target ~10 GB legacy import + headroom) |
| **External sharing** | Disabled by default; enable per-document via view-only link for Public documents |
| **Site Collection Admin** | Platform Admin (role from `ONEDRIVE_PERMISSION_POLICY.md`) |

### 2.1 Site Navigation Structure

```
RAE Document Center (hub)
├── 📚 Document Libraries (this phase)
│   ├── Administration
│   ├── FinanceProcurement
│   ├── PlanningPolicy
│   ├── AcademicServices
│   ├── Research
│   └── SOPManuals
├── 📋 Lists (Phase M365-4)
│   └── RAE Document Registry
├── 🔄 Workflows (Phase M365-5)
│   └── Power Automate flows
└── 📊 Reports (Phase M365-9)
    └── Governance dashboard
```

---

## 3. Document Libraries Overview

Six libraries mirror the taxonomy categories from `taxonomy.json`. Library names are English slugs; Thai display names are set via SharePoint column defaults and the taxonomy.

| Library Name | Taxonomy ID | Thai Name | Sort | Legacy Rows | Files | Metadata-Only |
|---|---|---|---|---|---|---|
| `Administration` | `admin` | งานบริหารและธุรการ | 1 | 42 | 9 | 33 |
| `FinanceProcurement` | `finance-procurement` | งานคลังและพัสดุ | 2 | 35 | 20 | 15 |
| `PlanningPolicy` | `policy-planning` | งานนโยบาย แผนและประกันคุณภาพ | 3 | 57 | 10 | 47 |
| `AcademicServices` | `academic-service` | งานบริการวิชาการ | 4 | 47 | 43 | 4 |
| `Research` | `research` | งานวิจัย | 5 | 576 | 530+45dup | 1 |
| `SOPManuals` | `manuals` | คู่มือปฏิบัติงาน | 6 | 15 | 15 | 0 |
| **Total** | | | | **772** | **627** | **100** |

> **Metadata-only note:** 100 records with `MigrationStatus = Metadata Only` have no physical file.  
> These are NOT uploaded as empty/dummy files. They will be registered in **RAE Document Registry** (Microsoft List, Phase M365-4) with `status = MetadataOnly` and `LegacySourceURL` preserved.

---

## 4. Folder Strategy per Library

Folders within each library reflect `Subcategory` values from the migration manifest. This preserves the legacy RAE WTMS sub-navigation structure.

### 4.1 Folder Rules

- **Depth:** Maximum 2 levels (Library → Subcategory folder)
- **Naming:** Use exact Thai subcategory names; no path separators `/` → replace with `\` via SharePoint folder hierarchy
- **No nesting beyond level 2** — keep flat enough for SharePoint view performance
- **Special folders:**  
  - `_Inbox` — staging for new uploads before metadata assignment  
  - `_Review` — orphan/unreadable files pending classification  
  - `_Archive` — obsolete documents; hidden from default view

### 4.2 Library Folder Structure

#### Administration (9 files)
```
Administration/
└── งานบริหารและธุรการ/     (9 files)
    └── _Inbox/             (new uploads)
```

#### FinanceProcurement (20 files)
```
FinanceProcurement/
└── งานคลังและพัสดุ/        (20 files)
    └── _Inbox/
```

#### PlanningPolicy (10 files)
```
PlanningPolicy/
└── งานนโยบาย แผนและประกันคุณภาพ/   (10 files)
    └── _Inbox/
```

#### AcademicServices (43 files)
```
AcademicServices/
├── คู่มือ/                          (8 files)
├── แบบฟอร์มงานบริการวิชาการ/       (13 files)
├── แบบฟอร์มศูนย์ความเป็นเลิศ/      (5 files)
├── แบบฟอร์มแหล่งทุนภายนอก/         (17 files — includes duplicates)
└── _Inbox/
```

#### Research (530 primary + 45 duplicate links)
```
Research/
├── งานวิจัย-การจัดการความรู้/       (1 file)
├── งานวิจัย-ทุนวิจัย/              (4 files)
├── งานวิจัย-ประกาศงานวิจัย/        (1 file)
├── งานวิจัย-ระเบียบการบริหารงานวิจัย/ (1 file)
├── งานวิจัย-รายงานผลงานวิจัย/       (2 files)
├── งานวิจัย/การจัดการความรู้/       (5 files)
├── งานวิจัย/การประเมินผลงานวิจัย/  (6 files)
├── งานวิจัย/คลินิกวิจัย/           (6 files)
├── งานวิจัย/ฐานข้อมูลงานวิจัย/     (4 files)
├── งานวิจัย/ทรัพย์สินทางปัญญา/    (9 files)
├── งานวิจัย/ทุนวิจัย/              (53 files)
├── งานวิจัย/ประกาศงานวิจัย/        (165 files)
├── งานวิจัย/มาตรฐานการวิจัย/       (27 files)
├── งานวิจัย/ระบบสารสนเทศงานวิจัย/ (11 files)
├── งานวิจัย/ระเบียบการบริหารงานวิจัย/ (55 files)
├── งานวิจัย/รายงานผลงานวิจัย/      (76 files)
├── งานวิจัย/วิจัยสถาบัน/           (63 files)
├── งานวิจัย/แบบฟอร์มงานวิจัย/      (93 files — highest volume)
├── งานวิจัย/แผนงานวิจัย/           (2 files)
├── งานวิจัย/จริยธรรมการวิจัย/      (1 file)
└── _Inbox/
```

#### SOPManuals (15 files)
```
SOPManuals/
└── งานวิจัย-คู่มือการวิจัย/        (15 files)
    └── _Inbox/
```

### 4.3 Duplicate Handling in Folders

- Duplicate links (45 rows, `MigrationStatus = Duplicate (linked)`) are **not uploaded as separate files**
- The primary file exists in its source folder
- Duplicate records are registered in the Microsoft List (Phase M365-4) with `DuplicateOf` pointing to primary `DocumentID`
- SharePoint search returns the primary file; the List tracks all legacy URL aliases

---

## 5. Versioning Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Versioning enabled | Yes | Track all changes post-migration |
| Version type | Major and minor | Minor for metadata edits, major for content |
| Major version limit | Keep all | Compliance requirement |
| Minor (draft) version limit | 10 | Avoid storage bloat |
| Require check out | No | Not required for operational workflow |
| Draft item security | Only authors and approvers | Prevent accidental publishing |

---

## 6. Retention Policy (Guidance — configure via Purview)

| Library | Retention Period | Review Trigger | Action on Expiry |
|---------|-----------------|----------------|-----------------|
| Administration | 7 years | Document date | Move to `_Archive` folder |
| FinanceProcurement | 10 years | Document date | Move to `_Archive` → notify owner |
| PlanningPolicy | 7 years | Document date | Review before archive |
| AcademicServices | 5 years | Document date | Move to `_Archive` |
| Research | 10 years | Document date | Notify Research owner |
| SOPManuals | Until superseded + 3 years | Version review (every 2 years) | Mark obsolete; archive |

> Retention labels configured via Microsoft Purview Compliance Center, not this document. Labels correspond to `DocumentStatus` values: `Current`, `Obsolete`, `Archived`.

---

## 7. Search and Discovery

- **Site search scope:** All 6 libraries included by default
- **Refiners:** TargetLibrary, Category, Subcategory, PublicVisibility, DocumentStatus, MigrationStatus
- **Search schema:** `DocumentID`, `LegacySourceURL`, `SHA256` promoted as managed properties
- **External search:** Disabled by default; only `PublicVisibility = Public` documents may be exposed via Graph API (Phase M365-8)

---

## 8. SharePoint → Portal Integration (Preview)

```
SharePoint Libraries → Microsoft Lists Registry → Registry Export JSON → RAE Portal
```

- Phase M365-8 will consume a scheduled JSON export from Microsoft Lists
- Portal is **read-only** and **stateless** — no files served from portal server
- Public documents surfaced via `storage_url` (view-only SharePoint link)
- Documents with `PublicVisibility = Internal` or `Restricted` are excluded from export

---

## 9. Pre-Implementation Checklist

Before site creation in Microsoft 365:

- [ ] Confirm SharePoint Online license availability (Phase M365-1)
- [ ] Confirm tenant URL and naming convention with IT admin
- [ ] Register M365 groups for each library's owner group (from `taxonomy.json`)
- [ ] Confirm retention labels in Microsoft Purview
- [ ] Sign off by Category Owners on folder structure
- [ ] Confirm external sharing policy with IT Security

---

## Related Documents

| Document | Path |
|----------|------|
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
| Taxonomy | `docs/document-center/taxonomy.json` |
| Library Schema | `docs/m365/library-schema.md` |
| Content Types | `docs/m365/content-types.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Migration Field Map | `docs/m365/migration-field-map.csv` |
| Migration Manifest | `migration/sharepoint-migration-manifest.csv` |
| OneDrive Permission Policy | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` |
