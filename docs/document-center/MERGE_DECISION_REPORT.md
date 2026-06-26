# Merge Decision Report — Phase 5A.8

**Project:** RAE Document Center  
**Phase:** 5A.8 — Merge Decision Pack  
**Date:** 2026-06-18  
**Source:** 5 documents with `action=merge` + 2 duplicate-content findings

---

## Summary

Identified 2 merge groups containing 7 source documents. No records were actually merged — only canonical recommendations are defined. Source lineage is preserved.

| Metric | Count |
|--------|-------|
| Total merge groups | 2 |
| Total source documents | 7 |
| Canonical documents proposed | 2 |
| Human decisions required | 7 (all) |

---

## Merge Groups

### MERGE-GROUP-001 — Sample Letters (5 documents)

| Source Document | Title | Canonical? |
|-----------------|-------|------------|
| RAE-DC-0027 | ตัวอย่างหนังสือราชการ หนังสือภายใน | ✅ Canonical |
| RAE-DC-0028 | ตัวอย่างหนังสือราชการ หนังสือภายนอก | Merge into 0027 |
| RAE-DC-0029 | ตัวอย่างหนังสือราชการ คำสั่ง | Merge into 0027 |
| RAE-DC-0030 | ตัวอย่างหนังสือราชการ ประกาศ | Merge into 0027 |
| RAE-DC-0031 | ตัวอย่างหนังสือราชการ หนังสือประทับตรา | Merge into 0027 |

**Proposed Canonical:** RAE-DC-0027 → "ตัวอย่างหนังสือราชการ (ฉบับรวม)"

**Merge Reason:** All 5 documents are sample letter types under the same theme "ตัวอย่างหนังสือราชการ". They could be consolidated into a single reference document with sub-sections for each letter type (ภายใน, ภายนอก, คำสั่ง, ประกาศ, ประทับตรา).

**Alternative:** Keep as 5 separate entries if users need to download individual letter types.

---

### MERGE-GROUP-002 — Attendance Forms (2 documents)

| Source Document | Title | Canonical? |
|-----------------|-------|------------|
| RAE-DC-0004 | แบบแจ้งการลงเวลาปฏิบัติงาน (เข้า ออก เข้าและออก เข้าสาย ออกก่อน) | ✅ Canonical |
| RAE-DC-0013 | แบบฟอร์มลงเวลาปฏิบัติราชการ | Merge into 0004 |

**Proposed Canonical:** RAE-DC-0004 → "แบบฟอร์มลงเวลาปฏิบัติงาน (ฉบับรวม)"

**Merge Reason:** Both documents are attendance/timekeeping forms. RAE-DC-0004 has a more detailed title (specifies เข้า ออก เข้าและออก เข้าสาย ออกก่อน). The original notes already indicate "may merge with RAE-DC-0004". The merged entry would contain both PDF and WORD versions.

---

## Canonical Selection Criteria

Canonical documents were selected based on:

1. **Lowest ID number** — Earlier IDs are preferred as canonical
2. **Most descriptive title** — The title that best represents the merged content
3. **Source lineage preservation** — All source document IDs are recorded in the merge pack

---

## Source Lineage Preservation

No source documents are deleted. If human approves a merge:

1. The canonical document's `notes` field will list all merged source IDs
2. Merged source documents will be marked `status: obsolete` with a reference to the canonical
3. The canonical document's `tags` will include all tags from merged sources
4. File versions from all sources will be preserved in OneDrive

---

## Impact on Registry

If human approves all merges:

| Metric | Before | After |
|--------|--------|-------|
| Total documents | 40 | 35 |
| Merge groups resolved | 0 | 2 |
| Documents marked obsolete | 0 | 5 (4 from group 1 + 1 from group 2) |
| Canonical documents | 0 | 2 |

---

## Human Decision Required

For each merge group, human must decide:

### MERGE-GROUP-001 (Sample Letters)
- [ ] **Option A:** Merge into 1 canonical document (RAE-DC-0027)
- [ ] **Option B:** Keep as 5 separate documents
- [ ] **Option C:** Partial merge (e.g., merge ภายใน+ภายนอก, keep others separate)

### MERGE-GROUP-002 (Attendance Forms)
- [ ] **Option A:** Merge into 1 canonical document (RAE-DC-0004)
- [ ] **Option B:** Keep as 2 separate documents

---

## Related Documents

- [merge-decision-pack.csv](./merge-decision-pack.csv) — Full merge decision table
- [audit-matrix.csv](./audit-matrix.csv) — Original merge-candidate findings
- [migration-matrix.v2.csv](./migration-matrix.v2.csv) — Original merge actions
