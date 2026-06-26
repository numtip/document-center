# Phase 5A.6 — Registry Hardening Before OneDrive Migration

**Project:** RAE Document Center  
**Phase:** 5A.6 — Registry Hardening Before OneDrive Migration  
**Status:** Complete  
**Date:** 2026-06-18  
**Source of Truth:** GitHub metadata  
**Storage Layer:** OneDrive (pending — not yet provisioned)

---

## Summary

Phase 5A.6 hardened the document registry system in preparation for OneDrive migration. Starting from the legacy website data (`dlw1.MD`) and the existing taxonomy/data model from earlier phases, this phase:

1. Created a **migration matrix** cataloging all legacy documents with triage decisions
2. Built a **registry draft** from the matrix, conforming to the `REGISTRY_DATA_MODEL.md` schema
3. Created **two validation scripts** (matrix + registry) for ongoing quality assurance
4. Generated an **OneDrive migration prep map** — a human-actionable checklist for the physical migration step
5. Produced this report

**No files were uploaded to OneDrive. No production systems were touched. No git commits were made.**

---

## Files Created

| File | Purpose |
|------|---------|
| `docs/document-center/migration-matrix.v2.csv` | Triage decisions for all legacy documents (42 rows) |
| `docs/document-center/document-registry.draft.json` | Registry draft conforming to data model (40 documents) |
| `docs/document-center/onedrive-migration-prep.csv` | Human-actionable OneDrive migration checklist (40 rows) |
| `scripts/validate-document-migration-matrix.ts` | CSV matrix validator |
| `scripts/validate-document-registry.ts` | JSON registry validator |
| `scripts/generate-registry-draft.ts` | Matrix → registry draft generator |
| `scripts/generate-onedrive-prep-map.ts` | Registry → prep map generator |
| `package.json` | Node.js project config with npm scripts |
| `tsconfig.json` | TypeScript configuration |

## Files Changed

| File | Change |
|------|--------|
| `scripts/validate-document-registry.ts` | Fixed owner validation to allow `needs-human-review` status with TBD owners |

---

## Validation Results

### Migration Matrix (`migration-matrix.v2.csv`)

| Metric | Value |
|--------|-------|
| Status | ✅ PASSED |
| Total rows | 42 |
| Required columns | All present |
| Duplicate IDs | 0 |
| Invalid actions | 0 |
| Empty categories on keep/rewrite/merge/archive | 0 |

### Registry Draft (`document-registry.draft.json`)

| Metric | Value |
|--------|-------|
| Status | ✅ PASSED |
| JSON parse | Valid |
| Required fields | All present on all 40 documents |
| Invalid status values | 0 |
| Duplicate IDs | 0 |
| Category taxonomy match | ✅ All match |
| Empty owner violations | 0 (all marked `needs-owner`) |

---

## Registry Counts by migrationStatus

| migrationStatus | Count | Meaning |
|-----------------|-------|---------|
| `needs-owner` | 36 | Owner TBD — requires human assignment |
| `needs-human-review` | 4 | Owner TBD + review action — requires human judgment |
| `needs-onedrive-url` | 0 | Ready for OneDrive (blocked by owner assignment) |
| `metadata-ready` | 0 | Fully ready (blocked by owner + URL) |
| **Total** | **40** | |

> Note: All 40 documents have `migrationStatus=needs-owner` because every legacy document owner is currently marked TBD. Owner assignment is the critical-path blocker for all documents.

---

## Migration Action Breakdown (from matrix)

| Action | Count | Registry Impact |
|--------|-------|-----------------|
| `keep` | 30 | Direct registry entries |
| `merge` | 5 | Registry entries — note which docs to merge |
| `rewrite` | 1 | Registry entry — content rewrite required |
| `review` | 4 | Registry entries with `needs-human-review` status |
| `drop` | 2 | Excluded from registry (2 outdated assessment forms) |
| **Total** | **42** | **40 in registry, 2 excluded** |

---

## Remaining Human Actions

### Critical Path (blocks everything)

1. **Assign owners to all 40 documents** — Every document needs a responsible person/unit. Start with category leads:
   - `admin` category: 40 documents (all legacy admin forms)
   - No documents in other categories yet (legacy source was `dlw1.MD` = admin tab only)

