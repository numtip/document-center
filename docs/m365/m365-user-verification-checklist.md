# M365 Tenant Verification Checklist — User Guide

**Phase:** EA-1B — Tenant Evidence Collection  
**Status:** Checklist created — evidence collection not yet started  
**Last updated:** 2026-07-14  
**Estimated time:** 30–45 minutes

---

## 1. Purpose

This checklist guides you through the minimum tenant verification sequence. Each step tells you exactly where to click, what to observe, and what evidence to return.

**Return evidence to the Agent in small batches.** Screenshots can be captured and shared one section at a time.

### Before You Start

- You need a Maejo University M365 account with **at least basic access** (no admin rights required initially)
- You may need admin assistance for steps marked with 🔐 (admin)
- Do NOT upload documents, create lists, create flows, or register apps
- **Blur/crop out all personal information** from screenshots

---

## 2. Step 1 — Microsoft 365 Account / License Context

**Goal:** Confirm you can access the M365 environment.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 1.1 | Go to https://www.office.com | Sign in with your MJU account | M365 home page loads with app icons | Screenshot showing the app launcher |
| 1.2 | Click the app launcher (waffle icon, top-left) | — | List of available apps (Word, Excel, SharePoint, Teams, etc.) | Screenshot of app list |
| 1.3 | Click "My Account" (profile picture → My account) → Subscriptions | — | License information and available services | Screenshot (blur email, name) |
| 1.4 | Note your tenant URL | It appears in the browser address bar (e.g., `mju.sharepoint.com`, `mju.onmicrosoft.com`) | Tenant domain | Text return: tenant URL |

**Sensitive info:** Blur your name, email, and profile picture from screenshots.

---

## 3. Step 2 — SharePoint Online

