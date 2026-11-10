# Validation and limits


The [expert-review suite](../evals/expert-review/README.md) has six synthetic conversation cases and 19 calibration controls. All 19 controls passed. The initial agent pilot passed five of six artifact graders. A focused rerun later passed after a reproduced grader defect was fixed. These development results do not establish performance on unseen cases or domain expertise. The [report](../evals/expert-review/REPORT.md) and [ledger](../evals/expert-review/CROSS_EXAMINE_LEDGER.md) describe the incomplete review coverage and other limits.

```bash
python3 evals/expert-review/calibration.py eval-runs/expert-calibration
```

The [Cross-Examine suite](../evals/cross-examine/README.md) has five audit cases, 11 calibration controls, and exercises that check whether a generator applies a learned lesson to a related task. All 11 controls passed. Local calibration needs Python 3.11+ with standard-library SQLite serialization support. Local execution uses the host user's permissions. Docker is optional for isolated execution. The capture skills do not require it.

The [workflow chart and model checks](../evals/cross-examine/workflow/README.md) describe the attacker, defender, and independent intent reviewer. Five weakened model configurations produced counterexamples when safeguards for independent judgment, observed replay, valid alternatives, or original intent were removed. The model checks do not prove that agents follow the playbook.

```bash
python3 evals/cross-examine/calibration.py eval-runs/cross-calibration
```

These 30 controls check the original suites' grading machinery. A [before/after skill comparison](../evals/shortened-skills/REPORT.md) adds fresh capture, authoring, stored-output execution, and repair-review exercises. It addresses an authoring control gap and two verifier-repair edge cases. The shared SQL-task ambiguity is [resolved in fixture v5](../evals/cross-examine/evidence/contract-v5/REPORT.md): updates must preserve collection membership. Fresh adversarial search was blocked by automatic review, and held-out effectiveness remains unverified.

| Component | Recorded checks | Limits |
| --- | --- | --- |
| Bootstrap | A [synthetic development exercise](../evals/bootstrap/REPORT.md) covered the interview, two scenario authors, explicit approval/correction/deferral, two evaluator authors, and 56 deterministic grader-control verdicts with no mismatches. A later [Cross-Examine audit](../evals/bootstrap/CROSS_EXAMINE_LEDGER.md) reproduced and repaired input-fidelity and required-field validation gaps. | One scripted fixture; no product execution, human judge calibration, held-out effectiveness, or host plugin discovery. |
| Create Eval | A [Create Eval review](../evals/create-eval/REPORT.md) covered three review areas and six attempts against v0.3.0 without reproducing a confirmed flaw. It checked trace changes, review amendments, and restarts, and included agent-authored development examples. | The verifier review analyzed the specification. These checks do not establish end-to-end skill performance. The [ledger](../evals/create-eval/CROSS_EXAMINE_LEDGER.md) records the remaining gaps. |
| Local trace reviewer | Seventeen HTTP and persistence checks passed with synthetic data. Python and JavaScript syntax checks passed. | Browser access was disabled during validation, so rendering and browser interaction remain unverified. |
| Export helper | Local checks used synthetic data and a simulated model adapter. | Actual Privacy Filter inference and PII-detection performance remain unverified. |

The repo contains no patient records or real expert-session datasets. Historical evidence keeps its original versions, source records, and repository names. Use the installation commands above for the current pack.


Additional project-local generation, fault injection and DSPy compatibility results are in the [methods report](../evals/methods/REPORT.md). These remain exposed synthetic development evidence.

The [Calibrate Judge report](../evals/calibrate-judge/REPORT.md) adds offline agreement, typed/LLM normalization, bounded selection and final-exposure controls. Its simulated outcomes are separate from real model/human-gold calibration. The [simplification report](../evals/simplification/REPORT.md) adds deletion interactions, original-baseline gates and a simulated model-migration comparison. All eleven control groups passed. Of 56 native tests, 55 passed and the optional DSPy SDK check was skipped; these are mechanics checks, not real-model simplification results.

The [Ablation/Bitter Lesson audit](../evals/simplification/CROSS_EXAMINE_LEDGER.md) confirms and repairs durable-ledger drift under an operator fault. The [skill-pack ablation](../evals/skill-ablation/REPORT.md) compares full and shortened instructions with eight fresh agent exercises, frozen native scoring and exposed confirmation cases.
