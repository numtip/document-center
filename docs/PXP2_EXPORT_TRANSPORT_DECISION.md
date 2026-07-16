# PXP-2 Export Transport Decision

**Date**: 2026-07-16

---

## Chosen Mechanism: Playwright + SharePoint REST API

**Approach**: Use the existing Playwright persistent browser profile to authenticate and query the RAE Document Registry via SharePoint REST API.

**Rationale**: This mechanism is already proven in production (EA-8, EA-9, EA-10, EA-11). It requires no new Azure App Registration, no Graph API permissions changes, and no additional tenant configuration.

---

## Alternatives Considered

| Alternative | Reason Not Chosen |
|---|---|
| Power Automate export flow | No existing flow in tenant (confirmed: "Power Automate staff-upload (WF-01 — ยังไม่มี flow ใน tenant)") |
| Microsoft Graph API | Requires Graph app registration + admin consent; existing access uses SharePoint REST via browser session |
| CSV export from Microsoft Lists | Manual step; not automatable; requires browser interaction |
| Manual browser export | Not reproducible; no CI/CD integration; error-prone for 627 records |
| Graph `sites/{site-id}/lists/{list-id}/items` | Requires site/list ID discovery; same REST endpoint as chosen approach but needs app registration |

---

## Authentication Model

| Property | Value |
|---|---|
| Authentication method | Playwright persistent browser profile (`.browser-profile/m365/`) |
| Session type | M365 organizational sign-in (cookie-based) |
| Token refresh | Automatic via browser session cookies |
| MFA handling | One-time interactive login; profile persists across runs |
| Headless mode | Supported (used in EA-11 reconciliation) |

---

## Pagination Method

- **API**: SharePoint REST `/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items`
- **Parameters**: `$top=500`, `$skip=N`
- **Fields selected**: `Id,Title,Document_x0020_ID,Category,Status,Visibility,Storage_x0020_URL,Updated_x0020_Date`
- **Max page size**: 500 (SharePoint REST limit)
- **Expected pages**: 2 (500 + 127 = 627)
- **Proven**: EA-11 reconciliation confirmed 2 pages

---

## Retry Policy

| Condition | Action |
|---|---|
| HTTP 429 (throttle) | Wait 30s, retry up to 3 times |
| HTTP 5xx | Wait 10s, retry up to 3 times |
| Network timeout | Wait 5s, retry up to 2 times |
| Auth session expired | Re-authenticate via browser profile |

---

## Rate-Limit Behavior

SharePoint REST API basic limits:
- 60 requests per minute per app principal (higher for browser sessions)
- Pagination requests are well within limits
- Export runs as a single sequential scan — no burst behavior

---

## Secret Handling

| Secret | Storage |
|---|---|
| Browser session cookies | `.browser-profile/m365/` — gitignored |
| Site URL | Hardcoded in scripts (not sensitive) |
| No tokens, passwords, or API keys | N/A |

---

## Scheduled Execution Suitability

| Requirement | Status |
|---|---|
| Unattended headless mode | Supported (headless=True) |
| Profile reusability | Verified (profile persists across runs) |
| CI/CD integration | Requires GitHub Actions runner with browser profile injection |
| Secret management | GitHub secrets for auth profile (recommended but not required today) |

**Current limitation**: Full unattended CI/CD export requires the browser profile to be available on the runner. For now, export is designed for local/manual execution with `workflow_dispatch` triggers.

---

## Known Limitations

1. **Browser profile dependency**: Export requires an authenticated browser profile initialized via interactive login
2. **No anonymous access**: All Registry reads flow through the browser session
3. **SharePoint REST pagination**: 500-item page limit requires pagination
4. **No Power Automate fallback**: No existing flow to extend

---

## Verdict

**SELECTED: Playwright + SharePoint REST API (existing proven mechanism)**
**No new tenant configuration required.**
