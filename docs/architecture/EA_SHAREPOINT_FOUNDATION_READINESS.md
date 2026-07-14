# EA SharePoint Foundation Readiness Assessment — RAE Document Center

**Version:** 1.0  
**Status:** Assessment only — no provisioning  
**Date:** 2026-07-12  
**Authority:** EA-3F Forward Architecture Readiness

---

## Purpose

Assess readiness for the future EA-3F SharePoint Foundation implementation phase. This is a **readiness assessment**, not a provisioning plan. Every classification is derived from repository evidence only — no tenant capabilities are assumed or claimed without direct evidence.

---

## Classification Legend

| Classification | Meaning |
|----------------|---------|
| **READY** | The dependency exists in canonical repository, is validated, and requires no further design or decision before EA-3F. |
| **READY_WITH_DECISION** | The dependency exists but has open architectural choices that must be resolved via ADR before EA-3F implementation can proceed. |
| **BLOCKED_BY_TENANT_AUDIT** | Readiness cannot be determined without direct M365 tenant evidence. The tenant capability audit must complete first. |
| **NOT_READY** | The dependency does not exist and must be designed/built before EA-3F can proceed. No external source exists — this is forward implementation work. |

---

## Readiness Assessment

### 1. Target SharePoint Site

| Aspect | Detail |
|--------|--------|
| **Site name** | RAE Document Center (per M365 Blueprint Phase M365-3) |
| **Site type** | Communication site (implied by public-facing role) |
| **Evidence in repo** | `M365 FoundationBlueprint.MD` — Phase M365-3, bullet: "Create Site: RAE Document Center" |
| **Design deliverable** | `sharepoint-site-design.md` — **does not exist** |
| **Architecture constraint** | Website is presentation layer only; SharePoint is operational governance layer |

**Classification: NOT_READY**

The site topology, navigation structure, hub association, and external sharing settings must be designed and approved. No site design document exists. The M365 Blueprint names the site but provides no structural detail beyond the name.

---

### 2. Proposed Document Libraries

| Aspect | Detail |
|--------|--------|
| **Target libraries** | Administration, FinanceProcurement, Research, AcademicServices, PlanningPolicy, SOPManuals (6 libraries per Blueprint Phase M365-3) |
| **OneDrive equivalent** | 6 category folders in `PHASE3_ONEDRIVE_STORAGE_GUIDE.md` (01–06) |
| **Evidence in repo** | `M365 FoundationBlueprint.MD` lists 6 library names. `taxonomy.json` defines 6 matching categories. |
| **Gap vs. claim** | Claim says 10 libraries. Blueprint lists 6. 4 additional libraries are unaccounted for. |
| **Design deliverable** | `library-schema.md` — **does not exist** |

**Classification: NOT_READY**

Six of the target libraries can be derived from existing taxonomy categories. The claimed 10-library set (4 additional) must be resolved via ADR. Library schema (columns, templates, versioning, retention) must be designed from scratch. The claimed 10-library target is inconsistent with the Blueprint's 6 libraries — this scope question needs resolution before design.

---

### 3. Taxonomy Dependencies

| Aspect | Detail |
|--------|--------|
| **Existing taxonomy** | `taxonomy.json` v1.0.0 — 6 flat categories with Thai/English names, folder mappings, owner groups |
| **Target taxonomy** | Claimed 10 domains / 30 categories / 62 subcategories / 11 document types |
| **Evidence in repo** | Only v1.0.0 flat taxonomy exists. Hierarchical v2 taxonomy does not exist |
| **SharePoint impact** | Content types, site columns, managed metadata, and library views all depend on taxonomy structure |

**Classification: READY_WITH_DECISION**

The existing v1.0.0 taxonomy is validated and usable as a minimal starting point. However, EA-3F provisioning against 6 flat categories would produce a fundamentally different architecture than provisioning against a hierarchical v2 taxonomy. An ADR must decide: keep v1, extend compatibly, or replace with v2 before SharePoint content types and site columns can be designed.

---

### 4. Metadata Dependencies

| Aspect | Detail |
|--------|--------|
| **Existing registry** | `REGISTRY_DATA_MODEL.md` — 13 fields locked v1.0.0 |
| **Target registry** | Claimed 26 fields in M365 Blueprint Phase M365-4 (10 fields for Lists) |
| **Evidence in repo** | 13-field model is real and validated. No extended 26-field model exists |
| **SharePoint impact** | Site columns, content type columns, and list columns all derive from the registry data model |

**Classification: READY_WITH_DECISION**

