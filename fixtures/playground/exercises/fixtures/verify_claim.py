"""Intentionally flawed audit fixture. This is not the native project evaluator."""

import json
from pathlib import Path
import sys

result = json.loads(Path(sys.argv[1]).read_text())
accepted = result.get('action') == 'create_ticket'
print(json.dumps({'passed': accepted, 'boundary': 'intentionally defective action-claim proxy'}))
raise SystemExit(0 if accepted else 1)
