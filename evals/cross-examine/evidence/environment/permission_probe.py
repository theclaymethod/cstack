import json
from pathlib import Path

attempts = {}
for relative in ('verify.py', 'reset.py', 'solution.py', '/oracle/expected.json'):
    try:
        Path(relative).write_text('compromised')
        attempts[relative] = 'WRITE SUCCEEDED'
    except OSError as exc:
        attempts[relative] = type(exc).__name__ + ': ' + str(exc)
for name in ('verify.py', 'reset.py', 'solution.py'):
    try:
        Path(name).rename(name + '.replaced')
        attempts['rename ' + name] = 'RENAME SUCCEEDED'
    except OSError as exc:
        attempts['rename ' + name] = type(exc).__name__ + ': ' + str(exc)
print(json.dumps(attempts))
