# Architecture Principles

**Version**: 1.0.2  
**Effective**: 2026-07-16  
**Status**: NORMATIVE — all RAE digital systems must adhere

---

## Principles

### 1. Build Less. Govern More.

Prefer extending the governed M365 and Registry foundation over building parallel systems. Every new platform should consume existing data — not recreate it. Governance documentation and ADRs precede implementation.

**Implication**: No new document store without ADR. No custom registry. No shadow metadata.

---

### 2. Metadata First.

Documents are discoverable only when metadata is applied at upload time and synchronized to the Registry. Filename alone is insufficient. All platforms filter, search, and export via structured metadata fields.

**Implication**: Follow [REFERENCE_STANDARDS.md](../canonical/REFERENCE_STANDARDS.md). Registry sync after every upload batch.

**ADR**: [ADR-005](../adr/ADR-005-metadata-first-architecture.md)

---

### 3. Microsoft 365 is Source of Truth.

SharePoint document libraries are the authoritative file store. Git holds standards and tooling — never production document binaries. All Storage URLs point to SharePoint.

**Implication**: No Git LFS for documents. No duplicate file stores. Authenticated access via tenant identity.

**ADR**: [ADR-001](../adr/ADR-001-m365-source-of-truth.md)

---

### 4. Website is Presentation Layer.

Portals, websites, and apps display metadata and link to SharePoint. They do not store, upload, or authoritatively version master files. Multiple presentation layers may consume the same Registry export.

**Implication**: Next.js, Research Portal, and GitHub Pages preview are all presentation — not storage.

**ADR**: [ADR-002](../adr/ADR-002-website-presentation-layer.md)

---

### 5. Static-first Public Experience.

Public portals should consume a scheduled, validated Registry export JSON — not live SharePoint REST in browser-facing deployments. Preview builds must reject production URLs. Public records filtered by visibility and status.

**Implication**: Build export pipeline before Next.js production. GitHub Pages remains 3-record demo.

**ADR**: [ADR-009](../adr/ADR-009-public-experience-separation.md)

---

### 6. AI Consumes Governed Data Only.

AI systems (RAG, assistants, analytics) ingest from Registry export or authenticated governed APIs — never uncontrolled SharePoint scraping, never bypassing visibility model. DocumentID is the canonical join key.

**Implication**: AI governance ADR required before ingestion. `internal` documents excluded from public RAG.

---

### 7. Architecture Before Implementation.

No platform development begins without referencing the canonical repository, reading applicable ADRs, and completing the project bootstrap template. Deviations require ADR before code.

**Implication**: [PROJECT_BOOTSTRAP_TEMPLATE.md](PROJECT_BOOTSTRAP_TEMPLATE.md) is mandatory for new projects.

---

## Principle Hierarchy

When principles conflict, resolve in this order:

1. Microsoft 365 is Source of Truth
2. Metadata First
3. Website is Presentation Layer
4. Build Less. Govern More
5. Static-first Public Experience
6. AI Consumes Governed Data Only
7. Architecture Before Implementation

---

## Mapping to ADRs

| Principle | Primary ADR |
|-----------|-------------|
| M365 Source of Truth | ADR-001 |
| Presentation Layer | ADR-002 |
| Metadata First | ADR-005 |
| Registry Pattern | ADR-003 |
| Library Strategy | ADR-004 |
| Governance Deferred | ADR-006 |
| Production Freeze | ADR-008 |
| Public Separation | ADR-009 |

---

## Related Documents

- [CONSUMER_IMPLEMENTATION_GUIDE.md](CONSUMER_IMPLEMENTATION_GUIDE.md)
- [SYSTEM_OF_RECORDS.md](SYSTEM_OF_RECORDS.md)
- [docs/canonical/CANONICAL_REPOSITORY_CHARTER.md](../canonical/CANONICAL_REPOSITORY_CHARTER.md)
