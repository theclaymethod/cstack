import sqlite3
import shutil
from pathlib import Path

for name in ('state.sqlite', 'state.sqlite-wal', 'state.sqlite-shm', 'state.sqlite-journal'):
    path = Path(name)
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)

with sqlite3.connect('state.sqlite') as db:
    db.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, status TEXT NOT NULL)')
    db.execute('DELETE FROM orders')
    db.executemany('INSERT INTO orders VALUES (?, ?)', [(1, 'pending'), (2, 'shipped')])
for artifact in ('result.json', 'audit.json'):
    path = Path(artifact)
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)
