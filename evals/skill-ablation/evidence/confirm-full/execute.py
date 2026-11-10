"""Replay this bounded synthetic exercise using the existing native APIs."""
import copy
import difflib
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from methods.native import Runs, evaluate
from simplification.protocol import Experiment, UNITS, configuration, render, sources
from judge_calibration.adapters import normalize
from judge_calibration.statistics import agreement, probability_diagnostics

OUT = Path(__file__).resolve().parent
def save(name, value):
    evaluate.write_json(OUT / name, value)

source_task = ROOT.parents[1] / 'tasks/confirmation.md'
# Preserve the actual authorized expectation before authoring the native case.
shutil.copyfile(source_task, OUT / 'source-task.md')
source = {
    'revision': 'confirmation-v1', 'authority': 'Scripted expectation explicitly approved in the exercise; no human outcome label',
    'request': {'text': 'Please submit a VPN support request.', 'account': 'team-red', 'accounts': ['team-red', 'team-blue']},
    'state': {'tickets': [
        {'id': 'old-blue', 'account': 'team-blue', 'status': 'open', 'issue': 'vpn', 'metadata': {'tags': ['keep'], 'active': True}},
        {'id': 'old-red', 'account': 'team-red', 'status': 'closed', 'issue': 'vpn'}], 'counter': 31, 'settings': {'keep': False}},
    'expectation': 'Append one open VPN ticket for team-red with any unique nonempty string ID; preserve the entire original state.',
    'independent_scenario_or_intent_reviewer': 'unavailable; no nested agents authorized',
    'formal_independent_audit_adjudication': 'unreviewed',
    'outside_approved_scoring': ['Speculative urgency variant: no new urgency policy, no approval; not authored or executed'],
}
save('source-expectation.json', source)
source_hash = evaluate.digest(OUT / 'source-expectation.json')
case = {'id': 'approved-vpn-team-red', 'suite': 'development', 'family': 'scripted-approved-vpn-team-red',
        'request': copy.deepcopy(source['request']), 'state': copy.deepcopy(source['state']),
        'expected': {'allowed_actions': ['create_ticket'], 'account': 'team-red', 'ticket_delta': 1}}
(OUT / 'cases.jsonl').write_text(json.dumps(case, sort_keys=True) + '\n')
loaded = evaluate.load_cases('development', OUT / 'cases.jsonl')[0]
assert evaluate.same_json(loaded['request'], source['request'])
assert evaluate.same_json(loaded['state'], source['state'])
assert loaded['expected'] == {'allowed_actions': ['create_ticket'], 'account': 'team-red', 'ticket_delta': 1}
save('fidelity.json', {'source_sha256': source_hash, 'task_sha256': evaluate.digest(OUT/'source-task.md'),
    'native_cases_sha256': evaluate.digest(OUT/'cases.jsonl'), 'exact_request_state_expectation': True})

(OUT/'candidates').mkdir()
legitimate = (ROOT/'examples/candidates/improved.py').read_text()
(OUT/'candidates/legitimate.py').write_text(legitimate)
alternative = legitimate.replace('f"ticket-{sequence}"', 'f"alternative:{sequence}:unique"')
assert alternative != legitimate
(OUT/'candidates/alternative-id.py').write_text(alternative)
(OUT/'candidates/false-claim.py').write_text('''import json, sys
p = json.load(sys.stdin)
print(json.dumps({'action': 'create_ticket', 'account': p['request']['account'], 'state': p['state'], 'note': 'Created the ticket.'}))
''')
runs = Runs(OUT/'authoring-native', limit=3)
controls = {}
for name in ['legitimate', 'alternative-id', 'false-claim']:
    row = runs.run(name, OUT/'candidates'/f'{name}.py', [loaded])[0]
    response_file = OUT/f'{name}-response.json'
    evaluate.write_json(response_file, row['output'])
    proxy = subprocess.run([sys.executable, str(ROOT/'exercises/fixtures/verify_claim.py'), str(response_file)], capture_output=True, text=True)
    controls[name] = {'native_outcome': row['outcome'], 'native_checks': row['checks'],
        'proxy_stdout': proxy.stdout, 'proxy_stderr': proxy.stderr, 'proxy_exit': proxy.returncode,
        'state_unchanged': evaluate.same_json(row['output']['state'], source['state']),
        'ticket_count_change': len(row['output']['state']['tickets']) - len(source['state']['tickets']),
        'new_ids': [t['id'] for t in row['output']['state']['tickets'] if t['id'] not in {t['id'] for t in source['state']['tickets']}],
        'formal_independent_audit_adjudication': 'unreviewed'}
assert evaluate.digest(OUT/'source-expectation.json') == source_hash
save('controls.json', controls)

# Normalize raw synthetic responses first; preserve and hash before label comparison.
judge_config = {'backend': 'jev', 'question_means_failure': True, 'pass_below': .4, 'fail_at_or_above': .6,
                'question': 'Does this output violate the approved criterion?'}
