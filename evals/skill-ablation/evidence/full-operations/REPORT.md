# Installed-skill operations exercise

All requested workflows ran in this disposable workspace using its installed skills and existing native execution paths. The 34 native run directories contain **252 actual candidate case processes**: 198 PASS, 54 intentional/observed FAIL, zero ERROR/UNKNOWN, zero incomplete. Judge work additionally used **102 deterministic response processes**. These pooled counts are accounting, not a product-performance estimate. Provider, network and paid calls, new dependencies and nested agents: zero.

`manifest.json` locates every native run, exact IDs, source identity, candidate snapshot and judge run. `commands.jsonl` records workflow argv, cwd, exit, elapsed process time and stdout/stderr files. `usage.json`, `inspection.json` and `result-summary.json` provide machine-readable accounting, consistency checks and outcomes. Core evaluator/spec/rubric/cases and the original support agent are unchanged; current hashes match every native run's frozen identity. Python/runtime identity is preserved by native manifests.

## Run Eval and Hill Climb

Original development result: 4/8 PASS, 4 FAIL; conforming example: 8/8 PASS. Every output/state/error and source snapshot is retained in `run-original/` and `run-conforming/`. Exact development membership matches. Gains: how-to, generic trouble report, duplicate, ambiguous account. These are synthetic task scores; no human outcome labels or human-agreement measurement were supplied.

The native campaign used 32 of its 48-case allowance, including all eight reserved confirmation executions. Baseline 4/8; regression example 6/8, rejected because `dev-closed` and `dev-unrelated` changed from PASS to FAIL. Its earlier evidence remains in `hill-climb/attempts/`. The conforming example reached 8/8, with baseline/candidate confirmation 2/4 versus 4/4 and zero regressions. Native `finish` selected attempt 2 and `verify` validated completed evidence. The reviewable snapshot/diff are `hill-climb/best.py` and `best.diff`; the live product was not replaced. Stop reason: confirmation complete, with 16 cases unspent. This was supplied-candidate selection, not independently discovered optimization.

## Calibrate Judge

The documented offline demonstration produced 24 native source rows across 12 families: eight rows/four families each for train, validation and final workflow roles. Public inputs contain opaque IDs, criterion version, actual output and permitted expected task behavior; gold, family, role and provenance remain in separate label rows. Both outputs for each source task stay in one role. Inspected projections, raw responses, normalization and campaign-anchored hashes agree. These ordinary files and host processes provide no malicious-access containment.

Baseline configs are claim-only at 0.8; both selected fixtures are state-witness at 0.5. Final plans/configurations and all predictions were frozen before final comparison; the state is `final_consumed`, exposes train/validation/final and rejects further fitting. All data are readable synthetic material. Final feedback is now exposed; this is not blind or human-gold calibration. The state-witness policy deliberately reuses the native oracle.

| Final fixture | Agreement | Nominal kappa | TP / FN / FP / TN | Coverage |
| --- | --- | --- | --- | --- |
| Typed baseline | 6/8 | 0 | 0 / 2 / 0 / 6 | 8/8 |
| Typed selected | 8/8 | 1 | 2 / 0 / 0 / 6 | 8/8 |
| LLM baseline | 4/8 | -1/3 | 0 / 2 / 2 / 4 | 8/8 |
| LLM selected | 8/8 | 1 | 2 / 0 / 0 / 6 | 8/8 |

Failure is positive. Baseline typed/LLM false-pass rates among gold failures are 2/2; false rejections among gold passes are respectively 0/6 and 2/6. Selected rates are 0/2 and 0/6. Errors/UNKNOWN are zero by both gold classes. Each final comparison has six gold passes and two failures. The four-family, 200-draw paired bootstrap leaves kappa/failure-catch/false-pass intervals undefined because 19 draws have undefined denominators; those draws were not discarded. Point kappa alone does not establish readiness.

