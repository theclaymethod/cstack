import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
FROZEN = BASE.parent / 'frozen/fixtures/playground'
sys.dont_write_bytecode = True
sys.path.insert(0, str(FROZEN))

from simplification.protocol import Experiment, UNITS, configuration
from methods.native import evaluate

experiment = Experiment(BASE / 'clean-controls', limit=36, confirmation_reserve=12)
configs = {
    'old-existing': configuration('old-fixture', set(UNITS)),
    'old-reduced': configuration('old-fixture', {'contract', 'legacy-auth', 'duplicate-b'}),
    'new-simplified': configuration('new-fixture', {'contract', 'duplicate-b'}),
}
for label, config in configs.items():
    experiment.measure(label, config)
experiment.freeze({'final-' + label: config for label, config in configs.items()})
for label in experiment.plan:
    experiment.confirm(label)
experiment.finish()
receipt = {
    'native_case_executions': experiment.runs.reserved,
    'runs': {label: {'outcomes': record['outcomes'], 'config': record['config']}
             for label, record in experiment.records.items()},
    'final_comparisons': {
        label: experiment.compare('final-old-existing', label)
        for label in ('final-old-reduced', 'final-new-simplified')
    },
}
evaluate.write_json(BASE / 'clean-controls-receipt.json', receipt)
print(json.dumps(receipt, indent=2))
