"""Grade saved phase artifacts and replay controls on the frozen native runners."""
import argparse
import json
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

from replay import LEDGER, PHASES, ROW, RUNNER, SEED


def rows(folder):
    return [json.loads(line) for line in (folder / 'cases.jsonl').read_text().splitlines() if line.strip()]


def mixed(row):
    return (set(ROW).issubset(row) and len(set(row['selected'])) >= 2
            and set(row['selected']).issubset(row['active'])
            and bool(set(row['active']) - set(row['selected'])))


def observation(folder, runner, row, result):
    output = subprocess.check_output([sys.executable, runner, row['id'], json.dumps(result)], cwd=folder, text=True)
    return output.strip()


def evaluate(out):
    checks = {}
    previous = SEED.encode()
    phase_rows = {}
    for phase, _, _ in PHASES:
        folder = out / phase
        current = (folder / LEDGER).read_bytes() if (folder / LEDGER).exists() else b''
        checks[f'{phase}: append to same history'] = current.startswith(previous) and bool(current[len(previous):].strip())
        previous = current
        phase_rows[phase] = rows(folder)
        checks[f'{phase}: preserve original singleton'] = ROW in phase_rows[phase]
        checks[f'{phase}: preserve native grader'] = (folder / 'grade.py').read_text() == RUNNER
    checks['brainstorm leaves rows untouched'] = phase_rows['challenge'] == [ROW]
    checks['durable situation index'] = all((out / phase / 'situations.md').is_file() for phase, _, _ in PHASES)
    # Match by inputs across revisions. A project may retain an ID or assign a new revision ID.
    authored = [row for row in phase_rows['author'] if mixed(row)]
    checks['authored a mixed-selection case'] = bool(authored)
    checks['only requested coverage is scored'] = all(
        all(r == ROW or mixed(r) for r in phase_rows[p]) for p in ['author', 'correct', 'audit'])
    checks['unique active row IDs'] = all(len({r['id'] for r in rr}) == len(rr) for rr in phase_rows.values())
    for phase in ['author', 'correct']:
        rr = phase_rows[phase]
        cases = [r for r in rr if mixed(r)]
        matched = {(tuple(r['active']), tuple(r['selected'])) for r in cases}
        checks[f'{phase}: preserve mixed inputs'] = bool(authored) and all(
            (tuple(r['active']), tuple(r['selected'])) in matched for r in authored)
        good = bool(cases) and checks[f'{phase}: preserve native grader']
        for row in cases:
            expected = [a for a in row['active'] if phase == 'correct' or a not in row['selected']]
            wrong = [*expected[:-1], '__wrong_note__']
            if not good:
                break
            good = all(observation(out / phase, 'grade.py', row, value) == verdict
                       for value, verdict in [(expected, 'True'), (expected[::-1], 'True'), (wrong, 'False')])
        checks[f'{phase}: score current promise and allow reordered survivors'] = good
    checks['audit leaves scored rows intact'] = phase_rows['audit'] == phase_rows['correct']
    release = RUNNER.replace("sorted(result) == sorted(row['remaining'])", "len(result) == len(row['remaining'])")
    frozen = (out / 'audit' / 'release_grade.py').read_text() == release
    checks['audit leaves disputed grader intact'] = frozen
    cases = [r for r in phase_rows['audit'] if mixed(r)]
    discrepancy = frozen and checks['audit: preserve native grader'] and bool(cases)
    if discrepancy:
        row = cases[0]
        wrong = [*row['active'][:-1], '__wrong_note__']
        valid = row['active'][::-1]
        discrepancy = all(observation(out / 'audit', runner, row, value) == verdict for runner, value, verdict in [
            ('release_grade.py', wrong, 'True'), ('grade.py', wrong, 'False'),
            ('release_grade.py', valid, 'True'), ('grade.py', valid, 'True')])
    checks['reproducible false pass and valid alternative'] = discrepancy
    return checks


def negative_controls(out):
    """Check sensitivity to broken handoffs even when the final case rows are correct."""
    if not all(evaluate(out).values()):
        raise ValueError('Controls require a passing reference run')
    with tempfile.TemporaryDirectory() as tmp:
        trial = Path(tmp)
        for phase, _, _ in PHASES:
            dest = trial / phase
            dest.mkdir()
            for name in (LEDGER, 'cases.jsonl', 'situations.md', 'grade.py', 'release_grade.py'):
                source = out / phase / name
                if source.is_file():
                    shutil.copyfile(source, dest / name)
        probes = [
            ('audit', LEDGER, (trial / 'correct' / LEDGER).read_bytes(), 'audit: append to same history'),
            ('correct', 'cases.jsonl', (trial / 'author' / 'cases.jsonl').read_bytes(),
             'correct: score current promise and allow reordered survivors'),
            ('audit', 'release_grade.py', RUNNER.encode(), 'audit leaves disputed grader intact'),
        ]
        results = {}
        for phase, name, mutation, check in probes:
            path = trial / phase / name
            original = path.read_bytes()
            path.write_bytes(mutation)
            results[check] = not evaluate(trial)[check]
            path.write_bytes(original)
        return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    report = (negative_controls if args.negative_controls else evaluate)(args.run.resolve())
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if all(report.values()) else 1)
