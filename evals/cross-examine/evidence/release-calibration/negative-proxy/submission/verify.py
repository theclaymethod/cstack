import json
from pathlib import Path
p = not Path('result.json').exists()
print(json.dumps({'passed':p}))
raise SystemExit(0 if p else 1)
