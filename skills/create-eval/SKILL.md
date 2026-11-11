---
name: create-eval
description: Create repeatable evals from expert findings, model traces, or a new feature's task contract. Use for early trace collection, case and rubric authoring, or grader calibration.
---

# Create Eval

Define the capability and decision this eval supports. Establish source authority, judged unit, observable success and legitimate alternatives. Separate assertion correctness, preferences, process and missing evidence; one bad assertion does not label its neighbors. Keep ambiguous cases provisional while other work continues.

## Evidence and cases

For interviewing and scenario approval, use [Bootstrap](../bootstrap/SKILL.md). Resolve capture amendments/retractions through [findings-to-cases](references/from-findings.md), retaining the original reviewed output. Privacy/meaning review supplies no label authority.

Use [early development](references/early-development.md) when traces are absent: execute realistic feature inputs and review actual evidence where available. Label synthetic, hypothetical and mocked material; missing setup remains unrun. [Existing eval workflows](references/ecosystem.md) are optional tools for discovery and calibration.

Make evidence reviewable before a large batch, using the existing viewer or [local trace review](references/trace-review.md). Include legitimate passes and boundary failures. A supported negative can be useful without a replacement answer; unreplayable annotations stay in an explicit incomplete queue outside scored denominators.

Reuse project format/runner. Prefer Harbor for new executable tasks while preserving established/owner choices; read [formats](references/formats.md). Stored-output review can use the [local package](../run-eval/references/package.md). Data/adapters belong in the project.

Retain replay inputs or execution entrypoint, original output, source authority, construction family, intended role and applicable criteria. Use deterministic checks for observable properties and independent binary questions for interpretation, preserving passing direction and applicability. Stateful tasks require reset, actual resulting state and preservation checks.

Keep labels/rationales and label-bearing metadata outside allowlisted judge inputs; references enter only when the grading task permits them. Split by source/construction family. Track development, calibration, final, regression and frontier roles; renaming exposed cases cannot restore independence. Open reserved final semantics only when explicitly authorized.

## Completion contract

The package remains a draft until legitimate, failing, boundary and alternative controls execute through its real grading path. Preserve earlier evidence when checks change. Use [judge guidance](references/judges.md) and [Calibrate Judge](../calibrate-judge/SKILL.md) for semantic fitting to authoritative labels; freeze criteria, parser, model/config, runner, sampling and budget before comparison.

Use [Cross-Examine](../cross-examine/SKILL.md) for requested/needed adversarial hardening, with original intent, access and a bounded budget. Use [Run Eval](../run-eval/SKILL.md) for authorized execution. Report paths, actual checks, source limits and incomplete cases, separating judge agreement from product performance and development from independent evidence.

Authoring supplies no authority for product fixes, paid calls, reserved-data access or publication. Requested sharing follows [export](../expert-mode/references/export.md).

Offer [calibration capture](../expert-mode/references/calibration-capture.md) for corrections or user-confirmed outcome labels collected during authoring.
