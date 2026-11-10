"""Run the existing C Stack control suites plus this test repo's native checks."""

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

from source_checkout import locate

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--suite', choices=['all', 'expert-review', 'cross-examine', 'bootstrap', 'bootstrap-audit', 'hill-climb-audit', 'adversarial-cases', 'adversarial-audit', 'methods', 'judge-calibration', 'playground'], default='all')
    parser.add_argument('--dspy-check', action='store_true', help='Require optional DSPy SDK compatibility in the methods group')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = locate(args.source, ROOT)
    output = args.out.resolve()
    if not (source / 'plugin.json').is_file() or json.loads((source / 'plugin.json').read_text()).get('name') != 'cstack':
        raise SystemExit('Use --source with a C Stack checkout')
    output.mkdir(parents=True, exist_ok=False)
    commands = {
        'expert-review': ([sys.executable, str(source / 'evals/expert-review/calibration.py'), str(output / 'expert-review')], source),
        'cross-examine': ([sys.executable, str(source / 'evals/cross-examine/calibration.py'), str(output / 'cross-examine'), '--executor', 'local'], source),
        'bootstrap': ([sys.executable, str(source / 'evals/bootstrap/replay.py'), str(output / 'bootstrap')], source),
        'bootstrap-audit': ([sys.executable, str(source / 'evals/bootstrap/cross_examine.py'), str(output / 'bootstrap-audit')], source),
        'hill-climb-audit': ([sys.executable, str(source / 'evals/hill-climb/cross_examine.py'), '--out', str(output / 'hill-climb-audit')], source),
        'adversarial-cases': ([sys.executable, str(source / 'evals/adversarial-cases/replay.py'), '--out', str(output / 'adversarial-cases')], source),
        'adversarial-audit': ([sys.executable, str(source / 'evals/adversarial-cases/cross_examine.py'), '--out', str(output / 'adversarial-audit')], source),
        'methods': ([sys.executable, '-m', 'methods.run', '--out', str(output / 'methods')]
                    + (['--dspy-check'] if args.dspy_check else []), ROOT),
        'judge-calibration': ([sys.executable, '-m', 'judge_calibration.run', '--out', str(output / 'judge-calibration')], ROOT),
        'playground': ([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], ROOT),
    }
    selected = commands if args.suite == 'all' else {args.suite: commands[args.suite]}
    results = []
    for name, (command, cwd) in selected.items():
        print('Running ' + name, flush=True)
        proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        timed_out = False
        try:
            stdout, stderr = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate()
        (output / (name + '.stdout.txt')).write_text(stdout)
        (output / (name + '.stderr.txt')).write_text(stderr)
        result = {'suite': name, 'command': command, 'cwd': str(cwd), 'exit': proc.returncode,
                  'status': 'timeout' if timed_out else 'passed' if proc.returncode == 0 else 'failed',
                  'stdout': name + '.stdout.txt', 'stderr': name + '.stderr.txt'}
        results.append(result)
        (output / 'summary.json').write_text(json.dumps({'scope': 'Local synthetic control suites and native fixture tests; not model-performance evaluation', 'results': results}, indent=2) + '\n')
        print(json.dumps({'suite': name, 'status': result['status']}), flush=True)
    print(json.dumps({'evidence_directory': str(output), 'results': results}, indent=2))
    raise SystemExit(0 if all(result['status'] == 'passed' for result in results) else 1)


if __name__ == '__main__':
    main()
