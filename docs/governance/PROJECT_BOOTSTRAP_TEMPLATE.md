# Project Bootstrap Template

**Version**: 1.0.2  
**Effective**: 2026-07-16

Every new RAE digital project **must** include the following references in its project README or charter before implementation begins.

Copy this template into the new project's repository.

---

## Project Identity

```markdown
# [Project Name]

**RAE Platform**: [Research Portal | Learning Center | Green Office | Next.js | AI Knowledge Platform | Other]
**Canonical dependency**: document-center @ `document-center-v1.0.2`
**Status**: [Planning | Development | Production]
```

---

## Required References

### Architecture Reference

| Item | Link |
|------|------|
| Architecture Baseline v1.0 | `https://github.com/numtip/document-center/blob/main/docs/release/ARCHITECTURE_BASELINE_v1.0.md` |
| Enterprise Dependency Graph | `docs/governance/ENTERPRISE_DEPENDENCY_GRAPH.md` |
| Architecture Principles | `docs/governance/ARCHITECTURE_PRINCIPLES.md` |

### Canonical Reference

| Item | Link |
|------|------|
| Canonical Repository Charter | `docs/canonical/CANONICAL_REPOSITORY_CHARTER.md` |
| Canonical Certificate | `docs/governance/CANONICAL_REPOSITORY_CERTIFICATE.md` |
| Repository Operation Policy | `docs/governance/REPOSITORY_OPERATION_POLICY.md` |

### Metadata Reference

| Item | Link |
|------|------|
| Reference Standards | `docs/canonical/REFERENCE_STANDARDS.md` |
| Taxonomy | `docs/document-center/taxonomy.json` |
| Registry Export Contract | `docs/m365/registry-export-contract.md` |

### ADR Reference

| ADR | Applicability |
|-----|---------------|
| ADR-001 M365 Source of Truth | All projects |
| ADR-002 Presentation Layer | All portal/UI projects |
| ADR-003 Registry Pattern | All metadata consumers |
| ADR-004 Library Strategy | All document projects |
| ADR-009 Public Separation | All public-facing projects |

Full index: `docs/adr/README.md`

List project-specific ADRs below:

```markdown
| ADR | Title | Status |
|-----|-------|--------|
| ADR-NNN | [project-specific decision] | Proposed |
```

### Release Reference

```markdown
| Property | Value |
|----------|-------|
| Canonical repo tag | document-center-v1.0.2 |
| Production baseline | document-center-v1.0.0 |
| Pinned date | [YYYY-MM-DD] |
```

### Dependency Declaration

```markdown
## Dependencies

| Dependency | Type | Consumes | Writes |
|------------|------|----------|--------|
| SharePoint (M365) | Storage | Files via Storage URL | [none / via approved workflow] |
| RAE Document Registry | Metadata | Export JSON / List | [none / via sync tool] |
| Canonical Repository | Standards | ADRs, schemas, taxonomy | none |
| [Other] | | | |

## Never Modifies

- [ ] SharePoint library structure (without ADR)
- [ ] Registry idempotency key (DocumentID)
- [ ] DocumentID format
- [ ] Canonical architecture baseline
```

---

## Pre-Implementation Checklist

- [ ] Architecture reference reviewed
- [ ] Canonical reference pinned to tag
- [ ] Metadata reference standards confirmed
- [ ] Required ADRs read; project ADRs drafted if deviating
- [ ] Release tag pinned
- [ ] Dependency declaration complete
- [ ] Consumer guide section reviewed: [CONSUMER_IMPLEMENTATION_GUIDE.md](CONSUMER_IMPLEMENTATION_GUIDE.md)
- [ ] No duplicate system of record: [SYSTEM_OF_RECORDS.md](SYSTEM_OF_RECORDS.md)

---

## Approval

| Role | Name | Date |
|------|------|------|
| Project lead | | |
| Architecture owner | | |

---

## Related Documents

- [CONSUMER_IMPLEMENTATION_GUIDE.md](CONSUMER_IMPLEMENTATION_GUIDE.md)
- [docs/canonical/DEPENDENT_PROJECTS.md](../canonical/DEPENDENT_PROJECTS.md)
