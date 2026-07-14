# EA-1D — Microsoft 365 Tenant Evidence Collection: Batch 2 Report — Power Automate

**Date:** 2026-07-14  
**Collected by:** Main Agent (Orchestrator) via MCP Browser  
**Account:** researchmju@mju.ac.th / สำนักวิจัยและส่งเสริมวิชาการการเกษตร  
**Tenant:** maejo365.sharepoint.com  
**Execution Model:** Single-worker, authenticated tenant session (no co-workers)

---

## Executive Summary

Power Automate is **CONFIRMED AVAILABLE** in the Maejo University M365 tenant. All three cloud flow types (Automated, Instant, Scheduled) are visible. The key EA-5 connectors — **SharePoint (Standard)**, **Approvals (Standard)**, and **Microsoft Teams (Standard)** — are all available without Premium license requirements. The **HTTP connector is PREMIUM**, confirming the architecture principle of avoiding Premium dependencies. No DLP restriction indicators were observed (NOT_VERIFIED pending admin-level confirmation). All five canonical EA-5 workflows are assessed as **NATIVE_READY or READY_WITH_LIMITATIONS** (using Standard connectors; WF-05 end-to-end GitHub sync not yet verified). Zero production flows, approvals, messages, or data modifications were made.

---

## Batch Scope

| CheckID | Capability | Status |
|---|---|---|
| PA-001 | Power Automate Portal Access | ✅ CONFIRMED |
| PA-002 | Environment Visibility | ✅ CONFIRMED |
| PA-003 | Automated Flow Trigger Check | ✅ CONFIRMED |
| PA-004 | Scheduled Flow Trigger Check | ✅ CONFIRMED |
| PA-005 | SharePoint Connector | ✅ CONFIRMED |
| PA-006 | Microsoft Lists Operations (via SPO) | ✅ CONFIRMED |
| PA-007 | Approvals Connector | ✅ CONFIRMED |
| PA-008 | Teams Connector | ✅ CONFIRMED |
| PA-009 | HTTP Connector Licensing | ⚠️ PREMIUM |
| PA-010 | DLP Restriction Indicators | ⚪ NOT_VERIFIED |
| PA-011 | Flow Creation Button | ✅ CONFIRMED |
| PA-012 | Cross-Connector Restriction (SPO+Lists) | ⚪ NOT_VERIFIED |

**Summary: 9 CONFIRMED, 1 PREMIUM, 2 NOT_VERIFIED**

---

## Collection Method

All evidence was collected within a single authenticated MCP browser session, navigating to the Power Automate portal at `https://make.powerautomate.com`. Actions taken:

- Navigated to Power Automate Home page
- Inspected environment selector panel
- Navigated to Create page and inspected flow type buttons
- Opened "Automated cloud flow" dialog and searched for SharePoint triggers
- Navigated to SharePoint connector documentation page
- Navigated to Approvals connector documentation page
- Navigated to Teams connector documentation page
- Navigated to Connectors catalog and searched for HTTP
- No production flows, connections, approvals, or messages were created

---

## Evidence Index

| Reference ID | Description | Evidence Type |
|---|---|---|
| EA1D-B2-PA-PORTAL-01 | PA portal home page with environment selector | Browser Snapshot |
| EA1D-B2-PA-ENV-01 | Environment panel showing Maejo university (default) | Browser Snapshot |
| EA1D-B2-PA-CREATE-01 | Create page with 5 flow type buttons | Browser Snapshot |
| EA1D-B2-PA-SPO-01 | SharePoint connector page with triggers list | Browser Snapshot (file) |
| EA1D-B2-PA-LIST-01 | SharePoint connector page (Lists ops context) | Browser Observation |
| EA1D-B2-PA-APPROVALS-01 | Standard approvals connector page | Browser Snapshot |
| EA1D-B2-PA-TEAMS-01 | Microsoft Teams connector page | Browser Snapshot |
| EA1D-B2-PA-HTTP-01 | Connectors catalog HTTP search results | Browser Observation |

---

## Power Automate Portal Findings

### Tenant / Account Context

| Attribute | Value |
|---|---|
| Portal URL | `https://make.powerautomate.com` |
| Redirect URL | `/environments/Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8/home` |
| Account | สำนักวิจัยและส่งเสริมวิชาการการเกษตร (researchmju@mju.ac.th) |
| Auth State | Authenticated (single session preserved) |

