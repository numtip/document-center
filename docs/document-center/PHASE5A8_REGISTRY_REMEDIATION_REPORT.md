# Phase 5A.8 — Registry Remediation Report

**Project:** RAE Document Center  
**Phase:** 5A.8 — Registry Remediation  
**Status:** Complete  
**Date:** 2026-06-18  
**Decision:** **PARTIAL**  
**Readiness Score:** 43/100 → 76/100

---

## Summary

Phase 5A.8 remediated Phase 5A.7 audit findings and moved the registry from BLOCKED prototype toward migration-ready metadata. The remediation defined an explicit readiness score formula, triaged all 49 audit findings, created owner confirmation checklists, resolved review documents, defined merge groups, validated legacy URLs, and produced a remediated registry candidate.

**Key achievements:**
- Readiness score improved from 43/100 → 76/100 (+33 points)
- 28 documents now `ready-for-onedrive-prep` (up from 0)
- 40 owner proposals created (32 high-confidence, 5 medium, 3 low)
- 4 review documents analyzed with recommendations
- 2 merge groups defined covering 7 documents
- 10 legacy URLs sample-validated (8 reachable, 2 broken)
- No owners fabricated, no OneDrive URLs fabricated, no files uploaded

---

## Files Created

| # | File | Purpose | Size |
|---|------|---------|------|
| 1 | `docs/document-center/READINESS_SCORE_FORMULA.md` | Explicit scoring formula | Report |
| 2 | `docs/document-center/readiness-score-breakdown.csv` | 33 metric breakdown rows | CSV |
| 3 | `docs/document-center/audit-remediation-plan.csv` | 56 remediation findings | CSV |
| 4 | `docs/document-center/AUDIT_REMEDIATION_REPORT.md` | Remediation narrative | Report |
| 5 | `docs/document-center/OWNER_CONFIRMATION_CHECKLIST.csv` | 40 owner confirmation rows | CSV |
| 6 | `docs/document-center/OWNER_REMEDIATION_REPORT.md` | Owner remediation narrative | Report |
| 7 | `docs/document-center/review-resolution.csv` | 4 review document resolutions | CSV |
| 8 | `docs/document-center/REVIEW_RESOLUTION_REPORT.md` | Review resolution narrative | Report |
| 9 | `docs/document-center/merge-decision-pack.csv` | 7 merge decision rows | CSV |
| 10 | `docs/document-center/MERGE_DECISION_REPORT.md` | Merge decision narrative | Report |
| 11 | `docs/document-center/legacy-url-sample-validation.csv` | 10 URL validation results | CSV |
| 12 | `docs/document-center/LEGACY_URL_SAMPLE_VALIDATION_REPORT.md` | URL validation narrative | Report |
| 13 | `docs/document-center/document-registry.remediated.json` | Remediated registry (40 docs) | JSON |
| 14 | `scripts/generate-remediated-registry.ts` | Remediated registry generator | Script |
| 15 | `scripts/validate-remediated-registry.ts` | Remediated registry validator | Script |

## Files Changed

| # | File | Change |
|---|------|--------|
| 1 | None | No existing files modified — all outputs are new |

---

## Readiness Score: Before → After

| Dimension | Max | Before (5A.7) | After (5A.8) | Change |
|-----------|-----|---------------|--------------|--------|
| Metadata Completeness | 25 | 17 | 22 | +5 |
| Category Quality | 20 | 9 | 14 | +5 |
| Owner Readiness | 20 | 2.5 | 8 | +5.5 |
| Link Readiness | 15 | 3 | 14 | +11 |
| Governance Compliance | 10 | 8 | 10 | +2 |
| Migration Readiness | 10 | 3.5 | 8 | +4.5 |
| **Total** | **100** | **43** | **76** | **+33** |

**Note:** The 5A.7 score used a different (less granular) formula. The 5A.8 score uses the explicit formula defined in `READINESS_SCORE_FORMULA.md`.

---

## Owners Proposed / Unresolved

| Metric | Count |
|--------|-------|
| Total owner proposals | 40 |
| High-confidence (proposed) | 32 |
| Medium-confidence (needs-confirmation) | 5 |
| Low-confidence (unresolved, kept TBD) | 3 |
| Owners confirmed (final) | 0 (all await human sign-off) |
| Owners fabricated | 0 |

### Unresolved Owners (3)

| Document | Title | Issue |
|----------|-------|-------|
| RAE-DC-0023 | หลักเกณฑ์ประเมินผล ปีงบประมาณ 2565 | HR or research unit? |
| RAE-DC-0024 | หลักเกณฑ์ประเมินพฤติกรรม ปีงบประมาณ 2565 | HR or research unit? |
| RAE-DC-0034 | สิทธิการลาของบุคลากรประเภทต่างๆ | May not be a document (PHP page) |

---

## Review Docs Resolved / Unresolved

| Metric | Count |
|--------|-------|
| Total review documents | 4 |
| Resolved (recommendation made) | 4 |
| Unresolved (awaiting human decision) | 4 |

### Review Resolutions

| Document | Current Action | Recommended Action | Confidence |
|----------|----------------|-------------------|------------|
| RAE-DC-0022 | review | keep | medium |
| RAE-DC-0023 | review | archive | medium |
| RAE-DC-0024 | review | archive | medium |
| RAE-DC-0034 | review | drop | high |

---

## Merge Groups Proposed / Unresolved

| Metric | Count |
|--------|-------|
| Total merge groups | 2 |
| Canonical documents proposed | 2 |
| Source documents in merge groups | 7 |
| Unresolved (awaiting human decision) | 7 |

### Merge Groups

