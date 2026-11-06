import json
from pathlib import Path
passed = not Path("result.json").exists()
print(json.dumps({"passed":passed}))
raise SystemExit(0 if passed else 1)
