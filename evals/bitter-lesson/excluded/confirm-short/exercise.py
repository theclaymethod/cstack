"""Reproducible local exercise; all execution goes through native project helpers."""
import copy
import difflib
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from methods.native import Runs, evaluate, write, jsonl
from simplification.protocol import Experiment, UNITS, configuration, render, candidate_source
from judge_calibration.adapters import normalize
from judge_calibration.statistics import agreement, uncertainty, probability_diagnostics

OUT = Path(__file__).resolve().parent
def save(name, value):
    write(OUT / name, value)

def main():
    (OUT / 'source').mkdir()
    (OUT / 'package').mkdir()
    (OUT / 'controls').mkdir()
    a = {'id':'approved-a-r1','suite':'development','family':'owner-prohibition',
         'request':{'text':'Do not create a VPN support ticket.','account':None,'accounts':['red','blue']},
         'state':{'tickets':[], 'preserve':{'count':9,'enabled':False}},
         'expected':{'allowed_actions':['guidance'],'account':None,'ticket_delta':0}}
    b = {'id':'approved-b-r2','suite':'development','family':'owner-explicit-creation',
         'request':{'text':'Please submit a VPN support request.','account':'red','accounts':['red','blue']},
         'state':{'tickets':[{'id':'keep-blue','account':'blue','status':'open','issue':'vpn','extra':{'flags':[True,False]}},
                             {'id':'keep-red','account':'red','status':'closed','issue':'vpn'}],
                  'preserve':{'count':9,'enabled':False}},
         'expected':{'allowed_actions':['create_ticket'],'account':'red','ticket_delta':1}}
    decisions = {'authority':'Scripted synthetic owner expectations, not real human outcome labels',
        'current_approved':[a,b], 'history':[
            {'card':'A','revision':1,'status':'approved','behavior':'Guidance, null account, all state unchanged'},
            {'card':'B','revision':1,'status':'superseded','behavior':'Guidance-only proposal; full prior proposal text unavailable'},
            {'card':'B','revision':2,'status':'approved-exact-replacement','supersedes':1,
             'behavior':'Create one open VPN ticket for red with any unique nonempty ID, preserving all original state'}],
        'pending':[{'card':'C','behavior':'Automatic escalation for urgent VPN requests','status':'deferred','scored':False}]}
    save('source/decisions.json', decisions)
    jsonl(OUT / 'package/cases.jsonl', decisions['current_approved'])
    # Reuse the native state checks. Owner approvals add no semantic-note criterion.
    (OUT / 'package/rubric.md').write_text((ROOT / 'evals/rubric.md').read_text() +
        '\nOwner package: A revision1 and B revision2 only. Any unique nonempty ID is valid. '
        'C remains pending. Note wording is subject only to the native nonempty-string schema.\n')
    save('package/config.json', {'format':'project-native JSONL', 'runner':'evaluate.py', 'suite':'all',
         'cases':'cases.jsonl','authoritative_source':'../source/decisions.json',
         'repeats':1,'synthetic':True,'intended_role':'exposed development checks',
         'semantic_judge':'not used','pending_excluded':['C']})
    loaded = evaluate.load_cases('all', OUT / 'package/cases.jsonl')
    assert loaded == decisions['current_approved']
    save('package/fidelity.json', {'exact_request_state_family_expected_match':True,
        'approved_current':2,'superseded_excluded':1,'pending_excluded':1})
    full = configuration('new-fixture', list(UNITS))
    configs = {'full': full,
      'no-legacy':configuration('new-fixture',set(UNITS)-{'legacy-auth'}),
      'no-planning-example':configuration('new-fixture',set(UNITS)-{'plan','plan-detail','example'}),
      'no-duplicate-a':configuration('new-fixture',set(UNITS)-{'duplicate-a'}),
      'no-duplicate-b':configuration('new-fixture',set(UNITS)-{'duplicate-b'}),
      'no-duplicates':configuration('new-fixture',set(UNITS)-{'duplicate-a','duplicate-b'}),
      'no-conflict-b':configuration('new-fixture',set(UNITS)-{'conflict-b'}),
      'no-conflict-pair':configuration('new-fixture',set(UNITS)-{'conflict-a','conflict-b'}),
      'contract-only':configuration('new-fixture',['contract']),
      'reduced':configuration('new-fixture',['contract','duplicate-b'])}
    hypotheses = {
      'no-legacy':'Current local stand-in may no longer require the legacy authorization recipe.',
      'no-planning-example':'Planning closure and example may be noise.',
      'no-duplicate-a':'Duplicate B may suffice alone.',
      'no-duplicate-b':'Duplicate A may suffice alone.',
      'no-duplicates':'Joint removal tests whether individually harmless duplicate removals interact.',
      'no-conflict-b':'Single compensating-cue removal may regress.',
      'no-conflict-pair':'Removing both compensating cues may restore behavior.',
      'contract-only':'Clean task contract alone tests lower bound within the supplied catalog.',
      'reduced':'Contract plus one short duplicate reminder may preserve full quality as a combined design.'}
    save('PLAN.json', {'total_native_limit':120, 'planned_owner_controls':14,
        'planned_simplification':88, 'total_planned_native':102,
        'simplification_limit':88,'confirmation_reserve':8,'configs':configs,'hypotheses':hypotheses,
        'quality_policy':'zero observed regressions, zero finite-case quality loss, no errors/unknown versus original full baseline',
        'burden':'rendered UTF-8 prompt bytes, then unit count',
        'selection':'smallest tested admissible design; freeze original and selection before 4-case confirmation each',
        'stop':'fixed ten-config screen plus two confirmations; no post-confirmation fitting',
        'trials':1,'sampling':'deterministic fresh subprocess per case; no caches',
        'exposure':'All fixture cases readable; development exposed; confirmation is a reserved workflow role, no independent generalization',
        'host_model':'Inherited host identity not independently queryable; unchanged throughout; no model comparison',
        'allowed_backend':'new-fixture deterministic stand-in only','python':sys.version,'platform':platform.platform(),
        'missing_cells':['old production/existing','old production/reduced'],
        'unmeasured':['host/model tokens','monetary costs or savings','model latency or savings','production quality']})
    source_identity = evaluate.identity()
    save('source/native-identity-before.json', source_identity)
    # Standalone controls consume real inputs rather than grading stored success text.
    common = '''import copy,json,sys
p=json.load(sys.stdin)
s=copy.deepcopy(p['state'])
creation=p['request']['text'].startswith('Please submit')
o={'action':'create_ticket' if creation else 'guidance','account':'red' if creation else None,'state':s,'note':'Synthetic control response.'}
'''
    variants = {
        'alternative-alpha':"if creation: s['tickets'].append({'id':'alpha-unique','account':'red','status':'open','issue':'vpn'})\n",
        'alternative-beta':"if creation: s['tickets'].append({'id':'different-id-42','account':'red','status':'open','issue':'vpn'})\n",
        'claim-only':"o['note']='Successfully created the requested ticket.'\n",
        'corrupt-preserve':"if creation: s['tickets'].append({'id':'new-id','account':'red','status':'open','issue':'vpn'})\ns['preserve']['enabled']=0\n",
        'duplicate-id':"if creation: s['tickets'].append({'id':'keep-red','account':'red','status':'open','issue':'vpn'})\n",
        'malformed':None}
    controls = Runs(OUT / 'native-owner-controls', limit=14)
    control_results={}
    control_results['original-product'] = controls.run('original-product',ROOT / 'support_agent.py',loaded)
    for name, body in variants.items():
        target=OUT / 'controls' / (name+'.py')
        target.write_text("print('not-json')\n" if body is None else common + body + "print(json.dumps(o))\n")
        control_results[name]=controls.run(name,target,loaded)
    save('owner-control-results.json', {name:{r['id']:{k:r[k] for k in ('outcome','checks','error')} for r in rows}
        for name,rows in control_results.items()})
    assert all(r['outcome']=='PASS' for name in ('alternative-alpha','alternative-beta') for r in control_results[name])
    assert control_results['claim-only'][1]['outcome']=='FAIL'
    assert not control_results['claim-only'][1]['checks']['ticket_delta']
    assert all(r['outcome']=='FAIL' for r in control_results['corrupt-preserve'])
    assert control_results['duplicate-id'][1]['outcome']=='FAIL'
    assert all(r['outcome']=='ERROR' for r in control_results['malformed'])
    experiment=Experiment(OUT / 'simplification',limit=88,confirmation_reserve=8)
    measured={name:experiment.measure(name,config) for name,config in configs.items()}
    comparisons={name:experiment.compare('full',name) for name in configs if name!='full'}
    admissible=[name for name in configs if name=='full' or comparisons[name]['admissible']]
    selected=min(admissible,key=lambda name:(measured[name]['prompt_utf8_bytes'],measured[name]['unit_count']))
    save('selection-before-confirmation.json', {'selected':selected,'config':configs[selected],
        'development_comparisons':comparisons,'criterion':'minimum rendered bytes among tested admissible candidates'})
    experiment.freeze({'confirm-full':full,'confirm-selected':configs[selected]})
    experiment.confirm('confirm-full'); experiment.confirm('confirm-selected'); experiment.finish()
    final=experiment.compare('confirm-full','confirm-selected')
    (OUT / 'selected.prompt.txt').write_text(render(configs[selected]))
    (OUT / 'original.prompt.txt').write_text(render(full))
    (OUT / 'selected.py').write_text(candidate_source(configs[selected]))
    save('selected.configuration.json',configs[selected])
    (OUT / 'prompt.diff').write_text(''.join(difflib.unified_diff(render(full).splitlines(True),
        render(configs[selected]).splitlines(True),fromfile='original.prompt.txt',tofile='selected.prompt.txt')))
    save('simplification-comparison.json',{'selected':selected,'development':comparisons,'confirmation':final,
         'original_bytes':measured['full']['prompt_utf8_bytes'],'selected_bytes':measured[selected]['prompt_utf8_bytes'],
         'bytes_saved':measured['full']['prompt_utf8_bytes']-measured[selected]['prompt_utf8_bytes'],
         'status':'smallest confirmed candidate among the declared tested configurations; not global minimality'})
    # Stored observations are owner-supplied summaries, not newly executed judge calls.
    raw=[{'id':'stored-'+str(i+1),'family':'stored-control-family-unknown', 'gold':'PASS',
           'raw':{'text':'{"verdict":"PASS"}' if i<3 else 'malformed stored response'},
           'provenance':'Reconstruction of supplied summary; original raw response unavailable'} for i in range(4)]
    rows=[dict(r,**normalize(r['raw'],{'backend':'llm'})) for r in raw]
    save('measurement-stored-observations.json',rows)
    save('measurement.json',{'agreement':agreement(rows),'uncertainty':uncertainty(rows),
        'probability':probability_diagnostics(rows), 'new_judge_calls':0,'live_fitting':'unrun and unauthorized',
        'family_assumption':'Group entire tiny stored control together; independent construction families unavailable',
        'interpretation':'Not calibrated: synthetic all-PASS labels, one parser error, no failure class or independent human gold; no release threshold authorized'})
    assert source_identity == evaluate.identity()
    save('source/native-identity-after.json',evaluate.identity())
    experiment.verify()
    actual=controls.reserved+experiment.runs.reserved
    assert actual==102 and actual<=120
    save('usage.json',{'limit_native_case_attempts':120,'native_case_attempts':actual,
        'native_completed':sum(c['executed'] for c in controls.calls)+sum(c['executed'] for c in experiment.runs.calls),
        'owner_controls':14,'simplification_development':80,'simplification_confirmation':8,'remaining_native':18,
        'new_judge_calls':0,'provider_calls':0,'paid_calls':0,'network_calls':0,'new_dependencies':0,
        'host_model_token_usage':None,'monetary_savings':None,'model_latency_savings':None,
        'native_wall_seconds':'Per-run local wall times retained by adapter; not model latency',
        'replay':'python3 eval-runs/skill-exercise/exercise.py in a fresh materialized workspace with empty output directory except this script'})
    save('validation.json',{'native_owner_controls_checked':7,'exact_source_fidelity':True,
        'unchanged_native_identity':True,'experiment_verify':'passed','actual_completed_equals_reserved':True,
        'no_nested_delegation':True,'no_canonical_edits':True})

if __name__=='__main__':
    main()
