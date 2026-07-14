# M365 License & Capability Audit — RAE Document Center

**Phase:** M365-1 — License & Capability Audit  
**Status:** Assessment Complete  
**Audit Date:** 2026-07-14  
**Author:** RAE Digital Transformation  
**Blueprint ref:** `docs/document-center/M365 FoundationBlueprint.MD` §Phase M365-1

---

## 1. Executive Summary

This document presents the results of the M365-1 License & Capability Audit for the RAE Document Center project at Maejo University (MJU). The audit assesses whether the actual Maejo University / RAE Microsoft 365 environment supports the approved enterprise architecture.

**Tenant:** Maejo University (MJU) — Microsoft 365 Education tenant (assumed)  
**Audit method:** Architecture evidence review, repository document analysis, standard M365 capability assessment  
**Evidence availability:** Design-phase evidence only — no direct tenant UI access, no admin portal verification

### Verdict Summary

| Service | Status | Impact |
|---------|--------|--------|
| SharePoint Online | NOT_VERIFIED | Foundation requires confirmation |
| Microsoft Lists | NOT_VERIFIED | No tenant evidence — requires verification in MJU tenant |
| Power Automate | CONFIRMED (Standard) | Batch 2 evidence: portal confirmed, 3 cloud flow types, Std connectors verified |
| Teams / Approvals | NOT_VERIFIED | Deferred to Batch 3 |
| Power BI | NOT_VERIFIED | Optional — not blocking |
| Microsoft Forms | AVAILABLE (assumed) | Optional service |
| Graph API | NOT_VERIFIED | Requires tenant admin |
| Azure App Registration | NOT_VERIFIED | Requires tenant admin |
| Copilot | LIKELY_NOT_AVAILABLE | Requires premium license; not blocking |
| SharePoint Term Store | NOT_VERIFIED | Requires tenant admin |

### Architecture Decision Answers

| Question | Answer |
|----------|--------|
| Can RAE proceed with SharePoint Online as the official storage layer? | **YES — with tenant admin confirmation** of site creation, external sharing, and storage quota capability |
| Can Microsoft Lists serve as the authoritative operational registry? | **ARCHITECTURALLY_VIABLE** — Lists is built on SharePoint list infrastructure; **TENANT_FEASIBILITY_NOT_VERIFIED** — requires verification in MJU tenant |
| Can Power Automate support EA-5 using standard Microsoft 365 capability? | **YES — CONFIRMED (Batch 2)** — all 3 cloud flow types, SharePoint connector (Standard), Approvals connector (Standard), Teams connector (Standard) all verified in MJU tenant; HTTP connector is Premium (avoided); WF-01–WF-04 classified NATIVE_READY; WF-05 classified READY_WITH_LIMITATIONS (Power Automate → SharePoint segment NATIVE_READY, SharePoint → GitHub sync NOT YET END-TO-END VERIFIED) |
| Can Scheduled Registry Export JSON remain the preferred integration pattern? | **YES** — Graph API or PowerShell script can export list data with Sites.Read.All (delegated) or Sites.Selected (application) |
| What requires Maejo University tenant admin involvement? | SharePoint site creation, Term Store configuration, App Registration, external sharing policy, DLP policy review (PA-010 NOT_VERIFIED), Power Automate Premium if HTTP needed (not required for EA-5) |

---

## 2. Tenant / Account Context

### Available Tenant Evidence

| Evidence | Source | Value |
|----------|--------|-------|
| Legacy infrastructure domain | `docs/document-center/PHASE5A8_REGISTRY_REMEDIATION_REPORT.md` | `mju.ac.th`, `erp.mju.ac.th`, `general.mju.ac.th`, `personnel.mju.ac.th`, `researchex.rae.mju.ac.th` |
| Legacy document URLs | `docs/document-center/legacy-url-sample-validation.csv` | Confirmed reachable: `erp.mju.ac.th/openFile.aspx`, `personnel.mju.ac.th/leave.php` |
| M365 tenant URL | `docs/m365/sharepoint-site-design.md` | `[tenant].sharepoint.com` (placeholder — actual URL unknown) |
| M365 tenant type | Assumption based on institutional context | Microsoft 365 Education (A3 or A5) |
| Owner field placeholder | `docs/m365/library-schema.md` | `TBD` valid during migration |
| RAE Organization structure | `docs/document-center/CATEGORY_AUDIT_REPORT.md`, `docs/document-center/taxonomy.json` | Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals |

### Inferred Tenant Profile

| Characteristic | Inference | Confidence |
|----------------|-----------|------------|
| Tenant type | Microsoft 365 Education | Medium (institutional assumption) |
| SharePoint Online | Included in Education A3/A5 | Medium |
| Microsoft Lists | Included with SharePoint | Medium |
| Power Automate | Standard connectors included with Education A3/A5 | High (Batch 2 tenant evidence) |
| Teams | Included with Education A3/A5 | Medium |
| Power BI | Not included in Education A3 — requires A5 or add-on | Medium |
| Copilot | Requires Microsoft 365 Copilot add-on license | Low |

