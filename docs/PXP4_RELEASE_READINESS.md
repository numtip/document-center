# PXP-4 Release Readiness Checklist

**Date**: 2026-07-16
**Repository**: G:\ProjectAI\document-center
**Branch**: `main`

---

## CI/CD Pipeline Readiness

### Workflow: `registry-export.yml` (`PXP-4 Registry Export`)

| Check | Status | Detail |
|---|---|---|
| Workflow name updated to PXP-4 | ✅ | `PXP-4 Registry Export` |
| Commit message reflects PXP-4 | ✅ | `deploy: pxp-4 registry export` |
| Validation report path points to PXP-4 | ✅ | `reports/pxp4-validation-report.json` |
| Artifact name updated to PXP-4 | ✅ | `pxp4-validation-artifacts` |
| Pipeline metadata tag updated | ✅ | `pxp4-ci-validate` |
| No browser auth in CI | ✅ | Workflow operates on static committed file only |
| No cookie-based SharePoint login | ✅ | No M365/SharePoint calls in CI |
| No real credentials in workflow | ✅ | Only `secrets.GITHUB_TOKEN` (auto-injected by Actions) |
| Concurrency guard | ✅ | One export at a time |
| Validate job timeout | ✅ | 15 min (fine for ~124 records) |
| Deploy job timeout | ✅ | 10 min (fine for build + deploy) |

### Validation Pipeline (CI Only — No M365 Access)

```
checkout → npm ci → check export exists → validate:public-registry → checksum → build → validate:pages → (approve) → deploy
```

All steps operate on the committed `data/document-registry.public.json`. No M365/SharePoint access required.

---

## Export Validation Gates

| Gate | Check | Pass/Fail | Blocks Release? |
|---|---|---|---|
| Schema version | Export matches `schemaVersion: "1.0.0"` | ☐ | Yes |
| Preview mode | `preview_mode` must be `false` | ☐ | Yes |
| Record count | `recordCount` matches `documents.length` | ☐ | Yes |
| Required fields | All contract fields present per document | ☐ | Yes |
| Status validation | Status ∈ {approved, published, current} | ☐ | Yes |
| Visibility validation | Visibility = `public` only | ☐ | Yes |
| Category validation | Category ∈ allowed set | ☐ | Yes |
| Download mode validation | DownloadMode ∈ allowed set | ☐ | Yes |
| Storage URL | HTTPS only | ☐ | Yes |
| UpdatedDate | Valid date string ≥ 10 chars | ☐ | Yes |
| Duplicate IDs | No duplicate DocumentIDs | ☐ | Yes |
| Forbidden fields | No private/internal metadata fields | ☐ | Yes |
| Deterministic ordering | Documents sorted by DocumentID | ☐ | Warning |
| SHA-256 checksum | File matches its committed checksum | ☐ | Yes |
| Build | Portal builds without errors | ☐ | Yes |
| Pages validation | All portal pages render correctly | ☐ | Yes |

---

## Deploy Gates

| Gate | Condition | Blocks Release? |
|---|---|---|
| Dry-run flag | `dry_run` must be `false` | Yes |
| Export exists | `data/document-registry.public.json` present | Yes |
| Validator passes | `npm run validate:public-registry` exits 0 | Yes |
| Environment approval | Manual approval in GitHub `production` environment required | Yes |

---

## Pre-Release Checks (Manual)

### Export File

- [ ] `data/document-registry.public.json` contains ~124 records (PXP-4 target)
- [ ] All ~124 records have `Visibility: "public"`
- [ ] No `internal` or `restricted` records leaked into public export
- [ ] Record count matches live registry eligible count
- [ ] No unexpected categories present
- [ ] All `StorageURL` values are valid HTTPS URLs
- [ ] All `DownloadMode` values are appropriate (AUTHENTICATED_SHAREPOINT, PUBLIC_SHAREPOINT_LINK, or PUBLIC_DISTRIBUTION_URL)
- [ ] SHA-256 checksum committed alongside export (`data/document-registry.public.sha256`)
- [ ] Preview data sample at `dist/preview/data/public-registry.sample.json` updated (3 records, `preview_mode: true`)
- [ ] Export generated from verified PXP-3/PXP-4 batch-marked records only
- [ ] Reconciliation confirmed: `total live = eligible + excluded`

### Runbook

- [ ] `docs/PXP2_CICD_RUNBOOK.md` updated to reference PXP-4 where applicable
- [ ] No CI/CD secrets or credentials referenced in runbook that are not actually configured

### Workflow

- [ ] Trigger dry-run validation before enabling deploy:
  ```bash
  gh workflow run registry-export.yml --ref main
  ```
- [ ] For full deploy:
  ```bash
  gh workflow run registry-export.yml --ref main -f dry_run=false
  ```
- [ ] Verify GitHub `production` environment approval gate is configured in repository Settings > Environments
- [ ] Approve the deploy job in the GitHub Actions UI when prompted

### Security

- [ ] CI workflow contains no Playwright browser profile secrets
- [ ] CI workflow contains no SharePoint/M365 credentials
- [ ] CI workflow contains no hardcoded secrets or tokens
- [ ] Only `GITHUB_TOKEN` (auto-injected) used for deployment

### Post-Deploy

- [ ] Validate deployed site at https://maejo365.github.io/document-center/
- [ ] Confirm public registry renders all ~124 records
- [ ] Confirm preview section shows correct sampled records
- [ ] Confirm download links are functional
- [ ] Verify no regression in existing pages (architecture, standards, ADR, roadmap, release, operations)

---

## Rollback Plan

```bash
# Restore previous export
git checkout HEAD~1 -- data/document-registry.public.json data/document-registry.public.sha256
git commit -m "revert: rollback registry export to previous snapshot"
git push origin main
```

Or revert the deploy commit on `gh-pages` branch directly if immediate rollback is needed.

---

## Blocker Summary

| Blocker | Severity | Owner | Notes |
|---|---|---|---|
| No current blocker identified | — | — | All CI/CD gates are static-file-based and validated |
| Export must be regenerated with ~124 public records | Required | Worker E | Requires local M365 auth to run `export-live-registry.py` |
| Preview sample needs updating | Required | Worker E | After new export generated, update preview data |
| Runbook references still say PXP-3 | Low | Worker E | Update `docs/PXP2_CICD_RUNBOOK.md` post-release |

---

## Recommended Next Action

1. **Regenerate** the public export locally (`python scripts/registry/export-live-registry.py`) with all ~124 PXP-4 records marked public
2. **Commit** the updated `data/document-registry.public.json` and `data/document-registry.public.sha256`
3. **Update** preview data sample at `dist/preview/data/public-registry.sample.json`
4. **Trigger** dry-run workflow to validate
5. **Resolve** any validation failures
6. **Trigger** deploy workflow (`dry_run=false`) and approve in GitHub Environments
7. **Verify** post-deployment
