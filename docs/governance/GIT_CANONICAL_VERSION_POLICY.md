# Git Canonical Version Policy

## Canonical Repository

**GitHub `numtip/document-center` IS the canonical repository.**

All authoritative metadata, schemas, runbooks, and governance artifacts for the RAE Document Center project live here and only here.

## Branch Model

- **`main` IS the integrated project baseline.** It is NOT a development branch.
- All workstations (HOME, WORK) are Git checkouts of this canonical repository.
- Active local-only project development is PROHIBITED after historical recovery completes.

## Frozen Rules

| # | Rule | Detail |
|---|------|--------|
| 1 | GitHub is canonical | All authoritative metadata, schemas, runbooks, and governance live here |
| 2 | main must not be force-pushed | main is the integrated baseline — rewrite is forbidden |
| 3 | architecture changes require ADR | Any architectural change needs an Architecture Decision Record |
| 4 | architecture artifacts belong in Git | Diagrams, ADRs, models, blueprints |
| 5 | IaC belongs in Git | PnP provisioning scripts, Terraform, any infrastructure-as-code |
| 6 | schemas belong in Git | taxonomy, registry schema, metadata models |
| 7 | Memory OS belongs in Git | AI agent context, Memory OS files |
| 8 | validated exports belong in Git | Production registry exports after validation |
| 9 | secrets never belong in Git | .env, tokens, certs, passwords — always .gitignore |
| 10 | M365 authentication artifacts never belong in Git | App registrations, client secrets, tenant-specific tokens |
| 11 | real master documents never belong in Git | Document files stay in SharePoint/OneDrive |
| 12 | GitHub Pages remains preview/demo only | Never serves real documents |

## Enforcement

- Pull requests targeting `main` must pass validation (`npm run validate:all`) and secret scanning before merge.
- Force-push protection must be enabled on the `main` branch in the GitHub repository settings.
- All team members share responsibility for upholding this policy.

## Exceptions

Any exception to these rules requires a documented ADR approved by the project lead.
