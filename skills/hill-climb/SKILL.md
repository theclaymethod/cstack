---
name: hill-climb
description: Improve a selected prompt, skill, program, or agent harness against an existing eval through bounded experiments. Use for /hill-climb or a requested optimization campaign with a defined editable target and evaluator.
---

# Hill Climb

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

Use the [shared decision ledger](../create-eval/references/decision-ledger.md) to pick up the failing rows and append each experiment’s decision and receipt. Start a trial with a failing case, a proposed change, and a prediction about which observable result should move. Compare against the fixed evaluator. Deliver a confirmed artifact/diff or an honest no-improvement result. [Bootstrap](../bootstrap/SKILL.md)/[Create Eval](../create-eval/SKILL.md) establish missing evals; [Run Eval](../run-eval/SKILL.md) owns faithful execution; [Cross-Examine](../cross-examine/SKILL.md) investigates scoring gaps. [Calibrate Judge](../calibrate-judge/SKILL.md) owns judge-target fitting. Use [Ablation](../ablation/SKILL.md) for removal and [Bitter Lesson](../bitter-lesson/SKILL.md) for model-migration simplification.

## Campaign contract

Recover owner decisions and the native runtime. Freeze [the contract](references/campaign.md): editable target, objective/direction, quality/regression/resource constraints, evaluation boundary, case/family membership, allowed feedback, trial/seed/judge/cache policy, total budget with confirmation reserve, stopping and promotion rule. Hash content/configuration and dependencies; IDs alone are insufficient. Keep unknown versions explicit.

Cases, labels, grader semantics and reserved answers remain outside candidate edits. An evaluator change needs a new comparable revision. Use existing infrastructure; [optimizers](references/optimizers.md) describes optional DSPy/Ax/GEPA/Halo integration. For generated data or DSPy, read [the project-local handoff](references/data-handoff.md); implementations stay outside installed skills.

## Execute attributable candidates

Run the original target and retain its snapshot, complete per-case outputs/state/errors and costs. Stored-output regrading cannot measure a changed target. Check legitimate alternatives, reset and the real schema, including malformed/extra/empty output behavior. Missing setup leaves execution unrun.

Propose from observed failure/success mechanisms, naming expected gains and nearby regressions. Snapshot each candidate, parentage and hypothesis before execution; separate concurrent writes. Feedback may include permitted development evidence, never unauthorized reserved labels. Test merged candidates anew.

Before work, verify identity and reserve its full applicable spend, including retries, proposer/model/tool work and confirmation. Library counters do not establish total cost. Execute exact declared membership/trials through the native grader; partial screens can nominate, not confirm. Preserve errors, rejected attempts and unknown measurements. Retain by the declared policy; retention is not promotion.

## Confirm, recover and deliver

Compare baseline and shortlist under the quality/regression policy and available uncertainty. Adaptive validation is selection evidence; independent claims require actually reserved, authorized evidence. Inconclusive results stay inconclusive; a tiny gain or small perfect sample supplies no general trust threshold.

Before proposing adoption, read one passing trace per target end to end, report issues no check grades and any required checks that skipped, and verify suspected bugs against the raw evidence before reporting them because viewers can omit fields.

Nominate only a confirmed admissible candidate; otherwise preserve the baseline. Stop at the budget/deadline/plateau/target. Persist reservations and evidence identity across interruptions: completed matching native evidence may reconcile without re-execution/recharge; partial/mismatched work stays incomplete and charged. Verify ledgers, source and exposure on resume; changed contracts start a new campaign.

Return exact selected artifact/diff, original/candidate identities, per-case gains/regressions, observed costs/errors, stopping and uncertainty, distinguishing development from confirmation/generalization. Keep trial edits in a candidate until the user reviews the result. For each proposed change, explain what the agent will do differently, give a before/after case, and flag regressions or uncertainty. Ask which changes to adopt and wait for explicit approval. Apply only the approved candidate if the target is unchanged since capture. If the user selects a subset, verify that exact combination before adoption. If nothing qualifies, report that outcome without an approval prompt. Deployment, publication and new paid scope need their own authority.

Offer [calibration capture](../expert-mode/references/calibration-capture.md) for corrections or user-reviewed outcomes; candidate improvements alone supply no human labels.

At an automated change checkpoint, offer review now, continue to the agreed stop, or continue for N more rounds. Follow the [change review](references/change-review.md) rules for inherited cadence and uncommitted experiments. Obtain explicit user acceptance of the proposed changes before any Git commit, including local or worker commits.
