# Co-climb protocol

Use this alongside [Co-Climb](../SKILL.md). [Hill Climb's campaign contract](../../hill-climb/references/campaign.md) owns execution, budgets and recovery; [Calibrate Judge's protocol](../../calibrate-judge/references/protocol.md) owns fitting and label authority. Keep snapshots, runners, adapters and datasets in the project, not in the installed skill.

## Establish the boundary

Record the owner's goal, editable target and judge components, their owners, original criterion meaning, metric direction and aggregation, regression constraints, budget and stopping rule. Preserve the original target and judge as recoverable snapshots.

Identify the climb set, a fresh second set from another author or family, and a sealed final set. Keep dependent originals, repairs and derivatives in the same source family. Record exposure: the two working sets support adaptive selection, not unseen-performance claims. Do not inspect sealed outputs, labels or findings during development.

Record content/configuration hashes for the target and the entire judge bundle: model, rubric, prompt, evidence adapter, parser, thresholds, fallback and retry/cache settings. State unavailable versions rather than guessing them. A block begins from frozen snapshots of both. Evaluate frozen candidates; only the declared side may change between candidates. Never silently replace the bundle that produced a score.

Budget target calls and all judge calls, including generation-loop judgments, controls, re-judging, repetitions and final confirmation. Reserve final work before searching. Preserve partial attempts, errors and unknown costs.

## Check evidence parity

Compare the actual target input with the actual judge payload on representative records before interpreting scores. Check values, units, ranges, statuses, demographics and free-text qualifiers, including null, omitted and transformed fields. An adapter summary is not evidence that every relevant field survived.

Give the judge the same permitted task record, not the target's hidden reasoning or calibration labels. Keep outcome labels, annotation rationales and label-bearing metadata outside runtime payloads. If a missing field explains a disagreement, classify it as evidence mismatch and fix/version the judge adapter before optimizing the target around the omission.

## Target block

1. Freeze the judge bundle, case membership, metric and trial policy. Run at least two identical controls on each working set. Preserve per-case outputs and judgments, not just aggregates.
2. Declare how the control spread is computed in the chosen metric. With two scalar control scores, the observed range is a simple spread. This is an empirical noise floor, not a confidence interval or evidence of statistical significance.
3. Change only the target. Execute it on both working sets under the same judge; saved-output regrading cannot measure a target change.
4. Promote a candidate only if its improvement exceeds the control spread on both sets and satisfies the original constraints. A tie or loss on either set makes the overall result a tie. Preserve regressions and errors in the comparison.
5. Replicate a promotion candidate before making it the next base. Stop as inconclusive if repetitions or budget cannot separate it from controls. Keep the original baseline for final confirmation.

Before each block, use the [handoff prompts](search-prompts.md) to record the active side, immutable evidence and allowed output. Bound the archive size and expansion count. Record parentage and mechanisms, including unsuccessful branches. Partial screens may allocate remaining search budget but cannot confirm a candidate. Retain a tradeoff as exploratory only under the declared family/objective and regression policy; no improvement is established until the promotion gate above passes. Keep several hypotheses when evidence and budget support them, not a fixed quota.

Pool only observations from the same judge build and comparable trial policy. Do not compare a new-judge score directly with an old-judge score.

## Triage and calibration

Review every major finding and abstention. Scan passed outputs for the same defect classes. Assign each item one of: target error, judge gap, judge false positive, evidence mismatch or uncertain. Validate a proposed cluster against the source records with a deterministic scan before producing calibration rows in bulk.

Define the condition named by each calibration row explicitly; condition-present is not automatically a product PASS. Confirmed target errors and judge gaps supply condition-present examples; confirmed false positives supply condition-absent examples. Preserve the original record, exact output, criterion, judge version, finding and adjudication authority.

Agent or deterministic findings keep that provenance; they do not become human gold. Uncertain items stay outside fitting and go to the owner or domain expert as concrete questions with answer options. Use the existing [calibration capture guide](../../expert-mode/references/calibration-capture.md) for retention consent and label authority. Retract invalid rows from active fitting while retaining the amendment and reason.

## Judge block

Freeze the target and saved output corpus. Change only the authorized judge components and calibration data. Narrow changes must trace to confirmed cases, an evidence fix or owner instruction. Changes to criterion meaning need owner adjudication; an easier scoring rule is not a target improvement.

Search judge variants against adjudicated-label agreement, costly class errors and coverage, never the target's product score. Keep complementary judge configurations as alternatives if the policy permits, but select one exact frozen evaluator per target comparison. Do not let candidates choose the judge that scores them best. An ensemble is a new evaluator bundle with its own calibration and budget, not a way to pool incompatible scores.

Before each rebuild, diff the criteria against the original judge, not only the previous revision. Trace every loosening to its evidence or decision. Version the complete rebuilt bundle and re-judge the same saved outputs, including controls and retained candidates, to isolate the scoring change.

Re-measure every retained target change under the new judge on both working sets. If it no longer separates from controls, revoke promotion and restore the previous admissible base within the authorized target snapshot. Mark old ranks stale. A branch can remain exploratory under the archive cap, but its old win cannot authorize selection. Record pruning, retention and rollback reasons. Do not overwrite unrelated live edits. If the judge also participates in generation, saved-output re-judging isolates scoring only: fresh target execution under the new in-loop judge is needed before claiming end-to-end improvement.

After rebuilding, inject known defects into finished outputs. Check both detection and the target loop's actual repair, preserving before/after outputs and judgments. Include legitimate controls so blanket rejection cannot pass this check. Keep synthetic injections labeled as such and out of the sealed set.

## In-loop versus final disagreement

Count final failures whose last in-loop judgment was clean. Use this as a diagnostic for final-judgment noise, not proof from the count alone. First verify identical output identity, criterion, evidence payload and judge bundle at the two stages; then re-judge frozen outputs to measure instability. A parity gap, systematic missed defect or changed output needs its own repair.

Do not assume more passes or consensus gating fixes disagreement. Report what the repeated measurements support and whether any proposed gating change was actually tested.

## Final confirmation and handoff

Freeze the final target, judge and evaluation plan before opening the sealed set. Run the selected target and original baseline once each on that set under the final judge. Complete the planned outputs and predictions before opening any held-out labels. Record the sealed set as consumed; do not use its failures for another tuning pass while retaining an unseen-final claim.

Deliver the decision ledger, retained/dropped target changes and replication evidence, judge changelog, calibration rows and retractions, per-output cost/latency, open expert questions and limits. Every number must identify its judge version and evidence source. Separate synthetic, agent-derived and human-reviewed evidence. A one-shot sealed comparison does not by itself establish statistical significance or production readiness.
