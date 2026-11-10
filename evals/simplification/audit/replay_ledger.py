"""Replay an operator ledger perturbation; never a candidate-access exploit."""
import argparse
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--project', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.project.resolve()))
from simplification.protocol import Experiment, configuration, UNITS

args.out.mkdir(parents=True, exist_ok=False)
experiment = Experiment(args.out / 'experiment', limit=8, confirmation_reserve=0)
clean = experiment.measure('original', configuration('old-fixture', set(UNITS)))
ledger = experiment.runs.directory / 'executions.json'
(args.out / 'ledger-before.json').write_bytes(ledger.read_bytes())
ledger.write_text('{"limit":0,"reserved":0,"actual_completed":0,"calls":[]}\n')
try:
    observed = experiment.checked('original')
except ValueError as error:
    outcome = {'rejected': True, 'reason': str(error)}
else:
    outcome = {'rejected': False, 'result': observed}
actual = len((experiment.runs.directory / 'original/traces.jsonl').read_text().splitlines())
result = {'access': 'operator fault injection; ledger outside candidate payload',
          'clean': clean, 'after_perturbation': outcome, 'actual_native_case_executions': actual,
          'in_memory_reservation': experiment.runs.reserved,
          'durable_ledger_after': json.loads(ledger.read_text())}
(args.out / 'observation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'rejected': outcome['rejected'], 'actual_native_cases': actual,
                  'in_memory_reservation': experiment.runs.reserved}))