**Goal:** Verify SharePoint site access and creation capability.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 2.1 | Office.com → SharePoint app (or URL: https://[tenant].sharepoint.com) | — | SharePoint home page loads | Screenshot showing SharePoint home |
| 2.2 | On the left, click "Sites" → "Active sites" (or scroll to see "Followed sites") | — | List of SharePoint sites you can access | Screenshot showing site list |
| 2.3 | Click "Create site" (if visible) OR navigate to SharePoint admin center | — | Site creation options OR "Access denied" message | Screenshot |
| 2.4 | Click on any existing site (or ask IT to create a test site) | — | Site loads with navigation | Screenshot of site home page |
| 2.5 | Click Settings (gear icon) → "Site contents" | — | List of libraries and lists on the site | Screenshot |
| 2.6 | Click "New" → "Document library" | In the dialog, note available options | Library creation dialog | Screenshot (do NOT click Create) |
| 2.7 | Press Escape or Cancel | — | — | — |

**Screenshots needed:** 2.1, 2.2, 2.3, 2.5, 2.6  
**Sensitive info:** Blur site names that reveal sensitive project names.

---

## 4. Step 3 — Microsoft Lists

**Goal:** Verify Microsoft Lists access.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 3.1 | Office.com → Lists app (or URL: https://[tenant].sharepoint.com/_layouts/15/pointpub.aspx) | — | Lists app loads | Screenshot |
| 3.2 | Click "New list" | — | List creation options (Blank list, From Excel, From existing list) | Screenshot |
| 3.3 | Click "Blank list" | — | List configuration form (Name, Description, Color, Icon) | Screenshot (do NOT create) |
| 3.4 | Press Cancel | — | — | — |
| 3.5 | If any existing lists are visible, click one to open it | Click "+ Add column" (or "Add column") | Available column types (Single text, Choice, Person/Group, etc.) | Screenshot of column type options |

**Screenshots needed:** 3.1, 3.2, 3.3, 3.5  
**Sensitive info:** None expected.

---

## 5. Step 4 — External Sharing Behavior (CRITICAL)

**Goal:** Determine if anonymous sharing links are permitted.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 4.1 🔐 | Go to https://admin.microsoft.com → SharePoint admin center → Policies → Sharing | — | External sharing page | Screenshot showing sharing settings |
| 4.2 | Look for "Anyone" (anonymous) links setting | — | Allowed / Not allowed / Limited to specific domains | Text: is "Anyone" sharing allowed? |
| 4.3 | Look for link expiration policy | — | Number of days before anonymous links expire | Text: link expiration days |
| 4.4 🔐 | If you have a test file in any site library, click its ⋯ menu → Share | Enter "Anyone with the link" (if available) | Available link types in the Share dialog | Screenshot of Share dialog |

**If you don't have admin center access:** Skip 4.1–4.3. Ask your IT admin: "What is our SharePoint external sharing policy? Are Anyone/anonymous links allowed?"

**Screenshots needed:** 4.1 (if accessible), 4.4 (if test file available)  
**Sensitive info:** Blur file names and user names.

---

## 6. Step 5 — Power Automate

**Goal:** Verify Power Automate availability.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 5.1 | Go to https://make.powerautomate.com | Sign in if prompted | Power Automate home page loads | Screenshot |
| 5.2 | On the left, click "Create" | — | Template gallery and creation options | Screenshot |
| 5.3 | Click "Automated cloud flow" | — | Trigger search box appears | Screenshot |
| 5.4 | In the search box, type "SharePoint" | — | SharePoint triggers are listed (When an item is created, etc.) | Screenshot showing SharePoint triggers |
| 5.5 | Close the flow builder (click ✕) → click "Discard" | — | — | — |
| 5.6 | Click "Create" → "Instant cloud flow" | — | Different trigger options | Screenshot |
| 5.7 | Search for "Approvals" | — | Approvals triggers visible | Screenshot |
| 5.8 | Close/discard | — | — | — |

**Screenshots needed:** 5.1, 5.2, 5.3, 5.4, 5.7  
**Important:** Do NOT save any flow. Discard all unsaved changes.

---

## 7. Step 6 — SharePoint Connector in Power Automate

**Goal:** Confirm the SharePoint connector is available and standard (not premium).

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 6.1 | Go to Power Automate → Create → Automated cloud flow | Search for any trigger | — | — |
| 6.2 | Click "Skip" or select any trigger | Click "+ New step" | Connector list/search appears | Screenshot |
| 6.3 | Search for "SharePoint" in the action search | — | SharePoint actions listed | Screenshot — look for "Standard" or "Premium" badge |
| 6.4 | Search for "Approvals" | — | Approvals actions listed | Screenshot |
| 6.5 | Search for "Teams" | — | Teams actions listed | Screenshot |
| 6.6 | Search for "HTTP" | — | HTTP action listed | Screenshot — check if "Premium" badge appears |
| 6.7 | Close/discard | — | — | — |

**Screenshots needed:** 6.3, 6.4, 6.5, 6.6  
**Key observation:** Does HTTP show a "Premium" badge?

---

## 8. Step 7 — Approvals / Teams

**Goal:** Verify Teams and Approvals availability.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 7.1 | Open Microsoft Teams (desktop or https://teams.microsoft.com) | — | Teams loads | Screenshot |
| 7.2 | On the left sidebar, click "Teams" | Click "Join or create a team" at the bottom | Team creation options | Screenshot |
| 7.3 | Click "Create team" | — | Team creation dialog | Screenshot (do NOT complete) |
| 7.4 | Press Cancel | — | — | — |
| 7.5 | On the left sidebar, click "Apps" | Search for "Approvals" | Approvals app appears in search results | Screenshot |

**Screenshots needed:** 7.1, 7.2, 7.3, 7.5  
**Sensitive info:** Blur team names and member names.

---

## 9. Step 8 — Entra / App Registration Visibility

**Goal:** Check if App Registrations can be created.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 8.1 🔐 | Go to https://entra.microsoft.com | Sign in with MJU account | Entra admin center loads OR "Access denied" | Screenshot |
| 8.2 🔐 | On the left, expand "Applications" | Click "App registrations" | List of existing app registrations OR access denied | Screenshot |
| 8.3 | If app registrations page loads | Look for "+ New registration" button | Button visible or grayed out | Screenshot |
| 8.4 | Click "+ New registration" (OBSERVE ONLY) | — | Registration form (Name, Supported account types) | Screenshot (do NOT submit) |
| 8.5 | Click "Cancel" | — | — | — |

**If you cannot access Entra:** Skip 8.1–8.5. Ask IT: "Can we create app registrations in Azure AD / Entra ID?"

**Screenshots needed:** 8.1, 8.2, 8.3, 8.4  
**Sensitive info:** Blur any existing app registration names.

---

## 10. Step 9 — Graph Feasibility

**Goal:** Determine if Graph API can be used for scheduled export.

| Step | Where to open | What to click | What to observe | Return to Agent |
|------|---------------|---------------|-----------------|-----------------|
| 9.1 | Go to https://developer.microsoft.com/en-us/graph/graph-explorer | — | Graph Explorer loads | Screenshot |
| 9.2 | Click "Sign in to Graph Explorer" | Sign in with your MJU account | Consent dialog may appear | Screenshot of consent (blur if personal) |
| 9.3 | After sign-in, type this in the query box: `GET https://graph.microsoft.com/v1.0/sites?search=*` | Click "Run query" | Response shows a list of SharePoint sites | Screenshot of response |
| 9.4 | Note: if you see an access error, note the error code | — | 403 = permission required; 401 = auth issue | Text: error code |
| 9.5 | If query succeeds, note a site ID from the response | Click a site | — | Text: site ID for reference |

**Screenshots needed:** 9.1, 9.3  
**Sensitive info:** Blur site names and IDs if they reveal sensitive info.

---

## 11. What to Return to the Agent

After completing the checklist, return:

1. **Screenshots** — named with step numbers (e.g., `step-2.1-sharepoint-home.png`)
2. **Text notes** — any errors, observations, or "Access denied" messages
3. **Admin responses** — if you asked your IT team questions, include their responses
4. **Any concerns** — unexpected behavior, blocked pages, confusing UI

**Do NOT return:**
- Passwords or tokens
- Personal email addresses (blur them)
- Document content
- Anything marked as confidential by MJU policy

---

## 12. Quick Reference — All Steps

| # | Service | Steps | Screenshots | Admin Required | Time |
|:-:|---------|:-----:|:-----------:|:--------------:|:----:|
| 1 | Account context | 1.1–1.4 | 3 | No | 3 min |
| 2 | SharePoint Online | 2.1–2.7 | 5 | Step 2.3 if admin center | 8 min |
| 3 | Microsoft Lists | 3.1–3.5 | 4 | No | 5 min |
| 4 | External sharing | 4.1–4.4 | 2 | Steps 4.1–4.3 | 5 min |
| 5 | Power Automate | 5.1–5.8 | 5 | No | 5 min |
| 6 | Connectors | 6.1–6.7 | 4 | No | 5 min |
| 7 | Teams / Approvals | 7.1–7.5 | 4 | No | 5 min |
| 8 | Entra / App Registration | 8.1–8.5 | 4 | Yes — Entra access | 5 min |
| 9 | Graph feasibility | 9.1–9.5 | 2 | Step 9.2 consent | 5 min |
| | **Total** | | **~33** | **1 admin section** | **~45 min** |

---

## Related Documents

| Document | Path |
|----------|------|
| Evidence Runbook | `docs/m365/m365-tenant-evidence-runbook.md` |
| Evidence Register | `docs/m365/m365-tenant-evidence-register.csv` |
| License & Capability Audit | `docs/m365/M365_LICENSE_AUDIT.md` |
| Admin Request Register | `docs/m365/m365-admin-request-register.md` |
