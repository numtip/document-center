#!/usr/bin/env python3
"""EA-10: Select all remaining NOT_MIGRATED READY documents in wave/batch structure."""
import csv
import hashlib
import json
import os
from collections import Counter

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
MANIFEST = os.path.join(r'G:\ProjectAI\document-center\migration', 'sharepoint-migration-manifest.csv')
RECON = os.path.join(EA10, 'ea-10-reconciliation-before.csv')
OUT = os.path.join(EA10, 'ea-10-selection.csv')
SUMMARY = os.path.join(EA10, 'ea-10-selection-summary.json')

EA6 = {'RAE-00009', 'RAE-00046', 'RAE-00146', 'RAE-00195', 'RAE-00662', 'RAE-00119'}
WAVE_SIZE = 100
BATCH_SIZE = 10

CAT_MAP = {
    'Administration': 'admin',
    'FinanceProcurement': 'finance-procurement',
    'Research': 'research',
    'AcademicServices': 'academic-service',
    'PlanningPolicy': 'policy-planning',
    'SOPManuals': 'manuals',
}


def load_migrated():
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
                if r.get('UploadStatus') == 'OK':
                    ids.add(r['DocumentID'])
    return ids


def file_info(path):
    if not os.path.exists(path):
        return None
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if size < 50_000:
        tier = 'small'
    elif size < 1_000_000:
        tier = 'medium'
    elif size < 5_000_000:
        tier = 'large'
    else:
        tier = 'xlarge'
    return size, sha, tier


def load_not_migrated_ids():
    if os.path.exists(RECON):
        with open(RECON, encoding='utf-8-sig') as f:
            return {r['DocumentID'] for r in csv.DictReader(f) if r['Status'] == 'NOT_MIGRATED'}
    migrated = load_migrated()
    with open(MANIFEST, encoding='utf-8-sig') as f:
        return {
            r['DocumentID'] for r in csv.DictReader(f)
            if r.get('MigrationStatus') == 'Ready'
            and r.get('LocalRelativePath', '').strip()
            and r['DocumentID'] not in migrated
        }


def distribute_batch(pool, batch_size):
    """Pick documents with size diversity within a batch."""
    if len(pool) <= batch_size:
        return pool[:]
    tiers = {'small': [], 'medium': [], 'large': [], 'xlarge': []}
    for x in pool:
        tiers[x['_tier']].append(x)
    picks, seen = [], set()

    def take(lst, n):
        for x in lst:
            if x['DocumentID'] in seen:
                continue
            picks.append(x)
            seen.add(x['DocumentID'])
            if len(picks) >= n:
                return

    take(tiers['xlarge'], min(2, batch_size))
    take(tiers['large'], min(max(2, batch_size // 5), batch_size))
    take(tiers['medium'], batch_size)
    take(tiers['small'], batch_size)
    for x in sorted(pool, key=lambda z: (z['_tier'], z['_size'])):
        if x['DocumentID'] not in seen:
            picks.append(x)
            seen.add(x['DocumentID'])
        if len(picks) >= batch_size:
            break
    return picks[:batch_size]


def main():
    os.makedirs(EA10, exist_ok=True)
    not_migrated = load_not_migrated_ids()
    with open(MANIFEST, encoding='utf-8-sig') as f:
        manifest = {r['DocumentID']: r for r in csv.DictReader(f)}

    candidates = []
    for doc_id in sorted(not_migrated, key=lambda x: int(x.split('-')[1])):
        r = manifest.get(doc_id)
        if not r:
            continue
        path = os.path.join(ROOT, r['LocalRelativePath'])
        info = file_info(path)
        if not info:
            continue
        size, sha, tier = info
        if sha != (r.get('SHA256') or '').strip():
            continue
        candidates.append({**r, '_size': size, '_tier': tier})

    # Build waves: up to 100 docs, 10 batches of 10
    out_rows = []
    seq = 0
    wave = 0
    remaining = candidates[:]
    while remaining:
        wave += 1
        wave_pool = remaining[:WAVE_SIZE]
        remaining = remaining[WAVE_SIZE:]
        batch_num = 0
        wave_rest = wave_pool[:]
        while wave_rest:
            batch_num += 1
            batch_tag = f'EA10-W{wave:02d}-B{batch_num:02d}'
            batch_items = distribute_batch(wave_rest, BATCH_SIZE)
            batch_ids = {x['DocumentID'] for x in batch_items}
            wave_rest = [x for x in wave_rest if x['DocumentID'] not in batch_ids]
            for x in batch_items:
                seq += 1
                lib = x['TargetLibrary']
                out_rows.append({
                    'Wave': wave,
                    'Batch': batch_num,
                    'BatchTag': batch_tag,
                    'BatchID': batch_tag,
                    'Sequence': seq,
                    'DocumentID': x['DocumentID'],
                    'Title': x.get('Title', ''),
                    'TargetLibrary': lib,
                    'SourceFile': os.path.basename(x['LocalRelativePath']),
                    'SHA256': x['SHA256'],
                    'FileSizeBytes': x['_size'],
                    'FileSize': x['_size'],
                    'FileSizeKB': round(x['_size'] / 1024, 1),
                    'SizeTier': x['_tier'],
                    'ManifestStatus': x.get('MigrationStatus', 'Ready'),
                    'PreflightStatus': 'PENDING',
                    'MigrationStatus': 'PENDING',
                    'RegistryStatus': 'PENDING',
                    'StorageURL': '',
                    'Error': '',
                    'ContentType': 'RAE Legacy Document',
                    'Category': x.get('Category', ''),
                    'Subcategory': x.get('Subcategory', ''),
                    'Owner': 'TBD',
                    'Status': x.get('Status', 'LegacyImported'),
                    'Visibility': x.get('PublicVisibility', 'PendingReview'),
                    'SourceURL': x.get('SourceURL', ''),
                    'LocalRelativePath': x['LocalRelativePath'],
                    'RegistryCategory': CAT_MAP.get(lib, ''),
                    'MigrationMethod': 'playwright-rest',
                    'UploadStatus': 'PENDING',
                    'MetadataStatus': 'PENDING',
                    'RetryCount': '0',
                    'FinalStatus': 'PENDING',
                    'RollbackStatus': 'PENDING',
                    'SelectionReason': f'EA-10 {x["_tier"]} {lib}',
                })

    fields = list(out_rows[0].keys()) if out_rows else []
    with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    summary = {
        'selected_total': len(out_rows),
        'waves': dict(Counter(r['Wave'] for r in out_rows)),
        'by_library': dict(Counter(r['TargetLibrary'] for r in out_rows)),
        'by_tier': dict(Counter(r['SizeTier'] for r in out_rows)),
        'by_extension': dict(Counter(
            os.path.splitext(r['SourceFile'])[1].lower() for r in out_rows
        )),
    }
    with open(SUMMARY, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f'Selected {len(out_rows)} -> {OUT}')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
