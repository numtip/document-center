#!/usr/bin/env python3
"""EA-11 build/lint QA."""
import json
import os
import subprocess
from datetime import datetime, timezone

REPO = r'G:\ProjectAI\document-center'
OUT = os.path.join(REPO, '.migration', 'rae-wtms', 'ea-11', 'ea-11-build-results.json')


def run(cmd):
    p = subprocess.run(['rtk'] + cmd, cwd=REPO, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
    out = (p.stdout or '') + (p.stderr or '')
    return p.returncode, out.strip()[-500:]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    lint_rc, lint_out = run(['npm', 'run', 'lint'])
    build_rc, build_out = run(['npm', 'run', 'build'])
    validate_rc, validate_out = run(['npm', 'run', 'validate:all'])

    result = {
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'lint': {'exit_code': lint_rc, 'pass': lint_rc == 0, 'tail': lint_out},
        'build': {'exit_code': build_rc, 'pass': build_rc == 0, 'tail': build_out},
        'validate_all': {'exit_code': validate_rc, 'pass': validate_rc == 0, 'tail': validate_out},
        'dist_exists': os.path.isdir(os.path.join(REPO, 'dist')),
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: result[k]['pass'] if isinstance(result[k], dict) and 'pass' in result[k] else result[k] for k in result}, indent=2))


if __name__ == '__main__':
    main()