The existing 13-field model can be mapped directly to SharePoint site columns and Lists columns. The M365 Blueprint Phase M365-4 proposes 10 fields for the Lists Registry schema — this is a subset of the 13-field model plus any new fields. An ADR must decide whether to extend to 26 fields or adopt a subset before SharePoint column definitions can be finalized. The 13-field model is sufficient for a minimal SharePoint foundation; the extended set is needed for full governance coverage.

---

### 5. Status Model

| Aspect | Detail |
|--------|--------|
| **Existing status values** | `current`, `obsolete`, `archived`, `draft` (4 values) |
| **Target status values** | Claimed expanded set including `pending-review`, `approved`, `published` |
| **Evidence in repo** | 4 values defined in `REGISTRY_DATA_MODEL.md` and enforced by validators |
| **SharePoint impact** | Status is a required field in the document registry. SharePoint content type choice column must match the approved status set |

**Classification: READY_WITH_DECISION**

The existing 4-value status model is validated and functional. An expanded status model would improve governance fidelity (e.g., distinguishing `draft` from `pending-review`, `approved` from `published`). The scope of expansion must be decided before SharePoint content type design — each status value maps to a choice column option. The decision is bounded: expand or keep, not whether a status model exists.

---

### 6. Visibility Model

| Aspect | Detail |
|--------|--------|
| **Existing visibility values** | `public`, `internal`, `restricted` (3 values) |
| **Evidence in repo** | Defined in `REGISTRY_DATA_MODEL.md`, enforced by `build-preview.ts` (blocks non-public from preview) |
| **SharePoint impact** | Visibility maps to SharePoint permission scopes, sharing policies, and item-level permissions |

**Classification: READY_WITH_DECISION**

The existing 3-value visibility model is validated and actively enforced by the preview pipeline. Mapping to SharePoint permission levels needs design (how `restricted` is enforced in SharePoint vs. OneDrive), but the conceptual model is ready. The decision is how SharePoint enforces each value, not what the values are.

---

### 7. Ownership Model

| Aspect | Detail |
|--------|--------|
| **Existing ownership** | `owner` field (email or role string) in registry, `owner_group` in taxonomy, 6 roles in `ONEDRIVE_PERMISSION_POLICY.md` |
| **Evidence in repo** | `REGISTRY_DATA_MODEL.md` requires non-empty `owner`. `ONEDRIVE_PERMISSION_POLICY.md` defines 6 roles. |
| **SharePoint impact** | SharePoint permission groups, column-level ownership, and approval workflows all depend on the ownership model |

**Classification: NOT_READY**

While the ownership concept exists in the registry, SharePoint permission groups (6 groups claimed) are not designed. The existing OneDrive roles (Platform Admin, Category Owner, Document Owner, Contributor, Reader, Archive Manager) are a starting point but must be mapped to SharePoint permission groups and Entra ID groups. The ownership model is documented-on-OneDrive but not designed-for-SharePoint.

---

### 8. Permission Model Dependency

| Aspect | Detail |
|--------|--------|
| **Existing permission model** | `ONEDRIVE_PERMISSION_POLICY.md` — OneDrive-specific folder-level permission matrix |
| **Target permission model** | SharePoint permission groups + Entra ID group mapping |
| **Evidence in repo** | OneDrive policy exists and is detailed. No SharePoint/AD permission mapping exists. |
| **SharePoint impact** | SharePoint site-level, library-level, and item-level permission inheritance must be designed |

**Classification: NOT_READY**

The OneDrive permission policy is a useful reference but is not a SharePoint permission design. SharePoint groups, permission levels, inheritance strategy, and external sharing policies are all undefined. The claimed 6 permission groups need design and AD group mapping that depends on tenant audit results (available groups, licensing).

---

### 9. Public Export Dependency

| Aspect | Detail |
|--------|--------|
| **Existing public export** | `build-preview.ts` — filters to `visibility=public` + `status=current` + demo URLs only |
| **Target public export** | Formal public export policy + automated Microsoft Lists → GitHub export |
| **Evidence in repo** | Preview pipeline exists and is validated. No formal public export policy document exists. |
| **SharePoint impact** | Public-facing documents require explicit visibility designation, valid share links, and owner accountability |

**Classification: NOT_READY**

The technical export pipeline exists (build-preview.ts), but no formal public export policy governs what qualifies for public export, who authorizes it, the review cycle, or the revocation process. Without this policy, SharePoint external sharing settings and Lists export scope cannot be configured. The pipeline is ready; the policy is not.

---

### 10. Migration Dependency

