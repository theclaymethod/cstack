---
name: calibrate-judge
description: Fit and validate an automated judge against authoritative labeled eval outcomes. Use for judge alignment, agreement measurement, or tuning Jev-style decision questions and traditional LLM judges. Keep judge implementations and model dependencies project-local.
---

# Calibrate Judge

Turn the project's grading standard into a reusable judge and measure how well it reproduces authoritative outcomes. Keep agreement, decision thresholds, probability calibration and repeated-input stability separate. A fitting score or typed output alone does not establish a calibrated judge.

This skill supplies instructions and references. Write judge code, native adapters, datasets and run artifacts in the consuming project. Reuse its format and runner. Missing gold or execution setup leaves the corresponding calibration unrun; a disclosed synthetic mechanics demonstration is still useful.

## Establish the contract

Recover original inputs, evaluated outputs/versions, allowed task references, labels, criterion scope, authority and source families. Read [the calibration protocol](references/protocol.md) for label auditing, data separation, freezing and handoff. Resolve project facts before asking the owner for missing judgments.

Establish the target decision and costly errors, supported label types, allowed abstention/fallback, backend/model, mutable judge components, budget and acceptance targets. Preserve choices the owner has not made. A missing release policy is not a pass. Do not infer permission for paid model calls, uploads, weight training or opening reserved labels from a request to write a skill or validate mechanics.

Freeze intended criteria and gold meaning. Wording, examples and input representation may be tuned to apply those criteria better. A semantic rubric change, corrected label or new aggregation rule requires recorded owner adjudication and a new comparable revision. Preserve disputed and incomplete annotations instead of forcing them into training gold.

## Execute the untuned judge

Map actual backend capabilities using [backend guidance](references/backends.md). Use the project's native request and response format. A Jev-style model may return typed probabilities without an explanation; a generative judge may return a structured verdict and optional concise evidence summary. Preserve native responses, unavailable fields, parsing/transport errors, model identity and costs.

Run the initial configuration before edits on declared development membership. Keep gold verdicts, annotation rationales, label-bearing names and selection metadata out of current judge inputs. Approved reference answers or expected task behavior may be legitimate inputs when the real judge is allowed to use them. Fitting feedback may expose development labels to a proposer; that does not make them runtime evidence.

Store complete predictions before comparing them with labels. Verify selected case/criterion coverage and unchanged inputs, configuration, parser and responses. A context that already saw final gold cannot supply blind validation merely by following instructions.

## Fit within the permitted scope

Inspect development disagreements and separate judge mistakes, unclear criteria, bad gold and missing evidence. For LLM judges, try clearer instructions, representative examples or declared inference settings. For typed models, tune atomic questions, criteria/option definitions and permitted state. Never fabricate target explanations.

Use [Hill Climb](../hill-climb/SKILL.md) for bounded candidate search when useful; DSPy/GEPA is optional. Keep a generative proposer separate from the typed judge it edits. Reserve confirmation resources and count model/reflector calls, retries, repetitions and comparison work in the relevant counters.

When genuine probabilities exist, assess their reliability and fit a supported mapping only when justified. Choose thresholds/review bands from separate or out-of-fold development predictions under the declared error policy. Keep probability fitting and decision selection distinct. Weight training is conditional on a supported interface, appropriate data and explicit scope; it is not required for this workflow.

## Confirm and decide

Read [measurement guidance](references/measurement.md). Report raw counts and class consequences alongside kappa and uncertainty. Use ordinal weighting only for a declared ordered scale. Preserve undefined statistics, UNKNOWN/errors, all-selected denominators and coverage. Report probability diagnostics, stability, latency and cost separately where measurable.

Freeze the selected judge, mappings and confirmation plan before final execution. Compare baseline and candidate on the same reserved cases under the declared trial policy. Freeze all planned predictions before opening final labels. Final disagreements used for edits become development exposure; preserve the result and obtain fresh evidence for a new independent claim.

Exercise legitimate alternatives, relevant failures, malformed responses, missing evidence, label leakage and targeted adversarial content. [Adversarial Cases](../adversarial-cases/SKILL.md) constructs challenges; [Cross-Examine](../cross-examine/SKILL.md) adjudicates suspected scoring gaps. Repeated calls on one frozen example measure repeatability, not additional independent labeled data.

Promote only when the declared evidence and acceptance policy support it. Otherwise retain the baseline or best disclosed development candidate and report not yet calibrated. Synthetic controls, mocked backend responses, actual provider calls and agreement with human labels establish different claims.

## Deliver the judge and evidence

Return the versioned judge configuration/program, project-local adapter and invocation, baseline/selected identities, data membership and exposure record, before/after metrics and uncertainty, costs, decision policy and unresolved limits. Mark live backend support unrun when only response shapes or mocks were tested. Keep an offline fixture artifact distinct from a deployable judge.

[Create Eval](../create-eval/SKILL.md) supplies cases and criteria. [Run Eval](../run-eval/SKILL.md) executes frozen judges and reports product results separately from judge agreement. A later product-optimization campaign keeps its approved judge fixed; evaluator changes start a new measurement revision.
