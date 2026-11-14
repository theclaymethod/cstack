---
name: co-climb
description: Improve an agent, prompt, skill, or program and its LLM judge through alternating bounded searches. Use for /co-climb or when apparent target failures may be judge errors.
---

# Co-Climb

Search one side while freezing the other. Read [the protocol](references/protocol.md) before execution and use [the block handoffs](references/search-prompts.md). [Hill Climb](../hill-climb/SKILL.md) owns target execution/recovery; [Calibrate Judge](../calibrate-judge/SKILL.md) owns fitting; [Cross-Examine](../cross-examine/SKILL.md) investigates disputed scoring. Keep implementations project-local. [Lessons](references/lessons.md) state evidence limits.

1. Freeze goal, criterion meaning, owners, editable artifacts, complete target/judge identities, working-set families, budget/reserve, constraints and promotion policy. Reserve sealed evidence for final confirmation.
2. Check actual target/judge evidence parity. Triage findings, abstentions and relevant passed outputs. Confirm labels with their real authority; exclude uncertainty from fitting. Repair/version evidence gaps before optimizing the target around them.
3. Choose the next side from confirmed failures, not a fixed cadence. Keep distinct evidence-backed branches within a declared cap, recording parents and exploratory/promoted/pruned status. Exploration and Pareto tradeoffs are not promotion.
4. Execute target changes against one frozen evaluator. Promote only replicated gains beyond control spread on both working sets. Search judges against authoritative labels and costly errors, never generous target scores. Missing policy/comparative evidence leaves selection unresolved.
5. After judge changes, invalidate ranks and re-judge saved baseline/archived outputs. Revoke unsupported promotions. A changed in-loop judge also requires fresh target executions before end-to-end claims.
6. Follow the [change review](../hill-climb/references/change-review.md) cadence. Offer review now, continue to the agreed stop, or continue for N more blocks. Workers return uncommitted candidates and evidence. During a batch the next side may search from a pending candidate; keep the accepted baseline separate. Review accumulated behavior changes at the checkpoint. Obtain explicit acceptance of the exact changes before any Git commit, including on a temporary branch.
7. Freeze the final pair and plan before the once-only sealed comparison. Deliver artifacts, decisions/receipts, replication, judge changes, calibration amendments, costs, questions and limits. Ask the user to approve the final tested pair before adoption, showing what the target does and what the judge accepts. Name each result's judge and source; missing execution stays unrun.
