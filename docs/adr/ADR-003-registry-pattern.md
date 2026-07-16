# ADR-003: Registry Pattern

**Status**: Accepted  
**Date**: 2026-07-14 (retroactive)  
**Phase**: EA-4 / EA-8

---

## Context

Six SharePoint libraries organize files by category, but users need cross-library search, filtering, and a single metadata view. SharePoint library views alone do not provide a unified discovery experience or a clean export surface for external portals.

## Decision

Implement a **RAE Document Registry** as a SharePoint List that acts as the metadata discovery layer. Each document is registered by DocumentID with Storage URL, category, status, and visibility. Registry sync uses AUTO_UPSERT (idempotent upsert by DocumentID).

| Property | Value |
|----------|-------|
| Idempotency key | DocumentID |
| Sync mode | AUTO_UPSERT |
| Tool | `_ea8_registry_sync.py` |

## Consequences

**Positive**:

- Single query surface for 627 documents across 6 libraries
- Idempotent sync safe for batch re-runs
- Clean export contract for Next.js (`registry-export-contract.md`)
- Document Center page binds to Registry List web part

**Negative**:

- Registry can drift from libraries if sync not run after uploads
- Additional List to maintain
- Two places to update if metadata changes (library item + Registry row)

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Search-only (no Registry) | No structured export; poor cross-library filter |
| JSON file in Git as registry | Not live; no SharePoint URL binding |
| SQL database | Additional infrastructure outside M365 |
| One mega-library | Loses category organization; poor UX |
