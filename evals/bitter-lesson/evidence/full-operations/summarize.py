"""Verify retained native evidence and emit inventories without new execution."""
import ast
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
from execute import ROOT, OUT

def read(path): return json.loads(path.read_text())
def write(path, data): path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('native',ROOT/'evaluate.py')
native=importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
inventory=[]; observations=[]
for manifest in sorted(OUT.rglob('manifest.json')):
    data=read(manifest)
    if 'candidate_hash' not in data: continue
    m,s=native.checked_run(manifest.parent)
    traces=[json.loads(line) for line in (manifest.parent/'traces.jsonl').read_text().splitlines()]
    inventory.append({'path':str(manifest.parent.relative_to(OUT)), 'candidate':str((manifest.parent/'candidate.py').relative_to(OUT)),
        'candidate_sha256':m['candidate_hash'],'suite':m['suite'],'case_ids':m['case_ids'],
        'executed':s['executed_count'],'complete':s['complete'],'counts':s['counts'],'score':s['score']})
    for trace in traces:
        if trace['id'] in ('dev-explicit','dev-duplicate','dev-closed','dev-unrelated','conf-howto'):
            observations.append({'run':str(manifest.parent.relative_to(OUT)), 'id':trace['id'],
                'input':trace['input'],'output':trace['output'],'checks':trace['checks'],'outcome':trace['outcome'],'error':trace['error']})
assert sum(r['executed'] for r in inventory)==260
write(OUT/'native-run-inventory.json',inventory)
write(OUT/'inspected-state-evidence.json',observations)
before=read(OUT/'source-before.json')
assert all(sha(ROOT/p)==value for p,value in before.items())
write(OUT/'source-after.json',{p:sha(ROOT/p) for p in before})
judgedir=OUT/'judge-calibration'; judge=read(judgedir/'results.json'); jstate=read(judgedir/'campaign/state.json')
inputs=[json.loads(line) for line in (judgedir/'dataset/inputs.jsonl').read_text().splitlines()]
assert all(set(r)=={'id','case','output','criterion_version'} for r in inputs)
predictions=list((judgedir/'campaign').rglob('predictions.jsonl'))
assert sum(len(p.read_text().splitlines()) for p in predictions)==96
assert jstate['worker_calls']==jstate['reserved_calls']==102
assert jstate['phase']=='final_consumed' and all(r['status']=='complete' for r in jstate['runs'])
simplify=read(OUT/'simplification/results.json')
def prompt(path):
    for node in ast.parse(path.read_text()).body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PROMPT' for t in node.targets):
            return ast.literal_eval(node.value)
orig=prompt(OUT/'simplification/native/final-old-existing/candidate.py')
old=prompt(OUT/'simplification/native/final-old-simplified/candidate.py')
chosen=prompt(OUT/'simplification/selected-offline-fixture.py')
assert old==chosen
assert len(orig.encode())==4193 and len(chosen.encode())==3667
write(OUT/'usage.json',{
    'native_candidate_case_executions':260,'native_limit':300,'remaining_native_allowance':40,
    'by_workflow':{'run_eval':16,'hill_climb':32,'judge_source_execution':24,'simplification':164,'claim_audit':24},
    'native_confirmation_executions':36,'native_outcomes':dict(sum((collections.Counter(r['counts']) for r in inventory),collections.Counter())),
    'incomplete_native_attempts':0,'judge_worker_processes':102,'judge_worker_limit':200,
    'judge_prediction_processes':96,'judge_repeatability_processes':6,
    'judge_pending_calls':0,'stored_output_repaired_verifier_replays':2,
    'final_inventory_validation':'260 stored observations rechecked with native.checked_run; no new candidate execution',
    'provider_calls':0,'paid_calls':0,'network_calls':0,'new_dependencies':0,'nested_agents':0,
    'model_token_usage':None,'model_cost':None,'production_latency_evidence':None})
result={
    'status':'completed with explicitly unreviewed independent audit',
    'run_eval':{'original':read(OUT/'run-original/summary.json'),'conforming':read(OUT/'run-conforming/summary.json'),'human_agreement':None},
    'hill_climb':{'selection':read(OUT/'hill-climb/selection.json'),'used':32,'limit':48,
        'rejected_regressions':['dev-closed','dev-unrelated'],'best_artifact':'hill-climb/best.py'},
    'judge':{'final':{k:{'agreement':v['agreement'],'uncertainty':v['uncertainty'],'probabilities':v['probabilities']} for k,v in judge['final'].items()},
        'selected_configs':judge['selected_configs'],'baseline_config_locations':['judge-calibration/campaign/llm-baseline-final/config.json','judge-calibration/campaign/jev-baseline-final/config.json'],
        'gold_authority':judge['authority'],'phase':jstate['phase'],'runtime_input_keys':list(inputs[0]),'workers':102,
        'family_count':12,'items':24,'final_items_per_judge':8,'live_backends':judge['live_backend_status']},
    'simplification':simplify,
    'cross_examine':{'false_claim_reproduced':True,'native_forgery':'FAIL','alternative_native_passes':8,'malformed_native_errors':8,
        'repaired_replays':read(OUT/'claim-audit/replays.json'),'independent_attacker':'unavailable','independent_intent_review':'unreviewed',
        'canonical_repair':'not performed','local_repair':'claim-audit/verify_claim.repaired.py'},
    'source_unchanged':True,'human_labels':None,'release_thresholds':None,'deployment':'unperformed',
    'usage':'usage.json','native_inventory':'native-run-inventory.json'}
write(OUT/'results.json',result)
artifacts=['hill-climb/best.py','hill-climb/best.diff','judge-calibration/selected-judge.fixture.json',
    'simplification/selected-offline-fixture.py','simplification/selected.diff','claim-audit/forged.py',
    'claim-audit/alternative.py','claim-audit/malformed.py','claim-audit/verify_claim.original.py','claim-audit/verify_claim.repaired.py']
write(OUT/'manifest.json',{'workspace':str(ROOT),'evidence_root':str(OUT),'native_runs':inventory,
    'candidate_artifacts':{p:sha(OUT/p) for p in artifacts},
    'skill_identities':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'.agents/skills').rglob('*.md'))},
    'commands':'commands.jsonl','usage':'usage.json','summary':'results.json','report':'REPORT.md',
    'baseline_sources':'source-before.json','final_sources':'source-after.json',
    'judge_raw_runs':[str(p.parent.relative_to(OUT)) for p in sorted(predictions)],
    'source_identity_unchanged':True})
print(json.dumps(read(OUT/'usage.json'),indent=2))
