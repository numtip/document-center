# RAE Document Registry — Lifecycle Model (Status & Visibility)

**Phase:** M365-4 — Microsoft Lists Registry Design  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-14  
**Applies to:** `RAE Document Registry` Microsoft List — Status and Visibility columns

---

## 1. Semantic Boundaries

The following fields have distinct and non-overlapping purposes:

| Field | Domain | Purpose |
|-------|--------|---------|
| **Status** | Document lifecycle state | Where the document is in its lifecycle (draft → review → approved → published/current → obsolete/archived) |
| **Visibility** | Information exposure classification | Who should be able to access the document (public, internal, restricted, private) |
| **MigrationStatus** | Migration processing condition | SharePoint-only field tracking import state (Ready, Duplicate (linked), Metadata Only, Pending Review) |
| **SourceSystem** | Source provenance | Originating system: `WTMS Migration`, `Manual Entry`, `Power Automate`, `Bulk Import`, `Direct Upload` |

**Core rule:** Migration conditions (`LegacyImported`, `MetadataOnly`) are NOT lifecycle statuses. They are represented through `SourceSystem = WTMS Migration` and the SharePoint `MigrationStatus` field. The registry Status column only uses the approved seven-value enterprise vocabulary.

---

## 2. Canonical Status Vocabulary

### 2.1 Approved Values (7 values)

| Status | Meaning | Registry Export | EA-3 DocumentStatus Mapping |
|--------|---------|:---------------:|-----------------------------|
| `draft` | Work in progress; not finalized | **Excluded** | DIRECT — same value |
| `review` | Under review by Category Owner | **Excluded** | **Registry addition** — no EA-3 equivalent |
| `approved` | Approved by Category Owner; ready for publication | **Excluded** | **Registry addition** — no EA-3 equivalent |
| `published` | Published and publicly accessible | **Included** | **Registry addition** — no EA-3 equivalent |
| `current` | Active, reviewed, in effect | **Included** | DIRECT — `Current` |
| `obsolete` | Superseded; retained for reference | **Excluded** | DIRECT — `Obsolete` |
| `archived` | Moved to `_Archive`; historical reference only | **Excluded** | DIRECT — `Archived` |

### 2.2 Values NOT in Status Vocabulary

The following values from earlier phases are NOT canonical lifecycle Status values:

| Legacy Value | Reason | Current Representation |
|-------------|--------|----------------------|
| `LegacyImported` | Migration processing state, not lifecycle | `SourceSystem = WTMS Migration` and SharePoint `MigrationStatus` |
| `MetadataOnly` | Migration condition, not lifecycle | `SourceSystem = WTMS Migration` and empty `StorageURL` with `LegacySourceURL` populated |

### 2.3 Status Display Mapping

| Registry Status | Display in Portal |
|----------------|:-----------------:|
| published | ฉบับเผยแพร่ |
| current | ฉบับปัจจุบัน |
| obsolete | เลิกใช้แล้ว |
| archived | เก็บถาวร |
| All others | _(not displayed — excluded from export)_ |

---

## 3. Canonical Visibility Vocabulary

### 3.1 Approved Values (4 values)

| Visibility | Meaning | Public Export | Portal Behavior |
|------------|---------|:-------------:|-----------------|
| `public` | Accessible to all | **Included** | Listed, download enabled |
| `internal` | M365 org users only | **Excluded** | Not listed on public portal |
| `restricted` | Access by exception only | **Excluded** | Not listed |
| `private` | Owner group only | **Excluded** | Not listed |

### 3.2 Values NOT in Visibility Vocabulary

| Legacy Value | Reason | Current Representation |
|-------------|--------|----------------------|
| `PendingReview` | Workflow/review state, not visibility classification | `Status = review` + `Visibility = internal` |

---

## 4. SharePoint → Registry Mapping

### 4.1 Status Mapping

| SharePoint DocumentStatus | Registry Status | Mapping Mode | Notes |
|--------------------------|----------------|:------------:|-------|
| `LegacyImported` | _(mapped via SourceSystem)_ | DERIVED | SharePoint-only migration value not represented in registry Status |
| `Draft` | `draft` | DIRECT | Case normalization |
| `Current` | `current` | DIRECT | Case normalization |
| `Obsolete` | `obsolete` | DIRECT | Case normalization |
| `Archived` | `archived` | DIRECT | Case normalization |
| `MetadataOnly` | _(mapped via SourceSystem)_ | DERIVED | SharePoint-only migration condition not represented in registry Status |
| _(not in SharePoint)_ | `review` | REGISTRY_ONLY | Registry-only; not written back to SharePoint |
| _(not in SharePoint)_ | `approved` | REGISTRY_ONLY | Registry-only; not written back to SharePoint |
| _(not in SharePoint)_ | `published` | REGISTRY_ONLY | Registry-only; not written back to SharePoint |

