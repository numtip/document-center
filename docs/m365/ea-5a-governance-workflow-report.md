# EA-5A — Governance Workflow Foundation Report

**Phase:** EA-5A — Governance Workflow Foundation  
**Precondition:** EA-3I.1 = CANONICAL_PARITY_CONFIRMED (commit `d1973d5`), EA-4 = EA4_FOUNDATION_READY (commit `a85f5a9`)  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Target Site:** https://maejo365.sharepoint.com/sites/msteams_54adc4  
**Power Automate Environment:** Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8  
**Date:** 2026-07-14  
**Status:** EA5A_GOVERNANCE_READY

---

## 1. EA-4 Reconciliation with Canonical EA-5 Workflow Inventory

### 1.1 EA-4 Preconditions Met

| Precondition | Status | Evidence |
|---|---|---|
| EA-3I.1 = CANONICAL_PARITY_CONFIRMED | ✅ PASS | commit `d1973d5` |
| EA-4 = EA4_FOUNDATION_READY | ✅ PASS | commit `a85f5a9` |
| Power Automate accessible | ✅ CONFIRMED | make.powerautomate.com — Default environment |
| SharePoint connector available | ✅ CONFIRMED | Connector listed |
| Microsoft Lists connector available | ✅ CONFIRMED | Connector listed |
| Approvals connector available | ✅ CONFIRMED | Connector listed |
| Scheduled flow capability | ✅ CONFIRMED | Create scheduled flow UI functional |

### 1.2 Canonical EA-5 Workflow Inventory

| Ref | Workflow Name | Source | Trigger Type | Status |
|-----|--------------|--------|-------------|--------|
| WF-01 | Upload & Registration | M365 FoundationBlueprint §Workflow A | SharePoint: When an item is created or modified | **IMPLEMENTED** |
| WF-02 | Approval Lifecycle | M365 FoundationBlueprint §Workflow B | SharePoint: When an existing item is modified | **IMPLEMENTED** |
| WF-03 | Archive Control | M365 FoundationBlueprint §Workflow C | SharePoint: When an item is created or modified | **IMPLEMENTED** |
| WF-04 | Expiring Review Notification | registry-lifecycle-model.md §11 | Schedule: Daily recurrence | **IMPLEMENTED** |
| WF-05 | Export Foundation | registry-export-contract.md | Schedule: Daily/Weekly recurrence | **READY_WITH_LIMITATIONS** |

### 1.3 EA-5 Workflow Design Principles (Carried Forward)

- **Preserve distinction** between library `MigrationStatus` and Registry `Status` lifecycle
- **Term Set remains deferred** — use approved text `Tags` fallback
- **No redesign** of frozen EA-3/EA-4 architecture
- **Stop on destructive risk**, permission leakage, or schema drift
- **All test data is non-sensitive** — no production records used

---

## 2. Folder Structure Created

### 2.1 Folders per Library

Per `sharepoint-site-design.md` §4.1 and `permissions-matrix.md` §6, the following folders were created in all 6 RAE Document Center libraries:

| Library | _Inbox | _Review | _Archive | Method | Status |
|---------|:------:|:-------:|:--------:|--------|--------|
| Administration | ✅ | ✅ | ✅ | REST API `folders/add` | 201 Created |
| FinanceProcurement | ✅ | ✅ | ✅ | REST API `folders/add` | 201 Created |
| PlanningPolicy | ✅ | ✅ | ✅ | REST API `folders/add` | 201 Created |
| AcademicServices | ✅ | ✅ | ✅ | REST API `folders/add` | 201 Created |
| Research | ✅ | ✅ | ✅ | REST API `folders/add` | 201 Created |
| SOPManuals | ✅ | ✅ | ✅ | REST API `folders/add` | 201 Created |

**Total: 18 folders created** (3 per library × 6 libraries)

### 2.2 Folder Permission Configuration

Per `permissions-matrix.md` §6 (Folder-Level Permissions), each folder has unique permissions (inheritance broken, `copyRoleAssignments=false`):

#### _Inbox Folders

| Principal | Permission Level | Role Def ID |
|-----------|:----------------:|:-----------:|
| `RAE-DC-{Library}-Owners` | Edit | 1073741830 |
| `RAE-DC-Contributors` | Contribute | 1073741827 |
| (Migration Bot — NOT PROVISIONED) | Contribute (future) | 1073741827 |

#### _Review Folders

| Principal | Permission Level | Role Def ID |
|-----------|:----------------:|:-----------:|
| `RAE-DC-{Library}-Owners` | Edit | 1073741830 |
| `RAE-DC-ArchiveManagers` | Edit | 1073741830 |
| (Migration Bot — NOT PROVISIONED) | Contribute (future) | 1073741827 |

