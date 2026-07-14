# EA-5B — Workflow Implementation & End-to-End Validation Report

**Phase:** EA-5B — Workflow Implementation & End-to-End Validation  
**Precondition:** EA-5A = EA5A_GOVERNANCE_READY (commit `eea468f`)  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Target Site:** https://maejo365.sharepoint.com/sites/msteams_54adc4  
**Power Automate Environment:** Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8  
**Date:** 2026-07-14  
**Status:** EA5B_BLOCKED

---

## 1. EA-5A State Audit (Precondition Verification)

### 1.1 EA-5A Preconditions

| Precondition | Status | Evidence |
|---|---|---|
| EA-5A commit = `eea468f` | ✅ CONFIRMED | git log |
| 18 governance folders created | ✅ CONFIRMED | REST API verify (all 18 folders 200 OK) |
| Folder permissions configured | ✅ CONFIRMED | Unique permissions on all folders per permissions-matrix.md |
| Power Automate accessible | ✅ CONFIRMED | make.powerautomate.com — Default environment |

### 1.2 Power Automate Flow Audit (BEFORE EA-5B)

**Method:** Navigated to `make.powerautomate.com/environments/Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8/flows` and verified "My flows" page.

| Flow | Expected from EA-5A | Actual State | Evidence |
|------|--------------------|----|---|
| WF-01 - RAE Upload & Registration | Flow skeleton (trigger only) | ❌ NOT FOUND | "You don't have any flows" |
| WF-02 - RAE Approval Lifecycle | Specification only | ❌ NOT FOUND | "You don't have any flows" |
| WF-03 - RAE Archive Control | Specification only | ❌ NOT FOUND | "You don't have any flows" |
| WF-04 - RAE Expiring Review Notification | Flow skeleton (scheduled) | ❌ NOT FOUND | "You don't have any flows" |
| WF-05 - RAE Export Foundation | READY_WITH_LIMITATIONS | ❌ NOT FOUND | "You don't have any flows" |

**Audit Conclusion:** Zero flows persisted in the Power Automate environment. EA-5A flow skeletons referenced in the EA-5A report were NOT saved to the tenant. The Power Automate "My flows" page shows "You don't have any flows."

> **Correction to EA-5A Report:** Tasks 4 and 7 ("WF-01 Flow skeleton" and "WF-04 Flow skeleton created") in Section 10.1 of the EA-5A report are **inaccurate**. No flows were saved at that time. This is documented here as a correction of record; the EA-5A GOVERNANCE_READY decision remains valid because the EA-5A phase's primary deliverables (folder structure, folder permissions, workflow specifications) were all achieved.

---

## 2. EA-5B Implementation Attempts

### 2.1 WF-01 — Upload & Registration (Attempted)

**Objective:** Create automated cloud flow: SharePoint item created/modified → filter _Inbox → create Registry record

**Steps Executed:**

| Step | Action | Result |
|------|--------|--------|
| 1 | Navigate to Power Automate Create page | ✅ Success |
| 2 | Enter flow name "WF-01 - RAE Upload & Registration" | ✅ Success |
| 3 | Select "Automated cloud flow" type | ✅ Success |
| 4 | Select trigger "When an item is created or modified" (SharePoint) | ✅ Success (via JavaScript click) |
| 5 | Configure trigger: Site Address = `https://maejo365.sharepoint.com/sites/msteams_54adc4` | ✅ Selected |
| 6 | Configure trigger: List Name = "Administration" | ⚠️ Entered as custom value — did NOT persist |
| 7 | Add Condition action (folder filter for `_Inbox`) | ✅ Action added |
| 8 | Set condition expression via Code view (JSON) | ⚠️ Partial — Monaco editor model not updated by browser_fill |
| 9 | Save flow | ❌ FAILED — "Invalid parameter for 'When an item is created or modified'. Error: 'List Name' is required." |

**WF-01 Final State:** NOT SAVED. Flow was in unsaved draft state with trigger "Invalid parameters" when closed.

### 2.2 WF-02 — Approval Lifecycle

**Objective:** Automated flow triggered on item modification → approval routing → status update

**Steps Executed:** None — blocked by WF-01 save failure; prioritized EA-5B report.

**WF-02 Final State:** NOT CREATED