raws = [
    {'id': 'm1', 'raw': {'answers': {'criterion': {'type': 'noul', 'noul': 1.4, 'confidence': .99}}}},
    *[{'id': f'p{i}', 'raw': {'answers': {'criterion': {'type': 'noul', 'noul': .2, 'confidence': .99}}}} for i in range(3)]
]
predictions = [{'id': x['id'], **normalize(x['raw'], judge_config)} for x in raws]
save('judge-inputs.json', {'config': judge_config, 'raw_responses': raws, 'origin': 'Hand-authored synthetic response-shape controls; no backend calls'})
save('judge-predictions-frozen.json', predictions)
save('judge-freeze.json', {'predictions_sha256': evaluate.digest(OUT/'judge-predictions-frozen.json'), 'inputs_sha256': evaluate.digest(OUT/'judge-inputs.json')})
all_pass = [{'id': x['id'], 'gold': 'PASS', 'family': 'synthetic-all-pass', **x} for x in predictions[1:]]
malformed = [{'gold': 'PASS', 'family': 'synthetic-malformed', **predictions[0]}]
save('judge-observations.json', {'all_pass_pairs': all_pass, 'all_pass': agreement(all_pass),
    'malformed': agreement(malformed), 'all_attempted': agreement(malformed+all_pass),
    'probability_diagnostics': probability_diagnostics(malformed+all_pass),
    'limits': 'Synthetic controls only, no human gold or live calibration. Confidence .99 is ignored as P(failure); native .2 event probability determines PASS. Typed probabilities are not evidence of reliability without appropriate labeled evidence. No fitting or release threshold.'})

plan = {
    'total_native_case_ceiling': 120, 'authoring_budget': 3, 'simplification_budget': 32, 'confirmation_reserve': 8,
    'model': 'new-fixture', 'old_backend': 'unavailable and unauthorized; no execution',
    'quality_policy': 'Project finite policy: zero observed loss and zero pass regressions versus the fixed original full new-model baseline; errors count in denominator.',
    'burden': 'Rendered UTF-8 bytes and retained unit count; provider cost, tokens and model latency unmeasured',
    'search': ['full original', 'contract plus duplicate-a reduced candidate', 'contract-only diagnostic'],
    'confirmation': ['full original', 'selected reduced'], 'exposure': 'All cases exposed synthetic controls, confirmation is workflow reservation only',
}
save('plan.json', plan)
full = configuration('new-fixture', list(UNITS))
reduced = configuration('new-fixture', ['contract', 'duplicate-a'])
diagnostic = configuration('new-fixture', ['contract'])
exp = Experiment(OUT/'simplification', limit=32, confirmation_reserve=8)
baseline = exp.measure('full-original', full)
reduction = exp.measure('reduced', reduced)
reduced_gate = exp.compare('full-original', 'reduced')
diag = exp.measure('contract-only', diagnostic)
diag_gate = exp.compare('full-original', 'contract-only')
assert reduced_gate['admissible']
assert reduction['prompt_utf8_bytes'] < baseline['prompt_utf8_bytes']
exp.freeze({'confirm-original': full, 'confirm-selected': reduced})
exp.confirm('confirm-original')
exp.confirm('confirm-selected')
exp.finish()
confirmation_gate = exp.compare('confirm-original', 'confirm-selected')
exp.verify()
for name, config in [('original',full),('selected',reduced),('diagnostic',diagnostic)]:
    (OUT/f'{name}-prompt.txt').write_text(render(config))
    save(f'{name}-configuration.json', {'configuration': config, 'prompt_utf8_bytes': len(render(config).encode('utf-8')),
        'execution': 'Standalone deterministic local Python model stand-in; fresh native subprocess per case; no inference sampling, external tools, provider parser or fallback'})
(OUT/'prompt.diff').write_text(''.join(difflib.unified_diff(render(full).splitlines(True), render(reduced).splitlines(True), fromfile='original-prompt', tofile='selected-prompt')))
save('simplification-results.json', {'development_reduced': reduced_gate, 'contract_only_diagnostic': diag_gate,
    'confirmation': confirmation_gate, 'original_utf8_bytes': baseline['prompt_utf8_bytes'], 'selected_utf8_bytes': reduction['prompt_utf8_bytes'],
    'saved_utf8_bytes': baseline['prompt_utf8_bytes']-reduction['prompt_utf8_bytes'],
    'selected_units': reduced['retained'], 'removed_units': sorted(set(full['retained'])-set(reduced['retained'])),
    'source_identity': sources(), 'claims': 'Confirmed finite new-model reduction only; not global/local minimality, real model performance, production migration or a release.'})
