#!/usr/bin/env python3
"""EA-10 live baseline reconciliation: manifest + SharePoint libraries + Registry."""
import argparse
import csv
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from _registry_upsert import build_count_duplicates_js, build_scan_libs_js

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
MANIFEST = os.path.join(r'G:\ProjectAI\document-center\migration', 'sharepoint-migration-manifest.csv')
BASELINE_OUT = os.path.join(EA10, 'ea-10-baseline.json')
RECON_BEFORE = os.path.join(EA10, 'ea-10-reconciliation-before.csv')
EXCEPTIONS = os.path.join(EA10, 'ea-10-exceptions.csv')

EA6 = {'RAE-00009', 'RAE-00046', 'RAE-00146', 'RAE-00195', 'RAE-00662', 'RAE-00119'}
LIBS = {
    'Administration', 'FinanceProcurement', 'PlanningPolicy',
    'AcademicServices', 'Research', 'SOPManuals',
}


def git_head():
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=r'G:\ProjectAI\document-center', text=True,
        ).strip()
    except Exception:
        return 'unknown'


def load_migrated_from_results():
    ids = set(EA6)
    for name in ('ea-7a-results.csv', 'ea-9-results.csv', 'ea-10-results.csv'):
        p = os.path.join(ROOT, 'pilot' if 'ea-10' not in name else EA10, name.replace('ea-10-', 'ea-10-'))
        if name == 'ea-10-results.csv':
            p = os.path.join(EA10, 'ea-10-results.csv')
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r.get('UploadStatus') == 'OK':
                    ids.add(r['DocumentID'])
    return ids


def load_manifest():
    with open(MANIFEST, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def registry_scan_js():
    return """(async function(){
var s=_spPageContextInfo.webServerRelativeUrl;
var r=await fetch(s+"/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items?$select=Id,Document_x0020_ID,Title,Storage_x0020_URL&$top=5000",{headers:{'accept':'application/json;odata=verbose'}});
var rows=(await r.json()).d.results||[];
return rows.map(x=>({
id:x.Id,document_id:x.Document_x0020_ID||'',
storage:(x.Storage_x0020_URL&&x.Storage_x0020_URL.Url)?x.Storage_x0020_URL.Url:''
}));
})()"""


def classify_ready(row, lib_map, reg_map, prior_success):
    doc_id = row['DocumentID']
    lib = row.get('TargetLibrary', '')
    path = os.path.join(ROOT, row.get('LocalRelativePath', ''))
    issues = []

    if not row.get('LocalRelativePath', '').strip():
        return 'BLOCKED', 'missing_local_path'
    if not os.path.exists(path):
        return 'BLOCKED', 'missing_source_file'
    if lib not in LIBS:
        return 'BLOCKED', 'invalid_library'

    in_lib = doc_id in lib_map
    in_reg = doc_id in reg_map
    lib_info = lib_map.get(doc_id, {})
    reg_info = reg_map.get(doc_id, {})

    if in_lib and in_reg:
        if lib_info.get('lib') != lib:
            return 'CONFLICT', 'library_mismatch'
        return 'ALREADY_COMPLETE', ''
    if in_lib and not in_reg:
        return 'LIBRARY_ONLY', 'registry_missing'
    if in_reg and not in_lib:
        return 'REGISTRY_ONLY', 'library_missing'
    if doc_id in prior_success:
        return 'CONFLICT', 'prior_success_not_in_library'
    return 'NOT_MIGRATED', ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--offline', action='store_true', help='Skip live SharePoint scan')
    args = ap.parse_args()

    os.makedirs(EA10, exist_ok=True)
    rows = load_manifest()
    ready = [r for r in rows if r.get('MigrationStatus') == 'Ready' and r.get('LocalRelativePath', '').strip()]
    prior_success = load_migrated_from_results()

    lib_map = {}
    reg_map = {}
    lib_counts = Counter()
    auth_state = 'not_checked'
    reg_total = 0
    reg_dups = []
    broken_urls = 0

    if not args.offline:
        with sync_playwright() as p:
            context = launch_persistent(p, headless=False)
            page = ensure_authenticated(get_page(context))
            page.goto(f'{SITE_DEFAULT}/Administration/Forms/AllItems.aspx?sw=bypass', timeout=120000)
            page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
            auth_state = 'authenticated'

            scan = page.evaluate(build_scan_libs_js())
            for item in scan:
                if item.get('error'):
                    continue
                did = item.get('document_id', '')
                if did:
                    lib_map[did] = item
                    lib_counts[item['lib']] += 1

            reg_rows = page.evaluate(registry_scan_js())
            reg_total = len(reg_rows)
            seen_reg = {}
            for r in reg_rows:
                did = r.get('document_id', '')
                if not did:
                    continue
                if did in seen_reg:
                    reg_dups.append(did)
                seen_reg[did] = r
                storage = r.get('storage', '')
                if storage and '/sites/msteams_54adc4/sites/' in storage:
                    broken_urls += 1
            reg_map = seen_reg

            dup_check = page.evaluate(build_count_duplicates_js())
            if dup_check.get('duplicates'):
                reg_dups.extend(dup_check['duplicates'])

            close_context(context)
    else:
        auth_state = 'offline_mode'

    recon_rows = []
    status_counts = Counter()
    not_migrated = []

    for r in ready:
        status, reason = classify_ready(r, lib_map, reg_map, prior_success)
        status_counts[status] += 1
        recon_rows.append({
            'DocumentID': r['DocumentID'],
            'Title': r.get('Title', ''),
            'TargetLibrary': r.get('TargetLibrary', ''),
            'Status': status,
            'Reason': reason,
            'InLibrary': r['DocumentID'] in lib_map,
            'InRegistry': r['DocumentID'] in reg_map,
            'PriorSuccess': r['DocumentID'] in prior_success,
        })
        if status == 'NOT_MIGRATED':
            not_migrated.append(r['DocumentID'])

    fields = list(recon_rows[0].keys()) if recon_rows else []
    with open(RECON_BEFORE, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(recon_rows)

    baseline = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'repository_head': git_head(),
        'manifest_row_count': len(rows),
        'manifest_ready_count': len(ready),
        'prior_success_count': len(prior_success),
        'already_complete_count': status_counts['ALREADY_COMPLETE'],
        'library_only_count': status_counts['LIBRARY_ONLY'],
        'registry_only_count': status_counts['REGISTRY_ONLY'],
        'not_migrated_count': status_counts['NOT_MIGRATED'],
        'conflict_count': status_counts['CONFLICT'],
        'blocked_count': status_counts['BLOCKED'],
        'remaining_eligible_count': status_counts['NOT_MIGRATED'],
        'library_item_counts': dict(lib_counts),
        'library_total_unique_ids': len(lib_map),
        'registry_row_count': reg_total,
        'registry_unique_ids': len(reg_map),
        'registry_duplicate_document_ids': sorted(set(reg_dups)),
        'registry_duplicate_count': len(set(reg_dups)),
        'broken_storage_url_count': broken_urls,
        'authentication_state': auth_state,
        'status_breakdown': dict(status_counts),
    }

    with open(BASELINE_OUT, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, ensure_ascii=False, indent=2)

    print(json.dumps(baseline, ensure_ascii=False, indent=2))
    return 0 if status_counts['CONFLICT'] == 0 else 0


if __name__ == '__main__':
    sys.exit(main())
