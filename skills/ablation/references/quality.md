# Establishing quality preservation

Use this reference when choosing acceptance evidence, especially for stochastic targets.

Define the quality metric and direction, original baseline, important slices, hard requirements, acceptable loss, sampling unit, repeats, uncertainty method and confirmation rule before selecting on results. A burden objective such as prompt bytes or enabled stages does not replace quality. Retain actual usage, errors, abstentions and fallback outcomes where relevant.

Bind persisted execution ledgers to campaign reservations and retained traces before comparing results. A correct task verdict can coexist with a contradictory accounting receipt; checking only candidate and summary hashes misses that drift. Verify counts and attempt identities across both records, keeping incomplete attempts charged.

## Comparison to the original

For higher-is-better quality let `d = candidate − original baseline`. Under an appropriate sampling design, a one-sided lower confidence bound above `−δ` can support non-inferiority at the predeclared maximum acceptable loss `δ`. This permits improvements; a symmetric equivalence test asks a different question. Choose the margin and confidence procedure from the task's consequences and available evidence, rather than adding a generic percentage or repeat count.

A nonsignificant difference may reflect low power. It is not evidence of equivalence. A point estimate inside the margin may still be inconclusive. Preserve that state. [Original equivalence-testing guidance](https://journals.sagepub.com/doi/full/10.1177/1948550617697177).

Keep all acceptance gates anchored to the original baseline. For example, accepting a small loss at every deletion step can produce a final loss larger than the owner's original allowance. When critical behaviors permit no observed regressions, apply that requirement separately from aggregate quality. Absence of observed regressions on a small sample is not a universal reliability guarantee.

## Trials and exposure

Use paired cases, comparable environments and declared resets. Retain trial-level outcomes and task/family identity. Repeated calls on the same task measure within-task variation; they are not new independent tasks. Dependence, metric structure, sparse failures and sample size affect the validity of a test or interval. Fixed seeds do not make different agent trajectories equivalent. [NLP statistical-testing guide](https://aclanthology.org/P18-1128.pdf).

Keep adaptive screening/validation separate from final confirmation. Repeated selection on a finite noisy criterion can overfit it. Freeze the chosen combined artifact before using reserved evidence; final feedback used for edits becomes development exposure. When no independent evidence exists, limit the claim to the exposed cases. [Selection-bias analysis](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf).

Deterministic finite-fixture comparisons can establish exact outcomes on those cases without statistical population claims. Reuse the project's native grader and keep errors in the selected denominator. For agents, verify real resulting state rather than only a textual success claim. [Agent-evaluation engineering guide](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

## Cost and judges

Measure rendered input size, total input/output/reasoning usage, retries, tool work and elapsed time separately where available. A smaller prompt can cause more output or tool calls; a more capable model can have a different price. Mark unavailable measurements rather than inventing savings.

Keep the approved evaluator fixed during product ablation. [Calibrate Judge](../../calibrate-judge/SKILL.md) owns changes to a judge's application of gold criteria; [Cross-Examine](../../cross-examine/SKILL.md) investigates suspected scoring gaps. Changes to grading semantics establish a new measurement revision and comparable baseline.
