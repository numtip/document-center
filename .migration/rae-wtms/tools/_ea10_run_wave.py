#!/usr/bin/env python3
"""EA-10 orchestration: run all batches in a wave sequentially with QA gates."""
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
TOOLS = os.path.join(ROOT, 'tools')
EA10 = os.path.join(ROOT, 'ea-10')


def run(cmd, desc):
    print(f'\n=== {desc} ===', flush=True)
    print(' '.join(cmd), flush=True)
    rc = subprocess.call(cmd, cwd=TOOLS)
    if rc != 0:
        print(f'FAILED: {desc} (exit {rc})', file=sys.stderr)
        sys.exit(rc)


def count_batches(wave):
    import csv
    sel = os.path.join(EA10, 'ea-10-selection.csv')
    with open(sel, encoding='utf-8-sig') as f:
        rows = [r for r in csv.DictReader(f) if int(r.get('Wave', 0)) == wave]
    return len({r.get('BatchTag', r.get('BatchID')) for r in rows})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wave', type=int, required=True)
    ap.add_argument('--from-batch', type=int, default=1)
    ap.add_argument('--skip-sync', action='store_true')
    args = ap.parse_args()

    py = sys.executable
    t0 = time.time()
    n_batches = count_batches(args.wave)

    for b in range(args.from_batch, n_batches + 1):
        run([py, '_ea10_batch_migrate.py', '--wave', str(args.wave), '--batch', str(b)],
            f'Wave {args.wave} Batch {b} migrate')
        run([py, '_ea10_batch_qa.py', '--wave', str(args.wave), '--batch', str(b), '--update-state'],
            f'Wave {args.wave} Batch {b} QA')

    if not args.skip_sync:
        run([py, '_ea8_registry_sync.py', '--sync-all'], f'Wave {args.wave} registry sync-all')

    run([py, '_ea10_wave_qa.py', '--wave', str(args.wave)], f'Wave {args.wave} report')

    elapsed = round(time.time() - t0, 1)
    state_path = os.path.join(EA10, 'ea-10-state.json')
    state = {}
    if os.path.exists(state_path):
        with open(state_path, encoding='utf-8') as f:
            state = json.load(f)
    state[f'wave_{args.wave:02d}_elapsed_sec'] = elapsed
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f'\nWave {args.wave} complete in {elapsed}s')


if __name__ == '__main__':
    main()
