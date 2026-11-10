"""Project-local repaired entrypoint; use native task checks on the frozen case."""
import importlib.util
import json
from pathlib import Path
import sys
repo = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('native_evaluate', repo/'evaluate.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
case = next(c for c in native.load_cases('development') if c['id'] == sys.argv[1])
result = native.grade(json.loads(Path(sys.argv[2]).read_text()), case)
print(json.dumps(result, sort_keys=True))
raise SystemExit(0 if result['outcome'] == 'PASS' else 1)
