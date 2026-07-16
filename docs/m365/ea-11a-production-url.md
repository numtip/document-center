# EA-11A — Production URL Decision

**Date**: 2026-07-16

---

## Official Production Portal

**URL users should bookmark (tenant-authenticated):**

```text
https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx
```

| Property | Value |
|----------|-------|
| **Portal type** | SharePoint Modern Site Page (Team site) |
| **Site** | สำนักวิจัยฯ — `/sites/msteams_54adc4` |
| **Page** | `RAE-Document-Center.aspx` (Page ID 2) |
| **Classification** | **PRODUCTION (operational)** |

---

## Supporting Production Endpoints

| Purpose | URL |
|---------|-----|
| Registry (full metadata) | `…/Lists/RAE%20Document%20Registry/AllItems.aspx` |
| Library browse (×6) | `…/{Library}/Forms/AllItems.aspx` |
| Site search | `…/_layouts/15/search.aspx` |

---

## Non-Production URLs

| URL | Classification | Why |
|-----|----------------|-----|
| `https://numtip.github.io/document-center/` | **PREVIEW** | 3 mock records; demo URLs only; README + build guard |
| `rae-nextjs-main` (external) | **STAGING / PLANNED** | Documented future public portal; not deployed from this repo |
| `docs/document-center/*.json` | **ARCHIVED / authoring** | Metadata authoring, not user portal |

---

## Explicit Answers

### 1. What URL should users bookmark?

**SharePoint Document Center page** (above). Requires Maejo365 authentication (private Team site).

### 2. Which URL is the official production portal?

**SharePoint `RAE-Document-Center.aspx`** — not GitHub Pages.

### 3. Is the production portal connected to the 627-document Registry?

**YES** — Registry List web part reads live SharePoint List (627 rows per EA-11 reconciliation). File downloads resolve to six libraries (627 files).

### 4. What remains before external/public production?

| Item | Status |
|------|--------|
| SharePoint operational portal | **Live** with 627 corpus |
| Anonymous public download | **Not enabled** — tenant auth required (EA-11 finding) |
| Registry export → GitHub/Next.js | **Not implemented** — P1 hardening backlog |
| Next.js public portal deployment | **Planned** — external repo, export contract defined |
| Governance activation | **Deferred** |

---

## Recommendation

Treat **SharePoint Document Center** as the current production portal for internal/organizational users. Treat **GitHub Pages** as UI preview only. Prioritize **Registry export automation** and **Next.js deployment** for a future internet-facing portal without changing the SharePoint file source of truth.
