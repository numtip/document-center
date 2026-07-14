# EA / M365 Architecture — Gap Matrix (Forward Implementation View)

**Project:** RAE Document Center  
**Analyst:** Co-Work B (EA / M365 Recovery Analyst)  
**Date:** 2026-07-12  
**Canonical repo:** `F:\projectAi\document-center` (GitHub: numtip/document-center)  
**Comparison basis:** Claimed EA artifact inventory (source unverifiable) vs. actual GitHub content  

---

## Purpose

Map every claimed EA / M365 architecture artifact against what actually exists in the canonical GitHub repository. Each artifact is classified to determine whether forward implementation is needed.

---

## Gap Matrix

### EA-3A — SharePoint Foundation

| # | Claimed Artifact | Detail | GitHub Status | Gap Classification | Notes |
|---|-----------------|--------|---------------|-------------------|-------|
| 1 | 10 document libraries | SharePoint Online document libraries for RAE | **PARTIAL** | PARTIAL | M365 Blueprint (Phase M365-3) lists 6 libraries. Claim says 10 — 4 additional libraries unaccounted for. |
| 2 | 21 site columns | Metadata columns defined at SharePoint site level | **MISSING** | MISSING | M365 Blueprint mentions 9 metadata columns in Phase M365-3. No SharePoint site-column schema documents exist. |
| 3 | 11 content types | SharePoint content types for document classification | **MISSING** | MISSING | No content type definitions exist in GitHub. REGISTRY_DATA_MODEL.md uses a flat document schema with no content type hierarchy. |
| 4 | 8 views | SharePoint list/library views for different user roles | **MISSING** | MISSING | UI_BLUEPRINT.md defines UI views for the Next.js frontend, not SharePoint views. No SharePoint-specific view definitions. |
| 5 | 6 permission groups | SharePoint permission groups for access control | **PARTIAL** | PARTIAL | ONEDRIVE_PERMISSION_POLICY.md defines 6 roles (Platform Admin, Category Owner, Document Owner, Contributor, Reader, Archive Manager). These are not SharePoint permission groups — they are role descriptions for OneDrive. |

### EA-3B — PnP Provisioning

| # | Claimed Artifact | Detail | GitHub Status | Gap Classification | Notes |
|---|-----------------|--------|---------------|-------------------|-------|
| 1 | PnP PowerShell preflight scripts | Provisioning scripts for SharePoint Online site setup | **MISSING** | MISSING | No .ps1 files, no PnP-related scripts, no provisioning automation of any kind exist in GitHub. |

### EA-3C.1 — M365 Tenant Assessment

| # | Claimed Artifact | Detail | GitHub Status | Gap Classification | Notes |
|---|-----------------|--------|---------------|-------------------|-------|
| 1 | M365 admin questions document | Admin questionnaire for tenant readiness | **MISSING** | MISSING | M365 FoundationBlueprint Phase M365-1 is a brief checklist, not a detailed admin questions document. |
| 2 | Tenant capability checklist | What M365 services are available/enabled | **PARTIAL** | PARTIAL | Phase M365-1 in the Blueprint lists 9 services to check. But this is a 1-page outline, not a detailed checklist with status. |
| 3 | Permission requirements document | Detailed permission matrix for M365 roles | **PARTIAL** | PARTIAL | ONEDRIVE_PERMISSION_POLICY.md covers OneDrive permissions. No M365-wide permission requirements document exists. |
| 4 | Integration decision matrix | Decisions on how M365 services integrate | **MISSING** | MISSING | M365 Blueprint describes a target architecture (WTMS → SharePoint → Lists → Power Automate → Portal) but includes no decision matrix comparing options with trade-offs. |

### EA-3D — Taxonomy v2

