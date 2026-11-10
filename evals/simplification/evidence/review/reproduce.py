"""Reproduce a frozen-plan mutation against a chosen protocol revision."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--project', type=Path, required=True)
parser.add_argument('--protocol', type=Path)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.project.resolve()))
if args.protocol:
    spec = importlib.util.spec_from_file_location('protocol_revision', args.protocol)
    protocol = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(protocol)
else:
    from simplification import protocol
experiment = protocol.Experiment(args.out, limit=4, confirmation_reserve=4)
declared = protocol.configuration('old-fixture', set(protocol.UNITS))
experiment.freeze({'final': declared})
experiment.plan['final'] = protocol.configuration('new-fixture', {'contract', 'duplicate-b'})
try:
    actual = experiment.confirm('final')['config']
except ValueError as error:
    result = {'declared': declared, 'guard_rejected_mutation': True, 'error': str(error),
              'native_case_executions': experiment.runs.reserved}
else:
    result = {'declared': declared, 'executed': actual, 'guard_rejected_mutation': False,
              'native_case_executions': experiment.runs.reserved}
(args.out / 'reproduction.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
