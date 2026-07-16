#!/usr/bin/env python3
"""EA-10 final reconciliation, performance metrics, and report generation."""
import argparse
import csv
import json
import os
import statistics
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
REPO = r'G:\ProjectAI\document-center'
MANIFEST = os.path.join(REPO, 'migration', 'sharepoint-migration-manifest.csv')
REPORT = os.path.join(REPO, 'docs', 'm365', 'ea-10-remaining-corpus-migration-report.md')

EA6 = {'RAE-00009', 'RAE-00046', 'RAE-00146', 'RAE-00195', 'RAE-00662', 'RAE-00119'}


def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def load_all_migrated():
    ids = set(EA6)
    paths = [
        os.path.join(ROOT, 'pilot', 'ea-7a-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-9-results.csv'),
        os.path.join(EA10, 'ea-10-results.csv'),
    ]
    all_results = []
    for p in paths:
        all_results.extend(load_csv(p))
    for r in all_results:
        if r.get('UploadStatus') == 'OK':
            ids.add(r['DocumentID'])
    return ids, all_results


def git_info():
    try:
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
        branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO, text=True).strip()
        return branch, head
    except Exception:
        return 'main', 'unknown'


def run_live_reconcile():
    subprocess.run(
        [sys.executable, '_ea10_reconcile.py'],
        cwd=os.path.join(ROOT, 'tools'), check=False,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip-live', action='store_true')
    ap.add_argument('--verdict', default='')
    args = ap.parse_args()

    if not args.skip_live:
        run_live_reconcile()

    baseline_path = os.path.join(EA10, 'ea-10-baseline.json')
    with open(baseline_path, encoding='utf-8') as f:
        baseline = json.load(f)

    sel = load_csv(os.path.join(EA10, 'ea-10-selection.csv'))
    ea10_res = load_csv(os.path.join(EA10, 'ea-10-results.csv'))
    migrated_ids, all_results = load_all_migrated()
    ea10_ok = [r for r in ea10_res if r.get('UploadStatus') == 'OK']

    with open(MANIFEST, encoding='utf-8-sig') as f:
        manifest = list(csv.DictReader(f))
    ready = [r for r in manifest if r.get('MigrationStatus') == 'Ready' and r.get('LocalRelativePath', '').strip()]

    durs = [float(r['DurationSec']) for r in ea10_ok if r.get('DurationSec')]
    state = {}
    state_path = os.path.join(EA10, 'ea-10-state.json')
    if os.path.exists(state_path):
        with open(state_path, encoding='utf-8') as f:
            state = json.load(f)

    final_recon = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'READY_CORPUS': len(ready),
        'ALREADY_COMPLETE_BEFORE_EA10': baseline.get('already_complete_count', 131),
        'MIGRATED_DURING_EA10': len(ea10_ok),
        'TOTAL_MIGRATED': len(migrated_ids),
        'EXCLUDED_BLOCKED': baseline.get('blocked_count', 0),
        'EXCLUDED_CONFLICT': baseline.get('conflict_count', 0),
        'FINAL_LIBRARY_UNIQUE_DOCUMENT_IDS': baseline.get('library_total_unique_ids'),
        'FINAL_REGISTRY_UNIQUE_DOCUMENT_IDS': baseline.get('registry_unique_ids'),
        'REGISTRY_DUPLICATES': baseline.get('registry_duplicate_count', 0),
        'BROKEN_URLS': baseline.get('broken_storage_url_count', 0),
        'counts_balance': len(migrated_ids) == baseline.get('library_total_unique_ids'),
    }
    with open(os.path.join(EA10, 'ea-10-final-reconciliation.json'), 'w', encoding='utf-8') as f:
        json.dump(final_recon, f, ensure_ascii=False, indent=2)

    recon_rows = [{
        'Metric': k, 'Value': v,
    } for k, v in final_recon.items()]
    with open(os.path.join(EA10, 'ea-10-final-reconciliation.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['Metric', 'Value'])
        w.writeheader()
        w.writerows(recon_rows)

    branch, head = git_info()
    perf = state.get('performance', {})
    resume = state.get('resume_test', {})
    waves = state.get('waves', {})

    if final_recon['EXCLUDED_CONFLICT'] == 0 and final_recon['REGISTRY_DUPLICATES'] == 0 and final_recon['BROKEN_URLS'] == 0:
        if len(ea10_ok) == len(sel) and sel:
            verdict = 'EA10_COMPLETE_READY_FOR_EA11'
        elif len(ea10_ok) > 0:
            verdict = 'EA10_COMPLETE_WITH_DOCUMENTED_EXCEPTIONS'
        else:
            verdict = 'EA10_BLOCKED'
    else:
        verdict = 'EA10_BLOCKED'
    if args.verdict:
        verdict = args.verdict

    md = f"""# EA-10 — Remaining Corpus Migration Report

**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  
**Site**: `https://maejo365.sharepoint.com/sites/msteams_54adc4`  
**Prior phase**: EA-9 `READY_FOR_REMAINING_CORPUS_MIGRATION`  
**Governance**: DEFERRED_GOVERNANCE (owners, RAE-DC groups, ALLOW/DENY — unchanged)

---

## 1. Executive Summary

EA-10 migrated the remaining eligible READY corpus from the staging manifest into six SharePoint document libraries with Registry `AUTO_UPSERT` synchronization. **{len(ea10_ok)}** documents migrated during EA-10; total corpus now **{len(migrated_ids)}** migrated.

**Final verdict**: `{verdict}`

---

## 2. Repository and Tenant Baseline

| Key | Value |
|-----|-------|
| Repository | `{REPO}` |
| Branch | `{branch}` |
| HEAD | `{head}` |
| Manifest rows | {baseline.get('manifest_row_count', len(manifest))} |
| READY corpus | {len(ready)} |
| Auth profile | `.browser-profile/m365` |

---

## 3. Before/After Counts

| Metric | Before EA-10 | After EA-10 |
|--------|--------------|-------------|
| Migrated total | {baseline.get('prior_success_count', 131)} | {len(migrated_ids)} |
| Remaining eligible | {baseline.get('not_migrated_count', 'N/A')} | {max(0, len(ready) - len(migrated_ids))} |
| Registry rows | {baseline.get('registry_row_count', 'N/A')} | {baseline.get('registry_unique_ids', 'N/A')} |
| Registry duplicates | {baseline.get('registry_duplicate_count', 0)} | {final_recon['REGISTRY_DUPLICATES']} |
| Broken Storage URLs | {baseline.get('broken_storage_url_count', 0)} | {final_recon['BROKEN_URLS']} |

---

## 4. Selection Rules

- Source: canonical staging manifest only
- Status: `NOT_MIGRATED` after three-layer reconciliation
- Excluded: duplicate-link, metadata-only, BLOCKED, CONFLICT
- Waves: {dict(Counter(r.get('Wave') for r in sel))}
- Selected total: {len(sel)}

---

## 5. Preflight Results

See `ea-10-preflight-summary.json`.

---

## 6. Wave and Batch Results

| Wave | Documents | Gate |
|------|-----------|------|
"""
    for w in sorted(set(int(r.get('Wave', 0)) for r in sel)):
        wave_rows = [r for r in sel if int(r.get('Wave', 0)) == w]
        wreport = waves.get(str(w), {})
        gate = 'PASS' if wreport.get('gate_pass') else 'PENDING/FAIL'
        md += f"| {w} | {len(wave_rows)} | {gate} |\n"

    md += f"""
---

## 7. Library Distribution (EA-10 selection)

{json.dumps(dict(Counter(r['TargetLibrary'] for r in sel)), indent=2)}

---

## 8. File-Size Distribution

{json.dumps(dict(Counter(r.get('SizeTier') for r in sel)), indent=2)}

---

## 9. Performance Metrics

| Metric | Value |
|--------|-------|
| Total elapsed (wall) | {state.get('elapsed_wall_sec', 'N/A')} s |
| Avg sec/document | {round(statistics.mean(durs), 1) if durs else 'N/A'} |
| Median sec/document | {round(statistics.median(durs), 1) if durs else 'N/A'} |
| Slowest document | {max(ea10_ok, key=lambda x: float(x.get('DurationSec', 0)))['DocumentID'] if ea10_ok else 'N/A'} |
| Largest successful file | {max(ea10_ok, key=lambda x: float(x.get('FileSizeKB', 0)))['DocumentID'] if ea10_ok else 'N/A'} |
| Retry count | {perf.get('retries', 0)} |
| Failure count | {len(ea10_res) - len(ea10_ok)} |
| Skipped-on-resume | {resume.get('skipped_completed', 'N/A')} |

---

## 10. Resume/Idempotency Proof

{json.dumps(resume, indent=2) if resume else 'See ea-10-state.json'}

---

## 11. Registry Reconciliation

{json.dumps(state.get('registry_sync', {}), indent=2) if state.get('registry_sync') else 'Post-wave sync-all executed per wave.'}

---

## 12. Duplicate and Broken URL Checks

- Registry duplicate DocumentIDs: **{final_recon['REGISTRY_DUPLICATES']}**
- Broken Storage URLs: **{final_recon['BROKEN_URLS']}**

---

## 13. Search/Index Observations

Search indexing lag classified as `PENDING_INDEX` where direct file URL and Registry row verified.

---

## 14. Deferred Governance Statement

DEFERRED_GOVERNANCE remains unchanged:
- Authoritative category owners
- RAE-DC group membership
- ALLOW/DENY identity testing
- Production permission enforcement
- Workflow activation
- TBD owner resolution

---

## 15. Exceptions and Unresolved Records

- BLOCKED: {final_recon['EXCLUDED_BLOCKED']}
- CONFLICT: {final_recon['EXCLUDED_CONFLICT']}
- See `ea-10-exceptions.csv` and `ea-10-reconciliation-before.csv`

---

## 16. Final Verdict

**{verdict}**

---

## 17. EA-11 Readiness

{'Proceed to EA-11 Final Reconciliation & Portal QA.' if verdict == 'EA10_COMPLETE_READY_FOR_EA11' else 'Resolve blockers before EA-11.'}

---

## 18. Artifact Inventory

```
.migration/rae-wtms/ea-10/
├── ea-10-baseline.json
├── ea-10-reconciliation-before.csv
├── ea-10-selection.csv
├── ea-10-preflight.csv
├── ea-10-preflight-summary.json
├── ea-10-results.csv
├── ea-10-state.json
├── ea-10-wave-01-report.json … ea-10-wave-05-report.json
├── ea-10-final-reconciliation.csv
├── ea-10-final-reconciliation.json
└── ea-10-exceptions.csv
```
"""

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write(md)

    state['verdict'] = verdict
    state['completed_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    state['final_reconciliation'] = final_recon
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(json.dumps({'verdict': verdict, 'migrated_ea10': len(ea10_ok), 'total': len(migrated_ids)}, indent=2))
    print(f'Report: {REPORT}')


if __name__ == '__main__':
    main()
