"""Bounded execution driver. Replays require new output paths; preserves all receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
sys.path.insert(0, str(WORKSPACE))
import evaluate

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

cases_path = ROOT / 'author/approved-cases.jsonl'
cards = json.loads((ROOT / 'source/approved-cards.json').read_text())
cases = evaluate.load_cases('development', cases_path)
required_ids = ['A-r1', 'B-r2']
if [c['id'] for c in cases] != required_ids:
    raise RuntimeError('Required current approved membership differs')
fidelity = []
for case, card in zip(cases, cards):
    expected_case = dict(id=f"{card['id']}-r{card['revision']}", suite='development',
                         **{key: card[key] for key in ('family', 'request', 'state', 'expected')})
    if not evaluate.same_json(case, expected_case):
        raise RuntimeError('Authoring changed the full approved card projection')
    fidelity.append({'id': case['id'], 'exact_full_projection': True,
                     'fields': ['id/revision', 'suite', 'family', 'request.text', 'request.account', 'request.accounts', 'entire initial state including counter and metadata', 'expected actions/account/delta'],
                     'preservation_semantics': 'native evaluator full original prefix and non-ticket state equality',
                     'reference': 'source/approved-cards.json'})
write(ROOT / 'verification/fidelity.json', {'required_ids': required_ids, 'approved': 2, 'authored': 2, 'exact': fidelity,
    'excluded_ids': ['C-r1', 'P-01-r1', 'B-r1'], 'schema_validated_by': 'evaluate.load_cases'})
controls = [('legitimate', ROOT / 'controls/legitimate.py'),
            ('alternative', ROOT / 'controls/alternative.py'),
            ('false-claim', ROOT / 'controls/false-claim.py'),
            ('initial-product', WORKSPACE / 'support_agent.py')]
usage = {'native_case_budget': 48, 'reserved_plan': 8, 'actual_case_attempts': 0,
         'network_provider_calls': 0, 'new_dependencies': 0, 'test_runs': 0,
         'nested_agents': 0, 'proposed_contrast_attempts': 0, 'fault_injection_attempts': 0,
         'model_token_usage': 'not exposed by this task runtime; not estimated', 'commands': []}
write(ROOT / 'usage.json', usage)
state_witnesses = []
outcomes = []
for name, candidate in controls:
    out = ROOT / 'native' / name
    command = [sys.executable, 'evaluate.py', 'run', '--candidate', str(candidate), '--cases', str(cases_path), '--suite', 'development', '--out', str(out)]
    usage['actual_case_attempts'] += 2
    usage['commands'].append(command)
    write(ROOT / 'usage.json', usage)
    process = subprocess.run(command, cwd=WORKSPACE, text=True, capture_output=True)
    write(ROOT / 'native' / f'{name}-command.json', {'argv': command, 'exit': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr})
    if process.returncode:
        raise RuntimeError(f'Native execution failed; preserved charged attempt for {name}')
    manifest, summary = evaluate.checked_run(out)
    if manifest['case_ids'] != required_ids:
        raise RuntimeError('Native coverage differs from required coverage')
    traces = [json.loads(line) for line in (out / 'traces.jsonl').read_text().splitlines()]
    for case, trace in zip(cases, traces):
        state = trace['output']['state']
        old_ids = {t['id'] for t in case['state']['tickets']}
        state_witnesses.append({'control': name, 'id': case['id'], 'source': f'native/{name}/traces.jsonl',
            'actual_state': state, 'initial_state': case['state'], 'stdout_matches_parsed': json.loads(trace['stdout']) == trace['output'],
            'new_tickets': [t for t in state['tickets'] if t['id'] not in old_ids],
            'original_ticket_prefix_unchanged': state['tickets'][:len(case['state']['tickets'])] == case['state']['tickets'],
            'other_state_unchanged': {k:v for k,v in state.items() if k != 'tickets'} == {k:v for k,v in case['state'].items() if k != 'tickets'},
            'state_witness_scope': 'Actual returned state from real candidate subprocess; fixture has no external ticket database.',
            'native_outcome': trace['outcome'], 'failed_checks': [k for k,v in trace['checks'].items() if not v]})
    outcomes.append({'control': name, 'counts': summary['counts'], 'outcomes': {r['id']:r['outcome'] for r in summary['results']},
                     'checked_run': 'passed'})
write(ROOT / 'verification/state-witnesses.json', state_witnesses)
before = json.loads((ROOT / 'source/frozen-before.json').read_text())
after = {path: sha(WORKSPACE / path) for path in before}
if before != after:
    raise RuntimeError('Original product/evaluator/spec/rubric/cases changed')
inventory = json.loads((ROOT / 'source/inventory.json').read_text())
actual_members = {p.name for p in (ROOT / 'source').iterdir() if p.is_file()}
if actual_members != set(inventory) | {'inventory.json'}:
    raise RuntimeError('Source membership changed')
if any(sha(ROOT / 'source' / name) != digest for name,digest in inventory.items()):
    raise RuntimeError('Source content changed')
write(ROOT / 'verification/results.json', {'frozen_before_equals_after': True, 'frozen_after': after,
    'required_source_membership_and_hashes_checked': sorted(actual_members),
    'required_controls': [name for name,_ in controls], 'required_ids': required_ids,
    'native_evidence_checker': 'evaluate.checked_run on all four runs; stdout, parsed output, identity, case coverage, outcomes and counts checked',
    'outcomes': outcomes, 'actual_case_attempts': usage['actual_case_attempts']})
print(json.dumps(outcomes, indent=2))