Typed probabilities are synthetic 0.15/0.65, with Brier 0.2975 baseline versus 0.0475 selected; they are not calibrated forecasts. Concentration confidence is distinct from event probability; typed explanations are absent. LLM verdicts have optional fixture reasons and no event probabilities. Additional local normalization controls cover polarity, Choice probabilities, confidence, malformed/missing responses and absent explanations; one-class kappa remains undefined. Three repeats on one frozen item per backend are deterministic stability checks, not six new gold items. The 102 processes comprise 96 scheduled predictions and six repeats. No live Jev/LLM backend, probability-calibrator fit, weight training or human calibration occurred. Selected artifact: `judge-calibration/selected-judge.fixture.json`; owner release policy remains null.

## Ablation and Bitter Lesson

The documented fixed demonstration used 164/200 native cases, including all 20 reserved confirmation cases, with zero observed loss/regression allowed against the original full old-model baseline. It tests protected/dependent units separately from behavior failures. The contract cannot be removed; retaining `plan-detail` after deleting `plan` is invalid before execution. Each duplicate reminder alone is removable, but their union loses `dev-duplicate` (7/8). Single conflict removals each score 4/8, while deleting the conflict pair succeeds. Combined accepted old-model deletions retain contract, duplicate-B and legacy authorization: 8/8 development, 4/4 confirmation; 3 units and 3,746 rendered UTF-8 bytes.

The selected new-model design retains contract and duplicate-B: 2 units, **3,667 bytes**, versus the original 9 units and **4,193 bytes**, a deletion of 526 bytes. AST inspection of actual candidate prompt constants confirms those byte counts and that both model rows use the identical simplified prompt.

| Stand-in | Existing design, development / confirmation | Shared simplified design, development / confirmation |
| --- | --- | --- |
| Old fixture | 8/8 / 4/4 | 4/8 / 2/4 |
| New fixture | 8/8 / 4/4 | 8/8 / 4/4 |

The selected new bundle matches both original-baseline and new-model-existing quality with zero observed regressions. Existing-design model effect is zero, new-model simplification effect zero, old-model simplification effect -0.5; the encoded interaction is +0.5. These are programmed stand-ins, not evidence of actual model capability or causal production improvement. Final membership was frozen before five confirmation configurations, with further fitting, duplicate and unplanned final calls refused. Cases remain exposed/readable. The command is a fixed control schedule: no discovered optimizer, global minimality, statistical non-inferiority or unseen generalization claim. `simplification/selected-offline-fixture.py`, `selected.diff`, candidate snapshots and native traces preserve exact decisions. Token usage, model costs and production latency savings are unavailable; local process duration is not model latency.

## Cross-Examine and limits

The intentionally defective proxy accepted a forged success claim with no created ticket. The forged candidate earned 0/8 native development passes (eight FAIL); the legitimate alternative passed 8/8 using different unique IDs and note wording. A matched forgery preserves the correct account and unrelated tickets but appends nothing: the original proxy accepts it, while the native grader and copied repaired entrypoint reject its mutation/delta/membership checks. The copied repair accepts the legitimate alternative. Canonical scoring was not changed. See `claim-audit/replay-results.json`, ledger, local teaching note and repaired entrypoint.

Independent attacker/defender/reviewer roles were unavailable; formal intent and repair adjudication remain **unreviewed**. This is a reproduced supplied proxy flaw, not a full independent audit or a new native-grader vulnerability. The local teaching note remains proposed pending independent review.

An exploratory inspector first assumed a list was a dictionary; a later inspector compared canonical JSON receipt hashes with pretty-printed file bytes. Both inspection errors are disclosed in `inspection.json`; the corrected inspector passed without changing source/run evidence or launching additional candidate/worker processes. The expected copied-verifier rejection exits 1 and is preserved as behavior, not an execution error. Release thresholds remain unset and deployment unperformed. Real human gold, owner acceptance policy, supported live backend identity/budget and production validation remain absent.
