"""Verify retained evidence without executing additional native cases."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from methods.native import evaluate

OUT = Path(__file__).resolve().parent
manifest = evaluate.read_json(OUT/'manifest.json')
for name, digest in manifest['files'].items():
    assert evaluate.digest(OUT/name) == digest, name
verified_runs = []
for p in sorted((OUT/'authoring-native').glob('*/manifest.json')) + sorted((OUT/'simplification/native').glob('*/manifest.json')):
    evaluate.checked_run(p.parent)
    verified_runs.append(str(p.parent.relative_to(OUT)))
ledgers = [evaluate.read_json(OUT/p) for p in ['authoring-native/executions.json','simplification/native/executions.json']]
actual = sum(x['actual_completed'] for x in ledgers)
reserved = sum(x['reserved'] for x in ledgers)
assert actual == reserved == 35
assert sum(sum(c['counts'].values()) for x in ledgers for c in x['calls']) == actual
assert all(c['status'] == 'complete' and c['reserved'] == c['executed'] for x in ledgers for c in x['calls'])
state = evaluate.read_json(OUT/'simplification/state.json')
assert state['status'] == 'finished' and len(state['plan']) == 2
contract = evaluate.read_json(OUT/'simplification/contract.json')
assert state['contract_hash'] == evaluate.digest(OUT/'simplification/contract.json')
assert state['native_receipt_sha256'] == evaluate.json_hash(ledgers[1])
assert contract['sources']['native'] == evaluate.identity()
for record in state['records'].values():
    assert record['config']['model'] == 'new-fixture'
assert len((OUT/'original-prompt.txt').read_bytes()) == 4193
assert len((OUT/'selected-prompt.txt').read_bytes()) == 3671
judge = evaluate.read_json(OUT/'judge-observations.json')
assert judge['all_pass']['kappa_decided'] is None
assert judge['all_pass']['kappa_undefined_reason'] == 'expected_disagreement_is_zero'
assert judge['all_attempted']['coverage'] == .75
assert judge['all_attempted']['other_by_gold']['PASS']['ERROR'] == 1
skills = ['bootstrap','create-eval','adversarial-cases','run-eval','calibrate-judge','ablation','bitter-lesson']
inventory = {'workspace_source':evaluate.read_json(ROOT/'.cstack-source.json'),
    'skill_lock':evaluate.read_json(ROOT/'cstack-skills.lock.json'),
    'used_installed_skills':{name:{'path':str(ROOT/'.agents/skills'/name/'SKILL.md'),
         'sha256':evaluate.digest(ROOT/'.agents/skills'/name/'SKILL.md')} for name in skills},
    'helper_sources':{name:evaluate.digest(ROOT/name) for name in ['judge_calibration/adapters.py','judge_calibration/statistics.py','exercises/fixtures/verify_claim.py','methods/native.py','simplification/protocol.py']}}
evaluate.write_json(OUT/'source-usage.json',inventory)
result={'prior_manifest_verified':True,'native_runs_checked':verified_runs,'actual_native_cases':actual,
        'reserved_native_cases':reserved,'finished_and_exact_confirmation_plan':True,
        'ledger_state_source_prompt_statistics_checks':'PASS','additional_native_executions':0}
evaluate.write_json(OUT/'verification.json',result)
manifest['files']={str(p.relative_to(OUT)):evaluate.digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p != OUT/'manifest.json'}
evaluate.write_json(OUT/'manifest.json',manifest)
print(json.dumps(result,sort_keys=True))
