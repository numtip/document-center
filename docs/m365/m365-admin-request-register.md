# M365 Admin Request Register — RAE Document Center

**Phase:** M365-1 — License & Capability Audit  
**Status:** Register created (requests not yet submitted)  
**Last updated:** 2026-07-14  
**Owner:** RAE Digital Transformation  
**Target:** Maejo University (MJU) M365 / Entra Administrator

---

## 1. Purpose

This register documents all requests that require Microsoft 365 / Entra tenant administration for the RAE Document Center project. Each request specifies minimum required permissions, business justification, and architecture dependency.

### Request Principles

1. **Least privilege** — every request specifies the minimum permission scope required
2. **Business justification** — every request maps to an approved architecture requirement
3. **No Global Admin requests** — all requests can be fulfilled with delegated or scoped admin roles
4. **Auditable** — every request is tracked with ID, status, and expected resolution phase

---

## 2. Request Register

### REQ-001 — SharePoint Tenant URL Confirmation

| Field | Value |
|-------|-------|
| **Capability** | SharePoint Online |
| **Requested Action** | Confirm Maejo University M365 tenant SharePoint URL (e.g., `mju.sharepoint.com`) |
| **Business Justification** | EA-3 design references `[tenant].sharepoint.com` as placeholder. Actual URL required for all provisioning and configuration. |
| **Architecture Dependency** | EA-3 (SharePoint Foundation) — site design, library schema, content types |
| **Minimum Permission / Scope** | Read-only — tenant URL is public information |
| **Security Consideration** | None — SharePoint tenant URL is discoverable |
| **Required By Phase** | EA-3 |
| **Priority** | HIGH |
| **Status** | NOT_SUBMITTED |

---

### REQ-002 — SharePoint Site Creation

| Field | Value |
|-------|-------|
| **Capability** | SharePoint Online — Site Collection |
| **Requested Action** | Create "RAE Document Center" SharePoint Team Site at `https://[tenant].sharepoint.com/sites/RAE-DocumentCenter`. OR confirm self-service site creation is permitted and provide instructions. If self-service is not permitted, create site with: Thai (th-TH) language; (UTC+07:00) time zone; minimum 100 GB quota; hub site capability (if available). |
| **Business Justification** | EA-3 design requires a dedicated SharePoint site as the document storage layer. All 6 document libraries, content types, and permissions are designed around this site. |
| **Architecture Dependency** | EA-3 (SharePoint Foundation); prerequisite for G-EA3 gate |
| **Minimum Permission / Scope** | SharePoint Administrator or Site Collection Administrator (for creation); delegated site owner (post-creation) |
| **Security Consideration** | External sharing disabled at site level by default; per-document anonymous links enabled only for Public documents |
| **Required By Phase** | EA-3 |
| **Priority** | HIGH |
| **Status** | NOT_SUBMITTED |

---

### REQ-003 — External Sharing Policy Disclosure

| Field | Value |
|-------|-------|
| **Capability** | SharePoint Online — External Sharing |
| **Requested Action** | Disclose current tenant-level external sharing policy, specifically: Are "Anyone" (anonymous) sharing links permitted? Are anonymous view-only links allowed? What is the default sharing link type? Is there link expiration policy? |
| **Business Justification** | The EA-7/EA-8 public portal architecture depends on anonymous view-only links for StorageURL. If anonymous links are not permitted, the portal integration pattern must be redesigned. This is the single highest-risk unknown in the architecture. |
| **Architecture Dependency** | EA-3 (per-document anonymous links for Public visibility); EA-7 (StorageURL pattern); EA-8 (public portal access) |
| **Minimum Permission / Scope** | Read-only — Sharing page in M365 admin center or SharePoint admin center |
| **Security Consideration** | Organizational policy must be respected. If anonymous sharing is restricted, the architecture adapts. Shared links should have expiration (e.g., 30 days) as recommended security practice. |
| **Required By Phase** | EA-3 (before site creation) |
| **Priority** | CRITICAL |
| **Status** | NOT_SUBMITTED |

---

### REQ-004 — Share anonymous link expiration (REQ-003 follow-up)

**Note:** This request is dependent on REQ-003 outcome. Only submit if anonymous sharing is permitted.

