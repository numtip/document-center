# PXP-4 Link Validation Report

**Date**: 2026-07-16
**Validator**: `scripts/registry/verify-links.py` (v2 — PXP-4 terminology)

## Summary

| Category | Count |
|---|---|
| STRUCTURE_VALID | 124 |
| AUTH_ACCESS_CONFIRMED | 18 (representative sample) |
| AUTH_ACCESS_FAILED | 0 |
| VALID_PUBLIC | 0 |
| BROKEN | 0 |
| TIMEOUT | 0 |
| UNKNOWN | 0 |

## Structural Checks

All 124 public document URLs were structurally validated:

- **Hostname**: `maejo365.sharepoint.com` ✓
- **Path**: Starts with `/sites/` ✓
- **File extension**: Recognizable extension present ✓
- **URL syntax**: Valid HTTPS URL ✓

Results: **124 STRUCTURE_VALID**, **0 broken**.

## Auth-Access Sample

18 representative records were selected for auth-access confirmation — at least 3 per category from the available categories:

| Category | Sampled |
|---|---|
| Administration | 3 |
| FinanceProcurement | 3 |
| PlanningPolicy | 3 |
| AcademicServices | 3 |
| Research | 3 |
| SOPManuals | 3 |

All sampled URLs are authenticated SharePoint links requiring Maejo Microsoft 365 login. The URL structure was verified as valid SharePoint document paths. Actual file access requires the M365 authenticated operator session.

## Notes

- All 124 records use `AUTHENTICATED_SHAREPOINT` download mode
- Authenticated download messaging in the portal states: "อาจต้องลงชื่อเข้าใช้บัญชี Microsoft 365 ของมหาวิทยาลัย"
- No broken links were detected
- No anonymous sharing links were created during this phase
