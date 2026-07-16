# Repository Operation Policy

**Version**: 1.0.2  
**Effective**: 2026-07-16  
**Status**: ACTIVE — READ-MOSTLY MODE

---

## Policy Statement

The RAE Enterprise Canonical Repository enters **READ-MOSTLY MODE** effective EA-14 (2026-07-16). Production implementation (SharePoint, Registry, 627-document corpus) is frozen. The repository serves as the long-term architectural reference for all RAE digital systems.

---

## READ-MOSTLY MODE

```text
┌─────────────────────────────────────────────────────────┐
│  READ-MOSTLY MODE (effective v1.0.2)                    │
│                                                         │
│  ✓ Read architecture, ADRs, standards, runbooks        │
│  ✓ Pin release tags for dependent projects             │
│  ✓ Limited documentation and governance updates        │
│                                                         │
│  ✗ No SharePoint modifications via this repo           │
│  ✗ No Registry data changes                            │
│  ✗ No architecture redesign                            │
│  ✗ No ADR decision reversals                           │
└─────────────────────────────────────────────────────────┘
```

---

## Changes Allowed (Without Architecture Review)

| Category | Examples | Version bump |
|----------|----------|--------------|
| Documentation | Typo fixes, link updates, clarifications | PATCH (1.0.x) |
| ADR (new) | Document new decisions for future platforms | MINOR (1.x.0) |
| Bug fixes | Script fixes that do not change M365 behavior | PATCH |
| Security fixes | Secret removal, gitignore updates | PATCH |
| Production maintenance | Runbook updates, operational clarifications | PATCH |

---

## Changes Requiring Architecture Review

| Category | Requirements |
|----------|-------------|
| Major architecture | Architecture Review + ADR + Change Request |
| Baseline amendment | MAJOR version + acceptance update |
| Standards breaking change | ADR + dependent project notification |
| New SharePoint library | ADR-004 amendment + MAJOR |
| Registry schema break | ADR-003 amendment + MAJOR |
| ADR reversal | Superseding ADR + architecture review |
| Governance activation | EA-6C change request + acceptance update |

**Process**: [CHANGE_CONTROL_POLICY.md](../canonical/CHANGE_CONTROL_POLICY.md)

---

## Explicitly Prohibited

- Modify SharePoint document libraries or files
- Modify Registry rows or schema
- Additional WTMS migration batches
- `--force` re-upload scripts
- Commit secrets, browser profiles, or document binaries
- Treat GitHub Pages as production data source
- Redefine DocumentID format or six-library strategy
- Reverse accepted ADR decisions without superseding ADR

---

## Production Maintenance

Operational tasks on live M365 systems follow [OPERATION_RUNBOOK_v1.0.md](../release/OPERATION_RUNBOOK_v1.0.md):

- Registry sync (`--sync-all`) for drift correction
- Spot URL verification
- Monthly QA reconcile (627/627/627)

These are **operational**, not architectural. Evidence must be logged; post-incident ADR if process changes.

---

## Change Request Template

For major architecture changes:

```markdown
## Change Request: [title]
- Requestor: [name]
- Date: [date]
- Baseline affected: [section reference]
- ADR: [new ADR-NNN or amendment]
- Impact on production: [none / operational / structural]
- Dependent projects: [list]
- Rollback plan: [procedure]
- Approval: [pending / approved / rejected]
```

---

## Related Documents

- [CANONICAL_REPOSITORY_CERTIFICATE.md](CANONICAL_REPOSITORY_CERTIFICATE.md)
- [ARCHITECTURE_LIFECYCLE.md](ARCHITECTURE_LIFECYCLE.md)
- [docs/canonical/REPOSITORY_GOVERNANCE.md](../canonical/REPOSITORY_GOVERNANCE.md)
