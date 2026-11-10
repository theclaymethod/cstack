"""Preserve first attempt; correct setup-only reset probe; reconcile evidence.

Run once after reproduce.py. It executes two additional candidate cases and no
process interruptions. The first driver's final expectation assertion failed;
all native artifacts and receipts from that attempt remain intact.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'evidence'
NATIVE = ROOT / 'evaluate.py'


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(directory):
    return {str(p.relative_to(directory)): sha(p) for p in directory.rglob('*') if p.is_file()}


def invoke(label, args):
    process = subprocess.run([sys.executable, str(NATIVE)] + [str(a) for a in args],
        cwd=ROOT, text=True, capture_output=True, timeout=30)
    record = {'label': label, 'command': process.args, 'exit_code': process.returncode,
              'stdout': process.stdout, 'stderr': process.stderr}
    write(OUT / (label + '.receipt.json'), record)
    assert process.returncode == 0, record
    return record


original = OUT / 'candidates/reset-probe.py'
fixed = OUT / 'candidates/reset-probe-r2.py'
assert not fixed.exists(), 'Write-once correction already executed'
fixed.write_text(original.read_text().replace('from pathlib import Path', 'import json\nimport sys\nfrom pathlib import Path'))
invoke('candidate-reset-probe-r2', ['run', '--candidate', fixed,
       '--suite', 'development', '--cases', OUT / 'cases.jsonl', '--out', OUT / 'native-reset-probe-r2'])
for label, left, right in [
    ('compare-alternative', OUT / 'native-clean', OUT / 'native-alternative'),
    ('compare-reset-r2', OUT / 'native-clean', OUT / 'native-reset-probe-r2'),
    ('compare-unreachable', OUT / 'lifecycle-clean/attempts/000-baseline',
     OUT / 'lifecycle-unreachable/attempts/000-baseline'),
]:
    invoke(label, ['compare', '--baseline', left, '--candidate', right])

observations = [read(OUT / (name + '.observation.json')) for name in [
    'lifecycle-clean', 'lifecycle-unreachable', 'lifecycle-partial',
    'lifecycle-published', 'lifecycle-memory', 'lifecycle-proposal']]
clean = rows(OUT / 'lifecycle-clean/attempts/000-baseline/traces.jsonl')
expected = {'clean':'PASS', 'alternative':'PASS', 'reset-probe':'ERROR', 'reset-probe-r2':'PASS',
            'false-claim':'FAIL', 'malformed':'ERROR', 'runtime-error':'ERROR'}
score_observations = []
cases = rows(OUT / 'cases.jsonl')
for name, outcome in expected.items():
    run = OUT / ('native-' + name)
    traces = rows(run / 'traces.jsonl')
    witnesses = []
    assert len(traces) == 2
    for case, trace in zip(cases, traces):
        assert trace['outcome'] == outcome
        witness = {'id': trace['id'], 'native_outcome': trace['outcome'],
                   'native_error': trace['error'], 'process_exit': trace['exit_code']}
        output = trace['output']
        if output:
            state, original_state = output['state'], case['state']
            original_ids = {ticket['id'] for ticket in original_state['tickets']}
            new = [ticket for ticket in state['tickets'] if ticket['id'] not in original_ids]
            prefix = state['tickets'][:len(original_state['tickets'])] == original_state['tickets']
            other = {k:v for k,v in state.items() if k != 'tickets'} == {
                k:v for k,v in original_state.items() if k != 'tickets'}
            met = prefix and other and len(new) == 1 and len(state['tickets']) == len(original_state['tickets'])+1
            met = met and new[0]['account'] == 'acct-a' and new[0]['status'] == 'open' and new[0]['issue'] == 'vpn'
            witness.update(original_prefix_preserved=prefix, other_state_preserved=other,
                           actual_new_tickets=new, original_creation_requirement_met=met)
            assert met == (outcome == 'PASS')
        else:
            witness.update(original_creation_requirement_met=None,
                limits='No valid returned state; no independently committed ticket service exists in this fixture.')
        if name.startswith('reset-probe'):
            witness['construction_revision'] = 'r2-corrected-imports' if name.endswith('r2') else 'r1-setup-error'
            if name.endswith('r2'):
                marker = json.loads(trace['stderr'])
                witness['candidate_cwd_witness'] = marker
                assert marker['reset_observed'] is True
                assert not Path(marker['cwd']).exists(), 'Native scratch not removed after trial'
            else:
                assert 'NameError' in trace['stderr']
                witness['classification'] = 'construction setup error; reset not exercised'
        witnesses.append(witness)
    if name == 'reset-probe-r2':
        assert witnesses[0]['candidate_cwd_witness']['cwd'] != witnesses[1]['candidate_cwd_witness']['cwd']
    score_observations.append({'candidate': name, 'summary': read(run / 'summary.json'),
                               'independent_witnesses': witnesses})

for obs in observations:
    label = obs['label']
    assert obs['post_status_state'] == obs['repeat_status_state']
    assert obs['post_status_files'] == obs['repeat_status_files']
    before, after = obs['pre_status_files'], obs['post_status_files']
    assert set(before) == set(after)
    assert all(before[name] == after[name] for name in before if name != 'state.json')
    assert inventory(OUT / label) == after
    if obs['activation_count']:
        events = rows(OUT / (label + '.activation.jsonl'))
        receipt = read(OUT / (label + '.receipt.json'))
        config = read(OUT / (label + '.config.json'))
        assert len(events) == 1 and events[0]['pid'] == receipt['pid']
        assert receipt['exit_code'] == -9 and events[0]['source_sha256'] == config['source_sha256'] == sha(NATIVE)
    if label not in ['lifecycle-partial', 'lifecycle-proposal']:
        retained = rows(OUT / label / 'attempts/000-baseline/traces.jsonl')
        assert [(r['id'], r['output'], r['outcome']) for r in retained] == [(r['id'], r['output'], r['outcome']) for r in clean]
    if label == 'lifecycle-partial':
        assert obs['actual_case_executions'] == 2
        assert obs['pre_status_state'] == obs['post_status_state']
        assert not (OUT / label / 'attempts/000-baseline/summary.json').exists()
        obs['construction_outcome'] = 'Activated partial interruption; incomplete evidence correctly remains pending and charged.'
    elif label == 'lifecycle-proposal':
        proposal = obs['post_status_state']['attempts'][1]
        assert proposal['decision_recovered'] is True and proposal['decision'] == 'retain improvement'
        assert obs['post_status_state']['best_attempt'] == 1
        obs['construction_outcome'] = 'Activated decision interruption; measured proposal correctly selected without replaying candidates.'
    elif label in ['lifecycle-published', 'lifecycle-memory']:
        assert obs['post_status_state']['attempts'][0]['completion_recovered'] is True
        obs['construction_outcome'] = 'Activated completed-measurement interruption; complete identity-matching evidence correctly reconciled.'
    else:
        assert obs['activation_count'] == 0 and obs['process_exit'] == 0
        obs['construction_outcome'] = 'Clean control' if label == 'lifecycle-clean' else 'Armed unreachable trigger; not activated.'

receipts = [read(path) for path in sorted(OUT.glob('*.receipt.json'))]
traces = list(OUT.glob('native-*/traces.jsonl')) + list(OUT.glob('lifecycle-*/attempts/*/traces.jsonl'))
counts = {'actual_native_candidate_case_executions': sum(len(rows(path)) for path in traces),
    'operator_process_interruptions': sum(receipt['exit_code'] == -9 for receipt in receipts),
    'lifecycle_reserved_case_runs': sum(obs['post_status_state']['used_case_runs'] for obs in observations),
    'actual_lifecycle_case_executions': sum(obs['actual_case_executions'] for obs in observations),
    'actual_custom_case_executions': sum(len(rows(path)) for path in OUT.glob('native-*/traces.jsonl')),
    'setup_rejected_operator_invocations': 1,
    'candidate_construction_setup_error_case_executions_included_above': 2,
    'candidate_case_budget': 120, 'process_interruption_budget': 4,
    'network_or_provider_calls': 0}
assert counts['actual_native_candidate_case_executions'] == 64
assert counts['operator_process_interruptions'] == 4
protected_before = read(OUT / 'protected-before.json')
protected_after = {name:sha(ROOT / name) for name in protected_before}
assert protected_before == protected_after
write(OUT / 'protected-after.json', protected_after)
write(OUT / 'lifecycle-observations.json', observations)
write(OUT / 'score-observations.json', score_observations)
write(OUT / 'counts.json', counts)
write(OUT / 'commands.json', receipts)
write(OUT / 'construction-setup-error.json', {
    'driver_revision': 'reproduce.py-r1', 'raw_driver_outcome': 'exit 1: final expected_outcomes assertion failed',
    'attribution': 'Attacker construction import-order error, not target/skill defect.',
    'probe_r1_native_score': 0.0, 'probe_r1_native_errors': 2,
    'actual_cases_before_correction': 62,
    'corrected_revision': 'reset-probe-r2.py imports json/sys before observation marker',
    'additional_cases': 2, 'additional_interruptions': 0,
    'reproduction': 'reproduce.py retains original failed construction; finalize.py corrects it once and harvests both revisions.'})
write(OUT / 'all-evidence-sha256.json', {str(p.relative_to(OUT)):sha(p) for p in OUT.rglob('*')
    if p.is_file() and p.name != 'all-evidence-sha256.json'})
print(json.dumps({'status':'complete', 'counts':counts, 'finding':'No demonstrated discrepancy in exercised boundaries.'}, indent=2))
