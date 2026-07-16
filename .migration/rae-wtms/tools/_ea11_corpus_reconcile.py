#!/usr/bin/env python3
"""EA-11 corpus reconciliation — manifest vs SharePoint vs Registry with pagination."""
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from _registry_upsert import build_scan_libs_js, storage_url

REPO = r'G:\ProjectAI\document-center'
ROOT = os.path.join(REPO, '.migration', 'rae-wtms')
EA11 = os.path.join(ROOT, 'ea-11')
MANIFEST = os.path.join(REPO, 'migration', 'sharepoint-migration-manifest.csv')
LIBS = {
    'Administration', 'FinanceProcurement', 'PlanningPolicy',
    'AcademicServices', 'Research', 'SOPManuals',
}
CAT_MAP = {
    'Administration': 'admin',
    'FinanceProcurement': 'finance-procurement',
    'Research': 'research',
    'AcademicServices': 'academic-service',
    'PlanningPolicy': 'policy-planning',
    'SOPManuals': 'manuals',
}


def registry_scan_paginated_js():
    return """(async function(){
var s=_spPageContextInfo.webServerRelativeUrl,out=[],skip=0,top=500,pages=0;
while(true){
var r=await fetch(s+"/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items?$select=Id,Title,Document_x0020_ID,Category,Status,Visibility,Storage_x0020_URL&$top="+top+"&$skip="+skip,{headers:{'accept':'application/json;odata=verbose'}});
if(!r.ok) return {error:'HTTP_'+r.status,rows:out,pages:pages};
var j=await r.json(),rows=j.d.results||[]; pages++;
for(var i=0;i<rows.length;i++){
var x=rows[i],st=x.Storage_x0020_URL;
out.push({id:x.Id,document_id:x.Document_x0020_ID||'',title:x.Title||'',category:x.Category||'',status:x.Status||'',visibility:x.Visibility||'',storage:(st&&st.Url)?st.Url:''});
}
if(rows.length<top) break; skip+=top;
}
return {rows:out,pages:pages,total:out.length};
})()"""


def load_manifest_ready():
    with open(MANIFEST, encoding='utf-8-sig') as f:
        return {
            r['DocumentID']: r for r in csv.DictReader(f)
            if r.get('MigrationStatus') == 'Ready' and r.get('LocalRelativePath', '').strip()
        }


def classify_issue(manifest, sp, reg):
    issues = []
    for doc_id, m in manifest.items():
        s = sp.get(doc_id)
        r = reg.get(doc_id)
        if not s and not r:
            issues.append({'DocumentID': doc_id, 'Classification': 'MISSING_SHAREPOINT', 'Detail': 'not in library or registry'})
        elif not s and r:
            issues.append({'DocumentID': doc_id, 'Classification': 'MISSING_SHAREPOINT', 'Detail': 'registry only'})
        elif s and not r:
            issues.append({'DocumentID': doc_id, 'Classification': 'MISSING_REGISTRY', 'Detail': 'library only'})
        elif s and r:
            if m.get('TargetLibrary') != s.get('lib'):
                issues.append({'DocumentID': doc_id, 'Classification': 'WRONG_LIBRARY', 'Detail': f"manifest={m.get('TargetLibrary')} sp={s.get('lib')}"})
            url = r.get('storage', '')
            if '/sites/msteams_54adc4/sites/' in url:
                issues.append({'DocumentID': doc_id, 'Classification': 'MALFORMED_STORAGE_URL', 'Detail': url[:120]})
            elif url and s.get('file_ref') and storage_url(s['file_ref']) not in url and doc_id not in url:
                issues.append({'DocumentID': doc_id, 'Classification': 'METADATA_MISMATCH', 'Detail': 'storage url mismatch'})
    sp_extra = set(sp) - set(manifest)
    reg_extra = set(reg) - set(manifest)
    for doc_id in sp_extra:
        issues.append({'DocumentID': doc_id, 'Classification': 'DUPLICATE_SHAREPOINT', 'Detail': 'not in manifest READY'})
    for doc_id in reg_extra:
        issues.append({'DocumentID': doc_id, 'Classification': 'DUPLICATE_REGISTRY', 'Detail': 'not in manifest READY'})
    return issues


