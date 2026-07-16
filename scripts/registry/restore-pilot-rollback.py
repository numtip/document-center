#!/usr/bin/env python3
"""
PXP-3 Rollback Restore — restores pilot records to their pre-publication state.
Usage: python scripts/registry/restore-pilot-rollback.py --all
       python scripts/registry/restore-pilot-rollback.py --doc RAE-00001
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '.migration', 'rae-wtms', 'tools'))
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from playwright.sync_api import sync_playwright
import requests

SITE = SITE_DEFAULT.rstrip('/')
ROLLBACK_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '.migration/pxp3/rollback-live-registry.json')

def main():
    if not os.path.exists(ROLLBACK_FILE):
        print(f"Rollback file not found: {ROLLBACK_FILE}")
        sys.exit(1)

    with open(ROLLBACK_FILE, encoding='utf-8') as f:
        rollback = json.load(f)

    print(f"Loaded {len(rollback)} rollback records")

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

    for rec in rollback:
        doc_id = rec['DocumentID']
        list_item_id = rec['ListItemId']
        prev_status = rec['PreviousStatus']
        prev_visibility = rec['PreviousVisibility']

        url = f"{SITE}/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items({list_item_id})/ValidateUpdateListItem"
        fields = [
            {'FieldName': 'Status', 'FieldValue': prev_status},
            {'FieldName': 'Visibility', 'FieldValue': prev_visibility},
        ]
        body = {'formValues': fields, 'bNewDocumentUpdate': False}
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 200:
            print(f"  Restored {doc_id}: Status={prev_status}, Visibility={prev_visibility}")
        else:
            print(f"  FAILED {doc_id}: {resp.status_code} {resp.text[:100]}")

if __name__ == '__main__':
    main()