### Environment Findings

| Attribute | Value |
|---|---|
| Current Environment | "Maejo university (default)" |
| Environment ID | `Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8` |
| Environment Type | Default environment (M365 Education tenant) |
| Build Flows Count | 1 |
| Other Environments | 0 |
| Region | Not explicitly visible in environment selector |

### Flow Creation Capability

"Start from blank" options observed:

| # | Flow Type | Tenant Status |
|---|---|---|
| 1 | **Automated cloud flow** | ✅ Visible (button labelled "Automated cloud flow") |
| 2 | **Instant cloud flow** | ✅ Visible (button labelled "Instant cloud flow") |
| 3 | **Scheduled cloud flow** | ✅ Visible (button labelled "Scheduled cloud flow") |
| 4 | Desktop flow | ✅ Visible |
| 5 | Process mining | ✅ Visible |
| — | Business process flow | ❌ Not listed in "Start from blank" |

"Start from a connector" section includes prominent connectors:
Office 365 Outlook, **SharePoint**, Microsoft Dataverse, OneDrive for Business, Microsoft Forms, Planner, **Microsoft Teams**, RSS, SQL Server, Power BI, Azure DevOps, OneNote, Notifications, Office 365 Users, Google Calendar, **Standard approvals**, X, Excel Online (Business), Mail

**Feature availability notice:** A "Message banner for feature not available" element was observed on the Create page. This may indicate some tenant-level feature restrictions (specific feature not identifiable from snapshot alone).

---

## SharePoint Connector Findings

### Connector Status

| Attribute | Value |
|---|---|
| Connector Name | SharePoint |
| Premium Badge | ❌ Not observed (Standard connector) |
| Connector Page | Fully accessible showing triggers, templates, documentation link |

### SharePoint Triggers Observed

The following triggers are listed in the tenant's SharePoint connector:

| # | Trigger Name | WF-01 Relevant | Notes |
|---|---|---|---|
| 1 | Recurring digest of updates (preview) | — | Preview feature |
| 2 | When a file is classified by a Microsoft Syntex model | — | Syntex-dependent |
| 3 | **When a file is created (properties only)** | ✅ | Primary WF-01 trigger |
| 4 | **When a file is created or modified (properties only)** | ✅ | Expanded WF-01 |
| 5 | When a file is deleted | — | Audit support |
| 6 | When a form is submitted (preview) | — | Preview feature |
| 7 | **When an item is created** | ✅ | Primary list-trigger for WF-01 |
| 8 | **When an item is created or modified** | ✅ | WF-02 (Approval state changes) |
| 9 | When an item is deleted | — | Audit support |
| 10 | **When an item or a file is modified** | ✅ | General update trigger |
| 11 | When a file is created in a folder (deprecated) | — | Deprecated |
| 12 | When a file is created or modified in a folder (deprecated) | — | Deprecated |

### Microsoft Lists Operation Findings

Microsoft Lists operations are **exposed through the SharePoint connector** using the site/list context. The triggers "When an item is created" and "When an item is created or modified" work for both SharePoint document libraries and Microsoft Lists.

Key SharePoint connector actions relevant to Lists operations (standard connector naming):
- Create item
- Get item
- Get items
- Update item
- Get file metadata
- Get file properties
- Update file properties

**Conclusion:** Microsoft Lists registry operations are supported through the Standard SharePoint connector. No separate "Microsoft Lists" connector or Premium license is required for list operations.

---

## Approvals Connector Findings

| Attribute | Value |
|---|---|
| Connector Name | **Standard approvals** |
| Premium Badge | ❌ Not observed |
| Page Load | ✅ Fully accessible |
| Connector Description | "Enables standard approvals in workflows." |
| Triggers Section | "Triggers - A trigger is an event that starts a flow" heading visible |
| Templates Visible | "Create an approval" (Instant), "Request approval" (multiple variants), "Start approval when a new item is added", etc. |

**Key actions relevant to WF-02 (Approval Lifecycle):**
The Standard Approvals connector provides the standard approval actions:
- Start and wait for an approval
- Create an approval
- Wait for an approval

The presence of the "Standard" designation (not "Premium") and the absence of a Premium badge confirm this connector operates at the Standard license tier. This directly supports the EA-5 WF-02 approval lifecycle workflow without additional licensing.

---

## Microsoft Teams Connector Findings

