"""Bounded operator process/storage experiments and native subprocess error cases."""
import errno
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from .native import ROOT, Runs, evaluate, read_rows, write
from .synthetic import case_for


def invoke(config, directory):
    config_file = directory / 'config.json'; write(config_file, config)
    proc = subprocess.Popen([sys.executable, str(ROOT / 'methods/fault_worker.py'), str(config_file)],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL); stdout, stderr = proc.communicate()
        write(directory / 'process.json', {'pid': proc.pid, 'exit': proc.returncode,
              'stdout': stdout, 'stderr': stderr, 'supervisor_timeout': True})
        raise RuntimeError('Fault worker timed out; incomplete experiment retained')
    result = {'pid': proc.pid, 'exit': proc.returncode, 'stdout': stdout, 'stderr': stderr,
              'supervisor_timeout': False}
    write(directory / 'process.json', result)
    return result


def inventory(path):
    return {str(p.relative_to(path)): evaluate.digest(p) for p in path.rglob('*') if p.is_file()}


def run(directory):
    directory = Path(directory).resolve(); directory.mkdir(parents=True, exist_ok=False)
    source_hashes = {f: evaluate.digest(ROOT / f) for f in evaluate.FROZEN_FILES}
    results = {'lifecycle': [], 'storage': [], 'subprocess': []}
    lifecycle_actual = 0
    for label, boundary, action in [('clean', 'unreached', 'noop'),
            ('armed-unreached', 'unreached', 'kill'),
            ('observed-noop', 'summary.published', 'noop'),
            ('reservation', 'reservation.published', 'kill'),
            ('summary', 'summary.published', 'kill'),
            ('completion', 'completion.published', 'kill')]:
        trial = directory / label; trial.mkdir()
        config = {'mode': 'lifecycle', 'root': str(ROOT), 'source_sha256': source_hashes['evaluate.py'],
                  'boundary': boundary, 'action': action, 'campaign': str(trial / 'campaign'),
                  'events': str(trial / 'events.jsonl'), 'completed': str(trial / 'completed.json')}
        receipt = invoke(config, trial)
        events = read_rows(trial / 'events.jsonl') if (trial / 'events.jsonl').exists() else []
        expected_activations = int(boundary != 'unreached')
        if len(events) != expected_activations or any(e['pid'] != receipt['pid'] for e in events):
            raise RuntimeError('Target boundary not observed as configured: ' + label)
        expected_exit = -9 if action == 'kill' and events else 0
        if receipt['exit'] != expected_exit:
            raise RuntimeError('Perturbation effect differs from configured action: ' + label)
        campaign = trial / 'campaign'
        before = json.loads((campaign / 'state.json').read_text())
        before_files = inventory(campaign)
        first = evaluate.campaign_status(campaign)
        after = json.loads((campaign / 'state.json').read_text())
        after_files = inventory(campaign)
        repeated = evaluate.campaign_status(campaign)
        if inventory(campaign) != after_files or first != repeated or before['used_case_runs'] != after['used_case_runs']:
            raise RuntimeError('Recovery reran or changed charged work')
        if set(before_files) != set(after_files) or any(before_files[p] != after_files[p] for p in before_files if p != 'state.json'):
            raise RuntimeError('Recovery modified measurement evidence')
        traces = list(campaign.glob('attempts/*/traces.jsonl'))
        actual = sum(len(read_rows(p)) for p in traces); lifecycle_actual += actual
        if boundary == 'reservation.published':
            if actual or after['best_attempt'] is not None or after['attempts'][0]['status'] != 'pending':
                raise RuntimeError('Incomplete reservation improperly promoted')
        elif actual != 8 or after['best_attempt'] != 0 or after['attempts'][0]['status'] != 'complete':
            raise RuntimeError('Completed measurement was not retained/recovered')
        for path in traces:
            evaluate.checked_run(path.parent)
        results['lifecycle'].append({'label': label, 'boundary': boundary, 'action': action,
            'activation_count': len(events), 'process': receipt, 'before': before, 'after': after,
            'before_files': before_files, 'after_files': after_files, 'actual_cases': actual})

    for operation in ['fsync', 'replace']:
        for action in ['noop', 'once', 'persistent']:
            trial = directory / ('storage-' + operation + '-' + action); trial.mkdir()
            config = {'mode': 'storage', 'root': str(ROOT), 'source_sha256': source_hashes['evaluate.py'],
                      'operation': operation, 'action': action, 'target': str(trial / 'published.json'),
                      'events': str(trial / 'events.jsonl'), 'completed': str(trial / 'completed.json')}
            receipt = invoke(config, trial)
            if receipt['exit'] != 0:
                raise RuntimeError('Storage worker failed before observations')
            observation = json.loads((trial / 'completed.json').read_text())
            events = read_rows(trial / 'events.jsonl') if (trial / 'events.jsonl').exists() else []
            expected = 0 if action == 'noop' else 1 if action == 'once' else 2
            if (len(events) != expected or observation['temporary_files']
                    or any(e['pid'] != receipt['pid'] or e['operation'] != operation for e in events)):
                raise RuntimeError('Storage activation/cleanup witness mismatch')
            for index, attempt in enumerate(observation['attempts']):
                fails = action == 'persistent' or action == 'once' and index == 0
                if (bool(attempt['error']) != fails or (fails and attempt['before'] != attempt['after'])
                        or fails and attempt['error']['errno'] != errno.ENOSPC):
                    raise RuntimeError('Failed storage write damaged publication')
            expected_revision = 1 if action == 'persistent' else 2
            if json.loads(observation['attempts'][-1]['after'])['revision'] != expected_revision:
                raise RuntimeError('Storage retry did not preserve intended once/persistent behavior')
            results['storage'].append({'operation': operation, 'action': action,
                                       'process': receipt, 'events': events, 'observation': observation})

    runs = Runs(directory / 'subprocess-native', 5)
    programs = {'healthy': 'import json,sys\np=json.load(sys.stdin)\np["state"]["tickets"].append({"id":"new","account":"acct-a","status":"open","issue":"vpn"})\nprint(json.dumps({"action":"create_ticket","account":"acct-a","state":p["state"],"note":"Created"}))\n',
        'deadline': 'import time\ntime.sleep(60)\n',
        'prefix-deadline': 'import sys,time\nsys.stdout.write("{\\\"action\\\":");sys.stdout.flush();time.sleep(60)\n',
        'valid-nonzero': 'print("{}",flush=True)\nraise SystemExit(2)\n',
        'malformed': 'print("not JSON")\n'}
    # The nonzero control emits a fully valid response before failing; exit status remains decisive.
    programs['valid-nonzero'] = programs['healthy'] + 'raise SystemExit(2)\n'
    for label, code in programs.items():
        candidate = directory / (label + '.py'); candidate.write_text(code)
        trace = runs.run(label, candidate, [case_for('subprocess:' + label, 'create')])[0]
        expected = 'PASS' if label == 'healthy' else 'ERROR'
        if trace['outcome'] != expected:
            raise RuntimeError('Subprocess failure misclassified')
        if label == 'prefix-deadline' and not trace['stdout'].startswith('{"action":'):
            raise RuntimeError('Prefix boundary not observed before timeout')
        results['subprocess'].append(trace)
    if {f: evaluate.digest(ROOT / f) for f in source_hashes} != source_hashes:
        raise RuntimeError('Protected native source changed')
    results.update(status='passed', source_hashes=source_hashes, actual_native_executions=lifecycle_actual + 5,
        process_interruptions=3, candidate_timeouts=2, budget={'max_cases': 53, 'max_interruptions': 3},
        scope='Operator process/API faults; not dependency outages, power loss or DSPy training labels',
        instrumentation='Source-pinned named mappings to native Python call/return events; version sensitive', provider_calls=0)
    write(directory / 'results.json', results)
    return results
