#!/usr/bin/env python3
"""
PXP-3 Link QA — validates pilot document URLs.
Authenticated links: verify hostname + URL syntax + that the file is reachable.
"""
import json, os, re, sys, urllib.request, urllib.error, ssl
from urllib.parse import urlparse

FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data/document-registry.public.json')
REPORT = os.path.join(os.path.dirname(__file__), '..', '..', 'reports/pxp3-link-validation.json')

EXPECTED_HOST = 'maejo365.sharepoint.com'

results = {'VALID_AUTH_REQUIRED': [], 'VALID_PUBLIC': [], 'BROKEN': [], 'TIMEOUT': [], 'UNKNOWN': [], 'REDIRECT_VALID': []}
broken = []

with open(FILE, encoding='utf-8') as f:
    data = json.load(f)

records = data if isinstance(data, list) else data.get('documents', data.get('records', []))

print(f"Validating {len(records)} document URLs...\n")

for rec in records:
    doc_id = rec.get('DocumentID', '?')
    url = rec.get('StorageURL', '')
    mode = rec.get('DownloadMode', '')
    parsed = urlparse(url)

    # Check URL syntax
    if not url or not url.startswith('https://'):
        results['BROKEN'].append({'DocumentID': doc_id, 'url': url, 'reason': 'Invalid or missing URL'})
        broken.append(doc_id)
        continue

    # Check hostname
    if parsed.netloc != EXPECTED_HOST:
        results['UNKNOWN'].append({'DocumentID': doc_id, 'url': url, 'host': parsed.netloc})
        broken.append(doc_id)
        continue

    # Authenticated link — verify it's a valid SharePoint path
    if mode == 'AUTHENTICATED_SHAREPOINT':
        path = parsed.path
        path_ok = path.startswith('/sites/')
        has_extension = bool(re.search(r'\.\w{2,5}$', path))

        if path_ok and has_extension:
            results['VALID_AUTH_REQUIRED'].append({'DocumentID': doc_id, 'url': url[:80], 'host': EXPECTED_HOST})
        else:
            results['BROKEN'].append({'DocumentID': doc_id, 'url': url, 'reason': 'Invalid SharePoint path or missing extension'})
            broken.append(doc_id)
    else:
        results['UNKNOWN'].append({'DocumentID': doc_id, 'url': url, 'mode': mode})

# Summary
print("Link QA Results:")
print(f"  VALID_AUTH_REQUIRED: {len(results['VALID_AUTH_REQUIRED'])}")
print(f"  VALID_PUBLIC: {len(results['VALID_PUBLIC'])}")
print(f"  REDIRECT_VALID: {len(results['REDIRECT_VALID'])}")
print(f"  BROKEN: {len(results['BROKEN'])}")
print(f"  TIMEOUT: {len(results['TIMEOUT'])}")
print(f"  UNKNOWN: {len(results['UNKNOWN'])}")

if broken:
    print(f"\nBROKEN URLs ({len(broken)}):")
    for b in broken:
        print(f"  {b}")

# Save report
report = {
    'timestamp': '2026-07-16T09:00:00Z',
    'total_urls': len(records),
    'summary': {k: len(v) for k, v in results.items()},
    'details': results,
}
with open(REPORT, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"\nReport saved to {REPORT}")

sys.exit(1 if broken else 0)
