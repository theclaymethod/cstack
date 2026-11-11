---
name: bitter-lesson
description: Revisit production prompts and context when upgrading models, testing which legacy steering and scaffolding can be removed. Use for model-migration simplification and retiring workarounds whose value may have changed with model capability.
---

# Bitter Lesson

Revisit inherited production prompt/context or workflow complexity when model capability changes. Use [Ablation](../ablation/SKILL.md) for removal and original-baseline quality gates, and [Hill Climb](../hill-climb/SKILL.md) for bounded experiments. Keep adapters and artifacts project-local.

## Contract and comparisons

Recover the actual model/version, assembled prompt/context, tools, orchestration, task contract, evals and operational policy. Identify why steering was added where history supports it; missing rationale remains unknown. Preserve task meaning, business rules and unavailable private/current facts while testing compensatory recipes, examples or scaffolding.

Establish authorized model(s), editable scope, quality/regression/resource policy and confirmation/release authority. Read [migration comparisons](references/migration.md). Compare original model/existing design, candidate model/existing design and candidate model/simplified design; where available use the **same** simplified design on the original model too. Record supported settings, source hashes, exact membership and reproducibility limits.

With only one model, compare its full and simplified designs and leave upgrade/interaction claims unrun. Missing old-model evidence cannot establish parity with its production bar. Offline stand-ins establish mechanics, not actual capability; unavailable access/budget is not permission for model calls.

## Simplify and confirm

Test explicit hypotheses through actual execution, including combined removals. A clean task-contract prompt can be a candidate. Keep evaluator/inputs fixed and record any other treatment. Compare the proposed bundle to original production **and** the candidate model's existing design where those cells exist; preserve per-case regressions, errors, uncertainty and total usage. Keep steering whose removal fails; no simplification is a valid outcome.

Freeze model/version, prompt/context assembly, tools, settings, parser and fallback before confirmation under the exposure policy. Deliver the selected bundle/diff, recoverable original, observed comparisons/costs, missing cells and limits. A newer identifier or smaller prompt alone earns no quality claim.

For authorized rollout, use the project's shadow/canary controls and rollback the complete bundle; otherwise prepare the handoff without deploying. Re-evaluate after relevant model, context, tool, distribution or evaluator changes.

Offer [calibration capture](../expert-mode/references/calibration-capture.md) for corrections or user-confirmed labels surfaced during comparisons.
