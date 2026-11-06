import json
import sqlite3
from pathlib import Path

try:
    expected = {'target': 'New Lane', 'preserve': 'Keep Street'}
    with sqlite3.connect('state.sqlite') as db:
        rows = dict(db.execute('SELECT id, address FROM customers'))
    passed = rows == {1: expected['target'], 2: expected['preserve']}
    passed = passed and json.loads(Path('audit.json').read_text()).get('method') == 'reference'
except (OSError, ValueError, TypeError, KeyError, AttributeError, sqlite3.Error):
    passed = False
print(json.dumps({'passed': bool(passed)}))
raise SystemExit(0 if passed else 1)
