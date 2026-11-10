---
name: bitter-lesson
description: Revisit production prompts and context when upgrading models, testing which legacy steering and scaffolding can be removed. Use for model-migration simplification and retiring workarounds whose value may have changed with model capability.
---

# Bitter Lesson

Test whether a candidate model makes inherited prompt or workflow complexity unnecessary. Deliver a simpler versioned model-plus-prompt bundle only when it preserves the product's quality contract. A stronger model is a reason to retest complexity, not evidence that a deletion works.

Keep implementations, adapters and experiments project-local. [Ablation](../ablation/SKILL.md) owns removal experiments and original-baseline quality gates; [Hill Climb](../hill-climb/SKILL.md) supplies bounded execution and evidence controls. This skill adds model comparisons and the production handoff.

## Recover the production contract

Inspect the actual production model/version, inference settings, assembled prompts, examples, context/retrieval, tools, orchestration, evals and operational constraints. Recover why candidate workarounds were added from available failures or history; label missing rationale as unknown.

Separate required task meaning and unavailable private/current facts from hypotheses about compensating for an older model. Preserve the former while testing the latter. Model intelligence does not supply missing business rules or fresh tool state. Useful simplification can remove orchestration while keeping substantial relevant context.

Establish the authorized candidate model, editable components, quality/loss policy, important production slices, resource budget, confirmation and release scope. Reuse prior decisions. Missing model access or an authorized live budget leaves that comparison unrun; offline fixtures establish mechanics only.

## Separate model and prompt effects

Read [migration comparisons](references/migration.md) before interpreting results. Run the production model with its existing design, the candidate model with that design, and the candidate model with the simplified design. Where available, also run the production model with the **same** simplified design to test the interaction.

Keep the evaluator, cases and comparable execution conditions fixed. Record unsupported settings or unavoidable interface differences. Pin actual versions where possible and retain reproducibility limits when aliases move. If an old backend is unavailable, disclose missing cells; a successful simplification on the new model does not prove the upgrade caused it to become possible.

## Remove inherited complexity

Use Ablation to test redundant reminders, old reasoning recipes, compensatory examples, duplicate context or mandatory workflow stages within the authorized scope. A clean prompt expressing the task contract can be another candidate when useful. State each hypothesis and preserve exact parentage and removal sets.

Run changed artifacts and their combined reductions. Compare quality with the original production baseline **and** with the candidate model using the existing design. The upgrade must not hide a harmful simplification, and a good simplification must not hide a harmful migration. Keep regression slices, errors, uncertainty and total resource use visible. Retain useful steering when its removal fails; a no-simplification result is valid.

## Confirm and hand off

Freeze the complete selected bundle: model/version, prompt, context assembly, tools, inference settings, parser and fallback policy. Confirm it with the agreed baseline comparisons and exposure policy before claiming preserved performance. Report model effects, simplification effects and unresolved interactions at the level the actual comparisons support.

Deliver the bundle and deletion diff, recoverable production baseline, before/after outcomes and measured costs, exact missing comparisons, and remaining uncertainty. When a rollout is authorized, use the project's shadow/canary process, predefined stop conditions and rollback of the complete bundle. Prepare the release handoff when deployment is outside scope. Re-evaluate after relevant model, prompt, context, tool, task-distribution or evaluator changes.
