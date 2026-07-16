# ADR-005: Metadata First Architecture

**Status**: Accepted  
**Date**: 2026-07-14 (retroactive)  
**Phase**: EA-4

---

## Context

Documents need discoverability beyond filename. WTMS had inconsistent metadata. SharePoint supports custom columns but only if populated at upload time. Without metadata, search and Registry export are useless.

## Decision

Apply **metadata at upload time** via SharePoint ValidateUpdateListItem before Registry sync. Required fields:

| Field | Value (migrated corpus) |
|-------|------------------------|
| DocumentID | From manifest (immutable) |
| Title | From manifest |
| Category1 | Taxonomy subcategory |
| Owner | `TBD` (placeholder) |
| DocumentStatus | `LegacyImported` |
| PublicVisibility | `PendingReview` |
| LegacySourceURL | WTMS source URL |

Metadata standards are normative in `docs/canonical/REFERENCE_STANDARDS.md`.

## Consequences

**Positive**:

- Structured search in SharePoint and Registry
- Export pipeline has required fields
- Audit trail from WTMS source URL
- Consistent field values across 627 documents

**Negative**:

- Upload pipeline must include metadata step (slower)
- Owner fields remain placeholder until governance
- Metadata drift if manual SharePoint edits bypass sync

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Filename-only identification | No category, status, or export fields |
| Post-upload manual metadata | Not scalable to 627 documents |
| Metadata in Registry only | Library items lack SharePoint-native search fields |
| AI-generated metadata | Unreliable for compliance documents; no training corpus |
