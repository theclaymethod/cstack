import json
import sqlite3
from pathlib import Path

try:
    passed = json.loads(Path('result.json').read_text()).get('success') is True
except (OSError, ValueError, TypeError, KeyError, AttributeError, sqlite3.Error):
    passed = False
print(json.dumps({'passed': bool(passed)}))
raise SystemExit(0 if passed else 1)