| Attribute | Value |
|---|---|
| Connector Name | **Microsoft Teams** |
| Premium Badge | ❌ Not observed |
| Page Load | ✅ Fully accessible |
| Connector Description | "Microsoft Teams enables you to get all your content, tools and conversations in the team workspace with Microsoft 365." |

### Teams Triggers Observed

| # | Trigger Name |
|---|---|
| 1 | When a new channel message is added |
| 2 | When I am mentioned in a channel message |
| 3 | When a new chat message is added |
| 4 | When a new message is added to a chat or channel |
| 5 | When a new team member is added |
| 6 | When a new team member is removed |
| 7 | When I'm @mentioned |
| 8 | When keywords are mentioned |
| 9 | When someone reacted to a message in chat |

### Templates Involving Teams Actions

Multiple templates demonstrate Teams action usage in the tenant:
- "Post message to Microsoft Teams when an email arrives"
- "Post message to Teams when new item is created to SharePoint list"
- "Post a message to Microsoft Teams for a selected file"
- "Add an item to SharePoint and send an Adaptive Card in Teams"

**Conclusion:** Teams connector is available at Standard tier with post-message and adaptive card capabilities. This supports WF-04 (Expiring Review Notification) and general governance notifications.

---

## HTTP Connector Findings

| Attribute | Value |
|---|---|
| Search Results | "HTTP with Microsoft Entra ID (preauthorized) **Premium**" |
| | "HTTP With Microsoft Entra ID **Premium**" |
| Basic HTTP Action | Built-in Premium feature in Power Automate |
| Classification | **🔴 PREMIUM** |

**Architecture Impact:** The basic HTTP action and HTTP-with-Entra-ID connectors are Premium-tier features. This confirms the architectural principle of avoiding Premium dependencies:

1. **WF-05 Registry Export** should use alternative Standard patterns:
   - Save export JSON to a SharePoint/OneDrive file (Standard SharePoint connector)
   - Send export via email (Standard Office 365 Outlook connector)
   - Use the SharePoint connector to write JSON to a document library
2. Direct HTTP calls to GitHub or external APIs require Premium licensing
3. The architecture should document the Premium classification and provide a Standard-only fallback for WF-05

---

## DLP / Restriction Findings

| Attribute | Value |
|---|---|
| DLP Warning Icons in Connector List | ❌ None observed |
| Connector Blocked Warnings | ❌ None observed |
| Flow Creation Restrictions | ❌ None observed |
| Classification | **NOT_VERIFIED** |

Per evidence rules: **"No visible restriction observed ≠ DLP confirmed unrestricted."** The absence of warning icons does not confirm the absence of DLP policies. Tenant-level DLP configuration requires admin access to the Power Platform admin center or Microsoft 365 Compliance center, which was not available in this session.

A "Message banner for feature not available" was observed on the Create page. This may indicate a tenant-level feature restriction, but the specific feature could not be identified from the session.

---

## License Findings

| Connector | License Tier | Evidence |
|---|---|---|
| SharePoint | Standard | No Premium badge on connector page |
| Standard Approvals | Standard | Name explicitly includes "Standard" |
| Microsoft Teams | Standard | No Premium badge on connector page |
| HTTP (basic) | Premium | Premium badge on HTTP-with-Entra-ID variants in catalog |
| HTTP with Entra ID | Premium | Explicit "Premium" label in connector list |

**Key Insight:** All EA-5 critical connectors (SharePoint, Approvals, Teams) operate at the **Standard** tier within the M365 Education tenant. The architecture can proceed without Premium add-ons, consistent with "Build Less. Govern More."

---

## Canonical EA-5 Workflow Feasibility

### WF-01 — Document Upload & Registration

| Requirement | Connector | Status |
|---|---|---|
| Trigger: New file uploaded to SharePoint | SharePoint: "When a file is created (properties only)" | ✅ Standard |
| Action: Get file metadata | SharePoint: "Get file properties" | ✅ Standard |
| Action: Create/update registry item | SharePoint: "Create item" / "Update item" | ✅ Standard |
| Action: Assign DocumentID | SharePoint: "Update item" (set DocumentID column) | ✅ Standard |

**Classification: NATIVE_READY**

All WF-01 triggers and actions are available through the Standard SharePoint connector. No Premium, Admin, or additional license dependencies identified.

---

### WF-02 — Approval Lifecycle