### OneDrive Migration Steps (after owner assignment)

2. **Provision OneDrive folder structure** — Create `RAE-Document-Center/` root and all category subfolders
3. **Upload files** — For each of the 40 documents, upload to the correct category folder
4. **Apply naming standard** — Rename files per `DOCUMENT_NAMING_STANDARD.md`
5. **Create share links** — Generate view-only share links for all `current` documents
6. **Update registry** — Set `storageUrl` to real OneDrive URLs
7. **Run link validation** — Verify all URLs resolve

### Review-Specific Steps

8. **Review 4 review-action documents** — Determine if they are current, outdated, or should be dropped:
   - `RAE-DC-0022`: ประกาศ คกก. ก.บ.ม. เรื่อง วัน เวลาปฏิบัติงาน พ.ศ.2564
   - `RAE-DC-0023`: หลักเกณฑ์ประเมินผล ปีงบประมาณ 2565
   - `RAE-DC-0024`: หลักเกณฑ์ประเมินพฤติกรรม ปีงบประมาณ 2565
   - `RAE-DC-0034`: สิทธิการลาของบุคลากรประเภทต่างๆ

### Merge-Specific Steps

9. **Merge 5 sample letter documents** — Consider combining `RAE-DC-0027` through `RAE-DC-0031` (ตัวอย่างหนังสือราชการ) into a single reference document

### Rewrite-Specific Steps

10. **Rewrite 1 document** — `RAE-DC-0032` (ขั้นตอนการขออนุมัติเดินทางไปต่างประเทศ) may need modern rewrite

---

## OneDrive Migration Readiness

| Readiness Criterion | Status |
|---------------------|--------|
| Migration matrix created | ✅ Complete |
| Registry draft generated | ✅ Complete |
| Validators working | ✅ Both pass |
| Prep map generated | ✅ Complete |
| OneDrive folder structure | ❌ Not provisioned |
| Document files uploaded | ❌ No files uploaded |
| Share links created | ❌ No links |
| Owners assigned | ❌ All 40 TBD |
| Link validation | ❌ Blocked by upload |

**Overall readiness: PARTIAL** — Metadata layer is hardened and validated. Physical OneDrive migration cannot proceed without human owner assignment and folder provisioning.

---

## Blockers

| # | Blocker | Impact | Resolution |
|---|---------|--------|------------|
| 1 | All 40 document owners are TBD | Cannot complete `storageUrl` assignment | Human must assign owners per category |
| 2 | OneDrive not provisioned | Cannot upload files or create links | Create `RAE-Document-Center/` folder structure |
| 3 | No legacy file inventory | Don't know which files physically exist | Manual inventory or ERP system query |
| 4 | Legacy links are ERP-hosted | Legacy URLs (erp.mju.ac.th) are not OneDrive links | Files must be downloaded from ERP and re-uploaded to OneDrive |

---

## Next Recommended Phase

**Phase 5B — Owner Assignment & OneDrive Provisioning**

1. Assign named owners for each document (or delegate to category leads)
2. Provision OneDrive `RAE-Document-Center/` folder structure with permissions
3. Create physical inventory of available files (from ERP system)
4. Upload files to OneDrive with proper naming
5. Generate share links and update registry `storageUrl` fields
6. Re-run validators to confirm `needs-owner` → `needs-onedrive-url` → `metadata-ready` progression

After Phase 5B, the registry will be ready for Phase 6 (UI integration with Next.js Document Center).

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [REGISTRY_DATA_MODEL.md](./REGISTRY_DATA_MODEL.md) | Schema reference |
| [taxonomy.json](./taxonomy.json) | Category definitions |
| [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md) | File naming rules |
| [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md) | Access control |
| [PHASE3_ONEDRIVE_STORAGE_GUIDE.md](./PHASE3_ONEDRIVE_STORAGE_GUIDE.md) | OneDrive foundation |
| [migration-matrix.v2.csv](./migration-matrix.v2.csv) | Triage decisions |
| [document-registry.draft.json](./document-registry.draft.json) | Registry draft |
| [onedrive-migration-prep.csv](./onedrive-migration-prep.csv) | Migration checklist |
