import ast, hashlib, json, pathlib, sys
repo=pathlib.Path.cwd(); base=repo/'eval-runs/skill-exercise'
sys.path.insert(0,str(repo))
from judge_calibration.adapters import normalize
from judge_calibration.statistics import agreement

def read(p): return json.loads(p.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p): return [json.loads(s) for s in p.read_text().splitlines()]
def save(name,value): (base/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

native=[]
for p in sorted(base.rglob('summary.json')):
    s=read(p)
    if 'executed_count' not in s: continue
    m=read(p.parent/'manifest.json'); traces=lines(p.parent/'traces.jsonl')
    assert s['complete'] and len(traces)==s['selected_count']==s['executed_count']
    assert [t['id'] for t in traces]==s['case_ids']==m['case_ids']
    assert digest(p.parent/'candidate.py')==s['candidate_hash']==m['candidate_hash']
    assert all(digest(repo/f)==h for f,h in m['identity']['files'].items())
    counts={name:sum(t['outcome']==name for t in traces) for name in ['PASS','FAIL','ERROR','UNKNOWN']}
    assert counts==s['counts']
    native.append({'directory':str(p.parent.relative_to(base)),'candidate':str((p.parent/'candidate.py').relative_to(base)),'candidate_sha256':s['candidate_hash'],'suite':m['suite'],'selected':s['selected_count'],'executed':s['executed_count'],'case_ids':s['case_ids'],'counts':counts,'score':s['score'],'identity':m['identity']})
assert sum(n['executed'] for n in native)==252
jdir=base/'judge-calibration'; state=read(jdir/'campaign/state.json')
inputs=lines(jdir/'dataset/inputs.jsonl'); private=lines(jdir/'dataset/labels.private.jsonl')
assert len(inputs)==len(private)==24
for row in inputs:
    assert set(row)=={'id','case','criterion_version','output'}
    assert set(row['case'])=={'expected','request','state'}
families={}
for row in private: families.setdefault(row['family'],set()).add(row['role'])
assert len(families)==12 and all(len(v)==1 for v in families.values())
prediction_count=0
for run in state['runs']:
    p=jdir/'campaign'/run['label']; manifest=read(p/'manifest.json')
    assert run['status']=='complete'
    assert digest(p/'manifest.json')==run['manifest_sha256']
    assert digest(p/'predictions.jsonl')==run['predictions_sha256']
    cfg=read(p/'config.json'); preds=lines(p/'predictions.jsonl')
    for pred in preds: assert normalize(pred['raw'],cfg,pred['exit_code'])==pred['decision']
    prediction_count+=len(preds)
assert prediction_count==96 and state['worker_calls']==102
assert state['phase']=='final_consumed' and 'final' in state['exposed_roles']
assert set(state['final_plan'])=={r['label'] for r in state['runs'] if r['role']=='final'}

cfg={'backend':'jev','question_means_failure':True,'pass_below':.5,'fail_at_or_above':.5}
def noul(p,confidence=None):
    ans={'type':'noul','noul':p}
    if confidence is not None: ans['confidence']=confidence
    return {'answers':{'criterion':ans}}
controls=[]
for label,raw,config,expect,prob in [
 ('confidence-is-not-event-probability',noul(.2,.99),cfg,'PASS',.2),
 ('yes-means-acceptable',noul(.8),dict(cfg,question_means_failure=False),'PASS',1-.8),
 ('choice-failure-probability',{'answers':{'criterion':{'type':'choice','choice':'FAIL','probabilities':{'PASS':.2,'FAIL':.8},'confidence':.11}}},cfg,'FAIL',.8),
 ('invalid-probability',noul(2),cfg,'ERROR',None),
 ('missing-evidence-shape',{'answers':{}},cfg,'ERROR',None),
 ('optional-explanation-absent',{'text':'{"verdict":"PASS"}'},{'backend':'llm'},'PASS',None),
 ('malformed-verdict',{'text':'{"verdict":"APPROVE"}'},{'backend':'llm'},'ERROR',None),
 ('duplicate-response-field',{'text':'{"verdict":"FAIL","verdict":"PASS"}'},{'backend':'llm'},'ERROR',None),
]:
    decision=normalize(raw,config)
    assert decision['verdict']==expect and decision['failure_probability']==prob
    controls.append({'label':label,'raw':raw,'config':config,'decision':decision})
undefined=agreement([{'gold':'PASS','verdict':'PASS'}])
assert undefined['kappa_decided'] is None

simp=read(base/'simplification/results.json'); simp_state=read(base/'simplification/state.json')
assert simp_state['status']=='finished' and simp_state['reserved_case_executions']==164
for label,record in simp_state['records'].items():
    p=base/'simplification/native'/label
    assert all(digest(p/name)==h for name,h in record['evidence'].items())
assert hashlib.sha256(json.dumps(read(base/'simplification/native/executions.json'),sort_keys=True,separators=(',', ':')).encode()).hexdigest()==simp_state['native_receipt_sha256']
prompts={}
for label in ['final-old-existing','final-old-reduced','final-old-simplified','final-new-existing','final-new-simplified']:
    candidate=base/'simplification/native'/label/'candidate.py'
    constants={node.targets[0].id:ast.literal_eval(node.value) for node in ast.parse(candidate.read_text()).body if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ['PROMPT','MODEL']}
    prompts[label]={'model':constants['MODEL'],'prompt_utf8_bytes':len(constants['PROMPT'].encode()),'prompt':constants['PROMPT']}
assert prompts['final-old-simplified']['prompt']==prompts['final-new-simplified']['prompt']
assert prompts['final-old-existing']['prompt_utf8_bytes']==4193
assert prompts['final-new-simplified']['prompt_utf8_bytes']==3667
save('inspection.json',{'native_runs':len(native),'native_case_processes':252,'native_all_complete':True,'source_frozen_checks':True,'input_projection_separate_from_gold':True,'source_families_partitioned':True,'judge_prediction_records':96,'repeatability_processes':6,'judge_final_phase':state['phase'],'judge_final_plan_labels':sorted(state['final_plan']),'judge_raw_normalization_consistent':True,'normalization_controls':controls,'undefined_kappa_control':undefined,'prompt_measurements':prompts,'inspection_incidents':[{'command':'inspect-evidence','exit_code':1,'error':'Inspector compared JSON canonical receipt hash to pretty-printed file hash; corrected inspector to protocol canonical JSON semantics. No source or run evidence changed.','native_cases_or_worker_calls_consumed':0},{'command':'inline read-only inspection of state.runs as a dictionary','exit_code':1,'error':'AttributeError: list has no items; subsequent inspection used its actual list schema','native_cases_or_worker_calls_consumed':0}]})
usage={'native_case_budget':300,'native_case_processes':252,'native_remaining':48,'by_workflow':{'run_eval':16,'hill_climb':32,'judge_source':24,'simplification':164,'cross_examine':16},'native_counts':{k:sum(n['counts'][k] for n in native) for k in ['PASS','FAIL','ERROR','UNKNOWN']},'native_incomplete':0,'fixture_judge_response_processes':102,'fixture_judge_unique_source_rows':24,'fixture_judge_families':12,'fixture_predictions':96,'fixture_repeatability_processes':6,'original_claim_proxy_processes':3,'repaired_verifier_processes':2,'stored_output_native_regrades':12,'adapter_normalizations_distinct_controls':8,'adapter_normalizations_additional_control_calls':16,'stored_prediction_normalizations':192,'provider_calls':0,'paid_calls':0,'network_calls':0,'dependencies_installed':0,'subagents':0,'model_cost':None,'production_latency':None}
save('usage.json',usage)
result={'scope':'controlled installed-skill operations exercise; synthetic deterministic fixtures','completed':['run-eval','hill-climb','calibrate-judge','ablation','bitter-lesson','cross-examine-reproduction'],'incomplete':['independent intent adjudication unavailable','real human-gold calibration unrun','live backend/model validation unrun'],'run_eval':{'original':read(base/'run-original/summary.json'),'conforming':read(base/'run-conforming/summary.json'),'human_agreement':None},'hill_climb':{'selection':read(base/'hill-climb/selection.json'),'used_cases':32,'maximum':48,'confirmation_reserve':8,'verified':True,'regression_rejected':['dev-closed','dev-unrelated']},'judge':{'results':read(jdir/'results.json'),'final_exposure':state['exposed_roles'],'nominal_kappa':{label:row['agreement']['kappa_decided'] for label,row in read(jdir/'results.json')['final'].items()}},'simplification':simp,'cross_examine':{'native_forged':read(base/'claim-audit/native-forged/summary.json')['counts'],'native_alternative':read(base/'claim-audit/native-alternative/summary.json')['counts'],'replay':read(base/'claim-audit/replay-results.json'),'independent_review':'unreviewed','repaired_artifact':'claim-audit/verify_claim.repaired.py','canonical_changed':False},'usage':usage,'release_thresholds':None,'deployment':'unperformed'}
save('result-summary.json',result)
manifest={'workspace':str(repo),'evidence_root':str(base),'source_checkout':'/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/skill-audit-ablation/post-audit-baseline','materialization_argv':['python3','fixtures/playground/scripts/new_workspace.py','--source','/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/skill-audit-ablation/post-audit-baseline','--out',str(repo)],'installed_skills':{name:{'path':str(repo/'.agents/skills'/name/'SKILL.md'),'sha256':digest(repo/'.agents/skills'/name/'SKILL.md')} for name in ['run-eval','hill-climb','calibrate-judge','ablation','bitter-lesson','cross-examine']},'native_runs':native,'judge_runs':[dict(row,directory='judge-calibration/campaign/'+row['label']) for row in state['runs']],'artifacts':{'hill_climb_selected':'hill-climb/best.py','hill_climb_diff':'hill-climb/best.diff','judge_selected':'judge-calibration/selected-judge.fixture.json','simplification_selected':'simplification/selected-offline-fixture.py','simplification_diff':'simplification/selected.diff','simplification_candidates':[str(p.relative_to(base)) for p in sorted((base/'simplification/candidates').glob('*.py'))],'claim_artifacts':[str(p.relative_to(base)) for p in sorted((base/'claim-audit').glob('*')) if p.is_file()]},'commands':'commands.jsonl','usage':'usage.json','inspection':'inspection.json','result_summary':'result-summary.json','report':'REPORT.md','independent_review':'unreviewed','release_thresholds':None,'deployment':'unperformed'}
save('manifest.json',manifest)
print(json.dumps({'native_runs':len(native),'usage':usage,'evidence_checks':'passed'}))
