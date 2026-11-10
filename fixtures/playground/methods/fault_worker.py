"""Owned-process fault driver. Never loaded by a support candidate or installed skill."""
import errno
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import sys


def main():
    config = json.loads(Path(sys.argv[1]).read_text())
    root = Path(config['root']).resolve()
    source = root / 'evaluate.py'
    if hashlib.sha256(source.read_bytes()).hexdigest() != config['source_sha256']:
        raise RuntimeError('Fault mapping source changed')
    spec = importlib.util.spec_from_file_location('fault_native', source)
    native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
    events = Path(config['events'])

    def event(item):
        item.update(pid=os.getpid(), source_sha256=config['source_sha256'])
        with events.open('a') as stream:
            stream.write(json.dumps(item, sort_keys=True) + '\n'); stream.flush(); os.fsync(stream.fileno())

    if config['mode'] == 'lifecycle':
        campaign = Path(config['campaign'])
        fired = False
        errors = set()

        def trace(frame, kind, arg):
            nonlocal fired
            if frame.f_code.co_filename != str(source):
                return trace
            if kind == 'exception':
                errors.add(id(frame))
            if fired or config['boundary'] == 'unreached':
                return trace
            name = frame.f_code.co_name
            boundary = config['boundary']
            reached = False
            if boundary == 'reservation.published':
                reached = name == 'reserve_attempt' and kind == 'return' and isinstance(arg, dict)
            elif boundary == 'summary.published':
                reached = name == 'complete_attempt' and kind == 'call'
            elif boundary == 'completion.published' and name == 'save_state' and kind == 'return':
                state = frame.f_locals.get('state', {})
                reached = bool(state.get('attempts')) and state['attempts'][-1]['status'] == 'complete'
            if reached and id(frame) not in errors:
                fired = True
                event({'boundary': boundary, 'function': name, 'event': kind,
                       'line': frame.f_lineno, 'action': config['action']})
                if config['action'] == 'kill':
                    os.kill(os.getpid(), signal.SIGKILL)
            return trace
        sys.settrace(trace)
        try:
            native.start_campaign(campaign, 24, 8)
        finally:
            sys.settrace(None)
        Path(config['completed']).write_text(json.dumps({'completed': True, 'activations': int(fired)}))
    else:
        # Interpose only this module's os reference, not the host/global os module.
        target = Path(config['target'])
        native.write_json(target, {'revision': 1})
        real_os = native.os
        count = 0
        attempt = 0

        class StorageBoundary:
            def __getattr__(self, name):
                original = getattr(real_os, name)
                if name != config['operation']:
                    return original

                def operation(*args, **kwargs):
                    nonlocal count
                    count += 1
                    fail = config['action'] != 'noop' and (count == 1 or config['action'] == 'persistent')
                    if fail:
                        event({'operation': name, 'occurrence': count, 'attempt': attempt,
                               'action': 'raise-OSError', 'errno': errno.ENOSPC})
                        raise OSError(errno.ENOSPC, 'Synthetic scoped storage boundary fault')
                    return original(*args, **kwargs)
                return operation

        native.os = StorageBoundary()
        attempts = []
        for attempt in [1, 2]:
            before = target.read_text()
            try:
                native.write_json(target, {'revision': 2})
                failure = None
            except OSError as error:
                failure = {'errno': error.errno, 'type': type(error).__name__}
            attempts.append({'attempt': attempt, 'before': before, 'after': target.read_text(),
                             'error': failure})
        native.os = real_os
        Path(config['completed']).write_text(json.dumps({'attempts': attempts,
              'temporary_files': [p.name for p in target.parent.glob('.write-*')]}))


if __name__ == '__main__':
    main()
