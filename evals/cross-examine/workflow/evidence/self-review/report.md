# CrossExamine

TLC reached 188 states and 220 steps. The chart draws 9 states and 9 arrows.
The view hides 40 steps, so the chart does not draw them.

## ReviewIsIndependent breaks
The shortest path has 4 steps:
0. Anchor the original eval
1. Freeze intent, scope and access: Attacker seeks a loophole
2. Submit candidate and claim: Replay the attack
3. Observe actual outcome and score: Independent review of finding
4. Save finding verdict and limits: Record evidence and lessons

## Rules that hold
TypeOK, FindingNeedsReplay, RepairNeedsFinding, RepairNeedsObservedRejection, ValidAlternativesRemain, OriginalIntentPreserved, EvidenceBeforeLessons, ReportIsRecorded, NoDeadlock, EventuallyReported
