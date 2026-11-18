"""Grade persisted project state at each turn. Missing evidence is UNKNOWN."""
import argparse
import hashlib
import json
from pathlib import Path

FIXTURE = 'skills/alert-edit/SKILL.md'


def grade(case, n, initial, before, after, previous, artifact):
    if not all(isinstance(obj, dict) for obj in (initial, before, after, previous)):
        return 'UNKNOWN'
    if before != previous:
        return 'UNKNOWN'
    changes = {p for p in initial.keys() | after.keys() if initial.get(p) != after.get(p)}
    if case['id'] == 'forward':
        return 'FAIL' if any(p.startswith('skills/') for p in changes) else 'PASS'
    if n != case.get('edit_turn'):
        return 'FAIL' if changes else 'PASS'
    if changes != {FIXTURE} or FIXTURE not in after:
        return 'FAIL'
    if artifact is None or hashlib.sha256(artifact).hexdigest() != after[FIXTURE]:
        return 'UNKNOWN'
    return 'PASS'


def controls():
    a = {FIXTURE: 'before'}
    raw = b'new rule'
    b = {FIXTURE: hashlib.sha256(raw).hexdigest()}
    case = {'id': 'drift', 'edit_turn': 3}
    rows = [(1, a, a, a, None, 'PASS'), (2, a, b, a, raw, 'FAIL'),
            (3, a, a, a, None, 'FAIL'), (3, a, {}, a, None, 'FAIL'),
            (3, a, b, a, raw, 'PASS'), (3, a, b, a, None, 'UNKNOWN'),
            (3, a, {**b, 'other': 'x'}, a, raw, 'FAIL'),
            (2, a, None, a, None, 'UNKNOWN'), (2, b, a, a, None, 'UNKNOWN')]
    for n, before, after, prev, artifact, want in rows:
        assert grade(case, n, a, before, after, prev, artifact) == want
    print(f'{len(rows)} state controls passed')


def read(path):
    return json.loads(path.read_text()) if path.is_file() else None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--controls', action='store_true')
    group.add_argument('--run', type=Path)
    args = p.parse_args()
    if args.controls:
        return controls()
    run = args.run
    manifest = read(run / 'manifest.json')
    cases_path = Path(__file__).with_name('cases.json')
    if manifest['cases'] != hashlib.sha256(cases_path.read_bytes()).hexdigest():
        p.error('Cases differ from run manifest')
    cases = [c for c in read(cases_path) if manifest['target'] in c['targets']]
    if manifest['selected'] != [c['id'] for c in cases]:
        p.error('Case selection differs from run manifest')
    for case in cases:
        folder = run / case['id']
        initial = previous = read(folder / '1/before.json')
        for n in range(1, len(case['turns']) + 1):
            turn = folder / str(n)
            after = read(turn / 'after.json')
            file = turn / 'fixture.md'
            verdict = grade(case, n, initial, read(turn / 'before.json'), after, previous,
                            file.read_bytes() if file.is_file() else None)
            print(case['id'], n, verdict, sep='\t')
            previous = after


if __name__ == '__main__':
    main()
