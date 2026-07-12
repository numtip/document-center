# EA Legacy Recovery Manifest — WORK PC Artifact Inventory

**Project:** RAE Document Center  
**Analyst:** Co-Work B (EA / M365 Recovery Analyst)  
**Date:** 2026-07-12  
**Recovery source:** `G:\ProjectAI\RAE-M365-Platform`  
**Canonical target:** `G:\ProjectAI\document-center` (WORK PC checkout)  

---

## Purpose

Manifest of artifacts to locate, inspect, and classify during the one-time WORK PC recovery operation. Each entry describes what to look for, what evidence supports its existence, and how to handle it once found.

---

## Recovery Item Registry

### EA-3A — SharePoint Foundation Artifacts

| # | Recovery Item | Expected Role | Evidence Required | Likely File/Path Pattern | Canonical Comparison Target | Import Classification |
|---|---------------|--------------|-------------------|--------------------------|----------------------------|----------------------|
| 1 | SharePoint Site Design Document | Blueprint for RAE Document Center SharePoint site structure | `.md` or `.docx` file at recovery source describing site topology, library structure, navigation | `RAE-M365-Platform\EA-3A\sharepoint-site-design.md` or `*-site-design*` | `docs/document-center/M365 FoundationBlueprint.MD` (Section M365-3) | REQUIRES_ADR_REVIEW |
| 2 | Document Library Schema (10 libraries) | Library definitions with column schemas | CSV, JSON, or MD listing 10 library names, descriptions, and schema | `RAE-M365-Platform\EA-3A\libraries\library-schema.*` or `*-libraries.*` | `docs/document-center/PHASE3_ONEDRIVE_STORAGE_GUIDE.md` (6 OneDrive folders) | MERGE_WITH_EXISTING |
| 3 | Site Column Definitions (21 columns) | Column definitions: name, type, required, default, choices | `.xml`, `.json`, or `.md` containing column definitions. Look for PnP schema XML. | `RAE-M365-Platform\EA-3A\columns\*.xml` or `columns\*.json` | NONE | IMPORT_AS_AUTHORITATIVE |
| 4 | Content Type Definitions (11 types) | Document content types with associated columns | `.xml` or `.json` content type definitions. PnP schema or manual spec. | `RAE-M365-Platform\EA-3A\content-types\*.xml` or `content-types\*.json` | NONE | IMPORT_AS_AUTHORITATIVE |
| 5 | View Definitions (8 views) | List/library views for different roles | View schema or description documents | `RAE-M365-Platform\EA-3A\views\*.md` or `views\*.json` | `docs/document-center/UI_BLUEPRINT.md` (frontend views only) | MERGE_WITH_EXISTING |
| 6 | SharePoint Permission Groups (6 groups) | Permission level definitions for SharePoint groups | Permission matrix or group definition document | `RAE-M365-Platform\EA-3A\permissions\*` | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` | MERGE_WITH_EXISTING |

### EA-3B — PnP Provisioning

| # | Recovery Item | Expected Role | Evidence Required | Likely File/Path Pattern | Canonical Comparison Target | Import Classification |
|---|---------------|--------------|-------------------|--------------------------|----------------------------|----------------------|
| 1 | PnP PowerShell Preflight Scripts | Automated provisioning scripts for SharePoint Online | `.ps1` files containing `Connect-PnPOnline`, `New-PnPList`, `Add-PnPContentType` commands | `RAE-M365-Platform\EA-3B\pnp\*.ps1` or `scripts\pnp-*` | NONE | REQUIRES_ADR_REVIEW |
| 2 | PnP provisioning template (if exists) | XML/JSON template for site provisioning | `.xml` PnP provisioning template files | `RAE-M365-Platform\EA-3B\templates\*.xml` or `pnp-template*` | NONE | REQUIRES_ADR_REVIEW |

### EA-3C.1 — M365 Tenant Assessment

| # | Recovery Item | Expected Role | Evidence Required | Likely File/Path Pattern | Canonical Comparison Target | Import Classification |
|---|---------------|--------------|-------------------|--------------------------|----------------------------|----------------------|
| 1 | M365 Admin Questions Document | Completed admin questionnaire for tenant readiness | `.md` or `.docx` with M365 admin questions and answers. Look for assessment narrative, IT responses. | `RAE-M365-Platform\EA-3C.1\m365-admin-questions.*` or `*-admin-survey*` | `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-1 checklist) | MERGE_WITH_EXISTING |
| 2 | Tenant Capability Checklist | Detailed checklist of available M365 services | `.md`, `.csv`, or `.xlsx` checklist with status per service | `RAE-M365-Platform\EA-3C.1\tenant-capability-checklist.*` or `*-capability-*` | `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-1) | MERGE_WITH_EXISTING |
| 3 | Permission Requirements Document | Detailed M365-wide permission requirements | `.md` document describing roles, permission scopes, and AD group mappings | `RAE-M365-Platform\EA-3C.1\permission-requirements.*` or `*-m365-permissions*` | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` | MERGE_WITH_EXISTING |
| 4 | Integration Decision Matrix | Compare/contrast integration approaches | `.md` or `.csv` evaluating integration options (Graph API vs export JSON vs other) | `RAE-M365-Platform\EA-3C.1\integration-decision-matrix.*` or `*-integration-*` | `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-8 mentions Registry Export JSON preference) | IMPORT_AS_AUTHORITATIVE |

### EA-3D — Taxonomy v2

| # | Recovery Item | Expected Role | Evidence Required | Likely File/Path Pattern | Canonical Comparison Target | Import Classification |
|---|---------------|--------------|-------------------|--------------------------|----------------------------|----------------------|
| 1 | Taxonomy v2 JSON/MD | Expanded taxonomy with 10 domains, 30 categories, 62 subcategories, 11 document types | `.json` or `.md` file with hierarchical taxonomy. Should show domain → category → subcategory tree. | `RAE-M365-Platform\EA-3D\taxonomy.v2.*` or `*-taxonomy-v2*` | `docs/document-center/taxonomy.json` (6 flat categories) | REQUIRES_ADR_REVIEW |
| 2 | Domain definitions (10) | Top-level domain metadata | Embedded in taxonomy v2 file or separate domain definitions | `RAE-M365-Platform\EA-3D\domains.*` | NONE | IMPORT_AS_AUTHORITATIVE |
| 3 | Document type taxonomy (11 types) | Document type classification system | Document type definitions with metadata mappings | `RAE-M365-Platform\EA-3D\document-types.*` | NONE | IMPORT_AS_AUTHORITATIVE |

### EA-3E — Extended Metadata Registry

| # | Recovery Item | Expected Role | Evidence Required | Likely File/Path Pattern | Canonical Comparison Target | Import Classification |
|---|---------------|--------------|-------------------|--------------------------|----------------------------|----------------------|
| 1 | Extended Registry Data Model (26 fields) | Full metadata schema with 26 fields | `.md`, `.json`, or `.csv` listing all fields, types, required status, validation rules | `RAE-M365-Platform\EA-3E\registry-data-model.*` or `*-extended-registry*` | `docs/document-center/REGISTRY_DATA_MODEL.md` (13 fields) | REQUIRES_ADR_REVIEW |
| 2 | Expanded Status Model | More granular document status values | Status model definition with transitions and rules | `RAE-M365-Platform\EA-3E\status-model.*` or embedded in registry doc | `docs/document-center/REGISTRY_DATA_MODEL.md` (4 statuses) | MERGE_WITH_EXISTING |
| 3 | Visibility Governance Rules | Detailed rules for document visibility | Governance document defining who can see what, exception process | `RAE-M365-Platform\EA-3E\visibility-governance.*` | `docs/document-center/REGISTRY_DATA_MODEL.md` (3 visibility values) + `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` | MERGE_WITH_EXISTING |
| 4 | Public Export Policy | Rules and process for public document export | Policy document defining export criteria, format, review cycle | `RAE-M365-Platform\EA-3E\public-export-policy.*` | NONE | IMPORT_AS_AUTHORITATIVE |
| 5 | AI Source Eligibility Policy | Which documents qualify as AI training source | Policy document with eligibility criteria, opt-out process | `RAE-M365-Platform\EA-3E\ai-source-policy.*` | NONE | IMPORT_AS_AUTHORITATIVE |

### Memory OS

| # | Recovery Item | Expected Role | Evidence Required | Likely File/Path Pattern | Canonical Comparison Target | Import Classification |
|---|---------------|--------------|-------------------|--------------------------|----------------------------|----------------------|
| 1 | Memory OS Configuration | AI agent context/project memory for coding agents | `.cursor/rules/`, `*.memory.*`, `memory-os.*`, `SKILL.md`, `AGENTS.md` files | `RAE-M365-Platform\\.ai\\*`, `RAE-M365-Platform\\.cursor\\*`, `RAE-M365-Platform\\CORE.md`, `RAE-M365-Platform\\SKILL.md` | NONE | REQUIRES_ADR_REVIEW |
| 2 | Agent workflow definitions | Automated agent workflows for the project | Workflow definition files | `RAE-M365-Platform\\.cursor\\workflows\\*` or workflow automation files | NONE | RETAIN_AS_HISTORICAL |

---

## Import Classification Guide

| Classification | Action |
|----------------|--------|
| **IMPORT_AS_AUTHORITATIVE** | The artifact does not exist in GitHub. Import as-is — it becomes the canonical version. |
| **MERGE_WITH_EXISTING** | A partial equivalent exists in GitHub. Compare, reconcile differences, then merge. |
| **RETAIN_AS_HISTORICAL** | Keep in recovery source for reference but do not import into GitHub. Useful for understanding decisions without polluting current docs. |
| **DO_NOT_IMPORT_DUPLICATE** | The artifact already exists in canonical GitHub with sufficient quality. Skip import. |
| **REQUIRES_ADR_REVIEW** | The artifact has architectural implications that need an Architecture Decision Record before import. |

---

## Recovery Item Count

| Import Classification | Count | Items |
|----------------------|-------|-------|
| IMPORT_AS_AUTHORITATIVE | 7 | Site columns, Content types, Integration decision matrix, Domain definitions, Document type taxonomy, Public export policy, AI source eligibility policy |
| MERGE_WITH_EXISTING | 9 | Library schema, View definitions, Permission groups, Admin questions, Capability checklist, Permission requirements, Status model, Visibility governance rules, DocumentID standard |
| RETAIN_AS_HISTORICAL | 1 | Agent workflow definitions (Memory OS) |
| DO_NOT_IMPORT_DUPLICATE | 0 | — |
| REQUIRES_ADR_REVIEW | 5 | Site design, PnP scripts, PnP templates, Taxonomy v2, Extended registry data model, Memory OS configuration |
| **Total** | **23** | (from 22 claimed artifacts + 1 Memory OS sub-item) |
