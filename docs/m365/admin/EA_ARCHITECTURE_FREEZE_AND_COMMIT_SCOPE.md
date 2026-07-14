# Architecture Freeze & Commit Scope — RAE Document Center M365

**Package:** Admin Package  
**Phase:** EA-1 through EA-4 (architecture complete, pre-implementation)  
**Status:** BASELINE_CAPTURED — NOT YET FROZEN  
**Last updated:** 2026-07-14  
**Blueprint ref:** `docs/document-center/M365 FoundationBlueprint.MD`

---

## 1. Architecture Baseline

### 1.1 Purpose of Freeze

The architecture freeze establishes a canonically agreed baseline of M365 architecture decisions for the RAE Document Center. Once frozen, no architectural element listed below may be changed, extended, or reinterpreted without formal reopening (see §9).

This freeze protects:

- **Design integrity** — downstream phases (EA-5, EA-7) depend on stable primitives
- **Implementation consistency** — site provisioning, list creation, and automation must target exact column names and values
- **Audit trail** — a frozen baseline anchors accountability for architectural decisions

### 1.2 Canonical DocumentID Format

| Property | Value | Constraint |
|----------|-------|------------|
| Pattern | `RAE-NNNNN` | Regex: `^RAE-\d{5}$` |
| Example | `RAE-00001` | Zero-padded, 5-digit sequential |
| Scope | All 6 document libraries + RAE Document Registry list | Unique across all containers |
| Assignment | Auto-assigned (or pre-assigned from migration manifest) | No manual collision |

> **This format is frozen.** No alternative ID scheme, suffix, or prefix variant may be introduced.

### 1.3 Canonical Status Values (7)

These values apply to the `DocumentStatus` column in every RAE document library and the registry list.

| # | Value | Meaning | Visible in Portal |
|---|-------|---------|:-----------------:|
| 1 | `draft` | Work in progress; not yet reviewed | No |
| 2 | `review` | Under review by Category Owner | Conditional |
| 3 | `approved` | Reviewed and approved for publishing | Conditional |
| 4 | `published` | Actively published and discoverable | Yes |
| 5 | `current` | Active, reviewed, published (alias for post-migration stability) | Yes |
| 6 | `obsolete` | Superseded but retained for reference | Conditional |
| 7 | `archived` | Moved to archive; not actively managed | No |

> **Migration note:** The library schema (`library-schema.md`) additionally defines `LegacyImported` and `MetadataOnly` as migration-phase values. These are **transitional only** and are not part of the canonical status set. Post-migration, all documents must map to one of the 7 canonical values above.

> **This set is frozen.** No new status value may be added. No existing value may be renamed.

### 1.4 Canonical Visibility Values (4)

These values apply to the `PublicVisibility` column.

| # | Value | Meaning | Portal Export |
|---|-------|---------|:-------------:|
| 1 | `public` | Accessible to all site visitors (anonymous link OK) | Included |
| 2 | `internal` | Visible to authenticated org users only | Included (authenticated) |
| 3 | `restricted` | Access by exception only; manual approval required | Excluded |
| 4 | `private` | Document owner / specific group only; no sharing link | Excluded |

> **`PendingReview`** is a pre-migration default defined in `library-schema.md` — it is **not** a canonical visibility value. It serves as the initial state for all 772 legacy records and must be resolved to one of the 4 canonical values during post-migration review.

> **This set is frozen.** No new visibility value may be added. No existing value may be renamed.

### 1.5 Core Architecture Principle

```
Build Less. Govern More.
```

- Prefer configuration over custom code
- Prefer declarative metadata over imperative workflow logic
- Prefer SharePoint native capabilities (content types, column validation, views) over Power Automate for data integrity
- Automate only what cannot be governed by platform rules

---

## 2. Verified Tenant Capabilities

Confirmed from EA-1C (Batch 1) and EA-1D (Batch 2) evidence batches. These capabilities are verified against the `researchmju` tenant.

