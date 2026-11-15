---
name: bootstrap
description: Bootstrap evaluators through an product discovery interview, a human-reviewed scenario index, and eval authoring in the target project's format. Use for /bootstrap or when turning a new behavior into its first reviewed evals.
---

# Bootstrap

Turn intent into reviewed scenarios and runnable evaluators for one behavior, preserving adjacent behavior. The user owns acceptable outcomes. [Create Eval](../create-eval/SKILL.md) authors checks; [Run Eval](../run-eval/SKILL.md) executes them; [Cross-Examine](../cross-examine/SKILL.md) provides optional hardening.

## Establish intent

Recover prior decisions and project-specific requirements, examples, authorized traces or fixtures. Production traces and a running implementation are optional; mark unavailable evidence and use explicit requirements plus synthetic proposals. Reuse the native format/runner, preferring Harbor for new executable tasks under [format guidance](../create-eval/references/formats.md). Use the [local package](../run-eval/references/package.md) only when needed; generators/adapters stay project-local.

Explore the product before proposing cases. Inspect its README, actual workflows, existing checks and examples. Report what you observed and identify assumptions. Ask the owner who uses the product, what starts and ends this workflow, and what outcome matters. Interview in short rounds of decisions whose prerequisites are settled. Offer a recommended default and a concrete contrast; wait for the owner before exploring dependent branches. Probe the nearest in-scope and out-of-scope requests, valid alternatives, costly errors, acceptable trade-offs, and what to preserve, clarify, or defer. Spend the interview on choices that would change the coverage. Confirm a short product brief with boundaries, priorities, assumptions and open decisions before turning it into a proposed scenario index.

### Starting with zero, one, or several suites

Inspect suite commands, case files, and actual checks first. Ask “Which part of the product do you want confidence in first?” With existing coverage, suggest a concrete choice: “Your routing suite checks explicit ticket requests. Should we cover guidance-only requests there, or start checking answer correctness?” With no suite or no preference, offer one ordinary workflow and its nearest behavioral contrast. Ask further questions only where answers would change expected behavior or coverage.

Keep one product-level scenario index grouped by workflow. Work on one group per interview; neighboring groups can be a single “later” line. Link existing cases that actually check the expectation. Flag partial coverage, conflicting checks, and approved gaps before generating new rows. Reuse an existing spec or index where possible. Review behavioral changes even when the suite already encodes a default. A case exercising a workflow without asserting the relevant outcome does not cover it.

A product can support several useful eval suites. Describe each candidate by the question it answers, the evidence it needs, and the product decision its result informs. For example, routing checks which action the agent took; answer quality checks whether the returned guidance is correct. The same support request can matter to both. If an existing suite answers the chosen question, extend it. If several suites could work, recommend one initial slice and park the others. Record scenario revision → suite, criterion, and case ID in the index; a pass in one suite covers only that criterion. Keep development and held-out examples separate when reusing a scenario across suites.

## Propose and review scenarios

Read [scenario generation](references/scenarios.md). Give independent authors distinct coverage and the same intent, facts and bounded budget, with separate outputs. They propose feasible conditions before wording and return guessed expectations, not gold or evaluator code. Merge by behavioral distinction, preserve construction families and expose gaps. If delegation is unavailable, disclose local-only coverage.

Use [Adversarial Cases](../adversarial-cases/SKILL.md) for hard boundaries/fault slices and [synthetic methods](../adversarial-cases/references/synthetic-methods.md) when useful. Its construction evidence does not replace approval or adjudication; execution/non-activation status stays explicit.

Write a durable, human-readable scenario index (default `SCENARIOS.md` beside the project's eval spec). Group scenarios by user workflow, including the ordinary path and meaningful boundary contrasts. Lead with the confirmed product brief and coverage gaps. Give each entry a stable ID and revision, situation, expected observable behavior including valid alternatives, rationale, and review status. Present this document for review. Ask which behaviors to approve, correct, or defer. A batch decision can cover explicitly named sections at the displayed revision. Keep executable rows and grader detail out of the interview.

Follow [labeling/checkpoints](references/labeling.md) for exact review scope and history. Expectation approval defines what should happen; it does not label an unseen output. Silence is pending; disapproval does not approve the inverse. Preserve exact reviewed revisions/history. Material changes need renewed review; an explicit correction approves its exact replacement. Keep pending/stale cards outside authoring, including on resume.

## Author and validate

Freeze current approved intent/cards, decision sources, alternatives, exclusions and runner mapping. Dispatch separate evaluator authors through Create Eval; reserve calibration examples/private labels from authors and expose only permitted evidence to the validator. Integrate under one coordinator.

Treat the index as the long-lived coverage map. Derive native rows only from approved, current entries. Record scenario ID/revision → case IDs beside each entry or in a linked mapping when the runner schema is fixed. One entry may need several cases. Mark approved entries awaiting implementation, plus deferred or stale entries, explicitly. On resume reconcile the index, decision history and mapping; a changed expectation reopens the affected entries and rows. Surface behavioral deltas to the owner at index level.

Protect approved source records from author edits. Check full schema and exact input/context/state/family/check fidelity against them: IDs and expected labels alone are insufficient. Return material meaning changes for review. Missing implementation leaves product execution unrun; contract-based checks and partial approved handoffs can still proceed. Preserve incomplete queues.

Before completion, run legitimate, failing, boundary and alternative controls through the real grader. Synthetic controls are not human labels. Semantic judges need explicit outcome labels and [calibration](../create-eval/references/judges.md). Keep families together and exposure honest; Run Eval freezes authorized results, retaining errors and unknowns separately.

Offer bounded Cross-Examine after reviewable evidence; run it when already requested. Bring any proposed repairs back to the user for a behavior-level decision before incorporating them into the approved package. Report package/command, approved/pending counts, covered intent and execution/calibration gaps. Authoring grants no additional publication, product-change or paid-campaign authority.

At decision checkpoints, offer [calibration capture](../expert-mode/references/calibration-capture.md); expectation approval remains distinct from output labeling.

At an automated change checkpoint, offer review now, continue to the agreed stop, or continue for N more rounds. Follow the [change review](../hill-climb/references/change-review.md) rules for inherited cadence and uncommitted experiments. Obtain explicit user acceptance of the proposed changes before any Git commit, including local or worker commits.
