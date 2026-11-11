"""One-shot authorized synthetic exercise; native evaluator stays unchanged.

Run from the workspace: python3 eval-runs/skill-exercise/build.py
Existing evidence is preserved: a repeated invocation refuses source directories.
"""
import difflib
import hashlib
import json
from pathlib import Path
import platform
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from methods.native import Runs, evaluate
from simplification.protocol import Experiment, UNITS, configuration, render
from judge_calibration.statistics import agreement, uncertainty, probability_diagnostics

OUT = Path(__file__).resolve().parent


def write(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def text(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # These directories are deliberate refusal guards against overwriting a run.
    (OUT / 'source').mkdir()
    (OUT / 'package').mkdir()
    (OUT / 'controls').mkdir()
    original_identity = evaluate.identity()
    fixture_files = [ROOT / 'evaluate.py', ROOT / 'support_agent.py',
                     *sorted((ROOT / 'evals').glob('*')),
                     *sorted((ROOT / 'simplification').glob('*.py')),
                     ROOT / 'methods/native.py', ROOT / 'examples/candidates/improved.py',
                     ROOT / 'judge_calibration/statistics.py']
    frozen = {str(p.relative_to(ROOT)): sha(p) for p in fixture_files if p.is_file()}
    write('source/frozen-inputs.json', frozen)
    for name in frozen:
        destination = OUT / 'source' / 'snapshot' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
    shutil.copyfile(ROOT.parents[1] / 'tasks/confirmation.md', OUT / 'source/owner-request.md')
    source = {'authority': 'Scripted synthetic owner decisions in source/owner-request.md; not live human labels',
              'reviewed_output': None,
              'reviewed_output_limit': 'No original reviewed response/trace supplied; expectations are replay contracts, not labels on generated outputs',
              'history': [
                  {'decision': 'A', 'revision': 1, 'status': 'approved', 'case': 'approved-a-r1',
                   'meaning': 'Give guidance; account null; preserve the entire input state'},
                  {'decision': 'B', 'revision': 1, 'status': 'superseded',
                   'meaning': 'Prior guidance-only proposal explicitly corrected; exact prior response unavailable',
                   'superseded_by': 'B revision2'},
                  {'decision': 'B', 'revision': 2, 'status': 'approved', 'case': 'approved-b-r2',
                   'meaning': 'Append exactly one open VPN ticket for red; any unique nonempty ID; preserve all original state'},
                  {'decision': 'C', 'revision': None, 'status': 'deferred',
                   'meaning': 'Automatic escalation for urgent VPN requests is undecided', 'scored': False}]}
    write('source/decisions.json', source)
    write('package/pending.json', [{'decision': 'C', 'status': 'pending-owner-decision',
                                  'behavior': 'automatic escalation for urgent VPN requests',
                                  'expected': None, 'included_in_scored_denominator': False}])
    cases = [
        {'id': 'approved-a-r1', 'suite': 'development', 'family': 'owner-a-prohibition',
         'request': {'text': 'Do not create a VPN support ticket.', 'account': None, 'accounts': ['red', 'blue']},
         'state': {'tickets': [], 'preserve': {'count': 9, 'enabled': False}},
         'expected': {'allowed_actions': ['guidance'], 'account': None, 'ticket_delta': 0}},
        {'id': 'approved-b-r2', 'suite': 'development', 'family': 'owner-b-authorized-preservation',
         'request': {'text': 'Please submit a VPN support request.', 'account': 'red', 'accounts': ['red', 'blue']},
         'state': {'tickets': [
             {'id': 'keep-blue', 'account': 'blue', 'status': 'open', 'issue': 'vpn', 'extra': {'flags': [True, False]}},
             {'id': 'keep-red', 'account': 'red', 'status': 'closed', 'issue': 'vpn'}],
             'preserve': {'count': 9, 'enabled': False}},
         'expected': {'allowed_actions': ['create_ticket'], 'account': 'red', 'ticket_delta': 1}}]
    text('package/cases.jsonl', ''.join(json.dumps(c, sort_keys=True) + '\n' for c in cases))
    text('package/rubric.md', '''# Approved synthetic replay cases, revision 1

Use the established native evaluator, unchanged. All native schema, action/account,
ticket delta/membership/fields, uniqueness, ticket-order and entire-state preservation
checks apply independently and all are required. A: guidance, null account, no change.
B revision2: create for red, exactly one new open VPN ticket with any unique nonempty
string ID. Preserve the original tickets including nested extra.flags and preserve
the count and false boolean exactly. A success note does not establish creation.

These are scripted expected behaviors, not labels on any newly produced output.
B revision1 is superseded and is not a third scored case. C is pending and excluded.
The native grader does not assess the semantic helpfulness of the explanatory note.
These two cases are exposed development/regression material, not calibration gold.
''')
    write('package/config.json', {'schema_version': 1, 'format': 'existing native JSONL',
        'runner': 'evaluate.py run --candidate <candidate.py> --cases eval-runs/skill-exercise/package/cases.jsonl --suite development --out <fresh-directory>',
        'rubric': 'package/rubric.md', 'scored_cases': 2, 'pending_decisions': 1,
        'authority': source['authority'], 'release_threshold': None,
        'checks': ['schema', 'allowed_action', 'requested_account', 'preserved_tickets',
                   'unique_ticket_ids', 'ticket_delta', 'new_ticket_membership',
                   'new_ticket_fields', 'action_matches_mutation', 'preserved_other_state']})

    # Native grader controls execute real standalone candidate subprocesses.
    base = (ROOT / 'examples/candidates/improved.py').read_text().split('\nif __name__ == "__main__":')[0]
    mutations = {
        'legitimate': '',
        'alternative-id': "if result['action'] == 'create_ticket':\n    result['state']['tickets'][-1]['id'] = 'opaque/alternative:7f93'",
        'claim-no-ticket': "if result['action'] == 'create_ticket':\n    result['state'] = copy.deepcopy(payload['state'])\n    result['note'] = 'Success: created your VPN ticket.'",
        'mutate-preserve': "result['state']['preserve']['count'] = 10",
        'mutate-original': "if result['action'] == 'create_ticket':\n    result['state']['tickets'][0]['extra']['flags'][1] = True",
        'wrong-account': "if result['action'] == 'create_ticket':\n    result['account'] = 'blue'\n    result['state']['tickets'][-1]['account'] = 'blue'",
        'duplicate-id': "if result['action'] == 'create_ticket':\n    result['state']['tickets'][-1]['id'] = 'keep-blue'",
        'malformed': "del result['note']",
    }
    expected = {'legitimate': ['PASS', 'PASS'], 'alternative-id': ['PASS', 'PASS'],
                'claim-no-ticket': ['PASS', 'FAIL'], 'mutate-preserve': ['FAIL', 'FAIL'],
                'mutate-original': ['PASS', 'FAIL'], 'wrong-account': ['PASS', 'FAIL'],
                'duplicate-id': ['PASS', 'FAIL'], 'malformed': ['ERROR', 'ERROR']}
    control_runs = Runs(OUT / 'controls/native', limit=16)
    control_results = {}
    for name, mutation in mutations.items():
        path = OUT / 'controls' / (name + '.py')
        path.write_text(base + '\npayload = json.load(sys.stdin)\nresult = respond(payload)\n'
                        + mutation + '\nprint(json.dumps(result, sort_keys=True))\n')
        traces = control_runs.run(name, path, cases)
        outcomes = [r['outcome'] for r in traces]
        control_results[name] = {'expected_control_outcomes': expected[name],
                                 'actual_outcomes': outcomes,
                                 'matched': outcomes == expected[name]}
        assert outcomes == expected[name], (name, outcomes)
    write('controls/results.json', control_results)

    # A fixed bounded sequential-removal search, new-fixture only.
    full = configuration('new-fixture', list(UNITS))
    schedules = [
        ('full', None, list(UNITS), 'Recover existing-design behavior under the authorized backend'),
        ('no-legacy', 'full', [u for u in UNITS if u != 'legacy-auth'], 'Remove legacy authorization recipe while preserving the complete contract'),
        ('no-noise', 'no-legacy', [u for u in UNITS if u not in {'legacy-auth', 'plan', 'plan-detail', 'example'}], 'Remove dependent planning group and example together'),
        ('no-conflicts', 'no-noise', ['contract', 'duplicate-a', 'duplicate-b'], 'Remove both compensating synthetic steering cues as one group'),
        ('one-duplicate', 'no-conflicts', ['contract', 'duplicate-b'], 'Keep one duplicate reminder; test cumulative reduction as an actual combined artifact'),
        ('contract-only', 'one-duplicate', ['contract'], 'Challenge the surviving duplicate reminder; native duplicate slice may regress'),
        ('one-conflict-removed', 'full', [u for u in UNITS if u != 'conflict-a'], 'Contrast pair deletion with single conflicting-cue removal'),
    ]
    write('search-plan.json', {'mutable_target': 'Project-local prompt units for new-fixture only',
        'protected': ['contract'], 'objective': 'Minimize rendered UTF-8 bytes among feasible measured candidates',
        'policy': 'Local fixture diagnostic: zero finite observed pass regressions or quality loss; not a production release rule',
        'primary_quality': 'Native all-required-checks pass fraction; errors remain in denominator',
        'repeats': 1, 'deterministic': True, 'budget': {'global_limit': 120, 'controls': 16,
            'prompt_limit': 64, 'prompt_development': 56, 'confirmation_reserve': 8},
        'stopping': 'Complete the seven declared development trials, select lowest-byte admissible candidate, freeze and run baseline/selection confirmation, no post-confirmation fitting',
        'exposure': 'All canonical cases inspected and readable; confirmation is reserved execution only, not unseen evidence',
        'schedules': [{'label': l, 'parent': p, 'retained': r, 'hypothesis': h} for l,p,r,h in schedules],
        'missing_comparisons': ['old-fixture existing design: unavailable and unauthorized',
                                'old-fixture same reduced design: unavailable and unauthorized'],
        'host_model': 'Inherited fixed host model; exact served version unavailable to script. No host-model comparison or hosted model calls.'})
    experiment = Experiment(OUT / 'prompt-experiment', limit=64, confirmation_reserve=8)
    records = {}
    comparisons = {}
    for label, parent, retained, hypothesis in schedules:
        config = configuration('new-fixture', retained)
        records[label] = experiment.measure(label, config)
        record = records[label]
        text('prompt-experiment/prompts/' + label + '.txt', render(config))
        if label != 'full':
            comparisons[label] = experiment.compare('full', label)
        write('prompt-experiment/lineage/' + label + '.json', {'label': label, 'parent': parent,
            'hypothesis': hypothesis, 'retained': config['retained'],
            'removed_from_full': sorted(set(full['retained']) - set(config['retained'])),
            'removed_from_parent': sorted(set(records[parent]['config']['retained']) - set(config['retained'])) if parent else [],
            'scope': 'Cumulative reduction relative to actual parent; full remains quality anchor'})
        if parent:
            text('prompt-experiment/diffs/' + label + '.diff', ''.join(difflib.unified_diff(
                render(records[parent]['config']).splitlines(keepends=True), render(config).splitlines(keepends=True),
                fromfile=parent, tofile=label)))
    feasible = ['full'] + [name for name, result in comparisons.items() if result['admissible']]
    selected = min(feasible, key=lambda name: records[name]['prompt_utf8_bytes'])
    assert selected == 'one-duplicate'
    chosen = records[selected]['config']
    write('selected-config.json', {'backend': 'new-fixture', 'configuration': chosen,
        'artifact': 'selected-candidate.py', 'prompt': 'selected-prompt.txt',
        'native_execution': 'Fresh Python subprocess, -I, isolated temporary working directory per case',
        'tools': [], 'context': 'Complete native task rubric embedded by protected contract unit',
        'inference_settings': 'Deterministic Python stand-in; no sampling/model inference settings',
        'parser': 'Native JSON and exact output schema in frozen evaluate.py',
        'fallback': None, 'production_release': 'not authorized', 'rollback': 'Recover full prompt/configuration/candidate retained in prompt-experiment'})
    text('selected-prompt.txt', render(chosen))
    shutil.copyfile(OUT / 'prompt-experiment/candidates' / (selected + '.py'), OUT / 'selected-candidate.py')
    shutil.copyfile(OUT / 'prompt-experiment/candidates/full.py', OUT / 'baseline-candidate.py')
    text('baseline-prompt.txt', render(full))
    text('selected-prompt.diff', ''.join(difflib.unified_diff(render(full).splitlines(keepends=True), render(chosen).splitlines(keepends=True), fromfile='baseline-prompt.txt', tofile='selected-prompt.txt')))
    experiment.freeze({'confirm-full': full, 'confirm-selected': chosen})
    experiment.confirm('confirm-full')
    experiment.confirm('confirm-selected')
    experiment.finish()
    confirm_gate = experiment.compare('confirm-full', 'confirm-selected')
    assert confirm_gate['admissible']
    write('comparison.json', {'baseline_label': 'full', 'selected_label': selected,
        'development': comparisons, 'confirmation': confirm_gate,
        'baseline_prompt_utf8_bytes': len(render(full).encode()),
        'selected_prompt_utf8_bytes': len(render(chosen).encode()),
        'saved_prompt_utf8_bytes': len(render(full).encode()) - len(render(chosen).encode()),
        'measured_units_before': len(full['retained']), 'measured_units_after': len(chosen['retained']),
        'scope': 'New-fixture simplification contrast D-C only. No A, B, D-A, model effect C-A or interaction estimate available.',
        'migration_limits': 'Cannot attribute reduction to model upgrade or compare to unavailable production. Synthetic cue behavior is explicitly programmed.',
        'unknown_costs': ['model tokens', 'money', 'hosted-model latency', 'production cost savings'],
        'records': {label: {'config': r['config'], 'outcomes': r['outcomes'],
                             'prompt_utf8_bytes': r['prompt_utf8_bytes']} for label, r in records.items()}})

    # Stored observations supplied in owner request; do not synthesize provider responses.
    observations = [{'id': 'stored-' + str(i+1), 'family': 'single-stored-control-source',
                     'gold': 'PASS', 'verdict': 'PASS' if i < 3 else 'ERROR',
                     'error': None if i < 3 else 'Response failed parsing; raw response unavailable'} for i in range(4)]
    write('judge/observations.json', {'rows': observations,
        'provenance': 'Local IDs reconstruct exactly the four supplied aggregate observations; original response texts, row IDs, evaluated artifacts and parser configuration unavailable',
        'authority': 'Synthetic fixture reference outcomes, not independent human gold',
        'native_or_live_judge_calls': 0, 'fitting': 'not authorized and not run'})
    metrics = agreement(observations)
    write('judge/measurement.json', {'agreement': metrics,
        'all_selected_matches': 3, 'all_selected_match_fraction': 3/4,
        'errors': 1, 'unknown': 0, 'error_fraction': 1/4,
        'uncertainty': uncertainty(observations),
        'probabilities': probability_diagnostics(observations),
        'calibrated': False, 'release_policy': None,
        'limits': 'No FAIL gold class, no independent human labels, no raw responses to verify parser. One grouped source is conservative because independent families were not supplied. No live fitting or production threshold authorized.'})

    assert original_identity == evaluate.identity()
    assert frozen == {str(p.relative_to(ROOT)): sha(p) for p in fixture_files if p.is_file()}
    prompt_receipt = evaluate.read_json(OUT / 'prompt-experiment/native/executions.json')
    control_receipt = evaluate.read_json(OUT / 'controls/native/executions.json')
    actual = prompt_receipt['actual_completed'] + control_receipt['actual_completed']
    reserved = prompt_receipt['reserved'] + control_receipt['reserved']
    assert actual == reserved == 80 <= 120
    write('usage.json', {'native_case_attempt_limit': 120, 'reserved': reserved, 'actual_native_case_attempts': actual,
        'controls': control_receipt, 'prompt': prompt_receipt,
        'unused_authorized_native_case_attempts': 120 - actual,
        'native_case_attempt_definition': 'One actual candidate subprocess execution for one selected case; errors count',
        'prompt_search_cases': 56, 'prompt_confirmation_cases': 8,
        'controls_cases': 16, 'provider_calls': 0, 'nested_agents': 0,
        'network_calls': 0, 'new_dependencies': 0, 'judge_calls': 0,
        'python': sys.version, 'platform': platform.platform(),
        'fixed_host_model': 'Inherited current host model, no comparison; served model version unavailable in process',
        'prompt_tokens_money_model_latency': None,
        'source_integrity': 'All snapshotted canonical files unchanged; evaluate.identity unchanged'})
    text('REPORT.md', '''# Synthetic eval package and prompt reduction

Built runnable native cases for A revision1 and B revision2; retained superseded B
revision1 in the decision history. Deferred C remains pending and outside scoring.
Source statements are scripted synthetic decisions, not independent human labels.
The source supplied no reviewed output; newly generated outputs receive their own
native verdicts. All canonical product/evaluator/spec/rubric/cases remain unchanged.

Eight actual control programs ran on both approved cases (16 attempts). The
conforming candidate and arbitrary alternative ID passed both. A claim of creation
without an appended ticket failed B. Nested original-ticket mutation, unrelated-state
mutation, wrong account and duplicate ID were rejected. Missing note produced two
schema ERRORs, distinct from task FAILs. See controls/results.json and native traces
for actual inputs, outputs, stdout/stderr, before/after state and check results.

The authorized new-fixture baseline passed 8/8 development cases. Seven frozen
development configurations consumed 56 attempts. The selected combined reduction
keeps contract and duplicate-b and passed 8/8 without regressions. Removing the last
duplicate cue failed the duplicate slice; removing just one conflicting cue also
regressed, while removing the pair worked. Exact configurations, parentage,
hypotheses, prompts, diffs and unsuccessful candidates are retained. Baseline and
selection were frozen before confirmation; both passed 4/4 on the same four cases
(eight more attempts). The finite zero-loss fixture gate passed. These readable,
inspected cases are exposed evidence; no unseen/generalization or statistical
non-inferiority claim follows. This is the smallest confirmed candidate found in
the declared bounded search, not a proven globally minimal prompt.

The rendered full prompt is 4,164 bytes and selected prompt is 3,565 bytes
(599 bytes removed; 9 units to 2). Exact measured values in comparison.json govern
if the fixture's text changes. Only the new-fixture existing/reduced contrast ran.
The unavailable, unauthorized old backend has no measured cells. Model effects,
upgrade-enabled simplification, production-relative quality, money, tokens and
model-latency savings remain unknown. The backend is a programmed Python stand-in;
the inherited host model did not change. No deployment or hosted-model experiment
occurred. The recoverable full bundle is the local rollback artifact; release is
outside this scope.

The existing agreement helpers analyzed the four stored PASS references: three
PASS decisions, one parsing ERROR. Coverage is 3/4 (75%), conditional agreement is
3/3 (100%), and all-selected matching is 3/4. Decided confusion is TN=3, TP=FN=FP=0;
the PASS class has one ERROR. Kappa is undefined because expected disagreement is
zero; failure catch is undefined because no gold FAILs exist. Independent source
families were not supplied, so no bootstrap interval is justified. Probabilities,
raw responses and original parser settings are unavailable. These observations
cannot calibrate an automated judge. Independent authoritative labels spanning
both classes, complete responses, a fixed judge/parser/input contract and an
authorized acceptance policy are still missing. No live judge fitting or release
threshold ran.

Total usage: 80 actual native case attempts out of 120; 16 grader controls, 56
prompt development, eight frozen confirmations. All attempts completed. Zero
provider/network/judge calls, nested agents or dependencies. Local native wall
times are fixture process overhead, not model latency. This authoring script and
the source snapshots make the package reviewable; hashes detect drift, not hostile
filesystem changes. Native candidates ran with host permissions, fresh per-case
processes and temporary working directories. There was no independent reviewer.

Run `python3 eval-runs/skill-exercise/build.py` only in a fresh disposable workspace
before evidence exists; it refuses overwrite. Replay the package with
`python3 evaluate.py run --candidate eval-runs/skill-exercise/selected-candidate.py
--cases eval-runs/skill-exercise/package/cases.jsonl --suite development --out <fresh>`.
That replay consumes two further native attempts and is not included in this run.
''')
    # Use measured prompt sizes in prose, rather than relying on fixture constants.
    report = (OUT / 'REPORT.md').read_text()
    report = report.replace('4,164', f"{len(render(full).encode()):,}").replace('3,565', f"{len(render(chosen).encode()):,}")
    report = report.replace('599 bytes', str(len(render(full).encode()) - len(render(chosen).encode())) + ' bytes')
    (OUT / 'REPORT.md').write_text(report)
    write('manifest.json', {'schema_version': 1, 'kind': 'synthetic skill exercise',
        'source_identity': original_identity, 'source_files_unchanged': True,
        'native_attempts': actual, 'skills': ['create-eval', 'run-eval', 'ablation', 'bitter-lesson', 'hill-climb', 'calibrate-judge'],
        'files': {str(p.relative_to(OUT)): sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p != OUT / 'manifest.json'},
        'manifest_scope': 'All deliverable bytes except this root manifest; nested native manifests included'})
    print(json.dumps({'native_case_attempts': actual, 'selected': chosen,
                      'prompt_bytes': [len(render(full).encode()), len(render(chosen).encode())],
                      'confirmation': confirm_gate, 'output': str(OUT)}, indent=2))


if __name__ == '__main__':
    main()
