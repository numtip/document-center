# EA-11A — Registry Validation

**Date**: 2026-07-16  
**Evidence**: EA-11 reconciliation artifacts + repository/runtime inspection

---

## Summary

| Portal | Registry Source | Record Count | Connected to 627? |
|--------|-----------------|-------------:|:-----------------:|
| SharePoint Document Center page | **RAE Document Registry (SharePoint List)** | **627** | **YES** |
| SharePoint Registry All Items | **Live List** | **627** | **YES** |
| Six libraries | **File metadata columns + Registry sync** | **627 files** | **YES** |
| GitHub Pages preview | **`preview/data/public-registry.sample.json`** | **3** | **NO** |
| Next.js (external) | **Registry export JSON (planned)** | **Not deployed** | **NO** |

---

## SharePoint Registry (Production)

| Check | Result |
|-------|--------|
| Document count | **627** unique DocumentIDs |
| Duplicate DocumentIDs | **0** |
| Broken Storage URLs | **0** |
| Registry pages scanned | **2** (paginated `$top=500`) |
| Sync mechanism | EA-8 `AUTO_UPSERT` by DocumentID |
| List web part on DC page | Bound to Registry List ID `cecc20fe-ec26-44aa-bd71-73a32a5326fb` |

**Fields exposed on Document Center page**: Title, Document ID, Category, Updated Date, Storage URL, Status.

---

## GitHub Pages (Preview)

| Check | Result |
|-------|--------|
| HTTP status | **200** (site reachable) |
| Data file | `preview/data/public-registry.sample.json` |
| `preview_mode` | `true` |
| Record count | **3** |
| Search source | Client-side `filterDocuments()` in `preview/app.js` |
| Download links | `example.sharepoint.com` demo URLs only |
| Build guard | `scripts/build-preview.ts` rejects real SharePoint URLs |
| Purpose | **Preview/demo UI only** |

---

## Next.js Portal

| Check | Result |
|-------|--------|
| Code in this repo | **None** |
| Documented location | `github.com/numtip/rae-nextjs-main` |
| Intended data source | Scheduled Registry export JSON per `docs/m365/registry-export-contract.md` |
| Export mechanism | **Not implemented** (Phase M365-7 deferred) |
| Current record count | **N/A** — not verified deployed |

---

## Public URL Verification Matrix

| URL | Accessible | HTTP | Search | Categories | Listing | Downloads |
|-----|:----------:|:----:|:------:|:----------:|:-------:|:---------:|
| SharePoint DC page | Auth required | 200* | Native SP search | 6 Quick Links | Registry web part | Via Storage URL (auth) |
| Registry All Items | Auth required | 200* | List filter | Category column | 627 rows | Storage URL column |
| GitHub Pages | Public | 200 | Client filter (3 docs) | 3 categories | 3 cards | Demo links only |
| Next.js | Unknown | — | — | — | — | — |

\*Authenticated session required; anonymous HEAD returns 401/403 (EA-11 public access tests: 59/59 AUTH_REQUIRED).

---

## Data Flow (Confirmed)

```text
WTMS staging corpus
        ↓
SharePoint libraries (627 files)  ← file source of truth
        ↓
RAE Document Registry (627 rows)  ← metadata discovery
        ↓
SharePoint Document Center page   ← current production UI
        ↓
(planned) Registry export JSON → Next.js / public portal
```

GitHub Pages reads **static sample JSON** — not connected to Registry.

---

## Remaining Work Before Full Public Production

1. **Registry export automation** — populate Next.js / optional static portal with 627 records
2. **Deploy Next.js portal** — verify `rae-nextjs-main` deployment URL and record count
3. **Anonymous access policy** — decide sharing links vs authenticated-only (tenant constraint)
4. **Governance activation** — deferred (owners, RAE-DC groups, workflows)
