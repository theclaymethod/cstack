---
name: calibrate-judge
description: Fit, align, and validate an automated judge (typed Jev-style decision model or LLM judge) against authoritative labeled eval outcomes. Use for agreement measurement, threshold/probability calibration, or judge tuning—not for optimizing the evaluated product itself. Keep judge implementations and model dependencies project-local.
---

# Calibrate Judge

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

Follow the [shared decision ledger](../create-eval/references/decision-ledger.md) from the disputed rows to their evidence, then append the calibration decision and receipt. Start with the decision this judge will make. Describe a costly false pass and a costly false rejection in the owner's terms. Keep label agreement, threshold selection, probability calibration and repeated-input stability distinct. Implement adapters/data/experiments in the project, reusing its runner and format.

## Execution architecture

Separate three roles so tuning never contaminates blind judging (see [harness mapping](../run-eval/references/harnesses.md)):

- **Proposer / tuner:** Sees only exposed development disagreements to refine LLM instructions/examples or typed questions/options.
- **Blinded judge executor (fresh subagent or isolated backend):** Receives only allowlisted runtime payloads—never gold labels, rationales, split names, or tuning history. Fan out parallel candidate/repeat batches under a pre-reserved budget. Where authorized, prefer a distinct model family/provider from the evaluated generator to reduce self-preference bias.
- **Deterministic comparator (code):** Freezes complete predictions and hashes before reading gold, computes agreement/error/probability metrics, and enforces final-exposure guards. Without isolated contexts, disclose any prior gold exposure instead of claiming blindness.

## Gold and backend contract

Recover original inputs, reviewed outputs/versions, criterion scope, permitted references, source families and label authority. Read [the protocol](references/protocol.md). Disputed/incomplete labels remain a visible queue. Freeze intended criteria; semantic rubric/gold/aggregation changes need owner adjudication and a new comparable revision.

Establish costly errors, labels, abstention/fallback, mutable judge components, supported model/backend, budget and acceptance policy. Missing release targets do not imply approval. Weight training, paid calls, uploads and reserved-label access require actual capability and scope; missing gold/setup leaves those claims unrun.

Map [backend capabilities](references/backends.md). Preserve raw responses, optional fields, normalization errors, versions and costs. Typed Jev-style decisions need no invented explanations; generative reasons are optional. Concentration confidence is not event probability.

## Baseline and bounded fitting

Execute the untuned judge on declared membership. Gold, annotation rationales and label-bearing selection metadata stay out of runtime payloads; approved task references can enter when legitimate. Store complete predictions before label comparison and verify coverage, inputs/configuration and response/parser identity. A context already exposed to final gold cannot claim blindness.

Use development disagreements to distinguish judge errors, ambiguous criteria, bad labels and missing evidence. Tune LLM instructions/examples/settings or typed questions/options/context without changing gold meaning. [Hill Climb](../hill-climb/SKILL.md) can search under a total budget/reserve; keep the proposer separate from its typed target.

Assess genuine probabilities before fitting a supported mapping. Choose thresholds/review bands from separate or out-of-fold development predictions under the error policy. Optional weight fitting needs a supported interface and explicit authority; it is not required.

## Confirmation and handoff

Read [measurement](references/measurement.md). Report counts, nominal or predeclared ordinal kappa and uncertainty, consequential class errors, UNKNOWN/ERROR and all-selected coverage. Preserve undefined quantities. Probability reliability, stability, latency and costs are separate measurements; repeated calls are not independent gold items.

Freeze the exact judge/model/parser/calibrator/threshold/fallback bundle and final plan. Complete all planned predictions before opening final labels; final-driven edits require new evidence. Exercise alternatives, malformed/missing responses and label leakage. [Adversarial Cases](../adversarial-cases/SKILL.md) builds challenges; [Cross-Examine](../cross-examine/SKILL.md) adjudicates scoring gaps.

Recommend a judge only under the declared evidence/policy; otherwise report not yet calibrated. Deliver configurations/code, invocation, original/selected identities, membership/exposure, metrics, costs and limits. Synthetic controls and response-shape mocks do not establish live backend or human-gold calibration. [Create Eval](../create-eval/SKILL.md) supplies criteria; [Run Eval](../run-eval/SKILL.md) executes frozen judges. Before replacing the active judge, summarize each proposed change in grading behavior, show an example verdict that changed, and name any new false passes or rejections. Ask the user which changes to adopt and wait for explicit approval. Keep the candidate separate while pending. Product optimization keeps its approved evaluator fixed.

Offer [calibration capture](../expert-mode/references/calibration-capture.md) for owner adjudications; consent to save is separate from authority to change gold.

At an automated change checkpoint, offer review now, continue to the agreed stop, or continue for N more rounds. Follow the [change review](../hill-climb/references/change-review.md) rules for inherited cadence and uncommitted experiments. Obtain explicit user acceptance of the proposed changes before any Git commit, including local or worker commits.
