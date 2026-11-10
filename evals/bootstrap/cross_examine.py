"""Replay the recorded Bootstrap validation flaws and repaired controls in copies."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
EVIDENCE = BASE / 'evidence/cross-examine'


def main():
    if len(sys.argv) > 1:
        output = Path(sys.argv[1]).resolve()
        output.mkdir(parents=True, exist_ok=False)
    else:
        runs = BASE.parents[1] / 'eval-runs'
        runs.mkdir(exist_ok=True)
        output = Path(tempfile.mkdtemp(prefix='bootstrap-audit-', dir=runs))
    if output == BASE or BASE in output.parents:
        raise ValueError('Audit outputs must be outside the source fixture')

    observations = []
    for revision in ['original', 'repaired']:
        copied = output / revision / 'evals/bootstrap'
        shutil.copytree(BASE, copied)
        replay = copied / 'replay.py'
        if revision == 'original':
            shutil.copyfile(EVIDENCE / 'original-replay.py', replay)
        cases = copied / 'fixture/evals/bootstrap-vpn.jsonl'
        baseline = cases.read_bytes()
        variants = [('baseline', baseline, 0, None)]
        for name, reason in [
            ('attempt-1-input-substitution', 'Authored input/family differs from the approved scenario'),
            ('attempt-2-required-fields-omitted', 'Case is missing required project fields'),
            ('attempt-3-alternative-narrowing', 'Authored expectation differs from approved contract'),
        ]:
            rejected = revision == 'repaired' or name == 'attempt-3-alternative-narrowing'
            variants.append((name, (EVIDENCE / (name + '.cases.jsonl')).read_bytes(), 1 if rejected else 0, reason if rejected else None))
        if revision == 'repaired':
            rows = [json.loads(line) for line in baseline.decode().splitlines()]
            source = json.loads((copied / 'evidence/approved-inputs.json').read_text())['cases']
            row = next(row for row in rows if row['id'] == 'bootstrap-vpn-s04-r2')
            row['input'] = source[row['id']]['renderings'][1]
            row['expected']['allowed_actions'].reverse()
            variants.append(('equivalent-structured-input', ('\n'.join(json.dumps(row, sort_keys=True) for row in rows) + '\n').encode(), 0, None))
        try:
            for name, candidate, expected_exit, reason in variants:
                cases.write_bytes(candidate)
                destination = output / revision / name
                command = [sys.executable, str(replay), str(destination)]
                proc = subprocess.run(command, capture_output=True, text=True)
                record = {'revision': revision, 'control': name, 'command': command, 'replay_sha256': hashlib.sha256(replay.read_bytes()).hexdigest(), 'candidate_sha256': hashlib.sha256(candidate).hexdigest(), 'expected_exit': expected_exit, 'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
                observations.append(record)
                if proc.returncode != expected_exit or (reason and reason not in proc.stderr):
                    raise AssertionError('Unexpected audit result: ' + revision + '/' + name)
                if expected_exit == 0:
                    result = json.loads(proc.stdout)
                    if result['expected_vs_observed_mismatches'] or result['case_control_verdicts'] != {'PASS': 5, 'FAIL': 43, 'ERROR': 8}:
                        raise AssertionError('Unexpected development-control verdicts')
        finally:
            cases.write_bytes(baseline)
            (output / 'before-after.json').write_text(json.dumps(observations, indent=2) + '\n')
    print(json.dumps({'evidence_directory': str(output), 'replay_observations': len(observations), 'result': 'Recorded original acceptances, repaired rejections, and legitimate controls reproduced', 'scope': 'Frozen synthetic development controls; no new agent workflow or held-out claim'}, indent=2))


if __name__ == '__main__':
    main()
