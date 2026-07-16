# Repository Governance

**Version**: 1.0.1  
**Effective**: 2026-07-16  
**Applies to**: RAE Enterprise Canonical Repository

---

## 1. Branch Strategy

| Branch | Purpose | Lifetime |
|--------|---------|----------|
| `main` | Canonical integrated baseline | Permanent |
| `feature/*` | Isolated development (docs, scripts, standards) | Temporary; merge via PR |
| `gh-pages` | GitHub Pages preview deployment | Managed by CI workflow |
| Tags | Release snapshots | Permanent |

**Rules**:

- `main` is protected; direct commits require review for architectural changes
- No long-lived forks of architecture documentation
- Feature branches must not modify production SharePoint or Registry data

---

## 2. Release Strategy

| Release type | Trigger | Version bump | Tag format |
|--------------|---------|--------------|------------|
| Documentation / governance | Standards, ADRs, runbooks | PATCH (1.0.x) | `document-center-v1.0.x` |
| Standards amendment | Reference standards change | MINOR (1.x.0) | `document-center-v1.x.0` |
| Architecture change | Baseline amendment | MAJOR (x.0.0) | `document-center-vx.0.0` |

Each release includes:

- Updated `CHANGELOG.md`
- Updated `VERSION` file
- Annotated git tag
- Release notes when applicable

---

## 3. Version Policy

Semantic Versioning ([semver.org](https://semver.org/)):

| Component | Meaning for this repository |
|-----------|----------------------------|
| MAJOR | Breaking architecture or standards change |
| MINOR | New standards, ADRs, non-breaking extensions |
| PATCH | Documentation fixes, governance clarifications |

Current: **1.0.1** (canonical elevation — governance only, no production changes)

---

## 4. Review Policy

| Change scope | Review requirement |
|--------------|-------------------|
| Typo / link fix | Single reviewer |
| New ADR | Architecture owner |
| Standards amendment | Architecture owner + affected domain owner |
| Baseline change | Architecture review board + acceptance update |
| Script change affecting M365 | Migration lead + dry-run evidence |

Pull requests must reference affected ADRs or state "no architectural impact."

---

## 5. Architecture Approval Policy

Architecture changes require:

1. Written ADR in `docs/adr/`
2. Comparison against `docs/release/ARCHITECTURE_BASELINE_v1.0.md`
3. Impact analysis on dependent projects (see [DEPENDENT_PROJECTS.md](DEPENDENT_PROJECTS.md))
4. Explicit approval before any production M365 change

**Pre-approved (frozen v1.0)**:

- Six SharePoint libraries
- Registry AUTO_UPSERT pattern
- SharePoint Document Center as production portal
- GitHub Pages as preview only

---

## 6. ADR Policy

| Rule | Detail |
|------|--------|
| Location | `docs/adr/ADR-NNN-title.md` |
| Numbering | Sequential; never reuse numbers |
| Status values | Proposed → Accepted → Deprecated → Superseded |
| Supersession | New ADR references superseded ADR |
| Retroactive ADRs | EA-13 ADR-001–009 document decisions already made |

Template: Context → Decision → Consequences → Alternatives Considered

---

## 7. Deprecation Policy

| Asset type | Deprecation process |
|------------|---------------------|
| ADR | Mark Superseded; link to replacement ADR |
| Standard field | Document in CHANGELOG; grace period for dependents |
| Script | Mark deprecated in header; retain until next MAJOR |
| Migration tool | Archive in `.migration/`; do not delete evidence |

Deprecated items remain in repository for audit trail.

---

## 8. Backward Compatibility Policy

| Layer | Policy |
|-------|--------|
| DocumentID format | Immutable (`RAE-NNNNN`) |
| Registry idempotency key | DocumentID — never change |
| Library names | Frozen; new libraries require ADR |
| Export JSON schema | Additive changes only in MINOR; breaking in MAJOR |
| Preview build | Must continue to reject production URLs |

Dependent projects must pin to a release tag when consuming standards.

---

## Related Documents

- [CANONICAL_REPOSITORY_CHARTER.md](CANONICAL_REPOSITORY_CHARTER.md)
- [CHANGE_CONTROL_POLICY.md](CHANGE_CONTROL_POLICY.md)
- [docs/adr/README.md](../adr/README.md)
