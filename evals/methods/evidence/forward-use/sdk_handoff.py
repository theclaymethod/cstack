"""Project-local DSPy boundary check; deterministic program, no models."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import dspy

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import evaluate as native

module_spec = importlib.util.spec_from_file_location('local_support', ROOT / 'examples/candidates/improved.py')
candidate = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(candidate)

cases = native.load_cases('development', OUT / 'cases.jsonl')
source_identity = native.identity()
examples = [dspy.Example(payload={'request': case['request'], 'state': case['state']},
                         criteria=case['expected']).with_inputs('payload') for case in cases]
assert all(set(example.inputs()) == {'payload'} for example in examples)
receipts = []

def metric(example, prediction, trace=None):
    result = native.grade(prediction.result, {**example.payload, 'expected': example.criteria})
    receipts.append(result)
    return float(result['outcome'] == 'PASS')

class LocalProgram(dspy.Module):
    def forward(self, payload):
        return dspy.Prediction(result=candidate.respond(copy.deepcopy(payload)))

result = dspy.Evaluate(devset=examples, metric=metric, num_threads=1, display_progress=False,
                       display_table=False)(LocalProgram())
assert result.score == 100.0 and len(receipts) == 6

# Native metric compatibility checks do not invoke the program again.
valid = copy.deepcopy(result.results[1][1].result)
valid['state']['tickets'][-1]['id'] = 'alternative-valid-id'
assert metric(examples[1], dspy.Prediction(result=valid)) == 1
wrong = copy.deepcopy(valid)
wrong['state']['tickets'][-1]['account'] = 'not-available'
assert metric(examples[1], dspy.Prediction(result=wrong)) == 0
assert receipts[-1]['outcome'] == 'FAIL'
assert metric(examples[1], dspy.Prediction(result={'note': 'bad shape'})) == 0
assert receipts[-1]['outcome'] == 'ERROR'

(OUT / 'dspy-examples.jsonl').write_text(''.join(json.dumps(dict(example), sort_keys=True) + '\n' for example in examples))
(OUT / 'dspy-metadata.json').write_text(json.dumps({
    'dspy_version': dspy.__version__, 'native_identity': source_identity,
    'cases_sha256': native.digest(OUT / 'cases.jsonl'),
    'provenance_sha256': native.digest(OUT / 'provenance.json'),
    'input_fields': ['payload'], 'excluded_input_fields': ['criteria', 'source', 'approval', 'family', 'operator_receipts'],
    'partition': 'all adaptive-development; connected construction ancestry',
    'authority': 'explicit synthetic contract; no human labels',
    'excluded': ['nonzero-treatment is execution reliability evidence; not model training label'],
    'resume_policy': 'Reject changed native_identity, cases hash, provenance hash, or input content hashes in provenance.'
}, indent=2, sort_keys=True) + '\n')
(OUT / 'dspy-check.json').write_text(json.dumps({
    'version': dspy.__version__, 'evaluate_score': result.score,
    'program_calls': 6, 'metric_calls': 9, 'provider_calls': 0,
    'native_subprocess_case_executions': 13, 'total_program_case_executions': 19,
    'metric_receipts': receipts,
    'checks': {'labels_excluded_from_inputs': True, 'alternate_valid_id': 'PASS',
               'wrong_account': 'FAIL', 'bad_shape': 'ERROR'},
    'limits': ['No GEPA API or optimizer compatibility tested', 'No prompt improvement or model performance claim',
               'ERROR handling checked in metric; SDK program exceptions were not injected']
}, indent=2, sort_keys=True) + '\n')
assert native.identity() == source_identity
print(json.dumps({'dspy': dspy.__version__, 'program_calls': 6, 'metric_calls': 9, 'score': result.score}))
