"""Operator-only tracer: preserves native runner source and stops this own process."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import signal
import sys

config_path = Path(sys.argv[1]).resolve()
config = json.loads(config_path.read_text())
root = Path(config['root']).resolve()
target = root / 'evaluate.py'
actual = hashlib.sha256(target.read_bytes()).hexdigest()
assert actual == config['source_sha256'], 'native source differs from armed source'
evidence = Path(config['activation_log'])
count = 0

def trace(frame, event, arg):
    global count
    if event == 'call' and frame.f_code.co_filename == str(target) and frame.f_code.co_name == config['function']:
        attempt = frame.f_locals.get('attempt', {})
        if attempt.get('id') == config['attempt_id']:
            count += 1
            item = {'event': 'trigger_reached', 'pid': os.getpid(), 'function': frame.f_code.co_name,
                    'line': frame.f_code.co_firstlineno, 'attempt_id': attempt['id'],
                    'source_sha256': actual, 'action': config['action']}
            with evidence.open('a') as out:
                out.write(json.dumps(item, sort_keys=True) + '\n')
                out.flush()
                os.fsync(out.fileno())
            if config['action'] == 'SIGKILL_SELF':
                os.kill(os.getpid(), signal.SIGKILL)
    return trace

sys.path.insert(0, str(root))
sys.argv = [str(target)] + config['native_args']
sys.settrace(trace)
try:
    runpy.run_path(str(target), run_name='__main__')
finally:
    sys.settrace(None)
    Path(config['completion_log']).write_text(json.dumps({'process_completed': True, 'activation_count': count}))
