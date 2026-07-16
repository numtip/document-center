# RAE Enterprise Canonical Repository

**Maejo University — Research and Academic Extension**

This repository is the **mandatory architectural reference** for all RAE digital platforms. It preserves the completed Document Center v1.0 production implementation and defines the standards, governance, and patterns that future projects must follow.

> **Enterprise Canonical Repository — FROZEN (v1.0.2).** Production frozen at v1.0.0 (627 SharePoint documents). Repository mode: **READ-MOSTLY**. All future RAE systems must consume this repository instead of redefining architecture.

---

## Purpose

| Role | Description |
|------|-------------|
| **Canonical reference** | Architecture, ADRs, metadata standards, registry model |
| **Production baseline** | Frozen v1.0 acceptance (627 files, 627 Registry rows) |
| **Governance hub** | Change control, reference standards, dependent project registry |
| **Operational toolkit** | Validation scripts, migration evidence, runbooks |

Start here: [Canonical Repository Charter](docs/canonical/CANONICAL_REPOSITORY_CHARTER.md) · [Enterprise Certificate](docs/governance/CANONICAL_REPOSITORY_CERTIFICATE.md)

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
├── canonical/          ← Standards, change control, charter
├── governance/         ← Enterprise governance (roadmap, lifecycle, certificate)
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
| Version | **1.0.2** |
| Repository mode | **READ-MOSTLY** (enterprise governance frozen) |
| Production freeze | `document-center-v1.0.0` |
| Enterprise governance | `document-center-v1.0.2` |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |

Release package: [docs/release/](docs/release/) · Enterprise governance: [docs/governance/](docs/governance/)

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

Details: [Dependent Projects](docs/canonical/DEPENDENT_PROJECTS.md) · [Consumer Guide](docs/governance/CONSUMER_IMPLEMENTATION_GUIDE.md) · [Platform Roadmap](docs/governance/RAE_ENTERPRISE_PLATFORM_ROADMAP.md)

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

Repository is in **READ-MOSTLY mode**. See [Repository Operation Policy](docs/governance/REPOSITORY_OPERATION_POLICY.md).

1. Read [Change Control Policy](docs/canonical/CHANGE_CONTROL_POLICY.md) before architectural changes
2. Submit an ADR for any deviation from [Reference Standards](docs/canonical/REFERENCE_STANDARDS.md)
3. Do not commit secrets, browser profiles, or document binaries
4. Do not modify production SharePoint or Registry without approved impact analysis
5. Compare against [Architecture Baseline v1.0](docs/release/ARCHITECTURE_BASELINE_v1.0.md)
6. New projects must use [Project Bootstrap Template](docs/governance/PROJECT_BOOTSTRAP_TEMPLATE.md)

---

## Key Documents

| Document | Path |
|----------|------|
| Charter | [docs/canonical/CANONICAL_REPOSITORY_CHARTER.md](docs/canonical/CANONICAL_REPOSITORY_CHARTER.md) |
| Enterprise Certificate | [docs/governance/CANONICAL_REPOSITORY_CERTIFICATE.md](docs/governance/CANONICAL_REPOSITORY_CERTIFICATE.md) |
| Architecture Principles | [docs/governance/ARCHITECTURE_PRINCIPLES.md](docs/governance/ARCHITECTURE_PRINCIPLES.md) |
| Consumer Guide | [docs/governance/CONSUMER_IMPLEMENTATION_GUIDE.md](docs/governance/CONSUMER_IMPLEMENTATION_GUIDE.md) |
| Reference Standards | [docs/canonical/REFERENCE_STANDARDS.md](docs/canonical/REFERENCE_STANDARDS.md) |
| Architecture Baseline | [docs/release/ARCHITECTURE_BASELINE_v1.0.md](docs/release/ARCHITECTURE_BASELINE_v1.0.md) |
| ADR Index | [docs/adr/README.md](docs/adr/README.md) |
| System of Records | [docs/governance/SYSTEM_OF_RECORDS.md](docs/governance/SYSTEM_OF_RECORDS.md) |
| Operation Runbook | [docs/release/OPERATION_RUNBOOK_v1.0.md](docs/release/OPERATION_RUNBOOK_v1.0.md) |

---

## Security

- Do not commit `.env`, certificates, tokens, or real SharePoint share URLs
- `.browser-profile/` is gitignored (M365 auth session)
- GitHub Pages preview ships only 3 demo records with `example.sharepoint.com` URLs

---

## License

Internal RAE project — confirm governance policy before external distribution.
