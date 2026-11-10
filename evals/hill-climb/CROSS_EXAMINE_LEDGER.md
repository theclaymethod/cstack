# Hill Climb Cross-Examine ledger

## 2026-11-10 — audit and fixture consolidation

The user authorized Cross-Examine and fixes for confirmed issues, using the playground, and clarified that the playground belongs inside cstack as a fixture. Original intent: improve an authorized artifact against a fixed eval through actual execution, per-case regression constraints, finite accounting including confirmation/errors, reliable resume, and preservation of the best verified artifact. No improvement is a normal outcome.

The playground is a deterministic synthetic support-agent task with visible cases. It makes no model-performance, hidden-test, semantic-helpfulness, or security-containment claim. The rubric expressly requires exactly four output fields and a nonempty explanatory note, while allowing any unique ticket ID and unrestricted nonempty explanatory wording.

### Roles, versions, and access

The coordinator was defender. Separate fresh attackers investigated scoring/evidence and campaign lifecycle. A fresh non-forked reviewer established intent before seeing findings, read raw native evidence without competitor narratives, and independently assessed the findings. The reviewer did not propose, author, repair, coordinate, or optimize candidates. A frozen repair checkpoint follows the original acceptance checkpoint.

One bounded round allowed up to three mechanisms per attacker, plus targeted repair replays. Candidate-scored edits were confined to standalone product files; frozen runner, spec, cases, rubric, contract, and operator state were unchanged. Lifecycle probes stopped actual native commands at specified execution boundaries. A separate extra-access robustness check is labeled as such below. Each role used separate copies. These were instructed host scopes, not OS-enforced isolation.

The original fifteen native tests passed before search. [Original hashes](evidence/cross-examine/original-hashes.json) and [original evaluator](evidence/cross-examine/original-evaluate.py) freeze that implementation. [Repair hashes](evidence/cross-examine/repaired-hashes.json) identify the reviewed source. All observations are development evidence, with original records retained.

## Confirmed: declared output schema can be bypassed

**Intent:** malformed output is an ERROR, not a passing behavior. The rubric requires exactly `action`, `account`, `state`, and a nonempty string `note`.

**Reproducer:** change only a legitimate candidate's output to use an empty note, an undeclared extra key, or both. [Empty-note](evidence/cross-examine/empty-note.py), [extra-key](evidence/cross-examine/extra-field.py), and [combined](evidence/cross-examine/combined.py) candidates preserve the legitimate ticket actions/state but violate the declared schema. Original protected file hashes were unchanged.

**Original observation:** empty-note and extra-key candidates each scored 12/12 PASS. The combined invalid candidate was retained, confirmed, selected, and delivered through a complete 24-case-attempt campaign. The ordinary `verify` command accepted its evidence. This is undeserved credit for malformed output, not a semantic helpfulness dispute or budget bypass.

**Repair:** the shared grading boundary enforces the exact top-level field set and a nonempty, non-whitespace note. Hill Climb's baseline/preflight guidance now calls for malformed-output controls against declared required/extra-field/value rules. The grader still permits alternative explanatory wording, object-key order, and unique ticket IDs.

**Observed repaired outcome:** invalid schema cases produce ERROR for every selected case. The combined candidate cannot replace the baseline. The original legitimate improved candidate and a candidate using different ticket IDs/nonempty wording remain accepted. [Original/repaired observations](evidence/cross-examine/before-after.json) record the results.

## Confirmed: complete native evidence can be stranded before ledger commit

**Intent:** preserve the best verified artifact and resume compatible work without free retries or duplicate spend. A truly partial run remains pending and charged.

**Reproducer:** stop a real proposal or confirmation command immediately after `run_suite` flushes a complete native run, before `execute_attempt` records completion in campaign state. The [fault hook](evidence/cross-examine/interrupt_cli.py) stops the process; it does not alter protected source or receipts. The original native `checked_run` independently accepts the complete retained evidence against the reservation's candidate/evaluation identity.

