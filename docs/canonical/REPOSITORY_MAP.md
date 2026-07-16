# Repository Map

**Version**: 1.0.1  
**Effective**: 2026-07-16

---

## 1. Repository Layout

```text
document-center/                          ← RAE Enterprise Canonical Repository
├── README.md                             ← Master entry point
├── VERSION                               ← Current semver (1.0.1)
├── CHANGELOG.md                          ← Release history
├── package.json                          ← Validation & preview scripts
│
├── docs/
│   ├── canonical/                        ← ★ Governance & standards (EA-13)
│   │   ├── CANONICAL_REPOSITORY_CHARTER.md
│   │   ├── REPOSITORY_GOVERNANCE.md
│   │   ├── REFERENCE_STANDARDS.md
│   │   ├── REPOSITORY_MAP.md               ← this file
│   │   ├── PROJECT_INDEX.md
│   │   ├── DEPENDENT_PROJECTS.md
│   │   ├── PROJECT_MEMORY_FREEZE_v1.md
│   │   └── CHANGE_CONTROL_POLICY.md
│   │
│   ├── adr/                              ← ★ Architecture Decision Records
│   │   ├── README.md
│   │   └── ADR-001 … ADR-009
│   │
│   ├── release/                          ← ★ v1.0 production freeze package
│   │   ├── ARCHITECTURE_BASELINE_v1.0.md
│   │   ├── DOCUMENT_CENTER_v1.0_PRODUCTION_FREEZE.md
│   │   ├── PRODUCTION_ACCEPTANCE_CERTIFICATE.md
│   │   ├── OPERATION_RUNBOOK_v1.0.md
│   │   ├── PROJECT_CLOSEOUT_REPORT.md
│   │   └── RELEASE_NOTES_v1.0.md
│   │
│   ├── architecture/                     ← Architecture audits & baselines
│   ├── document-center/                  ← Schemas, taxonomy, registry drafts
│   ├── m365/                             ← M365 phase reports & contracts
│   ├── governance/                       ← Legacy governance (convergence model)
│   ├── design/                           ← UI blueprints (Stitch v2)
│   ├── runbooks/                         ← Workstation & recovery runbooks
│   ├── audits/                           ← Tenant capability audits
│   └── reports/                          ← Generated reports
│
├── scripts/                              ← TypeScript validation & build
├── preview/                              ← GitHub Pages static preview
├── migration/                            ← SharePoint migration manifest
├── .migration/rae-wtms/                  ← Migration evidence & tools
│   ├── ea-10/                            ← EA-10 results & state
│   ├── ea-11/                            ← EA-11 QA evidence
│   └── tools/                            ← Python M365 automation scripts
│
└── .github/workflows/                    ← CI (Pages deploy)
```

---

## 2. Architecture Layers

```text
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                         │
│  SharePoint DC page │ GitHub Pages preview │ Future Next.js │
├─────────────────────────────────────────────────────────────┤
│  DISCOVERY LAYER                                            │
│  RAE Document Registry (SharePoint List — 627 rows)         │
├─────────────────────────────────────────────────────────────┤
│  STORAGE LAYER                                              │
│  6 SharePoint Document Libraries (627 files)                │
├─────────────────────────────────────────────────────────────┤
│  AUTHORING LAYER (archived)                                 │
│  WTMS staging corpus │ migration manifest │ taxonomy        │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Documentation Locations

| Need | Go to |
|------|-------|
| Start here | `README.md` |
| Why this repo exists | `docs/canonical/CANONICAL_REPOSITORY_CHARTER.md` |
| Frozen production architecture | `docs/release/ARCHITECTURE_BASELINE_v1.0.md` |
| Field values & naming | `docs/canonical/REFERENCE_STANDARDS.md` |
| Why a decision was made | `docs/adr/` |
| How to operate M365 | `docs/release/OPERATION_RUNBOOK_v1.0.md` |
| Migration history | `docs/m365/ea-*-*.md` |
| Registry export contract | `docs/m365/registry-export-contract.md` |
| What changed per release | `CHANGELOG.md` |

---

## 4. Scripts

| Path | Purpose |
|------|---------|
| `scripts/validate-document-migration-matrix.ts` | Matrix CSV validation |
| `scripts/validate-document-registry.ts` | Registry JSON validation |
| `scripts/generate-registry-draft.ts` | Registry draft generation |
| `scripts/build-preview.ts` | GitHub Pages preview build |
| `.migration/rae-wtms/tools/_ea8_registry_sync.py` | Registry AUTO_UPSERT |
| `.migration/rae-wtms/tools/_ea11_corpus_artifacts.py` | Corpus reconciliation |

---

## 5. Schemas

| File | Purpose |
|------|---------|
| `docs/document-center/taxonomy.json` | Category taxonomy |
| `docs/document-center/document-registry.draft.json` | Authoring registry schema |
| `docs/document-center/migration-matrix.v2.csv` | Migration matrix |
| `migration/sharepoint-migration-manifest.csv` | Canonical manifest (627 READY) |
| `docs/m365/registry-export-contract.md` | Export JSON contract |

---

## 6. Migration Artifacts

| Path | Contents |
|------|----------|
| `.migration/rae-wtms/ea-10/` | EA-10 selection, results, state, reconciliation |
| `.migration/rae-wtms/ea-11/` | EA-11 corpus summary, portal QA |
| `.migration/rae-wtms/tools/` | Phase automation scripts |
| `.migration/rae-wtms/metadata/` | Crawl & mapping metadata |

---

## 7. Release Package

Frozen at tag `document-center-v1.0.0`:

```text
docs/release/
├── ARCHITECTURE_BASELINE_v1.0.md
├── DOCUMENT_CENTER_v1.0_PRODUCTION_FREEZE.md
├── PRODUCTION_ACCEPTANCE_CERTIFICATE.md
├── OPERATION_RUNBOOK_v1.0.md
├── PROJECT_CLOSEOUT_REPORT.md
└── RELEASE_NOTES_v1.0.md
```

---

## 8. Canonical References

| Document | Role |
|----------|------|
| [CANONICAL_REPOSITORY_CHARTER.md](CANONICAL_REPOSITORY_CHARTER.md) | Repository purpose & authority |
| [REFERENCE_STANDARDS.md](REFERENCE_STANDARDS.md) | Normative field & naming standards |
| [CHANGE_CONTROL_POLICY.md](CHANGE_CONTROL_POLICY.md) | Required process for changes |
| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Full document index |
| [DEPENDENT_PROJECTS.md](DEPENDENT_PROJECTS.md) | Downstream consumers |
