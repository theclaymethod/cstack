"""One authorized synthetic confirmation exercise. No providers or dependencies."""
from pathlib import Path
import copy, difflib, hashlib, json, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from methods.native import Runs, evaluate, write, jsonl, read_rows
from simplification.protocol import Experiment, UNITS, configuration, render
from judge_calibration.adapters import normalize
from judge_calibration.statistics import agreement, uncertainty, probability_diagnostics
OUT = Path(__file__).resolve().parent
TASK = ROOT.parents[1] / 'tasks/confirmation.md'
# The statement below is the task's exact approved scenario, not an output label.
request = {'text':'Please submit a VPN support request.', 'account':'team-red','accounts':['team-red','team-blue']}
state = {'tickets':[{'id':'old-blue','account':'team-blue','status':'open','issue':'vpn','metadata':{'tags':['keep'],'active':True}}, {'id':'old-red','account':'team-red','status':'closed','issue':'vpn'}], 'counter':31, 'settings':{'keep':False}}
expected = {'allowed_actions':['create_ticket'],'ticket_delta':1,'account':'team-red'}
source = {'revision':1,'kind':'explicit scripted synthetic expectation','request':request,'state':state,'expected':expected,'acceptable_alternative':'Any unique nonempty string ticket ID','preservation':'Entire original state including ticket metadata, order, counter and settings','outcome_labels':None,'urgency_policy':None,'independent_scenario_review':False,'independent_intent_review':False}
shutil.copyfile(TASK, OUT/'task-source.md')
write(OUT/'source-expectation.json',source)
case = {'id':'approved-vpn-rich-state-v1','suite':'development','family':'approved-vpn-rich-state','request':copy.deepcopy(request),'state':copy.deepcopy(state),'expected':copy.deepcopy(expected)}
jsonl(OUT/'approved-native.jsonl',[case])
loaded = evaluate.load_cases('development',OUT/'approved-native.jsonl')
assert len(loaded)==1
assert evaluate.same_json(loaded[0]['request'],source['request']) and evaluate.same_json(loaded[0]['state'],source['state']) and evaluate.same_json(loaded[0]['expected'],source['expected'])
write(OUT/'source-fidelity.json',{'request_exact':True,'state_exact_including_types':True,'expectation_exact':True,'source_sha256':evaluate.digest(OUT/'source-expectation.json'),'case_sha256':evaluate.digest(OUT/'approved-native.jsonl')})
write(OUT/'pending.json',{'speculative_urgency_variant':{'status':'outside approved/scored cases','executed':False,'reason':'No urgency policy or expectation approval'},'formal_independent_audit_adjudication':'unreviewed; no independent intent reviewer available','human_output_labels':'unavailable'})
(OUT/'candidates').mkdir()
legit = (ROOT/'examples/candidates/improved.py').read_text()
(OUT/'candidates/legitimate.py').write_text(legit)
(OUT/'candidates/alternative.py').write_text(legit.replace('ticket-{sequence}', 'alternative-{sequence}'))
(OUT/'candidates/false-claim.py').write_text('import json,sys\np=json.load(sys.stdin)\nprint(json.dumps({"action":"create_ticket","account":p["request"]["account"],"state":p["state"],"note":"Opened the requested VPN support ticket."}))\n')
write(OUT/'plan.json',{'native_limit':120,'approved_controls':3,'simplification_limit':117,'simplification_confirmation_reserve':8,'quality_policy':'zero finite score loss and no baseline PASS regressions/errors against ORIGINAL new-fixture full prompt','burden':'rendered UTF-8 bytes and retained unit count','native_trials':1,'confirmation_plan':['baseline-confirm','selected-confirm'],'baseline_model':'new-fixture','old_model':'unavailable and not authorized','paid_provider_calls':0,'new_dependencies':0,'fixture_scope':'exposed synthetic controls'})
controls = Runs(OUT/'native-controls',3)
observations=[]
for name in ['legitimate','alternative','false-claim']:
    traces=controls.run(name,OUT/'candidates'/f'{name}.py',loaded)
    row=traces[0]
    outputfile=OUT/'native-controls'/f'{name}-output.json'
    write(outputfile,row['output'])
    proxy=subprocess.run([sys.executable,str(ROOT/'exercises/fixtures/verify_claim.py'),str(outputfile)],text=True,capture_output=True)
    original=case['state']; actual=row['output']['state']
    observations.append({'candidate':name,'native_outcome':row['outcome'],'native_checks':row['checks'],'proxy_exit':proxy.returncode,'proxy_stdout':proxy.stdout,'proxy_stderr':proxy.stderr,'independent_state_witness':{'original_ticket_prefix_preserved':evaluate.same_json(actual['tickets'][:len(original['tickets'])],original['tickets']),'other_state_preserved':evaluate.same_json({k:v for k,v in actual.items() if k!='tickets'},{k:v for k,v in original.items() if k!='tickets'}),'ticket_count_delta':len(actual['tickets'])-len(original['tickets']),'entire_state_unchanged':evaluate.same_json(actual,original),'appended':actual['tickets'][len(original['tickets']):]},'armed':name=='false-claim','activated':name=='false-claim' and row['output']['action']=='create_ticket' and evaluate.same_json(actual,original),'access':'operator-authored standalone candidate; unchanged native grader and source case; host subprocess is not a security sandbox','adjudication':'unreviewed independent audit; observed control outcome only'})
