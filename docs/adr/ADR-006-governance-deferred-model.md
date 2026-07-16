# ADR-006: Governance Deferred Model

**Status**: Accepted  
**Date**: 2026-07-15 (retroactive)  
**Phase**: EA-6C

---

## Context

EA-6C planned governance activation: category owners, RAE-DC security groups, ALLOW/DENY testing, Power Automate workflows, and owner assignment. Activating governance during migration would have blocked uploads, introduced permission errors, and slowed the 627-document corpus migration.

## Decision

**Defer all governance activation** until corpus migration is complete and production is frozen. Migration proceeds with placeholder values:

| Field | Deferred value |
|-------|----------------|
| Owner | `TBD` |
| PublicVisibility | `PendingReview` |
| Registry Visibility | `internal` |
| Security groups | Not created |
| Workflows | Not activated |

Governance activation becomes a future phase requiring change control (EA-6C backlog).

## Consequences

**Positive**:

- Migration completed without permission blockers
- 627/627/627 achieved on schedule
- Governance can be designed against complete corpus
- No partial ALLOW/DENY states during upload

**Negative**:

- Owner fields show placeholder
- No automated approval workflows
- Public access policy undecided
- Manual review required for visibility changes

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Activate governance before migration | Would block uploads; untested group model |
| Partial governance (pilot library only) | Inconsistent policy across corpus |
| Skip governance entirely | Non-compliant with university document policy long-term |
| Git-based approval workflow | Not integrated with SharePoint ACL model |
