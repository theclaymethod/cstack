---
name: create-eval
description: Create repeatable evals from expert findings, model traces, or a new feature's task contract. Use for early trace collection, case and rubric authoring, or grader calibration.
---

# Create Eval

For trace analysis, synthetic inputs, failure discovery, or calibration, consult [existing eval skills](references/ecosystem.md). Use the relevant skill when available or its upstream guidance. These are optional references, not bundled dependencies.

For an intent interview and human approval of generated scenarios before authoring, use [Bootstrap](../bootstrap/SKILL.md). Continue here when the behavior and reviewed cases are already established.

## Define the decision

Establish the intended capability, observable success, expert authority, and acceptable alternatives. Identify what each case judges, such as an assertion, whole output, or environment outcome. One wrong assertion does not label its neighbors. Keep factual correctness, preferences, process requirements, and missing evidence distinct.

Use deterministic checks for directly observable properties. Use independent binary questions for open-ended criteria, with passing answers and applicability. Stateful tasks need actual execution, reset, and resulting-state checks, including what must remain unchanged. Stored text alone does not test execution.

Resolve material ambiguity from local evidence first. Ask only for missing judgments that change the task or pass condition. Keep affected cases provisional while continuing independent work.

## Gather evidence and make it reviewable

Inspect original inputs, outputs, and expert statements. Resolve amendments, retractions, and rubric versions before importing captures through [from findings to cases](references/from-findings.md). Preserve the reviewed output rather than replacing it with a repaired result. Export privacy and meaning reviews do not establish expert label authority or judge calibration.

For a new product or feature without relevant traces, follow [early development](references/early-development.md). Run realistic inputs through the actual feature and review the traces with the expert. Explicit task invariants can support initial checks. Keep hypothetical failures, synthetic examples, and mocked outputs labeled as such. Missing execution setup remains unrun.

Provide a viewer before producing a large batch. Reuse the project's viewer, `build-review-interface`, or the bundled [local trace review tool](references/trace-review.md). Review outputs, tool interactions, retrieved evidence, and resulting state. Let observed failures inform the taxonomy; keep hypotheses separate.

Include legitimate passes and realistic boundary failures. Agent agreement does not create expert gold. A supported negative can be useful without a replacement answer if its rejection criterion is observable. Keep unreplayable annotations in an incomplete queue, outside scored denominators, and report exclusions.

## Package the cases

Prefer Harbor for new executable agent tasks; preserve established or owner-selected formats. Read [format selection](references/formats.md). For stored-output review, [the local package contract](../run-eval/references/package.md) uses `rubric.md`, `cases.jsonl`, and `config.json`. Keep data and run evidence outside skill installations.

Retain replay inputs, the reviewed output or execution entrypoint, applicable checks, source authority, construction family, and intended use. Write one binary question per independent requirement. Preserve supported alternatives, conditions, and passing direction. Insufficient evidence stays unknown; execution errors are distinct from domain failures.

Keep expert labels and rationales separate from judge inputs. Build blind payloads with an allowlist that excludes label-bearing names, source notes, and prior verdicts too. Reference answers belong in the payload only when the grading task legitimately uses them.

Split by source or construction family. Keep development, calibration, final test, regression, and frontier roles explicit. Exposed cases remain development evidence regardless of renaming. Open final-test semantics only on explicit instruction.

## Check the grader

Keep the package a draft until legitimate passes, clear failures, and relevant boundaries run through the real grading path. Check supported alternatives too.

For semantic judges, read [judge calibration](references/judges.md). Use [Calibrate Judge](../calibrate-judge/SKILL.md) to fit a judge to authoritative labels before freezing it for product evaluation. Use separate expert-labeled development and calibration examples from both classes. Freeze the rubric, prompt, parser, model/configuration, runner version, sampling, and budget before comparison. Changes create a new revision; preserve earlier results.

Use [Cross-Examine](../cross-examine/SKILL.md) when requested or when adversarial hardening is needed before a score drives decisions. Supply original intent, permitted shortcuts, access limits, the frozen grading path, and a bounded budget. Record untested risks honestly; reading a checklist is not an audit.

Use [Run Eval](../run-eval/SKILL.md) when execution is requested and authorized. Compare meaningful baselines when available, with costs and trial conditions. Regression coverage and model discrimination are separate claims.

## Hand off

Report the package path, measured capability, evidence sources, replayable cases, unresolved cases, and actual validation limits. Separate grader calibration from product performance and development results from held-out evidence.

Authoring adds no authority for product fixes, paid campaigns, opening reserved cases, publication, or uploads. For requested sharing, follow [the export workflow](../expert-mode/references/export.md).
