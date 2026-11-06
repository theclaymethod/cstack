# CrossExamine

TLC reached 121 states and 137 steps. The chart draws 9 states and 9 arrows.
The view hides 24 steps, so the chart does not draw them.

## FindingNeedsReplay breaks
The shortest path has 4 steps:
0. Anchor the original eval
1. Freeze intent, scope and access: Attacker seeks a loophole
2. Submit candidate and claim: Replay the attack
3. Observe actual outcome and score: Independent review of finding
4. Save finding verdict and limits: Record evidence and lessons

## RepairNeedsObservedRejection breaks
The shortest path has 7 steps:
0. Anchor the original eval
1. Freeze intent, scope and access: Attacker seeks a loophole
2. Submit candidate and claim: Replay the attack
3. Observe actual outcome and score: Independent review of finding
4. Finding accepted [repair authorized]: Defender proposes a repair
5. Freeze proposed repair: Replay exploit and valid alternatives
6. Collect observed results: Independent review of repair
7. Record repair verdict and limits: Record evidence and lessons

## Rules that hold
TypeOK, ReviewIsIndependent, RepairNeedsFinding, ValidAlternativesRemain, OriginalIntentPreserved, EvidenceBeforeLessons, ReportIsRecorded, NoDeadlock, EventuallyReported