### 2.3 WF-03 — Archive Control

**Objective:** Scheduled daily flow → query items with DocumentStatus = "obsolete" → move to _Archive folder

**Steps Executed:** None

**WF-03 Final State:** NOT CREATED

### 2.4 WF-04 — Expiring Review Notification

**Objective:** Scheduled daily flow → query items with ReviewDate within 30 days → send email notification

**Steps Executed:** None

**WF-04 Final State:** NOT CREATED

### 2.5 WF-05 — Export Foundation

**Objective:** Scheduled flow → query Registry → generate JSON export → save to SharePoint

**Steps Executed:** None beyond EA-5A specification

**WF-05 Final State:** READY_WITH_LIMITATIONS (specification documented, no actual flow)

---

## 3. Blocking Factors

### 3.1 Power Automate UI Automation Constraints

| Blocker | Impact | Evidence |
|---------|--------|---------|
| **Trigger List Name field does not accept browser_fill** | Cannot configure SharePoint trigger target library | Save failed: "List Name is required" |
| **Monaco code editor rejects programmatic value updates** | Cannot set condition expression via Code view | `browser_fill` updates DOM value but Monaco model ignores it |
| **CORS blocks Power Automate API calls from browser** | Cannot create/configure flows via REST API from browser context | Prior session: "Failed to fetch" / HTML response |
| **Dynamic UI refs change between snapshots** | Unreliable click targeting in multi-step flows | Refs reset after each action panel interaction |
| **Dropdown combobox selections don't persist** | Custom-typed list names are accepted in UI but not bound to model | List Name = "Administration" shown but not saved |

### 3.2 Identity / Owner Dependencies (Carried from EA-4 and EA-5A)

| Dependency | Status | Impact |
|-----------|--------|--------|
| Category Owner user assignments | 🔴 UNRESOLVED | WF-02 approval routing cannot resolve recipient |
| `RAE-DC-Contributors` members | 🔴 UNRESOLVED | WF-01 notification routing blocked |
| `RAE-DC-ArchiveManagers` members | 🔴 UNRESOLVED | WF-03 archive notification routing blocked |
| `RAE-DC-MigrationBot` service account | 🔴 NOT PROVISIONED | WF-01 bulk import entry point blocked |
| Power Automate connection binding | 🟡 PARTIAL | All connectors listed but no flow was saved to bind them |

### 3.3 End-to-End Test Blocked

Since no flows could be saved, the end-to-end validation path is blocked:

```
upload → metadata → Registry → lifecycle → archive/review notification
   ❌         ❌          ❌          ❌                    ❌
```

All pipeline stages require functional Power Automate flows that do not exist.

---

## 4. Complete Workflow Specifications (for Manual Implementation)

These specifications are carried forward from EA-5A and enhanced with additional detail. A tenant administrator or Power Automate developer can implement all 5 flows using these specifications.

### 4.1 WF-01: Upload & Registration

**Flow Type:** Automated cloud flow  
**Trigger:** SharePoint — "When an item is created or modified"  
**Required Connections:** SharePoint, Microsoft Lists, Office 365 Outlook  

**Trigger Configuration:**
- Site Address: `https://maejo365.sharepoint.com/sites/msteams_54adc4`
- List Name: (one flow per library: Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals)

**Action Sequence:**

```
[Trigger] When an item is created or modified
  │
  ├── [Action 1] Condition: Is the item in the _Inbox folder?
  │   Expression: contains(triggerBody()?['Path'], '_Inbox')
  │   Operator: is equal to / true
  │
  ├── [TRUE Branch]
  │   ├── [Action 2] Compose: Generate DocumentID
  │   │   Expression: if(empty(triggerBody()?['RAE_DocumentID']),
  │   │              concat('RAE-PENDING-', formatDateTime(utcNow(), 'yyyyMMddHHmmss')),
  │   │              triggerBody()?['RAE_DocumentID'])
  │   │
  │   ├── [Action 3] SharePoint: Create item (in "RAE Document Registry")
  │   │   Site: https://maejo365.sharepoint.com/sites/msteams_54adc4
  │   │   List: RAE Document Registry
  │   │   Fields:
  │   │     Title          = triggerBody()?['{FilenameWithExtension}']
  │   │     RAE_DocumentID = outputs('Compose_DocumentID')
  │   │     Category       = (derived from library name — see mapping below)
  │   │     Status         = "draft"
  │   │     Visibility     = "internal"
  │   │     SourceSystem   = "Direct Upload"
  │   │     Version        = "1.0"
  │   │     StorageURL     = triggerBody()?['{Link}']
  │   │     Owner          = "TBD"   ← resolved when group members are assigned
  │   │
  │   └── [Action 4] Office 365 Outlook: Send an email
  │       To: (Site Admin TEST — temp until Category Owner resolved)
  │       Subject: "[RAE-DC] New document uploaded: @{triggerBody()?['{FilenameWithExtension}']}"
  │       Body: Document uploaded to _Inbox. DocumentID: @{outputs('Compose_DocumentID')}
  │
  └── [FALSE Branch] — Terminate / do nothing (files outside _Inbox not processed)
```

