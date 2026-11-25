---
name: create-eval
description: Author repeatable eval cases, deterministic checks, and binary judge rubrics from expert findings, model traces, or approved scenarios in the project's native format or Harbor. Use for early trace collection, findings-to-cases conversion, or building an executable eval package—not for running an already-frozen suite or fitting judge weights.
---

# Create Eval

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

Start with one decision the eval will inform and one case where a wrong answer would change that decision. Establish source authority, judged unit, observable success and legitimate alternatives. Separate assertion correctness, preferences, process and missing evidence; one bad assertion does not label its neighbors. Keep ambiguous cases provisional while other work continues.

## Execution architecture

- **Inline authoring & review:** Keep evidence triage, [local trace review](references/trace-review.md), verifier modality matching, and unresolved clarifications with the user.
- **Parallel trace collection (optional):** When traces are absent, collect early-development runs across independent scenario slices in isolated scratch or worktree states under [early development](references/early-development.md).
- **Fresh control validator:** Before leaving draft status, dispatch a fresh, non-forked subagent to execute legitimate, failing, boundary, alternative, and wrong-product controls plus offline code-check replays through the real grading path, and inspect allowlisted judge payloads for label leakage. Without subagents, run deterministic control scripts inline and disclose self-checking; see [harness mapping](../run-eval/references/harnesses.md).

## Evidence and cases

Read the [shared decision ledger](references/decision-ledger.md) on entry and append the authored row IDs and evidence at handoff. When [Adversarial Cases](../adversarial-cases/SKILL.md) supplies `situations.md`, author rows for supported situations and carry their stable IDs into the row or case mapping. Reuse an existing row when it already covers that situation. Keep open, rejected and merged entries out of new scored rows. Write the row IDs and actual control results back beside the situation so downstream runs can trace the expectation.

For interviewing and scenario approval, use [Bootstrap](../bootstrap/SKILL.md). Resolve capture amendments/retractions through [findings-to-cases](references/from-findings.md), retaining the original reviewed output. Privacy/meaning review supplies no label authority.

Use [early development](references/early-development.md) when traces are absent: execute realistic feature inputs and review actual evidence where available. Label synthetic, hypothetical and mocked material; missing setup remains unrun. [Existing eval workflows](references/ecosystem.md) are optional tools for discovery and calibration.

Make evidence reviewable before a large batch, using the existing viewer or [local trace review](references/trace-review.md). Include legitimate passes and boundary failures. A supported negative can be useful without a replacement answer; unreplayable annotations stay in an explicit incomplete queue outside scored denominators.

Reuse project format/runner. Prefer Harbor for new executable tasks while preserving established/owner choices; read [formats](references/formats.md). Stored-output review can use the [local package](../run-eval/references/package.md). Data/adapters belong in the project.

Retain replay inputs or execution entrypoint, original output, source authority, construction family, intended role and applicable criteria. Use deterministic checks for observable properties and independent binary questions for interpretation, preserving passing direction and applicability. Stateful tasks require reset, actual resulting state and preservation checks. Match the verifier modality to the promise: do not substitute an eval suite for formal concurrency or ordering verification (model checking or statecharts plus code replay) or for live end-to-end UI visual proof. When an eval judges UI, playback, or multimodal behavior, capture the actual channel artifact (screenshots, recordings, audio, or resulting state) rather than grading text summaries alone.

Keep labels/rationales and label-bearing metadata outside allowlisted judge inputs; references enter only when the grading task permits them. Split by source/construction family. Track development, calibration, final, regression and frontier roles; renaming exposed cases cannot restore independence. Open reserved final semantics only when explicitly authorized.

## Completion contract

The package remains a draft until legitimate, failing, boundary and alternative controls execute through its real grading path. Preserve earlier evidence when checks change. Use [judge guidance](references/judges.md) and [Calibrate Judge](../calibrate-judge/SKILL.md) for semantic fitting to authoritative labels; freeze criteria, parser, model/config, runner, sampling and budget before comparison.

Before owner review, use [Cross-Examine](../cross-examine/SKILL.md) with original intent, access and a bounded budget. Run two plausible wrong products through the real verifier: one returns the right artifact with wrong content, and one always emits the artifact. Include at least one negative-space guard where the behavior must not occur, and verify that the always-emit product fails it. Record what ran and what the verifier missed; a hypothetical control is not evidence.

To prove a code check offline, replay the failing capture through the real check twice: once with the smallest change that should pass, and once with a plausible near miss that should still fail. Record both observed outcomes as evidence about the check, not the product.

Use [Run Eval](../run-eval/SKILL.md) for authorized execution. Report paths, actual checks, source limits and incomplete cases, separating judge agreement from product performance and development from independent evidence.

Authoring supplies no authority for product fixes, paid calls, reserved-data access or publication. Requested sharing follows [export](../expert-mode/references/export.md).

Offer [calibration capture](../expert-mode/references/calibration-capture.md) for corrections or user-confirmed outcome labels collected during authoring.
