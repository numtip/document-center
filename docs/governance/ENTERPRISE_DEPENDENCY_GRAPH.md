# Enterprise Dependency Graph

**Version**: 1.0.2  
**Effective**: 2026-07-16

Every future RAE project must consume **governed data only** — no parallel document stores, no duplicate registries, no ungoverned metadata.

---

## Layer Model

```text
                    ┌──────────────────────────────────────┐
                    │         AI SERVICES (future)         │
                    │  RAG │ Assistants │ Analytics        │
                    └──────────────────┬───────────────────┘
                                       │ governed export only
                    ┌──────────────────▼───────────────────┐
                    │       EXPERIENCE LAYER (future)    │
                    │  Next.js │ Research │ Learning │ GO  │
                    └──────────────────┬───────────────────┘
                                       │ read-only JSON / API
                    ┌──────────────────▼───────────────────┐
                    │        EXPORT LAYER (to build)     │
                    │  public-registry.json │ scheduled   │
                    └──────────────────┬───────────────────┘
                                       │ Registry sync
                    ┌──────────────────▼───────────────────┐
                    │     REGISTRY (complete — frozen)     │
                    │  RAE Document Registry — 627 rows    │
                    └──────────────────┬───────────────────┘
                                       │ metadata from libraries
                    ┌──────────────────▼───────────────────┐
                    │   MICROSOFT 365 (complete — frozen)  │
                    │  6 SharePoint Libraries — 627 files│
                    └──────────────────────────────────────┘
```

---

## Data Flow Rules

| Rule | Enforcement |
|------|-------------|
| Files live only in SharePoint | ADR-001 |
| Metadata discovered via Registry | ADR-003 |
| Portals never store master files | ADR-002 |
| Export filters by visibility + status | Export contract |
| AI consumes export, not raw SharePoint | ADR-009 |
| No duplicate source of truth | [SYSTEM_OF_RECORDS.md](SYSTEM_OF_RECORDS.md) |

---

## Project Dependency Matrix

```text
Microsoft 365 (SharePoint)
    │
    ├──► Registry (AUTO_UPSERT sync)
    │         │
    │         ├──► SharePoint Document Center (production — live)
    │         │
    │         └──► Export Layer (planned)
    │                   │
    │                   ├──► Next.js Public Portal
    │                   ├──► Research Portal
    │                   ├──► Learning Center
    │                   ├──► Green Office
    │                   └──► AI Knowledge Platform
    │
    └──► Governance (M365 — deferred EA-6C)
              │
              └──► Owners, groups, workflows, public access
```

---

## Consumption Contract

Future projects **may**:

- Read Registry export JSON (when export layer exists)
- Read taxonomy and reference standards from this repository
- Link to SharePoint Storage URLs (authenticated)
- Display metadata filtered by visibility

Future projects **must not**:

- Create parallel document libraries without ADR
- Store document binaries in application repos
- Write to Registry without approved sync tooling
- Bypass visibility model for AI ingestion
- Redefine DocumentID format or library strategy

---

## Canonical Repository Position

```text
┌─────────────────────────────────────────┐
│  RAE Enterprise Canonical Repository    │  ← standards, ADRs, contracts
│  (this repo — READ-MOSTLY)              │
└──────────────────┬──────────────────────┘
                   │ references only
                   ▼
         All layers above consume
         governed data — never redefine
```

---

## Related Documents

- [RAE_ENTERPRISE_PLATFORM_ROADMAP.md](RAE_ENTERPRISE_PLATFORM_ROADMAP.md)
- [CONSUMER_IMPLEMENTATION_GUIDE.md](CONSUMER_IMPLEMENTATION_GUIDE.md)
- [SYSTEM_OF_RECORDS.md](SYSTEM_OF_RECORDS.md)
- [docs/adr/ADR-001-m365-source-of-truth.md](../adr/ADR-001-m365-source-of-truth.md)
