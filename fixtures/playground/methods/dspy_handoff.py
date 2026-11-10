"""Optional project-local DSPy examples and native metrics. No LM is configured."""
import copy
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import runpy
import tempfile
from .native import ROOT, evaluate, jsonl, read_rows, write
from .synthetic import case_for, partition


def validate_records(records):
    if not records:
        raise ValueError('Cannot export an empty corpus')
    ids = [row['case']['id'] for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate case identity')
    for row in records:
        case, metadata = row['case'], row['metadata']
        if metadata['label_status'] != 'fixture-contract-derived':
            raise ValueError('Proposed/unreviewed labels cannot become DSPy gold')
        if metadata['source_identity'] != evaluate.identity()['files']:
            raise ValueError('Data was derived under a different native contract/source')
        if not metadata['ancestors']:
            raise ValueError('Construction lineage is required')
        actual_hash = evaluate.json_hash({'request': case['request'], 'state': case['state']})
        if metadata['input_hash'] != actual_hash:
            raise ValueError('Input changed after expectation construction')
        # This demonstration supports exactly the fixture's generated command templates.
        intents = [intent for intent in ['create', 'deny', 'guidance']
                   if case_for('validation', intent)['request']['text'] == case['request']['text']]
        if len(intents) != 1:
            raise ValueError('This local exporter has no contract model for that command')
        expected = case_for(case['id'], intents[0], case['request']['account'],
                            case['request']['accounts'], case['state']['tickets'])['expected']
        if not evaluate.same_json(expected, case['expected']):
            raise ValueError('Expected behavior differs from the structured fixture contract')
    # Apply the native schema/loader rather than inventing another case parser.
    with tempfile.TemporaryDirectory(prefix='dspy-case-validation-') as temp:
        case_file = Path(temp) / 'cases.jsonl'; jsonl(case_file, [r['case'] for r in records])
        evaluate.load_cases('all', case_file)


def export(records_file, directory):
    records = read_rows(records_file); validate_records(records)
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=False)
    splits = partition(records)
    for name, rows in splits.items():
        jsonl(directory / (name + '.jsonl'), rows)
    manifest = {'source_identity': evaluate.identity()['files'],
                'files': {name: evaluate.digest(directory / (name + '.jsonl')) for name in splits},
                'counts': {name: len(rows) for name, rows in splits.items()},
                'input_fields': ['request', 'state'], 'label_kind': 'criterion-only fixture-contract-derived',
                'exposure': 'Both partitions are exposed development data; validation is not a final test',
                'optimizer': 'No model calls or optimization performed', 'provenance': 'Rows retain lineage outside model inputs'}
    write(directory / 'manifest.json', manifest)
    return manifest


def load(directory):
    import dspy
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text())
    if manifest['source_identity'] != evaluate.identity()['files']:
        raise ValueError('DSPy dataset native source changed')
    result = {}
    all_rows = []
    for name in ['train', 'validation']:
        path = directory / (name + '.jsonl')
        if evaluate.digest(path) != manifest['files'][name]:
            raise ValueError('Exported DSPy dataset changed')
        rows = read_rows(path)
        if len(rows) != manifest['counts'][name] or not rows:
            raise ValueError('Incomplete DSPy dataset membership')
        validate_records(rows); all_rows.extend(rows)
        result[name] = [dspy.Example(request=copy.deepcopy(row['case']['request']),
                        state=copy.deepcopy(row['case']['state']), case=copy.deepcopy(row['case']))
                        .with_inputs('request', 'state') for row in rows]
    validate_records(all_rows)
    # Repartition the connected ancestry, catching cross-file source-family leaks.
    canonical = partition(all_rows)
    for name in result:
        if {e.case['id'] for e in result[name]} != {r['case']['id'] for r in canonical[name]}:
            raise ValueError('Construction siblings crossed the frozen development partition')
    return result


def verdict(gold, prediction):
    error = prediction.get('execution_error')
    if error:
        return {'outcome': 'ERROR', 'checks': {}, 'error': str(error)}
    return evaluate.grade(prediction.get('result'), gold.case)


def metric(gold, prediction, trace=None):
    return float(verdict(gold, prediction)['outcome'] == 'PASS')


