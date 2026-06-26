# Legacy Link Audit Report — Phase 5A.7

**Project:** RAE Document Center  
**Phase:** 5A.7 — Legacy URL Validation  
**Date:** 2026-06-18  
**Source file:** `dlw1.MD` (legacy website HTML)

---

## Summary

Extracted **48 legacy URLs** from the source HTML across 40 document candidates. No URLs were mass-crawled — analysis is metadata-only.

| Metric | Value |
|--------|-------|
| Total URLs extracted | 48 |
| Unique document IDs mapped | 40 |
| Documents with multiple URLs | 8 |
| URLs using HTTPS | 24 |
| URLs using HTTP (insecure) | 24 |
| Direct file downloads (.pdf/.doc/.docx/.xls) | 5 |
| ERP `openFile.aspx` URLs | 38 |
| `wtms_document_download.aspx` URLs | 5 |
| Dynamic PHP page | 1 |
| Office Online viewer URLs | 1 |

**All URLs are `not-tested`** — no HTTP requests were made per mandatory rules.

---

## URL Domain Breakdown

| Domain | Count | Protocol | Notes |
|--------|-------|----------|-------|
| `erp.mju.ac.th` | 31 | Mixed (HTTPS: 19, HTTP: 12) | Primary ERP system — `openFile.aspx` |
| `www.e-manage.mju.ac.th` | 3 | HTTP only | Document management system |
| `e-manage.mju.ac.th` | 2 | HTTP only | Same system without `www` prefix |
| `www.admin.general.mju.ac.th` | 2 | HTTP only | Admin general site |
| `www.general.mju.ac.th` | 5 | HTTP only | General site — `wtms_document_download.aspx` |
| `personnel.mju.ac.th` | 4 | HTTP only | Personnel site — direct file downloads |
| `researchex.rae.mju.ac.th` | 2 | HTTP only | RAE research site — direct .docx files |
| `view.officeapps.live.com` | 1 | HTTPS | Office Online viewer wrapping ERP URL |

---

## Suspicious / Risky URLs

### 🔴 HIGH RISK

| Document | URL | Issue |
|----------|-----|-------|
| RAE-DC-0034 | `http://personnel.mju.ac.th/leave.php` | **Dynamic PHP page, not a document download.** This is a web page, not a file. Cannot be migrated to OneDrive as-is. May need to be excluded or converted to a reference document pointing to the live URL. |

### 🟡 MEDIUM RISK

| Document | URL | Issue |
|----------|-----|-------|
| RAE-DC-0004 | `https://view.officeapps.live.com/op/view.aspx?src=...` | **Double-wrapped URL** — Office Online viewer wrapping an ERP URL. The viewer URL may break if the underlying ERP URL changes. Should extract the direct ERP URL instead. |
| RAE-DC-0017 | `http://personnel.mju.ac.th/edoc/forms/13045.doc` | **Legacy `.doc` format** — not `.docx`. May require conversion. |
| RAE-DC-0021 | `http://personnel.mju.ac.th/edoc/forms/23707.doc` | **Legacy `.doc` format** — not `.docx`. May require conversion. |
| RAE-DC-0006 | `http://personnel.mju.ac.th/edoc/tor/02_assessment_support_2563.xls` | **Legacy `.xls` format** — direct file download from personnel site. |
| RAE-DC-0039 | `http://researchex.rae.mju.ac.th/form/05-report1.docx` | **RAE research site** — direct .docx file. May not be accessible outside campus network. |
| RAE-DC-0040 | `http://researchex.rae.mju.ac.th/form/06-report1.docx` | **RAE research site** — direct .docx file. Same accessibility concern. |

### 🟢 LOW RISK

| Issue | Count | Documents |
|-------|-------|-----------|
| HTTP instead of HTTPS | 24 | Multiple — all `personnel.mju.ac.th`, `general.mju.ac.th`, `e-manage.mju.ac.th`, `admin.general.mju.ac.th` domains |
| Inconsistent `www` prefix | 3 | RAE-DC-0009 vs RAE-DC-0011 (same ERP, different prefix) |
| Inconsistent `www` prefix | 2 | RAE-DC-0013 (e-manage vs www.e-manage) |

---

## Duplicate URL Analysis

✅ **No duplicate URLs found.** Each URL maps to a unique document ID and file version.

### Near-Duplicate Patterns

| Pattern | Documents | Notes |
|---------|-----------|-------|
| Same ERP domain, sequential IDs | RAE-DC-0014 + RAE-DC-0015 | Leave forms — different `id` params |
| Same ERP domain, sequential IDs | RAE-DC-0018 + RAE-DC-0019 | Resignation forms — different `id` params |
| Same `wtms_document_download` pattern | RAE-DC-0027 through RAE-DC-0031 | Sample letters — different `id` params |

---

## URL Format Issues

| Issue | Count | Example |
|-------|-------|---------|
| HTTP instead of HTTPS | 24 | `http://erp.mju.ac.th/...` |
| `www` prefix inconsistency | 5 | `http://erp.mju.ac.th/` vs `http://www.erp.mju.ac.th/` |
| `e-manage` prefix inconsistency | 5 | `http://e-manage.mju.ac.th/` vs `http://www.e-manage.mju.ac.th/` |
| Base64-encoded IDs in `wtms` URLs | 5 | `id=MzY1Njkx` (base64) |
| Query string encoding | 1 | `&amp;` HTML entity in URL (from HTML source) |

---

## Migration Implications

### OneDrive Upload Strategy

All 40 documents will need to be **downloaded from their legacy URLs and re-uploaded to OneDrive**. The legacy URLs will NOT be used as `storageUrl` in the production registry.

| Download Source | Document Count | Notes |
|-----------------|----------------|-------|
| ERP `openFile.aspx` | 31 | Requires ERP access — may need authenticated download |
| `wtms_document_download.aspx` | 5 | May require session/cookie |
| `personnel.mju.ac.th` direct files | 4 | Direct downloads — simpler |
| `researchex.rae.mju.ac.th` direct files | 2 | Direct downloads — simpler |

### Files Requiring Format Conversion

| Document | Current Format | Target |
|----------|----------------|--------|
| RAE-DC-0017 | `.doc` | `.docx` |
| RAE-DC-0021 | `.doc` | `.docx` |
| RAE-DC-0006 | `.xls` | `.xlsx` |

---

## Recommendations

1. **RAE-DC-0034 (leave.php)** — Decide: is this a reference document (keep as-is with link) or does it need to be converted to a downloadable PDF? Currently it's a dynamic web page, not a file.

2. **All HTTP URLs** — When re-uploading to OneDrive, ensure the new share links use HTTPS.

3. **RAE-DC-0004 double-wrapped URL** — When downloading, use the direct ERP URL, not the Office Online viewer wrapper.

4. **Legacy `.doc` files** — Convert to `.docx` during upload process for modern compatibility.

5. **ERP authenticated access** — Confirm that ERP `openFile.aspx` URLs can be bulk-downloaded, or if manual download is required.

---

## Detailed Audit

Full URL-by-URL audit available in: `legacy-link-audit.csv`
