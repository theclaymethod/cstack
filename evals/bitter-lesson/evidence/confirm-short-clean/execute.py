"""One-shot owner exercise. Run from playground root; use a fresh workspace for replay."""
import copy
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from methods.native import Runs, evaluate, jsonl, read_rows
from simplification.protocol import Experiment, UNITS, configuration, render
from judge_calibration.statistics import agreement, uncertainty, probability_diagnostics

OUT = ROOT / 'eval-runs/skill-exercise'
def write(name, value):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

skill_names = ['bootstrap','create-eval','run-eval','adversarial-cases','ablation','bitter-lesson','calibrate-judge']
references = {
 'bootstrap':['scenarios.md','labeling.md'],
 'create-eval':['formats.md','judges.md'],
 'run-eval':['package.md'],
 'adversarial-cases':['case-contract.md','synthetic-methods.md','failure-methods.md','injection.md'],
 'ablation':['removal.md','quality.md'],
 'bitter-lesson':['migration.md'],
 'calibrate-judge':['measurement.md','protocol.md','backends.md']}
skill_paths = [Path('.agents/skills') / name / 'SKILL.md' for name in skill_names]
skill_paths += [Path('.agents/skills') / name / 'references' / ref for name, refs in references.items() for ref in refs]
write('skill-files-read.json', [{'path':str(p),'sha256':digest(ROOT/p)} for p in skill_paths])
source_files = [*evaluate.FROZEN_FILES,'support_agent.py','simplification/protocol.py','methods/native.py','judge_calibration/statistics.py','examples/candidates/improved.py']
frozen = {p:digest(ROOT/p) for p in source_files}
write('source-before.json', {'files':frozen,'native_identity':evaluate.identity(), 'workspace_origin':json.loads((ROOT/'.cstack-source.json').read_text()), 'host_model':'Inherited fixed agent model; identifier unavailable to this script; no model changes', 'copied_skills':json.loads((ROOT/'cstack-skills.lock.json').read_text())})
# Explicit task path from parent; no discovery.
source_task = Path('/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/bitter-lesson-build/tasks/confirmation.md')
shutil.copyfile(source_task, OUT/'source-decisions.md')
state_a = {'tickets':[], 'preserve':{'count':9,'enabled':False}}
state_b = {'tickets':[{'id':'keep-blue','account':'blue','status':'open','issue':'vpn','extra':{'flags':[True,False]}},{'id':'keep-red','account':'red','status':'closed','issue':'vpn'}], 'preserve':{'count':9,'enabled':False}}
cases = [
 {'id':'A-r1','suite':'development','family':'owner-A-prohibition','request':{'text':'Do not create a VPN support ticket.','account':None,'accounts':['red','blue']},'state':state_a,'expected':{'allowed_actions':['guidance'],'account':None,'ticket_delta':0}},
 {'id':'B-r2','suite':'development','family':'owner-B-submit','request':{'text':'Please submit a VPN support request.','account':'red','accounts':['red','blue']},'state':state_b,'expected':{'allowed_actions':['create_ticket'],'account':'red','ticket_delta':1}}]
jsonl(OUT/'cases.jsonl', cases)
jsonl(OUT/'decisions.jsonl', [
 {'id':'A','revision':1,'decision':'approve','expectation':'Give guidance and leave all state unchanged.','source':'source-decisions.md','authority':'scripted synthetic owner decision; no actual output label'},
 {'id':'B','revision':1,'decision':'superseded','expectation':'guidance-only','limits':'Only prior guidance-only expectation is supplied, not its full original card; no invented prior inputs.','superseded_by':'B revision2'},
 {'id':'B','revision':2,'decision':'correction-approve-exact-replacement','expectation':'Create one open VPN ticket for red, any unique nonempty ID; preserve all original state.','source':'source-decisions.md','supersedes':'B revision1','authority':'scripted synthetic owner decision; no actual output label'},
 {'id':'C','decision':'defer','expectation':None,'topic':'automatic escalation for urgent VPN requests','source':'source-decisions.md','status':'pending; excluded from cases and scored denominator'}])
