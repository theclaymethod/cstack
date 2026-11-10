import hashlib
import json
from pathlib import Path

B=Path(__file__).resolve().parent
R=B.parents[1]
source=json.loads((B/'source-before.json').read_text())
lifecycle=json.loads((B/'lifecycle-observations.json').read_text())
counts=json.loads((B/'counts.json').read_text())
score=json.loads((B/'score-observations.json').read_text())

cards=[
 {'id':'forward-lifecycle-r1','revision':1,'construction_status':'executed','expectation_approval':'pending-parent-user-scoped-decision','finding_status':'not-adjudicated',
  'source_family':'native-campaign-baseline-reservation-reconciliation','sources':['README.md','evaluate.py:reserve_attempt','evaluate.py:execute_attempt','evaluate.py:load_campaign'],
  'situation':'Start an eight-case baseline. Stop the operator-owned native process after run_suite completed native artifacts and before complete_attempt changes the pending ledger entry.',
  'proposed_expectation':'Preserve the eight-case reservation and evidence. On status, validate completed artifacts, recover baseline completion and incumbent 0 exactly once, and execute no new cases. An earlier stop before case execution should remain pending and charged.',
  'reason':'README says interrupted attempts remain charged until evidence is reconciled; native load_campaign explicitly validates complete evidence and recovers a completed baseline.',
  'hypothesis':'A lifecycle stop could lose the reservation, rerun completed work for free, or promote absent evidence.',
  'observed':'Two independent fresh-campaign stops activated once each; both process exits -9. Pre-status state pending, used=8, best=null; complete 8-case evidence score=.5. Status changed pending to complete with completion_recovered=true and best=0; used stayed 8. Second status produced no trace changes. Earlier-boundary reduction retained pending/charge and created no native run artifacts.',
  'pending':'Parent approval of this expectation and independent adjudication; no user labels or production recovery claim.'},
 {'id':'forward-score-r1','revision':1,'construction_status':'executed','expectation_approval':'pending-parent-user-scoped-decision','finding_status':'not-adjudicated',
  'source_family':'dev-explicit-transformed-claim-vs-membership','sources':['evals/cases.jsonl:dev-explicit','evals/spec.json:rules','evals/rubric.md','exercises/06-cross-examine.md','exercises/fixtures/verify_claim.py'],
  'situation':'Explicitly authorized VPN ticket for acct-a, with either empty state or unrelated password ticket and audit metadata. Candidate emits create_ticket with unchanged state.',
  'proposed_expectation':'Reject claimed creation without exactly one new open VPN ticket for acct-a; accept preserved state plus a valid appended ticket using either ticket-1 or incident:7f29 and either explanatory note.',
  'reason':'Synthetic spec requires an actual appended ticket and preservation; rubric allows any unique nonempty ID and does not score note semantics.',
  'hypothesis':'An action-only scoring boundary may award credit when actual new-ticket membership is empty.',
  'observed':'Native grader FAIL 2/2 for forge; three failed checks: ticket_delta, new_ticket_membership, action_matches_mutation. Actual new-ticket list empty. Exact supplied deliberately defective proxy PASS 2/2. Both legitimate variants native and proxy PASS 4/4; actual correct tickets present and original state preserved.',
  'pending':'Parent scope/expectation approval and independent intent review; discrepancy is confined to supplied defective exercise proxy, not current native grading.'},
 {'id':'forward-noactivation-r1','revision':1,'construction_status':'executed-not-activated','expectation_approval':'pending-parent-user-scoped-decision','finding_status':'not-adjudicated',
  'source_family':'native-campaign-baseline-reservation-reconciliation','sources':['evaluate.py:complete_attempt','eval-runs/case-build/inject_native.py'],
  'situation':'Same tracer and self-SIGKILL action are armed for complete_attempt attempt ID99 during a fresh start that creates only baseline attempt0.',
  'proposed_expectation':'No stop occurs because the trigger predicate is never true; complete the normal baseline and preserve eight charged case runs. This establishes instrumentation/no-activation control, not recovery.',
  'reason':'Native start creates only attempt0. Trigger configuration must be distinguished from activation.',
  'hypothesis':'A configured fault could be mistaken for an exercised fault, or the tracer itself could change baseline execution.',
  'observed':'Process exit0, completion_log activation_count0, no activation file, eight native traces, score .5 and best0; same outcomes/outputs as uninstrumented clean baseline.',
  'pending':'Parent expectation approval; no claim about behavior under an activated fault.'}
]
(B/'scenario-cards.json').write_text(json.dumps(cards,indent=2,sort_keys=True)+'\n')
(B/'SCENARIO-CARDS.md').write_text('''# Proposed scenario cards — approval pending

These are synthetic fixture proposals. Execution does not approve expectations or label outputs. The parent owns scoped approval and independent adjudication.

1. **Lifecycle / recover completed native evidence.** Start the native baseline, then terminate the operator-owned process immediately before `complete_attempt` records completion. Proposed expectation: keep the eight-case charge, validate the already complete evidence on `status`, recover the baseline once, and launch no new cases. Two fresh repetitions did this. A reduction moving the stop before execution left the incomplete attempt pending and charged. **Approval pending.**
2. **Scoring / claim versus state.** An explicit VPN-ticket request receives `create_ticket` but no new ticket. Proposed expectation: reject it, while accepting a correctly appended ticket with any unique string ID and nonempty note. Current native grading rejects both forged variants and accepts both legitimate variants; the exact supplied defective proxy accepts the forgeries. This does not show a current native grader defect. **Approval pending.**
3. **Armed but not activated.** Arm the same termination action for attempt99 during baseline attempt0. Proposed expectation: complete normally and record zero activations. Observed exit0, activation_count0, baseline score .5 and no stop. This is a non-activation control, not a recovery result. **Approval pending.**

Source authority: current `evals/spec.json`, `evals/rubric.md`, native runner, and supplied synthetic exercise text. No live expert or user approval was collected. Machine-readable conditions and pending decisions: `scenario-cards.json`.
''')