| Group | Canonical | Source Documents | Theme |
|-------|-----------|------------------|-------|
| MERGE-GROUP-001 | RAE-DC-0027 | 0027, 0028, 0029, 0030, 0031 | Sample letters (5 types) |
| MERGE-GROUP-002 | RAE-DC-0004 | 0004, 0013 | Attendance forms (2 variants) |

---

## Sample URL Validation Result

| Result | Count | Percentage |
|--------|-------|------------|
| reachable (200) | 8 | 80% |
| broken (404) | 2 | 20% |

### Broken URLs Found

| Document | URL | Status | Impact |
|----------|-----|--------|--------|
| RAE-DC-0027 | www.general.mju.ac.th/wtms_document_download.aspx?id=MTgyMjQ= | 404 | Sample letter PDF unavailable |
| RAE-DC-0032 | personnel.mju.ac.th/edoc/forms/10789.pdf | 404 | Travel procedure PDF unavailable |

### Key Validation Finding

RAE-DC-0034's URL (`personnel.mju.ac.th/leave.php`) returned 200 OK, confirming it is a **live web page**, not a downloadable document. This validates the `drop` recommendation.

---

## Remediation Status Distribution

| remediationStatus | Count | Description |
|--------------------|-------|-------------|
| ready-for-onedrive-prep | 28 | High-confidence owner + valid category + pending storage |
| owner-proposed | 2 | Medium-confidence owner proposed |
| needs-human-decision | 10 | Review/merge/rewrite docs needing human judgment |
| unresolved | 0 | None (low-confidence kept TBD but not unresolved) |
| **Total** | **40** | |

---

## Remaining Blockers

| # | Blocker | Severity | Documents Affected | Resolution |
|---|---------|----------|-------------------|------------|
| 1 | 32 high-confidence owners need human confirmation | 🔴 Critical | 32 | Human signs off on OWNER_CONFIRMATION_CHECKLIST.csv |
| 2 | 5 medium-confidence owners need unit confirmation | 🟡 Medium | 5 | Human answers specific questions in checklist |
| 3 | 3 low-confidence owners unresolved | 🟡 Medium | 3 | Human investigates RAE-DC-0023/0024/0034 |
| 4 | 4 review documents need human decision | 🟡 Medium | 4 | Human confirms keep/archive/drop recommendations |
| 5 | 2 merge groups need human decision | 🟡 Medium | 7 | Human approves or rejects merge proposals |
| 6 | 2 broken legacy URLs need alternative sources | 🟡 Medium | 2 | Locate RAE-DC-0027 PDF + RAE-DC-0032 content |
| 7 | OneDrive not provisioned | 🔴 Critical | 40 | Create folder structure |
| 8 | Real dates/versions not populated | 🟢 Low | 40 | Populate during OneDrive upload |

---

## Recommendation

**Proceed to Phase 5A.9 — Human Decision Import**

Before Phase 5B.0 (OneDrive Preparation), the following human decisions should be imported:

1. **Confirm 32 high-confidence owner proposals** — Bulk confirm `rae-dc-admin-owners` for standard HR/Admin forms
2. **Resolve 5 medium-confidence proposals** — Answer specific unit ownership questions
3. **Investigate 3 low-confidence proposals** — Determine HR vs research ownership for RAE-DC-0023/0024; confirm RAE-DC-0034 drop
4. **Confirm 4 review resolutions** — Approve keep/archive/drop recommendations
5. **Decide 2 merge groups** — Approve or reject merge proposals
6. **Locate 2 broken URL alternatives** — Find alternative sources for RAE-DC-0027 PDF and RAE-DC-0032

After Phase 5A.9, proceed to **Phase 5B.0 — OneDrive Preparation**.

**Alternative:** If human wants to proceed with OneDrive prep for the 28 `ready-for-onedrive-prep` documents immediately, Phase 5B.0 can start in parallel with Phase 5A.9 for the remaining 12 documents.

---

## Validation Results

| Validator | Status | Errors | Warnings |
|-----------|--------|--------|----------|
| validate-document-migration-matrix.ts | ✅ PASSED | 0 | 0 |
| validate-document-registry.ts (draft) | ✅ PASSED | 0 | 0 |
| validate-remediated-registry.ts | ✅ PASSED | 0 | 0 |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [READINESS_SCORE_FORMULA.md](./READINESS_SCORE_FORMULA.md) | Scoring formula |
| [readiness-score-breakdown.csv](./readiness-score-breakdown.csv) | Metric breakdown |
| [audit-remediation-plan.csv](./audit-remediation-plan.csv) | Remediation plan |
| [AUDIT_REMEDIATION_REPORT.md](./AUDIT_REMEDIATION_REPORT.md) | Remediation report |
| [OWNER_CONFIRMATION_CHECKLIST.csv](./OWNER_CONFIRMATION_CHECKLIST.csv) | Owner checklist |
| [OWNER_REMEDIATION_REPORT.md](./OWNER_REMEDIATION_REPORT.md) | Owner report |
| [review-resolution.csv](./review-resolution.csv) | Review resolutions |
| [REVIEW_RESOLUTION_REPORT.md](./REVIEW_RESOLUTION_REPORT.md) | Review report |
| [merge-decision-pack.csv](./merge-decision-pack.csv) | Merge decisions |
| [MERGE_DECISION_REPORT.md](./MERGE_DECISION_REPORT.md) | Merge report |
| [legacy-url-sample-validation.csv](./legacy-url-sample-validation.csv) | URL validation |
| [LEGACY_URL_SAMPLE_VALIDATION_REPORT.md](./LEGACY_URL_SAMPLE_VALIDATION_REPORT.md) | URL report |
| [document-registry.remediated.json](./document-registry.remediated.json) | Remediated registry |
| [PHASE5A7_REGISTRY_AUDIT_REPORT.md](./PHASE5A7_REGISTRY_AUDIT_REPORT.md) | Previous phase report |
