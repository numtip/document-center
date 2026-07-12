# Project Baseline — RAE Document Center

| Field | Value |
|-------|-------|
| **Project** | RAE Document Center |
| **Canonical Repository** | https://github.com/numtip/document-center |
| **Default Branch** | main |
| **Handoff Baseline Commit** | `87802abcfe40dd643ec8ad233dc1b3c45308c7ac` |
| **Architecture Status** | OneDrive-based metadata registry with proposed M365 Foundation blueprint (not yet implemented) |

## Known Archives for Recovery

| Source | Purpose | Status |
|--------|---------|--------|
| `G:\ProjectAI\RAE-M365-Platform` | ONE-TIME historical recovery source | Active |

> **Important**: `G:\ProjectAI\RAE-M365-Platform` is NOT a second canonical project. It is a recovery source only. After historical recovery is complete, all authoritative work must flow through the canonical repository at https://github.com/numtip/document-center.

## Branch Strategy

- `main` — Integrated project baseline. Protected. No force-pushes.
- Feature branches — Short-lived branches created from `main`, merged via pull request.
- `gh-pages` — GitHub Pages deployment branch (preview/demo only).

## Governance Reference

See [docs/governance/GIT_CANONICAL_VERSION_POLICY.md](docs/governance/GIT_CANONICAL_VERSION_POLICY.md) for the full canonical version policy.
