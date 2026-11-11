"""Known synthetic controls, not an automatic optimizer or production migration."""
import difflib
from pathlib import Path

from methods.native import evaluate
from .protocol import Experiment, UNITS, configuration


def score(record):
    values = list(record['outcomes'].values())
    return sum(value == 'PASS' for value in values) / len(values)


def run(directory):
    experiment = Experiment(directory, limit=200, confirmation_reserve=20)
    full = set(UNITS)
    baseline = configuration('old-fixture', full)
    experiment.measure('original', baseline)
    diagnostics, individually_removable = {}, set()
    for unit in sorted(full):
        try:
            config = configuration('old-fixture', full - {unit})
        except ValueError as error:
            diagnostics[unit] = {'status': 'invalid-before-execution', 'reason': str(error)}
            continue
        label = 'leave-out-' + unit
        record = experiment.measure(label, config)
        comparison = experiment.compare('original', label)
        diagnostics[unit] = {'status': 'measured', 'run': label, 'score': score(record), **comparison}
        if comparison['admissible']:
            individually_removable.add(unit)
    union = configuration('old-fixture', full - individually_removable)
    experiment.measure('naive-union', union)
    naive_comparison = experiment.compare('original', 'naive-union')
    if naive_comparison['admissible']:
        raise AssertionError('Fixture did not expose the declared duplicate-removal interaction')

    current, current_label = full, 'original'
    history = []
    groups = [('drop-noise', {'plan', 'plan-detail', 'example'}),
              ('drop-duplicate-a', {'duplicate-a'}), ('drop-duplicate-b', {'duplicate-b'}),
              ('drop-conflict-a', {'conflict-a'}), ('drop-conflict-b', {'conflict-b'}),
              ('drop-conflict-pair', {'conflict-a', 'conflict-b'})]
    for label, removals in groups:
        config = configuration('old-fixture', current - removals)
        result = experiment.measure(label, config)
        comparison = experiment.compare('original', label)
        accepted = comparison['admissible'] and result['unit_count'] < len(current)
        history.append({'run': label, 'parent': current_label, 'removed': sorted(removals),
                        'accepted': accepted, **comparison})
        if accepted:
            current, current_label = set(config['retained']), label
    selected_old = configuration('old-fixture', current)
    if current != {'contract', 'legacy-auth', 'duplicate-b'}:
        raise AssertionError('Declared removal controls changed; inspect per-case results')

    # This same simplified design is used for both model rows of the matrix.
    simplified = current - {'legacy-auth'}
    old_simple = configuration('old-fixture', simplified)
    new_full = configuration('new-fixture', full)
    new_simple = configuration('new-fixture', simplified)
    experiment.measure('old-simplified', old_simple)
    experiment.measure('new-existing', new_full)
    experiment.measure('new-simplified', new_simple)
    if (experiment.compare('original', 'old-simplified')['admissible']
            or not experiment.compare('new-existing', 'new-simplified')['admissible']
            or not experiment.compare('original', 'new-simplified')['admissible']):
        raise AssertionError('Synthetic model-by-design comparison did not show its declared controls')

    plan = {'final-old-existing': baseline, 'final-old-reduced': selected_old,
            'final-old-simplified': old_simple, 'final-new-existing': new_full,
            'final-new-simplified': new_simple}
    experiment.freeze(plan)
    for label in plan:
        experiment.confirm(label)
    experiment.finish()
    final_ablation = experiment.compare('final-old-existing', 'final-old-reduced')
    final_release = experiment.compare('final-old-existing', 'final-new-simplified')
    final_simplification = experiment.compare('final-new-existing', 'final-new-simplified')
    if not all(row['admissible'] for row in (final_ablation, final_release, final_simplification)):
        raise AssertionError('Finite confirmation controls did not preserve declared quality')
    before = experiment.checked('final-old-existing')
    after = experiment.checked('final-new-simplified')
    matrix_names = {'old-existing': 'final-old-existing', 'old-simplified': 'final-old-simplified',
                    'new-existing': 'final-new-existing', 'new-simplified': 'final-new-simplified'}
    matrix = {key: {'run': label, 'score': score(experiment.checked(label)),
                   'config': experiment.checked(label)['config']} for key, label in matrix_names.items()}
    a, b, c, d = [matrix[key]['score'] for key in matrix_names]
    blocked = {}
    for name, operation in {
        'refitting-after-final': lambda: experiment.measure('late-edit', new_simple),
        'unplanned-final': lambda: experiment.confirm('unplanned'),
        'duplicate-final': lambda: experiment.confirm('final-new-simplified'),
    }.items():
        try:
            operation()
        except ValueError:
            blocked[name] = True
        else:
            raise AssertionError('Closed final experiment accepted more work')
    original_path = experiment.runs.directory / 'final-old-existing' / 'candidate.py'
    chosen_path = experiment.runs.directory / 'final-new-simplified' / 'candidate.py'
    artifact = Path(directory) / 'selected-offline-fixture.py'
    artifact.write_bytes(chosen_path.read_bytes())
    (Path(directory) / 'selected.diff').write_text(''.join(difflib.unified_diff(
        original_path.read_text().splitlines(True), chosen_path.read_text().splitlines(True),
        fromfile='original-offline-fixture.py', tofile='selected-offline-fixture.py')))
    result = {'status': 'passed', 'policy': {'quality_loss': 0, 'observed_pass_regressions': 0,
        'objective': 'fewer retained units and fewer rendered prompt UTF-8 bytes'},
        'diagnostics': diagnostics, 'naive_union': naive_comparison, 'reduction_history': history,
        'old_model_reduction': {'config': selected_old, 'confirmation': final_ablation},
        'migration': {'matrix': matrix, 'model_effect_existing_design': c - a,
            'simplification_effect_old': b - a, 'simplification_effect_new': d - c,
            'interaction': (d - c) - (b - a), 'release_vs_original': final_release,
            'simplification_vs_new_existing': final_simplification},
        'burden': {'original_units': before['unit_count'], 'selected_units': after['unit_count'],
            'original_prompt_utf8_bytes': before['prompt_utf8_bytes'],
            'selected_prompt_utf8_bytes': after['prompt_utf8_bytes'],
            'token_count': None, 'model_cost_or_latency_savings': 'not measured'},
        'selected_artifact': artifact.name, 'selected_sha256': evaluate.digest(artifact),
        'native_case_executions': experiment.runs.reserved, 'limit': experiment.runs.limit,
        'confirmation_case_executions': sum(len(row['outcomes']) for row in experiment.records.values()
                                            if row['suite'] == 'confirmation'),
        'closed_controls': blocked, 'provider_calls': 0, 'paid_calls': 0,
        'minimality': 'Smallest feasible candidate in this scripted search; no minimality sweep or global claim',
        'promotion': 'Offline fixture artifact only; no deployable production prompt or real model validation',
        'source_identity': experiment.contract['sources'],
        'limits': ['All task cases and expected outcomes are synthetic and readable.',
                   'Model capability and prompt interactions are explicitly programmed stand-ins.',
                   'No model inference, human labels, statistical non-inferiority or production rollout tested.',
                   'One-shot protocol; no resume loader or adversarial host/filesystem isolation.']}
    evaluate.write_json(Path(directory) / 'results.json', result)
    return result
