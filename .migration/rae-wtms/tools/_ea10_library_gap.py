#!/usr/bin/env python3
"""Find IDs in results/registry but missing from library scan."""
import csv
import json
import os
import sys

from playwright.sync_api import sync_playwright
from _m365_browser import close_context, ensure_authenticated, get_page, launch_persistent
from _registry_upsert import build_scan_libs_js

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')


def main():
    res_ids = set()
    with open(os.path.join(EA10, 'ea-10-results.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r.get('UploadStatus') == 'OK':
                res_ids.add(r['DocumentID'])

    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(ctx))
        scan = page.evaluate(build_scan_libs_js())
        lib_ids = {x['document_id'] for x in scan if x.get('document_id')}
        close_context(ctx)

    missing = sorted(res_ids - lib_ids, key=lambda x: int(x.split('-')[1]))
    print(json.dumps({'results_ok': len(res_ids), 'library_ids': len(lib_ids), 'missing_in_library': len(missing), 'sample': missing[:10]}))
    with open(os.path.join(EA10, 'ea-10-library-gap.json'), 'w', encoding='utf-8') as f:
        json.dump({'missing': missing}, f, indent=2)
    return 0 if not missing else 1


if __name__ == '__main__':
    sys.exit(main())