def gepa_metric(gold, prediction, trace=None, pred_name=None, pred_trace=None, program_trace=None):
    import dspy
    native = verdict(gold, prediction)
    failed = [name for name, passed in native['checks'].items() if not passed]
    feedback = ('Native execution/schema error: ' + str(native['error']) if native['outcome'] == 'ERROR'
                else 'Native required checks failed: ' + ', '.join(failed) if failed
                else 'Native required state, authorization and membership checks passed.')
    output = prediction.get('result')
    if native['outcome'] != 'ERROR':
        feedback += ' ' + json.dumps({'actual_action': output['action'],
            'allowed_actions': gold.case['expected']['allowed_actions'],
            'actual_ticket_delta': len(output['state']['tickets']) - len(gold.case['state']['tickets']),
            'required_ticket_delta': gold.case['expected']['ticket_delta']}, sort_keys=True)
    return dspy.Prediction(score=float(native['outcome'] == 'PASS'), feedback=feedback,
                           outcome=native['outcome'], checks=native['checks'], error=native['error'])


def smoke(directory, output):
    # The caller controls this project-local cache; importing the SDK needs no home writes.
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    os.environ.setdefault('DSPY_CACHEDIR', str(output / 'sdk-cache'))
    import dspy
    splits = load(directory)
    examples = splits['train'] + splits['validation']
    respond = runpy.run_path(str(ROOT / 'examples/candidates/improved.py'))['respond']

    class LocalSupport(dspy.Module):
        def __init__(self):
            super().__init__(); self.invocations = 0

        def forward(self, request, state):
            self.invocations += 1
            return dspy.Prediction(result=respond({'request': request, 'state': state}))

    program = LocalSupport()
    evaluation = dspy.Evaluate(devset=examples, metric=metric, num_threads=1,
                               display_progress=False, display_table=False)(program)
    if evaluation.score != 100.0 or program.invocations != len(examples):
        raise RuntimeError('Actual DSPy Evaluate disagrees with conforming native metric')
    checks = []
    for example in examples:
        if set(example.inputs().keys()) != {'request', 'state'}:
            raise RuntimeError('Expected labels/operator metadata leaked into model inputs')
        predicted = program(**example.inputs())
        feedback = gepa_metric(example, predicted, pred_name='program')
        checks.append({'case_id': example.case['id'], 'metric': metric(example, predicted),
                       'feedback': dict(feedback.items())})
    creation = next(e for e in examples if e.case['expected']['ticket_delta'] == 1)
    false_claim = dspy.Prediction(result={'action': 'create_ticket', 'account': creation.case['expected']['account'],
                          'state': copy.deepcopy(creation.state), 'note': 'Claimed creation'})
    rejected = gepa_metric(creation, false_claim)
    malformed = gepa_metric(creation, dspy.Prediction(result='not a native output'))
    execution_error = gepa_metric(creation, dspy.Prediction(execution_error='fixture timeout'))
    if rejected.outcome != 'FAIL' or rejected.score or malformed.outcome != 'ERROR' or execution_error.outcome != 'ERROR':
        raise RuntimeError('DSPy feedback collapsed invalid execution or accepted a false claim')
    result = {'status': 'passed', 'dspy_version': importlib.metadata.version('dspy'),
              'sdk_source_hashes': {name: evaluate.digest(inspect.getfile(getattr(dspy, name)))
                                    for name in ['Example', 'Prediction', 'Module', 'Evaluate', 'GEPA']},
              'program_sha256': evaluate.digest(ROOT / 'examples/candidates/improved.py'),
              'adapter_sha256': evaluate.digest(Path(__file__)),
              'sdk_program_invocations': program.invocations, 'examples': len(examples),
              'evaluate_percentage': evaluation.score, 'scalar_metric_fraction': 1.0,
              'checks': checks, 'false_claim': dict(rejected.items()), 'malformed': dict(malformed.items()),
              'execution_error': dict(execution_error.items()), 'provider_calls': 0,
              'scope': 'Actual DSPy Example/Module/Evaluate/Prediction and GEPA metric interface compatibility; '
                       'deterministic in-process fixture program, no LM or optimizer compile, no optimization-gain claim'}
    write(output / 'results.json', result)
    return result
