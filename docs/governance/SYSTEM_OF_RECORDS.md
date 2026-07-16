# System of Records

**Version**: 1.0.2  
**Effective**: 2026-07-16

**Policy**: No duplicate sources of truth. Each data domain has exactly one authoritative system.

---

## Record Ownership

| Domain | System of Record | Location | Notes |
|--------|------------------|----------|-------|
| **Documents** | Microsoft 365 SharePoint | 6 document libraries, 627 files | ADR-001; files never in Git |
| **Metadata** | RAE Document Registry | SharePoint List, 627 rows | ADR-003; discovery layer |
| **Portal (production)** | SharePoint Document Center | Site page + Registry web part | Operational portal |
| **Portal (public — future)** | Next.js | `rae-nextjs-main` (external) | Consumes export JSON only |
| **Governance** | Microsoft 365 | Groups, permissions, workflows | Deferred EA-6C |
| **Source Code** | GitHub | `numtip/document-center` | Standards, ADRs, tooling |
| **Analytics** | Future Platform | Not yet designated | v4.x AI-native phase |

---

## Prohibited Duplicates

| Domain | Do NOT create |
|--------|---------------|
| Documents | Git LFS store, Azure Blob mirror, local file share master |
| Metadata | Git-hosted live registry, parallel SharePoint List, custom SQL |
| DocumentID index | Project-local ID scheme, second registry |
| Public records | GitHub Pages production corpus, unfiltered export |
| Governance | Shadow permission model outside M365 |

---

## Data Flow (Single Path)

```text
Documents:     WTMS (archived) → SharePoint libraries ONLY
Metadata:      SharePoint libraries → Registry ONLY (AUTO_UPSERT)
Export:        Registry → public-registry.json ONLY (when built)
Public UI:     Export JSON → Next.js ONLY
Standards:     Canonical Repository (GitHub) ONLY
Analytics:     Future platform ONLY (TBD)
```

---

## Join Keys

| Relationship | Key |
|--------------|-----|
| File ↔ Registry row | DocumentID (`RAE-NNNNN`) |
| Registry ↔ Export | DocumentID |
| Export ↔ Portal | DocumentID |
| Export ↔ AI ingestion | DocumentID |
| Standards ↔ All projects | Release tag |

---

## Read Copies (Not Systems of Record)

| Copy | Source | Purpose |
|------|--------|---------|
| `docs/document-center/document-registry.draft.json` | Authoring schema | Validation only |
| `preview/data/public-registry.sample.json` | Mock data | UI demo (3 records) |
| `.migration/rae-wtms/ea-*/` CSV/JSON | Migration evidence | Audit trail |
| GitHub Pages `dist/` | Preview build | Demo deployment |

These are **never** authoritative for production decisions.

---

## Enforcement

Violations require:

1. Immediate stop of duplicate source creation
2. ADR explaining why duplicate was attempted
3. Remediation plan to converge to single system of record
4. Architecture review before resuming

See [REPOSITORY_OPERATION_POLICY.md](REPOSITORY_OPERATION_POLICY.md).

---

## Related Documents

- [ENTERPRISE_DEPENDENCY_GRAPH.md](ENTERPRISE_DEPENDENCY_GRAPH.md)
- [docs/adr/ADR-001-m365-source-of-truth.md](../adr/ADR-001-m365-source-of-truth.md)
- [docs/adr/ADR-003-registry-pattern.md](../adr/ADR-003-registry-pattern.md)