| # | Claimed Artifact | Detail | GitHub Status | Gap Classification | Notes |
|---|-----------------|--------|---------------|-------------------|-------|
| 1 | 10 domains | Top-level taxonomy domains | **MISSING** | MISSING | GitHub taxonomy.json has 6 categories (v1.0.0). Claim says 10 domains — 4 additional domains unaccounted for. |
| 2 | 30 categories | Mid-level taxonomy categories | **MISSING** | MISSING | GitHub has no mid-level category layer. The flat 6-category model has no hierarchical breakdown. |
| 3 | 62 subcategories | Detailed subcategory classification | **MISSING** | MISSING | No subcategory field exists in REGISTRY_DATA_MODEL.md. |
| 4 | 11 document types | Document type classification | **MISSING** | MISSING | REGISTRY_DATA_MODEL.md has `file_type` (extension-based) not document types. No document type taxonomy exists. |

### EA-3E — Extended Metadata Registry

| # | Claimed Artifact | Detail | GitHub Status | Gap Classification | Notes |
|---|-----------------|--------|---------------|-------------------|-------|
| 1 | 26 metadata fields | Total fields in the registry schema | **MISSING** | MISSING | REGISTRY_DATA_MODEL.md defines 13 fields for the Document object (id, title, category, owner, file_type, status, updated_date, onedrive_path, storage_url, tags, version, visibility, note). Claim says 26 — 13 additional fields unaccounted for. |
| 2 | 15 required registry fields | Mandatory fields | **MISSING** | MISSING | REGISTRY_DATA_MODEL.md has 10 required fields (all except storage_url, note, and tags are conditional). Claim says 15 — 5 additional required fields unaccounted for. |
| 3 | Expanded status model | More granular status values | **MISSING** | MISSING | GitHub has 4 status values (current, obsolete, archived, draft). Consider additional states as part of forward design (e.g., pending-review, approved, published). |
| 4 | Visibility governance rules | Rules for who can see what | **PARTIAL** | PARTIAL | REGISTRY_DATA_MODEL.md defines 3 visibility values (public, internal, restricted). ONEDRIVE_PERMISSION_POLICY.md adds governance context. The claimed version may have more granular rules. |
| 5 | DocumentID standard | ID format and assignment rules | **PRESENT_EQUIVALENT** | PRESENT_EQUIVALENT | DOCUMENT_NAMING_STANDARD.md covers this thoroughly. If the WORK PC version is more detailed, consider MERGE_WITH_EXISTING. |
| 6 | Public export policy | Rules for exporting/publishing public documents | **MISSING** | MISSING | No formal public export policy document exists. The README and UI_BLUEPRINT.md mention public vs internal, but no formal export policy. |
| 7 | AI source eligibility policy | Which documents can be used as AI training/source material | **MISSING** | MISSING | No AI-related governance documents exist in GitHub. |

### Memory OS

| # | Claimed Artifact | Detail | GitHub Status | Gap Classification | Notes |
|---|-----------------|--------|---------------|-------------------|-------|
| 1 | Memory OS / AI agent context | AI agent configuration and context for the project | **MISSING** | MISSING | No .cursor/, SKILL.md, AI.md, CORE.md, AGENTS.md, or any Memory OS artifacts found in the canonical repository. Zero references to "Memory OS" in any file. |

---

## Summary

| EA Phase | Artifacts Claimed | PRESENT_EQUIVALENT | PARTIAL | MISSING | Implementation Priority |
|----------|------------------|-------------------|---------|---------|-------------------|
| EA-3A | 5 | 0 | 2 | 3 | **HIGH** — Missing SharePoint foundation blocks EA-3F site provisioning |
| EA-3B | 1 | 0 | 0 | 1 | **HIGH** — No provisioning automation exists |
| EA-3C.1 | 4 | 0 | 2 | 2 | **HIGH** — Missing tenant assessment docs block M365 readiness |
| EA-3D | 4 | 0 | 0 | 4 | **CRITICAL** — Taxonomy v2 with 10 domains is essential for EA-3F |
| EA-3E | 7 | 1 | 2 | 4 | **HIGH** — Extended fields and expanded model needed |
| Memory OS | 1 | 0 | 0 | 1 | **MEDIUM** — Agent context useful but not blocking architecture |
| **Total** | **22** | **1** | **6** | **15** | |

### Classification Definitions

| Classification | Meaning |
|----------------|---------|
| **PRESENT_EQUIVALENT** | The artifact exists in GitHub with equivalent scope and detail. |
| **PARTIAL** | Some coverage exists in GitHub but scope/detail is less than claimed. |
| **MISSING** | No equivalent artifact exists in the canonical GitHub repository. |

