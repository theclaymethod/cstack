"""Operator-only source-pinned tracer; never imported by evaluated candidates."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import signal
import sys

config = json.loads(Path(sys.argv[1]).read_text())
target = Path(config['target']).resolve()
actual = hashlib.sha256(target.read_bytes()).hexdigest()
if actual != config['source_sha256']:
    raise SystemExit('SETUP ERROR: source hash does not match target')
activations = 0


def tracer(frame, event, arg):
    global activations
    if frame.f_code.co_filename != str(target):
        return tracer
    local = frame.f_locals
    phase = config['phase']
    predicate = (
        phase == 'partial-2' and event == 'line'
        and frame.f_code.co_name == 'run_suite' and frame.f_lineno == 222
        and len(local.get('results', [])) == 2
        or phase == 'published-summary' and event == 'return'
        and frame.f_code.co_name == 'write_json'
        and str(local.get('path', '')).endswith('/000-baseline/summary.json')
        or phase == 'completed-memory' and event == 'return'
        and frame.f_code.co_name == 'complete_attempt'
        and local.get('attempt', {}).get('id') == 0
        or phase == 'proposal-decision' and event == 'return'
        and frame.f_code.co_name == 'decide_proposal'
        and local.get('attempt', {}).get('id') == 1
        or phase == 'unreachable' and event == 'return'
        and frame.f_code.co_name == 'complete_attempt'
        and local.get('attempt', {}).get('id') == 999
    )
    if predicate:
        activations += 1
        evidence = {'phase': phase, 'event': event, 'function': frame.f_code.co_name,
                    'line': frame.f_lineno, 'source_sha256': actual,
                    'pid': os.getpid(), 'action': 'SIGKILL_SELF',
                    'attempt_id': local.get('attempt', {}).get('id'),
                    'results_observed': len(local.get('results', []))}
        with Path(config['activation']).open('a') as stream:
            stream.write(json.dumps(evidence, sort_keys=True) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.kill(os.getpid(), signal.SIGKILL)
    return tracer


sys.argv = [str(target)] + config['native_args']
sys.path.insert(0, str(target.parent))
sys.settrace(tracer)
try:
    runpy.run_path(str(target), run_name='__main__')
finally:
    sys.settrace(None)
    Path(config['completion']).write_text(json.dumps({'activations': activations}))
