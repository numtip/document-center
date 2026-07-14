# Provisioning Gate — RAE Document Center

**Phase:** M365-1 — License & Capability Audit  
**Status:** Gate Definitions (design-phase)  
**Last updated:** 2026-07-14  
**Blueprint ref:** `docs/document-center/M365 FoundationBlueprint.MD`

---

## 1. Purpose

This document defines the provisioning gates that must be passed before implementing each phase of the RAE Document Center architecture. Gates prevent premature implementation when dependencies are unresolved, capabilities are unverified, or mandatory preconditions are unmet.

### Gate Principles

1. **No gate may be bypassed** without documented exception signed by RAE Digital Transformation and tenant admin
2. **Evidence is required** — architecture requirements alone do not satisfy a gate
3. **Multiple gates may be open simultaneously** if no dependency chain exists
4. **EA-5 implementation is explicitly gated** behind EA-3 and EA-4 provisioning

---

## 2. Gate 1 — EA-3 SharePoint Provisioning

**Gate ID:** G-EA3  
**Phase:** EA-3 — SharePoint Foundation  
**Gate Type:** Implementation (creating real M365 resources)

### 2.1 Required Capabilities

| # | Capability | Minimum Level | Dependency |
|---|------------|:-------------:|:----------:|
| G1.1 | SharePoint Online | AVAILABLE | Tenant subscription |
| G1.2 | M365 tenant URL | Confirmed | IT admin |
| G1.3 | Site creation capability | Self-service or admin-provisioned | Tenant policy |
| G1.4 | External sharing policy | Known (any policy is OK — design adapts) | Tenant admin disclosure |
| G1.5 | Storage quota | Minimum 100 GB available | Tenant subscription |

### 2.2 Required Evidence

| # | Evidence | Source |
|---|----------|--------|
| E1.1 | Tenant URL documentation (e.g., `mju.sharepoint.com`) | IT admin confirmation |
| E1.2 | Site collection creation confirmation or self-service access | M365 admin center / IT admin |
| E1.3 | Anonymous sharing policy documented | M365 admin center sharing report |
| E1.4 | Available storage quota | M365 admin center Storage metrics |

### 2.3 Pass Condition

All required capabilities are AVAILABLE or AVAILABLE_WITH_LIMITATIONS, and all required evidence is documented.

### 2.4 Conditional Pass

Some capabilities are AVAILABLE_WITH_LIMITATIONS or ADMIN_REQUIRED, AND all limitations are documented with mitigation plans. The following conditional passes are acceptable:

| Condition | Mitigation |
|-----------|------------|
| Anonymous sharing disabled | StorageURL in portal uses authenticated view links OR portal redirects to SharePoint for auth |
| Storage quota under 100 GB | Request quota increase; begin with pilot migration |
| Hub site unavailable | Defer hub features; operate as standalone site collection |
| Site requires admin provisioning | Submit site creation request with design specification from `sharepoint-site-design.md` |

### 2.5 Block Condition

| Condition | Impact |
|-----------|--------|
| SharePoint Online not provisioned in tenant | **BLOCKED** — foundation cannot proceed |
| Site creation denied by policy and admin | **BLOCKED** — no SharePoint site possible |

### 2.6 Owner / Admin Dependency

| Dependency | Owner |
|------------|-------|
| Tenant admin confirmation of SPO availability | MJU M365 Administrator |
| Site creation (if self-service unavailable) | MJU M365 Administrator |
| Storage quota increase (if required) | MJU M365 Administrator |
| Hub site features (if required) | MJU M365 Administrator |
| External sharing policy approval (if change needed) | MJU M365 Administrator |

---

## 3. Gate 2 — EA-4 Microsoft Lists Provisioning

**Gate ID:** G-EA4  
**Phase:** EA-4 — Microsoft Lists Registry Design  
**Gate Type:** Implementation (creating real M365 resources)

### 3.1 Dependencies

```
G-EA3 (EA-3 SharePoint site must be provisioned)
  └── G-EA4 (EA-4 Registry list created on that site)
```

### 3.2 Required Capabilities

| # | Capability | Minimum Level | Dependency |
|---|------------|:-------------:|:----------:|
| G2.1 | SharePoint Online (site exists) | PROVISIONED | G-EA3 passed |
| G2.2 | Microsoft Lists | AVAILABLE | SharePoint Online |
| G2.3 | Person/Group columns | AVAILABLE | M365 identity directory |
| G2.4 | Choice columns | AVAILABLE | Standard Lists |
| G2.5 | Column indexing | AVAILABLE | Standard Lists |
| G2.6 | Content Types | PUBLISHED | Site collection |

### 3.3 Required Evidence

| # | Evidence | Source |
|---|----------|--------|
| E2.1 | RAE Document Center site exists | Site URL verified reachable |
| E2.2 | Site collection admin rights or appropriate permissions | Permission verification |
| E2.3 | Internal column names captured from actual SharePoint | Site columns created and verified |
| E2.4 | Registered SharePoint internal names document | Registry mapping verification |
| E2.5 | Content types published and added to libraries | Content type verification |