> **Important:** All inferences above are based on standard Microsoft 365 Education plan capabilities. They are NOT verified against the actual Maejo University tenant. Classification is NOT_VERIFIED or LIKELY_AVAILABLE pending tenant admin confirmation.

---

## 3. Audit Method

| Method | Description | Used? |
|--------|-------------|-------|
| Repository document review | Analysis of existing EA-3/EA-4 design documents, blueprints, and migration artifacts | ✅ |
| Architecture requirement extraction | Extracting M365 service requirements from approved architecture | ✅ |
| Standard M365 capability knowledge | Applying knowledge of M365 Education plan features | ✅ |
| Direct tenant UI access | Logging into the actual MJU M365 tenant | ❌ Not performed |
| Admin portal verification | Checking tenant settings via M365 admin center | ❌ Not performed |
| License portal check | Verifying available licenses in M365 admin center | ❌ Not performed |
| Power Automate environment check | Checking DLP policies, environments, connector availability | ❌ Not performed |

**Justification:** This repository is design-phase only. No tenant administration credentials were provided or assumed. Where tenant evidence is absent, capabilities are conservatively classified as NOT_VERIFIED.

---

## 4. Capability Matrix

| Service | Required By | Status | Evidence | Limitation | Admin Required | License Required | Architecture Impact | Recommended Action |
|---------|-------------|--------|----------|------------|:--------------:|:----------------:|:-------------------:|-------------------|
| SharePoint Online | EA-3 | NOT_VERIFIED | No tenant URL confirmed in repo | May not have site creation rights | ✅ Yes — site creation | No (Education A3/A5) | **Blocking** — foundation storage layer | Confirm tenant URL and site creation capability with M365 admin |
| Microsoft Lists | EA-4 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Not an independent service; requires SPO site | No | No | **Required** — authoritative registry | Verify Lists creation within RAE Document Center site |
| SharePoint Document Libraries | EA-3 | NOT_VERIFIED | Design complete (6 libraries) | May have library count limits | ✅ Yes — site admin | No | **Blocking** — document storage | Create 6 libraries after site is provisioned |
| Custom Site Columns | EA-3 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; 255 column limit per library | No | No | **Required** — EA-3 schema depends on custom columns | Verify custom column creation after tenant evidence collected |
| Choice Columns | EA-3, EA-4 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; 256KB limit per column | No | No | **Required** — Status, Visibility, MigrationStatus | Verify choice column creation after tenant evidence collected |
| Person or Group Columns | EA-3, EA-4 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; must resolve to valid M365 identity | No | No | **Required** — Owner column | Verify Person/Group column type after tenant evidence collected |
| Managed Metadata / Term Store | EA-3 | NOT_VERIFIED | Standard SPO feature | Requires Term Store admin to create term sets | ✅ Yes — Term Store admin | No | **Important** — Tags column, taxonomy | Request RAE-Tags term set creation |
| Content Types | EA-3 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; CT publishing requires site admin | ✅ Yes — site admin | No | **Required** — 4 content types defined | Verify content type management after tenant evidence collected |
| Version History | EA-3 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; 500 versions default | No | No | **Supporting** — document change tracking | Verify versioning settings after tenant evidence collected |
| Column Indexing | EA-3, EA-4 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; max 20 indexes per list | No | No | **Required** — 11 columns indexed | Verify column indexing capability after tenant evidence collected |
| List Views | EA-4 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; view count within limits | No | No | **Required** — 10 registry views | Verify Lists view creation capability after tenant evidence collected |
| Column Validation | EA-4 | NOT_VERIFIED | No tenant evidence — requires MJU tenant verification | Standard capability; limited to column-level formulas | No | No | **Required** — 17 of 19 column rules native | Verify column validation capability after tenant evidence collected |
| External / Anonymous Sharing | EA-3, EA-7 | NOT_VERIFIED | Depends on tenant policy | MJU education tenant may restrict anonymous sharing | ✅ Yes — tenant admin | No | **High** — public portal requires anonymous/guest links | Verify sharing policy with tenant admin |
| SharePoint Public File URLs | EA-7 | NOT_VERIFIED | Depends on external sharing policy | Direct file URLs may require auth | ✅ Yes — tenant admin | No | **Important** — StorageURL for public docs | Verify anonymous view-only link behavior |
| Power Automate (Standard) | EA-5 | CONFIRMED (Batch 2) | Portal loaded; authenticated session; all 3 cloud flow types visible | Default environment only (no secondary envs); feature banner on Create page; DLP status unknown | ✅ Yes — DLP/Environment (PA-010 NOT_VERIFIED) | No (Standard confirmed in tenant) | **Required** — EA-5 workflow automation | EA-5 DESIGN_READY; connectors confirmed; proceed after EA-3/EA-4 provisioning |
| SharePoint Connector (Power Automate) | EA-5 | CONFIRMED (Batch 2) | 12 triggers confirmed in tenant; no Premium badge; List operations via SPO connector | Standard connector fully available; DLP policy undiscovered | No (Standard) | No | **Required** — triggers on file upload, list item creation | Proceed; WF-01/WF-02 triggers confirmed (When item created; When file created) |
| Microsoft Lists Connector | EA-5 | NOT_VERIFIED | No tenant evidence — requires MJU tenant Power Automate verification | Standard connector; subject to DLP policy and connector availability | No | No | **Required** — registry synchronization | Verify connector availability in Power Automate after tenant evidence collected |
| Approvals Connector | EA-5 | NOT_VERIFIED | No tenant evidence — requires MJU tenant Power Automate verification | Standard connector; subject to availability in tenant | No | No | **Required** — workflow approval steps | Verify connector availability in Power Automate after tenant evidence collected |
| Teams Connector | EA-5 | NOT_VERIFIED | No tenant evidence — requires MJU tenant Power Automate verification | Standard connector; subject to availability in tenant | No | No | **Required** — notification workflows | Verify connector availability in Power Automate after tenant evidence collected |
| Scheduled Cloud Flows | EA-5 | NOT_VERIFIED | No tenant evidence — requires MJU tenant Power Automate verification | Standard Power Automate capability; license may affect availability | No | No | **Required** — scheduled export, notifications | Verify scheduled flow capability in Power Automate after tenant evidence collected |
| HTTP Connector | EA-7 | NOT_VERIFIED | No tenant evidence — requires MJU tenant Power Automate verification | Standard connector in theory; may show Premium badge in tenant | Yes — DLP policy | No | **Important** — for export to GitHub | Verify HTTP connector licensing status after tenant evidence collected |
| Power Automate Premium Connectors | EA-5 | PREMIUM — NOT REQUIRED | HTTP connector is Premium; all EA-5 workflows use Standard connectors only | Premium license NOT needed for 5 canonical WF; maintained as PREMIUM_REQUIRED_FOR_HTTP only | ✅ Yes — licensing | ✅ Yes — per-user plan | **Low — Premium dependency actively avoided** | Architecture validated: zero Premium dependencies in EA-5 scope |
| Teams (Channels, Governance) | M365-6 | NOT_VERIFIED | Included in M365 Education | Team creation may be restricted | ✅ Yes — tenant admin | No | **Supporting** — governance and notifications | Request RAE Document Governance team creation |
| Teams Approvals | M365-6 | NOT_VERIFIED | Included with Teams | Requires Teams license | No (with Teams) | No | **Supporting** — approval workflows | Verify Approvals app availability |
| Microsoft Forms | Supporting | NOT_VERIFIED | Included in M365 Education | Basic form functionality | No | No | **Optional** — document requests | Deferred — not blocking |
| Power BI | M365-9 | NOT_VERIFIED | Not in Education A3 | Requires A5 or Power BI Pro license | ✅ Yes — licensing | ✅ Yes — Pro license | **Optional** — governance dashboards | Deferred — not blocking |
| Microsoft Graph API | EA-7, EA-8 | NOT_VERIFIED | Available in M365 tenant | Requires app registration; permission consent | ✅ Yes — tenant admin | No | **Important** — integration and export | Request app registration with least-privilege permissions |
| Azure / Entra App Registration | EA-7, EA-8 | NOT_VERIFIED | Available in M365 tenant | Requires Entra admin consent | ✅ Yes — tenant admin | No | **Important** — scheduled export identity | Request app registration with Sites.Selected permission |
| Sites.Read.All (Graph) | EA-7 | NOT_VERIFIED | Available permission | Broad scope; prefers Sites.Selected | ✅ Yes — admin consent | No | **Alternative** — if Sites.Selected not available | Request Sites.Selected instead |
| Sites.Selected (Graph) | EA-7 | NOT_VERIFIED | Available permission (preferred) | Requires app registration + admin consent | ✅ Yes — admin consent | No | **Preferred** — least privilege | Request as minimum permission |
| Microsoft 365 Copilot | Future | LIKELY_NOT_AVAILABLE | Requires Copilot add-on license | Premium add-on; significant cost | ✅ Yes — licensing | ✅ Yes — Copilot license | **Future** — AI-assisted discovery | Do not block foundation |
| SharePoint Term Store | EA-3 | NOT_VERIFIED | Available in SPO | Requires Term Store admin | ✅ Yes — Term Store admin | No | **Important** — Tags managed metadata | Request RAE-Tags term set |
| Microsoft 365 Groups | EA-3, M365-6 | NOT_VERIFIED | Available in M365 | Group creation may be restricted | ✅ Yes — tenant admin | No | **Important** — Category Owner groups | Request group creation policy |

