# PXP-2 CI/CD Runbook

**Date**: 2026-07-16

---

## Workflow Structure

The PXP-2 export pipeline is designed for both local and CI/CD execution:

### Local Export

```bash
python scripts/registry/export-live-registry.py
```

This requires:
1. An initialized Playwright browser profile at `.browser-profile/m365/`
2. Python 3.14+ with `playwright` and `requests` packages
3. An authenticated M365 session (one-time interactive login)

### GitHub Actions Workflow

A `workflow_dispatch` workflow is provided at:

```yaml
.github/workflows/registry-export.yml
```

Features:
- `workflow_dispatch` trigger (manual dispatch)
- Optional `schedule` trigger for periodic exports
- Concurrency guard (one export at a time)
- Artifact upload for audit reports
- Build + validate steps
- No secret leakage

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
| Export audit | `reports/pxp2-export-audit.json` |
| Summary report | `reports/pxp2-export-summary.md` |

---

## Scheduled Execution

Not currently available due to browser profile dependency.

Recommended approach when ready:
1. Store Playwright profile as GitHub secret
2. Export profile on runner: `echo "${{ secrets.BROWSER_PROFILE }}" | base64 -d > profile.tar.gz && tar -xzf profile.tar.gz`
3. Run export script with headless mode
4. Commit results and deploy

---

## Manual Dispatch

```bash
# Trigger workflow via GitHub CLI
gh workflow run registry-export.yml --ref main
```

---

## Rollback

```bash
git checkout HEAD~1 -- data/document-registry.public.json
git commit -m "revert: rollback registry export to previous snapshot"
```
