# Bootstrap development exercise

On 2026-11-10, a fresh agent used Bootstrap against the isolated [support-routing fixture](fixture/README.md). The coordinator supplied scripted user replies; every request, scenario, approval, correction, and observation is synthetic. Wording such as “user” or “human-confirmed” in the original role-play checkpoint describes the simulated role, not real expert annotation. These records provide no human judge-calibration evidence.

The fixture had an existing JSONL schema and stored-observation runner, an existing how-to case, no implementation, and no production traces. The initial request left ticket-creation boundaries unspecified.

## Observed workflow

The agent asked about routing intent and recorded provisional requirements without creating eval cases. After the coordinator clarified the policy, two independent scenario authors supplied ordinary and boundary proposals. An initial second dispatch hit the shared agent limit; it ran after capacity became available. The final six cards used both authors' proposals rather than the coordinator's temporary local boundary draft.

The scripted reviewer approved three cards, supplied an exact replacement for a fourth, disapproved a fifth without deciding its replacement, and deferred the sixth. The agent recorded the fourth card as revision 2 without asking the reviewer to approve their own replacement again. Its handoff excluded both unresolved cards. Two evaluator authors produced separate approved groups, then the coordinator integrated four cases in the fixture's existing format.

The generated package retained the existing how-to row unchanged. The corrected existing-ticket case accepts either guidance or clarification, with zero new tickets. Raw proposal status is retained in historical scenario records; the handoff's approved-revision map and decision ledger establish the current decisions.

## Grader controls

Four approved cases ran through the fixture's actual stored-observation runner over 14 invocations. The portable replay reproduced the same 56 case/control verdicts:

| Contract-derived controls | Observed verdicts |
| --- | ---: |
| Legitimate action/count pairs, including both corrected alternatives | 5 PASS |
| Wrong actions or ticket-count changes | 43 FAIL |
| Deliberately missing observations or noninteger counts | 8 ERROR |
| Expected versus observed mismatches | 0 |

Hashes verified that the original runner and existing suite were unchanged. These are deterministic development controls derived from scripted requirements, not product outputs, semantic judge calibration, or held-out effectiveness results.

Run the portable replay from the repository root:

```sh
python3 evals/bootstrap/replay.py
```

It creates a fresh ignored `eval-runs/bootstrap-*` directory containing observations, actual runner stdout/stderr, hashes, and a comparison summary. An optional first argument selects a new output directory. Expected outcomes are derived independently from the scripted approval contract in `replay.py`, so changing the authored expectations cannot silently redefine success.

## Evidence and limits

- [Intent history](evidence/intent.md), [displayed cards](evidence/review-cards.txt), and [scenario revisions](evidence/scenarios.jsonl).
- [Decisions](evidence/decisions.jsonl), [approved handoff](evidence/approved-handoff.json), and [incomplete queue](evidence/incomplete.jsonl).
- [Scenario and evaluator author outputs](evidence/scratch/), [authored cases](fixture/evals/bootstrap-vpn.jsonl), and [case mapping](evidence/case-map.json).
- [Observed validation summary](evidence/validation-summary.json) and [preserved-file hashes](evidence/preservation-before.json).

Checkpoint paths referring to `eval-runs/bootstrap/vpn-support` describe the original exercise workspace. Its retained records are relocated under `evidence/` here; the portable replay uses those paths directly.

Static review found no actionable defect in the playbook, sibling integration, or manifests. All six skill frontmatters validated and changed Markdown's local links resolved. Neither static checks nor this single agent exercise establish performance on unseen projects.

No assistant or ticket system ran. The fixture checks stored action categories and ticket-count deltas; it does not establish response quality, correct account assignment, referral content, reset behavior, or actual resulting ticket state. The original development exercise did not perform semantic judge calibration, independent held-out evaluation, host plugin discovery, or Cross-Examine. The replay reruns the grading controls; it does not rerun the agent interview or prove future agents follow the playbook.

## Follow-up Cross-Examine

A later bounded audit on 2026-11-10 reproduced two validation gaps: an authored input could change the approved decision boundary while retaining its ID and expected action, and rows missing required input/family fields were accepted. Both passed the original 56 action/count controls. The original results above remain valid for their narrow control scope; they did not establish input fidelity or schema acceptance.

The repaired replay validates required fields and compares inputs/families against an eval-owned [approved-input registry](evidence/approved-inputs.json) before grading. The registry preserves the frozen reviewed input representations and adds an equivalent structured S-04 rendering. It accepts JSON formatting/key-order changes and either approved action order; new semantic representations need review and a fixture revision. This fixture mechanism is not a general semantic-equivalence judge. Bootstrap's authoring instructions now require schema and approval fidelity using each target project's format.

The [audit ledger](CROSS_EXAMINE_LEDGER.md) records independent acceptance of both findings and the frozen repair, the before/after results, a clean correction/resume probe, and remaining limits. Replay the recorded artifact attacks and legitimate controls in disposable copies:

```sh
python3 evals/bootstrap/cross_examine.py
```

This reproduces recorded verifier behavior. It does not rerun agent interviews or establish held-out workflow effectiveness.
