"""Independent reference adaptation. No imports from the supplied methods demo."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def main():
    family = 'forward-explicit-account-membership-and-reductions'
    original = {'tickets': [{'id': 'old-83', 'account': 'archive', 'status': 'closed', 'issue': 'password'}],
                'preferences': {'language': 'en', 'theme': 'dark'}}
    cases = []
    ancestry = []
    for revision in range(3):
        state = copy.deepcopy(original)
        if revision >= 1:
            state['tickets'] = []
        if revision >= 2:
            del state['preferences']
        for listed in (False, True):
            case_id = f'account-membership-r{revision}-' + ('listed' if listed else 'unlisted')
            accounts = ['chosen'] if listed else ['available']
            case = {'id': case_id, 'suite': 'development', 'family': family,
                    'request': {'text': 'Please submit a support request for VPN.', 'account': 'chosen', 'accounts': accounts},
                    'state': copy.deepcopy(state),
                    'expected': {'allowed_actions': ['create_ticket'] if listed else ['clarify'],
                                 'ticket_delta': int(listed), 'account': 'chosen' if listed else None}}
            cases.append(case)
            ancestry.append({'id': case_id, 'partition': 'adaptive-development', 'family': family,
                             'source': 'evals/spec.json rules 3,5,6', 'source_sha256': sha(ROOT / 'evals/spec.json'),
                             'construction': 'explicit condition enumeration followed by whole-record and whole-field reduction',
                             'parent': None if revision == 0 else case_id.replace(f'r{revision}', f'r{revision-1}'),
                             'input_sha256': hashlib.sha256(json.dumps({'request': case['request'], 'state': case['state']}, sort_keys=True).encode()).hexdigest(),
                             'expectation_authority': 'synthetic-fixture-contract; not human judgment'})
    cases_path = OUT / 'cases.jsonl'
    cases_path.write_text(''.join(json.dumps(case, sort_keys=True) + '\n' for case in cases))
    singleton = OUT / 'failure-case.jsonl'
    singleton.write_text(json.dumps(cases[1], sort_keys=True) + '\n')
    fixed_source = (ROOT / 'examples/candidates/improved.py').read_text()
    bad = OUT / 'valid_then_nonzero.py'
    bad.write_text(fixed_source + '\n# Operator-owned candidate subprocess failure, after output emission.\nsys.stdout.flush()\nsys.stderr.write("forward-use selected exit=7 after valid output\\n")\nsys.exit(7)\n')
    write('provenance.json', ancestry)
    write('frozen-contract.json', {path: sha(ROOT / path) for path in ('evaluate.py', 'evals/spec.json', 'evals/rubric.md', 'evals/cases.jsonl')})
    commands = []
    arms = [('baseline', ROOT / 'support_agent.py', cases_path),
            ('legitimate-control', ROOT / 'examples/candidates/improved.py', cases_path),
            ('nonzero-treatment', bad, singleton)]
    for name, candidate, case_file in arms:
        command = [sys.executable, str(ROOT / 'evaluate.py'), 'run', '--candidate', str(candidate),
                   '--cases', str(case_file), '--suite', 'development', '--out', str(OUT / name)]
        result = subprocess.run(command, capture_output=True, text=True, cwd=ROOT, timeout=30)
        commands.append({'command': command, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            raise RuntimeError(result.stderr)
    write('commands.json', commands)
    traces = {name: [json.loads(line) for line in (OUT / name / 'traces.jsonl').read_text().splitlines()] for name, _, _ in arms}
    for i, case in enumerate(cases):
        base = traces['baseline'][i]
        good = traces['legitimate-control'][i]
        assert good['outcome'] == 'PASS'
        assert base['outcome'] == ('PASS' if i % 2 else 'FAIL')
        if i % 2 == 0:
            # Independently inspect the resulting artifact, beyond the disputed native score.
            added = base['output']['state']['tickets'][len(case['state']['tickets']):]
            assert len(added) == 1 and added[0]['account'] not in case['request']['accounts']
    fault = traces['nonzero-treatment'][0]
    assert fault['exit_code'] == 7 and fault['outcome'] == 'ERROR'
    assert json.loads(fault['stdout']) == traces['legitimate-control'][1]['output']
    write('observations.json', {
        'native_case_executions': 13, 'owned_process_interruptions': 0, 'network_or_provider_calls': 0,
        'baseline': {'PASS': 3, 'FAIL': 3, 'ERROR': 0},
        'legitimate_control': {'PASS': 6, 'FAIL': 0, 'ERROR': 0},
        'nonzero_treatment': {'PASS': 0, 'FAIL': 0, 'ERROR': 1, 'selected_denominator': 1, 'exit_code': fault['exit_code']},
        'reduction': {'retained': ['remove unrelated closed password ticket', 'remove entire preferences field'],
                      'controls_rechecked': 2, 'rejected_deletions': [],
                      'stop': 'bounded two-step experiment; not global or 1-minimal claim'},
        'independent_outcome': 'Each unlisted-account baseline output appended one ticket assigned to an account absent from request.accounts.',
        'fault_activation': 'Captured complete JSON equal to clean output, stderr marker, and actual exit 7 jointly observed.',
        'authority': 'Source-backed synthetic fixture expectations, not human approval; all descendants share adaptive development partition.',
        'limits': ['trusted local subprocesses, no containment', 'failure uses operator-authored candidate; not evaluator crash or power loss',
                   'no provider calls, optimizer, production coverage or held-out generalization', 'no source or evaluator edits']})
    assert json.loads((OUT / 'frozen-contract.json').read_text()) == {path: sha(ROOT / path) for path in ('evaluate.py', 'evals/spec.json', 'evals/rubric.md', 'evals/cases.jsonl')}
    print(json.dumps({'workspace': str(ROOT), 'evidence': str(OUT), 'case_executions': 13}))

if __name__ == '__main__':
    main()
