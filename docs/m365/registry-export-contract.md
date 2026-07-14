# RAE Document Registry — Export Readiness Contract

**Phase:** M365-4 — Microsoft Lists Registry Design  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-14  
**Purpose:** Define the contract between the Microsoft Lists Registry (EA-4) and the Scheduled Registry Export JSON (EA-7)

---

## 1. Export Architecture Context

```
Microsoft Lists Registry (RAE Document Registry)
    │
    ▼
Scheduled Registry Export JSON  ←── Phase M365-7 (Migration Pilot)
    │
    ▼
GitHub static data repository
    │
    ▼
Next.js Document Center (public portal)
```

This document defines the **contract** — the "what" — not the implementation. The export mechanism (Power Automate, Graph API, or other) is designed in Phase M365-7.

---

## 2. Export Contract Scope

| Scope | Included |
|-------|:--------:|
| Registry fields to JSON mapping | ✅ |
| Export eligibility criteria | ✅ |
| Transformation rules | ✅ |
| Null/empty behavior | ✅ |
| Privacy rules | ✅ |
| Validation dependencies | ✅ |
| Export format | ✅ |
| Export mechanism | ❌ Phase M365-7 |
| Scheduling | ❌ Phase M365-7 |
| Authentication | ❌ Phase M365-7 |
| Error handling | ❌ Phase M365-7 (specified in validation rules) |

---

## 3. JSON Schema

### 3.1 Root Document

```json
{
  "version": "1.0.0",
  "exported": "YYYY-MM-DDTHH:mm:ssZ",
  "source": "RAE Document Registry (Microsoft Lists)",
  "source_url": "https://[tenant].sharepoint.com/sites/RAE-DocumentCenter/Lists/RAEDocumentRegistry",
  "registry_version": 1,
  "documents": [
    { /* DocumentObject */ }
  ]
}
```

### 3.2 Document Object Schema

```json
{
  "document_id": "RAE-NNNNN",
  "title": "string",
  "description": "string | null",
  "category": "string",
  "subcategory": "string | null",
  "tags": ["string"] | [],
  "audience": ["string"] | [],
  "owner": "string",
  "department": "string | null",
  "status": "string",
  "visibility": "string",
  "updated_date": "YYYY-MM-DD",
  "published_date": "YYYY-MM-DD | null",
  "version": "string | null",
  "storage_url": "string | null",
  "related_documents": ["RAE-NNNNN"] | []
}
```

---

## 4. Export Field Mapping

### 4.1 Fields Exported to Public JSON

| Registry Field | Public JSON Field | Transformation | Null Behavior | Privacy Rule |
|----------------|------------------|----------------|:-------------:|:------------:|
| DocumentID | `document_id` | As-is | Blocking — record must have ID | None |
| Title | `title` | As-is | Blocking — record must have title | None |
| Description | `description` | As-is | Omit key if null; output `null` | Must not contain personal information |
| Category | `category` | As-is (taxonomy slug) | Blocking — record must have category | None |
| Subcategory | `subcategory` | As-is | Omit key if null; output `null` | None |
| Tags | `tags` | Split semicolons → array. Lowercase items. | Empty array `[]` if null | None |
| Audience | `audience` | As-is (array from multi-select) | Empty array `[]` if null | None |
| Owner | `owner` | Display name only; NOT internal email if group | Omit key if null | **Never expose personal email as primary identifier. Use M365 display name.** |
| Department | `department` | As-is | Omit key if null; output `null` | None |
| Status | `status` | As-is | Blocking — must be Current/Published/Approved for export | Must be in export-eligible set |
| Visibility | `visibility` | As-is | Blocking — must be Public for export | **Only Public records are exported** |
| UpdatedDate | `updated_date` | Format `YYYY-MM-DD` | Blocking — record must have date | None |
| PublishedDate | `published_date` | Format `YYYY-MM-DD` | Omit key if null; output `null` | None |
| Version | `version` | As-is | Omit key if null; output `null` | None |
| StorageURL | `storage_url` | As-is | Omit key if null; output `null` | None — URL is a SharePoint view-only link |
| RelatedDocuments | `related_documents` | Split comma-separated → array | Empty array `[]` if null | None — only DocumentIDs exposed |

### 4.2 Fields NOT Exported (Registry-Only)

| Registry Field | Reason |
|----------------|--------|
| Notes | Internal governance notes; not for public |
| ReviewDate | Governance metadata — internal only |
| LegacySourceURL | Dead/internal URL — no public value |
| DuplicateOf | Migration traceability — not publicly relevant |
| SourceSystem | Internal governance — distinguishes migration origin |
| RecordVersion | Internal change tracking — deferred |

### 4.3 Fields Exported Conditionally

| Registry Field | Export Condition | Public Field |
|----------------|-----------------|:------------:|
| StorageURL | Required when Status is Current/Published/Approved AND Visibility is Public | `storage_url` |
| PublishedDate | Only when Status is Published | `published_date` |
| Audience | Only when populated | `audience` |

---

## 5. Export Eligibility

### 5.1 Record-Level Eligibility

A record is eligible for public export ONLY when ALL conditions are met:

