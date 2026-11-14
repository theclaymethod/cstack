---
name: bootstrap
description: Bootstrap evaluators through an intent interview, parallel scenario generation, human approval of proposed expectations, and eval authoring in the target project's format. Use for /bootstrap or when turning a new behavior into its first reviewed evals.
---

# Bootstrap

Turn intent into reviewed scenarios and runnable evaluators for one behavior, preserving adjacent behavior. The user owns acceptable outcomes. [Create Eval](../create-eval/SKILL.md) authors checks; [Run Eval](../run-eval/SKILL.md) executes them; [Cross-Examine](../cross-examine/SKILL.md) provides optional hardening.

## Establish intent

Recover prior decisions and project-specific requirements, examples, authorized traces or fixtures. Production traces and a running implementation are optional; mark unavailable evidence and use explicit requirements plus synthetic proposals. Reuse the native format/runner, preferring Harbor for new executable tasks under [format guidance](../create-eval/references/formats.md). Use the [local package](../run-eval/references/package.md) only when needed; generators/adapters stay project-local.

Ask short rounds about triggers, observable success, unacceptable outcomes, valid alternatives, preserved behavior and clarification/defer boundaries. Resolve technical facts locally. Record the intent revision and unresolved decisions; coverage priorities, budgets and trust targets remain owner choices.

## Propose and review scenarios

Read [scenario generation](references/scenarios.md). Give independent authors distinct coverage and the same intent, facts and bounded budget, with separate outputs. They propose feasible conditions before wording and return guessed expectations, not gold or evaluator code. Merge by behavioral distinction, preserve construction families and expose gaps. If delegation is unavailable, disclose local-only coverage.

Use [Adversarial Cases](../adversarial-cases/SKILL.md) for hard boundaries/fault slices and [synthetic methods](../adversarial-cases/references/synthetic-methods.md) when useful. Its construction evidence does not replace approval or adjudication; execution/non-activation status stays explicit.

Follow [labeling/checkpoints](references/labeling.md): present stable card IDs, situation, guessed behavior and reason for approval, correction or deferral. Expectation approval defines what should happen; it does not label an unseen output. Silence is pending; disapproval does not approve the inverse. Preserve exact reviewed revisions/history. Material changes need renewed review; an explicit correction approves its exact replacement. Keep pending/stale cards outside authoring, including on resume.

## Author and validate

Freeze current approved intent/cards, decision sources, alternatives, exclusions and runner mapping. Dispatch separate evaluator authors through Create Eval; reserve calibration examples/private labels from authors and expose only permitted evidence to the validator. Integrate under one coordinator.

Protect approved source records from author edits. Check full schema and exact input/context/state/family/check fidelity against them: IDs and expected labels alone are insufficient. Return material meaning changes for review. Missing implementation leaves product execution unrun; contract-based checks and partial approved handoffs can still proceed. Preserve incomplete queues.

Before completion, run legitimate, failing, boundary and alternative controls through the real grader. Synthetic controls are not human labels. Semantic judges need explicit outcome labels and [calibration](../create-eval/references/judges.md). Keep families together and exposure honest; Run Eval freezes authorized results, retaining errors and unknowns separately.

Offer bounded Cross-Examine after reviewable evidence; run it when already requested. Bring any proposed repairs back to the user for a behavior-level decision before incorporating them into the approved package. Report package/command, approved/pending counts, covered intent and execution/calibration gaps. Authoring grants no additional publication, product-change or paid-campaign authority.

At decision checkpoints, offer [calibration capture](../expert-mode/references/calibration-capture.md); expectation approval remains distinct from output labeling.
