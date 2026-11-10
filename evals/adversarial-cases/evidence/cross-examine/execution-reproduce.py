"""Independent bounded construction using only frozen native runner commands.

Invoke in a freshly materialized frozen-source workspace. Output is write-once.
No network, providers, protected edits, or signals to unowned processes.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'evidence'
OUT.mkdir(exist_ok=False)
NATIVE = ROOT / 'evaluate.py'
commands = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def protected():
    files = [ROOT / name for name in ['evaluate.py', 'support_agent.py',
        'evals/spec.json', 'evals/cases.jsonl', 'evals/rubric.md']]
    files.extend(p for p in (ROOT / '.agents/skills').rglob('*') if p.is_file())
    return {str(p.relative_to(ROOT)): sha(p) for p in files}


def inventory(directory):
    return {str(p.relative_to(directory)): sha(p) for p in directory.rglob('*') if p.is_file()}


def invoke(label, args, expected=0, injected=False):
    command = ([sys.executable, str(HERE / 'inject.py')] if injected
               else [sys.executable, str(NATIVE)]) + [str(arg) for arg in args]
    process = subprocess.Popen(command, cwd=ROOT, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(timeout=45)
    record = {'label': label, 'command': command, 'pid': process.pid,
              'exit_code': process.returncode, 'stdout': stdout, 'stderr': stderr}
    write(OUT / (label + '.receipt.json'), record)
    commands.append(record)
    assert process.returncode == expected, record
    return record


write(OUT / 'protected-before.json', protected())
cases = []
for suffix, state, accounts, account in [
    ('context', {'tickets': [
        {'id': 'keep-closed', 'account': 'acct-a', 'status': 'closed', 'issue': 'vpn'},
        {'id': 'keep-other', 'account': 'acct-b', 'status': 'open', 'issue': 'vpn'}],
        'profile': {'tier': 'enterprise', 'flags': ['preserve', 7]}}, ['acct-a', 'acct-b'], 'acct-a'),
    ('reduced', {'tickets': []}, ['acct-a'], None),
]:
    cases.append({'id': 'exec-create-' + suffix, 'suite': 'development',
        'family': 'execution-creation-observation',
        'request': {'text': 'Please open a ticket for my VPN outage.',
                    'account': account, 'accounts': accounts}, 'state': state,
        'expected': {'allowed_actions': ['create_ticket'], 'ticket_delta': 1, 'account': 'acct-a'}})
casefile = OUT / 'cases.jsonl'
casefile.write_text(''.join(json.dumps(case, sort_keys=True) + '\n' for case in cases))

base = (ROOT / 'examples/candidates/improved.py').read_text()
candidates = OUT / 'candidates'
candidates.mkdir()
for name in ['clean', 'alternative', 'reset-probe', 'false-claim', 'malformed', 'runtime-error']:
    source = base
    if name == 'alternative':
        source = source.replace('f"ticket-{sequence}"', 'f"independent-{sequence}"')
        source = source.replace('Opened the requested VPN support ticket.', 'Request recorded. See your support queue.')
    elif name == 'reset-probe':
        source = source.replace('import copy', '''import copy
from pathlib import Path
scratch = Path.cwd() / 'candidate-local-state'
assert not scratch.exists(), 'prior trial state leaked into this case'
scratch.write_text('created only in native disposable cwd')
print(json.dumps({'cwd': str(Path.cwd()), 'reset_observed': True}), file=sys.stderr)''')
    elif name == 'false-claim':
        source = source.replace('print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))', '''payload = json.load(sys.stdin)
    output = {'action': 'create_ticket', 'account': 'acct-a', 'state': payload['state'],
              'note': 'Opened a ticket.'}
    print(json.dumps(output, sort_keys=True))''')
    elif name == 'malformed':
        source = source.replace('print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))',
                                'print("{this is not JSON}")')
    elif name == 'runtime-error':
        source = source.replace('print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))',
                                'raise RuntimeError("synthetic candidate crash before result")')
    (candidates / (name + '.py')).write_text(source)
    invoke('candidate-' + name, ['run', '--candidate', candidates / (name + '.py'),
          '--suite', 'development', '--cases', casefile, '--out', OUT / ('native-' + name)])

# All injected runs preserve the exact source. Hash-pinned tracing is operator access.
def inject(label, phase, native_args, expected=-9):
    config = {'target': str(NATIVE), 'source_sha256': sha(NATIVE), 'phase': phase,
              'activation': str(OUT / (label + '.activation.jsonl')),
              'completion': str(OUT / (label + '.completion.json')),
              'native_args': [str(a) for a in native_args]}
    configfile = OUT / (label + '.config.json')
    write(configfile, config)
    return invoke(label, [configfile], expected, True)


def state_observation(label, campaign, phase, receipt):
    pre = read(campaign / 'state.json')
    before = inventory(campaign)
    invoke(label + '-status', ['status', '--campaign', campaign])
    post = read(campaign / 'state.json')
    after = inventory(campaign)
    invoke(label + '-status-repeat', ['status', '--campaign', campaign])
    repeated = read(campaign / 'state.json')
    events = OUT / (label + '.activation.jsonl')
    retained_traces = list(campaign.glob('attempts/*/traces.jsonl'))
    actual = sum(len(rows(path)) for path in retained_traces)
    observation = {'label': label, 'phase': phase, 'process_exit': receipt['exit_code'],
        'activation_count': len(rows(events)) if events.exists() else 0,
        'pre_status_state': pre, 'post_status_state': post, 'repeat_status_state': repeated,
        'pre_status_files': before, 'post_status_files': after, 'repeat_status_files': inventory(campaign),
        'actual_case_executions': actual}
    write(OUT / (label + '.observation.json'), observation)
    return observation


observations = []
for label, phase in [('lifecycle-clean', None), ('lifecycle-unreachable', 'unreachable'),
                     ('lifecycle-partial', 'partial-2'), ('lifecycle-published', 'published-summary'),
                     ('lifecycle-memory', 'completed-memory')]:
    campaign = OUT / label
    args = ['start', '--campaign', campaign, '--max-case-runs', '24']
    receipt = invoke(label, args) if phase is None else inject(label, phase, args, 0 if phase == 'unreachable' else -9)
    observations.append(state_observation(label, campaign, phase, receipt))

label = 'lifecycle-proposal'
campaign = OUT / label
invoke(label + '-baseline', ['start', '--campaign', campaign, '--max-case-runs', '24'])
receipt = inject(label, 'proposal-decision', ['try', '--campaign', campaign,
    '--candidate', candidates / 'clean.py', '--hypothesis',
    'Explicit commands and duplicate-aware selection repair known synthetic baseline errors.'])
observations.append(state_observation(label, campaign, 'proposal-decision', receipt))

# Rejected setup does not invoke a candidate and must not be called fault activation.
badconfig = read(OUT / 'lifecycle-unreachable.config.json')
badconfig['source_sha256'] = '0' * 64
write(OUT / 'bad-source.config.json', badconfig)
invoke('setup-source-mismatch', [OUT / 'bad-source.config.json'], 1, True)

score_observations = []
for name in ['clean', 'alternative', 'reset-probe', 'false-claim', 'malformed', 'runtime-error']:
    run = OUT / ('native-' + name)
    summary = read(run / 'summary.json')
    traces = rows(run / 'traces.jsonl')
    witnesses = []
    for trace, case in zip(traces, cases):
        output = trace['output']
        original = case['state']
        witness = {'id': trace['id'], 'native_outcome': trace['outcome'],
                   'native_error': trace['error'], 'process_exit': trace['exit_code']}
        if output:
            state = output['state']
            old_ids = {ticket['id'] for ticket in original['tickets']}
            new = [ticket for ticket in state['tickets'] if ticket['id'] not in old_ids]
            witness.update({'original_prefix_preserved': state['tickets'][:len(original['tickets'])] == original['tickets'],
                'other_state_preserved': {k:v for k,v in state.items() if k != 'tickets'} ==
                                         {k:v for k,v in original.items() if k != 'tickets'},
                'actual_new_tickets': new,
                'original_creation_requirement_met': len(new) == 1 and
                len(state['tickets']) == len(original['tickets']) + 1 and
                new[0]['account'] == 'acct-a' and new[0]['status'] == 'open' and new[0]['issue'] == 'vpn'})
        else:
            witness['original_creation_requirement_met'] = None
            witness['limits'] = 'No valid returned state; execution error, no independently committed ticket service exists.'
        witnesses.append(witness)
    score_observations.append({'candidate': name, 'native_summary': summary, 'witnesses': witnesses})

all_traces = list(OUT.glob('native-*/traces.jsonl')) + list(OUT.glob('lifecycle-*/attempts/*/traces.jsonl'))
actual_count = sum(len(rows(path)) for path in all_traces)
counts = {'actual_native_candidate_case_executions': actual_count,
          'operator_process_interruptions': sum(command['exit_code'] == -9 for command in commands),
          'lifecycle_reserved_case_runs': sum(obs['post_status_state']['used_case_runs'] for obs in observations),
          'setup_rejections_without_candidate_execution': 1}
assert actual_count == 62, counts
assert counts['operator_process_interruptions'] == 4, counts
assert all(obs['post_status_state'] == obs['repeat_status_state'] for obs in observations)
assert all(obs['post_status_files'] == obs['repeat_status_files'] for obs in observations)
assert observations[2]['actual_case_executions'] == 2
assert observations[2]['post_status_state']['best_attempt'] is None
assert observations[2]['post_status_state']['attempts'][0]['status'] == 'pending'
for obs in observations[:2] + observations[3:5]:
    assert obs['post_status_state']['best_attempt'] == 0
    assert obs['post_status_state']['attempts'][0]['status'] == 'complete'
assert observations[5]['post_status_state']['best_attempt'] == 1
assert observations[5]['post_status_state']['attempts'][1]['decision_recovered'] is True
expected_outcomes = {'clean':'PASS', 'alternative':'PASS', 'reset-probe':'PASS',
                     'false-claim':'FAIL', 'malformed':'ERROR', 'runtime-error':'ERROR'}
for score in score_observations:
    assert all(w['native_outcome'] == expected_outcomes[score['candidate']] for w in score['witnesses'])
    assert score['native_summary']['selected_count'] == 2
write(OUT / 'lifecycle-observations.json', observations)
write(OUT / 'score-observations.json', score_observations)
write(OUT / 'counts.json', counts)
write(OUT / 'commands.json', commands)
write(OUT / 'protected-after.json', protected())
assert read(OUT / 'protected-before.json') == read(OUT / 'protected-after.json')
write(OUT / 'all-evidence-sha256.json', inventory(OUT))
print(json.dumps({'status': 'completed', 'counts': counts,
                  'scope': 'Independent synthetic development construction; no semantic skill verdict or adjudicated finding.'}, indent=2))