> SharePoint-to-registry synchronization is one-directional for values that exist in both systems. Registry-only values (`review`, `approved`, `published`) are not written back to SharePoint's `DocumentStatus` column.

### 4.2 Visibility Mapping

| SharePoint PublicVisibility | Registry Visibility | Mapping Mode | Notes |
|----------------------------|-------------------|:------------:|-------|
| `PendingReview` | `internal` | DERIVED | PendingReview maps to internal; workflow state handled by Status |
| `Public` | `public` | DIRECT | Case normalization |
| `Internal` | `internal` | DIRECT | Case normalization |
| `Restricted` | `restricted` | DIRECT | Case normalization |
| _(not in SharePoint)_ | `private` | REGISTRY_ONLY | Registry-only; for sensitive documents |

---

## 5. Legal Status Transitions

```
                  ┌──────────────────────┐
             ┌─── │        review        │
             │    └──────────┬───────────┘
             │               │
             │               ▼
             │    ┌──────────────────────┐
             │    │      approved        │
             │    └──────────┬───────────┘
             │               │
             │               ▼
      ┌──────┴───┐    ┌──────────────────────┐
      │  draft   │    │    published         │
      └──────┬───┘    └──────────┬───────────┘
             │                   │
             │                   ▼
             │          ┌──────────────────────┐
             └─────────►│      current         │
                        └──────────┬───────────┘
                                   │
                        ┌──────────┴───────────┐
                        │                      │
                        ▼                      ▼
              ┌──────────────────┐  ┌──────────────────┐
              │    obsolete      │  │    archived      │
              └──────────────────┘  └──────────────────┘
```

### 5.1 Legal Transitions (forward)

| From | To | Valid? | Trigger |
|------|----|:------:|---------|
| `draft` | `review` | ✅ | Author submits for review |
| `review` | `approved` | ✅ | Category Owner approves |
| `review` | `draft` | ✅ | Sent back for revision |
| `review` | `obsolete` | ✅ | Found not relevant |
| `approved` | `published` | ✅ | Publication action |
| `approved` | `current` | ✅ | Direct set to current (internal docs) |
| `published` | `current` | ✅ | Publication -> active maintenance |
| `current` | `review` | ✅ | Periodic review triggered |
| `current` | `obsolete` | ✅ | Superseded |
| `current` | `archived` | ✅ | Retention period expired |
| `obsolete` | `archived` | ✅ | Owner moves to archive |
| `archived` | `current` | ❌ | _(must go through review first)_ |
| `obsolete` | `current` | ❌ | Cannot un-obsolete without review |

### 5.2 Invalid Transitions

| From | To | Reason |
|------|----|--------|
| `draft` | `published` | Skip — must be reviewed first |
| `draft` | `current` | Skip — must be reviewed first |
| `draft` | `obsolete` | Skip — must be reviewed or assessed first |
| `draft` | `archived` | Skip — must be reviewed or assessed first |
| `archived` | `current` | Cannot un-archive to active without review |
| `obsolete` | `current` | Cannot un-obsolete without review |
| `archived` | `obsolete` | No meaningful transition |
| `obsolete` | `archived` | Allowed (one-way) |

---

## 6. Visibility Transitions

```
    public ◄─► internal
    public ◄─► restricted
    public ◀── private   (one-way: must go through internal first)
  internal ◄─► restricted
  internal ◄─► private
restricted ──► private (tightening only; reverse requires review)
```

**All transitions are valid in either direction**, except `private → public` (must go through `internal` first as a deliberate review step) and `restricted → public` (must be deliberate).

---

## 7. Public Exposure Eligibility

A record is eligible for public portal export when:

| Condition | Must Be |
|-----------|---------|
| Status | `approved` OR `published` OR `current` |
| Visibility | `public` |
| StorageURL | Not empty; HTTPS reachable |
| DocumentID | Not empty |
| Title | Not empty |
| Owner | Not empty (M365 identity resolved) |
| Category | Not empty; enabled taxonomy category |
| Description | Recommended but not blocking |