| # | Capability | Status | Evidence Source | Notes |
|---|------------|--------|----------------|-------|
| 1 | SharePoint Online | **CONFIRMED** | EA-1C / EA-1D | Tenant has active SPO license |
| 2 | Microsoft Lists | **CONFIRMED AVAILABLE** | EA-1C / EA-1D | Lists accessible from app launcher |
| 3 | Power Automate | **CONFIRMED** | EA-1C / EA-1D | Standard connectors visible |
| 4 | SharePoint connector | **CONFIRMED STANDARD** | EA-1C / EA-1D | Listed in Power Automate connector catalog |
| 5 | Approvals connector | **CONFIRMED STANDARD** | EA-1C / EA-1D | Listed in Power Automate connector catalog |
| 6 | Teams connector | **CONFIRMED STANDARD** | EA-1C / EA-1D | Listed in Power Automate connector catalog |
| 7 | Anyone/anonymous links | **CONFIRMED ENABLED** | EA-1C / EA-1D | Anonymous sharing policy permits |
| 8 | Site creation | **ADMIN REQUIRED** | EA-1C / EA-1D | `researchmju` cannot self-create sites |
| 9 | Managed Metadata / Term Store | **ADMIN REQUIRED** | EA-1C / EA-1D | Term Store not accessible at user level |

> **Capability status values:** CONFIRMED — verified by multiple evidence sources. CONFIRMED AVAILABLE — feature exists in tenant. CONFIRMED STANDARD — standard (non-premium) connector tier confirmed. ADMIN REQUIRED — feature exists but requires tenant admin action to provision or access.

---

## 3. Known Admin Dependencies

Items that require tenant administrator (`MJU M365 Administrator`) action before implementation can proceed.

| # | Dependency | Required For | EA Phase | Admin Action Required |
|---|------------|-------------|:--------:|-----------------------|
| 1 | Site creation | RAE Document Center SharePoint site | EA-3 | Submit site creation request with `sharepoint-site-design.md` specification |
| 2 | M365 Group creation / owner assignment | Site ownership and permission groups | EA-3 | Create M365 Group; assign Category Owners as members |
| 3 | Term Store access (RAE-Tags term set) | Managed Metadata column and term set creation | EA-3 / EA-4 | Provide Term Store Administrator access or create `RAE-Tags` term set on behalf |
| 4 | App registration (Entra ID) | Registry export automation | EA-7 | Create App Registration with `Sites.Selected` permission |
| 5 | Admin consent for Graph API permissions | Programmatic list access | EA-7 | Grant admin consent for `Sites.Selected` (or `Sites.Read.All`) |
| 6 | DLP policy review | Power Automate connector availability | EA-5 | Confirm DLP policy does not block SharePoint, Lists, or Approvals connectors |
| 7 | Storage quota increase (if required) | Accommodate migration data volume | EA-3 | Request quota increase from current allocation |

> **Tracking:** All admin requests are logged in `docs/m365/m365-admin-request-register.md`. Each dependency should be resolved before its dependent EA phase gate passes.

---

## 4. Files In Scope for Commit