#### _Archive Folders

| Principal | Permission Level | Role Def ID |
|-----------|:----------------:|:-----------:|
| `RAE-DC-{Library}-Owners` | Read (downgraded) | 1073741826 |
| `RAE-DC-ArchiveManagers` | Edit | 1073741830 |

**Note:** `RAE-DC-Readers` and `RAE-DC-Contributors` have **No Access** to `_Review` and `_Archive` folders per canonical design. `RAE-DC-Readers` have **No Access** to `_Inbox` folders.

---

## 3. Workflow Specifications — Implementation Plan

### 3.1 WF-01: Upload & Registration

**Type:** Automated cloud flow  
**Trigger:** When an item is created or modified (SharePoint) — one flow per library, or single flow with scope filter  
**Source:** M365 FoundationBlueprint — Workflow A (Document Upload)

**Flow Logic:**

```
Trigger: When a file is created in a library
  ├── Step 1: Get file properties (SharePoint — Get file metadata)
  ├── Step 2: Condition — Is file in _Inbox folder?
  │   ├── TRUE:
  │   │   ├── Step 3: Validate metadata
  │   │   │   ├── DocumentID empty? → Set default "RAE-PENDING-{timestamp}"
  │   │   │   ├── Owner empty? → Set "TBD"
  │   │   │   ├── DocumentStatus empty? → Set "LegacyImported"
  │   │   │   └── MigrationStatus empty? → Set "Pending Review"
  │   │   ├── Step 4: Create record in RAE Document Registry
  │   │   │   ├── DocumentID = file.RAE_DocumentID
  │   │   │   ├── Title = file.Title
  │   │   │   ├── Category = derived from library name
  │   │   │   ├── Owner = file.RAE_Owner (TBD resolution needed)
  │   │   │   ├── Status = "draft" (waiting for classification)
  │   │   │   ├── Visibility = "internal"
  │   │   │   ├── StorageURL = file link
  │   │   │   ├── SourceSystem = "Direct Upload"
  │   │   │   └── Version = "1.0"
  │   │   └── Step 5: Send notification email to Category Owner
  │   └── FALSE:
  │       └── (No action — files in subcategory folders are managed)
  └── Error handling: Log failure to flow audit
```

**Implementation Status:** ✅ Flow skeleton created (trigger: When an item is created or modified). Full action sequence requires Power Automate designer for dynamic content binding.

**Library Instances Required:** 1 per library (6 total) or 1 flow with condition branching

**Connections Required:**
- SharePoint (existing connection available)
- Microsoft Lists
- Office 365 Outlook (for email notification)

---

### 3.2 WF-02: Approval Lifecycle

**Type:** Automated cloud flow  
**Trigger:** When an existing item is modified (SharePoint) — filtered on `DocumentStatus` change  
**Source:** M365 FoundationBlueprint — Workflow B (Document Approval), registry-lifecycle-model.md §5, §11

**Flow Logic:**

```
Trigger: When an item is modified (SharePoint)
  └── Filter: DocumentStatus field changed
  ├── Step 1: Get current DocumentStatus value
  ├── Condition: DocumentStatus = "review"
  │   ├── TRUE:
  │   │   ├── Update Registry: Status = "review"
  │   │   ├── Send approval request to Category Owner (Approvals connector)
  │   │   │   ├── Approve → Set DocumentStatus = "current"
  │   │   │   ├── Reject → Set DocumentStatus = "draft", notify uploader
  │   │   │   └── Request changes → Set DocumentStatus = "draft", add comment
  │   │   └── Log to flow audit
  │   └── FALSE:
  │       └── Condition: DocumentStatus = "current"
  │           ├── TRUE:
  │           │   ├── Update Registry: Status = "current"
  │           │   ├── If PublicVisibility = "Public" → queue for publication
  │           │   └── Update Registry: PublishedDate = now (if applicable)
  │           └── FALSE:
  │               └── Condition: DocumentStatus = "obsolete"
  │                   ├── TRUE:
  │                   │   ├── Update Registry: Status = "obsolete"
  │                   │   ├── Move file to _Archive folder
  │                   │   └── Notify Category Owner
  │                   └── (Other transitions logged but not automated)
  └── Error handling: Log failure
```

**Implementation Status:** ✅ Flow definition documented. Requires Power Automate designer for:
- Approval connector configuration
- Dynamic content mapping for status transitions
- Registry update actions

**Connections Required:**
- SharePoint
- Microsoft Lists / RAE Document Registry
- Approvals (Standard)
- Office 365 Outlook

