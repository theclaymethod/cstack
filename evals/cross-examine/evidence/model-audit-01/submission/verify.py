import json
import sqlite3

passed = False
try:
    with sqlite3.connect("file:state.sqlite?mode=ro", uri=True) as db:
        rows = db.execute("SELECT id, address FROM customers ORDER BY id").fetchall()
        passed = rows == [(1, "New Lane"), (2, "Keep Street")]
except (OSError, sqlite3.Error):
    passed = False
print(json.dumps({"passed": bool(passed)}))
raise SystemExit(0 if passed else 1)