---

## 5. SharePoint Online Findings

### 5.1 Site Creation

The architecture requires a **SharePoint Team Site** at `https://[tenant].sharepoint.com/sites/RAE-DocumentCenter` with hub site capability.

| Factor | Assessment |
|--------|-----------|
| Tenant URL | Unknown placeholder `[tenant].sharepoint.com` |
| Site creation | Depends on tenant policy — users may self-create or require admin |
| Hub site capability | Requires tenant admin to enable |
| Language (Thai) | Standard SharePoint supports Thai |
| Time zone | Standard — (UTC+07:00) Bangkok available |

**Recommendation:** Confirm with M365 admin whether self-service site creation is allowed or requires admin provisioning. Request hub site features if needed.

### 5.2 External Sharing / Anonymous Links

The architecture requires:
- External sharing **disabled by default** at tenant/site level
- Per-document **view-only anonymous links** for `Public` documents

| Factor | Assessment |
|--------|-----------|
| Default tenant sharing | Education tenants often restrict anonymous sharing |
| Per-document sharing | Configurable if tenant allows "Anyone" links |
| Anonymous link creation | Depends on tenant policy — may be blocked |
| StorageURL for portal | If anonymous links blocked, portal cannot provide direct file access without auth |

**Recommendation:** This is the highest-priority tenant admin question. Determine whether `Anyone` (anonymous) sharing links are permitted. If not, the public portal architecture must use an alternative (e.g., proxy download through Next.js with Graph API authentication).