| Condition | Requirement |
|-----------|-------------|
| Status | `approved` OR `published` OR `current` |
| Visibility | `public` |
| DocumentID | Non-empty; valid format `RAE-NNNNN` |
| Title | Non-empty |
| Owner | Non-empty; valid M365 user or group |
| Category | Non-empty; matches enabled taxonomy category |
| UpdatedDate | Non-empty; valid date |
| StorageURL | Non-empty AND HTTPS AND reachable |

### 5.2 Mandatory Exclusion

Records in ANY of the following states are NEVER exported:

| State | Reason |
|-------|--------|
| Status = `draft` | Work in progress |
| Status = `review` | Under review |
| Status = `obsolete` | Superseded |
| Status = `archived` | Historical |
| Visibility = `internal` | Org-only scope |
| Visibility = `restricted` | Exception access |
| Visibility = `private` | Owner group only |
| Owner empty/null | Governance invalid |
| StorageURL empty (active records) | Broken reference |
| StorageURL HTTP (not HTTPS) | Security risk |

### 5.3 Export Set = Public + Eligible

The public export set is defined as:

```
ExportSet = Registry.Records WHERE
    Status IN (approved, published, current)
    AND Visibility = public
    AND DocumentID IS NOT NULL
    AND Title IS NOT NULL
    AND Owner IS NOT NULL
    AND StorageURL IS NOT NULL
    AND Category IS NOT NULL
```

---

## 6. Transformation Rules

| Rule ID | Field | Transformation | Example |
|---------|-------|---------------|---------|
| T1 | Tags | Split semicolons → lowercase string array | `"manual;operations"` → `["manual", "operations"]` |
| T2 | RelatedDocuments | Split commas → DocumentID string array | `"RAE-00001,RAE-00002"` → `["RAE-00001", "RAE-00002"]` |
| T3 | Owner | Resolve Person/Group → display name | `"John Doe"` (M365 display name) |
| T4 | UpdatedDate | Format as ISO 8601 date | `2026-07-14` |
| T5 | PublishedDate | Format as ISO 8601 date or null | `2026-07-14` or omitted |
| T6 | Null fields | Omit key from JSON object | If `published_date` is null, omit key |
| T7 | Empty arrays | Include as `[]` | `"tags": []` |
| T8 | StorageURL | Validate HTTPS scheme | If HTTP → flag as error, do not export |

---

## 7. Privacy Rules

| Rule ID | Rule | Enforced At |
|---------|------|:-----------:|
| P1 | Never export records with Visibility != Public | Export validation (Phase M365-7) |
| P2 | Never export Notes field | Registry schema — Notes is registry-only |
| P3 | Never export ReviewDate field | Registry schema — ReviewDate is registry-only |
| P4 | Never export LegacySourceURL | Export mapping — excluded from JSON schema |
| P5 | Never export DuplicateOf | Export mapping — excluded from JSON schema |
| P6 | Never export SourceSystem | Export mapping — excluded from JSON schema |
| P7 | Never export RecordVersion | Export mapping — excluded from JSON schema (deferred) |
| P8 | Owner: display name only, not raw email | Export transformation (T3) |
| P9 | Status must be approved/published/current | Export eligibility (E1) |
| P10 | Draft/review records never exported | Export eligibility (E2) |

---

## 8. Validation Dependencies

The export contract depends on the following validation rules from `registry-validation-rules.md`:

| Export Rule | Depends On Validation Rule |
|-------------|---------------------------|
| DocumentID non-empty | V1 |
| DocumentID unique | V2, X1 |
| Title non-empty | V4 |
| Owner non-empty | V8 |
| Status valid and eligible | V9, V10, X4 |
| Visibility valid and Public | V11, V12, X5 |
| UpdatedDate valid | V13, V14 |
| StorageURL non-empty (active) | R1, R2 |
| StorageURL HTTPS | R3 |
| StorageURL reachable | X7 |
| No broken links in export | X7 (release blocker) |

---

## 9. Export Format Specification

| Property | Value |
|----------|-------|
| **Format** | JSON (RFC 8259) |
| **Encoding** | UTF-8 without BOM |
| **File name** | `public-registry.json` |
| **Root** | Object with `version`, `exported`, `source`, `source_url`, `registry_version`, `documents` array |
| **Array ordering** | By `updated_date` DESC, then `document_id` ASC |
| **Null handling** | Omit key for null values (sparse JSON) |
| **Empty array handling** | Include empty arrays explicitly (`"tags": []`) |
| **Date format** | ISO 8601 date only: `YYYY-MM-DD` |
| **Boolean** | No boolean fields in v1 contract |

---

## 10. Contract Versioning

| Registry Version | Contract Version | Changes |
|-----------------|-----------------|---------|
| 1 | 1.0.0 | Initial EA-4 contract |

The `registry_version` field in the JSON root allows the Next.js portal to detect contract changes and validate schema compatibility.

---

## Related Documents

| Document | Path |
|----------|------|
| Registry Schema | `docs/m365/registry-list-schema.md` |
| Validation Rules | `docs/m365/registry-validation-rules.md` |
| Lifecycle Model | `docs/m365/registry-lifecycle-model.md` |
| Views | `docs/m365/registry-views.md` |
| UI Blueprint (Phase 4A) | `docs/document-center/UI_BLUEPRINT.md` |
| Registry Data Model (Phase 3.7) | `docs/document-center/REGISTRY_DATA_MODEL.md` |
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
