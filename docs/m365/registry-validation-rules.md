# RAE Document Registry — Validation Rules

**Phase:** M365-4 — Microsoft Lists Registry Design  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-14  
**Applies to:** `RAE Document Registry` Microsoft List

---

## 1. Validation Architecture

Validation operates at three levels:

```
Level 1: Column Validation — enforced by Microsoft Lists column settings
Level 2: Record Validation — cross-field rules within a single row
Level 3: Release Validation — exported JSON validation before portal deployment
```

| Level | Enforcer | When | Tool |
|-------|----------|------|------|
| Column | Microsoft Lists | On create/edit | Column formulas, required settings, unique constraints |
| Record | Microsoft Lists + manual review | On save | Column validation formula + human review |
| Release | Export script (Phase M365-7) | On export | JSON schema validator + integrity check |

---

## 2. Level 1 — Column Validation

Rules enforceable natively in Microsoft Lists:

| # | Rule | Column | Constraint | Native Lists? |
|---|------|--------|------------|:-------------:|
| V1 | DocumentID non-empty | DocumentID | `=NOT(ISBLANK([DocumentID]))` | ✅ Formula |
| V2 | DocumentID unique | DocumentID | Unique column constraint | ✅ Built-in |
| V3 | DocumentID format | DocumentID | Pattern: `RAE-\d{5}` | ❌ Power Automate |
| V4 | Title non-empty | Title | `=NOT(ISBLANK([Title]))` | ✅ Formula |
| V5 | Title max length | Title | Max 255 chars | ✅ Built-in |
| V6 | Category non-empty | Category | Required choice column | ✅ Built-in |
| V7 | Category allowed value | Category | Choice column restriction | ✅ Built-in |
| V8 | Owner non-empty | Owner | Person/Group required | ✅ Built-in |
| V9 | Status non-empty | Status | Required choice column | ✅ Built-in |
| V10 | Status allowed value | Status | Must be: draft, review, approved, published, current, obsolete, archived | ✅ Built-in |
| V11 | Visibility non-empty | Visibility | Required choice column | ✅ Built-in |
| V12 | Visibility allowed value | Visibility | Must be: public, internal, restricted, private | ✅ Built-in |
| V13 | UpdatedDate non-empty | UpdatedDate | Required date column | ✅ Built-in |
| V14 | UpdatedDate not future | UpdatedDate | `=[UpdatedDate]<=TODAY()` | ✅ Formula |
| V15 | SourceSystem non-empty | SourceSystem | Required choice column | ✅ Built-in |
| V16 | Version format | Version | Pattern: `\d+\.\d+` | ❌ Power Automate |
| V17 | Notes max length | Notes | Max 1000 chars | ✅ Built-in |
| V18 | Tags max length | Tags | Max 500 chars | ✅ Built-in |
| V19 | RecordVersion ≥ 1 | RecordVersion | Number min=1 | ✅ Built-in |

---

## 3. Level 2 — Record Validation

Cross-field rules requiring business logic:

| # | Rule | Condition | Invalid State | Native Lists? | Fallback |
|---|------|-----------|---------------|:-------------:|----------|
| R1 | StorageURL required for active documents | Status = current OR published OR approved | StorageURL is empty | ❌ | Manual review via "Missing Metadata" view |
| R2 | StorageURL required for public visibility | Visibility = public AND StorageURL is empty | StorageURL is empty | ❌ | Manual review via "Public Documents" view |
| R3 | StorageURL must be HTTPS | StorageURL is not empty | URL starts with HTTP:// | ❌ | Manual review |
| R4 | Public document with complete required fields | Visibility = public | Missing Description or empty Title | ❌ | Manual review via "Public Documents" view |
| R5 | Public document must not use restricted/private | Visibility = public | restricted or private selected | ✅ Built-in (choice restriction) | N/A — choice column enforces |
| R6 | DuplicateOf references valid DocumentID | DuplicateOf is not empty | Referenced DocumentID does not exist | ❌ | Power Automate (Phase M365-5) |
| R7 | ReviewDate not future for completed reviews | ReviewDate is populated AND ReviewDate > Today | Future date with no note | ❌ | Manual review via "Expiring Review" view |
| R8 | Category matches enabled taxonomy | Category value | Category not enabled in taxonomy.json | ✅ Choice column | N/A |
| R9 | Unsupported Status | Status value | Status not in approved vocabulary | ✅ Choice column | N/A |
| R10 | Unsupported Visibility | Visibility value | Visibility not in approved vocabulary | ✅ Choice column | N/A |
| R11 | SourceSystem required for migration records | SourceSystem = WTMS Migration | Missing LegacySourceURL or DuplicateOf not set | ❌ | Manual review |

