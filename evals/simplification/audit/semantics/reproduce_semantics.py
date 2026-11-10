"""Run bounded independent semantic controls using the unchanged native grader."""
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from methods.native import Runs, evaluate
from simplification.protocol import Experiment, UNITS, candidate_source, configuration, sources


def main():
    out = ROOT / 'eval-runs' / 'semantics-evidence'
    out.mkdir(exist_ok=False)
    evaluate.write_json(out / 'source-identity-before.json', sources())
    full = set(UNITS)
    lean_a = {'contract', 'legacy-auth', 'duplicate-a'}
    lean_b = {'contract', 'legacy-auth', 'duplicate-b'}
    shared = {'contract', 'duplicate-b'}
    designs = {
        'old-full': configuration('old-fixture', full),
        'old-no-a': configuration('old-fixture', full - {'duplicate-a'}),
        'old-no-b': configuration('old-fixture', full - {'duplicate-b'}),
        'old-no-duplicates': configuration('old-fixture', full - {'duplicate-a', 'duplicate-b'}),
        'old-conflict-a': configuration('old-fixture', full - {'conflict-a'}),
        'old-conflict-b': configuration('old-fixture', full - {'conflict-b'}),
        'old-conflict-pair': configuration('old-fixture', full - {'conflict-a', 'conflict-b'}),
        'old-lean-a': configuration('old-fixture', lean_a),
        'old-lean-b': configuration('old-fixture', lean_b),
        'old-shared': configuration('old-fixture', shared),
        'new-full': configuration('new-fixture', full),
        'new-shared': configuration('new-fixture', shared),
    }
    exp = Experiment(out / 'adapter', limit=120, confirmation_reserve=24)
    for label, config in designs.items():
        exp.measure(label, config)
    development = {label: exp.compare('old-full', label) for label in designs}
    finals = ['old-full', 'old-lean-a', 'old-lean-b', 'old-shared', 'new-full', 'new-shared']
    exp.freeze({'final-' + label: designs[label] for label in finals})
    for label in finals:
        exp.confirm('final-' + label)
    exp.finish()
    final = {label: exp.compare('final-old-full', 'final-' + label) for label in finals}
    final['simplification-vs-new-existing'] = exp.compare('final-new-full', 'final-new-shared')
    matrix = {label: exp.checked('final-' + label) for label in ['old-full', 'old-shared', 'new-full', 'new-shared']}
    scores = {label: sum(v == 'PASS' for v in row['outcomes'].values()) / len(row['outcomes']) for label, row in matrix.items()}
    interaction = (scores['new-shared'] - scores['new-full']) - (scores['old-shared'] - scores['old-full'])
    # Alternate observable representations use candidate access only. No labels
    # are embedded, and candidates receive ordinary request/state payloads.
    base = candidate_source(designs['old-lean-b'])
    alternate = base.replace('ticket-{sequence}', 'independent-{sequence}')
    alternate = alternate.replace('reply("guidance", "An open VPN ticket', 'reply("clarify", "An open VPN ticket')
    alternate = alternate.replace('"status": "open", "issue": "vpn"})', '"status": "open", "issue": "vpn", "audit": {"source": "fixture", "enabled": True}})')
    wrong_preservation = base.replace('state = copy.deepcopy(payload["state"])', 'state = copy.deepcopy(payload["state"]); state["operator_added"] = True')
    wrong_collision = base.replace('while f"ticket-{sequence}" in ticket_ids:', 'while False:')
    wrong_schema = base.replace('"note": note}', '"note": note, "extra": True}')
    native = Runs(out / 'native-representation-controls', limit=60)
    results = {}
    all_cases = evaluate.load_cases('all')
    for label, code in {'valid-alternate': alternate, 'wrong-preservation': wrong_preservation,
                        'wrong-id-collision': wrong_collision, 'wrong-output-shape': wrong_schema}.items():
        candidate = out / (label + '.py')
        candidate.write_text(code)
        traces = native.run(label, candidate, all_cases)
        results[label] = {r['id']: r['outcome'] for r in traces}
    # Separate, explicitly synthetic input cases test nested state/record metadata.
    # Canonical source membership and expectations stay untouched.
    enriched = []
    for original in all_cases:
        if original['id'] not in ('dev-explicit', 'dev-duplicate', 'dev-closed', 'conf-preservation'):
            continue
        row = copy.deepcopy(original)
        row['id'] = 'extra-' + row['id']
        row['family'] = 'attacker-semantics-metadata-preservation'
        row['state']['metadata'] = {'flag': True, 'count': 1, 'nested': [None, {'value': 'retain'}]}
        for ticket in row['state']['tickets']:
            ticket['external'] = {'flag': False, 'tags': ['unchanged']}
        enriched.append(row)
    for label, code in {'metadata-control': base, 'metadata-valid-alternate': alternate,
                        'wrong-json-type': base.replace('state = copy.deepcopy(payload["state"])',
                            'state = copy.deepcopy(payload["state"]); state["metadata"]["flag"] = 1')}.items():
        candidate = out / (label + '.py')
        candidate.write_text(code)
        traces = native.run(label, candidate, enriched)
        results[label] = {r['id']: r['outcome'] for r in traces}
    after = sources()
    evaluate.write_json(out / 'source-identity-after.json', after)
    assert after == exp.contract['sources']
    expected_valid = ['old-full', 'old-no-a', 'old-no-b', 'old-conflict-pair', 'old-lean-a', 'old-lean-b', 'new-full', 'new-shared']
    assert all(development[label]['admissible'] for label in expected_valid)
    assert all(not development[label]['admissible'] for label in ['old-no-duplicates', 'old-conflict-a', 'old-conflict-b', 'old-shared'])
    assert all(v == 'PASS' for v in results['valid-alternate'].values())
    assert all(v == 'PASS' for v in results['metadata-control'].values())
    assert all(v == 'PASS' for v in results['metadata-valid-alternate'].values())
    assert all(v == 'FAIL' for v in results['wrong-preservation'].values())
    assert all(v == 'ERROR' for v in results['wrong-output-shape'].values())
    assert results['wrong-id-collision']['dev-closed'] == 'FAIL'
    assert results['wrong-id-collision']['conf-preservation'] == 'FAIL'
    assert all(v == 'FAIL' for v in results['wrong-json-type'].values())
    total = exp.runs.reserved + native.reserved
    assert total == 180
    evaluate.write_json(out / 'results.json', {
        'status': 'bounded audit; no confirmed discrepancy',
        'access': 'public adapter APIs plus standalone candidate variants; no object/source mutation or operator fault injection',
        'native_case_executions': total, 'adapter_case_executions': exp.runs.reserved,
        'representation_case_executions': native.reserved,
        'all_attempts': len(exp.records) + len(native.calls),
        'development_comparisons': development, 'final_comparisons': final,
        'matrix_scores': scores, 'interaction': interaction,
        'representation_outcomes': results,
        'source_hashes_unchanged': True, 'provider_calls': 0, 'network_calls': 0,
        'limits': ['Finite readable synthetic cases; no human labels or population claim.',
                   'Cases with metadata are separate attacker-authored probes.',
                   'Fixed model stand-ins, not real model migrations.',
                   'No adversarial host containment or resume guarantee tested.']})
    print(json.dumps({'evidence': str(out), 'native_cases': total, 'status': 'no confirmed discrepancy'}, indent=2))


if __name__ == '__main__':
    main()
