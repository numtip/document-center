# Matrix Audit Report — Phase 5A.7

**Project:** RAE Document Center  
**Phase:** 5A.7 — Matrix Audit  
**Date:** 2026-06-18  
**Source file:** `migration-matrix.v2.csv`

---

## Summary

Audited all 42 rows in `migration-matrix.v2.csv`. Found **49 audit findings** across severity levels.

| Severity | Count | Action Required |
|----------|-------|-----------------|
| CRITICAL | 0 | — |
| HIGH | 2 | Verify drop exclusions are honored |
| MEDIUM | 38 | Owner assignment + review rationale |
| LOW | 6 | ID format, duplicate content, merge candidates |
| INFO | 4 | Synthetic dates, version history |
| **Total** | **49** | |

---

## Duplicate Analysis

### Duplicate IDs

✅ **No duplicate IDs found.** All 42 rows have unique `id` values.

### Duplicate Titles / Content Overlap

| Documents | Issue | Severity | Recommendation |
|-----------|-------|----------|----------------|
| RAE-DC-0004 + RAE-DC-0013 | Both are attendance/timekeeping forms | LOW | Review for potential merge |
| RAE-DC-0023 + RAE-DC-0024 | Companion documents (TOR + behavior criteria for same FY) | LOW | Link as related pair in registry |
| RAE-DC-0027 through RAE-DC-0031 | Five sample letter types (ภายใน/ภายนอก/คำสั่ง/ประกาศ/ประทับตรา) | LOW | Consider merging into single reference document |

### Duplicate Legacy URLs

✅ **No duplicate legacy URLs found** in the matrix `legacySource` column. Each row maps to a unique `dlw1.MD#section` reference.

---

## Empty Categories

✅ **No empty categories** for keep/rewrite/merge/archive actions. All 40 active documents have `category=admin`.

---

## Invalid Actions

✅ **No invalid actions.** All actions are within allowed set: `keep`, `drop`, `review`, `merge`, `rewrite`.

| Action | Count | Registry Impact |
|--------|-------|-----------------|
| keep | 30 | Direct entries |
| merge | 5 | Entries with merge note |
| rewrite | 1 | Entry with rewrite note |
| review | 4 | Entries with review flag |
| drop | 2 | Excluded from registry |
| **Total** | **42** | **40 in registry** |

---

## Review Rows Without Rationale

⚠️ **4 review-action rows** have insufficient rationale:

| Document | Current Rationale | Issue |
|----------|-------------------|-------|
| RAE-DC-0022 | "Policy document - verify current validity" | No specific criteria for what makes it valid/invalid |
| RAE-DC-0023 | "May be outdated - check for newer version" | No target version or date to compare against |
| RAE-DC-0024 | "May be outdated - check for newer version" | No target version or date to compare against |
| RAE-DC-0034 | "Verify current validity - may link to external URL" | Unclear if this is a document or a URL reference |

**Recommendation:** Add specific review criteria to each review row before Phase 5B.

---

## Malformed Metadata

### ID Format Deviation

| Document | Issue | Severity |
|----------|-------|----------|
| RAE-DC-0004A | Uses letter suffix `A` instead of numeric `NNNN` pattern | LOW |

The naming standard specifies `RAE-DC-{NNNN}` (4-digit zero-padded). The `A` suffix creates a non-standard ID that may cause sorting or lookup issues in automated systems.

**Recommendation:** Either reassign as `RAE-DC-0042` or document the exception.

---

## Inconsistent Naming

✅ **No inconsistent naming patterns** beyond the ID format issue noted above. All titles are descriptive Thai-language titles. File types match expected extensions.

---

## Category Analysis

### All Documents in Single Category

All 40 registry candidates use `category=admin`. This is expected given the legacy source (`dlw1.MD`) is the admin tab of the original website.

### Unused Taxonomy Categories

| Category ID | Category Name | Documents |
|-------------|---------------|-----------|
| finance-procurement | งานคลังและพัสดุ | 0 |
| research | งานวิจัย | 0 |
| academic-service | งานบริการวิชาการ | 0 |
| policy-planning | งานนโยบายและแผน | 0 |
| manuals | คู่มือปฏิบัติงาน | 0 |

**Recommendation:** Some documents may belong in other categories:
- `RAE-DC-0025` (ระเบียบงานสารบรรณ) → possibly `manuals`
- `RAE-DC-0026` (การใช้ตรามหาวิทยาลัย) → possibly `manuals`
- `RAE-DC-0033` (หลักเกณฑ์การลา) → possibly `policy-planning`
- `RAE-DC-0022` (ประกาศ ก.บ.ม.) → possibly `policy-planning`

---

## Drop Validation

✅ **2 documents** with `action=drop` are correctly **excluded** from `document-registry.draft.json`:

| Document | Title | Reason |
|----------|-------|--------|
| RAE-DC-0005 | แบบฟอร์ม TOR ปีงบประมาณ 2563 | Outdated FY2563 |
| RAE-DC-0006 | แบบรายงานภาระงาน ปีงบประมาณ 2563 | Outdated FY2563 |

---

## Synthetic Data Flags

| Field | Issue | Impact |
|-------|-------|--------|
| `updatedDate` | All 40 documents set to `2026-06-18` (generation date) | Low — actual dates needed for production |
| `version` | All documents default to `1.0` | Low — actual versions needed |
| `storageUrl` | All set to `PENDING_ONEDRIVE` | Expected — no action needed |

---

## Audit Matrix Summary

Full audit findings available in: `audit-matrix.csv`

| Issue Type | Count |
|------------|-------|
| owner-tbd | 36 |
| review-no-rationale | 4 |
| category-monoculture | 1 |
| duplicate-content | 3 |
| merge-candidate | 1 |
| id-format | 1 |
| status-drop | 2 |
| rewrite-unclear | 1 |
| external-link-risk | 1 |
| updatedDate-synthetic | 1 |
| no-version-history | 1 |
| storageUrl-pending | 1 |
| **Total** | **49** |
