# Controlled operations exercise

Completed the six installed skill workflows through actual local commands in this disposable workspace. Evidence validation recovered **252 native case executions in 34 run directories**, plus **102 deterministic judge worker processes**. There were no native execution errors, UNKNOWNs or incomplete cases. Three separate malformed-output controls correctly returned schema ERROR. Provider/paid calls: zero. Release thresholds remain unset; deployment was not performed.

`manifest.json` inventories every native run with exact IDs, counts, candidate hash and source identity; it also locates candidate snapshots, configurations and deletion diffs. `results.json` is the machine-readable outcome, `usage.json` separates process counters, and `commands.jsonl` records actual workflow argv, exits, stdout and stderr. `execute.py`, `claim_audit.py` and `inspect_results.py` preserve the orchestration and evidence checks.

## Run Eval and Hill Climb

Fresh development executions retained actual outputs, inputs, state, errors and frozen source identity. The original support program passed 4/8; the conforming example passed 8/8 on identical membership. Gains were dev-howto, dev-generic, dev-duplicate and dev-ambiguous. Inspected traces show the baseline creating unauthorized tickets for VPN guidance/trouble reports.

The native 48-case campaign reserved eight confirmation executions and used 32 cases: baseline eight, regression candidate eight, improved candidate eight, and four confirmation cases for each frozen baseline/selection. The 6/8 regression candidate was rejected because dev-closed and dev-unrelated lost previous passes: its outputs reused a closed ticket or another account's ticket. The improved candidate retained all passes, scored 8/8 development and 4/4 confirmation versus baseline 2/4 confirmation. `status` and `verify` completed successfully; no pending attempts remain. Stop reason: confirmation complete, with 16 unused case attempts. The original and rejected evidence remain in `campaign/attempts/`; selected program/diff are `campaign/best.py` and `campaign/best.diff`. The live support program was not replaced.

These are task-contract scores. No human outcome labels were supplied, so human agreement is unavailable.

## Calibrate Judge

Ran the documented offline demonstration once. It produced 24 native source outputs across 12 synthetic task families, with eight rows/four families in each train, validation and final role. The inspected runtime projection has only opaque ID, task request/state/expected reference, output and criterion version; correctness gold, family and selection role remain in the separate private-by-convention label file. This is inspected separation, not enforced filesystem containment. All fixture material is readable.

Retained baseline configs use claim-only policy with typed thresholds 0.8; selected configs use state-witness policy with thresholds 0.5. Both backend shapes and all configurations remain in `judge/campaign/`. The selected artifact is `judge/selected-judge.fixture.json`. The demonstration freezes its final plan and predictions before comparison, records final consumption and rejects refitting. I inspected the resulting plan/exposure state and checked all 96 ordinary persisted predictions against their raw response normalization. Six additional repeatability worker calls account for the full 102 worker processes; they repeat one item per backend and do not add source families.

Final nominal binary results, with failure as the positive class:

| Configuration | N | TP | FN | FP | TN | Kappa | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Typed baseline | 8 | 0 | 2 | 0 | 6 | 0 | 1 |
| Typed selected | 8 | 2 | 0 | 0 | 6 | 1 | 1 |
| LLM-shape baseline | 8 | 0 | 2 | 2 | 4 | -0.333333 | 1 |
| LLM-shape selected | 8 | 2 | 0 | 0 | 6 | 1 | 1 |

All four have zero ERROR/UNKNOWN by both gold classes. Baseline failure catch is zero; selected failure catch is one. The typed baseline false-rejection rate is zero, LLM-shape baseline 2/6, and both selected zero. Whole-family paired 95% percentile bootstrap uses 200 draws over four families. Kappa/failure-catch/false-pass interval bounds are null because 19 replicates have undefined statistics; these replicates were retained rather than dropped. Point perfection supplies no production trust threshold.

Typed fixed fixture probabilities have Brier 0.2975 baseline versus 0.0475 selected and log loss 0.817995 versus 0.229585. These are synthetic event scores, not calibrated forecasts; no probability calibrator was fitted. Additional local controls confirmed yes/failure versus yes/acceptable polarity, and that confidence 0.99 does not replace event probability 0.2. Typed rationales stay null; LLM-shape reasons are fixture text, optional, and carry no native probability. The selected state-witness policy deliberately reuses the native oracle. This establishes neither independent judge learning, real human gold, actual Jev/LLM execution nor live calibration. Real labeled authority, backend/model access and owner acceptance policy remain unavailable.

