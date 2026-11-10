"""Replay independently constructed cases through a fresh native playground workspace.

These are development controls, not an invocation or effectiveness test of a model.
The operator injector sends SIGKILL only to its own disposable native process.
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def invoke(command, cwd, receipt):
    proc = subprocess.Popen(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=90)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
        receipt.write_text(json.dumps({'command': command, 'timeout': True,
                                      'stdout': stdout, 'stderr': stderr}, indent=2) + '\n')
        raise RuntimeError('Timed out: ' + str(command[1]))
    receipt.write_text(json.dumps({'command': command, 'exit': proc.returncode,
                                  'stdout': stdout, 'stderr': stderr}, indent=2) + '\n')
    require(proc.returncode == 0, 'Command failed; see ' + str(receipt))


def validate(base, workspace=None):
    base = Path(base).resolve()
    workspace = Path(workspace).resolve() if workspace else base.parents[1]
    checks = []

    def check(condition, message):
        require(condition, message)
        checks.append(message)

    protected = {'AGENTS.md', 'README.md', 'evaluate.py', 'support_agent.py',
                 'evals/spec.json', 'evals/cases.jsonl', 'evals/rubric.md',
                 'exercises/06-cross-examine.md', 'exercises/fixtures/verify_claim.py',
                 'exercises/fixtures/forged-result.json', 'examples/candidates/improved.py'}
    protected.update(str(p.relative_to(workspace)) for p in (workspace / '.agents/skills').rglob('*')
                     if p.is_file())
    before_sources, after_sources = read(base / 'source-before.json'), read(base / 'source-after.json')
    check(set(before_sources) == set(after_sources) == protected
          and any(p.startswith('.agents/skills/adversarial-cases/') for p in protected),
          'Complete expected protected source inventory is present')
    current_sources = {p: hashlib.sha256((workspace / p).read_bytes()).hexdigest() for p in protected}
    check(before_sources == after_sources == current_sources,
          'Source records agree and match the current protected fixture and installed skills')
    commands = read(base / 'commands.json')
    expected_stops = {'lifecycle-complete-stop-1', 'lifecycle-complete-stop-2',
                      'lifecycle-before-execute'}
    lifecycle_labels = expected_stops | {'lifecycle-noop'}
    command_labels = {'lifecycle-clean'} | lifecycle_labels
    command_labels.update(label + suffix for label in lifecycle_labels
                          for suffix in ['-status', '-status-repeat'])
    candidates = ['forged', 'legitimate', 'legitimate-alternative']
    command_labels.update('native-' + name for name in candidates)
    command_labels.update('proxy-' + name + '-' + str(index) for name in candidates for index in range(2))
    check(len(commands) == len(command_labels) and {r['label'] for r in commands} == command_labels,
          'Every required command has exactly one recorded receipt')
    for receipt in commands:
        check(read(base / (receipt['label'] + '.receipt.json')) == receipt,
              'Retained command receipt matches command inventory: ' + receipt['label'])
        check(receipt['exit_code'] == (-9 if receipt['label'] in expected_stops else 0),
              'Expected process exit: ' + receipt['label'])

    native_spec = importlib.util.spec_from_file_location('adversarial_native_evaluate', workspace / 'evaluate.py')
    native = importlib.util.module_from_spec(native_spec)
    native_spec.loader.exec_module(native)
    run_paths = [base / label / 'attempts/000-baseline'
                 for label in ['lifecycle-clean', 'lifecycle-noop', 'lifecycle-complete-stop-1', 'lifecycle-complete-stop-2']]
    run_paths.extend(base / ('native-' + name) for name in candidates)
    for path in run_paths:
        native.checked_run(path)
        checks.append('Native retained-run validation: ' + str(path.relative_to(base)))

    clean = rows(base / 'lifecycle-clean/attempts/000-baseline/traces.jsonl')
    clean_outputs = [(r['id'], r['output'], r['outcome']) for r in clean]
    observations = read(base / 'lifecycle-observations.json')
    check(len(observations) == len(lifecycle_labels) and {r['label'] for r in observations} == lifecycle_labels,
          'All required lifecycle observations are present exactly once')
    for observation in observations:
        label = observation['label']
        pre, post = observation['pre_status_state'], observation['post_status_state']
        check(pre['used_case_runs'] == post['used_case_runs'] == 8,
              label + ': reservation remains charged')
        before = observation['pre_status_files']
        after = observation['post_status_files']
        check(set(before) == set(after) and all(before[k] == after[k] for k in before
                                                if k != 'state.json'),
              label + ': recovery creates no evidence and preserves original bytes')
        # Recompute the files after repeated status, independently of the builder's inventory.
        current = {str(p.relative_to(base / label)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (base / label).rglob('*') if p.is_file()}
        check(current == after, label + ': retained files match final inventory')
        if label == 'lifecycle-noop':
            check(observation['activation_count'] == 0 and observation['process_exit'] == 0
                  and not (base / (label + '.activation.jsonl')).exists()
                  and read(base / (label + '.completion.json'))['activation_count'] == 0,
                  label + ': armed trigger never activates')
        else:
            events = rows(base / (label + '.activation.jsonl'))
            config = read(base / (label + '.config.json'))
            check(observation['activation_count'] == len(events) == 1
                  and observation['process_exit'] == -9
                  and events[0]['function'] == config['function']
                  and events[0]['attempt_id'] == config['attempt_id']
                  and events[0]['source_sha256'] == config['source_sha256'],
                  label + ': targeted event and actual SIGKILL observed')
            check(pre['attempts'][0]['status'] == 'pending' and pre['best_attempt'] is None,
                  label + ': interruption precedes ledger completion')
        if label == 'lifecycle-before-execute':
            check(post == pre and post['attempts'][0]['status'] == 'pending'
                  and not (base / label / 'attempts').exists(),
                  label + ': rejected reduction lacks complete evidence and remains pending')
        else:
            traces = rows(base / label / 'attempts/000-baseline/traces.jsonl')
            check([(r['id'], r['output'], r['outcome']) for r in traces] == clean_outputs
                  and post['attempts'][0]['status'] == 'complete' and post['best_attempt'] == 0,
                  label + ': outcomes match clean control and completed evidence is retained')
            if label in expected_stops:
                check(post['attempts'][0]['completion_recovered'] is True,
                      label + ': native reconciliation recovers completed measurement')

    score_cases = rows(base / 'score-boundary.jsonl')
    check(len(score_cases) == 2, 'Both preserved-context and reduced scoring cases replayed')
    for candidate in candidates:
        traces = rows(base / ('native-' + candidate) / 'traces.jsonl')
        check(len(traces) == 2, candidate + ': both case variants executed')
        for index, trace in enumerate(traces):
            original, output = trace['input']['state'], trace['output']
            state = output['state']
            prior_ids = {ticket['id'] for ticket in original['tickets']}
            new = [ticket for ticket in state['tickets'] if ticket['id'] not in prior_ids]
            proxy_input = read(base / ('proxy-input-' + candidate + '-' + str(index) + '.json'))
            proxy_receipt = read(base / ('proxy-' + candidate + '-' + str(index) + '.receipt.json'))
            check(proxy_input == output and json.loads(proxy_receipt['stdout'])['passed'] is True,
                  candidate + '/' + trace['id'] + ': exact output accepted by supplied defective proxy')
            check(state['tickets'][:len(original['tickets'])] == original['tickets']
                  and {k: v for k, v in state.items() if k != 'tickets'}
                  == {k: v for k, v in original.items() if k != 'tickets'},
                  candidate + '/' + trace['id'] + ': original state preserved')
            if candidate == 'forged':
                check(not new and state == original and trace['outcome'] == 'FAIL',
                      trace['id'] + ': no actual ticket; native rejects false creation claim')
            else:
                check(len(new) == 1 and len(state['tickets']) == len(original['tickets']) + 1
                      and new[0]['account'] == 'acct-a' and new[0]['issue'] == 'vpn'
                      and new[0]['status'] == 'open' and trace['outcome'] == 'PASS',
                      candidate + '/' + trace['id'] + ': actual valid ticket accepted by native grader')
    traces = list(base.glob('lifecycle-*/attempts/*/traces.jsonl')) + list(base.glob('native-*/traces.jsonl'))
    actual = sum(len(rows(path)) for path in traces)
    counts = read(base / 'counts.json')
    check(actual == counts['actual_native_case_executions'] == 38
          and sum(r['exit_code'] == -9 for r in commands) == counts['operator_process_interruptions'] == 3,
          'Actual 38 case executions and three interruptions reconcile with receipts')
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    workspace = output / 'workspace'
    invoke([sys.executable, str(SOURCE / 'fixtures/playground/scripts/new_workspace.py'),
            '--source', str(SOURCE), '--out', str(workspace)], SOURCE, output / 'materialize.json')
    base = workspace / 'eval-runs/case-build'
    base.mkdir(parents=True)
    for name in ['build_forward.py', 'inject_native.py']:
        shutil.copy2(HERE / name, base / name)
    invoke([sys.executable, str(base / 'build_forward.py')], workspace, output / 'construction.json')
    checks = validate(base, workspace)
    result = {'scope': 'Replay of constructed synthetic development controls; no new skill invocation, '
                       'human labels, current-native finding, or production reliability claim',
              'checks': checks, 'counts': read(base / 'counts.json'), 'status': 'passed'}
    (output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'checks': len(checks), 'counts': result['counts']}, indent=2))


if __name__ == '__main__':
    main()