Organized by EA phase. All paths relative to repository root `G:\ProjectAI\document-center\`.

### EA-1 — License & Capability Audit

| # | File | Description |
|---|------|-------------|
| 1 | `docs/m365/M365_LICENSE_AUDIT.md` | License audit and capability inventory |
| 2 | `docs/m365/m365-tenant-readiness-matrix.csv` | Tenant readiness scoring matrix |
| 3 | `docs/m365/m365-provisioning-gate.md` | Provisioning gate definitions (G-EA3 through G-EA7) |
| 4 | `docs/m365/m365-admin-request-register.md` | Register of pending and fulfilled admin requests |

### EA-1B — Tenant Evidence (User Verification)

| # | File | Description |
|---|------|-------------|
| 5 | `docs/m365/m365-tenant-evidence-runbook.md` | Runbook for tenant evidence collection |
| 6 | `docs/m365/m365-tenant-evidence-register.csv` | Evidence register with collection status |
| 7 | `docs/m365/m365-user-verification-checklist.md` | User account verification checklist |

### EA-1C — Tenant Evidence Batch 1

| # | File | Description |
|---|------|-------------|
| 8 | `docs/m365/m365-tenant-evidence-batch-1-report.md` | Batch 1 evidence collection report |

### EA-1D — Tenant Evidence Batch 2

| # | File | Description |
|---|------|-------------|
| 9 | `docs/m365/m365-tenant-evidence-batch-2-report.md` | Batch 2 evidence collection report |

### EA-3 — SharePoint Foundation

| # | File | Description |
|---|------|-------------|
| 10 | `docs/m365/sharepoint-site-design.md` | Site architecture, navigation, and structure design |
| 11 | `docs/m365/library-schema.md` | Column definitions, defaults, views, and index strategy |
| 12 | `docs/m365/content-types.md` | Content type hierarchy (Base, Legacy, Active, Duplicate, Metadata) |
| 13 | `docs/m365/permissions-matrix.md` | Role definitions, permission levels, and sharing policy |
| 14 | `docs/m365/migration-field-map.csv` | Migration manifest-to-SharePoint column mapping |
| 15 | `docs/m365/m365-3-readiness-report.md` | EA-3 phase readiness assessment |

### EA-3P — SharePoint Provisioning (Planning)

| # | File | Description |
|---|------|-------------|
| 16 | `docs/m365/m365-sharepoint-registry-provisioning-plan.md` | Provisioning plan for SharePoint site and registry list |
| 17 | `docs/m365/m365-provisioning-manifest.csv` | Provisioning manifest with resource inventory |
| 18 | `docs/m365/m365-provisioning-authorization-gate.md` | Authorization gate for provisioning |

### EA-4 — Microsoft Lists Registry

| # | File | Description |
|---|------|-------------|
| 19 | `docs/m365/registry-list-schema.md` | RAE Document Registry list column definitions |
| 20 | `docs/m365/sharepoint-registry-field-map.csv` | Registry-to-SharePoint field mapping |
| 21 | `docs/m365/registry-views.md` | Registry list view definitions |
| 22 | `docs/m365/registry-validation-rules.md` | Validation rules for registry entries |
| 23 | `docs/m365/registry-owner-rules.md` | Owner assignment and governance rules |
| 24 | `docs/m365/registry-lifecycle-model.md` | Document lifecycle state machine model |
| 25 | `docs/m365/registry-export-contract.md` | Contract for registry data export format |
| 26 | `docs/m365/m365-4-readiness-report.md` | EA-4 phase readiness assessment |

### Admin Package

| # | File | Description |
|---|------|-------------|
| 27 | `docs/m365/admin/README.md` | Admin request package entry point |
| 28 | `docs/m365/admin/RAE_DOCUMENT_CENTER_SITE_PROVISIONING_REQUEST.md` | Formal technical provisioning request to MJU M365 administrators |
| 29 | `docs/m365/admin/RAE_DOCUMENT_CENTER_BUSINESS_JUSTIFICATION.md` | Business justification for RAE Document Center |
| 30 | `docs/m365/admin/RAE_DOCUMENT_CENTER_SECURITY_SCOPE.md` | Security and governance scope documentation |
| 31 | `docs/m365/admin/RAE_DOCUMENT_CENTER_ADMIN_HANDOFF_CHECKLIST.md` | Admin handoff checklist for post-provisioning confirmation |
| 32 | `docs/m365/admin/EA_ARCHITECTURE_FREEZE_AND_COMMIT_SCOPE.md` | (this file) Architecture baseline, freeze conditions, and commit scope |

**Total files in scope: 32**

---

## 5. Files Out of Scope

These files are present in the working tree but are explicitly excluded from the M365 architecture commit scope.

| Path | Reason for Exclusion |
|------|----------------------|
| `.migration/` (entire directory) | RAE-WTMS migration tooling and metadata. Contains intermediate scripts, debug outputs, and crawl artifacts. Not part of M365 architecture documentation. |
| `migration/` (entire directory) | Migration inventory and QA reports. Operationally consumed but not an architecture document. |
| `docs/reports/` (entire directory) | Business reports (e.g., LINE OA Executive Report). Out of scope for M365 infrastructure architecture. |
| `scripts/generate-line-oa-report.ts` | Standalone report generation script. Not related to M365 architecture. |

> **Note:** Certain files under `migration/` (e.g., `sharepoint-migration-manifest.csv`, `source-inventory.json`) are referenced as source data by architecture documents (see `library-schema.md` §1). These references do **not** pull the files into the architecture commit scope. The manifest is source data, not an architecture artifact.

---

## 6. Recommended Commit Sequence

Commits are grouped by phase to preserve logical isolation. Each group can be committed independently.

### Commit Group 1: EA-1 Foundation

```
M365-1: License audit, readiness matrix, provisioning gates, admin request register
```

Contains: EA-1 files (#1–4)

These are the foundational documents that establish the capability baseline and define gates. Should be committed first.

### Commit Group 2: EA-1B/1C/1D Evidence

```
M365-1B/1C/1D: Tenant evidence runbook, registers, and batch reports
```

Contains: EA-1B files (#5–7), EA-1C file (#8), EA-1D file (#9)

Tenant evidence collection artifacts. Separate from the audit phase because evidence collection is an ongoing operational activity. These files document what was verified and how.

### Commit Group 3: EA-3 SharePoint Foundation

```
M365-3: SharePoint site design, library schema, content types, permissions, field map, readiness
```

Contains: EA-3 files (#10–15)

The core SharePoint architecture package. Largest commit by content. Site design, schema, content types, and permissions form an interdependent set — they should be committed together.

### Commit Group 4: EA-3P Provisioning

```
M365-3P: SharePoint provisioning plan, manifest, and authorization gate
```

Contains: EA-3P files (#16–18)

Provisioning planning documents that operationalize EA-3. These can be committed independently since they reference but do not redefine EA-3 architecture.

### Commit Group 5: EA-4 Registry

```
M365-4: Microsoft Lists registry design, schema, views, validation, lifecycle, export contract, readiness
```

Contains: EA-4 files (#19–26)

The registry design package. Largest file count (8 files). Contains the complete specification for the RAE Document Registry list including the lifecycle state machine and export contract.

### Commit Group 6: Admin Package

```
admin: Admin request package — provisioning request, business justification, security scope, handoff checklist, freeze baseline
```

Contains: Admin Package files (#27–32)

The admin request package for MJU tenant administrators. Contains the formal provisioning request, business justification, security/governance scope, handoff checklist, and this freeze document. Should be committed last, after all architecture files are in the tree.

---

## 7. Recommended Commit Messages

### Template Format

```
{phase}: {short summary}

