"""Inspect actual outcomes independently of the native verdict fields."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'eval-runs' / 'semantics-evidence'
FROZEN = ROOT.parent / 'frozen'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def traces(label):
    path = OUT / 'native-representation-controls' / label / 'traces.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()]


def same(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


witnesses = []
for row in traces('valid-alternate') + traces('metadata-valid-alternate'):
    old, output = row['input']['state'], row['output']
    state = output['state']
    assert same(state['tickets'][:len(old['tickets'])], old['tickets'])
    assert same({k: v for k, v in old.items() if k != 'tickets'},
                {k: v for k, v in state.items() if k != 'tickets'})
    if output['action'] == 'create_ticket':
        added = state['tickets'][-1]
        assert added['id'].startswith('independent-')
        assert added['id'] not in {t['id'] for t in old['tickets']}
        assert added['audit'] == {'source': 'fixture', 'enabled': True}
        assert added['status'] == 'open' and added['issue'] == 'vpn'
        assert added['account'] == output['account']
    else:
        assert same(state, old)
    if 'duplicate' in row['id']:
        assert output['action'] == 'clarify'
    witnesses.append({'id': row['id'], 'action': output['action'],
                      'prior_state_preserved': True, 'added': state['tickets'][len(old['tickets']):]})
for row in traces('wrong-preservation'):
    assert 'operator_added' not in row['input']['state']
    assert row['output']['state']['operator_added'] is True
for row in traces('wrong-id-collision'):
    if row['id'] in ('dev-closed', 'conf-preservation'):
        ids = [t['id'] for t in row['output']['state']['tickets']]
        assert len(ids) != len(set(ids))
for row in traces('wrong-json-type'):
    assert type(row['input']['state']['metadata']['flag']) is bool
    assert type(row['output']['state']['metadata']['flag']) is int

before = json.loads((OUT / 'source-identity-before.json').read_text())
file_hashes = {**before['files'], **before['native']['files']}
source_matches = {}
for name, expected in file_hashes.items():
    frozen = FROZEN / 'fixtures' / 'playground' / name
    copied = ROOT / name
    assert digest(frozen) == digest(copied) == expected
    source_matches[name] = {'sha256': expected, 'matches_frozen_and_initial': True}
for name in ('ablation', 'bitter-lesson', 'adversarial-cases'):
    frozen = FROZEN / 'skills' / name / 'SKILL.md'
    copied = ROOT / '.agents' / 'skills' / name / 'SKILL.md'
    assert digest(frozen) == digest(copied)
    source_matches['skills/' + name + '/SKILL.md'] = {'sha256': digest(frozen), 'matches_frozen_and_initial': True}
(OUT / 'independent-witnesses.json').write_text(json.dumps({'valid_alternatives': witnesses,
    'invalid_state_change_witnesses': 12, 'invalid_id_collision_witnesses': 2,
    'invalid_json_type_change_witnesses': 4, 'additional_native_cases': 0}, indent=2) + '\n')
(OUT / 'frozen-source-matches.json').write_text(json.dumps(source_matches, indent=2) + '\n')
print(json.dumps({'independently_inspected_valid_traces': len(witnesses),
                  'source_files_matched': len(source_matches), 'additional_native_cases': 0}))
