#!/usr/bin/env python3
"""
PXP-3 Publish Pilot — updates live Registry records to Status=current, Visibility=public.
Uses Playwright auth + SharePoint REST API ValidateUpdateListItem.
Batch size: 6-12 records per group.
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '.migration', 'rae-wtms', 'tools'))
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from playwright.sync_api import sync_playwright
import requests

SITE = SITE_DEFAULT.rstrip('/')
CANDIDATES = os.path.join(os.path.dirname(__file__), '..', '..', 'reports/pxp3-pilot-candidates.json')

def main():
    with open(CANDIDATES, encoding='utf-8') as f:
        data = json.load(f)
    candidates = data['candidates']

    print(f"Publishing {len(candidates)} pilot records...")
    print("=" * 50)

    # Authenticate
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

    # Process in batches of 8
    batch_size = 8
    results = {'published': [], 'failed': [], 'total': len(candidates)}

    for i in range(0, len(candidates), batch_size):
        batch = candidates[i:i+batch_size]
        batch_num = i//batch_size + 1
        print(f"\nBatch {batch_num} ({len(batch)} records):")

        for rec in batch:
            doc_id = rec['DocumentID']
            list_item_id = rec['ListItemId']
            old_status = rec['Status']
            old_visibility = rec['Visibility']

            url = f"{SITE}/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items({list_item_id})/ValidateUpdateListItem"
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
                        err_msg = json.dumps(errs)[:200]
                        results['failed'].append({'DocumentID': doc_id, 'error': err_msg})
                        print(f"  {doc_id}: FIELD ERROR - {err_msg}")
                    else:
                        results['published'].append(doc_id)
                        print(f"  {doc_id}: Status=current, Visibility=public")
                else:
                    results['failed'].append({'DocumentID': doc_id, 'error': f'HTTP {resp.status_code}'})
                    print(f"  {doc_id}: FAILED (HTTP {resp.status_code})")
            except Exception as e:
                results['failed'].append({'DocumentID': doc_id, 'error': str(e)})
                print(f"  {doc_id}: EXCEPTION - {e}")

            time.sleep(0.3)  # Gentle throttle

        # Verify batch: re-read updated records
        print(f"\n  Verifying batch {batch_num}...")
        for rec in batch:
            doc_id = rec['DocumentID']
            list_item_id = rec['ListItemId']
            verify_url = f"{SITE}/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items({list_item_id})?$select=Status,Visibility"
            try:
                vresp = requests.get(verify_url, headers=headers, timeout=30)
                if vresp.status_code == 200:
                    vdata = vresp.json()
                    vrow = vdata.get('d', {})
                    vs = vrow.get('Status', '')
                    vv = vrow.get('Visibility', '')
                    status_ok = vs.lower() == 'current'
                    vis_ok = vv.lower() == 'public'
                    if not status_ok or not vis_ok:
                        print(f"  {doc_id}: VERIFY MISMATCH - Status={vs}, Visibility={vv}")
                else:
                    print(f"  {doc_id}: VERIFY FAILED (HTTP {vresp.status_code})")
            except Exception as e:
                print(f"  {doc_id}: VERIFY EXCEPTION - {e}")

    # Summary
    print("\n" + "=" * 50)
    print(f"Pilot publication complete:")
    print(f"  Published: {len(results['published'])}")
    print(f"  Failed: {len(results['failed'])}")

    # Save results
    results['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    out_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports/pxp3-publish-results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {out_path}")

    if results['failed']:
        print(f"\nFAILED records:")
        for f in results['failed']:
            print(f"  {f['DocumentID']}: {f['error']}")

    sys.exit(0 if not results['failed'] else 1)

if __name__ == '__main__':
    main()
