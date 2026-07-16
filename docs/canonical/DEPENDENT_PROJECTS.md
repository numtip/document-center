# Dependent Projects

**Version**: 1.0.1  
**Effective**: 2026-07-16

Future RAE digital platforms that consume standards and patterns from this canonical repository.

---

## Relationship Model

```text
RAE Enterprise Canonical Repository (this repo)
        │
        ├── READ: architecture, standards, ADRs, export contract
        │
        └── WRITE: none (this repo does not receive runtime data)
        
Dependent projects implement presentation and domain logic;
SharePoint + Registry remain authoritative for documents.
```

---

## RAE Next.js (`rae-nextjs-main`)

| Property | Value |
|----------|-------|
| **Purpose** | Public-facing Document Center portal |
| **Consumes** | Registry export JSON (`public-registry.json`), taxonomy, reference standards |
| **Writes** | Nothing to SharePoint or Registry (read-only consumer) |
| **Authority** | This repo for schema; SharePoint for document truth |

**Integration requirements**:

- Pin to a release tag of export contract
- Filter: `visibility=public` + `status=current`
- Never embed production SharePoint credentials in frontend

---

## Research Portal

| Property | Value |
|----------|-------|
| **Purpose** | Research division document discovery and reporting |
| **Consumes** | Research library metadata, taxonomy `research` category, Registry export subset |
| **Writes** | New research documents via SharePoint (not via this repo) |
| **Authority** | SharePoint Research library; Registry sync for metadata |

**Must reference**: ADR-004 (library strategy), REFERENCE_STANDARDS (DocumentID, naming)

---

## Green Office

| Property | Value |
|----------|-------|
| **Purpose** | Sustainability documentation and compliance records |
| **Consumes** | Taxonomy extensions (future), metadata standards, governance model |
| **Writes** | Documents to appropriate SharePoint library |
| **Authority** | SharePoint for files; ADR required for new library or category |

**Must reference**: CHANGE_CONTROL_POLICY before adding categories or libraries

---

## Learning Center

| Property | Value |
|----------|-------|
| **Purpose** | Training materials and academic service documents |
| **Consumes** | AcademicServices library metadata, SOPManuals category |
| **Writes** | Training docs via SharePoint upload workflow |
| **Authority** | SharePoint AcademicServices / SOPManuals libraries |

**Must reference**: REFERENCE_STANDARDS (status, visibility), OPERATION_RUNBOOK (Registry sync)

---

## AI Knowledge Platform

| Property | Value |
|----------|-------|
| **Purpose** | RAG / knowledge retrieval over RAE document corpus |
| **Consumes** | Registry export JSON, Storage URLs (authenticated), taxonomy, DocumentID index |
| **Writes** | Nothing to SharePoint; may cache embeddings externally |
| **Authority** | SharePoint for source files; this repo for metadata schema |

**Constraints**:

- Respect visibility model (`internal` vs `public`)
- Do not expose AUTH_REQUIRED URLs anonymously
- DocumentID is the canonical join key

---

## Future AI Assistants

| Property | Value |
|----------|-------|
| **Purpose** | Conversational access to RAE documents and policies |
| **Consumes** | Registry metadata, taxonomy, ADRs (for grounding), export JSON |
| **Writes** | None to production systems without governance approval |
| **Authority** | This repo for standards; SharePoint for document access |

**Must reference**: ADR-006 (governance deferred), ADR-009 (public separation)

---

## Integration Checklist for New Dependent Projects

1. Read [CANONICAL_REPOSITORY_CHARTER.md](CANONICAL_REPOSITORY_CHARTER.md)
2. Review [REFERENCE_STANDARDS.md](REFERENCE_STANDARDS.md)
3. Pin to a release tag (`document-center-v1.0.x`)
4. Submit ADR for any architectural deviation
5. Do not duplicate metadata schemas — import or link
6. Do not store document binaries in dependent repos

---

## Related Documents

- [PROJECT_INDEX.md](PROJECT_INDEX.md)
- [docs/m365/registry-export-contract.md](../m365/registry-export-contract.md)
- [docs/adr/ADR-009-public-experience-separation.md](../adr/ADR-009-public-experience-separation.md)
