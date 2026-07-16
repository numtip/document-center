# Document Center v1.0 — Production Freeze

**Release Version**: 1.0.0  
**Freeze Date**: 2026-07-16  
**Status**: PRODUCTION FROZEN — PROJECT COMPLETED

---

## Executive Summary

The RAE Document Center Version 1.0 production release freezes a fully migrated document corpus of **627 READY files** into Microsoft 365 SharePoint, synchronized to the **RAE Document Registry**, and exposed through the operational **SharePoint Document Center** portal. Migration phases EA-6 through EA-11 are complete. Governance workflows remain deferred by design. GitHub Pages serves a **3-record demo preview only**.

---

## Architecture

```text
WTMS staging corpus (archived)
        ↓
SharePoint document libraries (627 files — source of truth)
        ↓
RAE Document Registry (627 rows — metadata discovery)
        ↓
SharePoint Document Center page (production UI)
        ↓
(planned) Registry export → Next.js public portal
```

**Site**: `https://maejo365.sharepoint.com/sites/msteams_54adc4`

---

## Production URL

```text
https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx
```

Requires Maejo365 authentication (private Team site).

---

## Repository

| Item | Value |
|------|-------|
| Repository | `G:\ProjectAI\document-center` |
| Remote | `https://github.com/numtip/document-center.git` |
| Branch | `main` |
| Release commit | Tagged as `document-center-v1.0.0` on `main` |
| Tag | `document-center-v1.0.0` |

---

## Migration Statistics

| Metric | Count |
|--------|------:|
| Manifest READY corpus | 627 |
| SharePoint files (unique DocumentID) | 627 |
| Registry rows (unique DocumentID) | 627 |
| EA-6 pilot | 6 |
| EA-7A expanded | 25 |
| EA-9 controlled scale | 100 |
| EA-10 remaining corpus | 496 |
| Duplicate DocumentIDs | 0 |
| Broken Storage URLs | 0 |
| Migration failures (final) | 0 |

**Approved libraries**: Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals

---

## Known Limitations

| Limitation | Impact |
|------------|--------|
| GitHub Pages shows **3 demo records** only | Not production portal |
| Anonymous file download requires tenant auth | AUTH_REQUIRED for unauthenticated access |
| Registry export to Next.js not implemented | External public portal pending |
| SharePoint search indexing lag | PENDING_INDEX acceptable; direct URLs resolve |
| Owner fields remain `TBD` | Display placeholder until governance |
| Document status `draft` / visibility `internal` in Registry | Governance deferred |

---

## Deferred Governance

The following remain **DEFERRED_GOVERNANCE** and are **not** activated in v1.0:

- Authoritative category owners
- RAE-DC group membership
- ALLOW/DENY identity testing
- Production permission enforcement
- Power Automate governance workflows
- Owner assignment (`TBD` → named people)

---

## Support Scope

**In scope (v1.0)**:

- SharePoint file access via six libraries
- Registry metadata discovery
- Document Center page browsing and native search
- Registry sync via `_ea8_registry_sync.py --sync-all`
- Operational runbook procedures

**Out of scope (v1.0)**:

- Additional WTMS migration batches
- Architecture redesign
- Governance activation
- Anonymous public portal without export pipeline

---

## Future Roadmap (Post v1.0 — Not Started)

| Phase | Description |
|-------|-------------|
| Production Hardening | Registry export automation, monitoring, link validation |
| Next.js portal | Deploy `rae-nextjs-main` with 627-record export |
| Governance Activation | Owners, groups, workflows (EA-6C deferred) |
| Public access policy | Sharing links vs authenticated-only decision |

---

## GitHub Pages Validation (Preview Environment)

| Check | Result |
|-------|--------|
| URL | `https://numtip.github.io/document-center/` |
| Deployment | Active via `.github/workflows/pages.yml` → `gh-pages` branch |
| Data source | `preview/data/public-registry.sample.json` |
| Record count | **3** demo records |
| `preview_mode` | `true` |
| Storage URLs | `example.sharepoint.com` (mock) |
| Classification | **PREVIEW / DEMO — not production** |

**Recommendation**: Keep GitHub Pages as the **Preview Environment** for UI blueprint validation. Production corpus (627 records) is served only via SharePoint + Registry.

---

## Related Artifacts

- `docs/release/ARCHITECTURE_BASELINE_v1.0.md`
- `docs/release/PRODUCTION_ACCEPTANCE_CERTIFICATE.md`
- `docs/release/OPERATION_RUNBOOK_v1.0.md`
- `docs/release/PROJECT_CLOSEOUT_REPORT.md`
- `docs/release/RELEASE_NOTES_v1.0.md`
- `docs/m365/ea-11a-portal-discovery.md`
