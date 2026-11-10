"""Run bounded project-local method experiments and export a DSPy-ready development corpus."""
import argparse
import json
from pathlib import Path
from . import synthetic, faults, dspy_handoff
from .native import ROOT, evaluate, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--dspy-check', action='store_true', help='Require the optional pinned SDK; no LM calls')
    args = parser.parse_args()
    out = args.out.resolve()
    if out == ROOT or ROOT in out.parents:
        # Generated trials belong in eval-runs inside a materialized workspace. Canonical
        # fixture output is rejected; generated workspaces carry a factory source marker.
        if not (ROOT / '.cstack-source.json').exists() or (ROOT / 'eval-runs') not in out.parents:
            raise SystemExit('Use a materialized workspace eval-runs directory or an external output path')
    out.mkdir(parents=True, exist_ok=False)
    before = {p: evaluate.digest(ROOT / p) for p in evaluate.FROZEN_FILES}
    generated = synthetic.run(out / 'synthetic')
    perturbations = faults.run(out / 'faults')
    dataset = dspy_handoff.export(out / 'synthetic/records.jsonl', out / 'dspy-data')
    sdk = dspy_handoff.smoke(out / 'dspy-data', out / 'dspy-check') if args.dspy_check else {
        'status': 'not-run', 'reason': 'Optional SDK check requires --dspy-check and methods/requirements-dspy.txt'}
    after = {p: evaluate.digest(ROOT / p) for p in evaluate.FROZEN_FILES}
    if before != after:
        raise RuntimeError('Native evaluation contract changed')
    result = {'status': 'passed', 'scope': 'Local synthetic methods; not a skill/model optimization effectiveness measurement',
              'source_before': before, 'source_after': after,
              'synthetic': {k: generated[k] for k in ['actual_native_executions', 'selected_case_ids', 'additional_mechanism', 'comparison']},
              'faults': {k: perturbations[k] for k in ['actual_native_executions', 'process_interruptions', 'candidate_timeouts']},
              'dataset': dataset, 'dspy': sdk,
              'actual_native_executions': generated['actual_native_executions'] + perturbations['actual_native_executions'],
              'deferred': {'Hypothesis': 'Explicit bounded enumeration suffices for this initial sequence vocabulary',
                           'Z3': 'No constraint boundary requiring a solver in this tiny fixture',
                           'Toxiproxy': 'No network dependency adapter exists',
                           'semantic_judges': 'Native observable state is directly checkable',
                           'live_DSPy_optimization': 'Model, mutable DSPy target and budget remain unspecified'},
              'provider_calls': 0}
    write(out / 'results.json', result)
    print(json.dumps({k: result[k] for k in ['status', 'actual_native_executions', 'synthetic', 'faults', 'deferred']}, indent=2))


if __name__ == '__main__':
    main()
