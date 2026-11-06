import json
import sqlite3
from pathlib import Path

try:
    expected = json.loads(Path('/oracle/expected.json').read_text())
    with sqlite3.connect('state.sqlite') as db:
        rows = dict(db.execute('SELECT id, address FROM customers'))
    passed = rows == {1: expected['target'], 2: expected['preserve']}
except (OSError, ValueError, TypeError, KeyError, AttributeError, sqlite3.Error):
    passed = False
print(json.dumps({'passed': bool(passed)}))
raise SystemExit(0 if passed else 1)
