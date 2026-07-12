# Project Baseline — RAE Document Center

| Field | Value |
|-------|-------|
| **Project** | RAE Document Center |
| **Canonical Repository** | https://github.com/numtip/document-center |
| **Default Branch** | main |
| **Handoff Baseline Commit** | `87802abcfe40dd643ec8ad233dc1b3c45308c7ac` |
| **Architecture Status** | OneDrive-based metadata registry with proposed M365 Foundation blueprint (not yet implemented) |

## Source of Truth

No external recovery sources exist or have ever existed. This repository is the sole source of project history. All architecture artifacts, governance documents, schemas, and tooling are authored directly against the canonical repository — nothing is imported from elsewhere.

## Branch Strategy

- `main` — Integrated project baseline. Protected. No force-pushes.
- Feature branches — Short-lived branches created from `main`, merged via pull request.
- `gh-pages` — GitHub Pages deployment branch (preview/demo only).

## Governance Reference

See [docs/governance/GIT_CANONICAL_VERSION_POLICY.md](docs/governance/GIT_CANONICAL_VERSION_POLICY.md) for the full canonical version policy.
