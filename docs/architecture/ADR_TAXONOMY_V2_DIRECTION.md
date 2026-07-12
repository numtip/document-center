# ADR: Taxonomy v2 Direction — RAE Document Center

**Status:** Proposed  
**Date:** 2026-07-12  
**Authority:** EA-3F Forward Architecture Readiness  
**Canonical repository:** `numtip/document-center`

---

## Context

The RAE Document Center taxonomy has three representations across the canonical repository and EA documentation:

1. **Implemented v1.0.0** — `taxonomy.json`: 6 flat categories, locked, validated, consumed by all registry scripts and the preview pipeline.
2. **Proposed extended taxonomy** — `M365 FoundationBlueprint.MD` Phase M365-2: 6 current categories + 4 future categories (Green Office, Research Portal, Learning Center, Quality Assurance) = 10 total categories.
3. **Claimed hierarchical v2** — Referenced only in `EA_RECOVERY_GAP_MATRIX.md` and `EA_LEGACY_RECOVERY_MANIFEST.md` as a "claimed" artifact with 10 domains, 30 categories, 62 subcategories, 11 document types. **No file evidence exists** — this is a design concept, not a real artifact.

---

## Comparison

| Dimension | V1.0.0 (Implemented) | Blueprint Extended (Proposed) | Hierarchical V2 (Claimed) |
|-----------|----------------------|-------------------------------|---------------------------|
| **Evidence** | `taxonomy.json` — real file | `M365 FoundationBlueprint.MD` — real proposal | No file exists |
| **Depth** | Flat: Category only | Flat: Category only | 4 levels: Domain → Category → Subcategory → Document Type |
| **Breadth** | 6 categories | 10 categories (6 + 4 future) | 10 domains, 30 categories, 62 subcategories, 11 document types |
| **Status** | Locked v1.0.0 | Proposed | Never created (claimed only) |
| **Validated** | Yes — consumed by 4 scripts, 0 errors | No | No |
| **Migration compatibility** | Current baseline | Compatible with v1 (additive) | Breaking — restructure required |
| **OneDrive mapping** | 6 folders (01–06) | 10 folders | No folder mapping defined |
| **Document registry usage** | `category` field references taxonomy `id` | Same model | Would need new `domain` + `subcategory` + `document_type` fields |
| **SharePoint content type impact** | Category = choice column | Category = extended choice column | Content types would need multi-level hierarchy (managed metadata) |

---

## Options

### Option A: KEEP_V1

**Decision:** Lock v1.0.0 as final. No expansion. Accept the 6-category limitation.

**Impact:**
- All current validators work unchanged.
- SharePoint content types use 6 categories as a choice column.
- The 4 future categories (Green Office, Research Portal, Learning Center, Quality Assurance) are either added as separate content types or folded into existing categories as metadata.
- No hierarchical taxonomy path. All classification is single-level.

| Pro | Con |
|-----|-----|
| Zero migration cost | Cannot represent domain/subcategory relationships |
| All validators pass as-is | May limit SharePoint managed metadata usefulness |
| Simplest implementation | Green Office / QA documents forced into existing categories |
| Fastest path to EA-3F | Extended taxonomy work deferred indefinitely |

### Option B: EXTEND_COMPATIBLY

**Decision:** Extend `taxonomy.json` to add the 4 future categories (v1.1.0). Keep flat structure. No hierarchy.

**Impact:**
- Add 4 new category entries to `taxonomy.json`.
- Version bump from 1.0.0 to 1.1.0.
- All existing 6 categories remain unchanged — 0 migration impact.
- All existing validated records remain valid — `category` field values are unchanged.
- New OneDrive folders (07–10) created for new categories.
- SharePoint content types get an extended choice column (10 values).

| Pro | Con |
|-----|-----|
| Preserves all validated data | No hierarchy — still single-level |
| Low migration cost | Category count grows over time |
| All validators compatible with update | Does not address claimed 62-subcategory requirement |
| Quick implementation | |
| Aligns with Blueprint Phase M365-2 scope | |

