#!/usr/bin/env python3
"""Retrieve live Registry data for PXP-3 publication assessment. Main Agent only."""
import json, os, sys
sys.path.insert(0, r'G:\ProjectAI\document-center\.migration\rae-wtms\tools')
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from playwright.sync_api import sync_playwright
import requests
from collections import Counter

SITE = SITE_DEFAULT.rstrip('/')

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

# Build sanitized snapshot (no document content, no owner references)
snapshot = []
rollback = []
for r in rows:
    st = r.get('Storage_x0020_URL') or {}
    storage_url = st.get('Url','') if isinstance(st, dict) else ''
    updated = r.get('Updated_x0020_Date','') or ''
    rec = {
        'ListItemId': r.get('Id'),
        'DocumentID': r.get('Document_x0020_ID',''),
        'Title': (r.get('Title','') or '')[:200],
        'Category': r.get('Category',''),
        'Status': r.get('Status',''),
        'Visibility': r.get('Visibility',''),
        'StorageURL': storage_url[:250],
        'UpdatedDate': updated,
    }
    snapshot.append(rec)
    rollback.append({
        'ListItemId': r.get('Id'),
        'DocumentID': r.get('Document_x0020_ID',''),
        'PreviousStatus': r.get('Status',''),
        'PreviousVisibility': r.get('Visibility',''),
    })

# Create directories
os.makedirs('.migration/pxp3', exist_ok=True)

# Sanitized snapshot for Worker B
with open('.migration/pxp3/registry-sanitized.json', 'w', encoding='utf-8') as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=2)

# Rollback data
with open('.migration/pxp3/rollback-live-registry.json', 'w', encoding='utf-8') as f:
    json.dump(rollback, f, ensure_ascii=False, indent=2)

# Summary
cats = Counter(r['Category'] for r in snapshot)
statuses = Counter(r['Status'] for r in snapshot)
vis = Counter(r['Visibility'] for r in snapshot)
with_url = sum(1 for r in snapshot if r['StorageURL'])

summary = {
    'total': len(snapshot),
    'with_storage_url': with_url,
    'without_storage_url': len(snapshot) - with_url,
    'by_category': dict(cats),
    'by_status': dict(statuses),
    'by_visibility': dict(vis),
}
print(json.dumps(summary, indent=2, ensure_ascii=False))