**Library → Category Mapping:**
| Library | Category Value |
|---------|---------------|
| Administration | Administration |
| FinanceProcurement | Finance & Procurement |
| PlanningPolicy | Planning & Policy |
| AcademicServices | Academic Services |
| Research | Research |
| SOPManuals | SOPs & Manuals |

**Note:** Create 6 copies of this flow (one per library) OR use a single flow with parallel condition branches per library (increases complexity).

---

### 4.2 WF-02: Approval Lifecycle

**Flow Type:** Automated cloud flow  
**Trigger:** SharePoint — "When an existing item is modified"  
**Required Connections:** SharePoint, Approvals, Office 365 Outlook  

**Trigger Configuration:**
- Site Address: `https://maejo365.sharepoint.com/sites/msteams_54adc4`
- List Name: (one flow per library — same pattern as WF-01)

**Action Sequence:**

```
[Trigger] When an existing item is modified
  │
  ├── [Action 1] Condition: Did DocumentStatus change to "review"?
  │   Expression: triggerBody()?['DocumentStatus'] is equal to 'review'
  │
  ├── [TRUE Branch — Submit for Review]
  │   ├── [Action 2] SharePoint: Update item in RAE Document Registry
  │   │   Set Status = "review"
  │   │
  │   ├── [Action 3] Approvals: Start and wait for an approval
  │   │   Approval type: Approve/Reject — First to respond
  │   │   Title: "Review request: @{triggerBody()?['Title']}"
  │   │   Assigned to: (Category Owner — UNRESOLVED; use Site Admin temporarily)
  │   │   Details: Document ID: @{triggerBody()?['RAE_DocumentID']}
  │   │
  │   ├── [Action 4] Condition: Was it Approved?
  │   │   Expression: body('Start_and_wait_for_an_approval')?['outcome'] is equal to 'Approve'
  │   │
  │   │   ├── [TRUE — Approved]
  │   │   │   ├── [Action 5a] SharePoint: Update item (library) — Set DocumentStatus = "current"
  │   │   │   └── [Action 5b] SharePoint: Update item (Registry) — Set Status = "current"
  │   │   │
  │   │   └── [FALSE — Rejected]
  │   │       ├── [Action 5c] SharePoint: Update item (library) — Set DocumentStatus = "draft"
  │   │       └── [Action 5d] Office 365 Outlook: Send email — notify uploader of rejection
  │   │
  │   └── [Action 6] Log to flow audit (Compose action with timestamp + outcome)
  │
  └── [FALSE Branch]
      ├── Condition: Did DocumentStatus change to "obsolete"?
      │   ├── [TRUE — Obsolete]
      │   │   ├── SharePoint: Update Registry Status = "obsolete"
      │   │   ├── SharePoint: Move file to _Archive folder
      │   │   └── Office 365 Outlook: Notify Category Owner
      │   └── (Other status transitions logged but not automated)
```

---

### 4.3 WF-03: Archive Control

**Flow Type:** Scheduled cloud flow  
**Trigger:** Recurrence — Daily at 02:00 UTC  
**Required Connections:** SharePoint  

**Action Sequence:**

