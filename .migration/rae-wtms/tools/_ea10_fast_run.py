#!/usr/bin/env python3
"""EA-10 fast orchestrator — wave-level sync/QA only, minimal overhead."""
import argparse
import csv
import json
import os
import subprocess
import sys
import time

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
TOOLS = os.path.join(ROOT, 'tools')
STATE = os.path.join(EA10, 'ea-10-state.json')


def wave_complete(wave):
    sel = os.path.join(EA10, 'ea-10-selection.csv')
    res = os.path.join(EA10, 'ea-10-results.csv')
    with open(sel, encoding='utf-8-sig') as f:
        ids = {r['DocumentID'] for r in csv.DictReader(f) if int(r.get('Wave', 0)) == wave}
    if not os.path.exists(res):
        return False
    with open(res, encoding='utf-8-sig') as f:
        ok = {r['DocumentID'] for r in csv.DictReader(f) if r.get('UploadStatus') == 'OK'}
    return ids <= ok


def first_incomplete_batch(wave):
    sel = os.path.join(EA10, 'ea-10-selection.csv')
    res = os.path.join(EA10, 'ea-10-results.csv')
    ok = set()
    if os.path.exists(res):
        with open(res, encoding='utf-8-sig') as f:
            ok = {r['DocumentID'] for r in csv.DictReader(f) if r.get('UploadStatus') == 'OK'}
    with open(sel, encoding='utf-8-sig') as f:
        rows = [r for r in csv.DictReader(f) if int(r.get('Wave', 0)) == wave]
    for r in sorted(rows, key=lambda x: (int(x['Batch']), int(x['Sequence']))):
        if r['DocumentID'] not in ok:
            return int(r['Batch'])
    return 1


def run(cmd):
    return subprocess.call(cmd, cwd=TOOLS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-wave', type=int, default=1)
    ap.add_argument('--to-wave', type=int, default=5)
    ap.add_argument('--resume-check', action='store_true', help='Final resume validation only')
    args = ap.parse_args()

    py = sys.executable
    t0 = time.time()

    if args.resume_check:
        run([py, '_ea10_batch_migrate.py', '--wave', '1', '--batch', '1'])
        print('Final resume check: skipped completed items (exit 0/1 expected)', flush=True)
        sys.exit(0)

    for wave in range(args.from_wave, args.to_wave + 1):
        if wave_complete(wave):
            print(f'Wave {wave}: skip (complete)', flush=True)
            continue

        from_batch = first_incomplete_batch(wave)
        print(f'Wave {wave}: start from batch {from_batch}', flush=True)

        rc = run([py, '_ea10_fast_migrate.py', '--wave', str(wave), '--from-batch', str(from_batch)])
        if rc != 0:
            sys.exit(rc)

        run([py, '_ea8_registry_sync.py', '--sync-all'])
        run([py, '_ea10_wave_qa.py', '--wave', str(wave), '--fast'])

        if wave == 1:
            run([py, '_ea10_batch_migrate.py', '--wave', '1', '--batch', '1'])
            print('Wave 1 resume check done', flush=True)

    elapsed = round(time.time() - t0, 1)
    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding='utf-8') as f:
            state = json.load(f)
    state['fast_mode_elapsed_sec'] = elapsed
    state['elapsed_wall_sec'] = round(state.get('elapsed_wall_sec', 0) + elapsed, 1)
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f'Fast run complete | {elapsed}s', flush=True)


if __name__ == '__main__':
    main()
