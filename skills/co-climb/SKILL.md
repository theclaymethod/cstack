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
6. Within the search, promotions select experimental parents only. After each completed target climb, judge calibration or cross-examination that proposes changes, the coordinator presents the user with each behavior change, a before/after case and relevant regressions or uncertainty. Ask which changes to keep and wait for explicit approval before carrying them into the next block. Workers return proposals to the coordinator. Record the decision against the reviewed candidate identities; keep the last approved baseline if declined. Trial branches inside a block can run autonomously.
7. Freeze the final pair and plan before the once-only sealed comparison. Deliver artifacts, decisions/receipts, replication, judge changes, calibration amendments, costs, questions and limits. Ask the user to approve the final tested pair before adoption, showing what the target does and what the judge accepts. Name each result's judge and source; missing execution stays unrun.
