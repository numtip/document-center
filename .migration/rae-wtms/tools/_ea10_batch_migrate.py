#!/usr/bin/env python3
"""EA-10 wrapper for controlled wave/batch migration."""
import subprocess
import sys

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = ROOT + r'\ea-10'
SEL = EA10 + r'\ea-10-selection.csv'
RES = EA10 + r'\ea-10-results.csv'


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--wave', type=int, required=True)
    ap.add_argument('--batch', type=int, required=True)
    ap.add_argument('--force', action='store_true')
    args, rest = ap.parse_known_args()

    batch_tag = f'EA10-W{args.wave:02d}-B'
    cmd = [
        sys.executable, '_ea7a_batch_migrate.py',
        '--selection', SEL,
        '--results', RES,
        '--batch-tag', batch_tag,
        '--batch', str(args.batch),
    ]
    if args.force:
        cmd.append('--force')
    cmd.extend(rest)
    raise SystemExit(subprocess.call(cmd, cwd=ROOT + r'\tools'))


if __name__ == '__main__':
    main()