**Original observation:** after the proposal stop, `verify` leaves the measured 8/8 candidate pending at 16 charged attempts, and `finish` delivers the baseline despite complete comparable measurement. After a stop on completed incumbent confirmation, all 24 attempts are charged, but resume refuses to deliver any selected artifact. A separate committed-receipt/undecided-decision control already recovers correctly, narrowing the gap to the preceding completion commit.

The lifecycle attacker initially treated conservative pending behavior as a documented limitation. Independent intent review accepted the narrower complete-evidence gap: the original campaign reference contemplates reconciliation from native receipts, and complete identity-matching evidence is distinguishable from partial execution. This is recovery/liveness failure, not uncharged execution or a security bypass. [Original independent assessment](evidence/cross-examine/original-intent-review.md).

**Repair:** resume validates full native evidence against its pre-execution reservation: candidate hash, frozen identity, full case-source hash, exact suite membership, complete actual outputs/checks, and reserved case count. It then records completion and reconciles the retention decision without rerunning the artifact or changing charged spend. Partial, invalid, incompatible, and mismatched receipts remain pending and charged. The portable skill and campaign reference encode this distinction.

**Observed repaired outcome:** completed proposal evidence recovers at the same 16 charged attempts and the measured candidate survives selection at 24/24. Completed confirmation recovers and finishes at the existing 24/24, with native evidence byte-identical. The tests also cover baseline recovery and both confirmation phases. Genuine partial and invalid receipts stay pending and cannot promote; interrupted partial confirmation still requires a new campaign for additional confirmation work.

## Clean controls and limitations

- A normal campaign retained the valid improvement, rejected a regressing proposal, protected confirmation reserve, and delivered the selected artifact within budget.
- Interrupting after an already committed receipt but before its selection decision recovered with the same evidence and spend. This was already correct and is not credited as a repair.
- In an extra-access robustness check, changing a parsed retained output to contradict its subprocess stdout was rejected. This was an artifact-consistency test, not a permitted candidate-only exploit.
- The native suite includes existing partial-interruption, no-improvement, schema/source drift, receipt tampering, state preservation, and valid-alternative controls. It now has 22 tests including materialized-workspace checks.

No-finding and conservative rejection observations remain useful bounded results. These checks do not establish broad workflow immunity, provider behavior, stochastic optimization quality, unseen-data generalization, or malicious-process containment.

## Reproduce

From the C Stack repository root:

```sh
python3 evals/hill-climb/cross_examine.py
python3 -m unittest discover -s fixtures/playground/tests -v
```

The audit command runs original and repaired evaluators in disposable copies, preserves actual commands/stdout/stderr and identities, reproduces original wrong passes and recovery failures, and checks repaired outcomes. It is a replay of recorded mechanisms, not a new adversarial search or agent optimization campaign. [Replay commands](evidence/cross-examine/replay-commands.json) preserve the development checkpoint.

## Canonical fixture

`fixtures/playground/` now owns the product, evaluator, cases, exercises, and native tests. It contains no nested `.git`, generated skill copies, lock, or run outputs. This removes the separate maintained test repository and duplicate source-pack installation from the canonical tree.

Create a disposable local workspace with the current seven skills and its own Git repository:

```sh
python3 fixtures/playground/scripts/new_workspace.py --out eval-runs/playground
```

The command refuses existing destinations and recursive fixture output. Generated metadata resolves the owning C Stack checkout, so sync/control commands no longer assume a sibling `../cstack` layout. The original standalone checkout, including Git/runtime data, is preserved in an ignored legacy archive when consolidation is applied; historical receipts retain their original paths/hashes. This is source consolidation, not a rewrite of historical evidence.

## Frozen repair acceptance

The independent reviewer accepted the frozen repair after independently replaying the original/repaired audit, running all 22 fixture tests, and creating a new workspace with seven verified skill copies. [Assessment](evidence/cross-examine/frozen-repair-intent-review.md). The source changes were not tuned against iterative reviewer feedback. The final combined invocation passed all six suites: Expert Review, Cross-Examine, Bootstrap replay, Bootstrap audit, Hill Climb audit, and native fixture tests. [Recorded commands/results](evidence/cross-examine/all-controls.json).