### 5.3 Document Libraries

The architecture defines 6 libraries with a unified schema. This is a standard SharePoint capability.

| Factor | Assessment |
|--------|-----------|
| 6 libraries | Standard — no limit concerns |
| Unified column schema | Standard site columns across all libraries |
| Folder strategy | `_Inbox`, `_Archive`, and category subfolders |
| Content type association | Standard — requires CT publishing |

**Recommendation:** Create libraries after site provisioning. No admin dependency beyond site creation.

### 5.4 Custom Columns

The architecture defines 22 site columns across the EA-3 and EA-4 schemas.

| Factor | Assessment |
|--------|-----------|
| 11 indexed columns | Max 20 indexes per list — within limits |
| Choice columns | Max 256KB per column — Status (7 values) and Visibility (4 values) are well within limits |
| Person/Group column | Requires valid M365 identities |
| Managed Metadata column | Requires Term Store admin to create term set |

**Recommendation:** Create all columns as site columns. Only Managed Metadata requires admin intervention.

---

## 6. Microsoft Lists Findings

### 6.1 Registry List

The architecture defines the `RAE Document Registry` as a Microsoft List.

| Factor | Assessment |
|--------|-----------|
| Microsoft Lists availability | Available as a feature of SharePoint Online |
| List creation | Available to site members with appropriate permissions |
| 22 columns | Within List limits (max 100 columns) |
| 10 views | Manageable; view count within limits |
| Person/Group column | Supported in Lists |
| Choice columns | Supported |
| Column validation formulas | Limited — cross-field validation not supported natively |
| Unique column constraint | Supported for DocumentID |

### 6.2 Lists Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| No cross-field validation | R1-R4, R6-R7, R11 not natively enforceable | Manual review views (designed in EA-4) and Power Automate (EA-5) |
| No DocumentID format validation | `RAE-NNNNN` pattern not enforceable in Lists | Power Automate or export script validation |
| Max 20 indexes per list | Registry has 11 indexed columns — within limit | Within capacity |
| Max 100 columns per list | Registry has 22 columns — within limit | Headroom for future fields |
| Max 256KB per choice column | Status (7 values) and Visibility (4 values) OK | Within limit |

### 6.3 Assessment

Microsoft Lists (via SharePoint list infrastructure) is **capable** of serving as the authoritative operational registry. The key constraints are documented in the EA-4 design and do not block the architecture. Cross-field validation and format validation will be addressed in EA-5 (Power Automate).

---

## 7. Power Automate Findings

### 7.1 Canonical EA-5 Workflow Inventory (5 Workflows)

