# Architecture Baseline v1.0

**Version**: 1.0.0  
**Effective**: 2026-07-16  
**Status**: FROZEN — all future modifications must reference this baseline

---

## 1. Architecture

```text
Source corpus (WTMS staging — frozen)
        ↓
SharePoint document libraries (file storage — authoritative)
        ↓
RAE Document Registry (metadata — discovery layer)
        ↓
SharePoint Document Center page (operational portal)
```

The website/portal does **not** store master files. SharePoint libraries are the file source of truth.

---

## 2. Site Boundary

| Property | Value |
|----------|-------|
| Tenant | `maejo365.sharepoint.com` |
| Site | `/sites/msteams_54adc4` |
| Type | Private Team Site (M365 Group) |
| Production page | `SitePages/RAE-Document-Center.aspx` |

---

## 3. Approved Libraries

| Library | Registry category slug |
|---------|------------------------|
| Administration | `admin` |
| FinanceProcurement | `finance-procurement` |
| PlanningPolicy | `policy-planning` |
| AcademicServices | `academic-service` |
| Research | `research` |
| SOPManuals | `manuals` |

No additional libraries without architecture review.

---

## 4. Registry

| Property | Value |
|----------|-------|
| List name | RAE Document Registry |
| Idempotency key | DocumentID |
| Upsert mode | AUTO_UPSERT (EA-8) |
| Sync tool | `_ea8_registry_sync.py --sync-all` |
| Target count | 627 unique DocumentIDs |

**Critical Registry fields**: DocumentID, Title, Category, Storage URL, Status, Visibility, Source System

---

## 5. Metadata Model (SharePoint library items)

| Field | Source |
|-------|--------|
| DocumentID | Manifest (immutable) |
| Title | Manifest |
| Category1 | Manifest subcategory/category |
| Owner | `TBD` (placeholder) |
| DocumentStatus | `LegacyImported` |
| PublicVisibility | `PendingReview` |
| LegacySourceURL | WTMS source URL |

---

## 6. Status Model

| Layer | Status values (v1.0) |
|-------|---------------------|
| Manifest | `Ready` (migrated corpus) |
| SharePoint file | Uploaded + metadata applied |
| Registry | `draft` |
| Migration result | `UploadStatus=OK`, `RegistryStatus=AUTO_UPSERT` |

---

## 7. Visibility Model

| Layer | v1.0 value |
|-------|------------|
| SharePoint PublicVisibility | `PendingReview` |
| Registry Visibility | `internal` |
| GitHub Pages preview | `public` (demo records only) |
| Tenant anonymous access | Not enabled |

---

## 8. Portal Topology

| Portal | URL | Role |
|--------|-----|------|
| **Production** | SharePoint Document Center page | Operational user portal |
| **Registry direct** | Registry AllItems.aspx | Metadata admin view |
| **Preview** | `numtip.github.io/document-center/` | UI demo (3 records) |
| **Planned** | `rae-nextjs-main` | Future public portal via export JSON |

---

## 9. Document Flow

1. Document selected from canonical manifest (`MigrationStatus=Ready`)
2. Preflight: SHA-256, source file, library assignment
3. Upload via `playwright-rest` to target library (`{DocumentID}{ext}`)
4. Metadata applied via ValidateUpdateListItem
5. Registry AUTO_UPSERT by DocumentID
6. Result persisted to phase results CSV

**Forbidden**: `--force` re-upload, recrawl WTMS, architecture redesign, governance activation without change control.

---

## 10. Change Control

Any modification to libraries, Registry schema, portal topology, or migration method requires:

1. Reference to this baseline document
2. Explicit architecture approval
3. Updated acceptance certificate