| Field | Value |
|-------|-------|
| **Capability** | SharePoint Online — Anonymous Link Settings |
| **Requested Action** | If anonymous sharing is permitted, configure minimum link expiration as appropriate for MJU policy (recommended: 30 days for Public document links). OR confirm current expiration policy. |
| **Business Justification** | The registry export process produces static JSON. StorageURL links referencing expired anonymous links will break in the public portal. Link lifecycle must be managed. |
| **Architecture Dependency** | EA-7 (Registry Export); EA-8 (Public Portal) |
| **Minimum Permission / Scope** | SharePoint Administrator or Sharing Policy Administrator |
| **Security Consideration** | Link expiration reduces risk of unauthorized access to stale links |
| **Required By Phase** | EA-7 |
| **Priority** | MEDIUM |
| **Status** | NOT_SUBMITTED |

---

### REQ-005 — SharePoint Term Store: RAE-Tags Term Set

| Field | Value |
|-------|-------|
| **Capability** | SharePoint Managed Metadata / Term Store |
| **Requested Action** | Create the "RAE-Tags" term set in the SharePoint Term Store. Term set should be open (users can add terms). Create the "RAE-Tags" term group (or use existing group). Add initial tag values from the existing taxonomy (see `docs/document-center/taxonomy.json`). |
| **Business Justification** | The EA-3 library schema defines a `Tags` column of type Managed Metadata referencing the RAE-Tags term set. Managed Metadata enables consistent tagging and taxonomy enforcement across all 6 document libraries. |
| **Architecture Dependency** | EA-3 (Tags column in library-schema.md); EA-4 (Tags column in registry-list-schema.md) |
| **Minimum Permission / Scope** | Term Store Administrator — requires dedicated admin role |
| **Security Consideration** | Term set is shared taxonomy. Ensure only authorized administrators can modify the term set structure. |
| **Required By Phase** | EA-3 |
| **Priority** | HIGH |
| **Status** | NOT_SUBMITTED |

---

### REQ-006 — Power Automate Environment and Connector Verification

| Field | Value |
|-------|-------|
| **Capability** | Power Automate |
| **Requested Action** | Confirm Power Automate is available in the tenant. Identify available environments (default vs dedicated). Verify that the following standard connectors are available and not restricted by DLP policy: SharePoint, Microsoft Lists (same as SharePoint), Approvals, Teams, Schedule, HTTP. |
| **Business Justification** | EA-5 workflow automation depends on Power Automate with standard connectors. EA-5 implementation is gated behind this verification (G-EA5). Without Power Automate, all EA-5 workflows must be performed manually. |
| **Architecture Dependency** | EA-5 (Power Automate Governance); prerequisite for G-EA5 gate |
| **Minimum Permission / Scope** | Power Automate admin center read access; or tenant admin to check DLP policies |
| **Security Consideration** | DLP policies may restrict connector usage. EA-5 design uses only standard connectors; premium connector access is not requested. |
| **Required By Phase** | EA-5 |
| **Priority** | HIGH |
| **Status** | NOT_SUBMITTED |

---

### REQ-007 — Power Automate DLP Policy Adjustment (Conditional)

**Note:** This request is conditional on REQ-006 outcome. Only submit if DLP policies block standard SharePoint/Lists connectors.

| Field | Value |
|-------|-------|
| **Capability** | Power Automate — DLP Policy |
| **Requested Action** | If existing DLP policy blocks SharePoint or Microsoft Lists standard connectors in the default environment, create a DLP exception policy that allows these connectors, OR create a dedicated environment with allowed connectors. |
| **Business Justification** | SharePoint and Microsoft Lists connectors are the core of EA-5 workflow automation. Without them, the approved architecture cannot be implemented. |
| **Architecture Dependency** | EA-5 (Power Automate Governance) |
| **Minimum Permission / Scope** | Power Automate Administrator or DLP Policy Administrator |
| **Security Consideration** | Limit allowed connectors to only those required (SharePoint, Lists, Approvals, Teams, Schedule, HTTP). Do NOT globally allow all connectors. |
| **Required By Phase** | EA-5 |
| **Priority** | HIGH |
| **Status** | NOT_SUBMITTED |

---

### REQ-008 — Azure / Entra App Registration