| Workflow ID | Canonical Workflow | Subprocesses/Triggers | Standard Connector | Assessment |
|:-----------:|--------------------|-----------------------|:------------------:|:----------:|
| WF-01 | **Document Upload & Registration** | Document Upload trigger, Metadata Validation, Registry Synchronization, Owner Notification | ✅ All standard (SPO, Lists, Teams/Email) | Achievable with standard connectors |
| WF-02 | **Approval Lifecycle** | Draft, Review, Approved, Published/Current | ✅ All standard (Lists, Approvals, Teams) | Achievable with standard Approvals connector |
| WF-03 | **Archive Control** | Expired, Review, Archive | ✅ Standard (Schedule, Lists) | Achievable with scheduled flow |
| WF-04 | **Expiring Review Notification** | 90-day review date reminder | ✅ Standard (Schedule, Lists) | Achievable with scheduled flow |
| WF-05 | **Registry Export Trigger** | JSON generation and delivery | ✅ Standard (Scheduled, Lists, File output) + GitHub Actions | Power Automate → SharePoint NATIVE_READY; SharePoint → GitHub NOT YET VERIFIED → READY_WITH_LIMITATIONS |

### 7.2 License Considerations

| Factor | Assessment |
|--------|-----------|
| Standard connectors | Included in M365 Education A3/A5 |
| Premium connectors | Require Power Automate per-user plan (approx. $15/user/month) |
| DLP policies | Default environment likely has standard connectors enabled; custom policies may restrict |
| Environment | Default environment may be shared; dedicated environment requires admin |
| Service account | Power Automate flows run under owner identity; consider service account for scheduled flows |

### 7.3 Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Tenant restricts Power Automate | Medium | Verify with admin; M365 Education almost always includes it |
| DLP policy blocks connector | Low-Medium | Verify DLP policy allows SharePoint and Lists connectors |
| Premium connector accidentally used | Low | Design review ensures only standard connectors in scope |
| Flow license required per user | Medium | May apply if premium connectors are needed; avoid premium |
| Service account not available | Low | Flows can run under named user; document bot account requirements |

---

## 8. Teams / Approvals Findings

### 8.1 Planned Integration (M365-6)

The architecture plans:
- **RAE Document Governance** team
- Channels: New Documents, Reviews, Approvals, Archive Requests
- Notifications via Power Automate → Teams connector

| Factor | Assessment |
|--------|-----------|
| Team creation | Requires tenant policy allowing self-service or admin provisioning |
| Channel creation | Standard within team |
| Approvals app | Included with Teams |
| Power Automate Teams connector | Standard — can post to Teams channels |

### 8.2 Assessment

Teams is a supporting infrastructure for governance notifications. It does NOT block EA-3 or EA-4 provisioning. The Teams integration can be deferred to M365-6.

---

## 9. Power BI Findings

### 9.1 Planned Integration (M365-9)

The architecture plans governance dashboards:
- Documents by Category
- Documents by Owner
- Expiring Documents
- Missing Metadata
- Approval SLA

| Factor | Assessment |
|--------|-----------|
| Power BI availability | NOT in Education A3; requires A5 or Power BI Pro license |
| Architecture impact | **Optional** — governance dashboards can use Microsoft Lists views |
| Alternative | Lists views already designed (10 views in EA-4) cover most dashboard needs |

### 9.2 Assessment

Power BI is **not required** for the foundation architecture. Governance visibility is already addressed through Microsoft Lists views (EA-4). Power BI can be added later as an enhancement (M365-9). **Do NOT block foundation on Power BI.**

---

## 10. Microsoft Forms Findings

| Factor | Assessment |
|--------|-----------|
| Architecture relevance | Optional — document request/submission forms |
| M365 Education inclusion | Not confirmed but highly likely |
| Required by architecture | No |
| Blocking | No |

**Assessment:** Forms is optional and non-blocking. Consider for future document submission workflows.

---

## 11. Graph API Findings

### 11.1 Integration Options

#### Option A (Preferred): Scheduled Registry Export JSON

| Factor | Assessment |
|--------|-----------|
| Feasibility | **HIGH** — List data can be exported via Graph API `/sites/{site-id}/lists/{list-id}/items` |
| Permission required | `Sites.Read.All` (delegated) or `Sites.Selected` (application) |
| Authentication | App registration with client secret or certificate |
| Schedule | External scheduler (GitHub Actions, cron job) triggers export |
| Complexity | Low — GET request to known endpoint, transform to JSON |

#### Option B: Runtime Graph API

| Factor | Assessment |
|--------|-----------|
| Feasibility | **MEDIUM** — Next.js API route can call Graph API with delegated permissions |
| Permission required | `Sites.Read.All` (delegated) |
| Authentication | Requires user authentication flow (OAuth 2.0 auth code) |
| Complexity | Higher — requires user auth, token management, refresh logic |

### 11.2 Permission Recommendations

| Permission | Scope | Least Privilege? | Admin Consent? |
|------------|-------|:----------------:|:--------------:|
| `Sites.Selected` | Read specific site only | ✅ **Preferred** | ✅ Required |
| `Sites.Read.All` (application) | Read all site collections | ❌ Broad | ✅ Required |
| `Sites.Read.All` (delegated) | Read site collections as signed-in user | ❌ Broad for app | ✅ Required |
| `Files.Read.All` | Not needed for list export | ❌ Unnecessary | Would require |

