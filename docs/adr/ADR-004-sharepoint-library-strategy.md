# ADR-004: SharePoint Library Strategy

**Status**: Accepted  
**Date**: 2026-07-14 (retroactive)  
**Phase**: EA-3

---

## Context

627 documents span administration, finance, policy, academic services, research, and SOPs. A single library would be unmanageable. WTMS used category-based organization that needed mapping to SharePoint structure.

## Decision

Use **six document libraries** mapped to taxonomy categories:

| Library | Category slug |
|---------|---------------|
| Administration | `admin` |
| FinanceProcurement | `finance-procurement` |
| PlanningPolicy | `policy-planning` |
| AcademicServices | `academic-service` |
| Research | `research` |
| SOPManuals | `manuals` |

Files named `{DocumentID}{extension}`. No additional libraries without architecture review.

## Consequences

**Positive**:

- Mirrors organizational structure
- Library-level permissions possible (future governance)
- Manageable library sizes (largest: Research ~530 items)
- Clear manifest-to-library mapping

**Negative**:

- Cross-library queries require Registry
- Research library requires REST pagination ($top=500)
- Library assignment errors require file move + re-sync

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Single "Documents" library | 627 items unmanageable; no category UX |
| Library per WTMS folder | Too many libraries; over-provisioned |
| OneDrive folders | No SharePoint List integration; weak governance |
| 12+ micro-libraries | Operational overhead; manifest complexity |
