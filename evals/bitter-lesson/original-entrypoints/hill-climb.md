---
name: hill-climb
description: Improve a selected prompt, skill, program, or agent harness against an existing eval through bounded experiments. Use for /hill-climb or a requested optimization campaign with a defined editable target and evaluator.
---

# Hill Climb

Run a bounded campaign that changes an authorized artifact, executes it, and compares its behavior with a baseline. Deliver the best verified artifact and evidence, including an honest no-improvement result.

Use [Bootstrap](../bootstrap/SKILL.md) or [Create Eval](../create-eval/SKILL.md) when the behavior or evaluator is not established. [Run Eval](../run-eval/SKILL.md) owns faithful execution and scoring; [Cross-Examine](../cross-examine/SKILL.md) investigates suspected scoring gaps.

When the mutable target is the judge itself, [Calibrate Judge](../calibrate-judge/SKILL.md) owns label authority, agreement and confirmation; this skill can supply its bounded search. Product optimization keeps the approved evaluator fixed.

Use [Ablation](../ablation/SKILL.md) when the objective is removal under a quality constraint; [Bitter Lesson](../bitter-lesson/SKILL.md) adds comparisons for model-upgrade simplification.

## Establish the campaign

Inspect project instructions, existing eval commands, candidate entrypoints, data splits, and the user's intent. Recover decisions already supplied. Ask only for missing owner judgments that change the experiment:

- What artifact and components may change? What outcome should improve, and is the aim a particular task or a reusable system?
- What regressions, latency, cost, or other constraints determine whether a candidate is admissible?
- What bounded budget and stopping rule apply? What evidence permits promotion of a candidate?

Keep technical lookups in the project rather than turning them into interview questions. Scope may include instructions, examples, code, model settings, or control flow when authorized. Evaluation inputs, source labels, graders, scoring semantics, and reserved answers stay outside candidate edits. An evaluator defect is separate work with a new revision and comparable baseline.

Write the [campaign contract](references/campaign.md): mutable target, frozen evaluation boundary, objective/direction, case membership, constraints, trial protocol, allowed feedback, budget, confirmation allowance, stopping, and promotion rule. Pin actual model/tool versions where available; retain unknowns honestly. Hash content and configuration, including inputs and runner dependencies. Names and case IDs alone do not establish unchanged evaluation semantics.

See [optimizer choices](references/optimizers.md) when selecting a backend. An agent-led proposal loop is valid; DSPy, Ax, GEPA, and Halo are optional integrations, not installation prerequisites.

For generated training/evaluation data or a DSPy integration, read [the data handoff](references/data-handoff.md). Keep dataset, adapter and dependency code project-local; the shared [generation](../adversarial-cases/references/synthetic-methods.md) and [failure](../adversarial-cases/references/failure-methods.md) references help choose a method.

## Execute the baseline

Run the original target through the actual execution boundary and capture fresh outputs, tool/state evidence where applicable, per-case verdicts, errors, resource usage, and artifact/configuration identity. Regrading stored outputs can check a grader but cannot measure a changed target. Missing execution setup leaves the campaign unrun; prepare the contract and identify the missing entrypoint.

Check applicable schema, case membership, reset, and representative legitimate outcomes before optimizing. Exercise malformed output too: enforce declared required/extra-field and nonempty-value rules through the same grading path, so a high score cannot bypass the output contract. Preserve an independently recoverable baseline artifact and its evidence. For stochastic targets, use the declared repeat/seed/judge/cache protocol; use paired comparisons where meaningful. A run exception, missing result, or unavailable observation remains distinct from a behavior failure.

## Diagnose and propose

Read per-case evidence and inspect representative failures and existing successes. State a concrete hypothesis: the observed mechanism, the proposed change, expected affected cases, and nearby behavior that could regress.

Make attributable candidates within the authorized scope. Snapshot candidate content and parentage before execution. Parallel proposals use separate copies and run state; one coordinator owns integration. Start with independent hypotheses when useful, then record which later proposals depend on earlier results.

Feed proposers evidence relevant to the hypothesis: failed assertions, actual outputs, trace excerpts, source-bound observations, and measured costs. Keep interpretation separate from verifier facts. Search labels and examples may be used when the task permits them; reserved evidence and final-test feedback follow the declared exposure policy.

## Evaluate and retain

Before each execution, verify the frozen contract and reserve enough remaining budget for the declared operation, including confirmation. Count baseline runs, retries, screening, optimizer/proposer work, and final checks in the applicable counters. Record measured and unknown costs separately. A library's metric-call counter is not automatically the campaign's total spend.

Execute the changed artifact with the declared trials and complete selected membership. Record actual evaluated IDs, per-case outcomes, errors, comparisons, and costs. Partial or cheap screening can nominate a candidate; it does not satisfy the full confirmation protocol. Validate source/schema fidelity as well as expected scores, and reject contract drift rather than silently rebasing.

Test any merged candidate as a new artifact. Preserve rejected attempts and the baseline; stop or narrow the campaign when evidence shows the premise or search direction needs reconsideration.

## Confirm and select

Confirm shortlisted candidates against the baseline using the agreed comparison, regression checks, and evidence volume. Repeatedly consulted validation cases are adaptive selection evidence. Independently reserved cases can support stronger claims only when they actually stayed outside fitting and opening them is authorized. Without independent evidence, report improvement on the exposed cases rather than generalization.

Apply the owner's objective and constraint policy to per-case outcomes as well as the aggregate. Leave inconclusive comparisons inconclusive; neither a tiny gain nor a perfect small run establishes a universal trust threshold.

Promote only a candidate that satisfies the declared confirmation and admissibility rules. If none does, retain the baseline and report no verified improvement. Deliver a selected candidate as a reviewable artifact/diff; apply it to the authorized target when that is the requested promotion behavior and the working target has not acquired unrelated changes. Publishing, deployment, new paid budgets, or broader product changes need their own existing authorization.

## Stop, resume, and report

Stop at the declared budget, deadline, plateau, target, or user instruction. Preserve the best verified artifact even if the last proposal fails. Write durable state before and after executions so an interruption leaves an attempt visibly incomplete. If execution finished before its ledger update, reconcile complete native evidence with the original reservation and frozen contract before recovering its result or decision; avoid a new execution or charge for that reconciliation. Partial, invalid, or mismatched evidence stays incomplete and charged. Resume only after checking the exact target/eval/configuration and exposure history; use a new campaign for a changed contract. An interrupted execution may have consumed resources and must not be retried as free work.

Report the selected artifact and diff, baseline and candidate identities, measured capability, per-case changes and regressions, actual runs/costs, stopping reason, and remaining uncertainty. Distinguish search retention, development improvement, confirmation, and product/generalization claims. If no candidate earns promotion, make the retained baseline and unresolved opportunity concrete.
