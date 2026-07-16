# Consumer Implementation Guide

**Version**: 1.0.2  
**Effective**: 2026-07-16  
**Audience**: Teams building future RAE digital platforms

Every consumer project must reference this guide before implementation. **Consume governed data; never redefine architecture.**

---

## Common Requirements (All Projects)

| Requirement | Reference |
|-------------|-----------|
| Pin to release tag | `document-center-v1.0.2` or later |
| Read charter | [CANONICAL_REPOSITORY_CHARTER.md](../canonical/CANONICAL_REPOSITORY_CHARTER.md) |
| Follow standards | [REFERENCE_STANDARDS.md](../canonical/REFERENCE_STANDARDS.md) |
| Declare dependencies | [PROJECT_BOOTSTRAP_TEMPLATE.md](PROJECT_BOOTSTRAP_TEMPLATE.md) |
| Submit ADR for deviations | [CHANGE_CONTROL_POLICY.md](../canonical/CHANGE_CONTROL_POLICY.md) |

---

## Research Portal

| Property | Value |
|----------|-------|
| **Purpose** | Research division document discovery and reporting |
| **Consumes** | Research library metadata, Registry export subset, taxonomy `research` category, DocumentID index |
| **Never modifies** | SharePoint files, Registry rows, DocumentID format, library structure |
| **Reference documents** | ADR-004, REFERENCE_STANDARDS §7, export contract |
| **Required ADR** | None if conforming; ADR required for new library or category |
| **Required standards** | DocumentID (`RAE-NNNNN`), naming, visibility model |

**Integration pattern**: Read-only Registry export filtered to `category=research`. Link to SharePoint Storage URLs (authenticated).

---

## Learning Center

| Property | Value |
|----------|-------|
| **Purpose** | Training materials and academic service document access |
| **Consumes** | AcademicServices + SOPManuals library metadata, taxonomy, Registry export |
| **Never modifies** | SharePoint libraries, Registry schema, governance groups |
| **Reference documents** | ADR-004, OPERATION_RUNBOOK, REFERENCE_STANDARDS §4–5 |
| **Required ADR** | ADR required if adding training-specific taxonomy extensions |
| **Required standards** | Status values, visibility (`internal` default), library mapping |

**Integration pattern**: Authenticated SharePoint access or Registry export subset. Sync via approved `_ea8_registry_sync.py` only.

---

## Green Office

| Property | Value |
|----------|-------|
| **Purpose** | Sustainability documentation and compliance records |
| **Consumes** | Taxonomy, metadata standards, governance model (when activated) |
| **Never modifies** | Existing six libraries without ADR; Registry idempotency key |
| **Reference documents** | CHANGE_CONTROL_POLICY, ADR-006, ARCHITECTURE_LIFECYCLE §2.x |
| **Required ADR** | **Required** — new category or library for Green Office documents |
| **Required standards** | Full REFERENCE_STANDARDS; baseline comparison mandatory |

**Integration pattern**: New documents uploaded to approved library via SharePoint workflow; Registry sync follows AUTO_UPSERT.

---

## Next.js (Public Experience Portal)

| Property | Value |
|----------|-------|
| **Purpose** | Public-facing Document Center for approved public records |
| **Consumes** | `public-registry.json` export, taxonomy, preview UI blueprint |
| **Never modifies** | SharePoint, Registry, canonical schemas; no production credentials in frontend |
| **Reference documents** | ADR-002, ADR-009, registry-export-contract.md, REFERENCE_STANDARDS §10 |
| **Required ADR** | None if conforming to export contract; ADR for schema extensions |
| **Required standards** | Export filter: `visibility=public` + `status=current`; DocumentID join key |

**Repository**: `rae-nextjs-main` (external consumer)

**Integration pattern**:

```text
Registry → Export Layer → public-registry.json → Next.js (read-only)
```

Never connect Next.js directly to SharePoint REST in public deployment.

---

## AI Knowledge Platform

| Property | Value |
|----------|-------|
| **Purpose** | RAG / knowledge retrieval over RAE document corpus |
| **Consumes** | Registry export JSON, DocumentID index, taxonomy, Storage URLs (authenticated) |
| **Never modifies** | SharePoint, Registry, visibility assignments; no anonymous URL exposure |
| **Reference documents** | ADR-001, ADR-009, SYSTEM_OF_RECORDS, ARCHITECTURE_PRINCIPLES |
| **Required ADR** | **Required** — AI ingestion scope, embedding store, retention policy |
| **Required standards** | Visibility model enforced; `internal` docs excluded from public RAG |

**Integration pattern**: Ingest from governed export only. DocumentID is canonical join key. Respect AUTH_REQUIRED tenant policy.

---

## Anti-Patterns (All Projects)

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Duplicate document store | Violates ADR-001 |
| Custom DocumentID format | Breaks Registry idempotency |
| Git-hosted live registry | Violates ADR-003 |
| GitHub Pages as production | Violates ADR-009 |
| Direct WTMS recrawl | Production frozen (ADR-008) |
| Ungoverned AI ingestion | Violates ARCHITECTURE_PRINCIPLES |

---

## Onboarding Checklist

- [ ] Read [CONSUMER_IMPLEMENTATION_GUIDE.md](CONSUMER_IMPLEMENTATION_GUIDE.md) (this document)
- [ ] Complete [PROJECT_BOOTSTRAP_TEMPLATE.md](PROJECT_BOOTSTRAP_TEMPLATE.md)
- [ ] Pin canonical repo tag
- [ ] Declare dependencies in project README
- [ ] Submit ADR if deviating from standards
- [ ] Verify no duplicate system of record

---

## Related Documents

- [DEPENDENT_PROJECTS.md](../canonical/DEPENDENT_PROJECTS.md)
- [ENTERPRISE_DEPENDENCY_GRAPH.md](ENTERPRISE_DEPENDENCY_GRAPH.md)
- [PROJECT_BOOTSTRAP_TEMPLATE.md](PROJECT_BOOTSTRAP_TEMPLATE.md)