---

## 4. Level 3 — Release Validation

Validation performed during registry export (Phase M365-7):

| # | Rule | Description | Blocking? |
|---|------|-------------|:---------:|
| X1 | No duplicate DocumentIDs | Export JSON must have unique IDs | ✅ **Blocking** |
| X2 | No missing DocumentID | Every record must have DocumentID | ✅ **Blocking** |
| X3 | No missing Owner | Owner must be non-empty on every exported record | ✅ **Blocking** |
| X4 | No missing Status | Status must be non-empty | ✅ **Blocking** |
| X5 | No missing Visibility | Visibility must be non-empty | ✅ **Blocking** |
| X6 | No missing StorageURL for active public docs | Conditional requirement (R1, R2) | ✅ **Blocking** |
| X7 | All public StorageURLs resolve | HTTP check against every exported StorageURL | ✅ **Blocking** |
| X8 | Public records exclude internal governance fields | LegacySourceURL, Notes, ReviewDate must not be in public export | ✅ **Blocking** |
| X9 | Public records have valid Status for export | Only Current, Published, Approved are exported | ✅ **Blocking** |
| X10 | Public records have Visibility = Public | Only Public records are exported | ✅ **Blocking** |
| X11 | Internal-only governance notes excluded | Notes field must be excluded from public export | ✅ **Blocking** |
| X12 | Personal information minimized | Owner email only; no personal identifiers beyond display name | ✅ **Blocking** |
| X13 | Draft/review records excluded | Records with draft or review status must not appear in export | ✅ **Blocking** |

---

## 5. Mandatory Invalid Conditions

The following conditions render a record invalid and must be resolved before the record can be considered for public export:

| Condition | Rule Reference | Severity |
|-----------|---------------|:--------:|
| Missing DocumentID | V1, X2 | **BLOCKING** |
| Duplicate DocumentID | V2, X1 | **BLOCKING** |
| Missing Owner | V8, X3 | **BLOCKING** |
| Missing Status | V9, X4 | **BLOCKING** |
| Missing Visibility | V11, X5 | **BLOCKING** |
| Missing StorageURL (active documents) | R1, X6 | **BLOCKING** |
| Public document with incomplete required metadata | R4, X9 | **BLOCKING** |
| Unsupported Category | R8 | **BLOCKING** |
| Unsupported Status | R9 | **BLOCKING** |
| Unsupported Visibility | R10 | **BLOCKING** |
| Broken public StorageURL | X7 | **BLOCKING** |
| Draft/review records in export | X13 | **BLOCKING** |

---

## 6. Validation Enforcement Responsibility

| Level | Native Lists | Manual (by Owner) | Power Automate (Phase M365-5) | Export Script (Phase M365-7) |
|-------|:------------:|:-----------------:|:----------------------------:|:---------------------------:|
| Level 1 — Column | 17 of 19 rules | — | 2 rules (V3, V16) | — |
| Level 2 — Record | 4 of 11 rules | 4 rules | 3 rules | — |
| Level 3 — Release | — | — | — | All 13 rules |

> **Current implementation constraint:** In EA-4 (pre-Power Automate), approximately 50% of validation rules require manual review. This is acceptable for the design phase. Automated enforcement is added in Phase M365-5.

---

## 7. Validation Formula Examples (Microsoft Lists)

### Unique DocumentID (Lists supports native unique constraint — no formula needed)

### UpdatedDate not future:
```excel
=[UpdatedDate]<=TODAY()
```

### Title non-empty:
```excel
=NOT(ISBLANK([Title]))
```

### Owner non-empty:
Enforced via "Require that this column contains information" setting on Person/Group column.

---

## Related Documents

| Document | Path |
|----------|------|
| Registry Schema | `docs/m365/registry-list-schema.md` |
| Views | `docs/m365/registry-views.md` |
| Lifecycle Model | `docs/m365/registry-lifecycle-model.md` |
| Owner Rules | `docs/m365/registry-owner-rules.md` |
| Export Contract | `docs/m365/registry-export-contract.md` |
| Registry Data Model (Phase 3.7) | `docs/document-center/REGISTRY_DATA_MODEL.md` |
