# M365 Tenant Evidence Runbook — RAE Document Center

**Phase:** EA-1B — Tenant Evidence Collection Preparation  
**Status:** Runbook created — collection not yet started  
**Last updated:** 2026-07-14  
**Audit reference:** `docs/m365/M365_LICENSE_AUDIT.md`  
**Evidence register:** `docs/m365/m365-tenant-evidence-register.csv`  
**User checklist:** `docs/m365/m365-user-verification-checklist.md`

---

## 1. Purpose

This runbook provides a structured, repeatable method for collecting evidence from the Maejo University (MJU) Microsoft 365 tenant. The evidence collected will replace the current `NOT_VERIFIED` classifications in the EA-1 License & Capability Audit with observed tenant facts.

**Goal:** Upgrade the EA-1 verdict from `INSUFFICIENT_EVIDENCE` to either `TENANT_READY`, `TENANT_READY_WITH_CONDITIONS`, or `TENANT_NOT_READY`.

---

## 2. Safety Rules

### 2.1 Before Starting

| Rule | Description |
|------|-------------|
| R1 | **Do NOT create any production resources.** Observe only. |
| R2 | **Do NOT implement Power Automate flows.** Browse the connector list only. |
| R3 | **Do NOT create an Entra/App Registration.** Browse the UI only. |
| R4 | **Do NOT delete or modify existing tenant configuration.** |
| R5 | **Do NOT upload test documents** unless explicitly directed by the Architect. |
| R6 | **Do NOT expose passwords, tokens, secrets, or private document content** in screenshots. |
| R7 | **Blur/crop out personal information** (names, email addresses, admin details) from all screenshots. |
| R8 | **Document everything** — screenshots and notes are better than memory. |
| R9 | **Collect evidence in the ordered sequence** defined in the User Verification Checklist. |

### 2.2 If Something Goes Wrong

| Situation | Action |
|-----------|--------|
| Access denied / permission error | Note the error message. Mark check as ADMIN_REQUIRED. Do NOT request permission elevation beyond what the runbook specifies. |
| Feature not found | Note the attempted navigation path. Mark check as NOT_AVAILABLE or NOT_VERIFIED. |
| Accidental resource creation | Contact tenant admin immediately. Document the incident. |
| Unsure about a step | Skip the check. Mark as NOT_VERIFIED. Note the reason. |

---

## 3. Evidence Classification

Every piece of evidence must be classified using these categories:

| Classification | Meaning | Used When |
|---------------|---------|-----------|
| `OBSERVED` | Evidence captured from tenant UI | User directly observed the capability |
| `ADMIN_CONFIRMED` | Tenant admin confirmed capability | Admin provided written/verbal confirmation |
| `DOCUMENTED` | Evidence from tenant documentation | Official MJU M365 documentation |
| `ARCHITECTURE_REQUIREMENT` | Required by approved architecture | Design documents specify this |
| `ASSUMPTION` | Reasonable inference | Standard M365 capability without tenant proof |
| `UNKNOWN` | No evidence or inference possible | Cannot determine |

### Evidence Quality

| Quality | Definition |
|---------|-----------|
| **Direct** | Screenshot or screen capture from tenant UI |
| **Verified** | Confirmed by tenant admin via email/ticket |
| **Inferred** | Logical deduction from observed evidence |
| **Unverified** | No supporting evidence collected |

---

## 4. SharePoint Verification

### 4.1 Access & Site Discovery

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.1.1 | Open https://[tenant]-admin.sharepoint.com OR https://admin.microsoft.com → SharePoint admin center | SharePoint admin center loads | Screenshot of admin center |
| 4.1.2 | Navigate to "Active sites" | List of all SharePoint sites | Screenshot showing at least partial site list |
| 4.1.3 | Search for "RAE Document Center" or check if the site exists | Site appears OR does not appear | Screenshot of search result |
| 4.1.4 | If site does NOT exist: check "Create" or "+" button | Create option visible or disabled | Screenshot of site creation UI state |

