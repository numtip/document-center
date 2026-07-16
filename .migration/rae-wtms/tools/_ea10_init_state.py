#!/usr/bin/env python3
"""Initialize EA-10 state from baseline."""
import json
import os

ROOT = r'G:\ProjectAI\document-center\.migration\rae-wtms'
EA10 = os.path.join(ROOT, 'ea-10')
BASE = os.path.join(EA10, 'ea-10-baseline.json')
OUT = os.path.join(EA10, 'ea-10-state.json')


def main():
    with open(BASE, encoding='utf-8') as f:
        base = json.load(f)
    state = {
        'phase': 'EA-10',
        'started_at': base.get('timestamp'),
        'baseline': {
            'prior_success_count': base.get('prior_success_count', 131),
            'already_complete_count': base.get('already_complete_count'),
            'not_migrated_count': base.get('not_migrated_count'),
            'remaining_eligible_count': base.get('remaining_eligible_count'),
            'registry_row_count': base.get('registry_row_count'),
            'registry_duplicate_count': base.get('registry_duplicate_count'),
        },
        'selected': 0,
        'waves': {},
        'batches': {},
        'resume_test': {},
        'performance': {},
        'governance': 'DEFERRED_GOVERNANCE',
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f'Initialized {OUT}')


if __name__ == '__main__':
    main()
