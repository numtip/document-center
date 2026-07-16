# PXP-2 Download Link Assessment

**Date**: 2026-07-16

---

## Approach

Download modes are determined dynamically from StorageURL characteristics since no explicit `DownloadMode` field exists in the live Registry.

### Resolution Rules

1. **`AUTHENTICATED_SHAREPOINT`** — Default for all `maejo365.sharepoint.com` URLs. These are organizational SharePoint links requiring M365 authentication.
2. **`PUBLIC_SHAREPOINT_LINK`** — URLs containing `guest` or `anonymous` tokens (anonymous sharing links).
3. **`PUBLIC_DISTRIBUTION_URL`** — Reserved for known public CDN/distribution URLs (none currently available).

### Record-Level Assessment

The export pipeline evaluates each StorageURL at mapping time. The assessment is recorded in the export audit under `download_mode_breakdown`. Expected results for a full 627-record export:

| Download Mode | Expected Count | Notes |
|---|---|---|
| `AUTHENTICATED_SHAREPOINT` | 627 (all eligible) | All migrated documents stored in SharePoint libraries |
| `PUBLIC_SHAREPOINT_LINK` | 0 | No anonymous sharing links created during migration |
| `PUBLIC_DISTRIBUTION_URL` | 0 | No public CDN distribution configured |

### Privacy Verification

- No StorageURL is claimed as public based solely on hostname or path.
- SharePoint URLs are classified as `AUTHENTICATED_SHAREPOINT` (requiring organizational sign-in).
- No auto-creation of anonymous sharing links is performed.
- Any record without a valid StorageURL is excluded from export.

### Limitation

Only `AUTHENTICATED_SHAREPOINT` mode is verifiable without live SharePoint access to test sharing permissions. Public link verification requires:
- Opening each URL in an anonymous browser session
- Confirming no authentication prompt appears
- Confirming file content is accessible

This is documented as a constraint in the link validation report.
