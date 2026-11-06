import sqlite3
import shutil
from pathlib import Path


with sqlite3.connect('state.sqlite') as db:
    db.execute('CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, address TEXT NOT NULL)')
    db.executemany('INSERT OR IGNORE INTO customers VALUES (?, ?)', [(1, 'Old Road'), (2, 'Keep Street')])
for artifact in ('result.json', 'audit.json'):
    path = Path(artifact)
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)
