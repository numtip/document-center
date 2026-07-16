# Architecture Lifecycle

**Version**: 1.0.2  
**Effective**: 2026-07-16

Defines the version roadmap for the RAE Enterprise Canonical Repository and associated platform portfolio.

---

## Version 1.x — Maintenance Only

**Current phase. Active.**

| Scope | Detail |
|-------|--------|
| Document Center | Production frozen — 627/627/627 |
| Repository mode | READ-MOSTLY |
| Allowed changes | Documentation, ADRs, bug fixes, security fixes, runbook updates |
| Forbidden | SharePoint changes, Registry changes, architecture redesign, ADR reversal |
| Patch releases | 1.0.x governance and documentation |

**Exit criteria for 1.x**: All enterprise governance docs complete (EA-14). ✓

---

## Version 2.x — Platform Expansion

**Not started. Requires change control.**

| Scope | Detail |
|-------|--------|
| New platforms | Research Portal, Learning Center, Green Office |
| Prerequisites | Registry export pipeline, taxonomy extension ADRs |
| Governance | Partial EA-6C activation (owners, groups) |
| Repository changes | New ADRs, standards extensions (MINOR bump) |
| Production | Document Center remains frozen baseline |

**Deliverables**:

- Research Portal MVP consuming Registry export
- Learning Center authenticated access
- Green Office taxonomy ADR and library assignment
- Updated dependent project registry

---

## Version 3.x — Unified Public Experience

**Not started. Requires MAJOR planning.**

| Scope | Detail |
|-------|--------|
| Public portal | Next.js deployment (`rae-nextjs-main`) |
| Export layer | Scheduled Registry export → `public-registry.json` |
| Public access | Tenant policy decision (anonymous vs authenticated) |
| Repository changes | Export contract implementation docs, MAJOR if schema break |
| UX | Fuse.js search, static-first public experience |

**Deliverables**:

- Production Registry export automation
- Next.js portal with filtered public records
- Public access policy ADR
- Link validation and monitoring

---

## Version 4.x — AI Native Platform

**Not started. Requires MAJOR planning + AI governance ADR.**

| Scope | Detail |
|-------|--------|
| AI services | RAG, assistants, analytics over governed corpus |
| Prerequisites | Export layer, visibility enforcement, embedding governance |
| Data boundary | AI consumes export only — never raw SharePoint scrape |
| Repository changes | AI integration ADRs, ingestion standards |
| Analytics | Future platform (system of record TBD) |

**Deliverables**:

- AI Knowledge Platform with governed ingestion
- DocumentID-indexed embedding store
- Visibility-aware retrieval (no internal doc leakage)
- AI assistant integration guidelines

---

## Lifecycle Diagram

```text
v1.0.x  ──►  MAINTENANCE (current — frozen production)
    │
    ▼
v2.x    ──►  PLATFORM EXPANSION (Research, Learning, Green Office)
    │
    ▼
v3.x    ──►  UNIFIED PUBLIC EXPERIENCE (Next.js + export layer)
    │
    ▼
v4.x    ──►  AI NATIVE PLATFORM (RAG, assistants, analytics)
```

---

## Transition Rules

| From → To | Requirement |
|-----------|-------------|
| 1.x → 2.x | Architecture review + platform ADRs + export pipeline plan |
| 2.x → 3.x | Public access policy ADR + export contract implemented |
| 3.x → 4.x | AI governance ADR + visibility enforcement proven |

Each transition requires baseline comparison per [CHANGE_CONTROL_POLICY.md](../canonical/CHANGE_CONTROL_POLICY.md).

---

## Related Documents

- [RAE_ENTERPRISE_PLATFORM_ROADMAP.md](RAE_ENTERPRISE_PLATFORM_ROADMAP.md)
- [REPOSITORY_OPERATION_POLICY.md](REPOSITORY_OPERATION_POLICY.md)
- [docs/canonical/CHANGE_CONTROL_POLICY.md](../canonical/CHANGE_CONTROL_POLICY.md)
