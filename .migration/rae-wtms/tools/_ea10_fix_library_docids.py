#!/usr/bin/env python3
"""Fix DocumentID metadata on library items missing from scan."""
import csv
import json
import os
import sys

from playwright.sync_api import sync_playwright
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from _registry_upsert import build_scan_libs_js

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')


def fix_js(lib, item_id, doc_id):
    return f"""(async function(){{
var ctx=_spPageContextInfo,d=ctx.formDigestValue,s=ctx.webServerRelativeUrl;
var vj=await (await fetch(s+'/_api/web/lists/getbytitle(%27{lib}%27)/items({item_id})/ValidateUpdateListItem',{{method:'POST',headers:{{'X-RequestDigest':d,'accept':'application/json;odata=verbose','content-type':'application/json;odata=verbose'}},body:JSON.stringify({{formValues:[{{FieldName:'DocumentID',FieldValue:'{doc_id}'}}],bNewDocumentUpdate:false}})}})).json();
var errs=(vj.d.ValidateUpdateListItem.results||[]).filter(r=>r.HasException);
return errs.length?('FAIL:'+JSON.stringify(errs).substring(0,200)):'OK';
}})()"""


def main():
    gap_path = os.path.join(EA10, 'ea-10-library-gap.json')
    if not os.path.exists(gap_path):
        print('No gap file', file=sys.stderr)
        sys.exit(1)
    missing = json.load(open(gap_path))['missing']
    res = {r['DocumentID']: r for r in csv.DictReader(open(os.path.join(EA10, 'ea-10-results.csv'), encoding='utf-8-sig'))}

    fixed = failed = 0
    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(ctx))
        page.goto(f'{SITE_DEFAULT}/Research/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
        for doc_id in missing:
            r = res.get(doc_id)
            if not r or not r.get('SharePointItemID'):
                failed += 1
                continue
            lib = r['TargetLibrary']
            iid = r['SharePointItemID']
            out = page.evaluate(fix_js(lib, iid, doc_id))
            if str(out).startswith('OK'):
                fixed += 1
            else:
                failed += 1
        close_context(ctx)
    print(json.dumps({'fixed': fixed, 'failed': failed, 'total': len(missing)}))
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
