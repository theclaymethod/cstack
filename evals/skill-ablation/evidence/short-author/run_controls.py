"""Invoke the real native CLI and preserve receipts; do not reimplement grading."""
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
WORKSPACE = BASE.parents[1]
receipt = []
for name in ('legitimate', 'alternative_unique_id', 'false_creation_claim', 'guidance_only', 'original_support_agent'):
    relative = BASE.relative_to(WORKSPACE)
    args = [sys.executable, 'evaluate.py', 'run', '--candidate', str(relative / 'controls' / (name + '.py')), '--cases', str(relative / 'author/approved.jsonl'), '--suite', 'development', '--out', str(relative / 'native-runs' / name)]
    process = subprocess.run(args, cwd=WORKSPACE, text=True, capture_output=True)
    (BASE / 'native-runs' / (name + '.stdout.txt')).write_text(process.stdout)
    (BASE / 'native-runs' / (name + '.stderr.txt')).write_text(process.stderr)
    receipt.append({'name': name, 'argv': args, 'cwd': str(WORKSPACE), 'exit_code': process.returncode})
    (BASE / 'native-runs/command-receipts.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if process.returncode != 0:
        raise SystemExit(f'Native command errored: {name}: {process.stderr}')
    result = json.loads((BASE / 'native-runs' / name / 'summary.json').read_text())
    print(json.dumps({'control': name, 'counts': result['counts'], 'executed': result['executed_count']}))