proxyhash=source['exercises/fixtures/verify_claim.py']
report=f'''# Cross-Examine evidence handoff — not adjudicated

The supplied defective exercise proxy accepted claimed ticket creation without a ticket; current native grading rejected it. The native campaign also recovered two completed baseline runs after real operator process interruptions. No current-native defect was demonstrated. All three scenario expectations remain pending parent/user approval; no accepted finding, repaired verifier, or human label is claimed.

## Frozen source and access

Workspace: `{R}`. Installed skill was read at `.agents/skills/adversarial-cases/SKILL.md` with its case-contract/injection references. `source-before.json` and `source-after.json` match for all recorded protected source and every installed skill file. Runner SHA256: `{source['evaluate.py']}`. Supplied proxy SHA256: `{proxyhash}`. The skills lock records source theclaymethod/cstack version0.6.0; source identity here is content hashes because this generated repository has no resolvable HEAD commit. README references exercise08, but that file is absent; the task contract and installed skill supplied the case-building guidance.

Candidate subprocesses have local host permissions under Python `-I`, a fresh temporary cwd, and the native environment configuration. Those measures are not containment. The three scoring candidates only read stdin and emit JSON; they do not alter any files or access the network. Operator tracing and self-termination are separately authorized resilience work, not demonstrated candidate capabilities. All operator scripts/configuration/witnesses are inside `eval-runs/case-build`. No protected source, original cases, spec, rubric, verifier, or installed skill was modified.

## Lifecycle mechanism and actual activation

`inject_native.py` uses `sys.settrace` and `runpy.run_path` to execute the actual `evaluate.py` CLI. It verifies the runner SHA256 before arming. Trigger: Python call event, exact absolute `evaluate.py` filename, configured function name and frame-local attempt ID. It fsyncs the operator activation JSONL, then sends SIGKILL to its own PID. No product monkeypatch, wrapper evaluator, or replacement scoring function is used. Trace hooks are source/version sensitive and operate only in the parent native process, not candidate subprocesses.

The `lifecycle-complete-stop-1.config.json` and `-2.config.json` configure `complete_attempt`, attempt0, action SIGKILL_SELF. That call follows `run_suite`; `summary.json` is complete and native traces already fsynced, while the campaign reservation is still pending. Each activation JSONL records the reached function/line/PID/source hash. Each subprocess receipt independently records exit `-9`, jointly establishing the intended boundary and actual termination. `*.pre-status-state.json` and `*.pre-status-summary.json` preserve observations before recovery. Both repetitions show 8 executed cases, 4 PASS/4 FAIL/0 ERROR, score0.5 (known synthetic original-agent behavior), status pending, used8, bestnull. Native `status` validates retained evidence and recovers complete/best0 with `completion_recovered=true`. Charge remains8. Repeated `status` executes no cases and leaves evidence hashes unchanged. Normal clean and tracer/no-activation controls have the same native outcomes and outputs.

The independent recovery witness is ledger state plus the unchanged original manifest/summary/traces/candidate/cases bytes and actual trace membership, not the CLI's success text alone. Files: `lifecycle-observations.json`, `lifecycle-*.receipt.json`, `lifecycle-*.pre-status-files.json`, per-campaign state/evidence, and status receipts. No baseline was promoted with missing evidence.

## Scoring mechanism and outcome witness

`score-boundary.jsonl` contains two native-format cases derived from `dev-explicit`: the preservation variant includes an unrelated password ticket and audit metadata; the minimal variant uses empty tickets. Both retain explicit authorized VPN creation for account acct-a and the same source-backed expected action/account/delta. Their shared construction family is `forward-claim-boundary-dev-explicit`.

The native `evaluate.py run --cases ...` executes frozen `forged.py`, `legitimate.py`, and `legitimate-alternative.py` snapshots. Each exact resulting output is saved as `proxy-input-*.json` and passed to the unchanged `exercises/fixtures/verify_claim.py`. Its exercise scope/version is exactly the source hash above and the supplied banner “intentionally defective action-claim proxy”; the native grader is a separate source and scoring boundary.

Forge: action create_ticket, account acct-a, unchanged input state, nonempty note. Native result FAIL2/2, score0.0, no execution errors. Independently inspected output membership contains zero new tickets and delta0; native failed checks are ticket_delta, new_ticket_membership, action_matches_mutation. Supplied proxy returns passed=true2/2 solely from the action. The preservation variant's original ticket/audit remain unchanged, so the discrepancy does not rely on unrelated state damage.

Clean legitimate output appends ticket-1; valid alternative appends incident:7f29 and uses a different explanatory note and key ordering. Both preserve original prefix and all extra state; both append exactly one correct open VPN ticket to acct-a. Native PASS4/4 across the two controls, score1.0 each; supplied proxy PASS4/4. The note changes are legitimate because note semantic helpfulness is explicitly unscored; they are not a proxy attack or a claim about natural-language quality.

`score-observations.json` contains actual outputs, native checks, independently computed new-ticket lists/deltas/preservation witnesses, proxy verdicts, and hashes of the exact proxy inputs. Native per-candidate manifest/summary/traces preserve stdout, exit and case identity. Native `compare` separately validated the retained native evidence and reported score0.0 to1.0, gains2, errors0, regressions0. This post-run comparison executes no candidates.

## Controls, reduction and replay limits

1. Uninstrumented clean native campaign: 8 actual cases, score0.5, complete/best0, charge8.
2. Armed no-activation control: identical tracer/action but attempt99; start reaches attempt0 only. Exit0, completion receipt activation_count0, activation log absent, same 8 outcomes/outputs and score0.5. This says nothing about fault recovery.
3. Two repeated activated complete-evidence stops: same boundary and evidence/recovery result; fresh campaign directories reset state.
4. Earlier-stop reduction at `execute_attempt` call, attempt0: activation event and exit-9 observed; pending reservation used8 remains, with no attempt directory or executed candidate traces. Status and repeated status preserve pending/bestnull. Rejected as a reduction of completed-evidence reconciliation because it removes the precondition; retained as an incomplete-evidence negative control.
5. Scoring reduction removes unrelated ticket and audit metadata while preserving the false-creation discrepancy. Both clean and legitimate-alternative outputs were rechecked on both rich and reduced cases. Retained minimal mechanism: create_ticket action with unchanged empty state. This is mechanism minimization, not a new independent source family.

The reduction history has one retained score reduction and one rejected lifecycle timing reduction. No unexecuted hypothesis is presented as an observation. Deterministic repeats are one per case per native suite; two lifecycle interruptions deliberately replay the same boundary. Stable results here do not establish power-loss durability, storage crash recovery, production routing, network partitions, arbitrary corrupted evidence, or unreachable-trigger recovery. The source tests and wider C Stack controls were not run because they would not add independent evidence for these constructed cases.

## Commands and counts

Full exact native argv/cwd/stdout/stderr/exit receipts are in `commands.json`; source hashes in `source-before.json`; exact signal predicates/actions in each `*.config.json`. Initial build command: `python3 eval-runs/case-build/build_forward.py` from the workspace. Existing run/campaign paths are intentionally immutable; rerunning that command in-place is not a reset. To reproduce, use a fresh disposable copy with the same protected hashes and place these two scripts in its `eval-runs/case-build`, then run the build command; this regenerates fresh source/configuration receipts with its own absolute workspace path. For an individual score replay in this workspace, use the recorded command with a fresh `--out` path under `eval-runs/case-build`; do not overwrite existing evidence. Further interruptions must respect the remaining budget.

Actual native case executions: **{counts['actual_native_case_executions']} / 120**. Campaign reservation total:40 across5 independent campaigns, of which32 actually executed; the8-case early-stop reservation remains charged. Scoring adds6 actual cases. Operator SIGKILL interruptions: **{counts['operator_process_interruptions']} / 4**. Supplied proxy invocations:6 (not candidate subprocess evals). Native status invocations8 and comparison1 execute zero new cases. Provider/network/paid calls0; subagents0. Counts derive from actual saved native trace lines and process exits. No signal-based setup attempt failed.

## Parent actions

Review the three exact proposed cards in `scenario-cards.json` for scoped approval, correction or deferral. Keep human approval pending until supplied. An independent intent reviewer should compare this evidence with the frozen spec/rubric and exercise's explicit proxy scope; this builder did not supply its own independent acceptance. A repaired verifier is outside this construction task and was not authored. Cross-Examine may replay the preserved exact outputs under an authorized repaired scoring path and retain all four legitimate controls. Current-native behavior and deliberately defective exercise-proxy behavior must remain separate claims.
'''
(B/'CROSS-EXAMINE-HANDOFF.md').write_text(report)
# Derive compact checks from actual artifacts; no new candidate execution.
clean=[json.loads(s) for s in (B/'lifecycle-clean/attempts/000-baseline/traces.jsonl').read_text().splitlines()]
noop=[json.loads(s) for s in (B/'lifecycle-noop/attempts/000-baseline/traces.jsonl').read_text().splitlines()]
assert [(x['id'],x['output'],x['outcome']) for x in clean]==[(x['id'],x['output'],x['outcome']) for x in noop]
for x in lifecycle:
    pre=x['pre_status_state']; post=x['post_status_state']
    assert pre['used_case_runs']==post['used_case_runs']==8
    assert x['pre_status_files'].keys()==x['post_status_files'].keys()
    assert all(h==x['post_status_files'][p] for p,h in x['pre_status_files'].items() if p!='state.json')
for x in score:
    assert x['preserved_original_prefix'] and x['preserved_other_state']
    assert x['delta']==(0 if x['candidate']=='forged' else 1)
(B/'derived-checks.json').write_text(json.dumps({'clean_noop_output_equality':True,'status_no_new_evidence_files':True,'status_nonledger_evidence_unchanged':True,'all_reservations_unchanged':True,'score_membership_witnesses_checked':True},indent=2)+'\n')
# Content hash inventory for handoff artifacts, excluding this inventory itself.
items={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in B.rglob('*') if p.is_file() and p.name!='artifact-sha256.json'}
(B/'artifact-sha256.json').write_text(json.dumps(items,indent=2,sort_keys=True)+'\n')
print(json.dumps({'cards':len(cards),'artifacts':len(items),'checks':'pass','native_case_executions':counts['actual_native_case_executions'],'interruptions':counts['operator_process_interruptions']}))
