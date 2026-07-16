# PXP-3 Link Validation Report

**Date**: 2026-07-16
**Validator**: `scripts/registry/verify-links.py`

## Summary

| Category | Count |
|---|---|
| Total URLs | 24 |
| VALID_AUTH_REQUIRED | 24 |
| VALID_PUBLIC | 0 |
| BROKEN | 0 |
| TIMEOUT | 0 |
| UNKNOWN | 0 |

## Classification Rules

Each URL was validated using the following rules:

- **VALID_AUTH_REQUIRED**: SharePoint hostname (`maejo365.sharepoint.com`), valid site path starting with `/sites/`, file extension present
- **VALID_PUBLIC**: Verified anonymous public link (none in this pilot)
- **BROKEN**: Invalid URL syntax, wrong hostname, or missing file extension
- **TIMEOUT**: Unreachable after timeout (none in this pilot)
- **UNKNOWN**: Unknown hostname or download mode (none in this pilot)

## Notes

All 24 pilot documents use `AUTHENTICATED_SHAREPOINT` download mode. These URLs require Maejo Microsoft 365 login. No anonymous sharing links were created for this pilot — consistent with the PXP-3 plan to defer bulk anonymous link creation.

All 24 authenticated links pass URL validation (correct hostname, valid SharePoint path, recognizable file extension).