```
[Trigger] Recurrence (daily 02:00 UTC)
  │
  ├── [Action 1] SharePoint: Get items from RAE Document Registry
  │   Filter: Status eq 'obsolete' and ArchivedDate eq null
  │
  ├── [Action 2] Apply to each (loop over results)
  │   │
  │   ├── [Action 3] SharePoint: Get file metadata (by DocumentID / StorageURL)
  │   │
  │   ├── [Action 4] SharePoint: Move file to _Archive folder
  │   │   Destination: /sites/msteams_54adc4/{Library}/_Archive/{filename}
  │   │
  │   ├── [Action 5] SharePoint: Update item in Registry
  │   │   Set ArchivedDate = utcNow()
  │   │   Set Status = "archived"
  │   │
  │   └── [Action 6] Office 365 Outlook: Notify Category Owner (if resolved)
  │
  └── Error handling: Log failures to Compose action
```

---

### 4.4 WF-04: Expiring Review Notification

**Flow Type:** Scheduled cloud flow  
**Trigger:** Recurrence — Daily at 06:00 UTC  
**Required Connections:** SharePoint, Office 365 Outlook  

**Action Sequence:**

```
[Trigger] Recurrence (daily 06:00 UTC)
  │
  ├── [Action 1] Compose: Calculate 30-day threshold
  │   Expression: addDays(utcNow(), 30)
  │
  ├── [Action 2] SharePoint: Get items from RAE Document Registry
  │   Filter: Status ne 'archived' and Status ne 'obsolete'
  │           and ReviewDate le '@{outputs('Compose_Threshold')}'
  │           and ReviewDate ge '@{utcNow()}'
  │
  ├── [Action 3] Condition: Were any items found?
  │   Expression: length(body('Get_items')?['value']) greater than 0
  │
  └── [TRUE Branch — Items approaching review date]
      └── [Action 4] Apply to each
          │
          └── [Action 5] Office 365 Outlook: Send an email
              To: (Category Owner — UNRESOLVED; use Site Admin temporarily)
              Subject: "[RAE-DC] Review due: @{items('Apply_to_each')?['Title']}"
              Body: Document @{items('Apply_to_each')?['RAE_DocumentID']} is due for review
                    by @{items('Apply_to_each')?['ReviewDate']}. Please take action.
```

---

### 4.5 WF-05: Export Foundation

**Flow Type:** Scheduled cloud flow  
**Trigger:** Recurrence — Weekly (Sunday 01:00 UTC)  
**Required Connections:** SharePoint  
**Classification:** READY_WITH_LIMITATIONS  

**Action Sequence:**

```
[Trigger] Recurrence (weekly Sunday 01:00 UTC)
  │
  ├── [Action 1] SharePoint: Get items from RAE Document Registry
  │   Filter: Visibility eq 'public' and Status eq 'current'
  │   Select: Title, RAE_DocumentID, Category, Status, Visibility,
  │           ReviewDate, PublishedDate, StorageURL, Version
  │
  ├── [Action 2] Select: Transform to export schema
  │   Mapping:
  │     documentId  = item()?['RAE_DocumentID']
  │     title       = item()?['Title']
  │     category    = item()?['Category']
  │     status      = item()?['Status']
  │     visibility  = item()?['Visibility']
  │     version     = item()?['Version']
  │     publishedAt = item()?['PublishedDate']
  │     reviewBy    = item()?['ReviewDate']
  │     storageUrl  = item()?['StorageURL']
  │
  ├── [Action 3] Compose: Build JSON envelope
  │   Expression: {
  │     "exportedAt": "@{utcNow()}",
  │     "exportVersion": "1.0",
  │     "documentCount": @{length(body('Get_items')?['value'])},
  │     "documents": @{body('Select')}
  │   }
  │
  ├── [Action 4] SharePoint: Create file
  │   Site: https://maejo365.sharepoint.com/sites/msteams_54adc4
  │   Folder: /sites/msteams_54adc4/Documents/exports
  │   File name: "rae-registry-export-@{formatDateTime(utcNow(),'yyyyMMdd')}.json"
  │   File content: @{outputs('Compose_JSON_Envelope')}
  │
  └── [LIMITATION] GitHub sync requires external action:
      - GitHub Actions workflow triggered by repository dispatch
      - OR: Premium HTTP connector to GitHub API (outside EA-5 scope)
      - STATUS: READY_WITH_LIMITATIONS
```

---

## 5. End-to-End Test Plan (Cannot Execute — Flows Not Running)

