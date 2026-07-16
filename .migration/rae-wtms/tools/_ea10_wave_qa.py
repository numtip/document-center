#!/usr/bin/env python3
"""EA-10 wave-level QA report and registry sync trigger."""
import argparse
import csv
import json
import os
import random
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from _registry_upsert import build_count_duplicates_js, build_scan_libs_js

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
SEL = os.path.join(EA10, 'ea-10-selection.csv')
RES = os.path.join(EA10, 'ea-10-results.csv')
STATE = os.path.join(EA10, 'ea-10-state.json')
LIBS = [
    'Administration', 'FinanceProcurement', 'PlanningPolicy',
    'AcademicServices', 'SOPManuals', 'Research',
]


def load_csv(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def url_check_js(url):
    u = json.dumps(url, ensure_ascii=True)
    return f"""(async function(){{
try{{
var r=await fetch({u},{{method:'GET',credentials:'include',redirect:'follow'}});
return {{status:r.status,ok:r.ok,finalUrl:r.url}};
}}catch(e){{return {{status:0,ok:false,error:e.message}}}}
}})()"""


def search_js(query):
    q = json.dumps(query, ensure_ascii=True)
    return f"""(async function(){{
var ctx=_spPageContextInfo,s=ctx.webServerRelativeUrl;
var url=s+'/_api/search/query?querytext=%27'+encodeURIComponent({q})+'%27&rowlimit=20&selectproperties=%27Path,Title,Filename%27';
try{{
var r=await fetch(url,{{headers:{{'accept':'application/json;odata=verbose'}}}});
if(!r.ok) return 'HTTP_'+r.status;
var j=await r.json(),rows=j.d.query.PrimaryQueryResult.RelevantResults.Table.Rows.results||[];
return JSON.stringify(rows.map(x=>{{
var c={{}};x.Cells.results.forEach(cell=>c[cell.Key]=cell.Value);return c;
}}));
}}catch(e){{return 'FAIL:'+e.message}}
}})()"""


def classify_hits(hits, doc_id):
    if not hits:
        return 'NOT_FOUND'
    for h in hits:
        blob = (h.get('Path') or '') + (h.get('Filename') or '') + (h.get('Title') or '')
        if doc_id in blob:
            return 'FOUND'
    return 'PENDING_INDEX'


def pick_spot_samples(wave_rows, res_map):
    by_lib = defaultdict(list)
    by_tier = defaultdict(list)
    for r in wave_rows:
        doc_id = r['DocumentID']
        rr = res_map.get(doc_id, {})
        if rr.get('UploadStatus') != 'OK':
            continue
        by_lib[r['TargetLibrary']].append(r)
        by_tier[r.get('SizeTier', 'medium')].append(r)

    picks = []
    random.seed(42 + int(wave_rows[0].get('Wave', 1)))
    for lib in LIBS:
        pool = by_lib.get(lib, [])
        if pool:
            picks.append(random.choice(pool))
    for tier in ('small', 'medium', 'large', 'xlarge'):
        pool = by_tier.get(tier, [])
        if pool and len(picks) < 20:
            picks.append(random.choice(pool))
    return picks[:15]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wave', type=int, required=True)
    ap.add_argument('--fast', action='store_true', help='Minimal spot QA, no search')
    args = ap.parse_args()

    sel = load_csv(SEL)
    res_list = load_csv(RES) if os.path.exists(RES) else []
    res_map = {r['DocumentID']: r for r in res_list}
    wave_rows = [r for r in sel if int(r.get('Wave', 0)) == args.wave]
    wave_results = [res_map.get(r['DocumentID'], {}) for r in wave_rows]

    batch_tags = sorted({r.get('BatchTag', r.get('BatchID', '')) for r in wave_rows})
    batch_metrics = {}
    for tag in batch_tags:
        batch_rows = [r for r in wave_rows if r.get('BatchTag') == tag or r.get('BatchID') == tag]
        ok = sum(1 for r in batch_rows if res_map.get(r['DocumentID'], {}).get('UploadStatus') == 'OK')
        batch_metrics[tag] = {'expected': len(batch_rows), 'upload_ok': ok}

    upload_ok = sum(1 for r in wave_results if r.get('UploadStatus') == 'OK')
    registry_ok = sum(1 for r in wave_results if r.get('RegistryStatus') in ('AUTO_UPSERT', 'OK'))
    failed = len(wave_rows) - upload_ok
    durs = [float(r['DurationSec']) for r in wave_results if r.get('DurationSec') and r.get('UploadStatus') == 'OK']

    report = {
        'wave': args.wave,
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'expected': len(wave_rows),
        'UPLOAD_SUCCESS': upload_ok,
        'REGISTRY_SUCCESS': registry_ok,
        'FAILED': failed,
        'batch_metrics': batch_metrics,
        'gate_pass': failed == 0 and upload_ok == len(wave_rows) and registry_ok == upload_ok,
        'performance': {
            'avg_sec_per_doc': round(statistics.mean(durs), 1) if durs else 0,
            'median_sec': round(statistics.median(durs), 1) if durs else 0,
            'max_sec': max(durs) if durs else 0,
        },
        'spot_qa': [],
        'search': [],
        'registry_sync': {},
        'library_counts': {},
    }

    samples = pick_spot_samples(wave_rows, res_map)
    with sync_playwright() as p:
        context = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(context))
        page.goto(f'{SITE_DEFAULT}/Administration/Forms/AllItems.aspx?sw=bypass', timeout=120000)
        page.wait_for_function('typeof _spPageContextInfo !== "undefined"', timeout=120000)

        scan = page.evaluate(build_scan_libs_js())
        lib_counts = Counter()
        for item in scan:
            if not item.get('error'):
                lib_counts[item['lib']] += 1
        report['library_counts'] = dict(lib_counts)

        dup = page.evaluate(build_count_duplicates_js())
        report['registry_dup_check'] = dup

        for r in samples[:3 if args.fast else 8]:
            rr = res_map.get(r['DocumentID'], {})
            rel = rr.get('SharePointURL', '')
            abs_url = ('https://maejo365.sharepoint.com' + rel) if rel.startswith('/') else rel
            bad = '/sites/msteams_54adc4/sites/' in abs_url
            chk = page.evaluate(url_check_js(abs_url)) if abs_url and not bad else {'ok': False}
            report['spot_qa'].append({
                'DocumentID': r['DocumentID'],
                'TargetLibrary': r['TargetLibrary'],
                'SizeTier': r.get('SizeTier'),
                'url_ok': bool(chk.get('ok')),
                'bad_path': bad,
            })

        if not args.fast:
            thai = next((r for r in samples if any('\u0e00' <= c <= '\u0e7f' for c in r.get('Title', ''))), samples[0] if samples else None)
            if thai:
                raw = page.evaluate(search_js(thai.get('Title', '')[:20]))
                hits = json.loads(raw) if isinstance(raw, str) and raw.startswith('[') else []
                report['search'].append({
                    'query': thai.get('Title', '')[:20],
                    'doc_id': thai['DocumentID'],
                    'kind': 'thai_title',
                    'classification': classify_hits(hits, thai['DocumentID']),
                })
            if samples:
                fn = os.path.basename(res_map.get(samples[0]['DocumentID'], {}).get('SharePointURL', ''))
                if fn:
                    raw = page.evaluate(search_js(fn))
                    hits = json.loads(raw) if isinstance(raw, str) and raw.startswith('[') else []
                    report['search'].append({
                        'query': fn, 'doc_id': samples[0]['DocumentID'],
                        'kind': 'filename', 'classification': classify_hits(hits, samples[0]['DocumentID']),
                    })
        else:
            report['search'] = [{'skipped': 'fast_mode'}]

        close_context(context)

    out_path = os.path.join(EA10, f'ea-10-wave-{args.wave:02d}-report.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    if os.path.exists(STATE):
        with open(STATE, encoding='utf-8') as f:
            state = json.load(f)
        state.setdefault('waves', {})[str(args.wave)] = report
        with open(STATE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report['gate_pass'] else 1)


if __name__ == '__main__':
    main()