### 4.2 Site Creation

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.2.1 | In SharePoint admin center, check site creation policy | Self-service or admin-only | Screenshot or note |
| 4.2.2 | From any existing SharePoint site, click Settings → Site information → View all site settings | Site settings page | Screenshot |
| 4.2.3 | Navigate to Site collection features | Feature list visible | Screenshot |

### 4.3 Document Libraries

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.3.1 | On any existing site, go to Site contents | List of all libraries | Screenshot |
| 4.3.2 | Click "New" → "Document library" | Library creation dialog appears | Screenshot |
| 4.3.3 | (OBSERVE ONLY — do NOT create) | — | Note what options appear |

### 4.4 Custom Columns

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.4.1 | On any existing library, click "+ Add column" → "Show all column types" | Column type list visible (Single text, Choice, Person/Group, etc.) | Screenshot |
| 4.4.2 | Click "Choice" column type | Choice column configuration form | Screenshot |
| 4.4.3 | Click "Person or Group" | Person/Group column form | Screenshot |
| 4.4.4 | Click "Managed Metadata" | Term Store selection dialog (may require Term Store access) | Screenshot |

### 4.5 Content Types

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.5.1 | Site Settings → Content types → Create | Content type creation page | Screenshot |
| 4.5.2 | Check if existing content types can be modified | Edit button visible | Screenshot |

### 4.6 Managed Metadata / Term Store

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.6.1 | Site Settings → Term store management | Term Store admin page OR access denied | Screenshot |
| 4.6.2 | Check if "RAE Document Center" term group exists | Present or absent | Screenshot |
| 4.6.3 | Check if "RAE-Tags" term set exists | Present or absent | Screenshot |

### 4.7 Versioning

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.7.1 | Library Settings → Versioning settings | Versioning configuration page | Screenshot |
| 4.7.2 | Confirm major/minor versioning options are available | Options visible | Screenshot |

### 4.8 Column Indexing

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.8.1 | Library Settings → Indexed columns | Column index management page | Screenshot |
| 4.8.2 | Check if new indexes can be created | Add button visible | Screenshot |

### 4.9 External Sharing

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.9.1 | SharePoint admin center → Sharing | Sharing policy page | Screenshot |
| 4.9.2 | Check "Anyone" (anonymous) link setting | Allowed / Not allowed / Specific domains | Screenshot |
| 4.9.3 | Check "New and existing guests" setting | Setting visible | Screenshot |
| 4.9.4 | Check expiration and permission settings | Values visible | Screenshot |

---

## 5. Microsoft Lists Verification

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 5.1 | Open https://[tenant].sharepoint.com/_layouts/15/pointpub.aspx OR Lists app from M365 app launcher | Lists app loads | Screenshot |
| 5.2 | Click "New list" | List creation options appear | Screenshot |
| 5.3 | Select "Blank list" | List configuration form | Screenshot |
| 5.4 | (OBSERVE ONLY — do NOT create) | — | Note available options |
| 5.5 | On an existing list (if available), click the view dropdown → "Create new view" | View creation dialog | Screenshot |
| 5.6 | Check column types available in Lists (open any existing list, click "+ Add column") | Available column types | Screenshot |

---

## 6. Power Automate Verification

### 6.1 Portal Access

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 6.1.1 | Open https://make.powerautomate.com | Power Automate portal loads | Screenshot |
| 6.1.2 | Check environment selector (top-right) | At least one environment visible | Screenshot |
| 6.1.3 | Note: if redirected to login, authentication is required | Login page appears | Note |

### 6.2 Flow Capability (OBSERVE ONLY)

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 6.2.1 | Click "Create" in left navigation | Templates and creation options appear | Screenshot |
| 6.2.2 | Click "Automated cloud flow" | Flow builder opens with trigger search | Screenshot |
| 6.2.3 | Search for "SharePoint" in triggers | SharePoint triggers visible | Screenshot |
| 6.2.4 | Search for "Schedule" in triggers | Schedule triggers visible | Screenshot |
| 6.2.5 | Click "Instant cloud flow" | Different trigger options | Screenshot |
| 6.2.6 | Close/discard the flow — do NOT save | — | — |

