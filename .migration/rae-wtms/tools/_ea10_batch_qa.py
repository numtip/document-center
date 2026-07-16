#!/usr/bin/env python3
"""EA-10 per-batch QA gate with wave support."""
import argparse
import csv
import json
import os
import sys
from collections import Counter

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
SEL = os.path.join(EA10, 'ea-10-selection.csv')
RES = os.path.join(EA10, 'ea-10-results.csv')
STATE = os.path.join(EA10, 'ea-10-state.json')


def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wave', type=int, required=True)
    ap.add_argument('--batch', type=int, required=True)
    ap.add_argument('--update-state', action='store_true')
    args = ap.parse_args()

    tag = f'EA10-W{args.wave:02d}-B{args.batch:02d}'
    sel = [r for r in load_csv(SEL) if r.get('BatchTag') == tag or r.get('BatchID') == tag]
    res = {r['DocumentID']: r for r in load_csv(RES)}
    ids = [r['DocumentID'] for r in sel]

    upload_ok = metadata_ok = registry_ok = failed = 0
    broken_urls = []
    dup_ids = []
    seen = set()
    for doc_id in ids:
        if doc_id in seen:
            dup_ids.append(doc_id)
        seen.add(doc_id)
        r = res.get(doc_id, {})
        us = r.get('UploadStatus', '')
        ms = r.get('MetadataStatus', '')
        rs = r.get('RegistryStatus', '')
        if us == 'OK':
            upload_ok += 1
        else:
            failed += 1
        if ms in ('PASS', 'WARN'):
            metadata_ok += 1
        if rs in ('AUTO_UPSERT', 'OK'):
            registry_ok += 1
        url = r.get('SharePointURL', '')
        if us == 'OK' and (not url or '/sites/msteams_54adc4/sites/' in url):
            broken_urls.append(doc_id)

    metrics = {
        'wave': args.wave,
        'batch': args.batch,
        'batch_tag': tag,
        'expected': len(sel),
        'UPLOAD_SUCCESS': upload_ok,
        'METADATA_SUCCESS': metadata_ok,
        'REGISTRY_SUCCESS': registry_ok,
        'FAILED': failed,
        'DUPLICATES': len(dup_ids),
        'BROKEN_URLS': len(broken_urls),
        'broken_doc_ids': broken_urls,
        'gate_pass': (
            failed == 0
            and len(dup_ids) == 0
            and len(broken_urls) == 0
            and upload_ok == len(sel)
            and registry_ok == upload_ok
        ),
    }
    print(json.dumps(metrics, indent=2))

    if args.update_state:
        state = {}
        if os.path.exists(STATE):
            with open(STATE, encoding='utf-8') as f:
                state = json.load(f)
        key = f'W{args.wave:02d}-B{args.batch:02d}'
        batches = state.setdefault('batches', {})
        batches[key] = metrics
        state['last_wave'] = args.wave
        state['last_batch'] = args.batch
        ok_count = sum(1 for r in load_csv(RES) if r.get('UploadStatus') == 'OK')
        state['migrated_so_far'] = ok_count
        with open(STATE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    sys.exit(0 if metrics['gate_pass'] else 1)


if __name__ == '__main__':
    main()
