"""Rebuild this attacker's independent 76-case, four-interruption development run.

The components have been executed in the attached workspace. This convenience
wrapper is unexecuted: rerunning it consumes a fresh 76-case/four-stop budget.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent / 'frozen'
SCRIPTS = HERE / 'workspace/eval-runs/attack-execution'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    output = args.out.resolve()
    if HERE not in output.parents:
        raise SystemExit('Choose a new path inside this attacker-owned directory')
    subprocess.run([sys.executable, str(FROZEN / 'fixtures/playground/scripts/new_workspace.py'),
        '--source', str(FROZEN), '--out', str(output)], check=True)
    target = output / 'eval-runs/attack-execution'
    target.mkdir(parents=True)
    for name in ['inject.py', 'reproduce.py', 'finalize.py', 'reduce.py']:
        shutil.copyfile(SCRIPTS / name, target / name)
    for name, expected in [('reproduce.py', 1), ('finalize.py', 0), ('reduce.py', 0)]:
        process = subprocess.run([sys.executable, str(target / name)], cwd=output,
                                 text=True, capture_output=True, timeout=60)
        receipt = {'driver': name, 'exit_code': process.returncode,
                   'stdout': process.stdout, 'stderr': process.stderr,
                   'expected_exit': expected}
        (target / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
        if process.returncode != expected:
            raise SystemExit('Unexpected construction exit; see ' + str(target / (name + '.receipt.json')))
    print((target / 'evidence/counts.json').read_text())


if __name__ == '__main__':
    main()
