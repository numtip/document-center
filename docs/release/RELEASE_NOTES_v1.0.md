# Release Notes — Document Center v1.0.0

**Release**: `document-center-v1.0.0`  
**Date**: 2026-07-16  
**Status**: Production Frozen

---

## Overview

Version 1.0.0 completes the RAE Document Center migration project. All **627 READY** documents from the WTMS staging corpus are uploaded to SharePoint, synchronized to the RAE Document Registry, and accessible through the SharePoint Document Center production portal.

---

## What's Included

### Migration (Complete)

- 627 files across 6 SharePoint document libraries
- 627 Registry rows with Storage URLs
- 0 duplicate DocumentIDs
- 0 broken Storage URLs
- Idempotent Registry sync (`AUTO_UPSERT`)

### Production Portal

- SharePoint Document Center page on Maejo365 Team site
- Registry List as metadata discovery layer
- Native SharePoint search and library navigation

### Preview Environment

- GitHub Pages static preview at `https://numtip.github.io/document-center/`
- **3 demo records** from `preview/data/public-registry.sample.json`
- `preview_mode: true` — **not production**

### Documentation Package

- Production freeze manifest
- Architecture baseline v1.0
- Production acceptance certificate
- Operation runbook v1.0
- Project closeout report

---

## Production URLs

| Environment | URL |
|-------------|-----|
| **Production** | `https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx` |
| **Preview (demo)** | `https://numtip.github.io/document-center/` |

---

## GitHub Pages Validation (EA-12 Part F)

| Check | Result |
|-------|--------|
| Deployment | Active (`.github/workflows/pages.yml` → `gh-pages` branch) |
| Data source | `preview/data/public-registry.sample.json` |
| Record count | **3** (RAE-DC-0001, RAE-DC-0004, RAE-DC-0005) |
| `preview_mode` | `true` |
| Storage URLs | `example.sharepoint.com` mock links |
| Classification | **PREVIEW / DEMO only** |

**Recommendation**: Retain GitHub Pages as the **Preview Environment** for UI blueprint validation. Do not treat it as the production document corpus.

---

## Known Limitations

- Governance workflows deferred (owners, groups, ALLOW/DENY)
- Anonymous download requires Maejo365 authentication
- Registry export to Next.js public portal not implemented
- GitHub Pages disconnected from 627-record Registry

---

## Upgrade / Migration Notes

No upgrade path from v1.0 is defined. Future changes require:

1. Amendment to `ARCHITECTURE_BASELINE_v1.0.md`
2. New EA phase approval
3. Updated acceptance certificate

---

## Contributors & Phases

EA-6 through EA-12 migration and QA phases documented in `docs/m365/` and `.migration/rae-wtms/`.
