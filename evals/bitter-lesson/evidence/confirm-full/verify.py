"""Read-only consistency checks; no candidate subprocess executions."""
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT))
from methods.native import evaluate


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    usage = read(OUT / 'usage.json')
    ledgers = [read(OUT / p) for p in ['controls/native/executions.json', 'prompt-experiment/native/executions.json']]
    total = 0
    run_count = 0
    for ledger, subfolder in zip(ledgers, ['controls/native', 'prompt-experiment/native']):
        completed = 0
        for call in ledger['calls']:
            assert call['status'] == 'complete'
            run = OUT / subfolder / call['label']
            manifest, summary = evaluate.checked_run(run)
            assert summary['complete']
            assert call['reserved'] == call['executed'] == summary['executed_count'] == summary['selected_count']
            assert summary['counts'] == call['counts']
            traces = [json.loads(line) for line in (run / 'traces.jsonl').read_text().splitlines()]
            assert [r['id'] for r in traces] == manifest['case_ids']
            assert all(r['exit_code'] == 0 for r in traces)
            completed += summary['executed_count']
            run_count += 1
        assert ledger['reserved'] == ledger['actual_completed'] == completed <= ledger['limit']
        total += completed
    assert total == usage['actual_native_case_attempts'] == usage['reserved'] == 80 <= 120
    fixed = read(OUT / 'source/frozen-inputs.json')
    assert all(sha(ROOT / name) == expected == sha(OUT / 'source/snapshot' / name) for name, expected in fixed.items())
    state = read(OUT / 'prompt-experiment/state.json')
    assert state['status'] == 'finished'
    assert set(state['plan']) == {'confirm-full', 'confirm-selected'}
    for label, record in state['records'].items():
        assert record['status'] == 'complete'
        assert all(sha(OUT / 'prompt-experiment/native' / label / name) == expected for name, expected in record['evidence'].items())
    assert sha(OUT / 'selected-candidate.py') == state['records']['one-duplicate']['candidate_sha256']
    print(json.dumps({'checked_native_runs': run_count, 'checked_native_case_attempts': total,
                      'canonical_sources_unchanged': True, 'completed_frozen_plan': True,
                      'additional_native_case_attempts': 0}, indent=2))


if __name__ == '__main__':
    main()