**Public export MUST NEVER expose records with:**

- Status = `draft`, `review`, `obsolete`, `archived`
- Visibility = `internal`, `restricted`, `private`
- Empty or broken StorageURL (for active documents)
- Governance metadata (`Notes`, `ReviewDate`, `LegacySourceURL`)

---

## 8. Representation of Migration Source Conditions

### 8.1 Records with No Physical File (formerly "MetadataOnly")

For the ~100 WTMS migration records where the original file is inaccessible (404/403/login-required):

| Field | Value |
|-------|-------|
| Status | `current` or `obsolete` depending on document knowledge (not a special value) |
| Visibility | `internal` |
| SourceSystem | `WTMS Migration` |
| StorageURL | Empty (validated per rule: file does not exist) |
| LegacySourceURL | Preserved original URL |
| Notes | Reason the file was inaccessible |

These records are **never publicly exported** because `Visibility = internal`. Their lifecycle Status is set based on human assessment of whether the document is still relevant.

### 8.2 Records Awaiting Post-Migration Review

For migration records that have not yet been assigned an owner or reviewed:

| Field | Value |
|-------|-------|
| Status | `draft` (pending classification) |
| Visibility | `internal` |
| SourceSystem | `WTMS Migration` |

> No special status value (`LegacyImported`) is needed. The combination of `SourceSystem = WTMS Migration` + `Status = draft` + `Owner` still TBD captures the same condition without distorting lifecycle semantics.

### 8.3 Migration Condition Detection

The following query identifies migration records still in pre-review state:

```
Records WHERE SourceSystem = "WTMS Migration" AND Status = "draft"
```

This replaces the deprecated `Status = LegacyImported` filter.

---

## 9. Archive Behavior

| Action | Rule |
|--------|------|
| Moving to Archived | Status changed to `archived`. StorageURL may be retained or removed. StorageURL not validated. |
| Visibility on Archived | Should be changed to `internal` or `private`. Not publicly visible. |
| Reactivation from Archived | Not allowed directly. Must transition through `review` → `approved` → `current`. |

---

## 10. Obsolete Behavior

| Action | Rule |
|--------|------|
| Marking Obsolete | Status changed to `obsolete`. `RelatedDocuments` should reference the superseding DocumentID. |
| Notes on Obsolete | `Notes` must explain why the document is obsolete and what replaces it. |
| StorageURL on Obsolete | May be retained for reference access. Not validated. |
| Visibility on Obsolete | Should remain at or below the original visibility level. |

---

## 11. Interaction with Approval Workflow (Phase M365-5 Forward Reference)

This model is designed to be driven by Power Automate in Phase M365-5:

```
Trigger: Status changes to "review"
  → Notify Category Owner
  → Category Owner actions: Approve / Reject / Request Changes

Trigger: Status changes to "approved"
  → If Visibility = public: queue for publication
  → If Visibility != public: set Status to "current"

Trigger: Status changes to "published"
  → Validate StorageURL exists and is reachable
  → Add to public export queue
```

> No Power Automate flows are implemented in this phase.

---

## 12. Invalid Migrated Record Combinations

The following combinations represent data quality issues:

| Condition | Problem |
|-----------|---------|
| SourceSystem = WTMS Migration AND Status = published | A migration record should not be published without human review |
| SourceSystem = WTMS Migration AND Visibility = public | A migration record should not be public without explicit Owner decision |
| Status = draft AND Visibility = public | Draft documents must not be publicly visible |
| Status = archived AND Visibility = public | Archived documents must not be publicly visible |
| StorageURL empty AND Status = current/published/approved | Active documents must have a reachable StorageURL |

---

## Related Documents

| Document | Path |
|----------|------|
| Registry Schema | `docs/m365/registry-list-schema.md` |
| Validation Rules | `docs/m365/registry-validation-rules.md` |
| Owner Rules | `docs/m365/registry-owner-rules.md` |
| Views | `docs/m365/registry-views.md` |
| Export Contract | `docs/m365/registry-export-contract.md` |
| Library Schema (EA-3) | `docs/m365/library-schema.md` |
| Content Types (EA-3) | `docs/m365/content-types.md` |
| Registry Data Model (Phase 3.7) | `docs/document-center/REGISTRY_DATA_MODEL.md` |