### Option C: REPLACE_WITH_V2

**Decision:** Design a new hierarchical taxonomy: Domain → Category → Subcategory → Document Type. Replace `taxonomy.json` with a new schema.

**Impact:**
- New schema structure — breaking change.
- All existing document registry records need `domain`, `subcategory`, and `document_type` fields added (or mapped).
- Validators must be rewritten.
- OneDrive folder structure may need reorganization.
- SharePoint content types would use managed metadata columns.
- Significant design and implementation effort.

| Pro | Con |
|-----|-----|
| Full hierarchical classification | Breaking change to all existing records and validators |
| Aligns with EA governance best practices | 10/30/62/11 is a claimed scope — actual requirements may differ |
| Best long-term scalability | Requires full redesign — not simply "importing" a pre-existing v2 |
| Supports SharePoint managed metadata | Blocks EA-3F until complete |
| | Claimed v2 scope was never validated — may be over-engineered for RAE needs |

---

## Recommendation: EXTEND_COMPATIBLY (Option B)

### Rationale

1. **Preserves validated data.** All 40 document registry records, 42 migration matrix rows, and the example dataset validate against the existing 6 categories. Extending to 10 categories does not invalidate any existing record.

2. **Blueprint alignment.** The M365 Blueprint Phase M365-2 explicitly names the 4 future categories. The Blueprint is the approved roadmap. EXTEND_COMPATIBLY aligns taxonomy evolution with the Blueprint without exceeding it.

3. **No blocked path.** EXTEND_COMPATIBLY does not prevent a future hierarchical v2. If hierarchical classification becomes necessary, the v1.1 taxonomy can serve as the category layer (level 2) in a Domain → Category → Subcategory model. Domains can be added above without restructuring existing categories.

4. **Minimal implementation cost.** Taxonomy extensions are additive: 4 new JSON entries, 4 new OneDrive folders, and an updated choice column for SharePoint. Validators check category existence against `taxonomy.json` — they will automatically accept new categories on the next schema version.

5. **EA-3F friendly.** SharePoint content types can use the extended 10-category choice column from day one. No hierarchical managed metadata configuration needed for the initial provisioning.

### Conditions

- `taxonomy.json` is updated to v1.1.0 with 4 additional categories (see Phase EA-3F.1 correction scope — this is **not** part of the current phase; this ADR records the decision for the next implementation phase).
- All existing validators are verified to accept the extended set with a version bump (expected: no code changes needed; validators read `categories[]` dynamically).
- The 4 future categories use the same schema shape as existing ones (`id`, `name_th`, `name_en`, `folder`, `owner_group`, etc.).
- OneDrive folder numbering continues: `07-GreenOffice`, `08-ResearchPortal`, `09-LearningCenter`, `10-QualityAssurance`.

### Rejected Options

- **KEEP_V1** rejected because the Blueprint explicitly identifies 4 additional categories that are expected by the target architecture. Deferring indefinitely creates a gap between the taxonomy and the SharePoint library design.
- **REPLACE_WITH_V2** rejected because:
  - The 10/30/62/11 scope is a claimed artifact with no evidence — actual RAE taxonomy requirements are unknown.
  - Breaking change would delay EA-3F significantly.
  - A hierarchical v2 can be introduced later without breaking the extended v1.1 by layering domains above existing categories.

---

## Decision

```
ACCEPTED: EXTEND_COMPATIBLY
```

Action: When taxonomy extension is implemented (post-EA-3F readiness), `taxonomy.json` version shall become `1.1.0` with 4 new categories added. No structural change. No existing records affected.

---

## Related Documents

- `docs/document-center/taxonomy.json` — current v1.0.0 taxonomy
- `docs/document-center/M365 FoundationBlueprint.MD` — Phase M365-2: Information Architecture Design
- `docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md` — canonical current state
- `docs/architecture/EA_SHAREPOINT_FOUNDATION_READINESS.md` — taxonomy readiness classification
- `docs/architecture/EA_RECOVERY_GAP_MATRIX.md` — taxonomy gap detail (EA-3D)