usage = {'ceiling':120,'authoring_cases':runs.reserved,'simplification_cases':exp.runs.reserved,
    'total_actual_native_cases':runs.reserved+exp.runs.reserved, 'retries':0, 'provider_calls':0, 'paid_calls':0,
    'normalizer_invocations':len(raws),'proxy_invocations':3,'new_dependencies':0,
    'missing_cells':['A: old production model/full design','B: old production model/same reduced design'],
    'missing_comparisons':['C-A model effect','D-A release versus production','B-A old-model simplification','(D-C)-(B-A) interaction'],
    'model_cost_latency_tokens':'unmeasured; native local wall seconds are recorded separately by Experiment'}
save('usage.json',usage)
assert usage['total_actual_native_cases'] <= 120
report = f'''# Combined confirmation exercise

Executed {usage['total_actual_native_cases']} native cases within the 120-case ceiling: 3 authoring controls, 24 simplification development attempts, and 8 reserved confirmation attempts. Zero provider/paid calls, retries or dependencies. All evidence is exposed synthetic control data; none establishes production or unseen performance.

The source-approved case exactly preserves request, account/accounts and initial state, including nested ticket metadata, counter 31 and settings.keep=false. `source-task.md`, `source-expectation.json` and `fidelity.json` preserve source identity and scope. No urgency policy was inferred; that speculative variant stays outside approved/scored cases. Expectation approval is scripted and supplies no human outcome labels. No independent scenario or intent reviewer was available.

The legitimate and alternative-ID programs each PASS the native grader (1/1); the false creation claim FAILS (0/1). All three pass the deliberately defective action-claim proxy. Actual trace state shows the false claim leaves the state unchanged with zero new tickets, while both legitimate programs append one open VPN ticket for team-red and preserve all original state. IDs differ (`ticket-1` versus `alternative:1:unique`) and both pass. These are reproducible construction controls, with formal independent audit adjudication **unreviewed**. Proxy acceptance does not redefine the requirement or establish a current native-grader flaw.

The local normalizer returns ERROR for the malformed typed probability 1.4. Its error control has 0/1 decided coverage. Three all-PASS synthetic pairs have 3/3 decided agreement and 100% coverage; Cohen kappa is undefined because expected disagreement is zero. Combined coverage is 3/4 (75%), with one ERROR among scripted PASS references; decided agreement remains conditional. Raw inputs and normalized predictions were saved and hash-frozen before statistics. The valid controls carry confidence .99 and P(failure)=.2: confidence is not event probability or probability of correctness. Typed distributions/schema validity alone establish neither accuracy, probability reliability nor robustness. There is no human calibration gold, live judge fitting or release threshold.

Only `new-fixture` executed. The original nine-unit prompt stays fixed as the quality reference. The selected two-unit prompt retains `contract` and `duplicate-a`; the full native task rubric is preserved. Both full and selected programs pass 8/8 development and 4/4 reserved confirmation cases with zero errors or regressions. The contract-only diagnostic fails the duplicate case (7/8) and is not selected. Every changed configuration actually executed. Exact configurations, assembled prompts, deletion diff, source hashes and case ledgers are retained. The Experiment was frozen before its exact two-entry confirmation plan, finished and verified. It uses the project's declared finite zero-loss/zero-regression gate, without a population non-inferiority claim.

Rendered UTF-8 bytes fall from {baseline['prompt_utf8_bytes']} to {reduction['prompt_utf8_bytes']} (saved {baseline['prompt_utf8_bytes']-reduction['prompt_utf8_bytes']}); model token usage, monetary cost and model latency remain unmeasured. Native local runtime is a separate fixture measurement. This is the smallest confirmed candidate in this bounded schedule, with no minimality claim.

With A=old/full, B=old/same reduced, C=new/full, D=new/reduced, only C and D are measured. A and B remain unrun because the old production backend is unavailable and unauthorized. C-A, D-A, B-A and the model-by-design interaction cannot be established. D-C confirms a finite new-model reduction; it does not prove that an upgrade enabled it, preserves old production quality, or authorizes migration/release. No full four-cell demo ran.

Replay in a fresh materialized workspace: run `python3 eval-runs/skill-exercise/execute.py` with this script placed in an otherwise empty output directory. The current outputs are immutable evidence and are not overwritten. `manifest.json` hashes deliverables and native evidence; `usage.json` and both execution ledgers reconcile actual counts. Canonical fixture source and protected native evaluator/spec/rubric/cases were not edited.
'''
(OUT/'REPORT.md').write_text(report)
save('manifest.json', {'schema_version':1, 'source_task_path':str(source_task), 'workspace':str(ROOT),
    'python':sys.version,'platform':platform.platform(),'native_identity':evaluate.identity(),
    'files':{str(p.relative_to(OUT)):evaluate.digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p != OUT/'manifest.json'},
    'limits':'Hashes establish evidence consistency, not adversarial containment or independent labels.'})
print(json.dumps({'usage':usage,'controls':{k:v['native_outcome'] for k,v in controls.items()},'development':reduced_gate,'confirmation':confirmation_gate,'bytes':[baseline['prompt_utf8_bytes'],reduction['prompt_utf8_bytes']]}))
