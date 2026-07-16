# ADR-002: Website is Presentation Layer

**Status**: Accepted  
**Date**: 2026-07-14 (retroactive)  
**Phase**: EA-7B

---

## Context

Early designs conflated the Document Center website with document storage. Some artifacts referenced `document-registry.json` in Git as if it were the live registry. Users need a browsable portal but master files must remain in SharePoint.

## Decision

Websites and portals (SharePoint page, GitHub Pages preview, future Next.js) are **presentation layers only**. They display metadata and link to SharePoint Storage URLs. They do not store, upload, or authoritatively version document files.

```text
SharePoint libraries (files) → Registry (metadata) → Portal (presentation)
```

## Consequences

**Positive**:

- Clear separation of concerns
- Portal can be redesigned without moving files
- Multiple portals can consume same Registry export
- Preview environments cannot corrupt production data

**Negative**:

- Every portal needs Registry sync or export pipeline
- Broken Storage URLs surface as portal defects (not file loss)
- Two systems to maintain (SharePoint + portal)

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Git-hosted registry as live source | Stale immediately; no SharePoint URL binding |
| Portal uploads directly to Git | Violates access control; no M365 audit |
| Embedded files in static site | Cannot scale to 627 documents; no ACL |