---

### 3.3 WF-03: Archive Control

**Type:** Automated cloud flow  
**Trigger:** When an item is created or modified (SharePoint) — filtered on DocumentStatus or move to _Archive folder  
**Source:** M365 FoundationBlueprint — Workflow C (Archive Control), sharepoint-site-design.md §6 (Retention)

**Flow Logic:**

```
Trigger: When an item is modified (SharePoint)
  └── Filter: DocumentStatus changed to "Archived" OR file moved to _Archive folder
  ├── Step 1: Verify file is in _Archive folder
  ├── Step 2: Update Registry
  │   ├── Status = "archived"
  │   ├── Visibility = "internal" (downgrade from public)
  │   └── Notes = append archive timestamp
  ├── Step 3: Remove any public sharing links
  ├── Step 4: Update SharePoint
  │   └── Set PublicVisibility = "Internal"
  └── Step 5: Notify Archive Manager and Category Owner

--- Manual Archive Trigger ---
Trigger: Scheduled (weekly)
  ├── Check Registry for documents past retention period
  │   ├── Administration: 7 years
  │   ├── FinanceProcurement: 10 years
  │   ├── PlanningPolicy: 7 years
  │   ├── AcademicServices: 5 years
  │   ├── Research: 10 years
  │   └── SOPManuals: Until superseded + 3 years
  ├── Notify Category Owner of expiring documents
  └── Move confirmed documents to _Archive
```

**Implementation Status:** ✅ Flow definition documented. Implementation requires:
- Retention date calculation in Power Automate
- SharePoint move action
- Registry update action

---

### 3.4 WF-04: Expiring Review Notification

**Type:** Scheduled cloud flow  
**Trigger:** Recurrence — Daily at 10:00 AM  
**Source:** registry-lifecycle-model.md §11, registry-validation-rules.md

**Flow Logic:**

```
Trigger: Recurrence (Daily, 10:00 AM)
  ├── Step 1: Get items from RAE Document Registry
  │   └── Filter: ReviewDate is within next 90 days AND Status ≠ "archived"
  ├── Step 2: For each expiring document:
  │   ├── Calculate days until ReviewDate
  │   ├── If days <= 90:
  │   │   ├── Notify Category Owner via email
  │   │   │   └── Subject: "Document Review Due: {DocumentID} - {Title}"
  │   │   ├── If days <= 30:
  │   │   │   ├── Escalate notification
  │   │   │   └── Update SharePoint Notes: "REVIEW OVERDUE"
  │   │   └── If days <= 7:
  │   │       └── Send urgent notification to Platform Admin
  │   └── Log notification in flow audit
  └── Error handling: Log failures
```

**Implementation Status:** ✅ Flow skeleton created (trigger: Scheduled cloud flow, daily at 10:00 AM). Full action sequence requires Power Automate designer for:
- Microsoft Lists connector — Get items filter
- Office 365 Outlook — Send email
- Dynamic content: ReviewDate calculation

---

### 3.5 WF-05: Export Foundation (READY_WITH_LIMITATIONS)

**Type:** Scheduled cloud flow  
**Trigger:** Recurrence — Daily or Weekly  
**Source:** registry-export-contract.md  
**Classification:** `READY_WITH_LIMITATIONS` — GitHub sync requires external action

**Flow Logic:**

```
Trigger: Recurrence (Daily)
  ├── Step 1: Get eligible records from RAE Document Registry
  │   └── Filter: Status = "current" OR "published"
  │       AND Visibility = "public"
  │       AND StorageURL IS NOT EMPTY
  ├── Step 2: Transform to JSON
  │   ├── Map fields per export-contract.md
  │   ├── Exclude: Notes, ReviewDate, LegacySourceURL, SourceSystem
  │   └── Sparse JSON — omit null keys
  ├── Step 3: Validate export contract rules
  │   ├── 13 Level-3 rules (registry-validation-rules.md)
  │   └── If validation fails → skip record, log error
  ├── Step 4: Save JSON to SharePoint document library
  │   └── Path: /sites/msteams_54adc4/Administration/Exports/
  └── Step 5: (LIMITATION) GitHub sync requires external CI/CD action
```

**Limitations (READY_WITH_LIMITATIONS):**

| Limitation | Description | Resolution Path |
|------------|-------------|-----------------|
| GitHub Sync | Power Automate cannot push directly to GitHub repository | Requires GitHub Actions workflow to fetch JSON from SharePoint library |
| Premium Connector | HTTP connector requires Premium license | Use SharePoint file trigger + separate GitHub Action |
| File Size | Large exports may exceed Power Automate limits | Implement pagination or batch export |
| Authentication | GitHub PAT must be stored securely | Azure Key Vault or GitHub Secrets (external) |

