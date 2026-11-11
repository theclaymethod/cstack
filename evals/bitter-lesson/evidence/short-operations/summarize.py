import json,pathlib,hashlib,sys,ast,collections
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));from judge_calibration.adapters import normalize
out=root/'eval-runs/skill-exercise'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
runs=[];count=0;totals=collections.Counter();inspections=[]
for f in sorted(out.rglob('summary.json')):
 r=read(f)
 if 'executed_count' not in r:continue
 rows=[json.loads(l) for l in (f.parent/'traces.jsonl').read_text().splitlines()]
 assert len(rows)==r['executed_count']==r['selected_count']
 assert [x['id'] for x in rows]==r['case_ids']
 assert collections.Counter(x['outcome'] for x in rows)==collections.Counter({k:v for k,v in r['counts'].items() if v})
 assert sha(f.parent/'candidate.py')==r['candidate_hash']
 for row in rows:assert all(k in row for k in ['input','output','error','stdout','stderr'])
 runs.append({'directory':str(f.parent.relative_to(out)),'candidate':str((f.parent/'candidate.py').relative_to(out)),'case_ids':r['case_ids'],'executed':r['executed_count'],'counts':r['counts'],'candidate_sha256':r['candidate_hash']})
 count+=r['executed_count'];totals.update(r['counts'])
base=read(out/'run-baseline/manifest.json')
# Every original source stays unchanged, anchored to the first native run.
frozen=read(out/'simplification/results.json')['source_identity']['native']['files']
assert all(sha(root/k)==v for k,v in frozen.items())
assert sha(root/'support_agent.py')==read(out/'run-baseline/summary.json')['candidate_hash']
worker_rows=0;normalization=[]
for f in sorted((out/'judge/campaign').glob('*/predictions.jsonl')):
 cfg=read(f.parent/'config.json');rows=[json.loads(l) for l in f.read_text().splitlines()];worker_rows+=len(rows)
 for row in rows:
  assert set(row['input'])=={'id','case','output','criterion_version'}
  assert set(row['input']['case'])=={'request','state','expected'}
  assert normalize(row['raw'],cfg,row['exit_code'])==row['decision']
 normalization.append({'run':f.parent.name,'rows':len(rows),'raw_normalized_match':True,'payload_excludes_labels_families_roles':True})
js=read(out/'judge/campaign/state.json');jr=read(out/'judge/results.json');sr=read(out/'simplification/results.json');ss=read(out/'simplification/state.json')
assert worker_rows+sum(x['repetitions'] for x in jr['repeatability'].values())==js['worker_calls']==102
assert js['phase']=='final_consumed' and jr['final_refit_blocked']
assert sr['native_case_executions']==read(out/'simplification/native/executions.json')['actual_completed']==164
prompts={}
for label in ['original','drop-conflict-pair','new-simplified','final-old-simplified','final-new-simplified']:
 p=out/f'simplification/candidates/{label}.py'
 tree=ast.parse(p.read_text())
 prompt=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PROMPT' for t in n.targets))
 prompts[label]={'bytes':len(prompt.encode()),'sha256':hashlib.sha256(prompt.encode()).hexdigest(),'contains_contract': '# Synthetic support-agent contract' in prompt}
assert prompts['final-old-simplified']==prompts['final-new-simplified']
assert prompts['original']['bytes']==4193 and prompts['new-simplified']['bytes']==3667
# Exercise response semantics directly, separately from worker counts and native executions.
cfg=js['final_plan']['jev-selected-final'];probes=[]
for label,raw,expect in [('confidence-not-probability',{'answers':{'criterion':{'type':'noul','noul':0.2,'confidence':0.99}}},'PASS'),('missing-probability',{'answers':{'criterion':{'type':'noul','confidence':0.99}}},'ERROR'),('invalid-probability',{'answers':{'criterion':{'type':'noul','noul':1.2}}},'ERROR')]:
 d=normalize(raw,cfg);assert d['verdict']==expect;probes.append({'label':label,'raw':raw,'decision':d})