{body — optional details for complex commits}
```

### Group 1 — EA-1 Foundation

```
M365-1: License audit, readiness matrix, provisioning gates, admin request register

Architecture baseline for RAE Document Center M365 tenant capability and licensing.
Defines provisioning gates G-EA3 through G-EA7 with pass/fail conditions.
Includes admin dependency tracking for tenant administrator action items.
```

### Group 2 — EA-1B/1C/1D Evidence

```
M365-1B/1C/1D: Tenant evidence runbook, registers, and batch reports

Evidence collection artifacts from tenant verification activity.
Documents confirmed capabilities and admin-required dependencies
discovered during EA-1C (Batch 1) and EA-1D (Batch 2) evidence gathering.
```

### Group 3 — EA-3 SharePoint Foundation

```
M365-3: SharePoint site design, library schema, content types, permissions, field map, readiness

Complete SharePoint foundation design for RAE Document Center.
- Site design: architecture, navigation, and library structure
- Library schema: 15-column schema across 6 document libraries
- Content types: 4-tier hierarchy (Base → Legacy/Active/Duplicate + Metadata)
- Permissions: role-based access with least-privilege and separation of duties
- Field map: migration manifest columns mapped to SharePoint internal names
Includes EA-3 readiness assessment.
```

### Group 4 — EA-3P Provisioning

```
M365-3P: SharePoint provisioning plan, manifest, and authorization gate

Provisioning operational plan for creating the RAE Document Center site.
Defines resource inventory (provisioning manifest) and authorization gate
that must pass before site creation proceeds.
```

### Group 5 — EA-4 Registry

```
M365-4: Microsoft Lists registry design, schema, views, validation, lifecycle, export contract

Complete RAE Document Registry specification for Microsoft Lists.
- List schema: columns mapped to SharePoint field internal names
- Views: 7 registry views for different operational perspectives
- Validation: 12 validation rules for data integrity
- Owner rules: assignment, succession, and governance policy
- Lifecycle model: state machine with 7 status values and transition rules
- Export contract: JSON schema for programmatic registry export
Includes EA-4 readiness assessment.
```

### Group 6 — Admin Package

```
admin: Admin request package — provisioning request, business justification, security scope, handoff checklist, freeze baseline

