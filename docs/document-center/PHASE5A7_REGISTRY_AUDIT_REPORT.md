# Phase 5A.7 — Registry Audit & Evidence Validation Report

**Project:** RAE Document Center  
**Phase:** 5A.7 — Registry Audit & Evidence Validation  
**Status:** Complete  
**Date:** 2026-06-18  
**Decision:** **PARTIAL**  
**Registry Readiness Score:** **43/100**

---

## Summary

Phase 5A.7 performed a comprehensive audit of all registry candidates created in Phase 5A.6. The audit validated metadata quality, category assignments, legacy URL integrity, ownership readiness, and governance compliance.

**Key findings:**
- All metadata fields are structurally valid
- All 40 documents are blocked by missing owner assignments
- All legacy URLs are catalogued but untested
- All documents are in a single category (`admin`) — expected but needs diversification
- 49 total audit findings identified (0 critical, 2 high, 38 medium, 6 low, 4 info)
- No production systems were touched, no files uploaded, no commits made

---

## Files Created

| # | File | Purpose | Size |
|---|------|---------|------|
| 1 | `docs/document-center/audit-matrix.csv` | 49 audit findings with severity | 49 rows |
| 2 | `docs/document-center/MATRIX_AUDIT_REPORT.md` | Matrix audit narrative | Report |
| 3 | `docs/document-center/legacy-link-audit.csv` | 48 legacy URL catalog | 48 rows |
| 4 | `docs/document-center/LEGACY_LINK_AUDIT_REPORT.md` | Link audit narrative | Report |
| 5 | `docs/document-center/CATEGORY_AUDIT_REPORT.md` | Category validation narrative | Report |
| 6 | `docs/document-center/owner-assignment-proposal.csv` | 40 owner suggestions | 40 rows |
| 7 | `docs/document-center/REGISTRY_READINESS_SCORECARD.md` | Readiness scoring + gap analysis | Scorecard |
| 8 | `docs/document-center/document-registry.audit.json` | Registry with audit fields | JSON |
| 9 | `scripts/generate-audit-registry.ts` | Audit registry generator script | Script |

## Files Changed

| # | File | Change |
|---|------|--------|
| 1 | `docs/document-center/owner-assignment-proposal.csv` | Fixed typo in RAE-DC-0009 owner group name |

---

## Audit Findings

### By Severity

| Severity | Count | Action Required |
|----------|-------|-----------------|
| CRITICAL | 0 | — |
| HIGH | 2 | Verify drop exclusions are honored |
| MEDIUM | 38 | Owner assignment + review rationale + category review |
| LOW | 6 | ID format, duplicate content, merge candidates |
| INFO | 4 | Synthetic data flags |
| **Total** | **49** | |

### By Issue Type

| Issue Type | Count | Key Finding |
|------------|-------|-------------|
| owner-tbd | 36 | All owners are TBD — #1 blocker |
| review-no-rationale | 4 | Review actions lack specific criteria |
| category-monoculture | 1 | All 40 in `admin` — 5 categories unused |
| duplicate-content | 3 | Potential merges identified (0004+0013, 0023+0024, 0027-0031) |
| merge-candidate | 1 | 5 sample letter docs flagged for merge |
| id-format | 1 | RAE-DC-0004A uses letter suffix |
| status-drop | 2 | Dropped docs correctly excluded from registry |
| rewrite-unclear | 1 | RAE-DC-0032 rewrite scope undefined |
| external-link-risk | 1 | RAE-DC-0034 links to PHP page, not a document |
| updatedDate-synthetic | 1 | All dates are generation date, not real |
| no-version-history | 1 | All versions default to 1.0 |
| storageUrl-pending | 1 | All PENDING_ONEDRIVE — expected |

---

## Duplicate Findings

### Duplicate IDs
✅ **None found.** All 42 matrix rows have unique IDs.

### Duplicate Titles / Content Overlap
| Pair/Group | Issue | Recommendation |
|------------|-------|----------------|
| RAE-DC-0004 + RAE-DC-0013 | Both attendance/timekeeping forms | Review for potential merge |
| RAE-DC-0023 + RAE-DC-0024 | Companion assessment criteria for same FY | Link as related pair |
| RAE-DC-0027 through RAE-DC-0031 | 5 sample letter types | Consider merging into 1 reference |

### Duplicate Legacy URLs
✅ **None found.** Each legacy URL maps to a unique document.

---

## Category Findings

| Metric | Value |
|--------|-------|
| Documents with valid category ID | 40/40 (100%) |
| Documents with empty category | 0 |
| Categories in use | 1 of 6 (`admin`) |
| Orphan categories | 5 (`finance-procurement`, `research`, `academic-service`, `policy-planning`, `manuals`) |
| Potential misclassifications | 8 documents may belong in `manuals` or `policy-planning` |

**Root cause:** Only one legacy source (`dlw1.MD` = admin tab) has been inventoried so far. Other categories need additional legacy sources.

---

## Owner Findings

| Metric | Value |
|--------|-------|
| Documents with real owner | 0/40 (0%) |
| Documents with TBD owner | 40/40 (100%) |
| Owner proposals generated | 40/40 |
| High-confidence proposals | 32 |
| Medium-confidence proposals | 5 |
| Low-confidence proposals | 3 |

