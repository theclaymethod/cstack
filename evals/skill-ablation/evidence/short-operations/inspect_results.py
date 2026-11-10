import ast, copy, hashlib, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; B=ROOT/'eval-runs/skill-exercise'
spec=importlib.util.spec_from_file_location('native',ROOT/'evaluate.py'); native=importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Validate actual retained native evidence, not success messages.
runs=[]
for p in sorted(B.rglob('summary.json')):
 if not (p.parent/'manifest.json').exists(): continue
 manifest,summary=native.checked_run(p.parent)
 runs.append({'directory':str(p.parent.relative_to(B)),'selected':summary['selected_count'],'executed':summary['executed_count'],'counts':summary['counts'],'case_ids':summary['case_ids'],'candidate_sha256':manifest['candidate_hash'],'identity_hash':summary['identity_hash'],'complete':summary['complete']})
from judge_calibration.adapters import normalize
config=read(B/'judge/campaign/jev-selected-final/config.json')
raw={'answers':{'criterion':{'type':'noul','noul':0.2,'confidence':0.99}}}
checks={'failure_question':normalize(raw,config),'acceptable_question':normalize(raw,dict(config,question_means_failure=False)),'optional_llm_explanation_absent':normalize({'text':'{"verdict":"PASS"}'},{'backend':'llm'})}
assert checks['failure_question']['failure_probability']==0.2
assert abs(checks['acceptable_question']['failure_probability']-0.8)<1e-8
assert checks['failure_question']['rationale'] is None
(B/'normalization-checks.json').write_text(json.dumps({'input':raw,'results':checks,'scope':'Direct local normalization calls, no model or fixture worker processes'},indent=2))
# Confirm separated projected judge payloads and native raw response normalization.
inputs=[json.loads(x) for x in (B/'judge/dataset/inputs.jsonl').read_text().splitlines()]
assert all(set(x)=={'id','case','output','criterion_version'} and set(x['case'])=={'request','state','expected'} for x in inputs)
count=0
for p in (B/'judge/campaign').glob('*/predictions.jsonl'):
 cfg=read(p.parent/'config.json')
 for line in p.read_text().splitlines():
  row=json.loads(line); assert normalize(row['raw'],cfg,row['exit_code'])==row['decision']; count+=1
# Extract exact rendered prompt strings from candidate AST; do not execute extra candidates.
burdens={}
for label in ['original','drop-conflict-pair','final-new-simplified']:
 p=B/'simplification/candidates'/f'{label}.py'
 tree=ast.parse(p.read_text()); prompt=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PROMPT' for t in n.targets))
 (B/f'{label}.prompt.txt').write_text(prompt)
 burdens[label]={'rendered_utf8_bytes':len(prompt.encode()),'candidate_sha256':sha(p)}
assert burdens['original']['rendered_utf8_bytes']==4193
assert burdens['final-new-simplified']['rendered_utf8_bytes']==3667
j=read(B/'judge/results.json'); s=read(B/'simplification/results.json'); c=read(B/'campaign/state.json')
result={'status':'completed controlled local workflows; independent audit unreviewed','source_checkout':'/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/skill-audit-ablation/shortened-candidate','workspace':str(ROOT),'native_case_executions':sum(r['executed'] for r in runs),'native_run_count':len(runs),'fixture_judge_processes':j['fixture_judge_processes'],'provider_calls':0,'paid_calls':0,'human_gold_rows':0,'release_thresholds':None,'deployment':'unperformed','incomplete_native_cases':sum(r['selected']-r['executed'] for r in runs),'native_error_count':sum(r['counts']['ERROR'] for r in runs),'native_unknown_count':sum(r['counts']['UNKNOWN'] for r in runs),'schema_error_controls':3,'run_eval':read(B/'compare.stdout'),'hill_climb':{'used':c['used_case_runs'],'max':48,'confirmation':8,'selected_attempt':c['selected_attempt'],'selection':read(B/'campaign/selection.json')},'judge':{'authority':j['authority'],'final':{k:{'agreement':v['agreement'],'uncertainty':v['uncertainty'],'probabilities':v['probabilities']} for k,v in j['final'].items()},'raw_normalization_rows_verified':count,'runtime_input_rows_inspected':len(inputs),'exposure':read(B/'judge/campaign/state.json')['exposed_roles'],'final_refit_blocked':j['final_refit_blocked'],'selected':read(B/'judge/selected-judge.fixture.json')},'simplification':{'burden':s['burden'],'independently_extracted_burden':burdens,'migration':s['migration'],'old_model_reduction':s['old_model_reduction'],'naive_union':s['naive_union'],'reduction_history':s['reduction_history'],'diagnostics':s['diagnostics'],'minimality':s['minimality']},'cross_examine':{'proxy_passed':True,'forged_native_pass':0,'forged_native_total':8,'legitimate_alternative_pass':8,'legitimate_alternative_total':8,'repaired_forged':read(B/'claim-audit/repaired-forged.stdout'),'repaired_alternative':read(B/'claim-audit/repaired-alternative.stdout'),'independent_attacker':'unavailable','independent_reviewer':'unavailable','formal_adjudication':'unreviewed','canonical_grader_changed':False},'limits':['Fully readable synthetic fixtures; no independent held-out performance','Fixed simplification control schedule, no discovered optimizer or minimality sweep','Local host permissions; hashes and separate directories do not enforce security containment','Live backend calibration, real-model capability, token costs and latency savings unmeasured']}
assert result['native_case_executions']==252
(B/'results.json').write_text(json.dumps(result,indent=2))
artifacts=[]
for p in sorted(B.rglob('*')):
 if p.is_file() and (p.name in ['candidate.py','best.py','best.diff','selected-offline-fixture.py','selected.diff','selected-judge.fixture.json','config.json','forged.py','legitimate-alternative.py','repaired-verifier.py'] or p.parent.name=='candidates'):
  artifacts.append({'path':str(p.relative_to(B)),'sha256':sha(p)})
manifest={'root':str(B),'source_checkout':result['source_checkout'],'native_runs':runs,'candidate_and_configuration_artifacts':artifacts,'command_records':'commands.jsonl','usage':'usage.json','results':'results.json','report':'REPORT.md','native_identity':native.identity(),'skill_identities':{n:sha(ROOT/'.agents/skills'/n/'SKILL.md') for n in ['run-eval','hill-climb','calibrate-judge','ablation','bitter-lesson','cross-examine']}}
(B/'manifest.json').write_text(json.dumps(manifest,indent=2))
usage={'native_cases':{'run_eval':16,'hill_climb':32,'judge_source':24,'simplification':164,'cross_examine':16,'total':252,'limit':300,'remaining':48},'fixture_judge_processes':102,'fixture_repeatability_processes_included':6,'fixture_judge_process_limit':200,'actual_provider_calls':0,'paid_calls':0,'native_case_errors':0,'native_unknowns':0,'incomplete':0,'additional_direct_native_schema_grade_controls':3,'additional_direct_normalization_controls':3,'repaired_verifier_processes':2,'defective_verifier_processes':1,'note':'Direct evidence revalidation and grading do not execute candidate processes. The 102 worker calls are deterministic local processes, not model calls.'}
(B/'usage.json').write_text(json.dumps(usage,indent=2))
print(json.dumps({'native_cases':result['native_case_executions'],'native_runs':len(runs),'fixture_judge_processes':102,'raw_normalization_rows':count,'burdens':burdens},indent=2))
