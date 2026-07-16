#!/usr/bin/env python3
"""EA-11 public access tests from artifact URLs (no browser)."""
import csv
import json
import os
import random
import urllib.request

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA11 = os.path.join(ROOT, 'ea-11')
LIBS = ['Administration', 'FinanceProcurement', 'PlanningPolicy', 'AcademicServices', 'SOPManuals', 'Research']


def load_all_results():
    rows = []
    for path in [
        os.path.join(ROOT, 'pilot', 'ea-6b-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-7a-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-9-results.csv'),
        os.path.join(ROOT, 'ea-10', 'ea-10-results.csv'),
    ]:
        if os.path.exists(path):
            rows.extend(list(csv.DictReader(open(path, encoding='utf-8-sig'))))
    ok = {}
    for r in rows:
        if r.get('UploadStatus') in ('OK', 'UPLOADED_OK') and r.get('DocumentID'):
            ok[r['DocumentID']] = r
    return ok


def head_url(url):
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, 'PUBLIC_PASS' if resp.status < 400 else 'BROKEN'
    except urllib.error.HTTPError as e:
        return e.code, 'AUTH_REQUIRED' if e.code in (401, 403) else 'BROKEN'
    except Exception:
        return 0, 'TIMEOUT'


def main():
    os.makedirs(EA11, exist_ok=True)
    ok = load_all_results()
    by_lib = {lib: [] for lib in LIBS}
    for r in ok.values():
        by_lib.setdefault(r.get('TargetLibrary', ''), []).append(r)
    random.seed(11)
    picks = []
    seen = set()
    for lib in LIBS:
        for r in random.sample(by_lib.get(lib, []), min(10, len(by_lib.get(lib, [])))):
            if r['DocumentID'] not in seen:
                picks.append(r)
                seen.add(r['DocumentID'])

    results = []
    for r in picks:
        rel = r.get('SharePointURL', '')
        url = ('https://maejo365.sharepoint.com' + rel) if rel.startswith('/') else rel
        code, anon = head_url(url)
        results.append({
            'DocumentID': r['DocumentID'],
            'TargetLibrary': r.get('TargetLibrary', ''),
            'StorageURL': url,
            'AnonymousAccess': anon,
            'HttpStatus': code,
            'BadDuplicatePath': '/sites/msteams_54adc4/sites/' in url,
        })

    with open(os.path.join(EA11, 'ea-11-public-access-tests.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()) if results else ['DocumentID'])
        w.writeheader()
        w.writerows(results)

    summary = {
        'sampled': len(results),
        'anon_pass': sum(1 for x in results if x['AnonymousAccess'] == 'PUBLIC_PASS'),
        'auth_required': sum(1 for x in results if x['AnonymousAccess'] == 'AUTH_REQUIRED'),
        'broken': sum(1 for x in results if x['AnonymousAccess'] == 'BROKEN'),
        'note': 'Tenant policy requires auth for anonymous HEAD; expected AUTH_REQUIRED',
    }
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
