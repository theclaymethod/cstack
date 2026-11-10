---
name: ablation
description: Remove prompt instructions, examples, context, tools, or workflow steps while preserving required eval performance. Use for deletion experiments, component contribution analysis, or simplifying an existing system against a fixed evaluator.
---

# Ablation

Find a less burdensome version of the authorized target that meets its quality contract. Deliver the best confirmed reduction found within budget, its deletion diff, and evidence.

Put adapters, candidate generators and experiment artifacts in the consuming project. Reuse its runner and format. [Hill Climb](../hill-climb/SKILL.md) supplies bounded search, execution identity, accounting and confirmation; use the removal-specific rules here. [Bitter Lesson](../bitter-lesson/SKILL.md) adds model-migration comparisons.

## Define the removal experiment

Recover the baseline, actual assembled prompt/context or workflow, existing evals, and owner decisions.

Declare the removable units and their dependencies, protected task requirements, burden objective, primary quality measure, important regression slices, acceptable loss, trial protocol, budget and confirmation rule. Quality loss is relative to the **original baseline**, throughout the campaign. A missing loss policy is not permission to invent one; prepare diagnostic candidates and report any unsupported selection as unconfirmed.

Keep the model, evaluator, gold meaning, case membership, tool environment and unrelated settings fixed. Changing models, rewriting instructions, compressing context or replacing a tool is a different intervention; record it separately when authorized. Preserve necessary task information and behavior even when its wording is redundant.

## Measure, remove and test combinations

Run the original artifact through the actual execution boundary before editing. Retain its complete snapshot, per-case outcomes, state/tool evidence, errors and resource measurements. Missing execution setup leaves the performance experiment unrun.

Read [removal methods](references/removal.md) when choosing units, handling dependencies or investigating interactions. Distinguish two jobs:

- **Contribution analysis:** remove a unit from the same full baseline to measure its conditional effect.
- **Reduction:** build and execute a smaller combined candidate. A collection of harmless individual removals does not establish that their union works.

Start with attributable groups where useful, then finer deletions and selected combinations. Keep each candidate's retained/removed units, parent and actual diff. Check structural validity before execution. Record an invalid intervention, infrastructure error, behavior failure and inconclusive comparison distinctly. Charge actual attempts and preserve confirmation resources under the campaign contract.

Execute every changed candidate. Use the original baseline for quality gates and the current feasible candidate for the burden comparison. Test merged removals as a new candidate; revisit earlier survivors when later deletions change their contribution. Keep conditional successes and unsuccessful attempts recoverable.

## Confirm the reduction

Read [quality preservation](references/quality.md) for stochastic comparisons and non-inferiority. Apply the declared quality floor and critical-case constraints as well as the aggregate. Preserve UNKNOWN/errors and complete selected denominators.

Freeze the selected combined artifact before confirmation and compare it with the original baseline under the same protocol. Repeatedly consulted validation is selection evidence. Reserve independent confirmation where available; disclose exposure and finite fixture limits. A nonsignificant difference alone does not establish preservation.

Promote only a candidate meeting the declared quality, regression and burden rules. Otherwise retain the original or label the reduced artifact as an unconfirmed development candidate. Deliver the versioned artifact, exact deletion diff, tested combinations, per-case changes, uncertainty, measured burden, costs and stopping reason. Claim local minimality only for a completed declared sweep under its actual oracle; a budget stop establishes only the smallest confirmed candidate found.
