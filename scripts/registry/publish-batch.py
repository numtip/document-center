#!/usr/bin/env python3
"""
PXP-4 Batch Publisher — publishes Registry records to Status=current, Visibility=public.

Builds on PXP-3's publish-pilot.py with robust batch production features:
  • Batch size: 20-25 records per checkpoint
  • Idempotent: skips records already current/public
  • Checkpoint: saves progress after each batch to .migration/pxp4/publish-checkpoint.json
  • Resume: --resume flag continues from last checkpoint
  • Retry: one retry per failing record before marking as failed
  • Audit: logs each mutation with timestamp, success/fail, response
  • Dry-run: --dry-run flag previews changes without making them
  • Manifest: reads from reports/pxp4-batch-a-manifest.json
  • Output: writes results to reports/pxp4-batch-a-publish-results.json

Usage:
    python scripts/registry/publish-batch.py                          # Full run
    python scripts/registry/publish-batch.py --resume                 # Resume from checkpoint
    python scripts/registry/publish-batch.py --dry-run               # Preview only
    python scripts/registry/publish-batch.py --batch-size 25          # Custom batch size
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '.migration', 'rae-wtms', 'tools'))
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from playwright.sync_api import sync_playwright

# ── Paths ──────────────────────────────────────────────────────────────────
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(REPO_ROOT, 'reports')
MIGRATION_DIR = os.path.join(REPO_ROOT, '.migration')
PXP4_DIR = os.path.join(MIGRATION_DIR, 'pxp4')

DEFAULT_MANIFEST = os.path.join(REPORTS_DIR, 'pxp4-batch-a-manifest.json')
DEFAULT_CHECKPOINT = os.path.join(PXP4_DIR, 'publish-checkpoint.json')
DEFAULT_OUTPUT = os.path.join(REPORTS_DIR, 'pxp4-batch-a-publish-results.json')

SITE = SITE_DEFAULT.rstrip('/')
LIST_URL = f"{SITE}/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items"


# ── CLI ────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='PXP-4 Batch Publisher — publish records to current/public'
    )
    parser.add_argument(
        '--resume', action='store_true',
        help='Resume from last saved checkpoint'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview changes without making any updates'
    )
    parser.add_argument(
        '--batch-size', type=int, default=25,
        help='Records per checkpoint batch (default: 25)'
    )
    parser.add_argument(
        '--manifest', type=str, default=DEFAULT_MANIFEST,
        help=f'Manifest file path (default: {DEFAULT_MANIFEST})'
    )
    parser.add_argument(
        '--checkpoint', type=str, default=DEFAULT_CHECKPOINT,
        help=f'Checkpoint file path (default: {DEFAULT_CHECKPOINT})'
    )
    parser.add_argument(
        '--output', type=str, default=DEFAULT_OUTPUT,
        help=f'Output results file path (default: {DEFAULT_OUTPUT})'
    )
    return parser.parse_args()


# ── Auth ───────────────────────────────────────────────────────────────────

def authenticate() -> tuple:
    """Use Playwright browser profile to get cookies and digest."""
    print('[PXP-4] Authenticating via Playwright browser profile...', flush=True)
    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(ctx))
        ctx_info = page.evaluate("""() => ({
            webUrl: _spPageContextInfo.webServerRelativeUrl,
            digest: _spPageContextInfo.formDigestValue,
        })""")
        cookies = ctx.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        close_context(ctx)

    headers = {
        'Accept': 'application/json;odata=verbose',
        'X-RequestDigest': ctx_info['digest'],
        'Cookie': '; '.join(f"{k}={v}" for k, v in cookie_dict.items()),
    }
    print(f'[PXP-4] Authenticated. Digest: {ctx_info["digest"][:30]}...', flush=True)
    return headers


# ── Registry Read ──────────────────────────────────────────────────────────

def read_registry_item(headers: dict, list_item_id: int) -> dict:
    """Read a single registry item's Status and Visibility."""
    url = f"{LIST_URL}({list_item_id})?$select=Id,Status,Visibility,Document_x0020_ID"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json().get('d', {})


# ── Publish Record ─────────────────────────────────────────────────────────

