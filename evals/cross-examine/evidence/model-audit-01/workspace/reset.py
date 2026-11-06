import sqlite3
from pathlib import Path

with sqlite3.connect('state.sqlite') as db:
    db.execute('CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, address TEXT NOT NULL)')
    db.execute('DELETE FROM customers')
    db.executemany('INSERT INTO customers VALUES (?, ?)', [(1, 'Old Road'), (2, 'Keep Street')])
for artifact in ('result.json', 'audit.json'):
    Path(artifact).unlink(missing_ok=True)
