# PXP-2 / PXP-3 CI/CD Runbook

**Date**: 2026-07-16

---

## Workflow Structure

The PXP-2/ PXP-3 export pipeline is designed for both local and CI/CD execution:

### Local Export (Requires M365 Auth)

```bash
python scripts/registry/export-live-registry.py
```

This requires:
1. An initialized Playwright browser profile at `.browser-profile/m365/`
2. Python 3.14+ with `playwright` and `requests` packages
3. An authenticated M365 session (one-time interactive login)

**Important**: Local export uses Playwright-based browser automation to authenticate against SharePoint/M365. This requires an interactive browser session and cannot run unattended in CI/CD without a pre-seeded profile.

### GitHub Actions Workflow

A `workflow_dispatch` workflow is provided at:

```yaml
.github/workflows/registry-export.yml
```

Features:
- `workflow_dispatch` trigger only (manual dispatch — no schedule trigger, because browser-based M365 auth is not available in CI)
- Concurrency guard (one export at a time)
- 15-minute timeout on validate job
- Public export validation via `scripts/registry/validate-public-export.py` (`npm run validate:public-registry`)
- Schema, field, and eligibility validation (static file checks — no M365 access required)
- Portal build (`npm run build`)
- Page validation (`npm run validate:pages`)
- SHA-256 checksum verification
- Validation report artifact upload
- Deploy job with GitHub Environment protection (requires manual approval for `production` environment)

---

## Secret Requirements

| Secret | Purpose | Required for CI/CD? |
|---|---|---|
| `BROWSER_PROFILE` | Base64-encoded Playwright browser profile | Yes (for unattended export) |
| `SHAREPOINT_USERNAME` | M365 username | Not recommended (use profile) |
| `SHAREPOINT_PASSWORD` | M365 password | Not recommended (use profile) |

**Current Limitation**: Full unattended CI/CD export requires a pre-authenticated browser profile to be stored as a GitHub secret. This is not yet configured.

---

## Release Gates

| Gate | Check | Blocks Release? |
|---|---|---|
| Schema validation | Public export matches PXP-1 schema | Yes |
| Required-field validation | All contract fields present | Yes |
| Eligibility validation | Only eligible records exported | Yes |
| Visibility validation | No `internal`/`restricted` records in public output | Yes |
| Duplicate DocumentID validation | No duplicate IDs | Yes |
| Forbidden-field validation | No private/internal metadata | Yes |
| Record-count reconciliation | Live total = eligible + excluded | Yes |
| Build validation | Portal builds successfully | Yes |
| Pages validation | All portal pages render | Yes |
| Checksum verification | Export file matches its SHA-256 | Yes |
| **Deploy environment approval** | Manual approval in GitHub `production` environment | **Blocks deploy** |

---

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Export succeeded, all gates pass |
| 1 | Export failed or gate blocked |

---

## Artifacts

| Artifact | Path |
|---|---|
| Public export | `data/document-registry.public.json` |
| SHA-256 checksum | `data/document-registry.public.sha256` |
| Validation report | `reports/pxp3-validation-report.json` |

---

## Deploy Gates (PXP-3)

The deploy step is gated by three conditions:

1. **`dry_run` input must be `false`** — set this when triggering the workflow to enable deployment
2. **Export must exist** — `data/document-registry.public.json` must be present in the repository
3. **Validator must pass** — `npm run validate:public-registry` must exit with code 0

Additionally, the deploy job uses a GitHub **Environment** (`production`) which can require **manual approval** from designated reviewers before deployment proceeds. This is configured in the repository Settings > Environments.

---

## PXP-3 Pilot Results

The PXP-3 pilot updates ~24 records in the live Registry to `Visibility=Public` and produces a public export with ~24 eligible records.

### What changed in PXP-3

| Change | Detail |
|---|---|
| Workflow name | Updated to `PXP-3 Registry Export` |
| Validator | Uses dedicated `validate-public-export.py` via `npm run validate:public-registry` |
| Validation report | Auto-generated `reports/pxp3-validation-report.json` captured as CI artifact |
| Deploy gate | Separate `deploy` job with `environment: production` requiring manual approval |
| Inline Python checks | Removed — consolidated into the dedicated validator script |
| Schedule trigger | Removed — browser auth not available in CI |

### Validation pipeline (CI only — no M365 access)

```
checkout → npm ci → check export exists → validate:public-registry → checksum → build → validate:pages → (approve) → deploy
```

All validation steps operate on the committed `data/document-registry.public.json` file. No M365/SharePoint access is required.

---

## Future Entra ID Automation (Optional Enhancement)

To enable fully unattended CI/CD export (without browser profile), the pipeline can be upgraded to use **Entra ID (Azure AD) app-only authentication**:

1. Register an Entra ID application with SharePoint Online permissions
2. Store client ID and tenant ID as GitHub secrets
3. Use `msal` (Microsoft Authentication Library) to obtain token via client credentials flow
4. Replace Playwright browser login with REST API calls using the access token

This approach would:
- Eliminate the browser profile dependency
- Enable `schedule` triggers for periodic exports
- Work in any CI/CD environment without interactive login

Not implemented in PXP-3 — requires Entra ID admin consent and application registration.

---

## Manual Dispatch

```bash
# Trigger validate-only workflow (default — safe for testing)
gh workflow run registry-export.yml --ref main

# Trigger with deploy enabled (requires environment approval)
gh workflow run registry-export.yml --ref main -f dry_run=false
```

---

## Rollback

```bash
git checkout HEAD~1 -- data/document-registry.public.json
git commit -m "revert: rollback registry export to previous snapshot"
```