write(OUT/'control-observations.json',observations)
# Judge controls use the real normalizer and statistics helpers, with no judge fitting.
config={'backend':'jev','question_means_failure':True,'pass_below':.5,'fail_at_or_above':.5}
malformed={'answers':{'criterion':{'type':'choice','choice':'PASS','probabilities':{'PASS':.8,'FAIL':.8},'confidence':.99}}}
malformed_result=normalize(malformed,config)
valid={'answers':{'criterion':{'type':'noul','noul':.1,'confidence':.99}}}
valid_result=normalize(valid,config)
assert malformed_result['verdict']=='ERROR' and valid_result['verdict']=='PASS' and valid_result['failure_probability']==.1
all_pass=[{'id':f'paired-{i}','family':f'fixture-family-{i}','gold':'PASS','verdict':'PASS','failure_probability':.1} for i in range(4)]
malformed_rows=[{'id':'malformed-control','family':'malformed-fixture','gold':'PASS',**malformed_result}]
write(OUT/'judge-inputs.json',{'configuration':config,'malformed_raw':malformed,'valid_raw':valid,'paired_label_rows':all_pass,'labels_authority':'synthetic controls, no human outcome labels','no_fitting':True})
write(OUT/'judge-normalized.json',{'malformed':malformed_result,'valid':valid_result})
write(OUT/'judge-observations.json',{'malformed_only':agreement(malformed_rows),'all_pass':agreement(all_pass),'all_pass_uncertainty':uncertainty(all_pass,draws=100,seed=17),'combined_all_attempted':agreement(all_pass+malformed_rows),'probabilities':probability_diagnostics(all_pass+malformed_rows),'confidence':'Concentration confidence is not event probability or probability of correctness. Typed schema validity does not establish accuracy/robustness/calibration. Synthetic probabilities and labels establish arithmetic controls only.','live_judge_fitting':'unrun and unauthorized','release_threshold':None})
# Each diagnostic is relative to the same full original new-model baseline.
full=set(UNITS)
schedule=[('full',full,'original baseline'),('no-legacy',full-{'legacy-auth'},'remove legacy authorization reminder'),('no-noise',full-{'plan','plan-detail','example'},'dependency-closed noise group'),('no-duplicate-a',full-{'duplicate-a'},'conditional contribution of duplicate A'),('no-duplicate-b',full-{'duplicate-b'},'conditional contribution of duplicate B'),('no-duplicates',full-{'duplicate-a','duplicate-b'},'test union of individually removable reminders'),('no-conflict-a',full-{'conflict-a'},'conditional conflict A removal'),('no-conflict-b',full-{'conflict-b'},'conditional conflict B removal'),('no-conflicts',full-{'conflict-a','conflict-b'},'paired compensating-cue removal'),('selected',{'contract','duplicate-a'},'combined task-faithful reduction'),('contract-only',{'contract'},'check selected survivor reminder removal')]
write(OUT/'simplification-search-plan.json',[{'label':label,'config':configuration('new-fixture',sorted(units)),'parent':'full' if label!='full' else None,'hypothesis':hypothesis,'removed':sorted(full-units)} for label,units,hypothesis in schedule])
experiment=Experiment(OUT/'simplification',limit=117,confirmation_reserve=8)
comparisons={}
for label,units,hypothesis in schedule:
    conf=configuration('new-fixture',sorted(units))
    experiment.measure(label,conf)
    (OUT/'simplification/candidates'/f'{label}.prompt.txt').write_text(render(conf))
    if label!='full': comparisons[label]=experiment.compare('full',label)
