#!/usr/bin/env python3
"""Inspect library item fields for gap documents."""
import csv
import json
import sys
from playwright.sync_api import sync_playwright
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = ROOT + r'\ea-10'


def inspect_js(lib, item_id):
    return f"""(async function(){{
var s=_spPageContextInfo.webServerRelativeUrl;
var r=await fetch(s+'/_api/web/lists/getbytitle(%27{lib}%27)/items({item_id})?$select=Id,Title,DocumentID,FileRef',{{headers:{{'accept':'application/json;odata=verbose'}}}});
return await r.json();
}})()"""


def main():
    res = {r['DocumentID']: r for r in csv.DictReader(open(EA10 + r'\ea-10-results.csv', encoding='utf-8-sig'))}
    did = sys.argv[1] if len(sys.argv) > 1 else 'RAE-00634'
    r = res[did]
    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(ctx))
        page.goto(f'{SITE_DEFAULT}/Research/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
        out = page.evaluate(inspect_js(r['TargetLibrary'], r['SharePointItemID']))
        close_context(ctx)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
