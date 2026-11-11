"""Bounded local command receipts; invokes only the project's native controls."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def run(label, args):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
    (OUT / 'commands').mkdir(exist_ok=True)
    (OUT / 'commands' / (label + '.stdout')).write_text(p.stdout)
    (OUT / 'commands' / (label + '.stderr')).write_text(p.stderr)
    receipt = dict(label=label, argv=[sys.executable, *args], cwd=str(ROOT),
                   started=start, ended=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   exit_code=p.returncode)
    with (OUT / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(receipt, sort_keys=True) + '\n')
    print(label, p.returncode, flush=True)
    if p.returncode:
        print(p.stderr, flush=True)
        raise SystemExit(p.returncode)

if __name__ == '__main__':
    frozen = ['evaluate.py', 'evals/spec.json', 'evals/rubric.md', 'evals/cases.jsonl',
              'support_agent.py', 'examples/candidates/improved.py', 'examples/candidates/regression.py']
    identity = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in frozen}
    (OUT / 'source-before.json').write_text(json.dumps(identity, indent=2) + '\n')
    (OUT / 'exercise-contract.json').write_text(json.dumps({
        'native_limit': 300, 'hill_climb_limit': 48, 'hill_climb_confirmation_reserve': 8,
        'mutable': 'standalone candidate artifacts only', 'source_boundary': identity,
        'objective': 'strict development improvement, zero lost passing cases; paired confirmation',
        'policy': 'synthetic readable cases; one deterministic run per selected case',
        'judge': 'documented offline fixed policy grid only, worker ceiling 200',
        'simplification': 'documented fixed control, limit 200 and confirmation reserve 20',
        'release_thresholds': None, 'deployment': 'unperformed', 'human_labels': None,
        'independent_attacker': 'unavailable', 'independent_reviewer': 'unavailable/unreviewed'
    }, indent=2) + '\n')
    base = 'eval-runs/skill-exercise/'
    run('01-run-original', ['evaluate.py','run','--candidate','support_agent.py','--suite','development','--out',base+'run-original'])
    run('02-run-conforming', ['evaluate.py','run','--candidate','examples/candidates/improved.py','--suite','development','--out',base+'run-conforming'])
    run('03-compare', ['evaluate.py','compare','--baseline',base+'run-original','--candidate',base+'run-conforming'])
    campaign = base+'hill-climb'
    run('04-start', ['evaluate.py','start','--campaign',campaign,'--max-case-runs','48','--reserve-case-runs','8'])
    run('05-regression', ['evaluate.py','try','--campaign',campaign,'--candidate','examples/candidates/regression.py','--hypothesis','Ticket reuse may fix routing but can wrongly block closed or unrelated tickets; reject any lost passing case.'])
    run('06-improved', ['evaluate.py','try','--campaign',campaign,'--candidate','examples/candidates/improved.py','--hypothesis','Require affirmative authorization, unambiguous account and open target-account duplicate scope.'])
    run('07-finish', ['evaluate.py','finish','--campaign',campaign])
    run('08-status', ['evaluate.py','status','--campaign',campaign])
    run('09-verify', ['evaluate.py','verify','--campaign',campaign])
    run('10-judge', ['-m','judge_calibration.run','--out',base+'judge-calibration'])
    run('11-simplification', ['-m','simplification.run','--out',base+'simplification'])