| Aspect | Detail |
|--------|--------|
| **Existing migration artifacts** | Migration matrix (`migration-matrix.v2.csv`, 42 rows, validated), OneDrive prep-map generation |
| **Target migration** | OneDrive → SharePoint Online migration with metadata preservation |
| **Evidence in repo** | Migration matrix classifies 42 legacy documents (30 keep, 5 merge, 4 review, 2 drop, 1 rewrite). Prep-map generator exists. |
| **SharePoint impact** | Migration approach, tooling, and metadata mapping must be designed before site provisioning |

**Classification: NOT_READY**

The migration matrix provides an excellent document-level migration classification, but the SharePoint migration approach is undefined. Key decisions pending:
- Manual upload vs. migration tool (SharePoint Migration Tool, PnP, or custom)
- Metadata preservation strategy from JSON registry → SharePoint columns
- Link preservation for public documents
- Cutover approach (big bang vs. phased by category)

---

### 11. Tenant Capability Dependency

| Aspect | Detail |
|--------|--------|
| **Required capabilities** | SharePoint Online, Microsoft Lists, Power Automate, Teams Approvals, Forms, Power BI, Graph API, Azure App Registration, Copilot |
| **Evidence in repo** | `M365 FoundationBlueprint.MD` Phase M365-1 checklist (template only) |
| **Tenant evidence** | **None.** No `M365_LICENSE_AUDIT.md` exists. No tenant has been verified. |
| **SharePoint impact** | Without tenant verification, no SharePoint provisioning can proceed |

**Classification: BLOCKED_BY_TENANT_AUDIT**

Every capability listed in Blueprint Phase M365-1 is an unverified assumption. The `M365_LICENSE_AUDIT.md` deliverable was never produced. EA-3F cannot begin SharePoint provisioning until the tenant capability audit confirms SharePoint Online, Lists, and Power Automate are available in the target tenant with sufficient licensing.

---

## Summary

| # | Dependency | Classification |
|---|------------|---------------|
| 1 | Target SharePoint site | **NOT_READY** |
| 2 | Proposed document libraries | **NOT_READY** |
| 3 | Taxonomy dependencies | **READY_WITH_DECISION** |
| 4 | Metadata dependencies | **READY_WITH_DECISION** |
| 5 | Status model | **READY_WITH_DECISION** |
| 6 | Visibility model | **READY_WITH_DECISION** |
| 7 | Ownership model | **NOT_READY** |
| 8 | Permission model dependency | **NOT_READY** |
| 9 | Public export dependency | **NOT_READY** |
| 10 | Migration dependency | **NOT_READY** |
| 11 | Tenant capability dependency | **BLOCKED_BY_TENANT_AUDIT** |

### Readiness Count

| Classification | Count | Areas |
|----------------|-------|-------|
| READY | 0 | — |
| READY_WITH_DECISION | 4 | Taxonomy, Metadata, Status model, Visibility model |
| NOT_READY | 6 | SharePoint site, Libraries, Ownership, Permissions, Public export, Migration |
| BLOCKED_BY_TENANT_AUDIT | 1 | Tenant capability dependency |

---

## Immediate Actions for EA-3F Readiness

1. **Complete M365 tenant capability audit** (see `M365_TENANT_CAPABILITY_AUDIT_PLAN.md`) — unblocks the `BLOCKED_BY_TENANT_AUDIT` dependency. This is prerequisite to all other work.
2. **Resolve taxonomy ADR** (see `ADR_TAXONOMY_V2_DIRECTION.md`) — decides whether SharePoint content types model v1 or v2 taxonomy.
3. **Resolve registry ADR** (see `ADR_EXTENDED_REGISTRY_DIRECTION.md`) — decides the field set for SharePoint site columns and Lists schema.
4. **Author SharePoint site design** — site topology, navigation, hub, sharing settings.
5. **Design SharePoint permission groups** — map OneDrive roles + Entra ID groups to SharePoint permission levels.
6. **Author public export policy** — governance for what qualifies as public and how it is authorized.
7. **Define migration approach** — tooling, metadata mapping, cutover strategy.
8. **Author remaining NOT_READY artifacts** — ownership model detail, library schemas.

---

## Related Documents

- [M365 Tenant Capability Audit Plan](./M365_TENANT_CAPABILITY_AUDIT_PLAN.md) — audit plan for unblocking tenant dependencies
- [EA Forward Implementation Baseline](./EA_FORWARD_IMPLEMENTATION_BASELINE.md) — canonical current state
- [ADR: Taxonomy v2 Direction](./ADR_TAXONOMY_V2_DIRECTION.md) — taxonomy evolution decision
- [ADR: Extended Registry Direction](./ADR_EXTENDED_REGISTRY_DIRECTION.md) — registry schema evolution decision
