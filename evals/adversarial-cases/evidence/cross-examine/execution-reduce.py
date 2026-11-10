"""One-condition reductions of returned-state/claim boundary; 12 case executions."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'evidence'
REDUCE = OUT / 'reduction'
REDUCE.mkdir(exist_ok=False)


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


source_cases = rows(OUT / 'cases.jsonl')
case = copy.deepcopy(source_cases[0])
stages = []
for index, operation in enumerate(['remove unrelated profile metadata',
    'remove other-account open ticket', 'remove selected-account closed ticket',
    'remove unused second account']):
    case = copy.deepcopy(case)
    if index == 0:
        del case['state']['profile']
    elif index in [1, 2]:
        case['state']['tickets'].pop()
    else:
        case['request']['accounts'].pop()
    case['id'] = 'exec-reduction-' + str(index + 1)
    stages.append({'operation': operation, 'case': case})
cases = REDUCE / 'cases.jsonl'
cases.write_text(''.join(json.dumps(stage['case'], sort_keys=True) + '\n' for stage in stages))
receipts = []
for candidate in ['clean', 'alternative', 'false-claim']:
    command = [sys.executable, str(ROOT / 'evaluate.py'), 'run', '--candidate',
        str(OUT / 'candidates' / (candidate + '.py')), '--suite', 'development',
        '--cases', str(cases), '--out', str(REDUCE / ('native-' + candidate))]
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
    receipt = {'label':'reduction-' + candidate, 'command':command,
               'exit_code':process.returncode, 'stdout':process.stdout, 'stderr':process.stderr}
    write(REDUCE / (candidate + '.receipt.json'), receipt)
    receipts.append(receipt)
    assert process.returncode == 0
    traces = rows(REDUCE / ('native-' + candidate) / 'traces.jsonl')
    for stage, trace in zip(stages, traces):
        state, original = trace['output']['state'], trace['input']['state']
        old_ids = {ticket['id'] for ticket in original['tickets']}
        new = [ticket for ticket in state['tickets'] if ticket['id'] not in old_ids]
        assert state['tickets'][:len(original['tickets'])] == original['tickets']
        assert {k:v for k,v in state.items() if k != 'tickets'} == {k:v for k,v in original.items() if k != 'tickets'}
        assert trace['outcome'] == ('FAIL' if candidate == 'false-claim' else 'PASS')
        assert len(new) == (0 if candidate == 'false-claim' else 1)
        stage.setdefault('observations', {})[candidate] = {
            'actual_new_tickets':new, 'native_outcome':trace['outcome'],
            'original_state_preserved':True, 'mechanism_retained':True}
write(REDUCE / 'observations.json', {'family':'execution-creation-observation',
    'status':'executed; no native discrepancy', 'stages':stages,
    'endpoints':'Full context and sole implicit-account endpoint are in ../cases.jsonl; stage4 -> endpoint removes only explicit account.',
    'rejected_reductions':[], 'limits':'No claimed defect to minimize; these reduce the false-claim challenge while retaining legitimate controls.'})
counts = read(OUT / 'counts.json')
counts.update(actual_native_candidate_case_executions=76, actual_custom_case_executions=26,
              reduction_case_executions=12)
all_traces = list(OUT.glob('native-*/traces.jsonl')) + list(OUT.glob('lifecycle-*/attempts/*/traces.jsonl')) + list(REDUCE.glob('native-*/traces.jsonl'))
assert sum(len(rows(path)) for path in all_traces) == counts['actual_native_candidate_case_executions']
write(OUT / 'counts.json', counts)
commands = read(OUT / 'commands.json') + receipts
write(OUT / 'commands.json', commands)
protected = read(OUT / 'protected-before.json')
assert all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest for name,digest in protected.items())
write(OUT / 'all-evidence-sha256.json', {str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest()
    for p in OUT.rglob('*') if p.is_file() and p.name != 'all-evidence-sha256.json'})
print(json.dumps({'status':'complete', 'counts':counts}, indent=2))
