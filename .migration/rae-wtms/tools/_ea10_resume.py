#!/usr/bin/env python3
"""EA-10: resume remaining waves from current progress."""
import csv
import json
import os
import subprocess
import sys
import time

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
TOOLS = os.path.join(ROOT, 'tools')


def count_ok_by_wave():
    res_path = os.path.join(EA10, 'ea-10-results.csv')
    sel_path = os.path.join(EA10, 'ea-10-selection.csv')
    if not os.path.exists(res_path):
        return {}
    with open(res_path, encoding='utf-8-sig') as f:
        ok = {r['DocumentID'] for r in csv.DictReader(f) if r.get('UploadStatus') == 'OK'}
    with open(sel_path, encoding='utf-8-sig') as f:
        sel = list(csv.DictReader(f))
    by_wave = {}
    for r in sel:
        w = int(r['Wave'])
        if r['DocumentID'] in ok:
            by_wave[w] = by_wave.get(w, 0) + 1
    return by_wave


def batches_in_wave(wave):
    with open(os.path.join(EA10, 'ea-10-selection.csv'), encoding='utf-8-sig') as f:
        rows = [r for r in csv.DictReader(f) if int(r['Wave']) == wave]
    return sorted({int(r['Batch']) for r in rows})


def main():
    py = sys.executable
    t0 = time.time()
    progress = count_ok_by_wave()
    print('Progress by wave:', progress)

    for wave in range(1, 6):
        expected = {1: 100, 2: 100, 3: 100, 4: 100, 5: 96}.get(wave, 0)
        done = progress.get(wave, 0)
        if done >= expected:
            print(f'Wave {wave} already complete ({done}/{expected})')
            continue
        start_batch = (done // 10) + 1 if done % 10 == 0 and done > 0 else (done // 10) + 1
        if done > 0 and done % 10 == 0:
            start_batch = (done // 10) + 1
        elif done > 0:
            start_batch = (done // 10) + 1
        else:
            start_batch = 1
        # If partial batch completed, resume that batch (idempotent skip)
        if done > 0:
            start_batch = max(1, (done - 1) // 10 + 1)

        batches = batches_in_wave(wave)
        for b in batches:
            if b < start_batch:
                continue
            rc = subprocess.call([py, '_ea10_batch_migrate.py', '--wave', str(wave), '--batch', str(b)], cwd=TOOLS)
            if rc not in (0, 1):
                sys.exit(rc)
            rc = subprocess.call([py, '_ea10_batch_qa.py', '--wave', str(wave), '--batch', str(b), '--update-state'], cwd=TOOLS)
            if rc != 0:
                sys.exit(rc)

        subprocess.call([py, '_ea8_registry_sync.py', '--sync-all'], cwd=TOOLS)
        rc = subprocess.call([py, '_ea10_wave_qa.py', '--wave', str(wave)], cwd=TOOLS)
        if rc != 0:
            sys.exit(rc)
        progress = count_ok_by_wave()

    elapsed = round(time.time() - t0, 1)
    state_path = os.path.join(EA10, 'ea-10-state.json')
    with open(state_path, encoding='utf-8') as f:
        state = json.load(f)
    state['elapsed_wall_sec'] = round(state.get('elapsed_wall_sec', 858.3) + elapsed, 1)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f'Resume complete. Additional elapsed: {elapsed}s')


if __name__ == '__main__':
    main()