The following test plan is documented for execution once flows are manually implemented:

### 5.1 Test Sequence

| Step | Action | Expected Outcome | Verify Via |
|------|--------|-----------------|------------|
| T-01 | Upload test file `TEST_DOC_001.pdf` to `Administration/_Inbox` | WF-01 triggers | Flow run history |
| T-02 | Check RAE Document Registry for new entry | Record created with DocumentID, Status=draft | Registry list view |
| T-03 | Set DocumentStatus = "review" on library item | WF-02 triggers approval | Approvals page |
| T-04 | Approve in Approvals connector | DocumentStatus → "current", Registry Status → "current" | Library + Registry |
| T-05 | Set DocumentStatus = "obsolete" | WF-02 triggers archive path | Flow run history |
| T-06 | Next WF-03 scheduled run | File moved to `_Archive`, Registry ArchivedDate set | SharePoint folder |
| T-07 | Set ReviewDate to today + 15 days | WF-04 triggers next day | Email notification |
| T-08 | Next WF-05 scheduled run | JSON export file created in /exports | SharePoint file |
| T-09 | Check for duplicate Registry records | No duplicates for same file | Registry list filter |
| T-10 | Upload to non-_Inbox folder | WF-01 does NOT create Registry entry | Flow run history |

### 5.2 Cleanup Plan

After test evidence capture:
- Delete test file from `_Inbox` and `_Archive`
- Delete test Registry record
- Delete test export JSON file
- Turn off test flows (keep disabled, not deleted)

---

## 6. Validation Results

| Check | Status | Reason |
|-------|--------|--------|
| No duplicate Registry records | ⛔ CANNOT TEST | No flows running |
| No trigger loops | ⛔ CANNOT TEST | No flows running |
| No permission leakage | ✅ PARTIAL | Folder permissions verified in EA-5A |
| No status vocabulary drift | ✅ SPECIFICATION | Vocabulary separation maintained in specs |

---

## 7. Deviations / Blockers

| Deviation | Severity | Details |
|-----------|----------|---------|
| Power Automate new designer rejects programmatic input | 🔴 CRITICAL | `browser_fill` on Monaco code editor does not update flow model. Dropdown selections don't persist on save. |
| CORS blocks Power Automate API from browser | 🔴 CRITICAL | Direct `fetch()` calls to `make.powerautomate.com/api` fail with CORS/network errors |
| All WF-01 through WF-05 flows = NOT SAVED | 🔴 CRITICAL | Zero flows in tenant; no end-to-end testing possible |
| Category Owner identity unresolved | 🔴 CARRIED | Approval routing, notification routing all blocked |
| MigrationBot service account not provisioned | 🔴 CARRIED | Cannot use system account for automated uploads |
| Term Set deferred | 🔒 KNOWN | Text Tags fallback active per EA-3I decision |

---

## 8. Remediation Path

### Option A — Manual Power Automate UI Implementation (Recommended)

A tenant administrator or Power Automate developer manually creates the flows using the specifications in Section 4 of this report.

**Estimated effort:** 4–6 hours for all 5 workflows (experienced Power Automate developer)

**Prerequisites:**
- Power Automate license for implementation account
- SharePoint connection pre-configured
- Approvals connection pre-configured
- Office 365 Outlook connection pre-configured
- Category Owner email addresses resolved (for WF-02 and WF-04)

**Steps:**
1. Create WF-01 for each of the 6 libraries (or one shared flow with branching)
2. Create WF-02 for each of the 6 libraries (or one shared flow)
3. Create WF-03 (shared — scheduled)
4. Create WF-04 (shared — scheduled)
5. Create WF-05 (shared — scheduled)
6. Enable all flows
7. Run end-to-end test per Section 5.1

### Option B — Power Automate CLI (`pac flow`)

```powershell
# Install Power Platform CLI
rtk run pwsh -Command "winget install Microsoft.PowerPlatformCLI"

# Authenticate
rtk run pwsh -Command "pac auth create --environment Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8"

# Import a flow solution (if packaged as .zip)
rtk run pwsh -Command "pac solution import --path .\rae-dc-flows.zip"
```

**Note:** Requires Power Platform CLI with Dataverse/Power Automate permissions. Flow packages must be exported from another environment or built as solution components.

