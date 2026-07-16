#!/usr/bin/env python3
"""EA-11 public access and URL QA samples via Worker M365."""
import csv
import json
import os
import random
import sys
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA11 = os.path.join(ROOT, 'ea-11')
EA10_RES = os.path.join(ROOT, 'ea-10', 'ea-10-results.csv')
GAP = os.path.join(ROOT, 'ea-10', 'ea-10-library-gap.json')
LIBS = ['Administration', 'FinanceProcurement', 'PlanningPolicy', 'AcademicServices', 'SOPManuals', 'Research']


def url_check_js(url):
    u = json.dumps(url, ensure_ascii=True)
    return f"""(async function(){{
try{{
var r=await fetch({u},{{method:'GET',credentials:'include',redirect:'follow'}});
return {{status:r.status,ok:r.ok,finalUrl:r.url}};
}}catch(e){{return {{status:0,ok:false,error:e.message}}}}
}})()"""


def anon_check_js(url):
    u = json.dumps(url, ensure_ascii=True)
    return f"""(async function(){{
try{{
var r=await fetch({u},{{method:'HEAD',credentials:'omit',redirect:'follow'}});
return {{status:r.status,ok:r.ok}};
}}catch(e){{return {{status:0,ok:false,error:e.message}}}}
}})()"""


def pick_samples():
    rows = list(csv.DictReader(open(EA10_RES, encoding='utf-8-sig')))
    ok = [r for r in rows if r.get('UploadStatus') == 'OK']
    by_lib = {lib: [] for lib in LIBS}
    by_tier = {'small': [], 'medium': [], 'large': [], 'xlarge': []}
    thai = []
    gap_ids = set()
    if os.path.exists(GAP):
        gap_ids = set(json.load(open(GAP, encoding='utf-8')).get('missing', []))
    wave5 = []
    for r in ok:
        by_lib.setdefault(r['TargetLibrary'], []).append(r)
        by_tier.setdefault(r.get('SizeTier', 'medium'), []).append(r)
        if any('\u0e00' <= c <= '\u0e7f' for c in r.get('Title', '')):
            thai.append(r)
        if int(r.get('Sequence', 0)) >= 401:
            wave5.append(r)
    random.seed(11)
    picks = []
    seen = set()

    def add(r):
        if r['DocumentID'] not in seen:
            picks.append(r)
            seen.add(r['DocumentID'])

    for lib in LIBS:
        pool = by_lib.get(lib, [])
        for r in random.sample(pool, min(10, len(pool))):
            add(r)
    for tier in ('small', 'medium', 'large', 'xlarge'):
        pool = by_tier.get(tier, [])
        if pool:
            add(random.choice(pool))
    for r in thai[:3]:
        add(r)
    for r in wave5[:5]:
        add(r)
    for did in list(gap_ids)[:5]:
        r = next((x for x in ok if x['DocumentID'] == did), None)
        if r:
            add(r)
    ext_seen = set()
    for r in ok:
        ext = os.path.splitext(r.get('SharePointURL', ''))[1].lower()
        if ext and ext not in ext_seen:
            add(r)
            ext_seen.add(ext)
    return picks


def classify_auth(status, ok):
    if ok:
        return 'PUBLIC_PASS'
    if status in (401, 403):
        return 'AUTH_REQUIRED'
    if status in (0,):
        return 'TIMEOUT'
    if status >= 400:
        return 'BROKEN'
    return 'AUTH_REQUIRED'


def main():
    os.makedirs(EA11, exist_ok=True)
    samples = pick_samples()
    results = []
    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(ctx))
        page.goto(f'{SITE_DEFAULT}/Administration/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)
        for r in samples:
            rel = r.get('SharePointURL', '')
            url = ('https://maejo365.sharepoint.com' + rel) if rel.startswith('/') else rel
            bad = '/sites/msteams_54adc4/sites/' in url
            auth = page.evaluate(url_check_js(url)) if url and not bad else {'ok': False, 'status': 0}
            anon = page.evaluate(anon_check_js(url)) if url and not bad else {'ok': False, 'status': 0}
            results.append({
                'DocumentID': r['DocumentID'],
                'TargetLibrary': r['TargetLibrary'],
                'SizeTier': r.get('SizeTier', ''),
                'StorageURL': url,
                'AuthSession': 'PUBLIC_PASS' if auth.get('ok') else 'BROKEN',
                'AnonymousAccess': classify_auth(anon.get('status'), anon.get('ok')),
                'BadDuplicatePath': bad,
                'HttpStatus': auth.get('status', 0),
            })
        close_context(ctx)

    fields = list(results[0].keys()) if results else []
    with open(os.path.join(EA11, 'ea-11-public-access-tests.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    pass_auth = sum(1 for x in results if x['AuthSession'] == 'PUBLIC_PASS' and not x['BadDuplicatePath'])
    summary = {
        'sampled': len(results),
        'auth_pass': pass_auth,
        'auth_fail': len(results) - pass_auth,
        'anon_pass': sum(1 for x in results if x['AnonymousAccess'] == 'PUBLIC_PASS'),
        'auth_required': sum(1 for x in results if x['AnonymousAccess'] == 'AUTH_REQUIRED'),
        'broken': sum(1 for x in results if x['AnonymousAccess'] == 'BROKEN'),
        'bad_paths': sum(1 for x in results if x['BadDuplicatePath']),
    }
    print(json.dumps(summary, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    main()
