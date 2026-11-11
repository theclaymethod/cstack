"""Inspect fidelity and retained native evidence; does not execute candidates or replace grading."""
import hashlib, importlib.util, json
from pathlib import Path
root=Path(__file__).resolve().parent
workspace=root.parents[1]
spec=importlib.util.spec_from_file_location('native_evaluate',workspace/'evaluate.py')
native=importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
def read(p): return json.loads(p.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
handoff=read(root/'source/current-handoff-v1.json')
cases=native.load_cases('development',root/'author/approved.jsonl')
expected_membership=['approved-A-r1','approved-B-r2']
assert [c['id'] for c in cases]==expected_membership
fidelity=[]
for card,case in zip(handoff['approved_cards'],cases):
    checks={k: native.same_json(card[k],case[k]) for k in ['request','state','expected','family']}
    checks.update(current_revision=case['id']==f"approved-{card['id']}-r{card['revision']}",suite=case['suite']=='development')
    assert all(checks.values())
    fidelity.append({'card':f"{card['id']}:{card['revision']}",'case':case['id'],'checks':checks,'representation':'only envelope ID/suite added; source behavior mapped to native fields; ticket ID intentionally unconstrained'})
source_hashes=read(root/'evidence/source-freeze-before-author.json')
assert source_hashes=={p.name:digest(p) for p in sorted((root/'source').iterdir())}
protected=read(root/'evidence/protected-before.json')
assert protected=={p:digest(workspace/p) for p in protected}
results=[]; witnesses=[]; total=0
expected_outcomes={'legitimate':['PASS','PASS'],'alternative-id':['PASS','PASS'],'false-creation-claim':['PASS','FAIL'],'original-baseline':['FAIL','PASS'],'guidance-only':['PASS','FAIL']}
for name,expected in expected_outcomes.items():
    run=root/'native-runs'/name
    manifest,summary=native.checked_run(run)
    assert manifest['case_ids']==expected_membership
    actual=[r['outcome'] for r in summary['results']]
    assert actual==expected
    total+=summary['executed_count']
    results.append({'candidate':name,'outcomes':dict(zip(expected_membership,actual)),'counts':summary['counts'],'native_evidence_consistent':True})
    traces=[json.loads(line) for line in (run/'traces.jsonl').read_text().splitlines()]
    for trace,case in zip(traces,cases):
        # Observe raw subprocess JSON directly, independently of its note and native verdict.
        output=json.loads(trace['stdout']); state=output['state']; initial=case['state']
        originals=initial['tickets']; prior_ids={x['id'] for x in originals}
        new=[x for x in state['tickets'] if x['id'] not in prior_ids]
        witnesses.append({'candidate':name,'case':case['id'],'source':'retained actual subprocess stdout, not success note','action':output['action'],'account':output['account'],'initial_state':initial,'actual_resulting_state':state,'actual_ticket_delta':len(state['tickets'])-len(originals),'new_records':new,'original_ticket_prefix_preserved':state['tickets'][:len(originals)]==originals,'counter':state.get('counter'),'failed_native_checks':[k for k,v in trace['checks'].items() if not v]})
assert total==10 and total<=48
(root/'evidence/fidelity.json').write_text(json.dumps({'approved_count':2,'generated_count':2,'membership_exact':True,'source_frozen_unchanged':True,'protected_sources_unchanged':True,'rows':fidelity},indent=2)+'\n')
(root/'evidence/control-results.json').write_text(json.dumps(results,indent=2)+'\n')
(root/'evidence/state-witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
(root/'usage.json').write_text(json.dumps({'native_case_budget':48,'actual_native_case_attempts':total,'native_runs':5,'cases_per_run':2,'errors':0,'proposal_case_attempts':0,'fault_injections':0,'network_calls':0,'provider_calls':0,'paid_calls':0,'dependencies_installed':0,'nested_agents':0,'tests_run':0,'candidate_edits':'control copies under eval-runs only; canonical product unchanged','token_usage':'not available from local runtime; no invented token/cost/latency measure'},indent=2)+'\n')
print(json.dumps({'fidelity':'2/2 exact current approved cards; source hashes unchanged','native_attempts':total,'results':results},indent=2))