---

## Key Architecture Conflicts

1. **Taxonomy scope mismatch**: GitHub taxonomy.json defines 6 categories. Claimed EA-3D Taxonomy v2 has 10 domains, 30 categories, 62 subcategories, 11 document types. This is a fundamental scope difference — the GitHub taxonomy is a flat list; the claimed taxonomy is a multi-level hierarchy.

2. **Metadata field count**: GitHub REGISTRY_DATA_MODEL.md defines 13 document fields. Claimed EA-3E has 26 metadata fields — twice the current count. The expanded set likely includes fields for compliance dates, approval workflow state, retention schedule, and AI eligibility flags.

3. **SharePoint site maturity**: M365 FoundationBlueprint.MD describes intent (Phase M365-3: SharePoint Foundation) but no actual SharePoint site schema, content types, columns, or views exist. The claimed EA-3A implies these were designed.

4. **PnP automation gap**: GitHub has TypeScript validation scripts (Node.js/tsx) but zero PowerShell/PnP provisioning scripts. The claimed EA-3B suggests PnP was the chosen automation approach — this is a stack divergence that must be reconciled.

5. **Memory OS absence**: The claimed "Memory OS" AI agent context has zero presence in GitHub. If this represents agent knowledge or project context for AI coding tools, it was never committed to the canonical repository.

---

## EA-3F Readiness Determination

**Decision: FORWARD_IMPLEMENTATION_REQUIRED_BEFORE_EA_3F**

### Evidence

The canonical GitHub repository is **not ready** to support EA-3F planning. The following gaps are real and must be closed through forward design and implementation — no external source exists to import from.

1. **Taxonomy incompleteness**: EA-3F requires a mature taxonomy to define the information architecture. GitHub has 6 flat categories. The claimed Taxonomy v2 has 10 domains + 30 categories + 62 subcategories + 11 document types — an order of magnitude more structure. EA-3F planned against GitHub's 6 categories would produce a fundamentally different architecture than one planned against the full v2 taxonomy.

2. **SharePoint foundation missing**: EA-3F involves provisioning and configuring the M365 platform. Without the SharePoint site design, library schemas, content types, site columns, and permission groups from EA-3A, EA-3F would need to design these from scratch.

3. **Provisioning automation**: EA-3B's PnP scripts were never created. The provisioning approach must be designed from scratch.

4. **Metadata foundation insufficient**: GitHub's 13-field registry model (with 10 required fields) is simpler than the 26-field model described in the M365 Blueprint. EA-3F's governance and compliance requirements likely depend on the extended field set.

5. **Governance policies missing**: Public export policy, AI source eligibility policy, and expanded governance rules are absent. EA-3F's governance framework would be incomplete without these.

### What exists that IS usable for EA-3F

The following GitHub artifacts provide partial foundation and should inform EA-3F planning:

- **M365 FoundationBlueprint.MD** — Provides the target architecture vision and 9-phase M365 plan
- **REGISTRY_DATA_MODEL.md** — Locked data model that can serve as a baseline (to be extended)
- **taxonomy.json** — v1.0.0 can serve as a starting point for taxonomy expansion
- **ONEDRIVE_PERMISSION_POLICY.md** — Permission principles that can map to SharePoint permission groups
- **UI_BLUEPRINT.md** — Frontend architecture that defines the public experience layer
- **Document naming standard** — Stable ID convention that will carry forward

### Recommended path

1. **Design and author missing EA-3A–3E artifacts directly against the canonical repository** — there is no external source to import from. All SharePoint foundation, taxonomy v2, extended registry, governance policies, and provisioning approach must be designed and authored from scratch against the canonical repository.
2. **Reconcile taxonomy v2 with v1** via Architecture Decision Record
3. **Extend REGISTRY_DATA_MODEL.md** to cover the additional 13 fields
4. **Reconcile PnP approach with TypeScript validation approach** (or accept both)
5. **Then proceed with EA-3F planning** using the enriched artifact set
