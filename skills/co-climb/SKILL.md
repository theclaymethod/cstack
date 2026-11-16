---
name: co-climb
description: Use /co-climb to strengthen evals and improve the generator they test over a bounded number of cycles. Start with judge calibration, an adversarial case, or a disputed result.
---

# Co-Climb

Improve the evals and the generator together. Agree on a cycle limit and budget. Choose an entry from the evidence available.

- **Judge first.** Hill-climb the assistant judge on existing eval examples with authoritative expected judgments. Freeze the generator and its outputs. Check whether the judge catches a known defect and accepts a valid alternative.
- **Attacker first.** Use [Adversarial Cases](../adversarial-cases/SKILL.md) to challenge a promise the current evals claim to cover. Try a plausible wrong output and a nearby valid one. Run both through the current evaluator. A missed defect or rejected valid answer calls for an eval repair. A correctly detected generator failure goes straight to generator repair.
- **Disputed result.** Replay the exact output with the evidence the judge saw. Route a scoring gap to the eval side and a confirmed product failure to the generator side. Resolve ambiguous expectations with their owner.

Keep a project ledger of every experiment and adversarial case tried. Before adding a case to the scored suite, judge its relevance to the promise, user consequence, evidence, and distinct coverage. Show a nearby valid answer it must allow. A small detail can matter when it changes the outcome or violates an explicit contract. Reject cosmetic or needlessly pedantic distinctions and record why. Keep disputed expectations open.

One cycle challenges the current pair, repairs the side with a demonstrated gap, and replays the other side against that repair. Run the generator against the strengthened evals. Carry a remaining failure or newly passing output into the next challenge. Record what the evaluator now distinguishes and what the generator now does better, including when either has no confirmed gain. Stop at the agreed cycle limit, when evidence or spend runs out, or when neither side exposes an actionable gap.

Use [the protocol](references/protocol.md) and [block handoffs](references/search-prompts.md). [Hill Climb](../hill-climb/SKILL.md) handles generator trials, [Calibrate Judge](../calibrate-judge/SKILL.md) handles fitting, and [Cross-Examine](../cross-examine/SKILL.md) investigates disputed scoring.

1. Freeze goal, criterion meaning, owners, editable artifacts, complete target/judge identities, working-set families, budget/reserve, constraints and promotion policy. Reserve sealed evidence for final confirmation.
2. Check actual target/judge evidence parity. Triage findings, abstentions and relevant passed outputs. Confirm labels with their real authority; exclude uncertainty from fitting. Repair/version evidence gaps before optimizing the target around them.
3. Choose the next side from confirmed failures, not a fixed cadence. Keep distinct evidence-backed branches within a declared cap, recording parents and exploratory/promoted/pruned status. Exploration and Pareto tradeoffs are not promotion.
4. Execute target changes against one frozen evaluator. Promote only replicated gains beyond control spread on both working sets. Search judges against authoritative labels and costly errors, never generous target scores. Missing policy/comparative evidence leaves selection unresolved.
5. After judge changes, invalidate ranks and re-judge saved baseline/archived outputs. Revoke unsupported promotions. A changed in-loop judge also requires fresh target executions before end-to-end claims.
6. Follow the [change review](../hill-climb/references/change-review.md) cadence. Offer review now, continue to the agreed stop, or continue for N more blocks. Workers return uncommitted candidates and evidence. During a batch the next side may search from a pending candidate; keep the accepted baseline separate. Review accumulated behavior changes at the checkpoint. Obtain explicit acceptance of the exact changes before any Git commit, including on a temporary branch.
7. Freeze the final pair and plan before the once-only sealed comparison. Deliver artifacts, decisions/receipts, replication, judge changes, calibration amendments, costs, questions and limits. Ask the user to approve the final tested pair before adoption, showing what the target does and what the judge accepts. Name each result's judge and source; missing execution stays unrun.