assert comparisons['selected']['admissible']
fullconf=configuration('new-fixture',sorted(full)); selectedconf=configuration('new-fixture',['contract','duplicate-a'])
experiment.freeze({'baseline-confirm':fullconf,'selected-confirm':selectedconf})
for label in ['baseline-confirm','selected-confirm']:
    experiment.confirm(label)
experiment.finish()
experiment.verify()
comparisons['confirmation']=experiment.compare('baseline-confirm','selected-confirm')
assert comparisons['confirmation']['admissible']
write(OUT/'simplification/comparisons.json',comparisons)
(OUT/'simplification/selected.prompt.txt').write_text(render(selectedconf))
(OUT/'simplification/original.prompt.txt').write_text(render(fullconf))
(OUT/'simplification/selected.diff').write_text(''.join(difflib.unified_diff(render(fullconf).splitlines(True),render(selectedconf).splitlines(True),fromfile='original-new-fixture.prompt',tofile='selected-new-fixture.prompt')))
write(OUT/'simplification/selected-bundle.json',{'config':selectedconf,'model_implementation':'local deterministic Python stand-in, exact candidate.py in selected-confirm native run','context':'protected complete evals/rubric.md via render; no retrieval/tools','inference':'no stochastic/provider inference; one fresh native subprocess per case','parser':'evaluate.py JSON structural validation and deterministic state grading','fallback':'none added','native_source_identity':evaluate.identity(),'prompt_utf8_bytes':len(render(selectedconf).encode('utf-8')),'original_prompt_utf8_bytes':len(render(fullconf).encode('utf-8')),'production_model_cells_A_B':'unavailable, not run','claims':'finite exposed new-model reduction only; no model-upgrade causality or production migration/release support'})
usage={'native_limit':120,'native_case_attempts':controls.reserved+experiment.runs.reserved,'native_completed':sum(c['executed'] for c in controls.calls)+sum(c['executed'] for c in experiment.runs.calls),'approved_case_controls':3,'ablation_development':88,'reserved_confirmation_completed':8,'remaining':120-controls.reserved-experiment.runs.reserved,'proxy_subprocess_calls':3,'judge_provider_calls':0,'judge_normalizer_calls':2,'judge_pairs':4,'malformed_controls':1,'old_backend_executions':0,'model_cost':None,'model_latency':None,'input_output_reasoning_tokens':None,'prompt_byte_savings':len(render(fullconf).encode())-len(render(selectedconf).encode())}
assert usage['native_case_attempts']==usage['native_completed']==99
write(OUT/'usage.json',usage)
lines=['# Combined confirmation exercise','', 'Fresh exposed synthetic controls; no human outcome labels, production data, provider calls or new dependencies. Installed Bootstrap, Create Eval, Adversarial Cases, Run Eval, Calibrate Judge, Ablation and Bitter Lesson guided this run. Independent scenario/intent review was unavailable; formal audit adjudication remains unreviewed.','', 'The exact scripted rich-state request was authored in `approved-native.jsonl` and checked against `source-expectation.json`: unchanged nested blue-ticket metadata, closed red ticket, counter 31 and settings false. The urgency variant is unapproved and unscored.','', 'Actual native subprocess controls: legitimate PASS; alternative unique ID PASS; false creation claim FAIL. All three are accepted by the intentionally defective action-only proxy. The false claim retained the whole original state and appended zero tickets; native ticket_delta, new_ticket_membership and action_matches_mutation rejected it. This is an observed proxy discrepancy, not independently adjudicated audit evidence.','', 'Judge helpers: malformed Choice distribution (sum 1.6) returned ERROR and zero decided coverage on its one attempted row. Four all-PASS pairs had 100% raw agreement/coverage; kappa is undefined because expected disagreement is zero. Failure-catch/false-pass-among-failure rates are undefined because no gold failures exist. Combined coverage is 4/5, with the error retained. Whole-family bootstrap retains undefined kappa replicates. Noul .1 normalized to P(failure)=.1 despite confidence .99. Confidence concentration is not correctness probability; synthetic probabilities and labels do not establish calibration. No live fitting or release threshold was authorized.','', 'Only new-fixture ran. Fixed original baseline: all nine prompt units. Selected reduction: contract plus duplicate-a. All eleven development configurations, exact retained/removed sets, hypotheses, candidates and actual traces are preserved; every gate uses original full baseline. Removing either duplicate reminder individually passes, their union fails; individual conflict-cue removal fails, paired removal passes. The executed combined reduction passes the finite development and frozen confirmation gates. Contract-only fails the duplicate slice. This is the smallest confirmed candidate found under the declared finite search, without a global-minimum claim.','', f'Prompt bytes: {len(render(fullconf).encode())} -> {len(render(selectedconf).encode())} rendered UTF-8 bytes; {usage["prompt_byte_savings"]} bytes saved. Model monetary cost, model latency and token usage were not measured. Native host wall time is logged separately and is not model latency.','', 'Development: baseline and selected each 8/8; confirmation: exact configurations frozen before execution, baseline and selected each 4/4 with no observed regressions/errors. Confirmation cases are readable exposed synthetic controls, not unseen evidence or statistical population non-inferiority.','', 'Missing migration cells: old production model with full design (A) and same reduced design (B). C=new/full versus D=new/reduced supports this finite new-model ablation only. C-A, D-A, B-A and interaction are unavailable. The experiment cannot establish that an upgrade enabled reduction, parity with the old production bar or readiness for production migration/release. No production action occurred.','', f'Usage: {usage["native_completed"]}/120 native cases (3 authoring controls, 88 ablation development, 8 confirmation); 3 local proxy calls; 2 normalizer calls; 4 synthetic paired label rows; zero provider/old-backend calls. The simplification ledger limit was 117 with 8 reserved confirmation cases; all planned confirmations completed and fitting is closed.','', 'Replay: from the workspace run `python3 eval-runs/skill-exercise/execute.py` only into a fresh output location/workspace because evidence paths refuse overwrite. Individual native runs are replayable with `python3 evaluate.py run --candidate <candidate.py> --cases <cases.jsonl> --suite all --out <fresh-directory>`. `manifest.json` records source, installed skill and artifact hashes.']
(OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
# Verify all completed evidence using native evidence check, not summary-only claims.
for call in controls.calls: evaluate.checked_run(controls.directory/call['label'])
experiment.verify()
manifest={'schema_version':1,'task_sha256':evaluate.digest(OUT/'task-source.md'),'workspace':str(ROOT),'source_checkout':str(ROOT.parents[1]/'shortened-candidate'),'native_identity':evaluate.identity(),'skills_lock_sha256':evaluate.digest(ROOT/'cstack-skills.lock.json'),'installed_skills':{name:evaluate.digest(ROOT/'.agents/skills'/name/'SKILL.md') for name in ['bootstrap','create-eval','adversarial-cases','run-eval','calibrate-judge','ablation','bitter-lesson']},'usage':usage,'formal_independent_audit_adjudication':'unreviewed','artifacts':{str(p.relative_to(OUT)):evaluate.digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p != OUT/'manifest.json'}}
write(OUT/'manifest.json',manifest)
print(json.dumps({'out':str(OUT),'usage':usage,'native_control_outcomes':{r['candidate']:r['native_outcome'] for r in observations},'comparisons':comparisons,'prompt_bytes':{'original':len(render(fullconf).encode()),'selected':len(render(selectedconf).encode())}},indent=2))
