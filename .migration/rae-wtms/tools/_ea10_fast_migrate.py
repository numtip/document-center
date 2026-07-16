#!/usr/bin/env python3
"""EA-10 fast wave migration — continue-on-failure, state every 25 docs, minimal logging."""
import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from _ea7a_batch_migrate import load_results, migrate_row, save_result
from _m365_browser import close_context, ensure_authenticated, get_page, launch_persistent

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
SEL = os.path.join(EA10, 'ea-10-selection.csv')
RES = os.path.join(EA10, 'ea-10-results.csv')
STATE = os.path.join(EA10, 'ea-10-state.json')
STATE_INTERVAL = 25


def load_selection():
    with open(SEL, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def save_state_snapshot(state, force=False):
    state['updated_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def count_ok():
    if not os.path.exists(RES):
        return 0
    with open(RES, encoding='utf-8-sig') as f:
        return sum(1 for r in csv.DictReader(f) if r.get('UploadStatus') == 'OK')


def wave_targets(wave, from_batch=1):
    rows = load_selection()
    targets = [
        r for r in rows
        if int(r.get('Wave', 0)) == wave
        and int(r.get('Batch', 0)) >= from_batch
        and r.get('PreflightStatus') == 'READY'
    ]
    targets.sort(key=lambda x: (int(x['Batch']), int(x['Sequence'])))
    return targets


def log_line(wave, batch, uploaded, failed, elapsed, next_batch):
    print(f'Wave {wave} | Batch {batch} | Uploaded {uploaded} | Failed {failed} | Elapsed {elapsed:.0f}s | Next {next_batch}', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wave', type=int, required=True)
    ap.add_argument('--from-batch', type=int, default=1)
    args = ap.parse_args()

    targets = wave_targets(args.wave, args.from_batch)
    if not targets:
        print(f'Wave {args.wave}: nothing to migrate', file=sys.stderr)
        sys.exit(0)

    existing = load_results(RES)
    pending = [r for r in targets if existing.get(r['DocumentID'], {}).get('UploadStatus') != 'OK']
    if not pending:
        print(f'Wave {args.wave}: all complete', file=sys.stderr)
        sys.exit(0)

    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding='utf-8') as f:
            state = json.load(f)
    state['current_wave'] = args.wave
    state['fast_mode'] = True
    save_state_snapshot(state, force=True)

    wave_t0 = time.time()
    wave_ok_start = count_ok()
    batch_failed = []
    last_save_ok = count_ok()

    with sync_playwright() as p:
        context = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(context))

        current_batch = None
        batch_t0 = time.time()
        batch_uploaded = 0
        batch_failed_count = 0

        for row in pending:
            b = int(row['Batch'])
            if current_batch != b:
                if current_batch is not None:
                    elapsed = time.time() - batch_t0
                    next_b = b
                    log_line(args.wave, current_batch, batch_uploaded, batch_failed_count, elapsed, next_b)
                current_batch = b
                batch_t0 = time.time()
                batch_uploaded = 0
                batch_failed_count = 0

            if existing.get(row['DocumentID'], {}).get('UploadStatus') == 'OK':
                continue

            try:
                result = migrate_row(page, row)
            except Exception as e:
                result = {
                    'BatchID': row.get('BatchTag', row.get('BatchID')),
                    'Sequence': row['Sequence'],
                    'DocumentID': row['DocumentID'],
                    'TargetLibrary': row['TargetLibrary'],
                    'UploadStatus': 'FAIL',
                    'MetadataStatus': 'FAIL',
                    'RegistryStatus': 'SKIP',
                    'RollbackStatus': 'N/A',
                    'Error': str(e)[:200],
                    'DurationSec': 0,
                    'MigrationMethod': 'playwright-rest',
                    'Timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                }

            save_result(result, RES)
            existing[row['DocumentID']] = result

            if result.get('UploadStatus') == 'OK':
                batch_uploaded += 1
                ok_now = count_ok()
                if ok_now - last_save_ok >= STATE_INTERVAL:
                    state['migrated_so_far'] = ok_now
                    state['last_wave'] = args.wave
                    state['last_batch'] = b
                    save_state_snapshot(state)
                    last_save_ok = ok_now
            else:
                batch_failed_count += 1
                batch_failed.append(row)

        if current_batch is not None:
            elapsed = time.time() - batch_t0
            log_line(args.wave, current_batch, batch_uploaded, batch_failed_count, elapsed, 'END')

        # Retry failures once at wave end
        if batch_failed:
            retry_ok = 0
            for row in batch_failed:
                if existing.get(row['DocumentID'], {}).get('UploadStatus') == 'OK':
                    continue
                try:
                    result = migrate_row(page, row)
                    save_result(result, RES)
                    existing[row['DocumentID']] = result
                    if result.get('UploadStatus') == 'OK':
                        retry_ok += 1
                except Exception:
                    pass
            if retry_ok:
                print(f'Wave {args.wave} retry recovered {retry_ok}', flush=True)

        close_context(context)

    wave_ok = count_ok() - wave_ok_start
    wave_fail = len([r for r in pending if existing.get(r['DocumentID'], {}).get('UploadStatus') != 'OK'])
    wave_elapsed = time.time() - wave_t0
    fail_pct = (wave_fail / len(pending) * 100) if pending else 0

    state['migrated_so_far'] = count_ok()
    state['last_wave'] = args.wave
    state[f'wave_{args.wave:02d}_elapsed_sec'] = round(wave_elapsed, 1)
    state[f'wave_{args.wave:02d}_uploaded'] = wave_ok
    state[f'wave_{args.wave:02d}_failed'] = wave_fail
    save_state_snapshot(state, force=True)

    print(f'Wave {args.wave} done | +{wave_ok} ok | {wave_fail} fail | {wave_elapsed:.0f}s', flush=True)

    if fail_pct > 10:
        print(f'ABORT: >10% failures in wave {args.wave} ({fail_pct:.1f}%)', file=sys.stderr)
        sys.exit(1)
    sys.exit(0 if wave_fail == 0 else 0)


if __name__ == '__main__':
    main()
