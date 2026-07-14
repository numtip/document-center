# M365 Tenant Capability Audit Plan — RAE Document Center

**Version:** 1.0  
**Status:** Plan only — no audit executed  
**Date:** 2026-07-12  
**Authority:** EA-3F Forward Architecture Readiness

---

## Purpose

Define the evidence and methods required to verify M365 tenant capabilities for the RAE Document Center target architecture. This is an **audit plan only** — no tenant capabilities are claimed as available in this document. Every capability must be verified against the actual tenant before EA-3F SharePoint provisioning can proceed.

---

## Audit Scope

All M365 services referenced in the [M365 Foundation Blueprint](../document-center/M365%20FoundationBlueprint.MD) Phase M365-1 audit checklist, plus services identified during EA gap analysis.

---

## Decision Values

| Value | Meaning |
|-------|---------|
| **AVAILABLE** | Service is present in tenant, licensed for target users, and usable for RAE Document Center requirements |
| **LIMITED** | Service is present but with constraints (e.g., limited licensing, feature restrictions, regional unavailability) |
| **NOT_AVAILABLE** | Service is not present in tenant or not licensed for target users |
| **NOT_VERIFIED** | Audit has not been completed for this capability |

---

## Audit Targets

### 1. SharePoint Online

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | SharePoint Online service plan active in tenant. License assigned to RAE users. Communication site creation permitted. External sharing settings configurable. |
| **Validation method** | 1. Log in to Microsoft 365 Admin Center → Billing → Licenses → verify SharePoint Online (Plan 1 or 2) is assigned. 2. SharePoint Admin Center → verify "Create site" is not disabled. 3. Verify external sharing is enabled at tenant level (required for public documents). 4. Test: create a temporary Communication site (to be deleted after audit). |
| **Expected verification source** | M365 Admin Center (admin.microsoft.com) |
| **Architecture impact** | **CRITICAL** — SharePoint Online is the target storage layer. Without it, EA-3F cannot proceed. |
| **EA phase dependency** | EA-3F (SharePoint Foundation) — blocked until AVAILABLE |

---

### 2. Microsoft Lists

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Microsoft Lists available within the tenant. List creation permitted. Column types support choice, person, date, hyperlink, and multi-line text columns. |
| **Validation method** | 1. Navigate to `lists.microsoft.com` in tenant context. 2. Create a test list with one column of each required type (Choice, Person, Date/Time, Hyperlink, Multiple lines of text). 3. Verify list can be shared to target users. 4. Delete test list after audit. |
| **Expected verification source** | M365 tenant (lists.microsoft.com or SharePoint Admin Center) |
| **Architecture impact** | **CRITICAL** — Microsoft Lists is the target authoritative metadata registry. The entire governance model depends on Lists as the registry. |
| **EA phase dependency** | EA-3F (SharePoint Foundation), EA-3G (Lists Registry) — blocked until AVAILABLE |

---

### 3. Power Automate

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Power Automate license included in tenant plan. Flow creation permitted. SharePoint and Lists connectors available. Approval connector available. |
| **Validation method** | 1. Navigate to `make.powerautomate.com` in tenant context. 2. Verify "Create" button is active. 3. Check connector list for SharePoint, Microsoft Lists, Approvals, and Microsoft Teams connectors. 4. Create a minimal test flow with a manual trigger (do not connect production resources). 5. Delete test flow after audit. |
| **Expected verification source** | Power Automate portal (make.powerautomate.com) |
| **Architecture impact** | **HIGH** — Power Automate governs the document lifecycle (Upload, Approval, Archive Control workflows per Blueprint Phases M365-5). |
| **EA phase dependency** | EA-3H (Power Automate Governance) — blocked until AVAILABLE or LIMITED |

---

### 4. Teams / Approvals

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Microsoft Teams available in tenant. Approvals app available within Teams. Teams channel creation permitted. |
| **Validation method** | 1. Verify Teams license in M365 Admin Center → Billing → Licenses. 2. Open Teams desktop/web app. 3. Verify Approvals app appears in left sidebar or can be added. 4. Create a test team with channels (to be deleted after audit). |
| **Expected verification source** | M365 Admin Center + Teams client |
| **Architecture impact** | **MEDIUM** — Teams provides the operational governance channel for document reviews and approval notifications (Blueprint Phase M365-6). Not blocking for EA-3F but required for governance workflow. |
| **EA phase dependency** | EA-3I (Teams Integration) — impacted if LIMITED or NOT_AVAILABLE |

---

### 5. Microsoft Forms

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Microsoft Forms available in tenant. Form creation and response collection permitted. |
| **Validation method** | 1. Navigate to `forms.office.com` in tenant context. 2. Create a test form. 3. Verify form can be shared and responses collected. 4. Delete test form after audit. |
| **Expected verification source** | M365 tenant (forms.office.com) |
| **Architecture impact** | **LOW** — Forms may be used for document requests or feedback collection. Not a hard dependency for EA-3F. |
| **EA phase dependency** | Optional — no EA phase blocked |

---

### 6. Power BI

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Power BI service available in tenant. Report creation and sharing permitted. Power BI Desktop can connect to SharePoint Lists or Microsoft Lists. |
| **Validation method** | 1. Check Power BI license assignment in M365 Admin Center (Power BI Pro or Free). 2. Navigate to `app.powerbi.com` — verify "Create" button is active. 3. If Pro license available, test connection to a SharePoint list data source. |
| **Expected verification source** | M365 Admin Center + Power BI portal (app.powerbi.com) |
| **Architecture impact** | **LOW** — Power BI provides governance dashboards (Blueprint Phase M365-9). Not blocking for EA-3F. |
| **EA phase dependency** | EA-3J (Analytics & Compliance) — impacted if LIMITED or NOT_AVAILABLE |

