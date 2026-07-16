#!/usr/bin/env python3
"""EA-11 baseline freeze."""
import csv
import json
import os
import subprocess
from datetime import datetime, timezone

REPO = r'G:\ProjectAI\document-center'
EA11 = os.path.join(REPO, '.migration', 'rae-wtms', 'ea-11')
MANIFEST = os.path.join(REPO, 'migration', 'sharepoint-migration-manifest.csv')
OUT = os.path.join(EA11, 'ea-11-baseline.json')


def git(cmd):
    return subprocess.check_output(cmd, cwd=REPO, text=True).strip()


def main():
    os.makedirs(EA11, exist_ok=True)
    with open(MANIFEST, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    ready = [r for r in rows if r.get('MigrationStatus') == 'Ready' and r.get('LocalRelativePath', '').strip()]

    baseline = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'repository_branch': git(['git', 'branch', '--show-current']),
        'repository_head': git(['git', 'rev-parse', 'HEAD']),
        'ea10_commit': 'a787f30b1eb7f5e33eb5250b2ca1a862839bb2b6',
        'manifest_ready_count': len(ready),
        'expected_sharepoint_count': 627,
        'expected_registry_count': 627,
        'portal_preview_url': 'https://numtip.github.io/document-center/',
        'portal_preview_mode': 'demo_sample_3_records',
        'sharepoint_site': 'https://maejo365.sharepoint.com/sites/msteams_54adc4',
        'governance': 'DEFERRED_GOVERNANCE',
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, ensure_ascii=False, indent=2)
    print(json.dumps(baseline, indent=2))


if __name__ == '__main__':
    main()