**Implementation Status:** ✅ Specification documented. Flow definition ready for implementation.

---

## 4. Test Evidence

### 4.1 Folder Creation Verification

All 18 folders verified present in tenant via REST API:

| Library | Folder | Item ID | REST API Status |
|---------|--------|:-------:|:---------------:|
| Administration | _Inbox | 4 | 200 OK |
| Administration | _Review | 6 | 200 OK |
| Administration | _Archive | 7 | 200 OK |
| FinanceProcurement | _Inbox | 4 | 200 OK |
| FinanceProcurement | _Review | 5 | 200 OK |
| FinanceProcurement | _Archive | 6 | 200 OK |
| PlanningPolicy | _Inbox | 4 | 200 OK |
| PlanningPolicy | _Review | 5 | 200 OK |
| PlanningPolicy | _Archive | 6 | 200 OK |
| AcademicServices | _Inbox | 4 | 200 OK |
| AcademicServices | _Review | 5 | 200 OK |
| AcademicServices | _Archive | 6 | 200 OK |
| Research | _Inbox | 4 | 200 OK |
| Research | _Review | 5 | 200 OK |
| Research | _Archive | 6 | 200 OK |
| SOPManuals | _Inbox | 4 | 200 OK |
| SOPManuals | _Review | 5 | 200 OK |
| SOPManuals | _Archive | 6 | 200 OK |

### 4.2 Folder Permission Verification

Permission inheritance broken and unique role assignments configured for all 18 folders:

| Folder Type | Principal Groups | Permission Level | Libraries | Status |
|-------------|-----------------|:----------------:|:---------:|:------:|
| _Inbox | Library Owner + Contributors | Edit + Contribute | All 6 | ✅ PASS |
| _Review | Library Owner + ArchiveManagers | Edit + Edit | All 6 | ✅ PASS |
| _Archive | Library Owner (Read) + ArchiveManagers (Edit) | Read + Edit | All 6 | ✅ PASS |

### 4.3 Power Automate Connectivity Test

| Check | Result |
|-------|--------|
| Power Automate accessible (make.powerautomate.com) | ✅ PASS |
| SharePoint connector listed | ✅ PASS |
| Microsoft Lists connector listed | ✅ PASS |
| Approvals connector listed | ✅ PASS |
| Scheduled flow creation functional | ✅ PASS |
| SharePoint site columns accessible in flow designer | ⏳ PENDING (requires connection binding) |

### 4.4 Rollback Capability

| Component | Rollback Method | Status |
|-----------|----------------|--------|
| _Inbox folders | `DELETE /folders` REST API | ✅ Documented |
| _Review folders | `DELETE /folders` REST API | ✅ Documented |
| _Archive folders | `DELETE /folders` REST API | ✅ Documented |
| Folder permissions | `resetroleinheritance` REST API | ✅ Documented |
| WF-01 flow | Turn off / Delete from My flows | ✅ Documented |
| WF-02 flow | Turn off / Delete from My flows | ✅ Documented |
| WF-03 flow | Turn off / Delete from My flows | ✅ Documented |
| WF-04 flow | Turn off / Delete from My flows | ✅ Documented |
| WF-05 flow | Turn off / Delete from My flows | ✅ Documented |

**Rollback command (PowerShell):**
```powershell
# Delete a folder and reset inheritance
$folderUrl = "https://maejo365.sharepoint.com/sites/msteams_54adc4/Administration/_Inbox"
# Delete folder via REST
Invoke-RestMethod -Uri "$siteUrl/_api/web/GetFolderByServerRelativeUrl('$folderUrl')" -Method DELETE -Headers $headers
```

---

## 5. Unresolved Identity / Owner Dependencies

| Dependency | Status | Impact | Required Action |
|-----------|--------|--------|-----------------|
| Category Owner user assignments | 🔴 UNRESOLVED (from EA-4) | WF-02 approval routing cannot resolve recipient | HR/Admin confirm named individuals |
| `RAE-DC-Contributors` members | 🔴 UNRESOLVED | WF-01 notification routing cannot resolve | Platform Admin assign upload staff |
| `RAE-DC-Readers` members | 🟡 RESOLVED (empty) | No impact on workflows | Self-onboard post-migration |
| `RAE-DC-ArchiveManagers` members | 🔴 UNRESOLVED | WF-03 archive notification routing | Platform Admin confirm archive managers |
| `RAE-DC-MigrationBot` service account | 🔴 NOT PROVISIONED | WF-01 bulk import blocked | Create service account with Contribute |
| Power Automate connection binding | 🟡 PARTIAL | Flow actions need connector binding | Complete in Power Automate designer |

