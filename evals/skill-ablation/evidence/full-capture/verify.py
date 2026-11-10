"""Verify actual saved capture and native receipts without re-executing cases."""
import hashlib
import json
import pathlib

out = pathlib.Path(__file__).resolve().parent
root = out.parents[1]

def load(path):
    return json.loads(path.read_text())

def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]

for path in out.rglob('*.jsonl'):
    rows(path)
for path in out.rglob('*.json'):
    load(path)
assert (out/'source.md').read_bytes() == (root/'exercises/fixtures/review-session.md').read_bytes()
assert not load(out/'session-state.json')['expert_mode_active']
native = []
for directory, expected in [('native-baseline', 'FAIL'), ('native-regenerated', 'PASS')]:
    path = out/directory
    summary, manifest, traces = load(path/'summary.json'), load(path/'manifest.json'), rows(path/'traces.jsonl')
    assert summary['executed_count'] == len(traces) == 1
    assert traces[0]['id'] == 'dev-howto' and traces[0]['outcome'] == expected
    assert hashlib.sha256((path/'candidate.py').read_bytes()).hexdigest() == manifest['candidate_hash']
    native.append({'directory': directory, 'case': 'dev-howto', 'executed': 1,
                   'outcome': expected, 'candidate_sha256': manifest['candidate_hash'],
                   'expert_judgment': None, 'source_judgment_association': 'unproven'})
assert rows(out/'native-baseline/traces.jsonl')[0]['input'] == rows(out/'native-regenerated/traces.jsonl')[0]['input']
assert (root/'support_agent.py').read_bytes() == (out/'native-baseline/candidate.py').read_bytes()
for checkpoint in ['first', 'merge1', 'merge2']:
    path = out/'checkpoints'/checkpoint
    for file, digest in load(path/'hashes.json').items():
        assert hashlib.sha256((path/file).read_bytes()).hexdigest() == digest
    seed = next(x for x in rows(path/'reviews.jsonl') if x['record_id']=='prior-local-annotation')
    first_seed = next(x for x in rows(out/'checkpoints/first/reviews.jsonl') if x['record_id']=='prior-local-annotation')
    assert seed == first_seed
for file in ['reviews.jsonl', 'rubric.jsonl', 'observations.jsonl', 'exclusions.jsonl']:
    assert (out/'checkpoints/merge1'/file).read_bytes() == (out/'checkpoints/merge2'/file).read_bytes()
assert all(value == 0 for value in load(out/'merge2-merge-receipt.json')['added'].values())
reviews = rows(out/'reviews.jsonl')
assert next(x for x in reviews if x['record_id']=='review-howto-scope-amendment')['amends']=='review-howto-v1'
assert next(x for x in rows(out/'rubric.jsonl') if x['criterion_id']=='urgency-unresolved')['passing_answer'] is None
inventory = {'native_case_executions': sum(x['executed'] for x in native),
             'budget': 48, 'receipts': native, 'provider_calls': 0,
             'confirmation_case_executions': 0, 'verification': 'passed; no native reruns'}
(out/'usage.json').write_text(json.dumps(inventory, indent=2)+'\n')
print(json.dumps(inventory, indent=2))
