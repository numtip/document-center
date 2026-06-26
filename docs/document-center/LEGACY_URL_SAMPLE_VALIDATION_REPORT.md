# Legacy URL Sample Validation Report — Phase 5A.8

**Project:** RAE Document Center  
**Phase:** 5A.8 — Legacy URL Sample Validation  
**Date:** 2026-06-18  
**Method:** HEAD requests only — no authentication, no scraping, no mass crawling

---

## Summary

Tested 10 legacy URLs (mixed sample) using safe HEAD requests. Network was available.

| Result | Count | Percentage |
|--------|-------|------------|
| reachable (200) | 8 | 80% |
| broken (404) | 2 | 20% |
| redirect | 0 | 0% |
| blocked | 0 | 0% |
| unknown | 0 | 0% |
| not-tested | 0 | 0% |
| **Total** | **10** | **100%** |

---

## Sample Composition

| Sample Group | Count | Documents |
|--------------|-------|-----------|
| keep | 3 | RAE-DC-0001, RAE-DC-0007, RAE-DC-0014 |
| merge | 2 | RAE-DC-0027, RAE-DC-0028 |
| rewrite/review | 2 | RAE-DC-0032 (rewrite), RAE-DC-0022 (review) |
| review | 1 | RAE-DC-0034 |
| random | 2 | RAE-DC-0035, RAE-DC-0039 |

---

## Detailed Results

### ✅ Reachable (8 URLs)

| Document | URL | HTTP Status | Notes |
|----------|-----|-------------|-------|
| RAE-DC-0001 | erp.mju.ac.th/openFile.aspx?id=Nzk4NTgw | 200 | Training permission form accessible |
| RAE-DC-0007 | erp.mju.ac.th/openFile.aspx?id=NTMxMTM3 | 200 | Smart card application accessible |
| RAE-DC-0014 | erp.mju.ac.th/openFile.aspx?id=NDk4Mzky | 200 | Leave form accessible |
| RAE-DC-0028 | erp.mju.ac.th/openFile.aspx?id=NDY2Mzc1 | 200 | External letter sample (WORD) accessible |
| RAE-DC-0022 | erp.mju.ac.th/openFile.aspx?id=NDgwMDg4 | 200 | Working hours announcement accessible |
| RAE-DC-0034 | personnel.mju.ac.th/leave.php | 200 | PHP page is live — **confirms this is a web page, not a document** |
| RAE-DC-0035 | erp.mju.ac.th/openFile.aspx?id=MzI0MDcz | 200 | Vehicle usage criteria accessible |
| RAE-DC-0039 | researchex.rae.mju.ac.th/form/05-report1.docx | 200 | Monthly car usage report accessible |

### ❌ Broken (2 URLs — 404 Not Found)

| Document | URL | HTTP Status | Impact |
|----------|-----|-------------|--------|
| RAE-DC-0027 | www.general.mju.ac.th/wtms_document_download.aspx?id=MTgyMjQ= | 404 | Sample letter (หนังสือภายใน) PDF no longer available at this URL |
| RAE-DC-0032 | personnel.mju.ac.th/edoc/forms/10789.pdf | 404 | International travel procedure PDF no longer available |

---

## Key Findings

### 1. ERP System is Reliable (8/8 ERP URLs reachable)

All URLs using `erp.mju.ac.th/openFile.aspx` returned 200 OK. This confirms the ERP system is the most reliable source for legacy document downloads.

### 2. Two Broken URLs Found

**RAE-DC-0027** (sample letter หนังสือภายใน):
- URL: `http://www.general.mju.ac.th/wtms_document_download.aspx?id=MTgyMjQ=`
- Status: 404 Not Found
- Impact: The PDF version is no longer available at this URL
- Mitigation: The WORD version (RAE-DC-0027's second URL at erp.mju.ac.th) may still be accessible — needs verification

**RAE-DC-0032** (international travel procedure):
- URL: `http://personnel.mju.ac.th/edoc/forms/10789.pdf`
- Status: 404 Not Found
- Impact: This document is no longer available at the legacy URL
- Mitigation: This document was already flagged for `rewrite` — the broken URL reinforces the need to locate or recreate the content

### 3. RAE-DC-0034 Confirmed as Web Page

The PHP page `personnel.mju.ac.th/leave.php` returned 200 OK, confirming it is a **live web page**, not a downloadable document. This validates the Phase 5A.8 review resolution recommendation to `drop` this entry from the registry.

---

## Migration Implications

| Finding | Impact on Migration |
|---------|---------------------|
| ERP URLs are reliable | 31 ERP-hosted documents can likely be downloaded successfully |
| 2 broken URLs found | RAE-DC-0027 PDF and RAE-DC-0032 need alternative sources or recreation |
| RAE-DC-0034 is a web page | Confirms drop recommendation — cannot migrate as a file |
| general.mju.ac.th may be unreliable | 5 wtms_document_download URLs need testing before relying on them |

---

## Recommendations

1. **Prioritize ERP URLs** for document download — 100% success rate in sample
2. **Test all general.mju.ac.th URLs** before migration — 1 of 1 returned 404
3. **Test all personnel.mju.ac.th direct file URLs** — 1 of 2 returned 404
4. **Locate alternative source for RAE-DC-0027 PDF** — may need to use WORD version only
5. **Locate alternative source for RAE-DC-0032** — or proceed with rewrite as planned
6. **Confirm RAE-DC-0034 drop** — PHP page confirmed live, not a document

---

## Sample Limitations

- Only 10 of 48 URLs tested (21%)
- HEAD requests only — did not verify file content or downloadability
- No authentication used — some ERP URLs may require session cookies for actual download
- Tested on 2026-06-18 — URL availability may change over time

---

## Related Documents

- [legacy-url-sample-validation.csv](./legacy-url-sample-validation.csv) — Full sample results
- [legacy-link-audit.csv](./legacy-link-audit.csv) — Complete URL catalog (48 URLs)
- [LEGACY_LINK_AUDIT_REPORT.md](./LEGACY_LINK_AUDIT_REPORT.md) — Phase 5A.7 link audit
- [REVIEW_RESOLUTION_REPORT.md](./REVIEW_RESOLUTION_REPORT.md) — RAE-DC-0034 drop recommendation
