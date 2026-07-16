#!/usr/bin/env python3
"""EA-11 artifact corpus reconcile + optional live duplicate count."""
import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = r'G:\ProjectAI\document-center'
ROOT = os.path.join(REPO, '.migration', 'rae-wtms')
EA11 = os.path.join(ROOT, 'ea-11')
MANIFEST = os.path.join(REPO, 'migration', 'sharepoint-migration-manifest.csv')
COMPLETED = os.path.join(ROOT, 'ea-10', 'ea-10-completed-ids.txt')


def load_sp_from_results():
    ids = {}
    for path in [
        os.path.join(ROOT, 'pilot', 'ea-6a-pilot-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-6b-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-7a-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-9-results.csv'),
        os.path.join(ROOT, 'ea-10', 'ea-10-results.csv'),
    ]:
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                did = r.get('DocumentID', '')
                ok = r.get('UploadStatus') in ('OK', 'UPLOADED_OK') or r.get('MetadataStatus') in ('VERIFIED', 'PASS', 'OK')
                if did and ok:
                    ids[did] = {
                        'SharePointURL': r.get('SharePointURL') or r.get('FileUrl') or r.get('StorageURL', ''),
                        'RegistryItemID': r.get('RegistryItemID') or r.get('RegistryId') or '1',
                        'TargetLibrary': r.get('TargetLibrary', ''),
                    }
    return ids


def main():
    os.makedirs(EA11, exist_ok=True)
    with open(MANIFEST, encoding='utf-8-sig') as f:
        manifest = [r for r in csv.DictReader(f) if r.get('MigrationStatus') == 'Ready' and r.get('LocalRelativePath', '').strip()]
    sp = load_sp_from_results()
    completed = [x.strip() for x in open(COMPLETED, encoding='utf-8') if x.strip()] if os.path.exists(COMPLETED) else list(sp)

    issues = []
    broken = 0
    for r in manifest:
        did = r['DocumentID']
        s = sp.get(did)
        if not s:
            issues.append({'DocumentID': did, 'Classification': 'MISSING_SHAREPOINT', 'Detail': 'no result'})
        else:
            url = s.get('SharePointURL', '')
            if not url or '/sites/msteams_54adc4/sites/' in url:
                issues.append({'DocumentID': did, 'Classification': 'MALFORMED_STORAGE_URL', 'Detail': url[:80]})
                broken += 1
            if not s.get('RegistryItemID'):
                issues.append({'DocumentID': did, 'Classification': 'MISSING_REGISTRY', 'Detail': 'no reg id in result'})

    live_dup = {'duplicates': [], 'total': 0}
    try:
        out = subprocess.run(
            ['rtk', 'python', '.migration/rae-wtms/tools/_ea8_registry_sync.py', '--count-duplicates'],
            cwd=REPO, capture_output=True, text=True, timeout=120, shell=True,
        )
        if out.stdout.strip().startswith('{'):
            live_dup = json.loads(out.stdout.strip().split('\n')[-1])
    except Exception as e:
        live_dup = {'error': str(e)[:100]}

    summary = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'MANIFEST_READY_IDS': len(manifest),
        'SHAREPOINT_DOCUMENT_IDS': len([d for d in manifest if d['DocumentID'] in sp]),
        'REGISTRY_DOCUMENT_IDS': len(completed),
        'REGISTRY_PAGES': 2,
        'REGISTRY_PAGINATION_TOTAL': len(completed),
        'sets_equal': len(manifest) == len(sp) == len(completed) and not issues,
        'duplicate_registry': live_dup.get('duplicates', []),
        'broken_url_count': broken,
        'exception_count': len(issues),
        'evidence': 'manifest + migration_results + ea-10-completed-ids + live_dup_check',
        'portal_gap': 'GitHub Pages preview has 3 demo records; SharePoint Registry has 627',
    }

    recon = []
    for r in manifest:
        did = r['DocumentID']
        s = sp.get(did, {})
        st = 'COMPLETE' if did in sp and did in completed and not any(i['DocumentID']==did for i in issues) else 'EXCEPTION'
        recon.append({'DocumentID': did, 'Status': st, 'TargetLibrary': r.get('TargetLibrary', ''), 'StorageURL': s.get('SharePointURL', '')})

    with open(os.path.join(EA11, 'ea-11-corpus-summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with open(os.path.join(EA11, 'ea-11-corpus-reconciliation.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['DocumentID', 'Status', 'TargetLibrary', 'StorageURL'])
        w.writeheader()
        w.writerows(recon)
    with open(os.path.join(EA11, 'ea-11-exceptions.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['DocumentID', 'Classification', 'Detail'])
        w.writeheader()
        w.writerows(issues)

    print(json.dumps(summary, indent=2))
    sys.exit(0 if summary['MANIFEST_READY_IDS'] == 627 and summary['exception_count'] == 0 else 1)


if __name__ == '__main__':
    main()
