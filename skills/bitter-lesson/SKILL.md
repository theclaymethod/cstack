---
name: bitter-lesson
description: Revisit production prompts, context, and scaffolding when upgrading models, testing which legacy steering and workarounds can be removed across model-by-design comparisons. Use for model-migration simplification—not for same-model deletion alone (ablation).
---

# Bitter Lesson

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

Name one workaround the old model needed and the failure it prevented. That failure becomes a comparison case on the new model. Use [Ablation](../ablation/SKILL.md) for removal and original-baseline quality gates, and [Hill Climb](../hill-climb/SKILL.md) for bounded experiments. Keep adapters and artifacts project-local.

## Execution architecture

- **Parallel worktree cells:** Run each authorized Model × Design cell (A: old/existing, B: old/simplified, C: new/existing, D: new/simplified) in its own isolated Git worktree or run directory with pinned model/version, assembled prompt, tools, and settings, returning uncommitted candidates until explicit user approval.
- **Blind fixed judge:** Keep the approved evaluator fixed across all cells; when semantic judging is used, run a fresh isolated judge (ideally an authorized distinct provider/family) blind to which model or design produced each output.
- **Harness-aware candidates & fallback:** Treat replacing fragile prose reminders with deterministic hooks, tool bounds, or code verifiers as a separately scoped simplification candidate. Without parallel worktrees or subagents, run available cells sequentially, leaving missing old-model cells explicitly unrun and disclosing any shared judging context; see [harness mapping](../run-eval/references/harnesses.md).

## Contract and comparisons

Link the old workaround and its migration trial in the [shared decision ledger](../create-eval/references/decision-ledger.md). Recover the actual model/version, assembled prompt/context, tools, orchestration, task contract, evals and operational policy. Identify why steering was added where history supports it; missing rationale remains unknown. Preserve task meaning, business rules and unavailable private/current facts while testing compensatory recipes, examples or scaffolding.

Establish authorized model(s), editable scope, quality/regression/resource policy and confirmation/release authority. Read [migration comparisons](references/migration.md). Compare original model/existing design, candidate model/existing design and candidate model/simplified design; where available use the **same** simplified design on the original model too. Record supported settings, source hashes, exact membership and reproducibility limits.

With only one model, compare its full and simplified designs and leave upgrade/interaction claims unrun. Missing old-model evidence cannot establish parity with its production bar. Offline stand-ins establish mechanics, not actual capability; unavailable access/budget is not permission for model calls.

## Simplify and confirm

Test explicit hypotheses through actual execution, including combined removals. A clean task-contract prompt can be a candidate. Keep evaluator/inputs fixed and record any other treatment. Compare the proposed bundle to original production **and** the candidate model's existing design where those cells exist; preserve per-case regressions, errors, uncertainty and total usage. Keep steering whose removal fails; no simplification is a valid outcome.

Freeze model/version, prompt/context assembly, tools, settings, parser and fallback before confirmation under the exposure policy. Deliver the selected bundle/diff, recoverable original, observed comparisons/costs, missing cells and limits. A newer identifier or smaller prompt alone earns no quality claim.

Before adopting a simplified bundle, tell the user what each removal changes in practice, show a tested example and any regressions, and wait for explicit approval of that bundle. For authorized rollout, use the project's shadow/canary controls and rollback the complete bundle; otherwise prepare the handoff without deploying. Re-evaluate after relevant model, context, tool, distribution or evaluator changes.

Offer [calibration capture](../expert-mode/references/calibration-capture.md) for corrections or user-confirmed labels surfaced during comparisons.

At an automated change checkpoint, offer review now, continue to the agreed stop, or continue for N more rounds. Follow the [change review](../hill-climb/references/change-review.md) rules for inherited cadence and uncommitted experiments. Obtain explicit user acceptance of the proposed changes before any Git commit, including local or worker commits.
