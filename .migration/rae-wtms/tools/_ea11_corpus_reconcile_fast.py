#!/usr/bin/env python3
"""EA-11 corpus reconciliation — artifacts + live Registry paginated scan."""
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent

REPO = r'G:\ProjectAI\document-center'
ROOT = os.path.join(REPO, '.migration', 'rae-wtms')
EA11 = os.path.join(ROOT, 'ea-11')
MANIFEST = os.path.join(REPO, 'migration', 'sharepoint-migration-manifest.csv')
EA6 = {'RAE-00009', 'RAE-00046', 'RAE-00146', 'RAE-00195', 'RAE-00662', 'RAE-00119'}


def registry_scan_js():
    return """(async function(){
var s=_spPageContextInfo.webServerRelativeUrl,out=[],skip=0,top=500,pages=0;
while(true){
var r=await fetch(s+"/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items?$select=Id,Document_x0020_ID,Category,Status,Visibility,Storage_x0020_URL&$top="+top+"&$skip="+skip,{headers:{'accept':'application/json;odata=verbose'}});
if(!r.ok) return {error:'HTTP_'+r.status,rows:out,pages:pages,total:out.length};
var j=await r.json(),rows=j.d.results||[]; pages++;
for(var i=0;i<rows.length;i++){
var x=rows[i],st=x.Storage_x0020_URL;
out.push({document_id:x.Document_x0020_ID||'',category:x.Category||'',status:x.Status||'',visibility:x.Visibility||'',storage:(st&&st.Url)?st.Url:''});
}
if(rows.length<top) break; skip+=top;
}
return {rows:out,pages:pages,total:out.length};
})()"""


def load_sharepoint_from_results():
    ids = {}
    for rel in [
        os.path.join(ROOT, 'pilot', 'ea-7a-results.csv'),
        os.path.join(ROOT, 'pilot', 'ea-9-results.csv'),
        os.path.join(ROOT, 'ea-10', 'ea-10-results.csv'),
    ]:
        if not os.path.exists(rel):
            continue
        with open(rel, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r.get('UploadStatus') == 'OK' and r.get('SharePointURL') and r.get('RegistryItemID'):
                    ids[r['DocumentID']] = {
                        'lib': r.get('TargetLibrary', ''),
                        'url': r.get('SharePointURL', ''),
                        'reg_id': r.get('RegistryItemID', ''),
                    }
    for d in EA6:
        if d not in ids:
            ids[d] = {'lib': '', 'url': '', 'reg_id': ''}
    return ids


def main():
    os.makedirs(EA11, exist_ok=True)
    with open(MANIFEST, encoding='utf-8-sig') as f:
        manifest = {
            r['DocumentID']: r for r in csv.DictReader(f)
            if r.get('MigrationStatus') == 'Ready' and r.get('LocalRelativePath', '').strip()
        }
    sp = load_sharepoint_from_results()

    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=True)
        page = ensure_authenticated(get_page(ctx))
        page.goto(f'{SITE_DEFAULT}/Administration/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
        reg_pack = page.evaluate(registry_scan_js())
        close_context(ctx)

    reg_rows = reg_pack.get('rows', [])
    reg = {r['document_id']: r for r in reg_rows if r.get('document_id')}
    reg_dups = [k for k, v in Counter(r['document_id'] for r in reg_rows if r.get('document_id')).items() if v > 1]

    issues = []
    broken = 0
    for doc_id, m in manifest.items():
        s = sp.get(doc_id)
        r = reg.get(doc_id)
        if not s or not s.get('url'):
            issues.append({'DocumentID': doc_id, 'Classification': 'MISSING_SHAREPOINT', 'Detail': 'no result record'})
        if not r:
            issues.append({'DocumentID': doc_id, 'Classification': 'MISSING_REGISTRY', 'Detail': 'not in registry scan'})
        elif s and m.get('TargetLibrary') != s.get('lib') and s.get('lib'):
            issues.append({'DocumentID': doc_id, 'Classification': 'WRONG_LIBRARY', 'Detail': m.get('TargetLibrary') + ' vs ' + s.get('lib')})
        storage = r.get('storage', '') if r else ''
        if storage and '/sites/msteams_54adc4/sites/' in storage:
            issues.append({'DocumentID': doc_id, 'Classification': 'MALFORMED_STORAGE_URL', 'Detail': storage[:100]})
            broken += 1
        if s and s.get('url') and '/sites/msteams_54adc4/sites/' in s['url']:
            broken += 1

    summary = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'MANIFEST_READY_IDS': len(manifest),
        'SHAREPOINT_DOCUMENT_IDS': len([d for d in manifest if sp.get(d, {}).get('url')]),
        'REGISTRY_DOCUMENT_IDS': len(reg),
        'REGISTRY_PAGES': reg_pack.get('pages', 0),
        'REGISTRY_PAGINATION_TOTAL': reg_pack.get('total', len(reg)),
        'sets_equal': len(manifest) == len(sp) == len(reg) and not issues,
        'duplicate_registry': reg_dups,
        'broken_url_count': broken,
        'exception_count': len(issues),
        'evidence': 'manifest + migration_results + live_registry_paginated_scan',
    }

    recon = []
    for doc_id in sorted(manifest, key=lambda x: int(x.split('-')[1])):
        status = 'COMPLETE' if doc_id in sp and doc_id in reg and not any(i['DocumentID']==doc_id for i in issues) else 'EXCEPTION'
        if doc_id not in sp:
            status = 'MISSING_SHAREPOINT'
        elif doc_id not in reg:
            status = 'MISSING_REGISTRY'
        recon.append({
            'DocumentID': doc_id,
            'Status': status,
            'TargetLibrary': manifest[doc_id].get('TargetLibrary', ''),
            'StorageURL': reg.get(doc_id, {}).get('storage', sp.get(doc_id, {}).get('url', '')),
        })

    with open(os.path.join(EA11, 'ea-11-corpus-summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with open(os.path.join(EA11, 'ea-11-corpus-reconciliation.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=recon[0].keys())
        w.writeheader()
        w.writerows(recon)
    with open(os.path.join(EA11, 'ea-11-exceptions.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['DocumentID', 'Classification', 'Detail'])
        w.writeheader()
        w.writerows(issues)

    print(json.dumps(summary, indent=2))
    sys.exit(0 if summary['MANIFEST_READY_IDS'] == summary['REGISTRY_DOCUMENT_IDS'] == 627 and not reg_dups and broken == 0 else 1)


if __name__ == '__main__':
    main()