### 6.3 Connector Browsing (OBSERVE ONLY)

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 6.3.1 | Create a blank automated flow, add a step | Connector list appears | Screenshot |
| 6.3.2 | Search for "SharePoint" in connectors | SharePoint connector visible | Screenshot showing Standard badge |
| 6.3.3 | Search for "Approvals" | Approvals connector visible | Screenshot |
| 6.3.4 | Search for "Teams" | Teams connector visible | Screenshot |
| 6.3.5 | Search for "HTTP" | HTTP connector visible; check for Premium badge | Screenshot |
| 6.3.6 | Close/discard — do NOT save | — | — |

### 6.4 DLP Indicators

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 6.4.1 | In flow builder, check for any connector with warning icons | Yellow/red warning = DLP restriction | Screenshot |
| 6.4.2 | Try to add SharePoint action after Lists trigger (or vice versa) | If blocked, DLP cross-connector restriction | Note |

---

## 7. Teams / Approvals Verification

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 7.1 | Open Microsoft Teams desktop or web app | Teams loads | Screenshot |
| 7.2 | Click "Teams" in left sidebar → "Join or create a team" | Creation option visible or hidden | Screenshot |
| 7.3 | Click "Create team" → "From scratch" → "Private" | Team creation dialog | Screenshot (OBSERVE ONLY — do NOT complete) |
| 7.4 | Close/cancel — do NOT create | — | — |
| 7.5 | Click Apps (left sidebar) → Search "Approvals" | Approvals app visible | Screenshot |

---

## 8. Graph API Verification

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 8.1 | Open https://developer.microsoft.com/en-us/graph/graph-explorer | Graph Explorer loads | Screenshot |
| 8.2 | Sign in with MJU M365 account | Authentication prompt | Screenshot (blur credentials) |
| 8.3 | After sign-in, run GET `https://graph.microsoft.com/v1.0/sites?search=*` | List of SharePoint sites | Screenshot of response |
| 8.4 | Note which permissions are requested for the query | Consent dialog (if any) | Screenshot |
| 8.5 | (If consented) run GET `https://graph.microsoft.com/v1.0/sites/{site-id}/lists` | Lists within a site | Screenshot |

---

## 9. Entra App Registration Verification

| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 9.1 | Open https://entra.microsoft.com | Entra admin center loads | Screenshot |
| 9.2 | Navigate to Applications → App registrations | App registration list OR access denied | Screenshot |
| 9.3 | Check if "New registration" button is visible | Self-service or admin-only | Screenshot |
| 9.4 | Click "New registration" — fill nothing, just observe | Registration form visible | Screenshot; do NOT submit |
| 9.5 | Close/cancel — do NOT create | — | — |

---

## 10. Optional Services Verification

| Service | Step | Action |
|---------|------|--------|
| Power BI | 10.1 | Open https://app.powerbi.com — does it load? Access allowed or blocked? |
| Microsoft Forms | 10.2 | Open https://forms.microsoft.com — can forms be created? |
| Copilot | 10.3 | Check M365 app launcher for Copilot icon — is it present? |

These are optional and non-blocking. Skip if time is limited.

---

## 11. Evidence Capture Rules

| Rule | Description |
|------|-------------|
| E1 | Every screenshot must include the **browser URL bar** showing the page location |
| E2 | Screenshots must capture **relevant areas only** — crop unnecessary whitespace |
| E3 | **Blur/crop** all: user names, email addresses, admin names, phone numbers, passwords |
| E4 | **Blur** any document titles or content that could be sensitive |
| E5 | Name screenshots consistently: `{CheckID}_{description}.png` (e.g., `SPO-001_admin_center.png`) |
| E6 | For text-based evidence, copy/paste as plain text and save to a `.txt` file |
| E7 | Do NOT capture screenshots of login/password pages |
| E8 | If a step cannot be completed, note the **exact error message** as evidence |

---

## 12. Sensitive Information Rules

