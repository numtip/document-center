# EA / M365 WORK PC Recovery Runbook

**Project:** RAE Document Center  
**Analyst:** Co-Work B (EA / M365 Recovery Analyst)  
**Date:** 2026-07-12  

---

## Purpose

One-time procedure to recover missing EA / M365 architecture artifacts from the WORK PC at `G:\ProjectAI\RAE-M365-Platform` and integrate them into the canonical GitHub repository at `numtip/document-center`.

**This is a one-time recovery operation, not a recurring process.**

---

## Prerequisites

| Requirement | Detail |
|-------------|--------|
| **WORK PC access** | Physical or Remote Desktop access to the WORK PC |
| **Canonical checkout** | `G:\ProjectAI\document-center` must exist (canonical clone) |
| **Recovery source** | `G:\ProjectAI\RAE-M365-Platform` must be accessible |
| **GitHub credentials** | Write access to `numtip/document-center` |
| **Git tooling** | `rtk` alias must be configured |
| **Node.js** | `npm` and `tsx` available for validation |
| **EA gap matrix** | Read `docs/architecture/EA_RECOVERY_GAP_MATRIX.md` first |
| **Recovery manifest** | Read `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md` for per-item guidance |

---

## Workflow

### Step 1: Verify canonical checkout on WORK PC

```pwsh
rtk git -C G:\ProjectAI\document-center status
```

Expected: `On branch main` and `nothing to commit, working tree clean`

If the checkout does not exist:
```pwsh
rtk git clone https://github.com/numtip/document-center.git G:\ProjectAI\document-center
```

### Step 2: Create recovery branch from clean main

```pwsh
rtk git -C G:\ProjectAI\document-center checkout main
rtk git -C G:\ProjectAI\document-center pull origin main
rtk git -C G:\ProjectAI\document-center checkout -b recovery/ea-m365-baseline
```

### Step 3: Inspect recovery source

Verify the WORK PC source directory exists:

```pwsh
rtk ls G:\ProjectAI\RAE-M365-Platform
```

If the directory does not exist, halt recovery and document the absence.

If it exists, create a full inventory:

```pwsh
rtk find G:\ProjectAI\RAE-M365-Platform -type f | sort > recovery-source-file-inventory.txt
rtk wc -l recovery-source-file-inventory.txt
```

### Step 4: Classify each discovered artifact

For each file/directory found in the recovery source, classify using the manifest at `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md`.

Use the classification table:

| Classification | Action |
|----------------|--------|
| IMPORT_AS_AUTHORITATIVE | Copy to canonical repo as-is |
| MERGE_WITH_EXISTING | Compare with existing, reconcile differences, merge |
| RETAIN_AS_HISTORICAL | Keep in recovery source, do not import |
| DO_NOT_IMPORT_DUPLICATE | Skip — already in canonical |
| REQUIRES_ADR_REVIEW | Do not import; create ADR first |

Record classifications:

```pwrtk
# Template for each artifact:
# [CLASSIFICATION] G:\ProjectAI\RAE-M365-Platform\{relative_path} → docs/document-center/{target}
```

### Step 5: Content comparison

For MERGE_WITH_EXISTING artifacts, run side-by-side comparison:

```pwsh
rtk diff --no-index "G:\ProjectAI\document-center\{canonical_path}" "G:\ProjectAI\RAE-M365-Platform\{source_path}"
```

For JSON files:
```pwsh
rtk diff <(rtk python -m json.tool "canonical.json") <(rtk python -m json.tool "source.json")
```

Document differences in a comparison log:
```pwsh
# Append to comparison log
# echo "=== Artifact: ... ===" >> recovery-comparison-log.md
# echo "Differences: ..." >> recovery-comparison-log.md
```

### Step 6: Controlled import — IMPORT_AS_AUTHORITATIVE artifacts

Copy authoritative artifacts to canonical branch:

```pwsh
rtk cp "G:\ProjectAI\RAE-M365-Platform\{source}" "G:\ProjectAI\document-center\docs\document-center\{target}"
```

### Step 7: Controlled import — MERGE_WITH_EXISTING artifacts

For artifacts that need merging:

1. Read the canonical version.
2. Read the WORK PC version.
3. Reconcile differences, preserving the best of both.
4. Write the merged version to the canonical checkout.

```pwsh
# Manual merge process — no automated merge tool
# Write merged content to canonical path
```

### Step 8: Validate all imported artifacts

After imports, run the full validation suite:

```pwsh
rtk npm --prefix G:\ProjectAI\document-center run validate:all
```

If validation fails, fix issues before proceeding.

### Step 9: Secret scan

Scan all imported files for secrets before commit:

```pwsh
rtk rg -i "password|secret|token|api_key|PRIVATE_KEY|BEGIN RSA|BEGIN OPENSSH|client_secret|tenant_id|connection_string" G:\ProjectAI\document-center --iglob '!.git' 2>&1
```

