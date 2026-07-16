# Change Control Policy

**Version**: 1.0.1  
**Effective**: 2026-07-16  
**Applies to**: All future architectural modifications

---

## 1. Policy Statement

No architectural modification to the RAE Document Center or dependent platforms may proceed without formal change control. Production data (SharePoint files, Registry rows) must not change without approved impact analysis.

---

## 2. Required Before Any Architectural Change

| Step | Deliverable |
|------|-------------|
| 1. Architecture Review | Written review against frozen baseline |
| 2. ADR | New or amended ADR in `docs/adr/` |
| 3. Semantic Versioning | MAJOR/MINOR/PATCH bump per impact |
| 4. Baseline Comparison | Diff against `ARCHITECTURE_BASELINE_v1.0.md` |
| 5. Impact Analysis | Effect on dependent projects, Registry, libraries, portals |

---

## 3. Change Categories

| Category | Examples | Approval | Version |
|----------|----------|----------|---------|
| **Patch** | Typo, link fix, runbook clarification | Single reviewer | 1.0.x |
| **Minor** | New ADR, standards extension, new script | Architecture owner | 1.x.0 |
| **Major** | New library, Registry schema break, portal topology change | Architecture review + acceptance update | x.0.0 |
| **Production data** | Upload, delete, Registry row change | Migration lead + dry-run evidence | N/A (no repo version) |

---

## 4. Architecture Review Checklist

- [ ] References `docs/release/ARCHITECTURE_BASELINE_v1.0.md`
- [ ] ADR created or updated
- [ ] `REFERENCE_STANDARDS.md` impact assessed
- [ ] Dependent projects notified (see [DEPENDENT_PROJECTS.md](DEPENDENT_PROJECTS.md))
- [ ] Backward compatibility evaluated
- [ ] Rollback plan documented
- [ ] No secrets in commit scope

---

## 5. ADR Requirement

Every architectural decision must have an ADR containing:

1. **Context** — Problem and constraints
2. **Decision** — What was chosen
3. **Consequences** — Positive and negative effects
4. **Alternatives Considered** — Rejected options and why

Retroactive ADRs (EA-13 ADR-001–009) document decisions already implemented.

---

## 6. Baseline Comparison

Compare proposed change against frozen v1.0 baseline:

| Baseline element | Change allowed without MAJOR? |
|------------------|-------------------------------|
| Six libraries | No — requires MAJOR + ADR |
| DocumentID format | No — immutable |
| Registry idempotency key | No — immutable |
| AUTO_UPSERT pattern | No — requires ADR |
| Preview vs production separation | No — requires ADR |
| Documentation / runbooks | Yes — PATCH |
| New export field (additive) | Yes — MINOR |

---

## 7. Impact Analysis Template

```markdown
## Change: [title]
- Baseline section affected: [reference]
- ADR: [ADR-NNN]
- Dependent projects affected: [list]
- Registry impact: [none / additive / breaking]
- SharePoint impact: [none / metadata / structural]
- Rollback: [procedure]
- Version bump: [PATCH / MINOR / MAJOR]
```

---

## 8. Prohibited Without Approval

- Additional WTMS migration batches
- New SharePoint libraries
- Registry schema breaking changes
- `--force` re-upload scripts
- Governance workflow activation (EA-6C)
- Committing secrets, browser profiles, or document binaries
- Treating GitHub Pages as production data source

---

## 9. Emergency Changes

Production incidents (broken URLs, missing Registry rows) may proceed under [OPERATION_RUNBOOK_v1.0.md](../release/OPERATION_RUNBOOK_v1.0.md) without ADR, but require:

1. Post-incident ADR or runbook amendment within 5 business days
2. Evidence logged in migration artifacts
3. Corpus reconcile verification (627/627/627)

---

## Related Documents

- [REPOSITORY_GOVERNANCE.md](REPOSITORY_GOVERNANCE.md)
- [CANONICAL_REPOSITORY_CHARTER.md](CANONICAL_REPOSITORY_CHARTER.md)
- [docs/adr/README.md](../adr/README.md)
