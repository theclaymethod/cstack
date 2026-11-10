"""Replay synthetic development controls through the existing stored-observation runner."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'fixture'
WORKSPACE = BASE / 'evidence'
CASES = ROOT / 'evals/bootstrap-vpn.jsonl'
CONTRACT = {
    'S-01': ({'guidance'}, 0),
    'S-02': ({'guidance'}, 0),
    'S-03': ({'create_ticket'}, 1),
    'S-04': ({'guidance', 'clarify'}, 0),
}

def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    if len(sys.argv) > 1:
        output = Path(sys.argv[1]).resolve()
        output.mkdir(parents=True, exist_ok=False)
    else:
        run_root = BASE.parents[1] / 'eval-runs'
        run_root.mkdir(exist_ok=True)
        output = Path(tempfile.mkdtemp(prefix='bootstrap-', dir=run_root))
    manifest = json.loads((WORKSPACE / 'case-map.json').read_text())
    if set(manifest) != set(CONTRACT):
        raise ValueError('Approved subset mapping mismatch')
    actual_cases = [json.loads(s) for s in CASES.read_text().splitlines()]
    if len(actual_cases) != 4 or {x['id'] for x in actual_cases} != set(manifest.values()):
        raise ValueError('Missing, duplicate or extra authored case')
    for sid, case_id in manifest.items():
        row = next(x for x in actual_cases if x['id'] == case_id)
        actions, delta = CONTRACT[sid]
        if set(row['expected']['allowed_actions']) != actions or row['expected']['ticket_delta'] != delta:
            raise ValueError('Authored expectation differs from approved contract: ' + sid)
    totals = {'PASS': 0, 'FAIL': 0, 'ERROR': 0}
    mismatches = []
    executions = []
    controls = [(f'{action}-delta-{delta}', action, delta) for action in ['guidance', 'create_ticket', 'clarify'] for delta in [-1, 0, 1, 2]]
    controls.extend([('missing-observation', None, None), ('noninteger-ticket-delta', 'guidance', True)])
    for name, action, delta in controls:
        observations = [] if action is None else [{'case_id': cid, 'action': action, 'ticket_delta': delta} for cid in manifest.values()]
        observation_path = output / (name + '.observations.jsonl')
        observation_path.write_text(''.join(json.dumps(row) + '\n' for row in observations))
        proc = subprocess.run([sys.executable, 'runner.py', '--cases', str(CASES), '--observations', str(observation_path)], cwd=ROOT, text=True, capture_output=True)
        (output / (name + '.stdout.json')).write_text(proc.stdout)
        (output / (name + '.stderr.txt')).write_text(proc.stderr)
        if proc.returncode:
            raise RuntimeError(f'Runner setup failure on {name}: {proc.stderr}')
        result = json.loads(proc.stdout)
        expected = {}
        for sid, cid in manifest.items():
            allowed, required_delta = CONTRACT[sid]
            expected[cid] = 'ERROR' if action is None or type(delta) is not int else 'PASS' if action in allowed and delta == required_delta else 'FAIL'
        got = {x['id']: x['verdict'] for x in result['results']}
        if got != expected or len(result['results']) != len(expected):
            mismatches.append({'control': name, 'expected': expected, 'actual': result})
        for verdict in got.values():
            totals[verdict] += 1
        executions.append({'control': name, 'returncode': proc.returncode, 'expected_from': 'literal approved routing contract; synthetic development controls, not human outcome labels', 'expected_verdicts': expected, 'observed_verdicts': got})
    before = json.loads((WORKSPACE / 'preservation-before.json').read_text())
    current = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in before}
    if before != current:
        raise ValueError('Preserved suite or runner changed')
    hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [ROOT/'runner.py', CASES, WORKSPACE/'approved-handoff.json', WORKSPACE/'case-map.json', Path(__file__).resolve()] + sorted(output.glob('*'))}
    dump(output/'frozen-hashes.json', hashes)
    summary = {'evidence_directory': str(output), 'boundary': 'stored-observation; synthetic contract-derived development controls', 'approved_cases': 4, 'control_runs': len(executions), 'case_control_verdicts': totals, 'expected_vs_observed_mismatches': mismatches, 'suite_and_runner_unchanged': current == before, 'product_execution': 'unrun: no implementation', 'semantic_judge_calibration': 'not performed; excluded by user', 'independent_holdout': False, 'host': platform.platform(), 'python': sys.version, 'runs': executions}
    dump(output/'summary.json', summary)
    print(json.dumps({k:v for k,v in summary.items() if k != 'runs'}, indent=2))
    if mismatches:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