## Ablation and Bitter Lesson

Ran the documented fixed control schedule, not an agent-discovered optimizer. It completed 164 native cases within its 200-case ceiling, including 20 confirmation cases for five frozen configurations. All quality comparisons stayed anchored to the original baseline, with zero allowable finite-case loss/regressions. The protected task contract could not be deleted; a surviving plan detail without its parent was structurally invalid before execution, distinct from observed behavior failures.

The actual evidence demonstrates combination effects: each duplicate reminder can be removed individually, but their naive union loses dev-duplicate (7/8). The inspected output actually appends a duplicate ticket. Removing either compensating conflict cue alone yields 4/8; their combined deletion restores 8/8. The retained deletion history removes planning/example noise, duplicate-a, and the conflict pair, while rejecting removal of the remaining duplicate reminder. The old-model reduced artifact retains contract, duplicate-b and legacy-auth, with 8/8 development and 4/4 confirmation. Its rendered prompt has 3 units and 3746 UTF-8 bytes.

The shared simplified design retains exactly contract and duplicate-b for both model stand-ins:

| Programmed model | Existing design | Shared simplified design |
| --- | ---: | ---: |
| old-fixture | 4/4 | 2/4 |
| new-fixture | 4/4 | 4/4 |

With design held fixed, model effect is zero. Simplification effect is -0.5 on old-fixture and zero on new-fixture; the programmed interaction is +0.5 on the pass-rate scale. New/simplified passes both original-baseline and new/existing zero-loss gates. This is encoded fixture behavior, not evidence of a real model upgrade's capability.

I extracted actual PROMPT literals from retained candidate ASTs: original 9 units/4193 UTF-8 bytes; selected 2 units/3667 bytes, a 526-byte reduction. The exact extracted text is retained beside this report. `simplification/selected-offline-fixture.py`, `selected.diff`, baseline candidate, native traces and original/configuration records are preserved. Token usage, provider pricing, production latency and cost savings are unavailable. Recorded local subprocess wall time is not model-latency evidence. Confirmation cases remain readable/exposed; the fixed schedule supplies no global or local minimality sweep and no optimizer-discovery claim.

## Cross-Examine

Anchored intent: create one open VPN ticket for the authorized selected account, preserve original records and support legitimate wording/unique IDs. The intentionally defective verifier checks only action=create_ticket. Its supplied forged result was accepted, although its state has no ticket. Executing a candidate that emits this forged object through the native grader fails all eight development cases; on dev-explicit it fails ticket_delta, new_ticket_membership and action_matches_mutation (and its supplied account is also incorrect). This is a reproduced defect in the exercise proxy; the canonical grader already rejects it.

A standalone legitimate alternative uses different explanatory text and alternative-N IDs. Actual native execution passed 8/8, including closed/unrelated record-preservation cases. An observational repaired fixture in `claim-audit/repaired-verifier.py` delegates the complete contract to the unchanged native grader: the forged output fails and the legitimate alternative passes. Raw stdout/stderr, source copies, actual output/state and versioned candidates are retained.

`CROSS_EXAMINE_LEDGER.md` records scope and a project-local generator lesson draft. Independent attacker/defender separation and independent intent reviewer were unavailable under this controlled task. Formal adjudication and repair acceptance remain **unreviewed**. No full independent audit, security containment, canonical grader repair or transfer improvement is claimed.

## Execution and exposure limits

All cases, labels and programmed models are synthetic and readable. Final-role summaries and selected evidence were inspected after workflow completion; no post-final fitting occurred. Local subprocesses retain host permissions. Native hashes and revalidation detect inconsistency but do not establish isolation against a malicious writer.

The initial materialization command used a nonexistent root-level scripts path and failed with no case usage; the corrected fixtures/playground script succeeded. A mistakenly broad filename-only discovery command listed paths elsewhere in the shared working tree; no contents of other versions, tests or prior reports were opened or used. No tests were read or executed. Only this disposable workspace's eval-runs/skill-exercise contains experiment edits; canonical source/evaluator/spec/rubric/cases remain fixed.