### Option C — Logic Apps Deployment

Alternative implementation using Azure Logic Apps with ARM templates:
- Requires Azure subscription linked to tenant
- Logic Apps supports ARM template deployment for repeatable, version-controlled flow definitions
- More DevOps-friendly but requires Azure access beyond the current scope

---

## 9. Files Changed

| File | Change |
|------|--------|
| `docs/m365/ea-5b-workflow-implementation-report.md` | **NEW** — This report |
| `docs/m365/ea-5a-governance-workflow-report.md` | Correction: Flow skeleton status updated |

---

## 10. Commit Hash

| Phase | Commit Hash |
|-------|-------------|
| EA-5A (precondition) | `eea468f` |
| EA-5B (this report) | _pending commit_ |

---

## 11. Final Decision

**EA5B_BLOCKED** ⛔

### 11.1 Summary

| Task | Status | Reason |
|------|--------|--------|
| 1. Audit PA flows | ✅ Complete | All 5 flows = NOT FOUND in tenant |
| 2. Implement WF-01 | ❌ BLOCKED | Save failed — List Name required; cannot programmatically configure trigger |
| 3. Implement WF-02 | ❌ BLOCKED | Not attempted — blocked by same constraints |
| 4. Implement WF-03 | ❌ BLOCKED | Not attempted — blocked by same constraints |
| 5. Implement WF-04 | ❌ BLOCKED | Not attempted — blocked by same constraints |
| 6. Implement WF-05 to JSON boundary | ⚠️ SPEC ONLY | Specification complete; no flow saved |
| 7. End-to-end test | ❌ BLOCKED | Requires functional flows |
| 8. Verify no duplicate records | ❌ BLOCKED | Requires functional flows |
| 9. Clean up test artifacts | ✅ N/A | No artifacts created |

### 11.2 Primary Blocker

**Power Automate workflows cannot be created or configured via browser automation.** The new Power Automate designer requires direct human UI interaction for:
- Configuring trigger parameters (site + list name binding)
- Setting dynamic content expressions in condition steps
- Binding connector actions to SharePoint columns
- Saving flows with valid configuration

Browser automation (browser_fill, browser_click, browser_cdp) cannot reliably substitute for this interaction pattern.

### 11.3 What IS Unblocked

The following is complete and ready for EA-6 once flows are implemented manually:

- ✅ 18 governance folders (_Inbox, _Review, _Archive × 6 libraries)
- ✅ Folder permissions per permissions-matrix.md
- ✅ Content types associated and defaults set (EA-4)
- ✅ Library views created (EA-4)
- ✅ Library permissions configured (EA-4)
- ✅ RAE Document Registry schema provisioned (EA-3I.1)
- ✅ Complete workflow specifications (Sections 4.1–4.5 of this report)
- ✅ End-to-end test plan documented (Section 5.1)
- ✅ WF-05 export contract and JSON schema defined

---

## 12. Recommended Next Actions (Before EA-6)

**EA-5B must be re-attempted as a manual Power Automate implementation session before EA-6 can begin.**

Required actions (in order):

1. **[REQUIRED]** Manually implement WF-01 through WF-05 using Section 4 specifications
2. **[REQUIRED]** Run end-to-end test per Section 5.1
3. **[REQUIRED]** Verify no duplicate records, trigger loops, permission leakage, or status vocabulary drift
4. **[REQUIRED]** Clean up test artifacts
5. **[DEPENDENCY]** Resolve Category Owner assignments for WF-02 and WF-04 notification routing
6. **[DEPENDENCY]** Provision `RAE-DC-MigrationBot` service account (if needed for WF-01 bulk path)

**Only after all REQUIRED items are complete:**

> **EA-6 — Migration Pilot with 10–20 Representative Documents**

EA-6 prerequisites (all must be true before starting):
- [ ] EA-5B = `EA5B_WORKFLOWS_VALIDATED` (manual re-run required)
- [ ] Category Owners confirmed and groups populated
- [ ] WF-01 tested: upload → Registry auto-registration confirmed
- [ ] WF-02 tested: approval lifecycle confirmed
- [ ] WF-03 tested: archive move confirmed
- [ ] WF-04 tested: review notification confirmed
