"""Additional read-only checker runs; never executes native candidates."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

BASE = Path(__file__).resolve().parents[2]
PACKET = BASE / 'review-packet-repaired'
RECEIPTS = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def files(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}

results = []
for name in ['archive-baseline', 'h1-initial-state-mismatch', 'h2-reviewed-output-mismatch', 'h3-unsupported-source-quote']:
    archive = PACKET / name
    destination = RECEIPTS / ('additional-checker-' + name)
    destination.mkdir(exist_ok=False)
    before = files(archive)
    command = [sys.executable, str(archive / 'verify_archive.py')]
    run = subprocess.run(command, capture_output=True)
    (destination / 'stdout.bin').write_bytes(run.stdout)
    (destination / 'stderr.bin').write_bytes(run.stderr)
    after = files(archive)
    write_json(destination / 'inputs-before.json', before)
    write_json(destination / 'inputs-after.json', after)
    receipt = {
        'run_kind': 'additional read-only checker rerun for receipt preservation',
        'command': command,
        'cwd': str(Path.cwd()),
        'stdin': 'inherited; checker consumes no stdin',
        'exit_code': run.returncode,
        'checker_sha256': before['verify_archive.py'],
        'all_archive_files_unchanged': before == after,
        'stdout_sha256': sha(destination / 'stdout.bin'),
        'stderr_sha256': sha(destination / 'stderr.bin'),
        'native_candidate_invocations': 0,
    }
    write_json(destination / 'receipt.json', receipt)
    results.append({'archive': name, **receipt})
write_json(RECEIPTS / 'additional-checker-runs.json', results)
print(json.dumps([{'archive': r['archive'], 'exit_code': r['exit_code'], 'all_archive_files_unchanged': r['all_archive_files_unchanged']} for r in results], indent=2))
