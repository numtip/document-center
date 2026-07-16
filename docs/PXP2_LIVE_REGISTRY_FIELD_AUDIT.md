# PXP-2 Live Registry Field Audit

**Date**: 2026-07-16
**Source**: RAE Document Registry (SharePoint List)
**Site**: `https://maejo365.sharepoint.com/sites/msteams_54adc4`
**Access Method**: Playwright persistent browser profile + SharePoint REST API (Python requests)

---

## Field Mapping Table

| Live Registry Field | Internal Name | Type | Public Contract Field | Transformation | Required? | Risk / Notes |
|---|---|---|---|---|---|---|
| Title | `Title` | Text (single line) | `Title` | None | Yes | Straightforward mapping |
| Document ID | `Document_x0020_ID` | Text (single line) | `DocumentID` | None | Yes | Idempotency key; must be unique |
| Category | `Category` | Choice | `Category` | Map Thai display name to PXP-1 contract name (see category map below) | Yes | Live data uses Thai display names; 26 unique values vs 6 contract categories |
| Status | `Status` | Choice (draft, review, approved, published, current, obsolete, archived) | `Status` | Filter to `approved`/`published`/`current` only | Yes | Live data: ALL 627 records have `Status=draft` |
| Visibility | `Visibility` | Choice (public, internal, restricted, private) | `Visibility` | Filter to `public` only | Yes | Live data: ALL 627 records have `Visibility=internal` |
| Storage URL | `Storage_x0020_URL` | Hyperlink/URL | `StorageURL` | Extract `Url` property from SharePoint URL field | Yes | 627/627 have valid StorageURLs |
| DownloadMode | *Derived* | N/A | `DownloadMode` | Determined by URL analysis | Yes | All resolve to `AUTHENTICATED_SHAREPOINT` |
| Updated Date | `Updated_x0020_Date` | Date/Time | `UpdatedDate` | ISO 8601 format | Yes | Available in live data |
| ID | `ID` | Integer (internal) | N/A | Excluded | No | Internal SharePoint identifier |
| OwnerId | `OwnerId` | Lookup (integer) | N/A | Excluded | No | Internal user reference; privacy-sensitive |
| Legacy Source URL | `Legacy_x0020_Source_x0020_URL` | URL | N/A | Excluded | No | Internal legacy reference |
| PublicVisibility | `PublicVisibility` | Choice (PendingReview, Public, Internal, Restricted) | N/A | Excluded | No | ALL 627 empty (not populated) |
| DocumentStatus | `DocumentStatus` | Choice | N/A | Excluded | No | ALL 627 empty (not populated) |

---

## Category Name Mapping

| Live Registry Thai Name | PXP-1 Contract Value | Count |
|---|---|---|
| งานวิจัย/ประกาศงานวิจัย | Research | 160 |
| งานวิจัย/แบบฟอร์มงานวิจัย | Research | 85 |
| งานวิจัย/รายงานผลงานวิจัย | Research | 64 |
| งานวิจัย/ระเบียบการบริหารงานวิจัย | Research | 53 |
| งานวิจัย/ทุนวิจัย | Research | 46 |
| งานวิจัย/วิจัยสถาบัน | Research | 36 |
| research | Research | 33 |
| งานวิจัย/มาตรฐานการวิจัย | Research | 26 |
| แบบฟอร์มแหล่งทุนภายนอก | Research | 20 |
| งานคลังและพัสดุ | FinanceProcurement | 19 |
| งานวิจัย/คู่มือการวิจัย | Research | 14 |
| งานนโยบาย แผนและประกันคุณภาพ | PlanningPolicy | 10 |
| แบบฟอร์มงานบริการวิชาการ | AcademicServices | 10 |
| งานบริหารและธุรการ | Administration | 8 |
| คู่มือ | SOPManuals | 8 |
| งานวิจัย/ระบบสารสนเทศงานวิจัย | Research | 8 |
| งานวิจัย/คลินิกวิจัย | Research | 6 |
| งานวิจัย/การประเมินผลงานวิจัย | Research | 6 |
| แบบฟอร์มศูนย์ความเป็นเลิศ | Research | 4 |
| งานวิจัย/การจัดการความรู้ | Research | 3 |
| งานวิจัย | Research | 2 |
| บริหารจัดการ | Administration | 2 |
| งานบริการวิชาการ | AcademicServices | 1 |
| งานวิจัย/ฐานข้อมูลงานวิจัย | Research | 1 |
| งานวิจัย/ทรัพย์สินทางปัญญา | Research | 1 |
| งานวิจัย/แผนงานวิจัย | Research | 1 |

---

## Allowed Values (PXP-1 Contract)

### Status
- `approved` — 0 records in live data
- `published` — 0 records in live data
- `current` — 0 records in live data
- *(Live data: 627 have `draft`)*

### Visibility
- `public` — 0 records in live data
- *(Live data: 627 have `internal`)*

### Download Mode
- `AUTHENTICATED_SHAREPOINT` — all 627 StorageURLs
- `PUBLIC_SHAREPOINT_LINK` — 0 detected
- `PUBLIC_DISTRIBUTION_URL` — 0 detected

---

## Live Data Summary

| Metric | Value |
|---|---|
| Total records | 627 |
| Records with StorageURL | 627 (100%) |
| Records with Status=draft | 627 (100%) |
| Records with Visibility=internal | 627 (100%) |
| Records with Status in {approved,published,current} | 0 |
| Records with Visibility=public | 0 |
| PublicVisibility populated | 0 |
| DocumentStatus populated | 0 |
| Eligible for public export | **0** |

---

## Verdict

**LIVE REGISTRY ACCESSIBLE. FIELD MAPPING COMPLETE. ZERO RECORDS ELIGIBLE FOR PUBLIC EXPORT.**

The live Registry has not been prepared for public-facing use. All 627 records are marked as `draft`/`internal`. An administrative action is required to set appropriate Status and Visibility values before any records can appear in the public export.

This is NOT an export pipeline failure — the pipeline correctly detects and reports the eligibility state.
