# RAE Enterprise Platform Roadmap

**Version**: 1.0.2  
**Effective**: 2026-07-16  
**Status**: Enterprise Governance Freeze

---

## Overview

This roadmap defines the RAE digital platform portfolio. Document Center v1.0 is complete and frozen. All future platforms consume governed data from Microsoft 365 and reference this canonical repository — they do not redefine architecture.

---

## Completed

### ✓ Document Center (v1.0 — FROZEN)

| Property | Value |
|----------|-------|
| Status | **COMPLETE — Production frozen** |
| Files | 627 SharePoint documents |
| Registry | 627 rows |
| Production portal | SharePoint Document Center |
| Preview | GitHub Pages (3 demo records) |
| Release tag | `document-center-v1.0.0` |
| Canonical tag | `document-center-v1.0.2` |

**Deliverables**: Migration complete, Registry sync, operational runbook, acceptance certificate. See [docs/release/](../release/).

---

## Future Platforms

### Research Portal

| Property | Value |
|----------|-------|
| Priority | P1 |
| Purpose | Research division document discovery and reporting |
| Depends on | Document Center (Research library), Registry export, taxonomy |
| Blocked by | Registry export pipeline (production hardening) |
| Version target | 2.x platform expansion |

### Learning Center

| Property | Value |
|----------|-------|
| Priority | P2 |
| Purpose | Training materials and academic service documents |
| Depends on | Document Center (AcademicServices, SOPManuals libraries) |
| Blocked by | Governance activation (owner assignment) |
| Version target | 2.x platform expansion |

### Green Office

| Property | Value |
|----------|-------|
| Priority | P2 |
| Purpose | Sustainability documentation and compliance records |
| Depends on | Document Center taxonomy, metadata standards |
| Blocked by | Taxonomy extension ADR, category owner assignment |
| Version target | 2.x platform expansion |

### Public Experience Portal (Next.js)

| Property | Value |
|----------|-------|
| Priority | P1 |
| Purpose | Public-facing Document Center for `visibility=public` records |
| Depends on | Registry export JSON, export contract, Document Center corpus |
| Blocked by | Scheduled Registry export (EA-7 contract not yet implemented) |
| Version target | 3.x unified public experience |
| Repository | `rae-nextjs-main` (external) |

### AI Knowledge Platform

| Property | Value |
|----------|-------|
| Priority | P3 |
| Purpose | RAG / knowledge retrieval over RAE document corpus |
| Depends on | Registry export, DocumentID index, visibility model |
| Blocked by | Public access policy, export pipeline, embedding governance |
| Version target | 4.x AI-native platform |

---

## Future Integration Layer

```text
┌─────────────────────────────────────────────────────────────┐
│  EXPERIENCE LAYER (future)                                  │
│  Research Portal │ Learning Center │ Green Office │ Next.js │
├─────────────────────────────────────────────────────────────┤
│  EXPORT LAYER (to build)                                    │
│  Scheduled Registry Export → public-registry.json           │
├─────────────────────────────────────────────────────────────┤
│  DISCOVERY LAYER (complete — frozen)                        │
│  RAE Document Registry (627 rows)                           │
├─────────────────────────────────────────────────────────────┤
│  STORAGE LAYER (complete — frozen)                          │
│  6 SharePoint Document Libraries (627 files)                │
├─────────────────────────────────────────────────────────────┤
│  GOVERNANCE LAYER (deferred — EA-6C)                        │
│  Owners │ Groups │ Workflows │ Public access policy         │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependency Summary

| Platform | Requires Document Center | Requires Export Layer | Requires Governance |
|----------|:------------------------:|:---------------------:|:-------------------:|
| Research Portal | ✓ | ✓ | — |
| Learning Center | ✓ | — | ✓ |
| Green Office | ✓ | — | ✓ |
| Public Experience Portal | ✓ | ✓ | ✓ |
| AI Knowledge Platform | ✓ | ✓ | ✓ |

---

## Version Alignment

| Repository version | Platform phase |
|--------------------|----------------|
| 1.0.x | Document Center maintenance; governance docs |
| 2.x | Platform expansion (Research, Learning, Green Office) |
| 3.x | Unified public experience (Next.js) |
| 4.x | AI-native platform |

See [ARCHITECTURE_LIFECYCLE.md](ARCHITECTURE_LIFECYCLE.md).

---

## Related Documents

- [ENTERPRISE_DEPENDENCY_GRAPH.md](ENTERPRISE_DEPENDENCY_GRAPH.md)
- [CONSUMER_IMPLEMENTATION_GUIDE.md](CONSUMER_IMPLEMENTATION_GUIDE.md)
- [docs/canonical/DEPENDENT_PROJECTS.md](../canonical/DEPENDENT_PROJECTS.md)
- [docs/m365/ea-11-production-hardening-backlog.md](../m365/ea-11-production-hardening-backlog.md)