| Field | Value |
|-------|-------|
| **Capability** | Microsoft Entra ID — App Registration |
| **Requested Action** | Create a new App Registration in Entra ID for the "RAE Document Center — Registry Export" service. OR confirm self-service App Registration is permitted and provide instructions. If self-service is not permitted, create app registration with: Single-tenant application; Redirect URI not required (no interactive auth); Client secret or certificate for authentication. |
| **Business Justification** | The EA-7 scheduled registry export requires an automated identity to read Microsoft List data via Graph API. A service identity (app registration) is the standard approach for server-to-server automation. |
| **Architecture Dependency** | EA-7 (Registry Export — Scheduled Registry Export JSON); prerequisite for G-EA7 gate |
| **Minimum Permission / Scope** | Application Developer (for self-service registration) or Application Administrator (admin-created) |
| **Security Consideration** | Client secret must be stored securely. Prefer certificate-based authentication for production. See REQ-009 for API permission scope. |
| **Required By Phase** | EA-7 |
| **Priority** | MEDIUM |
| **Status** | NOT_SUBMITTED |

---

### REQ-009 — Graph API Permission Consent: Sites.Selected

| Field | Value |
|-------|-------|
| **Capability** | Microsoft Graph API — Permission Consent |
| **Requested Action** | Grant admin consent for the "RAE Document Center — Registry Export" app registration to use the `Sites.Selected` application permission. This permission grants read access to a specific SharePoint site only (the RAE Document Center site), NOT all sites. After consent is granted, the application must be granted access to the RAE Document Center site by the site administrator. |
| **Business Justification** | The scheduled registry export reads the RAE Document Registry Microsoft List via Graph API. Sites.Selected is the least-privilege permission that allows this. It is the preferred alternative to the broader Sites.Read.All permission. |
| **Architecture Dependency** | EA-7 (Registry Export) |
| **Minimum Permission / Scope** | Application Administrator or Global Administrator (for admin consent) |
| **Security Consideration** | Sites.Selected is the minimum required permission. It grants access ONLY to the specified site, not all site collections in the tenant. This follows least-privilege principle. |
| **Required By Phase** | EA-7 |
| **Priority** | MEDIUM |
| **Status** | NOT_SUBMITTED |

---

### REQ-010 — Environment Teams: RAE Document Governance Team Creation

| Field | Value |
|-------|-------|
| **Capability** | Microsoft Teams |
| **Requested Action** | Create "RAE Document Governance" Microsoft Team. OR confirm self-service team creation is permitted. If self-service is not permitted, create team with: Private team; Channels: General, New Documents, Reviews, Approvals, Archive Requests. |
| **Business Justification** | The M365-6 Teams Integration phase uses the team for governance notifications, approval requests, and operational communication. Team channels map to governance workflows. |
| **Architecture Dependency** | M365-6 (Teams Integration) |
| **Minimum Permission / Scope** | Teams Administrator (admin-created) or Team Owner (self-service) |
| **Security Consideration** | Private team; external guest access not required. Only designated Category Owners and Document Owners are members. |
| **Required By Phase** | M365-6 |
| **Priority** | LOW |
| **Status** | NOT_SUBMITTED |

---

### REQ-011 — Microsoft 365 Groups: Category Owner Groups

| Field | Value |
|-------|-------|
| **Capability** | Microsoft 365 Groups |
| **Requested Action** | Verify M365 Group creation policy. If group creation is self-service, confirm instructions. If restricted, request creation of the following groups (or equivalent): RAE-DC-Administration-Owners, RAE-DC-FinanceProcurement-Owners, RAE-DC-PlanningPolicy-Owners, RAE-DC-AcademicServices-Owners, RAE-DC-Research-Owners, RAE-DC-SOPManuals-Owners, RAE-DC-PlatformAdmins. |
| **Business Justification** | EA-3 permissions matrix defines SharePoint groups for Category Owners and Platform Admin. M365 Groups underpin these SharePoint permission groups and enable group-based governance. |
| **Architecture Dependency** | EA-3 (Permissions Matrix); M365-6 (Teams Integration) |
| **Minimum Permission / Scope** | Groups Administrator (if admin-created) or self-service group creation |
| **Security Consideration** | Groups are private; membership managed by Category Owners |
| **Required By Phase** | EA-3 |
| **Priority** | MEDIUM |
| **Status** | NOT_SUBMITTED |

---

### REQ-012 — Live test the document public view-only link

**Note:** This request is dependent on REQ-003 outcome. Only submit if anonymous sharing is permitted.