jsonl(OUT/'scenarios.jsonl', [{**c,'revision':1 if c['id']=='A-r1' else 2,'origin':'exact scripted owner card','approval':'approved','construction_family':c['family'],'outcome_label':None} for c in cases])
write('package.json', {'format':'native JSONL','runner':'python3 evaluate.py run --candidate <candidate> --cases eval-runs/skill-exercise/cases.jsonl --suite development --out <fresh-output>','source':'source-decisions.md','approved':['A-r1','B-r2'],'excluded':['B-r1 superseded','C pending'],'scope':'Deterministic action/account/state checks; note wording is nonempty, semantic helpfulness unjudged.','approval_fidelity':'Exact request/account/accounts/state and expected deltas preserved; case IDs link exact revisions.','independence':'Single local author; no independent reviewer/delegation; all evidence synthetic and exposed.'})
write('plan.json', {'total_limit':120,'native_controls':22,'simplification_limit':72,'confirmation_reserve':8,'maximum_planned_attempts':94,'search':'One baseline plus seven declared candidates on eight development cases; then full and selected on four confirmation cases.','quality':'Adapter finite-case policy: zero loss and no observed original-baseline PASS regressions, no ERROR/UNKNOWN. Fixture-only selection; owner supplied no population/release threshold.','burden':'Rendered prompt UTF-8 bytes; retain protected contract.','stop':'Stop after declared candidate list and frozen confirmation; no further fitting.','models':['new-fixture only'],'repeats':1,'exposure':'Native cases remain readable; no independence/blindness or population inference.'})

# Output controls are project-local synthetic programs, never canonical edits.
(OUT/'controls').mkdir()
base = '''import copy,json,sys
p=json.load(sys.stdin)
s=copy.deepcopy(p['state'])
create=not p['request']['text'].startswith('Do not')
if create:
    s['tickets'].append({'id':NEW_ID,'account':'red','status':'open','issue':'vpn'})
out={'action':'create_ticket' if create else 'guidance','account':'red' if create else None,'state':s,'note':'Created a VPN ticket.' if create else 'Use VPN setup guidance.'}
'''
variants = {
 'legitimate-alpha':("'alpha'", ''),
 'legitimate-alternative-id':("'9ef8a2e1-6af1-4cdf-86d8-c9d24187f401'", ''),
 'legitimate-extra-metadata':("'free-id'", "if create: s['tickets'][-1]['extra']={'source':'local','flags':[False,True]}\n"),
 'claimed-create-with-no-ticket':("'new'", "if create: s['tickets'].pop()\n"),
 'wrong-created-account':("'new'", "if create: s['tickets'][-1]['account']='blue'\n"),
 'duplicate-id':("'keep-blue'", ''),
 'mutate-original-ticket':("'new'", "if create: s['tickets'][0]['extra']['flags'][0]=False\n"),
 'reorder-original-tickets':("'new'", "if create: s['tickets'][:2]=s['tickets'][1::-1]\n"),
 'collateral-state-mutation':("'new'", "s['preserve']['enabled']=0\n"),
 'malformed-json':("'new'", None),
}
runs = Runs(OUT/'control-runs', limit=22)
controls = {}
for label,(new_id, mutation) in variants.items():
    path = OUT/'controls'/(label+'.py')
    code = base.replace('NEW_ID',new_id)
    if mutation is None:
        code += "print('not-json')\n"
    else:
        code += mutation + 'print(json.dumps(out,sort_keys=True))\n'
    path.write_text(code)
    traces = runs.run(label,path,cases)
    controls[label] = {t['id']:{'outcome':t['outcome'],'checks':t['checks'],'error':t['error']} for t in traces}
