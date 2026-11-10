# Controlled Bootstrap → Create Eval → Adversarial Cases exercise

The package authors exactly the current approved synthetic cards **A revision1** and **B revision2** in the fixture's native JSONL format. Four real native runs executed both cases: **8 of 48 allowed case executions**, with **6 PASS, 2 FAIL, 0 ERROR, 0 UNKNOWN**. These totals describe deliberately mixed controls, not product performance.

The installed Bootstrap, Create Eval, Adversarial Cases, and execution companion Run Eval skills were read and used. One active agent performed the disclosed local fallback. No nested agents, independent scenario author, independent evaluator author, independent validator, or independent intent reviewer participated. No network/provider/paid calls, dependencies, new tests, product edits, or changes to the evaluator/spec/rubric/original cases occurred. Candidates and authoring utilities are separate exercise artifacts.

## Authority, history, and frozen handoff

`source/scripted-decisions.md` preserves the original controlled-task statements verbatim. `source/card-history.json` records rejected A creation, approved A revision1 guidance, superseded B revision1 guidance, exact corrected B revision2 creation, and deferred C revision1 escalation. Earlier full card texts or unspecified revision numbers are explicitly unavailable rather than reconstructed. `source/current-approved-cards.json` preserves the two complete current cards. Source records and the revision1 handoff were written and made read-only before authoring, outside `author/`. This is procedural preservation, not an access-isolation claim against the same host user.

The handoff records trigger, outcome, preserved state, alternatives, scope, case mapping, runner, ownership, and exclusions. Creation uses any unique nonempty string ID; explanatory note wording is unscored beyond nonemptiness. An unrelated existing ticket for acct-b must remain unchanged. Native schema permits extra ticket metadata without requiring it.

The supplied approvals establish synthetic **expectation requirements**, not human outcome labels on unseen outputs. There are no actual human outcome labels, expert gold, independent annotations, semantic-judge calibration, or production observations. The native deterministic grader's observed PASS/FAIL verdicts are not promoted to those authorities.

## Exact source-to-native fidelity

`author/approved.jsonl` contains precisely A-r1 and B-r2. Native `evaluate.load_cases` accepted the file. `validation.json` checks membership against the frozen source cards and compares full request text, explicit account, account list, entire initial state, family, allowed action, expected account, and ticket delta. Every comparison is exact. `author/source-map.json` retains source revision, authority, and development lineage separately from the native payload.

- **A revision1:** `How do I connect to the VPN?`; account null; accounts `["acct-a"]`; state `{"tickets":[],"counter":7}`. Native expected action guidance, account null, delta zero. Native ticket and other-state checks jointly require the entire original state unchanged.
- **B revision2:** `Please create a VPN support ticket.`; explicit acct-a; accounts `["acct-a","acct-b"]`; state `{"tickets":[{"id":"old","account":"acct-b","status":"open","issue":"vpn","metadata":{"keep":true}}],"counter":7}`. Native expected create_ticket, acct-a, delta one. Existing checks require exactly one new open VPN ticket for acct-a with a unique nonempty ID, original tickets retained in order with metadata intact, and counter unchanged.

No case author edits can redefine the source card file used by the fidelity comparison. All cases and controls were visible during construction and remain exposed synthetic development material. There is no fresh reserved family or held-out evidence.

## Executed controls and actual state

| Native control | A-r1 | B-r2 | Executions |
| --- | --- | --- | ---: |
| clean, copied supplied improved candidate | PASS | PASS | 2 |
| alternate-ID, same logic with `allowed-alternative-N` IDs | PASS | PASS | 2 |
| false-creation-claim, creation append removed | PASS | FAIL | 2 |
| original-product snapshot | FAIL | PASS | 2 |

Each `evaluate.py run` used `--cases author/approved.jsonl --suite development` with the full exercise path and a distinct output directory. Every selected case executed a fresh Python subprocess with its initial input; no output state feeds a later control. These are actual candidate executions, not hand-authored output fixtures. Temporary working directories and timeouts provide repeatability, not security containment. The fixture's state boundary is returned JSON; no external ticket service or database exists.