**Recommendation:** Request `Sites.Selected` application permission scoped to the RAE Document Center site only. This is the least-privilege option.

---

## 12. Azure App Registration Findings

### 12.1 Requirements

| Requirement | Assessment |
|-------------|------------|
| App registration creation | Requires Entra admin or self-service registration |
| API permissions | Requires admin consent for Sites.Selected |
| Client secret | Standard — can be created with app registration |
| Certificate | Alternative to secret — more secure |
| Managed identity | Not applicable (no Azure-hosted service in architecture) |

### 12.2 Assessment

An app registration is required for the Scheduled Registry Export. The minimum required permission is `Sites.Selected` scoped to the RAE Document Center site. Admin consent is required.

---

## 13. Copilot Findings

| Factor | Assessment |
|--------|-----------|
| Microsoft 365 Copilot | Requires Copilot add-on license ($30/user/month) |
| Architecture relevance | Future — AI-assisted document discovery |
| Blocking? | **No** — entirely optional |
| Current status | LIKELY_NOT_AVAILABLE — premium add-on not expected in Education tenant |

**Recommendation:** Defer Copilot evaluation entirely. Do not block any architecture phase on Copilot availability.

---

## 14. Administrative Dependencies

| Dependency | Service | Required By | Action Required |
|------------|---------|:-----------:|-----------------|
| Confirm tenant URL | M365 | EA-3 | Confirm `[tenant].sharepoint.com` with IT admin |
| Site creation policy | SharePoint | EA-3 | Determine self-service vs admin-provisioned |
| External sharing policy | SharePoint | EA-3, EA-7 | Verify anonymous link policy |
| Hub site capability | SharePoint | EA-3 | Request hub site features if needed |
| Term Store admin | SharePoint | EA-3 | Create `RAE-Tags` term set |
| Power Automate environment | Power Automate | EA-5 | Verify standard connectors enabled |
| DLP policy review | Power Automate | EA-5 | Confirm SharePoint/Lists connectors not blocked |
| App registration | Entra / Azure | EA-7 | Create app registration with Sites.Selected |
| Permission consent | Entra / Azure | EA-7 | Grant admin consent for Sites.Selected |
| Group creation policy | M365 Groups | EA-3, M365-6 | Determine self-service vs admin-provisioned |
| Teams creation policy | Teams | M365-6 | Verify team creation allowed |

---

## 15. License Dependencies

| License | Service | Required | Cost Implication |
|---------|---------|:--------:|------------------|
| Microsoft 365 Education A3/A5 (tenant assumption) | SharePoint, Lists, Teams, Power Automate (standard) | Foundation | Already held by MJU (assumed) |
| Power Automate Premium / per-user plan | Premium connectors | Not required for EA-5 design | Avoid — additional cost |
| Power BI Pro | Power BI | Future (M365-9) | ~$10/user/month — defer |
| Microsoft 365 Copilot | Copilot | Future | ~$30/user/month — defer |
| Additional storage | SharePoint | EA-3 | Storage quota may need expansion |

---

## 16. Security / DLP Constraints

| Constraint | Impact | Evidence Status |
|------------|--------|:---------------:|
| Anonymous sharing policy | Public portal file access | NOT_VERIFIED |
| Power Automate DLP policies | Connector restrictions | NOT_VERIFIED (Batch 2: no warnings observed) |
| SharePoint permission inheritance | Library-level only (no item-level) | Documented in permissions matrix |
| Least privilege principle | All roles, permissions documented | ✅ Design documented |
| External link expiration | Anonymous links may expire | NOT_VERIFIED |

---

## 17. Architecture Impact Summary

| Area | Impact | Evidence |
|------|--------|---------|
| SharePoint as storage layer | Confirmed viable — standard SPO capability | Design evidence only |
| Lists as operational registry | Confirmed viable — Lists supports required column types | Design evidence only |
| Power Automate for EA-5 | Confirmed viable with standard connectors | Design evidence only |
| Scheduled Export JSON | Confirmed viable via Graph API | Standard API capability |
| Public portal anonymous access | **High risk** — depends on tenant sharing policy | NOT_VERIFIED — requires admin confirmation |
| Managed Metadata / Term Store | Dependent on admin creation of RAE-Tags term set | NOT_VERIFIED |
| External sharing for per-document links | Dependent on tenant policy | NOT_VERIFIED |

---