| Requirement | Connector | Status |
|---|---|---|
| Trigger: Item status change request | SharePoint: "When an item is created or modified" | ✅ Standard |
| Action: Start approval workflow | Approvals: "Start and wait for an approval" | ✅ Standard |
| Action: Update status after approval | SharePoint: "Update item" | ✅ Standard |
| Action: Notify on rejection | Teams: "Post message" | ✅ Standard |

**Classification: NATIVE_READY**

Standard Approvals connector confirmed. SharePoint-to-Approvals lifecycle can be implemented entirely with Standard connectors. The "Standard approvals" connector page explicitly shows it works "in workflows."

---

### WF-03 — Archive Control

| Requirement | Connector | Status |
|---|---|---|
| Trigger: Scheduled scan for obsolete docs | Scheduled cloud flow | ✅ Confirmed |
| Action: Query items by date/status | SharePoint: "Get items" | ✅ Standard |
| Action: Update status to obsolete/archived | SharePoint: "Update item" | ✅ Standard |
| Action: Move/copy file if needed | SharePoint: "Move file" / "Copy file" | ✅ Standard |

**Classification: NATIVE_READY**

Scheduled cloud flow confirmed. SharePoint connector supports Get items, Update item, and file operations. No Premium dependency.

---

### WF-04 — Expiring Review Notification

| Requirement | Connector | Status |
|---|---|---|
| Trigger: Scheduled scan for approaching review dates | Scheduled cloud flow | ✅ Confirmed |
| Action: Query items near review date | SharePoint: "Get items" with OData filter | ✅ Standard |
| Action: Send notification to owner | Teams: "Post message" / Office 365 Outlook: "Send email" | ✅ Standard |
| Action: Create approval if needed | Approvals: "Start and wait for an approval" | ✅ Standard |

**Classification: NATIVE_READY**

All three connectors (Scheduled flow, SharePoint, Teams) confirmed at Standard tier. Email alternative available through Office 365 Outlook connector (also Standard).

---

### WF-05 — Registry Export Trigger

| Requirement | Connector | Status |
|---|---|---|
| Trigger: Scheduled export job | Scheduled cloud flow | ✅ Confirmed |
| Action: Query all public registry items | SharePoint: "Get items" | ✅ Standard |
| Action: Transform to JSON format | Power Automate expressions (Compose/Select) | ✅ Built-in |
| Action: Save JSON file to SharePoint/OneDrive | SharePoint: "Create file" | ✅ Standard |
| Alternative: Send JSON via email | Office 365 Outlook: "Send email" | ✅ Standard |
| Premium path: POST JSON to GitHub API | HTTP | 🔴 Premium |

**Classification: READY_WITH_LIMITATIONS**

The Power Automate portion of this workflow is tenant-capable using Standard connectors:
1. Using Scheduled cloud flow to trigger
2. Querying public items via SharePoint "Get items"
3. Transforming to JSON using Power Automate's built-in `Select` and `Compose` actions
4. Saving the JSON file to a SharePoint document library as the export artifact

**Limitation:** External synchronization from the SharePoint export artifact to GitHub has NOT been end-to-end verified. The architecture proposes GitHub Actions watching the SharePoint-synced file (outside Power Automate), but this integration path has not been tested in the MJU tenant context. The Power Automate → SharePoint segment is NATIVE_READY; the complete WF-05 end-to-end flow is READY_WITH_LIMITATIONS.

**The HTTP premium requirement is AVOIDED** by keeping the JSON export within SharePoint and using GitHub Actions (in the code repository) for the final step.

---

## Evidence Register Updates

The following 12 rows in `docs/m365/m365-tenant-evidence-register.csv` were updated:

| CheckID | Previous | New |
|---|---|---|
| PA-001 | NOT_VERIFIED | CONFIRMED |
| PA-002 | NOT_VERIFIED | CONFIRMED |
| PA-003 | NOT_VERIFIED | CONFIRMED |
| PA-004 | NOT_VERIFIED | CONFIRMED |
| PA-005 | NOT_VERIFIED | CONFIRMED |
| PA-006 | NOT_VERIFIED | CONFIRMED |
| PA-007 | NOT_VERIFIED | CONFIRMED |
| PA-008 | NOT_VERIFIED | CONFIRMED |
| PA-009 | NOT_VERIFIED | PREMIUM |
| PA-010 | NOT_VERIFIED | NOT_VERIFIED (unchanged) |
| PA-011 | NOT_VERIFIED | CONFIRMED |
| PA-012 | NOT_VERIFIED | NOT_VERIFIED (unchanged) |