If secrets are detected, remove them and re-validate.

### Step 10: Commit recovery branch

```pwsh
rtk git -C G:\ProjectAI\document-center add -A
rtk git -C G:\ProjectAI\document-center commit -m "recovery: import EA/M365 architecture artifacts from WORK PC"
```

### Step 11: Push recovery branch

```pwsh
rtk git -C G:\ProjectAI\document-center push -u origin recovery/ea-m365-baseline
```

### Step 12: QC review checklist

Before creating pull request, verify:

| # | Check | Pass Criteria |
|---|-------|---------------|
| 1 | No broken paths | All imported paths exist and follow `docs/document-center/` or `scripts/` structure |
| 2 | Validators pass | `npm run validate:all` returns PASS |
| 3 | No secrets | Secret scan returns no findings |
| 4 | No binaries in Git | No `.pdf`, `.docx`, `.xlsx` files committed |
| 5 | All taxonomies valid | `taxonomy.json` references checked |
| 6 | Taxonomy v2 ADR exists | If v2 was imported, an ADR documents the migration from v1 |
| 7 | Registry schema consistent | Imported fields align with or extend REGISTRY_DATA_MODEL.md |
| 8 | Memory OS documented | If Memory OS artifacts found, location and purpose documented |
| 9 | Conflicts documented | Any conflicts between WORK PC and GitHub versions recorded in recovery report |
| 10 | Runbook final step done | See Step 14 below |

### Step 13: Create pull request

```pwsh
rtk gh pr create --title "recovery: EA/M365 architecture baseline from WORK PC" --body "$(cat <<'EOF'
## Summary

Recovery of EA/M365 architecture artifacts from WORK PC source at G:\ProjectAI\RAE-M365-Platform.

## Artifacts recovered

[List imported artifacts with classifications]

## Validation

- npm run validate:all: PASS/FAIL
- Secret scan: CLEAN/FLAGGED

## Architecture decisions required

[ADRs needed before merge]

EOF
)"
```

### Step 14: Retire WORK PC as active source

After successful merge:

```pwsh
# Rename to prevent accidental future use
rtk mv G:\ProjectAI\RAE-M365-Platform G:\ProjectAI\RAE-M365-Platform.RECOVERED.2026-07-12

# Or archive
# rtk tar -czf G:\ProjectAI\RAE-M365-Platform.RECOVERED.tar.gz G:\ProjectAI\RAE-M365-Platform
# rtk rm -rf G:\ProjectAI\RAE-M365-Platform
```

---

## Quick Reference

### All terminal commands (sequential execution)

```pwsh
# 1. Verify canonical checkout
rtk git -C G:\ProjectAI\document-center status

# 2. Create recovery branch
rtk git -C G:\ProjectAI\document-center checkout main
rtk git -C G:\ProjectAI\document-center pull origin main
rtk git -C G:\ProjectAI\document-center checkout -b recovery/ea-m365-baseline

# 3. Inspect recovery source
rtk ls G:\ProjectAI\RAE-M365-Platform
rtk find G:\ProjectAI\RAE-M365-Platform -type f | sort

# 4-7. Manual classification, comparison, and import

# 8. Validate
rtk npm --prefix G:\ProjectAI\document-center run validate:all

# 9. Secret scan
rtk rg -i "password|secret|token|api_key|PRIVATE_KEY|BEGIN RSA|BEGIN OPENSSH|client_secret|tenant_id|connection_string" G:\ProjectAI\document-center --iglob '!.git'

# 10. Commit
rtk git -C G:\ProjectAI\document-center add -A
rtk git -C G:\ProjectAI\document-center commit -m "recovery: import EA/M365 architecture artifacts from WORK PC"

# 11. Push
rtk git -C G:\ProjectAI\document-center push -u origin recovery/ea-m365-baseline

# 14. Retire source
rtk mv G:\ProjectAI\RAE-M365-Platform G:\ProjectAI\RAE-M365-Platform.RECOVERED.2026-07-12
```

### Error recovery

| Error | Action |
|-------|--------|
| WORK PC source not found | Document absence. Note: `G:\ProjectAI\RAE-M365-Platform` does not exist. Recovery impossible without source. |
| Canonical checkout not found | Clone: `rtk git clone https://github.com/numtip/document-center.git G:\ProjectAI\document-center` |
| Validation fails | Fix issues, re-validate, do not commit failing state |
| Secrets detected | Remove secrets from files, re-scan, then proceed |
| Merge conflicts (git) | Resolve manually. If conflicts span critical architecture decisions, escalate to Architecture Review. |
| PnP scripts reference different M365 tenant | Redact tenant-specific values before import. Record tenant context in ADR. |
| Taxonomy v2 incompatible with v1 | Do not import. Create ADR documenting the incompatibility. Re-concile taxonomy strategy before merge. |
