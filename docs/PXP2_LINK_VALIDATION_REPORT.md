# PXP-2 Link Validation Report

**Date**: 2026-07-16
**Pipeline**: pxp2-export-live-registry

---

## Approach

Link validation for the public export is performed in two stages:

### Stage 1: Syntactic Validation (Pipeline)

During the export pipeline, each StorageURL is validated for:

- HTTPS scheme presence
- Non-empty value
- Expected SharePoint tenant hostname (`maejo365.sharepoint.com`)

Results are recorded in the export audit.

### Stage 2: Access Validation (Manual / QA)

Cannot be fully automated because:

1. **Authenticated URLs** (`AUTHENTICATED_SHAREPOINT`) require M365 organizational sign-in. Automated validation would need session cookies.
2. **No public URLs** exist in the current export (0 eligible records).
3. **Rate limiting**: SharePoint may throttle repeated HTTP checks.

---

## Current Export Results

Since **0 records** are eligible for public export (all 627 have visibility=`internal`), there are no StorageURLs in the public export to validate.

---

## Link Categories

| Category | Definition | Count in Export |
|---|---|---|
| `VALID_PUBLIC` | Anonymous access returns HTTP 200 | 0 |
| `VALID_AUTH_REQUIRED` | SharePoint URL (requires sign-in) | 0 (in export) |
| `REDIRECT_VALID` | Redirects to valid destination | 0 |
| `BROKEN` | HTTP 404 or connection error | 0 |
| `TIMEOUT` | Request timed out | 0 |
| `RATE_LIMITED` | SharePoint throttled the check | 0 |
| `UNKNOWN` | Could not be determined | 0 |

---

## Authenticated Link Spot Check

During EA-11 reconciliation, a sample of 20 StorageURLs was verified to return HTTP 200 (authenticated). All StorageURLs in the Registry (627/627) are valid SharePoint library URLs.

---

## Privacy Note

No StorageURL is claimed as public based solely on hostname. SharePoint URLs on `maejo365.sharepoint.com` are classified as `AUTHENTICATED_SHAREPOINT` only.

---

## Verdict

**NO LINK VALIDATION ISSUES** — 0 public links to validate.
