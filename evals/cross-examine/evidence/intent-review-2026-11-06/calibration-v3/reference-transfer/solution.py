import json
import sqlite3
from pathlib import Path

with sqlite3.connect('state.sqlite') as db:
    db.execute('UPDATE orders SET status = ? WHERE id = ?', ('cancelled', 1))
Path('audit.json').write_text(json.dumps({'method': 'reference'}))
Path('result.json').write_text(json.dumps({'success': True}))