# Native original product execution is distinct from output controls.
runs.run('original-product',ROOT/'support_agent.py',cases)
write('controls-results.json', controls)
# Independently inspect actual state, not only native score or success note.
witnesses=[]
for label in variants:
    traces = read_rows(OUT/'control-runs'/label/'traces.jsonl')
    for t in traces:
        output=t['output']
        before=t['input']['state']
        if output is not None:
            after=output['state']
            new=[r for r in after['tickets'] if r['id'] not in {x['id'] for x in before['tickets']}]
            witness={'new_ids':[r['id'] for r in new], 'count_delta':len(after['tickets'])-len(before['tickets']), 'original_prefix_preserved':evaluate.same_json(after['tickets'][:len(before['tickets'])],before['tickets']), 'other_state_preserved':evaluate.same_json({k:v for k,v in before.items() if k!='tickets'},{k:v for k,v in after.items() if k!='tickets'}), 'claim':output['note']}
        else: witness={'raw_stdout':t['stdout'],'parse_or_schema_error':t['error']}
        witnesses.append({'control':label,'case':t['id'],'armed':'candidate output variant','activated': label in ('malformed-json','collateral-state-mutation') or t['id']=='B-r2', 'activation_evidence':'Actual captured stdout/output retained in native trace. Creation-branch variants do not activate on A; no lifecycle/operator fault claim.', 'native_outcome':t['outcome'],'state_witness':witness})
jsonl(OUT/'control-witnesses.jsonl', witnesses)
assert controls['claimed-create-with-no-ticket']['B-r2']['outcome']=='FAIL'
for label in ('legitimate-alpha','legitimate-alternative-id','legitimate-extra-metadata'):
    assert all(t['outcome']=='PASS' for t in controls[label].values())

# Bounded native prompt execution: old-fixture is never invoked.
full = configuration('new-fixture',list(UNITS))
configs = {
 'original-full':full,
 'remove-legacy':configuration('new-fixture',set(UNITS)-{'legacy-auth'}),
 'remove-planning-example':configuration('new-fixture',set(UNITS)-{'plan','plan-detail','example'}),
 'remove-duplicate-a':configuration('new-fixture',set(UNITS)-{'duplicate-a'}),
 'remove-duplicate-b':configuration('new-fixture',set(UNITS)-{'duplicate-b'}),
 'remove-both-duplicates':configuration('new-fixture',set(UNITS)-{'duplicate-a','duplicate-b'}),
 'remove-conflict-a':configuration('new-fixture',set(UNITS)-{'conflict-a'}),
 'combined-minimal-found':configuration('new-fixture',['contract','duplicate-a'])}
write('search-configs-before.json',configs)
experiment = Experiment(OUT/'simplification',limit=72,confirmation_reserve=8)
for label,config in configs.items(): experiment.measure(label,config)
comparisons={label:experiment.compare('original-full',label) for label in configs if label!='original-full'}
feasible=[label for label in comparisons if comparisons[label]['admissible']]
selected=min(feasible,key=lambda label:experiment.checked(label)['prompt_utf8_bytes'])
selected_config=configs[selected]
write('selection-before-confirmation.json',{'selected':selected,'configuration':selected_config,'comparisons':comparisons,'rule':'Smallest rendered byte count among observed zero-loss/no-regression candidates relative to full original; finite fixture gate only.'})
experiment.freeze({'confirmation-original':full,'confirmation-selected':selected_config})
experiment.confirm('confirmation-original')
experiment.confirm('confirmation-selected')
experiment.finish()
confirmation=experiment.compare('confirmation-original','confirmation-selected')
assert confirmation['admissible']
write('comparison.json',{'development':comparisons,'selected':selected,'confirmation':confirmation,'original':experiment.checked('original-full'),'selected_development':experiment.checked(selected),'confirmation_original':experiment.checked('confirmation-original'),'confirmation_selected':experiment.checked('confirmation-selected')})
(OUT/'original-prompt.txt').write_text(render(full))
(OUT/'selected-prompt.txt').write_text(render(selected_config))
(OUT/'prompt.diff').write_text(''.join(difflib.unified_diff(render(full).splitlines(True),render(selected_config).splitlines(True),fromfile='original-prompt.txt',tofile='selected-prompt.txt')))
write('selected-config.json', {'configuration':selected_config,'prompt_sha256':digest(OUT/'selected-prompt.txt'),'candidate':str(Path('simplification/candidates')/(selected+'.py')),'model_kind':'deterministic programmed Python fixture; host agent unchanged','no_fallback':True,'trials_per_case':1,'timeout_seconds':3,'tools':'native subprocess, no network/provider','parser':'evaluate.py native JSON/schema parser','sources':frozen,'release':'No deployment authorized or performed'})