def main():
    os.makedirs(EA11, exist_ok=True)
    manifest = load_manifest_ready()

    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=True)
        page = ensure_authenticated(get_page(ctx))
        print('Authenticated, scanning libraries...', flush=True)
        page.goto(f'{SITE_DEFAULT}/Administration/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
        lib_raw = page.evaluate(build_scan_libs_js())
        print(f'Library scan: {len(lib_raw)} items', flush=True)
        reg_pack = page.evaluate(registry_scan_paginated_js())
        print(f'Registry scan: {reg_pack.get("total", 0)} items, {reg_pack.get("pages", 0)} pages', flush=True)
        close_context(ctx)

    sp = {}
    for item in lib_raw:
        if item.get('error') or not item.get('document_id'):
            continue
        sp[item['document_id']] = item

    reg = {}
    reg_rows = reg_pack.get('rows', []) if isinstance(reg_pack, dict) else []
    for item in reg_rows:
        if item.get('document_id'):
            reg[item['document_id']] = item

    reg_dups = [k for k, v in Counter(r['document_id'] for r in reg_rows if r.get('document_id')).items() if v > 1]
    sp_dups = [k for k, v in Counter(s['document_id'] for s in sp.values()).items() if v > 1]

    issues = classify_issue(manifest, sp, reg)
    broken = [i for i in issues if i['Classification'] in ('MALFORMED_STORAGE_URL', 'BROKEN_STORAGE_URL')]

    summary = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'MANIFEST_READY_IDS': len(manifest),
        'SHAREPOINT_DOCUMENT_IDS': len(sp),
        'REGISTRY_DOCUMENT_IDS': len(reg),
        'REGISTRY_PAGES': reg_pack.get('pages', 0),
        'sets_equal': len(manifest) == len(sp) == len(reg) and not issues,
        'manifest_minus_sp': len(set(manifest) - set(sp)),
        'manifest_minus_reg': len(set(manifest) - set(reg)),
        'sp_minus_manifest': len(set(sp) - set(manifest)),
        'reg_minus_manifest': len(set(reg) - set(manifest)),
        'duplicate_sharepoint': sp_dups,
        'duplicate_registry': reg_dups,
        'broken_url_count': len(broken),
        'exception_count': len(issues),
        'by_library': dict(Counter(v['lib'] for v in sp.values())),
        'by_registry_category': dict(Counter(v.get('category') for v in reg.values())),
    }

    recon_rows = []
    all_ids = sorted(set(manifest) | set(sp) | set(reg), key=lambda x: int(x.split('-')[1]))
    for doc_id in all_ids:
        m = manifest.get(doc_id, {})
        s = sp.get(doc_id, {})
        r = reg.get(doc_id, {})
        status = 'COMPLETE'
        if doc_id not in manifest:
            status = 'EXTRA'
        elif doc_id not in sp:
            status = 'MISSING_SHAREPOINT'
        elif doc_id not in reg:
            status = 'MISSING_REGISTRY'
        recon_rows.append({
            'DocumentID': doc_id,
            'Status': status,
            'TargetLibrary': m.get('TargetLibrary', s.get('lib', '')),
            'RegistryCategory': r.get('category', ''),
            'StorageURL': r.get('storage', storage_url(s.get('file_ref', ''))),
            'RegistryStatus': r.get('status', ''),
            'RegistryVisibility': r.get('visibility', ''),
        })

    fields = list(recon_rows[0].keys()) if recon_rows else ['DocumentID', 'Status']
    with open(os.path.join(EA11, 'ea-11-corpus-reconciliation.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(recon_rows)

    with open(os.path.join(EA11, 'ea-11-corpus-summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    exc = [i for i in issues if i['Classification'] not in ('DUPLICATE_SHAREPOINT', 'DUPLICATE_REGISTRY') or True]
    with open(os.path.join(EA11, 'ea-11-exceptions.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['DocumentID', 'Classification', 'Detail'])
        w.writeheader()
        w.writerows(exc if exc else [])

    print(json.dumps(summary, indent=2))
    sys.exit(0 if summary['sets_equal'] and not reg_dups and not broken else 1)


if __name__ == '__main__':
    main()