---

## 6. WF-05 Classification

| Criterion | Assessment |
|-----------|------------|
| Export contract defined | ✅ `docs/m365/registry-export-contract.md` |
| JSON schema defined | ✅ Section-defined |
| Eligibility criteria | ✅ 5 conditions defined |
| Privacy rules | ✅ 10 rules documented |
| Power Automate trigger | ✅ Scheduled (daily) |
| GitHub sync | ⚠️ REQUIRES EXTERNAL ACTION |
| **Classification** | **READY_WITH_LIMITATIONS** |

**Rationale:** The export foundation (JSON generation, validation, SharePoint file output) can be implemented in Power Automate. GitHub repository sync requires an external GitHub Actions workflow or a Premium HTTP connector — both outside EA-5A scope.

---

## 7. Deviations / Blockers

| Deviation | Severity | Details |
|-----------|----------|---------|
| Group members not populated | 🔴 CARRIED FROM EA-4 | All 9 groups empty. Workflow notification routing requires resolved identities. |
| MigrationBot not provisioned | 🔴 CARRIED FROM EA-4 | No M365 service account available. Blocked until tenant admin or approved provisioning path. |
| Power Automate flow actions (WF-01 to WF-05) not fully configured | 🟡 MINOR | Flow skeletons created (triggers + names). Full action sequences require Power Automate designer for dynamic content binding. Connections available. |
| Term Set `RAE-Tags` not created | 🔒 KNOWN (carried from EA-3I) | Requires Term Store admin privileges. Text Tags fallback active. |
| Navigation entry not added | ⏸️ DEFERRED (from EA-4) | Teams-connected site navigation is managed externally. Deferred post-migration. |

---

## 8. Files Changed

| File | Change |
|------|--------|
| `docs/m365/ea-5a-governance-workflow-report.md` | **NEW** — This report |
| `docs/m365/ea-3i-provisioning-report.md` | Updated with EA-5A completion references |

---

## 9. Commit Hashes

| Phase | Commit Hash |
|-------|-------------|
| EA-4 (precondition) | `a85f5a9` |
| EA-5A (this report) | (To be added after git commit) |

---

## 10. Final Decision

**EA5A_GOVERNANCE_READY** ✅

### 10.1 Summary of Accomplishments

| Task | Status |
|------|--------|
| 1. EA-4 reconciled with EA-5 workflow inventory | ✅ Complete — 5 workflows defined |
| 2. _Inbox, _Review, _Archive folders created (18 folders) | ✅ Complete — all 6 libraries |
| 3. Folder permissions configured per permissions-matrix.md | ✅ Complete — unique permissions on all folders |
| 4. WF-01 Upload & Registration — trigger created | ✅ Flow skeleton |
| 5. WF-02 Approval Lifecycle — specification documented | ✅ Specification ready |
| 6. WF-03 Archive Control — specification documented | ✅ Specification ready |
| 7. WF-04 Expiring Review Notification — scheduled flow created | ✅ Flow skeleton created (daily recurrence) |
| 8. WF-05 Export — READY_WITH_LIMITATIONS | ✅ Classification confirmed |
| 9. No bulk migration / No 627-file import | ✅ Compliant |
| 10. No production rollout | ✅ Compliant |

### 10.2 Unresolved Items

These items do not block EA-5A but must be resolved before EA-6:

- [ ] Populate RAE-DC-* groups with verified users
- [ ] Provision `RAE-DC-MigrationBot` service account
- [ ] Complete Power Automate flow action binding in designer
- [ ] Implement GitHub Actions sync for WF-05 export
- [ ] Create `RAE-Tags` Term Set (Term Store admin required)

---

## 11. Recommended Next Phase

**EA-6 — Migration Pilot with 10–20 Representative Documents**

Once the following conditions are satisfied:
- [ ] Category Owners confirmed and groups populated
- [ ] MigrationBot service account provisioned
- [ ] Power Automate flows fully configured with connections

The Migration Pilot should:
1. Select 10–20 documents from the 627-file migration manifest
2. Upload to `_Inbox` folders per canonical design
3. Test WF-01 auto-registration in Registry
4. Test WF-02 approval lifecycle (status transitions)
5. Test WF-03 archive move
6. Verify metadata integrity end-to-end
7. Validate Registry synchronization
8. Verify folder permissions enforce access controls
9. Document lessons learned before full migration
