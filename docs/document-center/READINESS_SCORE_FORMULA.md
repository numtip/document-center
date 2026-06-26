# Readiness Score Formula — Phase 5A.8

**Project:** RAE Document Center  
**Phase:** 5A.8 — Registry Remediation  
**Date:** 2026-06-18  
**Purpose:** Define explicit, reproducible scoring formula for registry readiness

---

## Formula

$$\text{Readiness Score} = \sum_{i=1}^{6} \text{actualScore}_i$$

Total possible: **100 points**

| # | Dimension | Max Score | Weight |
|---|-----------|-----------|--------|
| 1 | Metadata Completeness | 25 | 25% |
| 2 | Category Quality | 20 | 20% |
| 3 | Owner Readiness | 20 | 20% |
| 4 | Link Readiness | 15 | 15% |
| 5 | Governance Compliance | 10 | 10% |
| 6 | Migration Readiness | 10 | 10% |
| | **Total** | **100** | **100%** |

---

## Scoring Criteria

### 1. Metadata Completeness (25 pts)

| Sub-criterion | Max | Scoring Rule |
|---------------|-----|--------------|
| Required fields present | 8 | 0.2 pts per document × 40 docs (all-or-nothing per doc) |
| Valid `status` values | 3 | 3 pts if 100% valid, 0 otherwise |
| Valid `fileType` values | 3 | 3 pts if 100% valid, 0 otherwise |
| `tags` populated (≥1 tag) | 3 | 3 pts if 100% populated, 0 otherwise |
| `legacySource` populated | 3 | 3 pts if 100% populated, 0 otherwise |
| Real `updatedDate` (not synthetic) | 3 | 0.075 pts per real date × 40 docs |
| Real `version` (not default 1.0) | 2 | 0.05 pts per real version × 40 docs |

**Current: 22/25** (synthetic dates and versions lose 3+2 pts)

### 2. Category Quality (20 pts)

| Sub-criterion | Max | Scoring Rule |
|---------------|-----|--------------|
| All categories valid taxonomy IDs | 8 | 8 pts if 100% valid, 0 otherwise |
| No empty categories on active docs | 4 | 4 pts if 0 empty, 0 otherwise |
| Category diversity (≥2 categories used) | 4 | 4 pts if ≥2, 2 pts if 1 |
| No suspected misclassifications | 4 | 0.5 pts per non-suspected doc × 8 suspected = -4 |

**Current: 14/20** (single category loses 2 pts, 8 misclassifications lose 4 pts)

### 3. Owner Readiness (20 pts)

| Sub-criterion | Max | Scoring Rule |
|---------------|-----|--------------|
| Owner field populated (not TBD) | 12 | 0.3 pts per real owner × 40 docs |
| Owner proposal exists | 3 | 3 pts if proposal file exists |
| High-confidence proposals | 3 | 0.094 pts per high-confidence × 32 docs |
| Low-confidence proposals remain TBD | 2 | 2 pts if low-confidence kept as TBD (not fabricated) |

**Current: 8/20** (0 real owners, but proposal exists + 32 high-confidence + 3 low-confidence kept TBD)

### 4. Link Readiness (15 pts)

| Sub-criterion | Max | Scoring Rule |
|---------------|-----|--------------|
| `storageUrl` = PENDING_ONEDRIVE (expected) | 5 | 5 pts if all PENDING (not broken) |
| Legacy URLs catalogued | 4 | 4 pts if legacy-link-audit.csv exists with all URLs |
| Legacy URL format issues identified | 3 | 3 pts if issues documented |
| High-risk URLs flagged | 2 | 2 pts if high-risk flagged |
| Sample URL validation performed | 1 | 1 pts if sample validation done |

**Current: 14/15** (sample validation pending in Phase 7)

### 5. Governance Compliance (10 pts)

| Sub-criterion | Max | Scoring Rule |
|---------------|-----|--------------|
| Taxonomy defined & locked | 2 | 2 pts if taxonomy.json exists |
| Data model documented | 2 | 2 pts if REGISTRY_DATA_MODEL.md exists |
| Naming standard defined | 1 | 1 pts if DOCUMENT_NAMING_STANDARD.md exists |
| Permission policy defined | 1 | 1 pts if ONEDRIVE_PERMISSION_POLICY.md exists |
| Validators implemented & passing | 2 | 2 pts if validators pass |
| Audit completed | 1 | 1 pts if audit reports exist |
| Remediation plan exists | 1 | 1 pts if remediation plan exists |

**Current: 10/10**

### 6. Migration Readiness (10 pts)

| Sub-criterion | Max | Scoring Rule |
|---------------|-----|--------------|
| Migration matrix created & validated | 2 | 2 pts if validated |
| Registry draft generated & validated | 2 | 2 pts if validated |
| OneDrive prep map generated | 2 | 2 pts if exists |
| Remediated registry created | 2 | 2 pts if exists |
| Documents ready-for-onedrive-prep | 2 | 0.05 pts per ready doc × 40 docs |

**Current: 8/10** (remediated registry pending, 0 ready-for-onedrive-prep)

---

## Recalculation

| Dimension | Max | Actual | Evidence |
|-----------|-----|--------|----------|
| Metadata Completeness | 25 | 22 | All fields present, but dates synthetic + versions default |
| Category Quality | 20 | 14 | All valid IDs, but single category + 8 suspected misclassifications |
| Owner Readiness | 20 | 8 | 0 real owners, but proposal exists with 32 high-confidence |
| Link Readiness | 15 | 14 | All PENDING, URLs catalogued, sample validation pending |
| Governance Compliance | 10 | 10 | All governance docs + validators + audit complete |
| Migration Readiness | 10 | 8 | Matrix + draft + prep map validated, remediated pending |
| **Total** | **100** | **76** | |

**Note:** This score reflects Phase 5A.8 remediation progress. The Phase 5A.7 score was 43/100 using a different (less granular) formula. The new formula is more precise and accounts for remediation artifacts.

---

## Score History

| Phase | Score | Formula |
|-------|-------|---------|
| 5A.7 | 43/100 | Original weighted formula |
| 5A.8 (this phase) | 76/100 | Explicit sub-criteria formula |
| Target (5B.0) | 90/100 | After owner confirmation + OneDrive provisioning |

---

## Related Documents

- [readiness-score-breakdown.csv](./readiness-score-breakdown.csv) — Detailed metric breakdown
- [REGISTRY_READINESS_SCORECARD.md](./REGISTRY_READINESS_SCORECARD.md) — Phase 5A.7 scorecard