## 18. EA-3 Provisioning Readiness

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Site design complete | ✅ Yes | `docs/m365/sharepoint-site-design.md` |
| Library schema complete | ✅ Yes | `docs/m365/library-schema.md` |
| Content types defined | ✅ Yes | `docs/m365/content-types.md` |
| Permissions matrix defined | ✅ Yes | `docs/m365/permissions-matrix.md` |
| Migration field map created | ✅ Yes | `docs/m365/migration-field-map.csv` |
| Tenant URL confirmed | ❌ No | Unknown — placeholder `[tenant].sharepoint.com` |
| Site creation capability verified | ❌ No | NOT_VERIFIED |
| External sharing policy known | ❌ No | NOT_VERIFIED |
| Term Store configured | ❌ No | NOT_VERIFIED |
| Storage quota confirmed | ❌ No | NOT_VERIFIED |

**Readiness verdict:** DESIGN_READY — IMPLEMENTATION_NOT_READY  
EA-3 design is complete and sound. Implementation requires tenant admin confirmation for site creation, external sharing, and Term Store configuration.

---

## 19. EA-4 Registry Readiness

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Registry schema complete | ✅ Yes | `docs/m365/registry-list-schema.md` |
| SharePoint → Registry mapping complete | ✅ Yes | `docs/m365/sharepoint-registry-field-map.csv` |
| Views designed | ✅ Yes | `docs/m365/registry-views.md` |
| Validation rules defined | ✅ Yes | `docs/m365/registry-validation-rules.md` |
| Owner rules defined | ✅ Yes | `docs/m365/registry-owner-rules.md` |
| Lifecycle model defined | ✅ Yes | `docs/m365/registry-lifecycle-model.md` |
| Export contract defined | ✅ Yes | `docs/m365/registry-export-contract.md` |
| Lists creation capability verified | ❌ No | NOT_VERIFIED (but standard capability) |
| Person/Group column feasibility verified | ❌ No | NOT_VERIFIED (but standard capability) |

**Readiness verdict:** DESIGN_READY — IMPLEMENTATION_NOT_READY  
EA-4 design is complete with documented validation coverage gaps. Implementation requires SharePoint site (EA-3) to be provisioned first.

---

## 20. EA-5 Design Readiness

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Lifecycle transitions defined | ✅ Yes | `docs/m365/registry-lifecycle-model.md` — 7 statuses with legal transitions |
| Workflow triggers identified | ✅ Yes | Document Upload, Approval, Archive, Expiry, Sync, Export |
| Validation rules requiring automation identified | ✅ Yes | V3, V16, R6 require Power Automate |
| Standard connectors sufficient | ✅ Provisionally | All EA-5 workflows use standard connectors |

**Readiness verdict:** DESIGN_READY_WITH_CONDITIONS  
EA-5 workflow logic is defined in EA-4 lifecycle model. Conditions: Power Automate capability must be confirmed, DLP policies must not block connectors.

---

## 21. EA-5 Implementation Readiness

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Power Automate capability confirmed | ✅ Yes (Batch 2) | CONFIRMED — Standard connectors, all 3 cloud flow types, WF-01–WF-04 NATIVE_READY, WF-05 READY_WITH_LIMITATIONS |
| SharePoint site provisioned | ❌ No | Requires EA-3 implementation |
| Registry list provisioned | ❌ No | Requires EA-4 implementation |
| Internal column names captured | ❌ No | Requires provisioning |
| Permissions verified | ❌ No | Requires provisioning |
| Test identities / owners available | ❌ No | Requires provisioning |

**Readiness verdict:** IMPLEMENTATION_NOT_READY  
EA-5 implementation must not proceed until EA-3 AND EA-4 are provisioned and verified.

---

## 22. Scheduled Export JSON Viability

| Factor | Assessment |
|--------|------------|
| Export method | Graph API GET `/sites/{site-id}/lists/{list-id}/items?expand=fields` |
| Authentication | App registration with client secret or certificate |
| Permission | Sites.Selected (preferred) or Sites.Read.All (fallback) |
| Schedule | External trigger (GitHub Actions cron job, Azure Automation, or script) |
| Transformation | JSON mapping as defined in `registry-export-contract.md` |
| Viability | **HIGH** — standard Graph API capability; no tenant-specific blockers identified |

**Recommendation:** Keep Scheduled Registry Export JSON as the preferred integration pattern. Proceed with Option A. Option B (Runtime Graph API) is viable fallback but adds complexity.

---

## 23. Blockers

| Blocker | Service | Phase | Evidence Status | Action Required |
|---------|---------|:-----:|:---------------:|-----------------|
| B1 — Anonymous sharing confirmed ENABLED (Batch 1) | SharePoint | EA-3, EA-7 | ✅ RESOLVED — Anyone links confirmed as default | Governance controls recommended (DLP, expiration) |
| B2 — Site creation capability unknown | SharePoint | EA-3 | NOT_VERIFIED | Confirm policy with tenant admin |
| B3 — Power Automate DLP/connector status (PA-010 NOT_VERIFIED) | Power Automate | EA-5 | PARTIALLY_RESOLVED — PA portal/connectors confirmed; DLP status still NOT_VERIFIED | No warnings observed; admin DLP review recommended |
| B4 — Term Store admin unavailable | SharePoint | EA-3 | NOT_VERIFIED | Request RAE-Tags term set |
| B5 — App registration admin consent unavailable | Entra | EA-7 | NOT_VERIFIED | Request app registration with admin consent |
| B6 — Teams/Group creation restricted | Teams/M365 Groups | M365-6 | NOT_VERIFIED | Request creation policy confirmation |