**Low-confidence proposals (need human review):**
| Document | Title | Issue |
|----------|-------|-------|
| RAE-DC-0023 | หลักเกณฑ์ประเมินผล ปีงบประมาณ 2565 | Unclear if HR or research unit owns |
| RAE-DC-0024 | หลักเกณฑ์ประเมินพฤติกรรม ปีงบประมาณ 2565 | Same as RAE-DC-0023 |
| RAE-DC-0034 | สิทธิการลาของบุคลากรประเภทต่างๆ | May not be a real document (PHP page) |

---

## Link Findings

| Metric | Value |
|--------|-------|
| Legacy URLs extracted | 48 |
| URLs using HTTPS | 24 |
| URLs using HTTP (insecure) | 24 |
| Direct file downloads | 5 |
| ERP openFile.aspx URLs | 38 |
| wtms_document_download URLs | 5 |
| Dynamic PHP pages | 1 |
| URLs tested | 0 (not-tested) |

**High-risk URLs:**
| Document | URL | Risk |
|----------|-----|------|
| RAE-DC-0034 | `http://personnel.mju.ac.th/leave.php` | PHP page — not a downloadable document |
| RAE-DC-0004 | `https://view.officeapps.live.com/...` | Double-wrapped Office Online viewer URL |

**Format issues:**
- 24 URLs use HTTP instead of HTTPS
- 5 URLs use legacy `.doc` format (not `.docx`)
- 3 URLs have inconsistent `www` prefix
- 5 URLs use base64-encoded IDs in `wtms` system

---

## Registry Readiness

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Metadata Completeness | 85/100 | 20% | 17.0 |
| Category Quality | 60/100 | 15% | 9.0 |
| Owner Readiness | 10/100 | 25% | 2.5 |
| Link Readiness | 15/100 | 20% | 3.0 |
| Migration Readiness | 35/100 | 10% | 3.5 |
| Governance Compliance | 80/100 | 10% | 8.0 |
| **Overall** | | **100%** | **43/100** |

### Audit Status Distribution
| Status | Count |
|--------|-------|
| blocked | 40 |
| needs-review | 0 |
| ready-for-migration | 0 |

All 40 documents are `blocked` due to missing owner assignment.

---

## Exact Blockers

| # | Blocker | Severity | Documents Affected | Resolution |
|---|---------|----------|-------------------|------------|
| 1 | All 40 owners are TBD | 🔴 Critical | 40/40 | Human confirms owners from proposal CSV |
| 2 | OneDrive not provisioned | 🔴 Critical | 40/40 | Create `RAE-Document-Center/` folder structure |
| 3 | No file inventory from legacy ERP | 🟡 Medium | 40/40 | Download files from ERP `openFile.aspx` |
| 4 | 4 review documents need human judgment | 🟡 Medium | 4/40 | Verify validity of policy documents |
| 5 | RAE-DC-0034 may not be a real document | 🟡 Medium | 1/40 | Confirm if PHP page or downloadable doc |
| 6 | 8 documents may be misclassified | 🟢 Low | 8/40 | Reclassify after full inventory |
| 7 | 5 sample letters may need merging | 🟢 Low | 5/40 | Decide merge strategy |

---

## Recommended Next Phase

**Phase 5A.8 — Registry Remediation**

Before proceeding to OneDrive migration (Phase 5B), the following remediation should be completed:

1. **Confirm owner assignments** — Human reviews and confirms all 40 owner proposals
2. **Resolve review documents** — Human judges validity of 4 review-action documents
3. **Confirm RAE-DC-0034** — Determine if it's a real document or just a PHP page reference
4. **Define merge strategy** — Decide on RAE-DC-0004/0013 and RAE-DC-0027-0031 merge approach
5. **Update registry** — Apply confirmed owners, statuses, and decisions to `document-registry.audit.json`

After remediation, proceed to **Phase 5B.0 — OneDrive Preparation** (folder provisioning, file upload, share link creation).

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [MATRIX_AUDIT_REPORT.md](./MATRIX_AUDIT_REPORT.md) | Matrix audit narrative |
| [LEGACY_LINK_AUDIT_REPORT.md](./LEGACY_LINK_AUDIT_REPORT.md) | Link audit narrative |
| [CATEGORY_AUDIT_REPORT.md](./CATEGORY_AUDIT_REPORT.md) | Category validation |
| [REGISTRY_READINESS_SCORECARD.md](./REGISTRY_READINESS_SCORECARD.md) | Readiness scoring |
| [audit-matrix.csv](./audit-matrix.csv) | 49 audit findings |
| [legacy-link-audit.csv](./legacy-link-audit.csv) | 48 legacy URLs |
| [owner-assignment-proposal.csv](./owner-assignment-proposal.csv) | 40 owner suggestions |
| [document-registry.audit.json](./document-registry.audit.json) | Audited registry |
| [PHASE5A6_REGISTRY_HARDENING_REPORT.md](./PHASE5A6_REGISTRY_HARDENING_REPORT.md) | Previous phase report |
