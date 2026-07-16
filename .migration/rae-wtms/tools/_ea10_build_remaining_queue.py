#!/usr/bin/env python3
"""Co-worker A: Build completed IDs and remaining/retry queues from artifacts."""
import csv
import hashlib
import json
import os
from datetime import datetime, timezone

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
MANIFEST = os.path.join(r'G:\ProjectAI\document-center\migration', 'sharepoint-migration-manifest.csv')
EA6 = {'RAE-00009', 'RAE-00046', 'RAE-00146', 'RAE-00195', 'RAE-00662', 'RAE-00119'}


def load_ok_ids():
    ids = set(EA6)
    for path in [
        os.path.join(ROOT, 'pilot', 'ea-7a-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-9-results.csv'),
        os.path.join(EA10, 'ea-10-results.csv'),
    ]:
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r.get('UploadStatus') == 'OK' and r.get('SharePointURL') and r.get('RegistryItemID'):
                    ids.add(r['DocumentID'])
    return ids


def main():
    os.makedirs(EA10, exist_ok=True)
    completed = sorted(load_ok_ids(), key=lambda x: int(x.split('-')[1]))
    with open(os.path.join(EA10, 'ea-10-completed-ids.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(completed) + '\n')

    sel_path = os.path.join(EA10, 'ea-10-selection.csv')
    remaining = []
    retry = []
    if os.path.exists(sel_path):
        with open(sel_path, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r['DocumentID'] not in completed:
                    path = os.path.join(ROOT, r['LocalRelativePath'])
                    row = {**r, 'QueueReason': 'NOT_COMPLETE'}
                    if os.path.exists(path):
                        with open(path, 'rb') as fh:
                            sha = hashlib.sha256(fh.read()).hexdigest()
                        if sha != r['SHA256'].strip():
                            row['QueueReason'] = 'SHA_MISMATCH'
                    else:
                        row['QueueReason'] = 'MISSING_SOURCE'
                    remaining.append(row)

    res_path = os.path.join(EA10, 'ea-10-results.csv')
    if os.path.exists(res_path):
        with open(res_path, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r.get('UploadStatus') not in ('OK', '') and r.get('DocumentID'):
                    retry.append(r)

    rem_fields = list(remaining[0].keys()) if remaining else ['DocumentID', 'QueueReason']
    with open(os.path.join(EA10, 'ea-10-remaining-queue.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rem_fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(remaining)

    retry_fields = list(retry[0].keys()) if retry else ['DocumentID', 'UploadStatus', 'Error']
    with open(os.path.join(EA10, 'ea-10-retry-queue.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=retry_fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(retry)

    summary = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'completed_count': len(completed),
        'remaining_count': len(remaining),
        'retry_count': len(retry),
    }
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