| Item | Action |
|------|--------|
| Tenant URL | OK to capture (e.g., `mju.sharepoint.com`) — tenant URLs are discoverable |
| Site URLs | OK to capture (e.g., `mju.sharepoint.com/sites/SomeSite`) |
| User email addresses | **BLUR** before sharing |
| Admin names | **BLUR** before sharing |
| API keys / secrets | **DO NOT CAPTURE** |
| Passwords | **DO NOT CAPTURE** |
| Personal identifiable information (PII) | **BLUR** |
| Document content | **DO NOT CAPTURE** unless explicitly a public test document |

---

## 13. Decision Matrix

After collecting all evidence, use this matrix to determine the EA-1 verdict:

### Verdict 1: TENANT_READY

All conditions must be satisfied:
- SharePoint Online is confirmed accessible
- At least one existing site or site creation capability confirmed
- Microsoft Lists is accessible
- Anonymous sharing is permitted OR feasible alternative identified
- Power Automate portal accessible with standard connectors visible
- Teams accessible
- Entra/app registration accessible (self-service or admin-provisioned)

### Verdict 2: TENANT_READY_WITH_CONDITIONS

Core capabilities are confirmed but conditional:
- SharePoint accessible + site creation admin-provisioned (condition: submit request)
- Anonymous sharing restricted but guest sharing works (condition: use authenticated links)
- Power Automate accessible but DLP needs adjustment (condition: admin action)
- Lists accessible via SharePoint (condition: site must exist first)

### Verdict 3: TENANT_NOT_READY

Any of these conditions:
- SharePoint Online not provisioned in tenant
- Microsoft Lists/infrastructure lists not available
- Power Automate not provisioned in tenant
- Site creation denied by all means

### Verdict 4: INSUFFICIENT_EVIDENCE

Evidence collection could not be completed:
- User cannot access M365 portals
- Essential screenshots could not be captured
- Tenant admin not reachable for escalation
- Fewer than 50% of required checks completed

---

## 14. Completion Checklist

| # | Item | Status |
|---|------|--------|
| 1 | SharePoint admin center accessed | ☐ |
| 2 | Active sites reviewed | ☐ |
| 3 | Site creation capability checked | ☐ |
| 4 | Document library creation options observed | ☐ |
| 5 | Column types confirmed (Choice, Person/Group, Managed Metadata) | ☐ |
| 6 | Content Types creation feasibility checked | ☐ |
| 7 | Term Store accessibility checked | ☐ |
| 8 | Versioning settings confirmed | ☐ |
| 9 | Column indexing confirmed | ☐ |
| 10 | External sharing policy documented (CRITICAL) | ☐ |
| 11 | Microsoft Lists app accessed | ☐ |
| 12 | List creation options observed | ☐ |
| 13 | List view creation options observed | ☐ |
| 14 | Power Automate portal accessed | ☐ |
| 15 | Flow creation options observed (no flow created) | ☐ |
| 16 | SharePoint connector confirmed visible | ☐ |
| 17 | Approvals connector confirmed visible | ☐ |
| 18 | Teams connector confirmed visible | ☐ |
| 19 | HTTP connector licensing status noted | ☐ |
| 20 | Teams accessed | ☐ |
| 21 | Team creation options observed | ☐ |
| 22 | Approvals app confirmed visible | ☐ |
| 23 | Graph Explorer accessed | ☐ |
| 24 | Graph API sites query attempted | ☐ |
| 25 | Entra portal accessed | ☐ |
| 26 | App registrations visibility checked | ☐ |

---

## Related Documents

| Document | Path |
|----------|------|
| Evidence Register | `docs/m365/m365-tenant-evidence-register.csv` |
| User Verification Checklist | `docs/m365/m365-user-verification-checklist.md` |
| License & Capability Audit | `docs/m365/M365_LICENSE_AUDIT.md` |
| Provisioning Gate | `docs/m365/m365-provisioning-gate.md` |
| Admin Request Register | `docs/m365/m365-admin-request-register.md` |