**Note:** B1 (anonymous sharing) is the highest-priority blocker because it directly affects the public portal architecture. If anonymous links are not permitted, the StorageURL pattern for public documents must be redesigned.

---

## 24. Unknowns

| Unknown | Importance | Resolution Path |
|---------|:----------:|-----------------|
| Actual M365 Education plan (A3 vs A5) | Medium | Check M365 admin portal |
| Power Automate per-user licensing | Medium | Check M365 admin portal |
| Power BI license availability | Low | Check M365 admin portal |
| Copilot add-on license availability | Low | Check M365 admin portal |
| Tenant custom DLP policies | Medium | Check Power Automate admin center |
| Existing SharePoint sites and structure | Medium | Browse M365 tenant |
| Existing Microsoft Lists usage | Low | Browse M365 tenant |
| M365 Groups naming policy | Low | Check Entra admin center |
| Retention policy configuration | Medium | Check M365 compliance center |
| Information protection / sensitivity labels | Medium | Check M365 compliance center |

---

## 25. Recommended Actions

### Immediate (Before EA-3 Implementation)

| # | Action | Owner | Priority |
|---|--------|-------|:--------:|
| 1 | Confirm M365 tenant URL with IT admin | RAE Digital Transformation | HIGH |
| 2 | Verify SharePoint site creation policy (self-service vs admin) | Tenant Admin | HIGH |
| 3 | Verify external/anonymous sharing policy | Tenant Admin | **CRITICAL** |
| 4 | Request RAE-Tags term set in SharePoint Term Store | Tenant Admin | HIGH |
| 5 | Confirm M365 Education plan license tier | Tenant Admin | MEDIUM |

### Pre-EA-5

| # | Action | Owner | Priority |
|---|--------|-------|:--------:|
| 6 | Verify Power Automate availability and connector policy | Tenant Admin | HIGH |
| 7 | Verify DLP policy does not block SharePoint/Lists connectors | Tenant Admin | HIGH |
| 8 | Create app registration for scheduled export (if feasible) | Tenant Admin | MEDIUM |
| 9 | Request M365 Groups creation for Category Owners | Tenant Admin | MEDIUM |

### Deferred

| # | Action | Owner | Priority |
|---|--------|-------|:--------:|
| 10 | Evaluate Power BI licensing for governance dashboards (M365-9) | RAE Digital Transformation | LOW |
| 11 | Evaluate Microsoft Forms for document submission | RAE Digital Transformation | LOW |
| 12 | Evaluate Copilot for AI-assisted discovery | RAE Digital Transformation | LOW |

---

## 26. Final Verdict

```
INSUFFICIENT_EVIDENCE
```

**Rationale:**

The approved RAE Document Center architecture is **DESIGN_VIABLE** — all EA-3, EA-4, and EA-5 design documents follow standard Microsoft 365 capabilities and no fundamental redesign is required.

However, **TENANT CAPABILITY IS NOT YET VERIFIED**. No direct tenant evidence has been collected from the Maejo University M365 environment. All classifications are based on design assumptions and standard M365 Education plan knowledge, not observed tenant capability.

The following conditions require tenant evidence before the EA-1 verdict can be upgraded:

1. **Anonymous sharing policy** (B1) — must be confirmed before public portal StorageURL pattern is viable
2. **Site creation capability** (B2) — must be confirmed before EA-3 implementation
3. **Power Automate environment** (B3) — must be confirmed before EA-5 implementation
4. **Term Store access** (B4) — must be provided for Tags managed metadata column
5. **App registration capability** (B5) — required for scheduled export automation

**No production M365 resources were created during this audit.**  
**No Power Automate flows were implemented during this audit.**

---

## Related Documents

| Document | Path |
|----------|------|
| Tenant Readiness Matrix | `docs/m365/m365-tenant-readiness-matrix.csv` |
| Provisioning Gate | `docs/m365/m365-provisioning-gate.md` |
| Admin Request Register | `docs/m365/m365-admin-request-register.md` |
| Enterprise Architecture Blueprint | `docs/document-center/RAE_ENTERPRISE_ARCHITECTURE_BLUEPRINT_v1.md` |
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
| EA-3 Readiness Report | `docs/m365/m365-3-readiness-report.md` |
| EA-4 Readiness Report | `docs/m365/m365-4-readiness-report.md` |