---

### 7. Microsoft Graph API

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Microsoft Graph API accessible from tenant. SharePoint and Lists API endpoints respond. Delegate or application permissions can be granted. |
| **Validation method** | 1. Open Graph Explorer (`developer.microsoft.com/graph/graph-explorer`) signed in with tenant account. 2. Test `GET /v1.0/sites/root` — should return root site. 3. Test `GET /v1.0/sites/root/lists` — should return lists. 4. Verify required permission scopes (`Sites.Read.All`, `Sites.ReadWrite.All`) are available. |
| **Expected verification source** | Graph Explorer or REST API test |
| **Architecture impact** | **MEDIUM** — Graph API is the integration interface for scheduled registry export (Blueprint Phase M365-8, Option A). The preferred Option B (Registry Export JSON) does not require Graph API. |
| **EA phase dependency** | EA-3K (Portal Integration) — dependent on integration option chosen |

---

### 8. Azure App Registration

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Azure AD tenant permits App Registrations. Users can create and manage App Registrations. API permissions can be granted (admin consent available if needed). |
| **Validation method** | 1. Navigate to Azure Portal (portal.azure.com) → App Registrations. 2. Verify "New registration" button is active. 3. Create a minimal test app registration (do not grant production permissions). 4. Verify API permissions blade is accessible and permissions can be added. 5. Delete test app registration after audit. |
| **Expected verification source** | Azure Portal (portal.azure.com) — App Registrations |
| **Architecture impact** | **MEDIUM** — App Registration is required for Graph API integration (Option A). Not required for Option B (Scheduled Registry Export JSON). |
| **EA phase dependency** | EA-3K (Portal Integration) — only if Option A selected |

---

### 9. Copilot Availability

| Dimension | Detail |
|-----------|--------|
| **Evidence required** | Microsoft Copilot (or M365 Copilot) license assigned. Copilot available in Teams, SharePoint, or Word/Excel context. |
| **Validation method** | 1. Check Copilot license assignment in M365 Admin Center. 2. Verify Copilot icon appears in Teams sidebar. 3. Open a SharePoint page and check for Copilot integration. |
| **Expected verification source** | M365 Admin Center + Teams/SharePoint client |
| **Architecture impact** | **LOW** — Copilot was listed in Blueprint Phase M365-1 checklist but has no specific EA phase dependency. Informational. |
| **EA phase dependency** | None (informational) |

---

## Audit Execution Plan

### Prerequisites

| Requirement | Detail |
|-------------|--------|
| Tenant admin access | Global Admin or appropriate delegated admin (SharePoint Admin, Power Platform Admin) |
| M365 admin credentials | Test credentials preferred; production admin account acceptable with documented scope |
| Test resource cleanup | All test sites, lists, flows, app registrations, and teams created during audit must be deleted after audit completion |
| Audit documentation | Results recorded in new file: `docs/audits/M365_LICENSE_AUDIT.md` — does not exist yet, to be created from this plan |
| Audit branch | Dedicated branch `audit/m365-tenant-capability` created from `main` after plan approval |

### Workflow

1. Create branch `audit/m365-tenant-capability` from `main`.
2. Execute each audit target above in sequence.
3. Record results in `docs/audits/M365_LICENSE_AUDIT.md` using the per-target format.
4. For each `NOT_AVAILABLE` or `LIMITED` finding, document:
   - Exact error or limitation observed
   - Workaround options (if any)
   - Architecture impact with specific EA phase reference
   - Escalation path (who to contact for license/feature enablement)
5. For each `AVAILABLE` finding, attach specific evidence (screenshot, API response, admin center path).
6. Do NOT include credentials, tokens, or tenant identifiers in the audit document.
7. Delete all test resources created during audit.
8. Commit audit branch and create PR against `main`.
9. After merge, update `EA_SHAREPOINT_FOUNDATION_READINESS.md` — specifically the `BLOCKED_BY_TENANT_AUDIT` classification.

### Output

| Artifact | Description | Location |
|----------|-------------|----------|
| M365 License Audit | Completed audit with per-service AVAILABLE/LIMITED/NOT_AVAILABLE/NOT_VERIFIED results | `docs/audits/M365_LICENSE_AUDIT.md` (to be created) |

---

## Summary

| # | Capability | Architecture Impact | EA Phase Dependency |
|---|-----------|---------------------|-------------------|
| 1 | SharePoint Online | **CRITICAL** | EA-3F (blocked) |
| 2 | Microsoft Lists | **CRITICAL** | EA-3F, EA-3G |
| 3 | Power Automate | **HIGH** | EA-3H |
| 4 | Teams / Approvals | **MEDIUM** | EA-3I |
| 5 | Microsoft Forms | **LOW** | Optional |
| 6 | Power BI | **LOW** | EA-3J |
| 7 | Microsoft Graph API | **MEDIUM** | EA-3K (Option A) |
| 8 | Azure App Registration | **MEDIUM** | EA-3K (Option A) |
| 9 | Copilot availability | **LOW** | Informational |

**All capabilities are currently NOT_VERIFIED.** No tenant has been accessed. No evidence has been collected. This plan defines what evidence is required and how to collect it.

---

## Related Documents

- `docs/document-center/M365 FoundationBlueprint.MD` — Phase M365-1: License & Capability Audit
- `docs/architecture/EA_SHAREPOINT_FOUNDATION_READINESS.md` — readiness assessment (tenant capability = BLOCKED_BY_TENANT_AUDIT)
- `docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md` — canonical current state