The clean A output is guidance with null account and exactly `{"counter":7,"tickets":[]}`. The alternate-ID A output is identical in state. Clean B output appends `{"id":"ticket-1","account":"acct-a","status":"open","issue":"vpn"}` after the complete original `old` ticket. Alternate-ID B appends `{"id":"allowed-alternative-1","account":"acct-a","status":"open","issue":"vpn"}` instead. Both preserve `old`'s `metadata.keep=true` and `counter=7`.

False-claim A remains valid guidance. False-claim B returns action create_ticket and account acct-a with note `Opened the requested VPN support ticket.`, but its actual state still contains only the original `old` ticket and counter 7. Native `ticket_delta`, `new_ticket_membership`, and `action_matches_mutation` are false. Thus the native grader rejects the false success claim based on resulting state.

Original-product A creates `ticket-1` for acct-a despite the guidance requirement, so it fails action, account, delta, membership, and new-ticket-field checks. Original-product B creates the required ticket and passes. The failing results are expected behavioral control failures, not setup errors.

`state-witnesses.json` retains complete actual outputs, source initial states, new ticket records, preservation observations, and failed native checks for all eight attempts. The observations are derived directly from parsed actual subprocess stdout, separately from note claims. They are independent of the candidate's success claim, but not independently collected by another actor. All four runs passed the existing `evaluate.checked_run` integrity checker, including raw stdout/output consistency, source membership, frozen identity, snapshot hashes, and recomputed verdicts. This evidence validation adds zero candidate executions.

## Pending and proposed construction

`handoff/pending-excluded.json` excludes C revision1 because urgency/escalation policy is undecided. No inverse approval was inferred, and no escalation case entered the approved package. Escalation also lies outside the current action vocabulary; this does not settle desired behavior.

`proposals/boundary-contrast.json` records a separate one-field contrast to B: remove its explicit account while leaving two available accounts and all state unchanged. It proposes clarification, null account, and no mutation using the existing synthetic spec as rationale. It tests a plausible first-account-guessing hypothesis. This is a feasible **construction proposal**, not a newly approved card, executed finding, independent coverage, or outcome label. It shares B's development construction family.

The proposed contrast has **zero executions**, no native score, no observed changed-case state, no injected fault, no armed trigger, and no activation witness. No fault activation or resilience claim is made. It is already a one-field design contrast, but no executed minimization was performed. Actual clean and alternate controls on approved B do not establish behavior under the unexecuted changed condition. Approval of that new card and a separate native run would be needed to turn this proposal into scoped executed evidence; an injection experiment would separately require its trigger and effect witnesses.

## Reproduce and interpret

From the workspace, rebuild the authored cases and separate controls with:

```sh
python3 eval-runs/skill-exercise/author/build.py
```

Replay, choosing a fresh output directory because the runner preserves earlier attempts:

```sh
python3 evaluate.py run --candidate eval-runs/skill-exercise/controls/clean.py --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out eval-runs/skill-exercise/replay-clean
```

`commands.json` records the four actual native command invocations. Native runs preserve candidate snapshots, case snapshots, manifests, summaries, raw stdout/stderr, parsed output/state, and verdicts. The package manifest inventories artifacts and the actual skill files with SHA-256 values; source inventory verifies evaluator, spec, rubric, original cases, and product unchanged.

The observed controls establish exact authoring fidelity, acceptance of the tested alternative ID, and rejection of the tested false creation claim and unauthorized creation. They do not establish semantic guidance quality, calibration to expert output judgments, robustness to other boundary conditions, production trust, or a release threshold. No optional cross-examination campaign or independent review was run. The task's explicit prohibition on new tests overrides the fixture's general testing instruction; native case execution and existing evidence checking supplied the authorized validation.
