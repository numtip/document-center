# RAE Enterprise Canonical Repository

**Maejo University — Research and Academic Extension**

This repository is the **mandatory architectural reference** for all RAE digital platforms. It preserves the completed Document Center v1.0 production implementation and defines the standards, governance, and patterns that future projects must follow.

> **Production is frozen at v1.0.0.** SharePoint holds 627 documents. This repository holds architecture, metadata standards, and tooling — not document binaries.

---

## Purpose

| Role | Description |
|------|-------------|
| **Canonical reference** | Architecture, ADRs, metadata standards, registry model |
| **Production baseline** | Frozen v1.0 acceptance (627 files, 627 Registry rows) |
| **Governance hub** | Change control, reference standards, dependent project registry |
| **Operational toolkit** | Validation scripts, migration evidence, runbooks |

Start here: [Canonical Repository Charter](docs/canonical/CANONICAL_REPOSITORY_CHARTER.md)

---

## Architecture

```text
SharePoint libraries (627 files — authoritative)
        ↓
RAE Document Registry (627 rows — metadata discovery)
        ↓
SharePoint Document Center page (production portal)
        ↓
(planned) Registry export → Next.js public portal
```

Websites are **presentation layers only** — they do not store master files. See [ADR-002](docs/adr/ADR-002-website-presentation-layer.md).

---

## Production URL

```text
https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx
```

Requires Maejo365 authentication. See [EA-11A Production URL](docs/m365/ea-11a-production-url.md).

| Environment | URL | Records |
|-------------|-----|--------:|
| **Production** | SharePoint Document Center (above) | 627 |
| **Preview** | https://numtip.github.io/document-center/ | 3 (demo) |

---

## Repository Structure

```text
docs/
├── canonical/          ← Governance, standards, change control (start here)
├── adr/                ← Architecture Decision Records (ADR-001–009)
├── release/            ← v1.0 production freeze package
├── m365/               ← M365 phase reports & contracts
├── document-center/    ← Taxonomy, schemas, migration matrices
├── architecture/       ← Architecture audits
└── design/             ← UI blueprints

scripts/                ← Validation & preview build (TypeScript)
preview/                ← GitHub Pages static preview (demo only)
.migration/rae-wtms/    ← Migration evidence & M365 automation tools
```

Full map: [Repository Map](docs/canonical/REPOSITORY_MAP.md) · Index: [Project Index](docs/canonical/PROJECT_INDEX.md)

---

## Current Release

| Item | Value |
|------|-------|
| Version | **1.0.1** |
| Production freeze | `document-center-v1.0.0` |
| Canonical elevation | `document-center-v1.0.1` |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |

Release package: [docs/release/](docs/release/)

---

## Dependent Projects

Future RAE platforms must reference this repository before implementation:

| Project | Consumes |
|---------|----------|
| RAE Next.js | Registry export JSON, taxonomy, standards |
| Research Portal | Research library metadata |
| Green Office | Taxonomy, governance model |
| Learning Center | AcademicServices / SOPManuals metadata |
| AI Knowledge Platform | Registry export, DocumentID index |
| AI Assistants | Metadata, ADRs, export JSON |

Details: [Dependent Projects](docs/canonical/DEPENDENT_PROJECTS.md)

---

## Scripts

```bash
rtk npm install
rtk npm run validate:all
rtk npm run build
```

| Command | Description |
|---------|-------------|
| `npm run validate:all` | Validate migration matrix + registry schema |
| `npm run build` | Build GitHub Pages preview into `dist/` |

Registry sync (M365): see [Operation Runbook v1.0](docs/release/OPERATION_RUNBOOK_v1.0.md)

---

## Contribution Rules

1. Read [Change Control Policy](docs/canonical/CHANGE_CONTROL_POLICY.md) before architectural changes
2. Submit an ADR for any deviation from [Reference Standards](docs/canonical/REFERENCE_STANDARDS.md)
3. Do not commit secrets, browser profiles, or document binaries
4. Do not modify production SharePoint or Registry without approved impact analysis
5. Compare against [Architecture Baseline v1.0](docs/release/ARCHITECTURE_BASELINE_v1.0.md)

---

## Key Documents

| Document | Path |
|----------|------|
| Charter | [docs/canonical/CANONICAL_REPOSITORY_CHARTER.md](docs/canonical/CANONICAL_REPOSITORY_CHARTER.md) |
| Reference Standards | [docs/canonical/REFERENCE_STANDARDS.md](docs/canonical/REFERENCE_STANDARDS.md) |
| Architecture Baseline | [docs/release/ARCHITECTURE_BASELINE_v1.0.md](docs/release/ARCHITECTURE_BASELINE_v1.0.md) |
| ADR Index | [docs/adr/README.md](docs/adr/README.md) |
| Project Memory | [docs/canonical/PROJECT_MEMORY_FREEZE_v1.md](docs/canonical/PROJECT_MEMORY_FREEZE_v1.md) |
| Operation Runbook | [docs/release/OPERATION_RUNBOOK_v1.0.md](docs/release/OPERATION_RUNBOOK_v1.0.md) |

---

## Security

- Do not commit `.env`, certificates, tokens, or real SharePoint share URLs
- `.browser-profile/` is gitignored (M365 auth session)
- GitHub Pages preview ships only 3 demo records with `example.sharepoint.com` URLs

---

## License

Internal RAE project — confirm governance policy before external distribution.