### 3.4 Pass Condition

EA-3 site is provisioned. All required capabilities are confirmed AVAILABLE. Content types are published. Column internal names are captured against actual SharePoint fields.

### 3.5 Conditional Pass

| Condition | Mitigation |
|-----------|------------|
| Content types not yet published | Publish content types before registry list creation |
| Term Store not configured | Defer RAE-Tags column; use text column as interim; configure Tags in EA-5 |

### 3.6 Block Condition

| Condition | Impact |
|-----------|--------|
| SharePoint site not provisioned | **BLOCKED** — no site to host registry list |
| Site permissions don't allow list creation | **BLOCKED** — cannot create registry list |

### 3.7 Owner / Admin Dependency

| Dependency | Owner |
|------------|-------|
| RAE Document Center site creation (if not done) | MJU M365 Administrator / Platform Admin |
| Content type publishing | Site Collection Administrator |
| Term Store configuration | Term Store Administrator |

---

## 4. Gate 3 — EA-5 Power Automate Implementation

**Gate ID:** G-EA5  
**Phase:** EA-5 — Power Automate Governance  
**Gate Type:** Implementation (creating real Power Automate flows)

### 4.1 Dependencies

```
G-EA3 (SharePoint site provisioned)
    │
    └── G-EA4 (Registry list provisioned on site)
        │
        └── G-EA5 (Power Automate implementation on provisioned site + list)
```

### 4.2 Required Capabilities

| # | Capability | Minimum Level | Dependency |
|---|------------|:-------------:|:----------:|
| G3.1 | Power Automate | AVAILABLE (standard connectors) | Tenant subscription |
| G3.2 | SharePoint connector | AVAILABLE | Power Automate + SharePoint |
| G3.3 | Microsoft Lists connector | AVAILABLE | Power Automate + Lists |
| G3.4 | Approvals connector | AVAILABLE | Power Automate + Approvals |
| G3.5 | Teams connector (optional — for notifications) | AVAILABLE | Power Automate + Teams |
| G3.6 | Scheduled flows capability | AVAILABLE | Power Automate |

### 4.3 Required Evidence

| # | Evidence | Source |
|---|----------|--------|
| E3.1 | Power Automate accessible from M365 app launcher | User account verification |
| E3.2 | SharePoint connector displays in connector list | Power Automate environment |
| E3.3 | Microsoft Lists connector displays in connector list | Power Automate environment |
| E3.4 | Approvals connector displays in connector list | Power Automate environment |
| E3.5 | Scheduled flow creation possible | Power Automate UI |
| E3.6 | DLP policy does not block required connectors | Power Automate admin center (admin view) |
| E3.7 | SharePoint site columns accessible in flow designer | Power Automate flow creation test |
| E3.8 | Registry list columns accessible in flow designer | Power Automate flow creation test |

### 4.4 Pass Condition

All conditions in 4.2 are confirmed. All evidence is documented. DLP policy confirmed non-blocking. Test Identity / Owner users exist.

### 4.5 Conditional Pass

| Condition | Mitigation |
|-----------|------------|
| Teams connector not available | Use email notifications instead (standard connector) |
| Scheduled flows in default environment only | Accept default environment; add dedicated env later |
| SharePoint connector available | Required — cannot proceed without this |
| Lists connector available | Required — cannot proceed without this |

### 4.6 Block Condition

| Condition | Impact |
|-----------|--------|
| Power Automate not provisioned in tenant | **BLOCKED** — cannot create flows |
| DLP policy blocks SharePoint or Lists connectors | **BLOCKED** — core workflow connectors unavailable |
| SharePoint site not provisioned (G-EA3 not passed) | **BLOCKED** — workflow triggers target non-existent site |
| Registry list not provisioned (G-EA4 not passed) | **BLOCKED** — workflow targets non-existent list |
| Internal column names not captured | **BLOCKED** — flows reference unknown field names |
| Permissions not verified | **BLOCKED** — flow run identity and access unknown |
| Test identities / owners unavailable | **BLOCKED** — cannot test approval workflows |

### 4.7 Explicit Implementation Prohibition

> **EA-5 (Power Automate) implementation must NOT begin until all of the following are confirmed:**
> 
> 1. Power Automate capability is verified (G3.1 — G3.3 passed)
> 2. SharePoint site (RAE Document Center) is provisioned (G-EA3 passed)
> 3. RAE Document Registry list is provisioned (G-EA4 passed)
> 4. SharePoint column internal names are captured and verified against actual fields
> 5. Registry list column internal names are captured and verified against actual fields
> 6. Permissions for flow owner/run-account are verified
> 7. Test identities and document owners are available in the M365 directory
> 
> **EA-5 DESIGN may begin earlier.** EA-5 DESIGN is not gated — workflow logic was defined in EA-4 lifecycle model. Only EA-5 IMPLEMENTATION (creating flows) is gated.