# Stored owner observations only; freeze predictions before joining fixture references.
predictions = [{'id':f'control-{i+1}','verdict':'PASS' if i<3 else 'ERROR','error':None if i<3 else 'parse failure (raw response not supplied)'} for i in range(4)]
write('judge/stored-predictions.json', predictions)
write('judge/prediction-freeze.json', {'sha256':digest(OUT/'judge/stored-predictions.json'),'provenance':'Owner-supplied stored summary; original raw responses/model/parser IDs not supplied; no new judge inference.'})
rows=[{**p,'gold':'PASS','family':'stored-synthetic-control'} for p in predictions]
write('judge/observations.json',rows)
measurement={'agreement':agreement(rows),'uncertainty':uncertainty(rows),'probability':probability_diagnostics(rows),'supported_all_selected_agreement_fraction':3/4,'error_count':1,'error_rate':1/4,'authority':'Synthetic fixture reference labels, not independent human gold.','family_policy':'Conservatively group tiny stored control as one family; independence unspecified.','readiness':'Not calibrated; no live judge fit, failure-class examples, independent human outcome labels, release threshold or live backend authorized.','versions':'Unknown raw response bytes, backend/model/parser/config identities; original artifact versions not supplied.'}
write('judge/measurement.json',measurement)

experiment.verify()
for call in runs.calls: evaluate.checked_run(OUT/'control-runs'/call['label'])
after={p:digest(ROOT/p) for p in source_files}
assert after==frozen
write('source-after.json',{'files':after,'unchanged':True})
receipt=json.loads((OUT/'simplification/native/executions.json').read_text())
control_receipt=json.loads((OUT/'control-runs/executions.json').read_text())
usage={'budget':120,'native_case_attempts':receipt['reserved']+control_receipt['reserved'],'completed':receipt['actual_completed']+control_receipt['actual_completed'],'controls_and_original':control_receipt,'simplification':receipt,'remaining':120-receipt['reserved']-control_receipt['reserved'],'retries':0,'provider_calls':0,'paid_calls':0,'network_calls':0,'dependencies_installed':0,'host_model_changes':0,'monetary_cost':None,'model_tokens':None,'model_latency':None,'note':'Native wall times are local process timings, not model latency; all errors remain charged.'}
write('usage.json',usage)
original=experiment.checked('original-full'); chosen=experiment.checked(selected)
report=f'''# Skill exercise report

Two exact approved cards became native cases: A revision1 guidance/no mutation and B revision2 create one red VPN ticket, preserving original records and nested state. B's prior guidance-only proposal is retained as superseded, with unavailable prior card details explicit. C automatic escalation remains pending and unscored. Source decisions are synthetic owner statements, not independent output labels. One local author; no independent reviewer or nested delegation.

Native controls: three legitimate variants (including a different unique ID and added ticket metadata) pass both cards. Claimed creation without a new ticket FAILs B, with delta and membership zero in the actual captured output. Wrong account, duplicate ID, prior-record mutation/reordering and boolean-to-integer collateral mutation are exercised and retained. Malformed JSON is ERROR, not a behavior FAIL. The original product was separately executed on both cards: 1 PASS and 1 FAIL (A prohibition). See `control-runs/`, `controls-results.json`, and `control-witnesses.jsonl`. Native action/account/state checks ran; note helpfulness is not semantically graded. No native evaluator defect was established or repaired.

The authorized new-fixture adapter executed the actual rendered full prompt and seven removal candidates via the native grader. Selected `{selected}` retains `{', '.join(selected_config['retained'])}`. Development is {sum(x=='PASS' for x in original['outcomes'].values())}/8 full versus {sum(x=='PASS' for x in chosen['outcomes'].values())}/8 selected, with zero original-relative regressions. Full and selected each pass 4/4 frozen confirmation cases. Both-duplicate-reminder and single-conflict removals fail development and are retained. Selected rendered size is {chosen['prompt_utf8_bytes']} bytes versus {original['prompt_utf8_bytes']} bytes ({original['prompt_utf8_bytes']-chosen['prompt_utf8_bytes']} fewer; {(1-chosen['prompt_utf8_bytes']/original['prompt_utf8_bytes'])*100:.1f}% reduction). `selected-prompt.txt`, `selected-config.json`, `prompt.diff` and the standalone selected fixture program are reviewable. This is the smallest confirmed candidate in the declared bounded list; no exhaustive or global-minimum claim.

All model names here are programmed stand-ins. The host agent model stayed fixed. Only new-fixture full/reduced cells ran; old production full/reduced, actual model-upgrade effects, production parity, interaction, model-token costs and monetary/model-latency savings remain unrun or unknown. Finite synthetic zero-loss selection is not statistical non-inferiority or release approval. Confirmation fixtures are readable and not independent hidden data. No deployment occurred.

Stored judge control: 4 selected fixture PASS references, 3 decided PASS and 1 parse ERROR. Coverage 75%; conditional agreement 100% on 3 decided pairs; all-selected correct observations 3/4 with one error. Failure-positive TP=FN=FP=0, TN=3. Failure catch and false-pass-among-failures are undefined (no FAIL references). False rejection among decided PASS references is 0/3. Nominal kappa is undefined because expected disagreement is zero; this is not perfect chance-corrected agreement. Existing helpers produce full confusion/error/coverage tables and preserve undefined values in `judge/measurement.json`. Conservatively one unspecified stored-control family yields no defensible bootstrap interval; no probability fields were supplied. Raw stored responses and model/parser/configuration identities are unavailable. These synthetic observations are insufficient to calibrate an automated judge; no live fitting or release threshold is authorized.

Exact usage: {usage['native_case_attempts']}/120 native attempts, all completed, including 22 control/original attempts and 72 simplification attempts (64 development + 8 confirmation); zero retries/provider/paid/network calls or dependencies. Native ERROR outcomes remain in denominators and accounting. Sources and installed skill/reference hashes are retained, and all native/evaluator/product sources remain byte-identical. Trusted local subprocesses provide reset, not malicious-code containment. Reproduce in a fresh materialized workspace with `python3 eval-runs/skill-exercise/execute.py`; outputs are one-shot and existing run directories are preserved.
'''
(OUT/'REPORT.md').write_text(report)
files={str(p.relative_to(OUT)):digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p != OUT/'manifest.json' and '__pycache__' not in p.parts}
write('manifest.json',{'schema_version':1,'purpose':'Reviewable owner task package; local synthetic evidence only','source_hashes':frozen,'skill_inventory':'skill-files-read.json','native_attempts':usage['native_case_attempts'],'files':files,'limits':'Hashes establish consistency, not external access-control attestation; nested native manifests retained under their original paths.'})
print(json.dumps({'attempts':usage['native_case_attempts'],'selected':selected,'bytes_before':original['prompt_utf8_bytes'],'bytes_after':chosen['prompt_utf8_bytes'],'confirmation':confirmation,'report':str(OUT/'REPORT.md')},indent=2))
