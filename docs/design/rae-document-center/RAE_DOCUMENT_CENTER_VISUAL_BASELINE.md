# RAE Document Center Visual Baseline V2

**Artifact name:** RAE Document Center Visual Baseline V2  
**Status:** FROZEN  
**Date:** 2026-07-15  
**Source:** Google Stitch design tool  
**Scope:** RAE Document Center only  

---

## 1. Purpose

Register the approved Stitch V2 visual design as the frozen visual baseline for RAE Document Center SharePoint Modern Page implementation. This baseline governs all visual rendering of the Document Center landing page within the existing RAE SharePoint site (`/sites/msteams_54adc4`).

---

## 2. Architecture Context

| Dimension | Reference |
|-----------|-----------|
| EA-3R decision | `REUSE_EXISTING_SITE_WITH_CONDITIONS` → resolved by EA-3S |
| Site reuse closure | `docs/m365/m365-existing-site-reuse-readiness-closure.md` |
| Implementation exception | `docs/m365/m365-existing-site-implementation-exception.md` |
| SharePoint foundation | `docs/m365/sharepoint-site-design.md` |
| EA Forward Implementation Baseline | `docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md` |
| Six canonical libraries | `Administration`, `FinanceProcurement`, `PlanningPolicy`, `AcademicServices`, `Research`, `SOPManuals` |
| Implementation target | SharePoint Modern Page on existing RAE site |

---

## 3. Frozen Source Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Stitch V2 ZIP | `docs/design/rae-document-center/stitch-v2/RAE_DOCUMENT_CENTER_STITCH_V2.zip` | Preserved, unmodified |
| Design specification | `docs/design/rae-document-center/stitch-v2/DESIGN.md` | Extracted, unmodified |
| Visual screenshot | `docs/design/rae-document-center/stitch-v2/screen.png` | Extracted, unmodified |
| HTML/CSS reference | `docs/design/rae-document-center/stitch-v2/code.html` | Extracted, reference only |

---

## 4. Governance Rules

### 4.1 Stitch Code is Reference Only
The `code.html` file is a design prototype. It is **not** production source code and must not be copied, deployed, or treated as an implementation asset.

### 4.2 No Visual Redesign Without Explicit Approval
The frozen design may not be visually redesigned, re-themeed, or restructured without formal approval. Minor fidelity adjustments within SharePoint web part constraints are permitted during implementation.

### 4.3 Shared RAE Ecosystem Design Language
The RAE green identity, Sarabun typography, and visual language are shared across the RAE ecosystem. This does **not** imply that portal content from Green Office, Learning Center, or other RAE units may be mixed into the Document Center page.

### 4.4 Content Scope
RAE Document Center content is limited to RAE institutional documents only:

- Administration
- FinanceProcurement
- PlanningPolicy
- AcademicServices
- Research
- SOPManuals

### 4.5 Explicit Exclusions
The following are excluded unless separately approved:

- Green Office content
- Learning Center content
- Any portal content outside the RAE Document Center scope

---

## 5. Approved Design Characteristics

| Characteristic | Detail |
|----------------|--------|
| **Institutional identity** | RAE green (`#005C3B`), warm ivory surface, gold accent (`#D8A01A`) |
| **Typography** | Sarabun exclusively (all weights 300–700) |
| **Search-first hero** | Prominent search bar in green hero section with quick-link chips |
| **Six canonical domains** | Card grid for Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals |
| **Quick access bar** | Horizontal links: Search All, Latest Updates, Documents to Review, RAE Document Registry |
| **Recent document list** | Tabular listing with DocumentID, title, category, date, status |
| **Governance/trust section** | Three trust indicators: assigned owner, version history, standardized classification |
| **Compact support area** | Footer with help text, support buttons, RAE copyright |
| **Layout model** | Fixed-fluid hybrid; max-width 1280px container; 4px baseline spacing |
| **Shape language** | Soft rounded corners (4px–16px); tonal layers over shadows |
| **SharePoint compatibility** | Designed for SharePoint Modern Page web part implementation |

---

## 6. Related Documents

| Document | Path |
|----------|------|
| SharePoint Web Part Mapping | `docs/m365/rae-document-center-webpart-mapping.md` |
| SharePoint Site Design | `docs/m365/sharepoint-site-design.md` |
| UI Blueprint (Next.js) | `docs/document-center/UI_BLUEPRINT.md` |
| EA Forward Implementation Baseline | `docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md` |
| Session Handoff | `docs/m365/SESSION-HANDOFF.md` |
