import json
import sqlite3
import subprocess
import sys
for statement in ("UPDATE customers SET address = 'Wrong Lane' WHERE id = 1", "DELETE FROM customers WHERE id = 2"):
    subprocess.run([sys.executable, '-I', '-B', 'reset.py'], check=True)
    with sqlite3.connect('state.sqlite') as db:
        db.execute(statement)
        rows = db.execute('SELECT id,address FROM customers ORDER BY id').fetchall()
    p = subprocess.run([sys.executable, '-I', '-B', 'verify.py'], capture_output=True, text=True)
    print(json.dumps({'statement': statement, 'rows': rows, 'verifier': p.stdout, 'exit': p.returncode}))