invert=dict(cfg,question_means_failure=False);d=normalize({'answers':{'criterion':{'type':'noul','noul':0.2}}},invert);assert d['failure_probability']==0.8
probes.append({'label':'inverse-yes-polarity','decision':d})
assert normalize({'text':'{"verdict":"PASS"}'},dict(cfg,backend='llm'))['rationale'] is None
usage={'native_case_limit':300,'native_case_executions':count,'native_breakdown':{'run_eval':16,'hill_climb':32,'judge_source':24,'simplification':164,'cross_examine':16},'native_counts_all_attempts':dict(totals),'native_incomplete':0,'offline_judge_worker_processes':102,'worker_breakdown':{'fitting_and_final':worker_rows,'stability':6},'offline_worker_ceiling':200,'cross_proxy_processes':3,'stored_native_regrades':2,'extra_adapter_probes':5,'provider_calls':0,'paid_calls':0,'dependencies_installed':0,'nested_agents':0,'release_thresholds':None,'deployment':'unperformed'}
assert count==sum(usage['native_breakdown'].values())==252
metrics={k:{'agreement':v['agreement'],'uncertainty':v['uncertainty'],'probabilities':v['probabilities']} for k,v in jr['final'].items()}
result={'status':'completed controls; independent audit unreviewed','usage':usage,'run_eval':{k:read(out/k/'summary.json')['counts'] for k in ['run-baseline','run-conforming']},'hill_selection':read(out/'hill/selection.json'),'judge_final':metrics,'judge_exposure':js['exposed_roles'],'judge_final_plan':js['final_plan'],'simplification':sr,'cross':{'forged_native':read(out/'cross/forged-run/summary.json')['counts'],'alternative_native':read(out/'cross/legitimate-alternative-run/summary.json')['counts'],'independent_intent_review':'UNREVIEWED','independent_attacker':'unavailable'},'unmeasured':['human agreement','live judge calibration','model inference costs','production latency','generalization','statistical non-inferiority'],'release_thresholds':None,'deployment':'unperformed'}
dump(out/'usage.json',usage);dump(out/'results.json',result);dump(out/'inspected-state.json',{'native_runs_inspected':runs,'raw_judge_normalization':normalization,'prompt_inspection':prompts,'adapter_probes':probes,'unchanged_frozen_sources':frozen,'inspection_correction':'An exploratory literal-eval of all assignments stopped on a nonliteral alias; PROMPT-only extraction above completed. No native executions added.','audit_ledger_correction':'new_ticket_fields was true for the empty forged output; divergence is ticket_delta, new_ticket_membership and action_matches_mutation.'})
ledger=out/'cross/CROSS_EXAMINE_LEDGER.md';ledger.write_text(ledger.read_text().replace('ticket delta, new membership, action/mutation and new-ticket fields','ticket delta, new membership and action/mutation'))
manifest={'workspace':str(root),'source':json.loads((root/'.cstack-source.json').read_text()),'skills_lock':'../../cstack-skills.lock.json','native_runs':runs,'selected_artifacts':['hill/best.py','hill/best.diff','judge/selected-judge.fixture.json','simplification/selected-offline-fixture.py','simplification/selected.diff','simplification/candidates/drop-conflict-pair.py','cross/legitimate-alternative.py'],'baseline_artifacts':['run-baseline/candidate.py','hill/attempts/000-baseline/candidate.py','judge/campaign/llm-baseline-final/config.json','judge/campaign/jev-baseline-final/config.json','simplification/candidates/original.py'],'configuration_and_state':['hill/contract.json','hill/state.json','judge/campaign/state.json','judge/dataset/manifest.json','simplification/contract.json','simplification/state.json','simplification/native/executions.json'],'commands':'commands.jsonl','usage':'usage.json','inspections':'inspected-state.json','results':'results.json','report':'REPORT.md'}
dump(out/'manifest.json',manifest)
print(json.dumps(usage,indent=2))