def publish_record(
    headers: dict, list_item_id: int, doc_id: str, dry_run: bool = False
) -> dict:
    """
    Publish a single record: Status->current, Visibility->public.

    Returns a result dict with keys:
      - doc_id, list_item_id, status (published|skipped|failed|dry-run)
      - error (if failed)
      - response (API response snippet)
    """
    entry = {
        'doc_id': doc_id,
        'list_item_id': list_item_id,
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    # ── Idempotency check ──────────────────────────────────────────────
    try:
        current = read_registry_item(headers, list_item_id)
        current_status = (current.get('Status') or '').strip().lower()
        current_visibility = (current.get('Visibility') or '').strip().lower()
    except Exception as e:
        entry['status'] = 'failed'
        entry['error'] = f'Pre-read failed: {e}'
        entry['response'] = str(e)[:200]
        return entry

    if current_status == 'current' and current_visibility == 'public':
        entry['status'] = 'skipped'
        entry['error'] = None
        entry['response'] = f'Already Status=current, Visibility=public'
        return entry

    if dry_run:
        entry['status'] = 'dry-run'
        entry['response'] = (
            f'Would update: Status={current_status}->current, '
            f'Visibility={current_visibility}->public'
        )
        return entry

    # ── Perform update ─────────────────────────────────────────────────
    url = f"{LIST_URL}({list_item_id})/ValidateUpdateListItem"
    fields = [
        {'FieldName': 'Status', 'FieldValue': 'current'},
        {'FieldName': 'Visibility', 'FieldValue': 'public'},
    ]
    body = {'formValues': fields, 'bNewDocumentUpdate': False}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 200:
            result_data = resp.json()
            errs = result_data.get('d', {}).get('ValidateUpdateListItem', {}).get('results', [])
            has_exception = any(e.get('HasException') for e in errs if isinstance(e, dict))
            if has_exception:
                entry['status'] = 'failed'
                entry['error'] = json.dumps(errs)[:300]
                entry['response'] = json.dumps(errs)[:300]
            else:
                entry['status'] = 'published'
                entry['error'] = None
                entry['response'] = 'Status=current, Visibility=public'
        else:
            entry['status'] = 'failed'
            entry['error'] = f'HTTP {resp.status_code}'
            entry['response'] = resp.text[:300]
    except Exception as e:
        entry['status'] = 'failed'
        entry['error'] = f'Exception: {e}'
        entry['response'] = str(e)[:300]

    return entry


# ── Checkpoint ─────────────────────────────────────────────────────────────

def load_checkpoint(path: str) -> dict:
    """Load checkpoint file. Returns None if not found or corrupt."""
    if not os.path.exists(path):
        print(f'[PXP-4] No checkpoint found at {path}', flush=True)
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            cp = json.load(f)
        print(
            f'[PXP-4] Loaded checkpoint: batch {cp.get("completed_batches", "?")} '
            f'completed, {len(cp.get("processed_ids", []))} records processed',
            flush=True,
        )
        return cp
    except (json.JSONDecodeError, KeyError) as e:
        print(f'[PXP-4] WARNING: Corrupt checkpoint ({e}), starting fresh', flush=True)
        return None


def save_checkpoint(path: str, cp: dict):
    """Atomically write checkpoint file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(cp, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
    print(f'[PXP-4] Checkpoint saved: batch {cp["completed_batches"]}', flush=True)


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    dry_run = args.dry_run
    batch_size = args.batch_size
    manifest_path = args.manifest
    checkpoint_path = args.checkpoint
    output_path = args.output

    # Validate batch size
    if not 20 <= batch_size <= 25:
        print(f'[PXP-4] ERROR: --batch-size must be between 20 and 25, got {batch_size}', file=sys.stderr)
        sys.exit(1)

    # ── Load manifest ──────────────────────────────────────────────────
    if not os.path.exists(manifest_path):
        print(f'[PXP-4] ERROR: Manifest not found: {manifest_path}', file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    total = len(manifest)
    print(f'[PXP-4] Loaded manifest: {total} records from {manifest_path}', flush=True)
    if dry_run:
        print(f'[PXP-4] DRY RUN MODE — no records will be updated', flush=True)

    # ── Resolve starting state ─────────────────────────────────────────
    published = []
    failed = []
    skipped = []
    audit_log = []
    start_index = 0
    processed_ids = set()

    if args.resume:
        cp = load_checkpoint(checkpoint_path)
        if cp:
            published = cp.get('results_so_far', {}).get('published', [])
            failed = cp.get('results_so_far', {}).get('failed', [])
            skipped = cp.get('results_so_far', {}).get('skipped', [])
            audit_log = cp.get('audit_log', [])
            processed_ids = set(cp.get('processed_ids', []))
            start_index = cp.get('completed_batches', 0) * batch_size
            # Walk forward past already-processed IDs to find the true resume point
            # (handles cases where batch_size changed between runs)
            manifest_remaining = []
            for rec in manifest:
                doc_id = rec.get('DocumentID', '').strip()
                entry_id = f"{rec.get('ListItemId')}:{doc_id}"
                if entry_id not in processed_ids and doc_id not in processed_ids:
                    manifest_remaining.append(rec)
                else:
                    start_index = manifest.index(rec) + 1
            print(
                f'[PXP-4] Resuming: {start_index}/{total} records already processed, '
                f'{len(manifest_remaining)} remaining',
                flush=True,
            )
            manifest = manifest[start_index:]

    # ── Authenticate ───────────────────────────────────────────────────
    headers = authenticate()

    # ── Process batches ─────────────────────────────────────────────────
    batch_num = (start_index // batch_size) + 1 if start_index > 0 else 1
    total_batches = (total + batch_size - 1) // batch_size

    for i in range(0, len(manifest), batch_size):
        batch = manifest[i:i + batch_size]
        batch_label = f'Batch {batch_num}/{total_batches}'
        print(f'\n[PXP-4] {batch_label}: processing {len(batch)} records...', flush=True)

        for rec in batch:
            list_item_id = rec.get('ListItemId')
            doc_id = rec.get('DocumentID', '').strip()

            if not list_item_id or not doc_id:
                entry = {
                    'doc_id': doc_id or '(unknown)',
                    'list_item_id': list_item_id,
                    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'status': 'failed',
                    'error': 'Missing ListItemId or DocumentID in manifest',
                    'response': '',
                }
                failed.append(doc_id or f'ListItemId={list_item_id}')
                audit_log.append(entry)
                print(f'  {doc_id}: INVALID — {entry["error"]}', flush=True)
                continue

            # Attempt 1
            entry = publish_record(headers, list_item_id, doc_id, dry_run=dry_run)

            # Retry logic (one retry on failure, not for skipped or dry-run)
            if entry['status'] == 'failed' and not dry_run:
                print(f'  {doc_id}: FAILED (attempt 1) — {entry["error"][:80]}... retrying...', flush=True)
                time.sleep(1)
                entry = publish_record(headers, list_item_id, doc_id, dry_run=False)

            # Record result
            audit_log.append(entry)

            if entry['status'] == 'published':
                published.append(doc_id)
                print(f'  {doc_id}: Status=current, Visibility=public', flush=True)
            elif entry['status'] == 'skipped':
                skipped.append(doc_id)
                print(f'  {doc_id}: SKIPPED — {entry["response"]}', flush=True)
            elif entry['status'] == 'dry-run':
                print(f'  {doc_id}: DRY-RUN — {entry["response"]}', flush=True)
            else:
                failed.append(doc_id)
                print(f'  {doc_id}: FAILED — {entry["error"][:120]}', flush=True)

            # Gentle throttle
            time.sleep(0.3)

        # ── Save checkpoint after each batch ───────────────────────────
        entry_ids = set()
        for rec in batch:
            doc_id = rec.get('DocumentID', '').strip()
            lid = rec.get('ListItemId')
            entry_ids.add(f"{lid}:{doc_id}")
            if doc_id:
                entry_ids.add(doc_id)
        processed_ids.update(entry_ids)

        # Add any records from before the current batch (resume scenario)
        if batch_num == 1 and start_index > 0:
            pass  # already handled in resume logic above

        checkpoint = {
            'batch_index': batch_num - 1,
            'completed_batches': batch_num,
            'processed_ids': sorted(processed_ids),
            'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'results_so_far': {
                'published': published,
                'failed': failed,
                'skipped': skipped,
            },
            'audit_log': audit_log,
        }
        save_checkpoint(checkpoint_path, checkpoint)
        batch_num += 1

        # Print batch summary
        print(
            f'  -> Batch {batch_num - 1}/{total_batches} complete. '
            f'Cumulative: {len(published)} published, {len(failed)} failed, '
            f'{len(skipped)} skipped',
            flush=True,
        )

    # ── Save final results ─────────────────────────────────────────────
    results = {
        'published': published,
        'failed': failed,
        'skipped': skipped,
        'total': total,
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'dry_run': dry_run,
        'audit_log': audit_log,
        'source_manifest': manifest_path,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'\n[PXP-4] Results saved to {output_path}', flush=True)

    # ── Final summary ──────────────────────────────────────────────────
    print(f'\n[PXP-4] {"DRY-RUN " if dry_run else ""}Publication complete:', flush=True)
    print(f'  Published: {len(published)}', flush=True)
    print(f'  Skipped (already current/public): {len(skipped)}', flush=True)
    print(f'  Failed: {len(failed)}', flush=True)

    if failed:
        print(f'\n[PXP-4] FAILED records:', flush=True)
        for fid in failed:
            print(f'  {fid}', flush=True)

    # Remove checkpoint on successful full run (non-dry-run)
    if not dry_run and len(failed) == 0 and os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)
        print(f'[PXP-4] Checkpoint cleared (all records processed successfully)', flush=True)

    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
