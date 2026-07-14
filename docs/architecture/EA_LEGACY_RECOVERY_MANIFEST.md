# EA / M365 Architecture — Forward Implementation Manifest

**Project:** RAE Document Center  
**Analyst:** Co-Work B (EA / M365 Architecture Analyst)  
**Date:** 2026-07-12  
**Canonical repo:** `numtip/document-center` (GitHub)

---

## Purpose

Manifest of forward-implementation items for EA / M365 architecture artifacts that exist only as claimed items (not as real, committed files in the canonical GitHub repository). Each entry describes what to build, what evidence supports the need, and how to proceed.

No external recovery source exists. All items in this manifest must be designed and authored directly against the canonical repository.

---

## Forward Implementation Item Registry

### EA-3A — SharePoint Foundation Artifacts

| # | Implementation Item | Expected Role | Evidence Required | Canonical Comparison Target | Implementation Classification |
|---|---------------------|--------------|-------------------|----------------------------|------------------------------|
| 1 | SharePoint Site Design Document | Blueprint for RAE Document Center SharePoint site structure | `.md` or `.docx` describing site topology, library structure, navigation | `docs/document-center/M365 FoundationBlueprint.MD` (Section M365-3) | NEEDS_ADR |
| 2 | Document Library Schema (10 libraries) | Library definitions with column schemas | CSV, JSON, or MD listing 10 library names, descriptions, and schema | `docs/document-center/PHASE3_ONEDRIVE_STORAGE_GUIDE.md` (6 OneDrive folders) | EXTEND_EXISTING |
| 3 | Site Column Definitions (21 columns) | Column definitions: name, type, required, default, choices | Schema document containing column definitions | NONE | BUILD_NEW |
| 4 | Content Type Definitions (11 types) | Document content types with associated columns | Content type definitions — PnP schema or manual spec | NONE | BUILD_NEW |
| 5 | View Definitions (8 views) | List/library views for different user roles | View schema or description documents | `docs/document-center/UI_BLUEPRINT.md` (frontend views only) | EXTEND_EXISTING |
| 6 | SharePoint Permission Groups (6 groups) | Permission level definitions for SharePoint groups | Permission matrix or group definition document | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` | EXTEND_EXISTING |

### EA-3B — PnP Provisioning

| # | Implementation Item | Expected Role | Evidence Required | Canonical Comparison Target | Implementation Classification |
|---|---------------------|--------------|-------------------|----------------------------|------------------------------|
| 1 | PnP PowerShell Preflight Scripts | Automated provisioning scripts for SharePoint Online | `.ps1` files containing `Connect-PnPOnline`, `New-PnPList`, `Add-PnPContentType` commands | NONE | NEEDS_ADR |
| 2 | PnP provisioning template (if applicable) | XML/JSON template for site provisioning | `.xml` PnP provisioning template files | NONE | NEEDS_ADR |

### EA-3C.1 — M365 Tenant Assessment

| # | Implementation Item | Expected Role | Evidence Required | Canonical Comparison Target | Implementation Classification |
|---|---------------------|--------------|-------------------|----------------------------|------------------------------|
| 1 | M365 Admin Questions Document | Completed admin questionnaire for tenant readiness | `.md` or `.docx` with M365 admin questions and answers | `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-1 checklist) | EXTEND_EXISTING |
| 2 | Tenant Capability Checklist | Detailed checklist of available M365 services | `.md`, `.csv`, or `.xlsx` checklist with status per service | `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-1) | EXTEND_EXISTING |
| 3 | Permission Requirements Document | Detailed M365-wide permission requirements | `.md` document describing roles, permission scopes, and AD group mappings | `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` | EXTEND_EXISTING |
| 4 | Integration Decision Matrix | Compare/contrast integration approaches | `.md` or `.csv` evaluating integration options (Graph API vs export JSON vs other) | `docs/document-center/M365 FoundationBlueprint.MD` (Phase M365-8 mentions Registry Export JSON preference) | BUILD_NEW |

### EA-3D — Taxonomy v2

| # | Implementation Item | Expected Role | Evidence Required | Canonical Comparison Target | Implementation Classification |
|---|---------------------|--------------|-------------------|----------------------------|------------------------------|
| 1 | Taxonomy v2 JSON/MD | Expanded taxonomy with 10 domains, 30 categories, 62 subcategories, 11 document types | `.json` or `.md` file with hierarchical taxonomy showing domain → category → subcategory tree | `docs/document-center/taxonomy.json` (6 flat categories) | NEEDS_ADR |
| 2 | Domain definitions (10) | Top-level domain metadata | Embedded in taxonomy v2 file or separate domain definitions | NONE | BUILD_NEW |
| 3 | Document type taxonomy (11 types) | Document type classification system | Document type definitions with metadata mappings | NONE | BUILD_NEW |

### EA-3E — Extended Metadata Registry

| # | Implementation Item | Expected Role | Evidence Required | Canonical Comparison Target | Implementation Classification |
|---|---------------------|--------------|-------------------|----------------------------|------------------------------|
| 1 | Extended Registry Data Model (26 fields) | Full metadata schema with 26 fields | `.md`, `.json`, or `.csv` listing all fields, types, required status, validation rules | `docs/document-center/REGISTRY_DATA_MODEL.md` (13 fields) | NEEDS_ADR |
| 2 | Expanded Status Model | More granular document status values | Status model definition with transitions and rules | `docs/document-center/REGISTRY_DATA_MODEL.md` (4 statuses) | EXTEND_EXISTING |
| 3 | Visibility Governance Rules | Detailed rules for document visibility | Governance document defining who can see what, exception process | `docs/document-center/REGISTRY_DATA_MODEL.md` (3 visibility values) + `docs/document-center/ONEDRIVE_PERMISSION_POLICY.md` | EXTEND_EXISTING |
| 4 | Public Export Policy | Rules and process for public document export | Policy document defining export criteria, format, review cycle | NONE | BUILD_NEW |
| 5 | AI Source Eligibility Policy | Which documents qualify as AI training source | Policy document with eligibility criteria, opt-out process | NONE | BUILD_NEW |

### Memory OS

| # | Forward Implementation Item | Expected Role | Evidence Required | Canonical Comparison Target | Implementation Classification |
|---|----------------------------|--------------|-------------------|----------------------------|------------------------------|
| 1 | Memory OS Configuration | AI agent context/project memory for coding agents | `.cursor/rules/`, `SKILL.md`, `AGENTS.md`, `CORE.md` files | NONE | NEEDS_ADR |
| 2 | Agent workflow definitions | Automated agent workflows for the project | Workflow definition files | NONE | BUILD_NEW |

---

## Implementation Classification Guide

| Classification | Action |
|----------------|--------|
| **BUILD_NEW** | The artifact does not exist anywhere. Must be newly authored. |
| **EXTEND_EXISTING** | A partial equivalent exists in GitHub. Extend the existing artifact. |
| **NEEDS_ADR** | The artifact has architectural implications that need an Architecture Decision Record before building. |

---

## Items Requiring Forward Implementation

| Implementation Classification | Count | Items |
|------------------------------|-------|-------|
| BUILD_NEW | 8 | Site columns, Content types, Integration decision matrix, Domain definitions, Document type taxonomy, Public export policy, AI source eligibility policy, Agent workflow definitions |
| EXTEND_EXISTING | 8 | Library schema, View definitions, Permission groups, Admin questions, Capability checklist, Permission requirements, Status model, Visibility governance rules |
| NEEDS_ADR | 6 | Site design, PnP scripts, PnP templates, Taxonomy v2, Extended registry data model, Memory OS configuration |
| **Total** | **22** | |