| Field | Value |
|-------|-------|
| **Capability** | SharePoint Online — Anonymous Sharing |
| **Requested Action** | After RAE Document Center site is created, verify that a view-only anonymous sharing link can be created on a test document uploaded to one of the 6 document libraries. Confirm the generated URL is accessible without M365 authentication. |
| **Business Justification** | The public portal architecture (EA-8) depends on stable StorageURLs that can be accessed without authentication. This test verifies the actual link behavior. |
| **Architecture Dependency** | EA-3 (StorageURL pattern); EA-7 (Registry Export includes StorageURL); EA-8 (Public Portal displays StorageURL) |
| **Minimum Permission / Scope** | Site admin or document owner can create sharing link |
| **Security Consideration** | Test document must not contain sensitive information |
| **Required By Phase** | EA-8 |
| **Priority** | MEDIUM |
| **Status** | NOT_SUBMITTED |

---

## 3. Request Summary

| ID | Request | Priority | Phase | Status | Admin Role Required |
|:--:|---------|:--------:|:-----:|:------:|---------------------|
| REQ-001 | Tenant URL confirmation | HIGH | EA-3 | NOT_SUBMITTED | Read-only |
| REQ-002 | SharePoint site creation | HIGH | EA-3 | NOT_SUBMITTED | SharePoint Administrator |
| REQ-003 | External sharing policy disclosure | **CRITICAL** | EA-3 | NOT_SUBMITTED | Read-only |
| REQ-004 | Anonymous link expiration (conditional) | MEDIUM | EA-7 | NOT_SUBMITTED | SharePoint Administrator |
| REQ-005 | Term Store: RAE-Tags term set | HIGH | EA-3 | NOT_SUBMITTED | Term Store Admin |
| REQ-006 | Power Automate environment verification | HIGH | EA-5 | NOT_SUBMITTED | Power Automate Admin |
| REQ-007 | DLP policy adjustment (conditional) | HIGH | EA-5 | NOT_SUBMITTED | Power Automate Admin |
| REQ-008 | Entra App Registration | MEDIUM | EA-7 | NOT_SUBMITTED | Application Developer / Admin |
| REQ-009 | Graph API permission consent | MEDIUM | EA-7 | NOT_SUBMITTED | Application Administrator |
| REQ-010 | Teams: RAE Document Governance | LOW | M365-6 | NOT_SUBMITTED | Teams Administrator |
| REQ-011 | M365 Groups: Category Owners | MEDIUM | EA-3 | NOT_SUBMITTED | Groups Administrator |
| REQ-012 | Anonymous link test (conditional) | MEDIUM | EA-8 | NOT_SUBMITTED | Site-level |

---

## 4. Submission Order

Requests should be submitted in the following prioritized order based on architecture dependencies:

```
Phase 1 (Pre-EA-3):
  └─ REQ-001: Tenant URL (informational)
  └─ REQ-003: Sharing policy disclosure (answers critical architecture question)
  └─ REQ-005: Term Store RAE-Tags (long lead time)

Phase 2 (EA-3 Implementation):
  └─ REQ-002: SharePoint site creation
  └─ REQ-011: M365 Groups (Category Owners)

Phase 3 (EA-5 Readiness):
  └─ REQ-006: Power Automate verification
  └─ REQ-007: DLP adjustment (if needed)

Phase 4 (EA-7 Readiness):
  └─ REQ-008: App registration
  └─ REQ-009: Permission consent
  └─ REQ-004: Link expiration (if needed)

Phase 5 (M365-6 Readiness):
  └─ REQ-010: Teams creation
  └─ REQ-012: Anonymous link test (if sharing permitted)
```

---

## 5. Role Mapping

| Admin Role | Required For | Requests |
|------------|-------------|:--------:|
| SharePoint Administrator | Site creation, sharing policies | REQ-002, REQ-004 |
| Term Store Administrator | Managed Metadata term sets | REQ-005 |
| Power Automate Administrator | Environment, DLP policies | REQ-006, REQ-007 |
| Application Developer / Application Administrator | App registration | REQ-008 |
| Application Administrator | API permission consent | REQ-009 |
| Teams Administrator | Team creation | REQ-010 |
| Groups Administrator | M365 Groups | REQ-011 |
| IT Admin (read-only) | Tenant URL, sharing policy | REQ-001, REQ-003 |

---

## Related Documents

| Document | Path |
|----------|------|
| License & Capability Audit | `docs/m365/M365_LICENSE_AUDIT.md` |
| Tenant Readiness Matrix | `docs/m365/m365-tenant-readiness-matrix.csv` |
| Provisioning Gate | `docs/m365/m365-provisioning-gate.md` |
| EA-3 Readiness Report | `docs/m365/m365-3-readiness-report.md` |
| EA-4 Readiness Report | `docs/m365/m365-4-readiness-report.md` |
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
