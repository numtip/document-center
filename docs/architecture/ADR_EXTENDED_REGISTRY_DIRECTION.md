# ADR: Extended Registry Direction — RAE Document Center

**Status:** Proposed  
**Date:** 2026-07-12  
**Authority:** EA-3F Forward Architecture Readiness  
**Canonical repository:** `numtip/document-center`

---

## Context

The RAE Document Center metadata registry has three representations:

1. **Implemented 13-field registry** — `REGISTRY_DATA_MODEL.md` (locked v1.0.0): `id`, `title`, `category`, `owner`, `file_type`, `status`, `updated_date`, `onedrive_path`, `storage_url`, `tags`, `version`, `visibility`, `note`.
2. **M365 Blueprint Lists schema (10 fields)** — `M365 FoundationBlueprint.MD` Phase M365-4: `DocumentID`, `Title`, `Category`, `Owner`, `Status`, `FileURL`, `Version`, `UpdatedDate`, `Tags`, `Notes`.
3. **Claimed 26-field extended model** — Referenced only in recovery documentation. **No file evidence exists.** The claimed field set likely includes compliance dates, approval workflow state, retention schedule, and AI eligibility flags.

---

## Comparison

| Registry Aspect | Existing 13-Field (Implemented) | Blueprint Lists 10-Field (Proposed) | Claimed 26-Field (No Evidence) |
|-----------------|--------------------------------|-------------------------------------|-------------------------------|
| **Evidence** | `REGISTRY_DATA_MODEL.md` — real, locked | `M365 FoundationBlueprint.MD` — real proposal | No file exists |
| **Field count** | 13 | 10 | 26 |
| **Required fields** | 10 | Not specified | Claimed 15 |
| **Status** | Locked, validated, consumed by scripts | Proposed | Concept only |
| **Validation** | 4 validators check registry data | Not implemented | Not implemented |
| **Microsoft Lists target** | No column mapping defined | 10 fields named | No column mapping defined |
| **SharePoint column mapping** | None | None | None |

---

## Field-by-Field Analysis

### Fields Reusable As-Is

These fields exist in the current registry, are confirmed valid, and map directly to Lists columns:

| Current Field | Lists Equivalent | Type | Notes |
|---------------|------------------|------|-------|
| `id` | DocumentID | String (Single line) | `RAE-DC-NNNN` format, validated for uniqueness |
| `title` | Title | String (Single line) | Human-readable title |
| `category` | Category | Choice | Drawn from `taxonomy.json` categories |
| `owner` | Owner | String (Single line) or Person | Currently email/role string; Person column preferred in Lists |
| `status` | Status | Choice | 4 validated values (current, obsolete, archived, draft) |
| `version` | Version | String (Single line) | Semantic version (`1.0`, `1.1`, `2.0`) |
| `updated_date` | UpdatedDate | Date/Time | YYYY-MM-DD format |
| `tags` | Tags | Multiple lines or JSON | Currently lowercase string array; Lists Multi-Choice or JSON |
| `note` / `notes` | Notes | Multiple lines of text | Free-text notes field |

**Count: 9 fields reusable as-is** (direct 1:1 mapping to Lists columns with type compatibility)

### Fields Requiring Mapping

These fields exist in the current registry but need schema mapping to Lists:

| Current Field | Lists Mapping | Mapping Risk | Notes |
|---------------|--------------|--------------|-------|
| `file_type` | Not in Blueprint 10-field set | **MEDIUM** — implied by FileURL extension | Could be derived from FileURL or added as separate choice column. Current validated values: `pdf`, `docx`, `xlsx`, `pptx`, `png`, `jpg`. |
| `onedrive_path` | Not in Blueprint 10-field set | **HIGH** — path structure will change | Current paths reference OneDrive folder structure (`06-คู่มือปฏิบัติงาน/RAE-DC-0001_...`). SharePoint migration will change paths to document library paths. Temporary field until migration. |
| `storage_url` | FileURL | **LOW** — rename only | Current field is OneDrive share link. Blueprint calls it FileURL. Post-migration, this becomes SharePoint item URL. Field semantics identical; name change only. |
| `visibility` | Not in Blueprint 10-field set | **MEDIUM** — governance-critical | Current 3 values (public, internal, restricted). Blueprint does not include this field, but it is essential for public-export governance. Should be retained and mapped to SharePoint permission scopes. |

**Count: 4 fields requiring mapping**

### New Fields (Blueprint or Claimed)

Fields that do not exist in the current registry but are named in the Blueprint or claimed in the extended model:

| Field | Source | Type | Priority | Notes |
|-------|--------|------|----------|-------|
| `FileURL` | Blueprint Phase M365-4 | Hyperlink or URL | **HIGH** | Blueprint names this explicitly. Maps to current `storage_url`. Same field, different name. |
| Compliance/Retention dates | Claimed 26-field | Date | **MEDIUM** | Needed for governance but not explicitly called out in Blueprint. Retention schedule for each document. |
| Approval workflow state | Claimed 26-field | Choice | **MEDIUM** | Related to expanded status model. Values like `pending-review`, `approved`. |
| AI eligibility flag | Claimed 26-field | Boolean/Choice | **LOW** | Which documents qualify as AI training source. Requires policy (does not exist yet). |
| Document type | Claimed 26-field | Choice | **MEDIUM** | Related to taxonomy v2 document type layer. Dependent on taxonomy ADR outcome. |

**Count: 5 new fields identified (2 high priority, 2 medium, 1 low)**

### Deprecated Fields

| Current Field | Deprecation Risk | Reason |
|---------------|-----------------|--------|
| `onedrive_path` | **Expected deprecation** after SharePoint migration | Paths will change from OneDrive folder structure to SharePoint document library paths. This field should be retained during migration as a legacy reference, then optionally retired. |

