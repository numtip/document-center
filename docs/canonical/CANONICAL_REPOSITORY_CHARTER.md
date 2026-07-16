# Canonical Repository Charter

**Repository**: RAE Enterprise Canonical Repository  
**Former name**: RAE Document Center (implementation project)  
**Version**: 1.0.1  
**Effective**: 2026-07-16  
**Status**: AUTHORITATIVE

---

## 1. Purpose

This repository is the **mandatory architectural reference** for all RAE digital platforms at Maejo University. It preserves the completed Document Center v1.0 implementation as a frozen production baseline while serving as the authoritative source for architecture, metadata standards, registry design, document governance, M365 integration patterns, and information architecture.

Future RAE projects **must reference** this repository before designing systems that touch documents, metadata, SharePoint, or public portals.

---

## 2. Authority

| Domain | Authority |
|--------|-----------|
| Architecture decisions | This repository + ADRs in `docs/adr/` |
| Production baseline | `docs/release/ARCHITECTURE_BASELINE_v1.0.md` (frozen v1.0) |
| Metadata & Registry model | `docs/canonical/REFERENCE_STANDARDS.md` |
| M365 integration patterns | `docs/m365/` phase reports + runbooks |
| Change control | `docs/canonical/CHANGE_CONTROL_POLICY.md` |

**Production data authority** remains in Microsoft 365 (SharePoint libraries + Registry). This repository does **not** store document binaries or live registry data.

---

## 3. Scope

### In scope

- Architecture documentation and ADRs
- Metadata schemas, taxonomy, and registry model
- Document governance standards (deferred activation documented)
- M365 integration patterns and runbooks
- Migration evidence and reconciliation artifacts
- Validation scripts and preview build tooling
- Release packages and acceptance certificates
- Operational runbooks

### Out of scope

- Document file storage (SharePoint is authoritative)
- Live Registry data (SharePoint List is authoritative)
- Production portal runtime (SharePoint page + future Next.js)
- Governance workflow activation (deferred — EA-6C)
- Additional WTMS migration (frozen at 627 documents)

---

## 4. Responsibilities

| Stakeholder | Responsibility |
|-------------|----------------|
| Architecture owner | Maintain baseline, ADRs, and change control |
| Registry owner | Ensure standards align with SharePoint List schema |
| Portal owner | Reference portal topology; do not fork architecture |
| Migration engineering | Preserve tools and evidence; no production changes without approval |
| Dependent projects | Consume standards; submit ADRs for deviations |

---

## 5. Architecture Ownership

Architecture ownership includes:

- Six-library SharePoint strategy
- Registry-as-discovery-layer pattern
- Presentation-layer separation (website ≠ file store)
- Preview vs production portal distinction
- Idempotent Registry sync (AUTO_UPSERT)

All modifications require [Change Control Policy](CHANGE_CONTROL_POLICY.md) compliance.

---

## 6. Change Governance

| Change type | Requirement |
|-------------|-------------|
| Documentation only | PR review; patch version bump |
| Standards amendment | ADR + architecture review |
| Production architecture | ADR + baseline comparison + acceptance update |
| Breaking standard change | Major version + dependent project notification |

See [REPOSITORY_GOVERNANCE.md](REPOSITORY_GOVERNANCE.md) and [CHANGE_CONTROL_POLICY.md](CHANGE_CONTROL_POLICY.md).

---

## 7. Repository Lifecycle

```text
EA-3 … EA-12  →  Implementation & migration (COMPLETE)
EA-13         →  Canonical repository elevation (THIS CHARTER)
Future        →  Governance docs, ADRs, standards maintenance
                →  No production data changes without change control
```

| Phase | Status |
|-------|--------|
| v1.0.0 Production freeze | COMPLETE |
| v1.0.1 Canonical elevation | ACTIVE |
| v1.1+ Standards evolution | Requires ADR |

---

## 8. Reference Policy

1. **Cite, don't copy** — Dependent projects link to this repo; do not duplicate architecture docs.
2. **ADR before deviation** — Any architectural deviation requires a new ADR referencing the baseline.
3. **Baseline is frozen** — v1.0 production architecture is immutable except via formal change control.
4. **Standards are normative** — `REFERENCE_STANDARDS.md` defines required field values, naming, and taxonomy.
5. **Memory is preserved** — `PROJECT_MEMORY_FREEZE_v1.md` captures operational lessons; consult before M365 automation.

---

## 9. Authoritative Sources

This repository is the authoritative source for:

| Domain | Primary document |
|--------|------------------|
| Architecture | `docs/release/ARCHITECTURE_BASELINE_v1.0.md` |
| Metadata | `docs/canonical/REFERENCE_STANDARDS.md` |
| Registry model | `docs/m365/registry-export-contract.md` |
| Document governance | `docs/m365/ea-6c-governance-decision-request.md` |
| M365 integration | `docs/m365/` + `docs/release/OPERATION_RUNBOOK_v1.0.md` |
| Information architecture | `docs/document-center/taxonomy.json` |
| ADRs | `docs/adr/` |

---

## Related Documents

- [REPOSITORY_GOVERNANCE.md](REPOSITORY_GOVERNANCE.md)
- [REPOSITORY_MAP.md](REPOSITORY_MAP.md)
- [PROJECT_INDEX.md](PROJECT_INDEX.md)
- [DEPENDENT_PROJECTS.md](DEPENDENT_PROJECTS.md)
