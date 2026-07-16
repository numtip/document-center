# ADR-001: Microsoft 365 as Source of Truth

**Status**: Accepted  
**Date**: 2026-07-14 (retroactive)  
**Phase**: EA-3

---

## Context

RAE documents were scattered across WTMS (legacy web CMS), local file shares, and authoring spreadsheets. Multiple copies existed with no single authoritative store. Git repositories cannot hold 627+ binary documents with appropriate access control for a university research office.

## Decision

Microsoft 365 SharePoint document libraries on the existing RAE Team site (`maejo365.sharepoint.com/sites/msteams_54adc4`) are the **authoritative file store**. Git holds metadata schemas, standards, and tooling only — never production document binaries.

## Consequences

**Positive**:

- Enterprise access control via M365 identity
- Version history and audit trail in SharePoint
- No document binary bloat in Git
- Aligns with university IT M365 investment

**Negative**:

- Requires authenticated access (no anonymous by default)
- Automation depends on browser/REST session management
- Offline access limited to SharePoint sync clients

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Git LFS for all documents | No enterprise ACL; poor fit for 627 mixed-format files |
| OneDrive personal folders | No organizational governance; single-user ownership |
| WTMS retention | Legacy system being decommissioned; no M365 integration |
| Azure Blob Storage | Additional infrastructure; no native university SSO |