Admin provisioning request package for MJU tenant administrators.
Includes formal site creation request, business justification,
security and governance scope, admin handoff checklist,
and architecture freeze baseline with commit scope.
```

---

## 8. Freeze Conditions

The architecture is considered **frozen** when **all** of the following conditions are met:

### 8.1 Technical Conditions

| # | Condition | Verification Method |
|---|-----------|-------------------|
| F1 | All 32 in-scope files exist at their documented paths | File system scan against §4 table |
| F2 | `DocumentID` format `RAE-NNNNN` is consistently used across all architecture documents | grep `RAE-\d{5}` across all in-scope files |
| F3 | Only the 7 canonical status values appear in status-related definitions | grep status definitions in library-schema.md, content-types.md, registry-lifecycle-model.md |
| F4 | Only the 4 canonical visibility values appear in visibility-related definitions | grep PublicVisibility definitions in library-schema.md, content-types.md |
| F5 | All 9 verified tenant capabilities in §2 match the evidence in EA-1C and EA-1D reports | Cross-reference with batch reports |
| F6 | All 7 admin dependencies in §3 are documented in `m365-admin-request-register.md` | Link check between §3 and admin request register |

### 8.2 Process Conditions

| # | Condition | Owner |
|---|-----------|-------|
| F7 | All 6 commit groups are committed to the repository | Developer |
| F8 | No architectural element in §1 (DocumentID, status, visibility) has been modified since the baseline was recorded | git diff against baseline |
| F9 | The architecture freeze is acknowledged by RAE Digital Transformation | Sign-off |

### 8.3 Freeze Declaration

Once conditions F1–F9 are met, the status of this document changes from `BASELINE_CAPTURED — NOT YET FROZEN` to:

```
Status: FROZEN — Architecture baseline locked
Date frozen: YYYY-MM-DD
Frozen by: [Name / Role]
```

---

## 9. Reopen Conditions

The architecture freeze may be **reopened** under any of the following conditions:

### 9.1 Automatic Reopen Triggers

| # | Trigger | Impact | Required Action |
|---|---------|--------|-----------------|
| R1 | Tenant capability status changes | Any capability in §2 changes status (e.g., `CONFIRMED` → `UNAVAILABLE`, or `ADMIN REQUIRED` → `CONFIRMED`) | Re-verify capability; update §2; re-freeze |
| R2 | SharePoint Online adds or removes column types relevant to library schema | Schema design assumptions invalidated | Review `library-schema.md` column type selections; update if needed |
| R3 | Microsoft Lists changes column/validation capabilities | Registry design assumptions invalidated | Review `registry-list-schema.md` and `registry-validation-rules.md` |
| R4 | Power Automate connector tier changes | EA-5 design assumptions invalidated | Review connector availability; update dependency table |
| R5 | Tenant policy change affecting anonymous sharing, external sharing, or DLP | Visibility model or permission assumptions invalidated | Review `permissions-matrix.md`; update visibility table |

### 9.2 Deliberate Reopen

| # | Reason | Process | Approver |
|---|--------|---------|----------|
| R6 | New EA phase requires modification of a frozen architectural element | Submit architecture change request with impact analysis | RAE Digital Transformation + M365 Administrator |
| R7 | Post-migration operational experience reveals deficiency in frozen values (status, visibility) | Document operational evidence; propose revised values | RAE Digital Transformation |
| R8 | Regulatory or compliance requirement mandates new status or visibility value | Cite regulation; assess impact on existing documents | RAE Digital Transformation + Legal/Compliance |

### 9.3 Reopen Declaration

When a reopen condition is triggered, this document's status changes to:

```
Status: REOPENED — Architecture baseline under review
Date reopened: YYYY-MM-DD
Reopen reason: {trigger reference, e.g., R2}
Reopened by: [Name / Role]
```

After resolution, the document returns to `FROZEN` status with an updated freeze date and a reopen history entry.

### 9.4 Reopen History

| Date | Reason | Resolution | New Freeze Date |
|------|--------|------------|:---------------:|
| — | — | — | — |

---

## Related Documents

| Document | Path |
|----------|------|
| License & Capability Audit | `docs/m365/M365_LICENSE_AUDIT.md` |
| Provisioning Gates | `docs/m365/m365-provisioning-gate.md` |
| Admin Request Register | `docs/m365/m365-admin-request-register.md` |
| Tenant Evidence Runbook | `docs/m365/m365-tenant-evidence-runbook.md` |
| EA-1C Batch 1 Report | `docs/m365/m365-tenant-evidence-batch-1-report.md` |
| EA-1D Batch 2 Report | `docs/m365/m365-tenant-evidence-batch-2-report.md` |
| SharePoint Site Design | `docs/m365/sharepoint-site-design.md` |
| Library Schema | `docs/m365/library-schema.md` |
| Content Types | `docs/m365/content-types.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Registry List Schema | `docs/m365/registry-list-schema.md` |
| Registry Lifecycle Model | `docs/m365/registry-lifecycle-model.md` |
| M365 Foundation Blueprint | `docs/document-center/M365 FoundationBlueprint.MD` |
