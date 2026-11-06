import sqlite3
from pathlib import Path

for artifact in ("state.sqlite", "state.sqlite-journal", "state.sqlite-wal", "state.sqlite-shm", "result.json", "audit.json"):
    Path(artifact).unlink(missing_ok=True)
with sqlite3.connect("state.sqlite") as db:
    db.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, address TEXT NOT NULL)")
    db.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Old Road"), (2, "Keep Street")])
