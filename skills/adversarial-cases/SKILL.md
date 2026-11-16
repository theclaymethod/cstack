---
name: adversarial-cases
description: Challenge existing evals with harder situations implied by the product spec. Review for over-specification and drift, maintain situations.md, and hand supported cases to Create Eval. Also construct reproducible fault cases for scoped audits.
---

# Adversarial Cases

Start with what the current evals let through. Read their inputs, assertions and observed results alongside the developer’s decisions, product examples and approved scenario index. Identify a promise that a generator could break while still passing. Cite the evidence for that reading and label any inference.

Vary a condition the existing cases take for granted. Hypothesize a plausible wrong outcome and a nearby valid alternative. Try both against the current grader when runnable and record what it actually distinguished. Ask what breaks for the user, whether the same promise applies, and whether the proposed check would reject something the developer allows. Drop cosmetic preferences and merge duplicate coverage. If the expectation requires a new product decision, record the concrete question for the owner and continue with supported cases.

Update the project’s `situations.md` in place. Give each distinct situation a stable ID, its parent scenario or eval, the changed condition, expected observable behavior, valid alternatives, and the source or open question. Mark it supported, open, merged or rejected with a short reason. Reuse IDs on reruns. Append each disposition and its evidence to the [shared decision ledger](../create-eval/references/decision-ledger.md). Pass its path and situation IDs to the next skill.

Use [Create Eval](../create-eval/SKILL.md) to turn supported situations into new rows in the project’s native eval format. Verify the rows against the wrong outcome and valid alternative, and link their IDs back to the situation. A request limited to brainstorming ends with the index. Downstream skills can consume the resulting suite and follow those links to the decision. The parent retains authority over disputed expectations and findings.

## When a challenge needs execution

Use the [case contract](references/case-contract.md) for exact inputs, source families, permissions, budget, reset and outcome witnesses. For a fault case, follow [injection and reduction](references/injection.md) through the real runner. Record whether the fault was armed, activated and observed, then replay the clean and legitimate-alternative controls. Keep unexecuted hypotheses labeled as proposals. [Synthetic methods](references/synthetic-methods.md) and [failure methods](references/failure-methods.md) cover case construction.

Return unresolved intent to [Bootstrap](../bootstrap/SKILL.md). For a scoring dispute, give [Cross-Examine](../cross-examine/SKILL.md) the reproducible discrepancy, controls and independent outcome witness. Route confirmed review signals through the parent’s [calibration capture](../expert-mode/references/calibration-capture.md).
