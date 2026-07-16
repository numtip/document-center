#!/usr/bin/env python3
"""EA-10 preflight validation for all selected documents."""
import csv
import hashlib
import json
import os
import sys
from collections import Counter

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
SEL = os.path.join(EA10, 'ea-10-selection.csv')
OUT = os.path.join(EA10, 'ea-10-preflight.csv')
SUMMARY = os.path.join(EA10, 'ea-10-preflight-summary.json')

EA6 = {'RAE-00009', 'RAE-00046', 'RAE-00146', 'RAE-00195', 'RAE-00662', 'RAE-00119'}
LIBS = {
    'Administration', 'FinanceProcurement', 'PlanningPolicy',
    'AcademicServices', 'Research', 'SOPManuals',
}
EXT_OK = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.jpg', '.png'}


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


def check_auth(page):
    try:
        page.goto(f'{SITE_DEFAULT}/Administration/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
        ctx = page.evaluate('() => _spPageContextInfo.webServerRelativeUrl')
        return bool(ctx)
    except Exception as e:
        return str(e)


def validate_row(r, migrated, seen, target_paths):
    issues = []
    did = r['DocumentID']
    path = os.path.join(ROOT, r['LocalRelativePath'])
    if did in migrated:
        issues.append('already_migrated')
    if did in seen:
        issues.append('duplicate_selection')
    seen.add(did)
    if not os.path.exists(path):
        issues.append('missing_file')
    elif not os.access(path, os.R_OK):
        issues.append('unreadable_file')
    else:
        with open(path, 'rb') as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        if sha != r['SHA256'].strip():
            issues.append('sha_mismatch')
        ext = os.path.splitext(path)[1].lower()
        if ext not in EXT_OK:
            issues.append('unsupported_ext')
        if not r.get('FileSizeBytes') and not r.get('FileSize'):
            issues.append('unknown_size')
    if r['TargetLibrary'] not in LIBS:
        issues.append('bad_library')
    target = f"{r['TargetLibrary']}/{did}{os.path.splitext(path)[1] if os.path.exists(path) else ''}"
    if target in target_paths:
        issues.append('duplicate_target_path')
    target_paths.add(target)
    return issues


def main():
    os.makedirs(EA10, exist_ok=True)
    migrated = load_migrated()
    with open(SEL, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    auth_ok = False
    auth_detail = ''
    with sync_playwright() as p:
        context = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(context))
        auth_result = check_auth(page)
        auth_ok = auth_result is True
        auth_detail = 'authenticated' if auth_ok else str(auth_result)
        close_context(context)

    seen = set()
    target_paths = set()
    preflight_rows = []
    ready = blocked = review = 0
    excluded_ids = []

    for r in rows:
        issues = validate_row(r, migrated, seen, target_paths)
        if not auth_ok:
            issues.append('auth_unreachable')
        status = 'READY'
        if issues:
            if any(x in issues for x in ('sha_mismatch', 'missing_file', 'already_migrated', 'bad_library')):
                status = 'BLOCKED'
                blocked += 1
                excluded_ids.append(r['DocumentID'])
            else:
                status = 'NEEDS_REVIEW'
                review += 1
                excluded_ids.append(r['DocumentID'])
        else:
            ready += 1
        r['PreflightStatus'] = status
        r['Error'] = ','.join(issues)
        preflight_rows.append(r)

    # Update selection: exclude blocked/review from migration
    valid_rows = [r for r in preflight_rows if r['PreflightStatus'] == 'READY']
    fields = list(preflight_rows[0].keys()) if preflight_rows else []
    with open(SEL, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(valid_rows)

    pf_fields = ['DocumentID', 'Wave', 'Batch', 'BatchTag', 'PreflightStatus', 'Error'] + [
        c for c in fields if c not in ('DocumentID', 'Wave', 'Batch', 'BatchTag', 'PreflightStatus', 'Error')
    ]
    with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=pf_fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(preflight_rows)

    summary = {
        'timestamp': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'total_selected': len(preflight_rows),
        'READY': ready,
        'BLOCKED': blocked,
        'NEEDS_REVIEW': review,
        'excluded_count': len(excluded_ids),
        'valid_for_migration': len(valid_rows),
        'authentication': auth_detail,
        'gate_pass': blocked == 0 and review == 0,
        'by_status': dict(Counter(r['PreflightStatus'] for r in preflight_rows)),
    }
    with open(SUMMARY, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, indent=2))
    if blocked or review:
        print(f'Excluded {len(excluded_ids)} items; continuing with {len(valid_rows)} valid', file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
