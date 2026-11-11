---
name: co-climb
description: Improve a generator and the LLM judge that scores it in alternating, frozen blocks while the judge is still being calibrated. Use for /co-climb, or when a hill climb's failures are as likely to be judge errors as target errors.
---

# Co-Climb

Improve a target and its immature judge together without letting either grade its own changes. Every block freezes both. A target block changes only the target; a judge block changes only the judge and its calibration data. [Hill Climb](../hill-climb/SKILL.md) owns campaign mechanics against a fixed evaluator, [Calibrate Judge](../calibrate-judge/SKILL.md) owns judge fitting, and [Cross-Examine](../cross-examine/SKILL.md) adjudicates disputed scoring. Read [the protocol](references/protocol.md) and [confirmed lessons](references/lessons.md). Keep runners, adapters and data project-local.

## Contract and evidence parity

Recover the owner's goal, the target and judge artifacts, who may change each, and the criteria whose meaning is fixed. Name three case sets: a climb set, a fresh second set from a different author or family, and a sealed set run once at the end. The sealed set never feeds triage, prompts or calibration. Budget the judge calls made during generation and re-judging as well as target calls.

Check evidence parity before the first block. The judge must receive the same record the target used, including values, units, ranges, statuses, demographics and free-text qualifiers. When the adapter drops a field, correct output looks unsupported and a target that happens to omit the field looks better. A parity fix is a judge change and starts a new judge version.

## Measure against noise

Each block runs at least two identical controls per set on one frozen judge build. Their spread is the noise floor. Keep a target change only when it beats that spread on both sets, then replicate it before it becomes the base. Pool only runs scored by the same judge build. A gain on one set with a tie or loss on the other is a tie.

When only the judge changes, re-judge saved outputs instead of generating new ones. This isolates the judge's effect and often shows that an earlier target win was a parity gap. Re-measure every retained change on each new judge version, and revert changes that no longer separate from controls.

## Triage every failure

Triage every major finding and abstention, not only the largest cluster. Scan outputs the judge passed for the defect classes you found. Classify each item as a target error, judge gap, judge false positive, evidence mismatch or uncertain. Before writing rows in bulk for a claimed cluster, check the claim against the record with a deterministic scan.

Confirmed target errors and judge gaps become condition-present calibration rows. Confirmed false positives become condition-absent rows. Keep references to the exact output, record and judge version. Uncertain items go to the owner or a domain expert as concrete questions with answer options, and stay out of calibration until answered. Offer [calibration capture](../expert-mode/references/calibration-capture.md) for those answers. Remove rows later shown to be wrong and record the removal.

## Revise the judge

Change criteria narrowly, and only for confirmed cases, an evidence fix or an owner instruction. Before each rebuild, diff the criteria against the original judge and trace every loosening to its cause. After each rebuild, plant known defects in finished outputs and confirm that the judge catches them and the target's loop repairs them.

When the judge runs inside the target's loop, count failing runs whose last in-loop pass was clean. If most are, the remaining failures come from noise in the final judgment, and more passes or consensus gating will not remove them.

## Confirm and deliver

Freeze the final target and judge. Run the target and the baseline once on the sealed set under that judge. Deliver the decision ledger, retained and dropped changes with their evidence, the judge changelog and calibration rows, cost and latency per output, open expert questions and limits. State which results come from synthetic cases and which judge version produced each number.
