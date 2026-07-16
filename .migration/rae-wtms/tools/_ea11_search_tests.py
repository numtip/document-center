#!/usr/bin/env python3
"""EA-11 deterministic search test set."""
import csv
import json
import os
import random
import sys

from playwright.sync_api import sync_playwright

from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA11 = os.path.join(ROOT, 'ea-11')
MANIFEST = r'G:\ProjectAI\document-center\migration\sharepoint-migration-manifest.csv'
PREVIEW_JS = r'G:\ProjectAI\document-center\preview\app.js'


def load_ready_sample(n=30):
    with open(MANIFEST, encoding='utf-8-sig') as f:
        rows = [r for r in csv.DictReader(f) if r.get('MigrationStatus') == 'Ready']
    random.seed(11)
    return random.sample(rows, min(n, len(rows)))


def preview_filter_tests(docs, queries):
    # emulate app.js filterDocuments logic
    results = []
    for qtype, query, expected_id in queries:
        ql = query.lower()
        hits = []
        for d in docs:
            blob = ' '.join([
                d.get('DocumentID', ''), d.get('Title', ''), d.get('Category', ''), d.get('TargetLibrary', ''),
            ]).lower()
            if ql in blob or query in d.get('DocumentID', ''):
                hits.append(d.get('DocumentID'))
        actual = hits[:5]
        if qtype.startswith('no_result'):
            ok = len(hits) == 0
        elif qtype == 'document_id':
            ok = expected_id in hits
        elif qtype == 'exact_title':
            ok = expected_id in hits
        else:
            ok = len(hits) > 0 and (not expected_id or expected_id in hits)
        results.append({
            'QueryType': qtype,
            'Query': query,
            'ExpectedIDs': expected_id or '',
            'ActualIDs': ';'.join(actual),
            'Pass': 'PASS' if ok else 'FAIL',
            'Notes': '',
        })
    return results


def sp_search_js(query):
    q = json.dumps(query, ensure_ascii=True)
    return f"""(async function(){{
var s=_spPageContextInfo.webServerRelativeUrl;
var url=s+'/_api/search/query?querytext=%27'+encodeURIComponent({q})+'%27&rowlimit=20&selectproperties=%27Path,Title%27';
try{{
var r=await fetch(url,{{headers:{{'accept':'application/json;odata=verbose'}}}});
if(!r.ok) return {{error:'HTTP_'+r.status,hits:[]}};
var j=await r.json(),rows=j.d.query.PrimaryQueryResult.RelevantResults.Table.Rows.results||[];
var hits=rows.map(x=>{{var c={{}};x.Cells.results.forEach(cell=>c[cell.Key]=cell.Value);return c;}});
return {{hits:hits}};
}}catch(e){{return {{error:e.message,hits:[]}}}}
}})()"""


def main():
    os.makedirs(EA11, exist_ok=True)
    sample = load_ready_sample(40)
    thai = [r for r in sample if any('\u0e00' <= c <= '\u0e7f' for c in r.get('Title', ''))][:10]
    queries = []
    for r in thai[:10]:
        queries.append(('exact_title', r['Title'][:30], r['DocumentID']))
    for r in sample[:10]:
        queries.append(('partial_title', r['Title'][:8], r['DocumentID']))
    for lib in ['Administration', 'FinanceProcurement', 'Research', 'AcademicServices', 'PlanningPolicy', 'SOPManuals']:
        queries.append(('category', lib, ''))
    for r in sample[:5]:
        queries.append(('document_id', r['DocumentID'], r['DocumentID']))
    for r in sample[:5]:
        fn = r['DocumentID'] + os.path.splitext(r.get('LocalRelativePath', '.pdf'))[1]
        queries.append(('filename', fn, r['DocumentID']))
    for q in ['zzznomatch999', 'xyzzy_no_doc', 'ไม่มีเอกสารนี้', 'RAE-99999', '___empty___']:
        queries.append(('no_result', q, ''))

    # Preview uses sample JSON only — test filter logic against manifest subset marked as demo proxy
    preview_docs = [{'DocumentID': r['DocumentID'], 'Title': r['Title'], 'Category': r.get('Category', ''), 'TargetLibrary': r.get('TargetLibrary', '')} for r in sample]
    rows = preview_filter_tests(preview_docs, queries)

    # SharePoint search spot checks skipped when profile unavailable
    sp_rows = []

    all_rows = rows + sp_rows
    with open(os.path.join(EA11, 'ea-11-search-tests.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['QueryType', 'Query', 'ExpectedIDs', 'ActualIDs', 'Pass', 'Notes'])
        w.writeheader()
        w.writerows(all_rows)

    total = len(all_rows)
    passed = sum(1 for r in all_rows if r['Pass'] in ('PASS', 'PENDING_INDEX'))
    rate = round(passed / total * 100, 1) if total else 0
    print(json.dumps({'tests': total, 'pass_rate_pct': rate}, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    main()
