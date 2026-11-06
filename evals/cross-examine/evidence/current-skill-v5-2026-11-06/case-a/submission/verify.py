import json,sqlite3
try:
    with sqlite3.connect('file:state.sqlite?mode=ro',uri=True) as db:
        passed=db.execute('SELECT id,address FROM customers ORDER BY id').fetchall()==[(1,'New Lane'),(2,'Keep Street')]
except (OSError,sqlite3.Error):
    passed=False
print(json.dumps({'passed':passed}))
raise SystemExit(0 if passed else 1)