**Count: 1 field with expected deprecation (not immediate)**

---

## Compatibility Risks

### Risk 1: OneDrive Path → SharePoint Path Change

**Severity: HIGH**

Every current document registry record contains an `onedrive_path` pointing to OneDrive folders. Post-migration, these paths will change to SharePoint document library paths. The registry must support both path types during migration. The `onedrive_path` field should be preserved as a legacy reference during migration, with a new `sharepoint_path` field added.

### Risk 2: Person Column Type

**Severity: MEDIUM**

The current `owner` field is a free-text string (email or role). Microsoft Lists supports Person columns that resolve to Entra ID users. If Person columns are used, legacy records with role-based owners (e.g., "Administration unit lead") will not resolve. A hybrid approach (Person column + free-text fallback) or a separate `owner_role` field may be needed.

### Risk 3: FileURL / storage_url Unification

**Severity: LOW**

The Blueprint names FileURL but the current registry calls it `storage_url`. Simple rename. No data loss. Must decide which name to standardize on for Lists.

### Risk 4: Tags Data Type

**Severity: LOW**

Current `tags` is a JSON string array. Microsoft Lists supports Multi-Choice columns (predefined choices) or JSON in a multi-line text field. Multi-Choice is more governable but limits flexibility. JSON multi-line preserves flexibility but requires parsing. Choice depends on whether tags should be governed (controlled vocabulary) or free-form.

---

## Recommendation: EXTEND_COMPATIBLY — Adopt 13+4 Field Model

### Decision Framework

| Factor | Assessment |
|--------|-----------|
| Current registry usability | High — 13 fields validated, consumed by 4 scripts, 40 documents clean |
| Blueprint alignment | Good — 9 of 10 Blueprint fields map directly to current fields |
| Claimed 26-field practicality | Poor — 5 new fields identified but 13 of the "26" are unaccounted for; no evidence the full 26-field set was ever designed |
| Implementation risk | Low for 13+4; High for full 26-field (unknown scope) |

### Recommended Registry Evolution

Phase 1 (EA-3F companion — Lists schema design):

| # | Field | Lists Column Type | Source | Action |
|---|-------|-------------------|--------|--------|
| 1 | DocumentID | Single line of text | Existing `id` | As-is |
| 2 | Title | Single line of text | Existing `title` | As-is |
| 3 | Category | Choice (from taxonomy) | Existing `category` | Extend choice list if taxonomy extended to 10 |
| 4 | Owner | Person or Single line | Existing `owner` | Try Person column; fallback to text for role-based owners. Document decision. |
| 5 | Status | Choice | Existing `status` | As-is (4 values). Extend if status model is expanded via separate ADR. |
| 6 | FileURL | Hyperlink or URL | Existing `storage_url` | Rename in Lists. Current field name can stay in JSON registry. |
| 7 | Version | Single line of text | Existing `version` | As-is |
| 8 | UpdatedDate | Date and Time | Existing `updated_date` | As-is |
| 9 | Tags | Multi-Choice or Multi-line | Existing `tags` | Decision needed: governed (Multi-Choice) vs. flexible (JSON multi-line). |
| 10 | Notes | Multiple lines of text | Existing `note` | As-is |
| 11 | File Type | Choice | Existing `file_type` | Retain — needed for search filter. Not in Blueprint but validated. |
| 12 | Visibility | Choice | Existing `visibility` | Retain — governance-critical. Not in Blueprint but essential. |
| 13 | OneDrive Path | Single line of text | Existing `onedrive_path` | Retain as legacy reference during migration. Deprecation post-migration. |

Phase 2 (Post-EA-3F, as needed):

| # | Field | When to Add | Precondition |
|---|-------|------------|--------------|
| 14 | SharePoint Path | After migration begins | SharePoint site provisioned |
| 15 | Retention Date | After compliance requirement confirmed | Tenant capability audit |
| 16 | Approval State | After Power Automate workflows designed | Taxonomy ADR + status model ADR |
| 17 | AI Eligibility | After AI source policy authored | Public export policy exists |
| 18 | Document Type | After taxonomy ADR implemented | Taxonomy extended to include document type layer |

### What This Means

- The existing 13-field registry is **not replaced**. It is the validated, proven schema.
- The Microsoft Lists schema (Phase M365-4) will use **all 13 existing fields**, with `storage_url` renamed to FileURL in Lists and 9 of 10 Blueprint fields directly mappable.
- `file_type` and `visibility` are retained despite not being in the Blueprint 10-field set — they are governance-critical and validated.
- The claimed 26-field set is not adopted wholesale. New fields beyond the current 13 are added incrementally as their preconditions are met (see Phase 2 table).
- No registry files are mutated in this phase. This ADR records the target schema direction for when Lists provisioning begins.

---

## Decision

```
ACCEPTED: EXTEND_COMPATIBLY (13+4 Model)
```

The Microsoft Lists schema reuses all 13 existing fields (9 with 1:1 mapping, 4 with mapping decisions documented above). Beyond the current 13, 5 new fields are identified for phased addition. The claimed 26-field set is not adopted as a single-phase expansion. No production or sample registry files are modified by this ADR.

---

## Related Documents

- `docs/document-center/REGISTRY_DATA_MODEL.md` — current locked 13-field schema
- `docs/document-center/M365 FoundationBlueprint.MD` — Phase M365-4: Microsoft Lists Registry (10 proposed fields)
- `docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md` — canonical current state
- `docs/architecture/EA_SHAREPOINT_FOUNDATION_READINESS.md` — metadata readiness classification
- `docs/architecture/EA_RECOVERY_GAP_MATRIX.md` — metadata gap detail (EA-3E)
