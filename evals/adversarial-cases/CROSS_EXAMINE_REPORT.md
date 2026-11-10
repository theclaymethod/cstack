# Cross-Examine: Adversarial Cases

Date: 2026-11-10. Audited frozen C Stack 0.6.0 using disposable playground workspaces; repaired 0.6.1. Two independent attackers and a fresh independent intent reviewer found two mechanisms worth fixing. The [ledger](CROSS_EXAMINE_LEDGER.md) records original intent, roles, versions, actual access, receipts, reductions, teaching changes and limits.

| Confirmed issue | Frozen observation | Repaired observation |
| --- | --- | --- |
| Native ticket schema imposed an unsupported exact-key restriction | Correct four-field ticket PASS; otherwise identical ticket plus `created_at` ERROR. This rejection conflicts with the unchanged written spec/rubric. | Both native candidates PASS. Metadata survives a subsequent request; mutating existing metadata still fails preservation. |
| Fixed construction replay accepted incomplete/contradictory evidence | Missing required treatment observations or command receipt, contradictory raw/parsed output, and two empty source inventories all passed. These are operator calibration probes on copied evidence. | All five probes reject; complete unmodified construction accepts. Native `checked_run` validates the seven retained runs, required coverage/receipt identities are checked, and source inventories match actual files. |

The shared skill's references now teach metadata/representation alternatives, checking required coverage independently of supplied rows, verifying actual source inventory membership, and using native retained-output verification. Bootstrap approval and Cross-Examine adjudication remain with the parent workflows. No source expectation, human approval status, original case or task rubric was rewritten to make a test pass.

## Execution and independent review

The execution attacker performed 76 actual native case executions and four owned-process interruptions, within its 120/4 allowance. It exercised additional lifecycle boundaries, a two-result partial run, interrupted proposal selection, errors, legitimate alternatives, reset observations and reductions. The partial run stayed pending/charged; completed evidence and decisions recovered without reruns. Its first reset wrapper failed with an import-order error; that setup failure and corrected revision are both preserved, rather than relabeled as a target defect.

The semantic attacker performed 71 actual case executions and three interruptions, within its separate 120/4 allowance. It generated valid and invalid output variants, reduced the metadata contrast, and ran one complete construction replay. Validator calibration made no further candidate executions or interruptions. Raw native outputs and original/reduced controls are retained beside the ledger.

The independent reviewer read original intent before scoring, adjudicated both mechanisms before repair, and accepted the frozen five-file core repair. It independently checked raw execution/state, source pins, original and repaired controls, and operator calibration; it did not author or optimize candidates or repairs. The [review](evidence/cross-examine/repair-intent-review.md) records accepted scope and final integration checks. These reviews used retained observations without additional candidate executions or process faults.

## Validation and replay

The portable [audit replay](cross_examine.py) launches the current native construction and the four original/repaired metadata contrasts, then applies the exact evidence mutations to separate copies. Each audit invocation uses **42 actual native case executions and three owned-process interruptions**; evidence mutations execute zero additional candidates. Its clean construction has **103 assertions**, not 103 independent scenarios. The frozen validator/source snapshots are retained for before/after comparison; old evidence and the initial development report remain historical 0.6.0 records.

```sh
python3 evals/adversarial-cases/cross_examine.py --out eval-runs/adversarial-audit
```

Or in a materialized playground:

```sh
python3 scripts/run_cstack_evals.py --suite adversarial-audit --out eval-runs/adversarial-audit-controls
python3 scripts/run_cstack_evals.py --suite all --out eval-runs/cstack-controls
```

Use new output paths. The all-controls run covers eight groups: original calibration/replays/audits, construction replay, the new adversarial audit and native fixture tests. The current native suite has **23 tests**, including the metadata creation/follow-up/preservation regression. The new regression was also run against the original evaluator and failed as expected. All eight skill packages pass validation. [Control summary](evidence/cross-examine/validation/summary.json) and [native test log](evidence/cross-examine/validation/playground.stderr.txt) retain exact local results; [audit results](evidence/cross-examine/validation/audit-results.json) record the contrast and mutation decisions.

## Interpretation

The native schema issue is a false rejection in the playground evaluator. The replay issue is missing consistency/coverage validation in a trusted operator's fixed development control path. Neither establishes a candidate exploit against protected host files, trusted attestation, or a failure of the normal constructor. The known intentionally defective action-only teaching proxy is not counted as a new finding.

These are exposed synthetic development cases, actual local construction and narrowly reproduced preventions. No human labels, high-level expectation approvals, held-out skill effectiveness, unseen generalization, broad reliability, power-loss durability, dependency resilience or security containment is established. Updating guidance is not a measured causal improvement in new generations. Source-sensitive process hooks and full-host permissions remain explicit limitations. Historical attacker scripts/paths describe their original workspaces; use the portable audit command for a relocated replay.
