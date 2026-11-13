---
name: co-climb
description: Improve an agent, prompt, skill, or program and the LLM judge that scores it through alternating, bounded searches. Use for /co-climb, or when a hill climb's failures are as likely to be judge errors as target errors.
---

# Co-Climb

Improve a target and its immature judge together without letting either grade its own changes. Snapshot both sides at every block boundary. A target block searches only the target against a fixed judge; a judge block searches only the judge against frozen outputs and adjudicated labels. [Hill Climb](../hill-climb/SKILL.md) owns campaign mechanics against a fixed evaluator, [Calibrate Judge](../calibrate-judge/SKILL.md) owns judge fitting, and [Cross-Examine](../cross-examine/SKILL.md) adjudicates disputed scoring. Read [the protocol](references/protocol.md), use [the block handoff prompts](references/search-prompts.md), and consult [lessons and their evidence status](references/lessons.md). Keep runners, adapters and data project-local.

## Contract and evidence parity

Recover the owner's goal, the target and judge artifacts, who may change each, and the criteria whose meaning is fixed. Name three case sets: a climb set, a fresh second set from a different author or family, and a sealed set run once at the end. The sealed set never feeds triage, prompts or calibration. Budget the judge calls made during generation and re-judging as well as target calls.

Check evidence parity before the first block. The judge must receive the same record the target used, including values, units, ranges, statuses, demographics and free-text qualifiers. When the adapter drops a field, correct output looks unsupported and a target that happens to omit the field looks better. A parity fix is a judge change and starts a new judge version.

## Search without collapsing too early

Set a branch cap and per-block budget before proposing. Keep a small archive of different hypotheses with parent IDs, artifact hashes, evidence, and status: exploratory, replicated, promoted or pruned. Extend more than one promising branch when budget permits. A partial screen or a tradeoff can justify further exploration, never promotion. Do not keep dominated branches merely to fill the cap; when only one branch has evidence, continue it or stop.

Compare branches only under the same judge bundle, case membership and trial policy. Retain complementary candidates using a declared per-family or multi-objective policy; protect costly errors and original constraints before aggregate gains. A Pareto tradeoff is not a confirmed improvement. Test merged branches anew. Preserve rejected trials and why they stopped.

Use failures to choose the next side: confirmed target defects lead to target search; judge gaps, false positives or evidence mismatches lead to calibration first. Never alternate just to satisfy a cadence. Judge proposals learn from adjudicated traces, not from which prompt awards the current agent the highest score.

## Measure against noise

Each block runs at least two identical controls per set on one frozen judge build. Their spread is the noise floor. Promote a target change only when it beats that spread on both sets, satisfies the constraints, and replicates. Other admissible candidates may remain exploratory within the branch cap; they do not replace the base. Pool only runs scored by the same judge build. A gain on one set with a tie or loss on the other is a tie.

When only the judge changes, re-judge saved outputs instead of generating new ones. This isolates the judge's effect and often shows that an earlier target win was a parity gap. Re-measure the baseline and archived target candidates on each new judge version. Invalidate old rankings; remove promotion from changes that no longer separate from controls, and prune or retain them only as explicitly budgeted exploratory branches.

## Triage every failure

Triage every major finding and abstention, not only the largest cluster. Scan outputs the judge passed for the defect classes you found. Classify each item as a target error, judge gap, judge false positive, evidence mismatch or uncertain. Before writing rows in bulk for a claimed cluster, check the claim against the record with a deterministic scan.

Confirmed target errors and judge gaps become condition-present calibration rows. Confirmed false positives become condition-absent rows. Keep references to the exact output, record and judge version. Uncertain items go to the owner or a domain expert as concrete questions with answer options, and stay out of calibration until answered. Offer [calibration capture](../expert-mode/references/calibration-capture.md) for those answers. Remove rows later shown to be wrong and record the removal.

## Revise the judge

Selecting a judge is an evidence-backed decision, not a placeholder for the next step. If the acceptance policy or comparative calibration results are missing, leave the selected judge unresolved and recover that evidence first. Naming an available judge does not make it the approved evaluator. Separate proposed actions from completed selection in every handoff.

Change criteria narrowly, and only for confirmed cases, an evidence fix or an owner instruction. Before each rebuild, diff the criteria against the original judge and trace every loosening to its cause. After each rebuild, plant known defects in finished outputs and confirm that the judge catches them and the target's loop repairs them.

When the judge runs inside the target's loop, saved-output re-judging isolates scoring, not changed generation behavior. Run fresh target executions before claiming end-to-end gains. Count failures with a clean last in-loop judgment, check output/evidence/bundle identity, then repeat frozen judgments before attributing disagreement to noise. Test any proposed extra passes or consensus gating; do not assume they fix it.

## Confirm and deliver

Freeze the final target and judge. Run the target and the baseline once on the sealed set under that judge. Deliver the decision ledger, retained and dropped changes with their evidence, the judge changelog and calibration rows, cost and latency per output, open expert questions and limits. State which results come from synthetic cases and which judge version produced each number.
