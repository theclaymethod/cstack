"""Independent skill-led offline campaign. No demo or test solution import."""
import argparse
import difflib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from simplification.protocol import Experiment, UNITS, configuration, render, sources
from methods.native import Runs, evaluate


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    full = set(UNITS)
    no_plan = full - {'plan', 'plan-detail'}
    no_example = no_plan - {'example'}
    one_dup = no_example - {'duplicate-a'}
    old_min = one_dup - {'conflict-a', 'conflict-b'}
    new_min = old_min - {'legacy-auth'}
    final_configs = {
        'confirm-old-full': configuration('old-fixture', full),
        'confirm-old-simple': configuration('old-fixture', old_min),
        'confirm-new-full': configuration('new-fixture', full),
        'confirm-new-old-simple': configuration('new-fixture', old_min),
        'confirm-old-migration-simple': configuration('old-fixture', new_min),
        'confirm-new-migration-simple': configuration('new-fixture', new_min),
    }
    owner = {
        'mutable': 'Only rendered prompt unit membership and explicitly simulated model identity; standalone snapshots',
        'protected': ['contract and embedded unchanged rubric', 'dependency plan-detail requires plan'],
        'frozen': sources(), 'unit_catalog': UNITS,
        'objective': ['minimize retained units', 'minimize rendered UTF-8 bytes'],
        'quality': {'original': 'old-full', 'metric': 'native fraction passing all checks',
                    'maximum_loss': 0, 'allowed_observed_pass_regressions': 0,
                    'errors_unknown': 'never admissible; keep in denominator',
                    'slices': 'every individual case/family'},
        'trial': {'deterministic': True, 'repeats': 1, 'reset': 'fresh native subprocess per case'},
        'exposure': 'All synthetic cases explicitly read; final execution is reserved workflow confirmation only',
        'budget': {'total_native_case_executions': 160, 'confirmation_reserve': 24,
                   'planned_development': 112, 'schema_control': 1, 'planned_total': 137},
        'confirmation_plan': final_configs,
        'stop': 'Execute the declared bounded deletion probes and six frozen confirmation cells; no production edits',
        'promotion': 'Local exposed-fixture selection only, under exact zero-loss quality gates; no real model conclusion',
        'costs': 'No actual provider/model/network/paid calls or dependencies; token costs unavailable',
        'comparison': 'Compare both simplified designs identically on both models, and to both existing-design controls',
        'rationale': 'Known synthetic cue design from project adapter; no production workaround history available',
        'driver_sha256': evaluate.digest(Path(__file__)),
    }
    write(out / 'owner-contract.json', owner)
    # Same sole native execution/grading path, one deliberately malformed output.
    malformed = out / 'malformed.py'
    malformed.write_text('print("{}")\n')
    controls = Runs(out / 'schema-control', limit=1)
    malformed_trace = controls.run('malformed', malformed, evaluate.load_cases('development')[:1])
    assert [r['outcome'] for r in malformed_trace] == ['ERROR']
    ex = Experiment(out / 'campaign', limit=159, confirmation_reserve=24)
    proposals = [
        ('old-full', 'old-fixture', full, None, 'Measure actual original full design'),
        ('old-no-plan', 'old-fixture', no_plan, 'old-full', 'Remove plan and dependent together'),
        ('old-no-example', 'old-fixture', no_example, 'old-no-plan', 'Contract supplies guidance semantics without example'),
        ('old-one-duplicate', 'old-fixture', one_dup, 'old-no-example', 'Retain one of two duplicate cues'),
        ('old-no-conflict-a', 'old-fixture', one_dup - {'conflict-a'}, 'old-one-duplicate', 'Measure first conflict cue deletion conditionally'),
        ('old-no-conflict-b', 'old-fixture', one_dup - {'conflict-b'}, 'old-one-duplicate', 'Measure second conflict cue deletion from same parent'),
        ('old-simple', 'old-fixture', old_min, 'old-one-duplicate', 'Delete interacting conflict pair as a new combined candidate'),
        ('old-no-legacy', 'old-fixture', new_min, 'old-simple', 'Probe whether authorization workaround remains necessary'),
        ('old-no-duplicate', 'old-fixture', old_min - {'duplicate-b'}, 'old-simple', 'Probe whether remaining duplicate cue can go'),
        ('old-alternate-duplicate', 'old-fixture', (old_min - {'duplicate-b'}) | {'duplicate-a'}, 'old-simple', 'Compare equal-unit alternative by actual rendered bytes'),
        ('new-full', 'new-fixture', full, 'old-full', 'Hold full design fixed for model comparison'),
        ('new-old-simple', 'new-fixture', old_min, 'old-simple', 'Use identical old reduced design on new fixture'),
        ('new-migration-simple', 'new-fixture', new_min, 'old-no-legacy', 'Use identical legacy-free design on new fixture'),
        ('new-contract-only', 'new-fixture', {'contract'}, 'new-migration-simple', 'Probe removal of final duplicate steering'),
    ]
    metadata = []
    records = {}
    for label, model, units, parent, hypothesis in proposals:
        config = configuration(model, units)
        parent_units = records[parent]['config']['retained'] if parent else sorted(units)
        entry = {'label': label, 'parent': parent, 'hypothesis': hypothesis,
                 'retained': config['retained'], 'removed_from_parent': sorted(set(parent_units) - set(units)),
                 'added_to_parent': sorted(set(units) - set(parent_units)), 'model': model}
        prompt = render(config)
        (out / (label + '.prompt.txt')).write_text(prompt)
        original = render(configuration('old-fixture', full))
        (out / (label + '.diff')).write_text(''.join(difflib.unified_diff(
            original.splitlines(True), prompt.splitlines(True), fromfile='original-full', tofile=label)))
        metadata.append(entry)
        write(out / 'proposals.json', metadata)
        records[label] = ex.measure(label, config)
        entry['quality_vs_original'] = ex.compare('old-full', label)
        write(out / 'proposals.json', metadata)
    # Native required schema and protocol configuration checks without new model/case attempts.
    try:
        configuration('old-fixture', full - {'plan'})
    except ValueError as err:
        write(out / 'invalid-structure.json', {'status': 'invalid intervention; not executed', 'error': str(err)})
    else:
        raise AssertionError('Dependency validation failed')
    ex.freeze(final_configs)
    for label in final_configs:
        records[label] = ex.confirm(label)
    comparisons = {}
    pairs = [
        ('old-simplification', 'confirm-old-full', 'confirm-old-simple'),
        ('model-full', 'confirm-old-full', 'confirm-new-full'),
        ('new-same-simplification', 'confirm-new-full', 'confirm-new-old-simple'),
        ('new-same-vs-original', 'confirm-old-full', 'confirm-new-old-simple'),
        ('old-migration-simplification', 'confirm-old-full', 'confirm-old-migration-simple'),
        ('new-migration-simplification', 'confirm-new-full', 'confirm-new-migration-simple'),
        ('migration-bundle-vs-original', 'confirm-old-full', 'confirm-new-migration-simple'),
    ]
    for name, left, right in pairs:
        comparisons[name] = ex.compare(left, right)
    ex.finish()
    counted = controls.reserved + ex.runs.reserved
    assert counted == 137 and ex.reserve == 0
    assert comparisons['old-simplification']['admissible']
    assert comparisons['new-migration-simplification']['admissible']
    assert comparisons['migration-bundle-vs-original']['admissible']
    assert not comparisons['old-migration-simplification']['admissible']
    results = {
        'scope': owner['exposure'], 'native_case_executions': counted,
        'development_case_executions': 112, 'confirmation_case_executions': 24,
        'schema_control_case_executions': 1, 'native_run_invocations': len(ex.runs.calls) + len(controls.calls),
        'actual_completed': sum(c['executed'] for c in ex.runs.calls + controls.calls),
        'provider_calls': 0, 'network_calls': 0, 'paid_calls': 0,
        'records': records, 'comparisons': comparisons,
        'selected_old': 'old-simple', 'selected_migration': 'new-migration-simple',
        'minimality': 'Smallest confirmed designs found in this declared bounded sweep; no global minimum claim',
        'missing': ['Real model versions and inference settings', 'Real token/cost/latency effects', 'Production coverage or unseen generalization'],
        'native_wall_seconds': sum(r['native_wall_seconds'] for r in records.values()),
    }
    write(out / 'result.json', results)
    lines = ['# Independent forward-use report', '',
             'Used Ablation and Bitter Lesson without demo/test solutions. Sole grader: evaluate.py through simplification.protocol.', '',
             'All cases are synthetic and exposed. This confirms local fixture outcomes and experiment mechanics, not real model performance.', '',
             '| Run | Model | Units | UTF-8 bytes | PASS / cases |',
             '| --- | --- | ---: | ---: | ---: |']
    for label, record in records.items():
        vals = list(record['outcomes'].values())
        lines.append(f"| {label} | {record['config']['model']} | {record['unit_count']} | {record['prompt_utf8_bytes']} | {vals.count('PASS')} / {len(vals)} |")
    lines += ['', 'The old selected design retains contract, legacy-auth, duplicate-b. The migration design retains contract and duplicate-b.',
              'Original-relative zero loss and zero pass regressions hold for both selected bundles on development and confirmation.',
              'The identical legacy-free design fails old-fixture but passes new-fixture, exposing an actual fixture model/design interaction.',
              'Single conflict removals fail, while deleting both succeeds. Removing both duplicate cues fails; at least one remains useful.',
              'The alternate duplicate-a design is also feasible; duplicate-b wins the UTF-8 byte tie-break.', '',
              f'Accounting: {counted}/160 native case executions; 112 development + 24 reserved confirmation + 1 malformed-output control. 21 native run invocations. No actual provider, network or paid calls.', '',
              'No observed skill-guidance error prevented execution. The guidance correctly disallows interpreting offline model names as real migration evidence. One ambiguity: Hill Climb says "strict improvement" in generic prose while the owner contract here minimizes burden at equal native quality; Ablation\'s burden objective resolves that for this campaign. The native spec\'s task-score promotion rule also targets ordinary bug fixing; this prompt-ablation campaign explicitly uses the authorized burden objective and original-relative quality gate.',
              'The adapter is deliberately one-shot and has no resumable state loader; this run completed, so recovery advice was not exercised. No operational cost reduction is claimed from prompt-byte changes.', '',
              'Reproduce from this workspace (fresh output path required):',
              '```sh', 'python3 eval-runs/forward_driver.py --out eval-runs/forward-repeat', '```', '',
              'Artifacts: owner-contract.json, proposals.json, result.json, rendered *.prompt.txt and *.diff; campaign/candidates contains executable snapshots and campaign/native contains native manifests, summaries, traces, outputs, and ledger. schema-control preserves the malformed native run.']
    (out / 'report.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'native_case_executions': counted, 'report': str(out / 'report.md'),
                      'old': records['old-simple']['prompt_utf8_bytes'],
                      'migration': records['new-migration-simple']['prompt_utf8_bytes']}, indent=2))

if __name__ == '__main__':
    main()