### 4.8 Owner / Admin Dependency

| Dependency | Owner |
|------------|-------|
| Power Automate environment availability verification | MJU M365 Administrator / Power Automate Admin |
| DLP policy review | MJU M365 Administrator / Power Automate Admin |
| Flow owner identity / service account | RAE Digital Transformation |
| Test document owners available | RAE Category Owners |

---

## 5. Gate 4 — EA-7 Registry Export Implementation

**Gate ID:** G-EA7  
**Phase:** EA-7 — Registry Export  
**Gate Type:** Implementation (creating export automation)

### 5.1 Dependencies

```
G-EA3 (SharePoint site provisioned)
    │
    ├── G-EA4 (Registry list provisioned)
    │   │
    │   └── G-EA5 (Power Automate flows operational — optional, for automated export trigger)
    │       │
    │       └── G-EA7 (Registry export implemented)
```

### 5.2 Required Capabilities

| # | Capability | Minimum Level | Dependency |
|---|------------|:-------------:|:----------:|
| G4.1 | Microsoft Graph API accessible | AVAILABLE | Tenant |
| G4.2 | Azure / Entra App Registration | CREATED | Tenant admin |
| G4.3 | API permission consent | GRANTED (Sites.Selected preferred) | Tenant admin |
| G4.4 | Client authentication | Secret or certificate | App registration owner |
| G4.5 | Export target (GitHub repository) | ACCESSIBLE | RAE team |

### 5.3 Required Evidence

| # | Evidence | Source |
|---|----------|--------|
| E4.1 | App registration exists with appropriate permissions | Entra admin center |
| E4.2 | Admin consent granted for Sites.Selected | Entra admin center — API permissions |
| E4.3 | Test Graph API call succeeds | API test (e.g., Graph Explorer or script) |
| E4.4 | GitHub repository accessible for export push | Git operation |
| E4.5 | Registry data validated against export contract | Comparison with `registry-export-contract.md` |

### 5.4 Pass Condition

Graph API access verified. App registration created with Sites.Selected permission. Admin consent granted. Export target (GitHub) accessible. Registry data validated.

### 5.5 Conditional Pass

| Condition | Mitigation |
|-----------|------------|
| Sites.Selected not available | Use Sites.Read.All (broader scope accepted with admin approval) |
| App registration creation requires admin | Submit registration request with permission specification |
| GitHub push requires PAT | Use Personal Access Token or GitHub Actions workflow |

### 5.6 Block Condition

| Condition | Impact |
|-----------|--------|
| Graph API not accessible | **BLOCKED** — cannot read list data programmatically |
| App registration cannot be created | **BLOCKED** — no identity for export |
| Admin consent denied | **BLOCKED** — cannot authenticate |

### 5.7 Owner / Admin Dependency

| Dependency | Owner |
|------------|-------|
| App registration creation | Entra Admin / MJU M365 Administrator |
| Admin consent grant | Entra Admin |
| Client secret management | App Registration Owner |
| GitHub repository access | RAE Digital Transformation |

---

## 6. Gate Summary

| Gate | Phase | Precondition | Type | Status |
|:----:|-------|:------------:|------|:------:|
| G-EA3 | EA-3 — SharePoint Provisioning | Tenant subscription with SPO | Implementation | **NOT_PASSED** — tenant confirmation required |
| G-EA4 | EA-4 — Microsoft Lists Registry | G-EA3 (Site exists) | Implementation | **NOT_PASSED** — G-EA3 must pass first |
| G-EA5 | EA-5 — Power Automate Implementation | G-EA3 + G-EA4 | Implementation | **NOT_PASSED** — G-EA3 + G-EA4 must pass first |
| G-EA7 | EA-7 — Registry Export | G-EA4 | Implementation | **NOT_PASSED** — G-EA4 must pass first |

### Current Phase Status

| Phase | Design Status | Implementation Status | Gate |
|-------|:-------------:|:---------------------:|:----:|
| EA-1 (this phase) | COMPLETE | NOT_STARTED | — |
| EA-3 | COMPLETE | NOT_STARTED | G-EA3 |
| EA-4 | COMPLETE | NOT_STARTED | G-EA4 |
| EA-5 | DESIGN_READY_WITH_CONDITIONS | IMPLEMENTATION_NOT_READY | G-EA5 |
| EA-7 | DESIGN_INPUTS_REQUIRED | NOT_STARTED | G-EA7 |

---

## Related Documents

| Document | Path |
|----------|------|
| License & Capability Audit | `docs/m365/M365_LICENSE_AUDIT.md` |
| Tenant Readiness Matrix | `docs/m365/m365-tenant-readiness-matrix.csv` |
| Admin Request Register | `docs/m365/m365-admin-request-register.md` |
| EA-4 Readiness Report | `docs/m365/m365-4-readiness-report.md` |
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
