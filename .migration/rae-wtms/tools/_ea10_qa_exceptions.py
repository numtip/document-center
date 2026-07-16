#!/usr/bin/env python3
"""Co-worker B: Exception-only QA from artifacts + optional live evidence export."""
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')


def main():
    issues = []
    sel = {}
    if os.path.exists(os.path.join(EA10, 'ea-10-selection.csv')):
        with open(os.path.join(EA10, 'ea-10-selection.csv'), encoding='utf-8-sig') as f:
            sel = {r['DocumentID']: r for r in csv.DictReader(f)}

    res = []
    if os.path.exists(os.path.join(EA10, 'ea-10-results.csv')):
        with open(os.path.join(EA10, 'ea-10-results.csv'), encoding='utf-8-sig') as f:
            res = list(csv.DictReader(f))

    dup_ids = [k for k, v in Counter(r['DocumentID'] for r in res).items() if v > 1]
    if dup_ids:
        issues.append({'type': 'DUPLICATE_RESULT_ROWS', 'ids': dup_ids})

    broken = []
    for r in res:
        if r.get('UploadStatus') == 'OK':
            url = r.get('SharePointURL', '')
            if not url or '/sites/msteams_54adc4/sites/' in url:
                broken.append(r['DocumentID'])
            if not r.get('RegistryItemID'):
                issues.append({'type': 'MISSING_REGISTRY', 'id': r['DocumentID']})
            if sel.get(r['DocumentID']) and r.get('TargetLibrary') != sel[r['DocumentID']].get('TargetLibrary'):
                issues.append({'type': 'LIBRARY_MISMATCH', 'id': r['DocumentID']})

    if broken:
        issues.append({'type': 'BROKEN_URL', 'ids': broken})

    fail = [r for r in res if r.get('UploadStatus') not in ('OK', '')]
    if fail:
        issues.append({'type': 'UPLOAD_FAILURES', 'count': len(fail), 'ids': [r['DocumentID'] for r in fail]})

    ok = sum(1 for r in res if r.get('UploadStatus') == 'OK')
    expected = len(sel)
    drift = expected - ok
    if drift > 5:
        issues.append({'type': 'COUNT_DRIFT', 'expected': expected, 'ok': ok, 'drift': drift})

    critical = any(i['type'] in ('DUPLICATE_RESULT_ROWS', 'COUNT_DRIFT', 'LIBRARY_MISMATCH') for i in issues)
    if broken and len(broken) > 5:
        critical = True

    out = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'ea10_ok': ok,
        'ea10_expected': expected,
        'issues': issues,
        'gate': 'PAUSE' if critical else 'CONTINUE',
        'broken_url_count': len(broken),
        'duplicate_count': len(dup_ids),
    }

    with open(os.path.join(EA10, 'ea-10-qa-exceptions.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(json.dumps({k: out[k] for k in ('ea10_ok', 'ea10_expected', 'gate', 'broken_url_count', 'duplicate_count', 'issues')}, indent=2))
    sys.exit(1 if critical else 0)


if __name__ == '__main__':
    main()
