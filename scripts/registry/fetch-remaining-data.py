#!/usr/bin/env python3
"""
PXP-4 — Retrieve remaining Registry metadata. Main Agent only.
Fetches all 627 records, creates sanitized snapshots.
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '.migration', 'rae-wtms', 'tools'))
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from playwright.sync_api import sync_playwright
import requests
from collections import Counter

SITE = SITE_DEFAULT.rstrip('/')
REPO = os.path.join(os.path.dirname(__file__), '..', '..')
PUBLISHED_FILE = os.path.join(REPO, 'reports/pxp3-publish-results.json')

# Already published from PXP-3
with open(PUBLISHED_FILE, encoding='utf-8') as f:
    PUBLISHED_IDS = set(json.load(f)['published'])

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

list_url = f"{SITE}/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items"
params = {
    '$select': 'Id,Title,Document_x0020_ID,Category,Status,Visibility,Storage_x0020_URL,Updated_x0020_Date',
    '$top': 1000,
}
resp = requests.get(list_url, headers=headers, params=params, timeout=60)
resp.raise_for_status()
data = resp.json()
rows = data.get('d', {}).get('results', [])

all_snapshot = []
remaining = []
rollback = []

for r in rows:
    st = r.get('Storage_x0020_URL') or {}
    storage_url = st.get('Url','') if isinstance(st, dict) else ''
    updated = r.get('Updated_x0020_Date','') or ''
    doc_id = r.get('Document_x0020_ID','') or ''

    rec = {
        'ListItemId': r.get('Id'),
        'DocumentID': doc_id,
        'Title': (r.get('Title','') or '')[:200],
        'Category': r.get('Category',''),
        'Status': r.get('Status',''),
        'Visibility': r.get('Visibility',''),
        'StorageURL': storage_url[:250],
        'UpdatedDate': updated,
    }
    all_snapshot.append(rec)

    if doc_id in PUBLISHED_IDS:
        continue  # Already published
        
    remaining.append(rec)
    rollback.append({
        'ListItemId': r.get('Id'),
        'DocumentID': doc_id,
        'PreviousStatus': r.get('Status',''),
        'PreviousVisibility': r.get('Visibility',''),
    })

os.makedirs(os.path.join(REPO, '.migration/pxp4'), exist_ok=True)

# Full sanitized snapshot (all 627)
with open(os.path.join(REPO, '.migration/pxp4/registry-sanitized-full.json'), 'w', encoding='utf-8') as f:
    json.dump(all_snapshot, f, ensure_ascii=False, indent=2)

# Remaining only (603)
with open(os.path.join(REPO, '.migration/pxp4/registry-sanitized.json'), 'w', encoding='utf-8') as f:
    json.dump(remaining, f, ensure_ascii=False, indent=2)

# Rollback for remaining
with open(os.path.join(REPO, '.migration/pxp4/batch-a-rollback.json'), 'w', encoding='utf-8') as f:
    json.dump(rollback, f, ensure_ascii=False, indent=2)

# Summary
cats = Counter(r['Category'] for r in remaining)
statuses = Counter(r['Status'] for r in remaining)
vis = Counter(r['Visibility'] for r in remaining)
with_url = sum(1 for r in remaining if r['StorageURL'].startswith('https://'))

print(f"Total scanned: {len(all_snapshot)}")
print(f"Already published: {len(PUBLISHED_IDS)}")
print(f"Remaining records: {len(remaining)}")
print(f"With valid StorageURL: {with_url}")
print(f"\nCategories ({len(cats)}):")
for c, n in cats.most_common(10):
    print(f"  {c}: {n}")
print(f"\nStatuses: {dict(statuses)}")
print(f"Visibilities: {dict(vis)}")
print(f"\nRollback records saved: {len(rollback)}")