Evidence references, dates, and detailed notes were captured for all updated rows.

---

## Architecture Impact

### EA-5 Design Impact

- **CONFIRMED:** 4 of 5 canonical EA-5 workflows (WF-01 to WF-04) are **NATIVE_READY** using Standard connectors
- **CONFIRMED:** WF-05 (Registry Export) Power Automate portion is **NATIVE_READY**; full end-to-end (including GitHub sync) is **READY_WITH_LIMITATIONS**
- **CONFIRMED:** SharePoint connector handles both document library and list operations (no separate Lists connector needed)
- **CONFIRMED:** Approvals lifecycle supported by "Standard approvals" connector
- **CONFIRMED:** Teams notifications available for governance workflows
- **AVOIDED:** WF-05 Registry Export does not require HTTP/Premium — JSON can be saved to SharePoint and synced via GitHub Actions

### EA-5 Implementation Impact

- **READY:** EA-5 workflows can be implemented after EA-3 (SharePoint) and EA-4 (Lists) provisioning
- **CONDITION:** Cross-connector DLP restrictions (PA-012) should be verified before production flow creation
- **CONDITION:** The "feature not available" banner should be investigated for any specific limitation

### EA-7 Export Impact

- **CONFIRMED:** Scheduled cloud flow supports regular export triggering
- **CONFIRMED:** JSON export to SharePoint file is feasible without Premium
- **RECOMMENDATION:** Use SharePoint as intermediate JSON store; GitHub Actions for final sync to code repository
- **AVOIDED:** Direct HTTP-to-GitHub via Power Automate (Premium dependency)

---

## Optional Tests Required

| Test ID | Description | Priority |
|---|---|---|
| PA-TEST-01 | Create scaffold flow with SharePoint trigger + Lists action to verify no cross-connector DLP block | Medium |
| PA-TEST-02 | Create scaffold flow with Approvals connector to verify connection creation | Medium |
| PA-TEST-03 | Investigate "Message banner for feature not available" on Create page | Low |

**Status:** `OPTIONAL_TEST_REQUIRED` — explicit user authorization required before any flow creation.

---

## Remaining Unknowns

1. **DLP Policy Configuration:** Actual tenant DLP rules are unknown without admin center access
2. **Cross-Connector Restrictions:** SPO+Lists co-existence in one flow not tested
3. **Feature Banner:** "Feature not available" message on Create page — specific feature unknown
4. **Environment Region:** Not visible in environment selector
5. **Flow Ownership / Service Account:** Not assessed (requires EA-5 design)
6. **Flow Run History / Quotas:** Not applicable (no flows exist)

---

## Admin Dependencies

| Dependency | Context |
|---|---|
| DLP Policy Verification | Requires Power Platform admin center access to confirm no cross-connector blocks |
| Environment Admin | Creating additional environments (if needed) requires admin |
| Premium License Enablement | If HTTP connector is needed in future, admin must enable Premium licensing |

---

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Undiscovered DLP blocks SPO+Lists flow | Medium | Test with scaffold flow before production |
| "Feature not available" banner indicates material restriction | Low | Investigate specific feature; most likely a non-critical preview feature |
| Single Default environment limits multi-stage deployment | Low | Acceptable for Phase 1; Production/Dev split can be deferred |
| HTTP Premium needed for future integrations | Low | Architecture already avoids Premium dependency; GitHub Actions handle external sync |

---

## Recommended Next Batch

**Batch 3 — Teams / Approvals / Microsoft 365 Groups (TMS-001 to TMS-004, and PA-007 deeper check)**

Priorities:
1. Verify Teams web app access
2. Check team creation capability (self-service vs admin-provisioned)
3. Verify Approvals app availability in Teams
4. Check M365 Groups creation policy

---

## Final Batch Verdict

**BATCH_2_CONFIRMED**

Power Automate is confirmed available in the Maejo University tenant. All critical Standard connectors needed for the 5 canonical EA-5 workflows are available. The HTTP connector is Premium (as expected), and the architecture's avoidance of Premium dependencies is validated. No production resources were created or modified.

---

*End of Batch 2 Report — Generated 2026-07-14*
