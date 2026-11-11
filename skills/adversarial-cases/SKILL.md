---
name: adversarial-cases
description: Construct controlled adversarial scenarios and executable fault-injection cases for Bootstrap, Cross-Examine, or a scoped eval workflow. Return proposed expectations, reproducible challenges, activation evidence, and outcome witnesses; the parent owns approval and adjudication.
---

# Adversarial Cases

Construct the smallest useful challenge to a specific requirement. The parent owns expectation approval and finding/repair adjudication; construction itself creates neither human labels nor accepted findings.

## Case contract

Recover original intent/revision, raw input/context/state, alternatives, runner, candidate access, permitted operator injections and bounded case/execution budget. Keep intent fixed, facts distinct from synthetic hypotheses, and situations feasible. An intentionally impossible user request may test clarification; an accidentally impossible environment is a different condition.

Use the native format or [case contract](references/case-contract.md). Preserve source/construction families through variants, repetition and reduction. Read [synthetic methods](references/synthetic-methods.md) for generation/selection and [failure methods](references/failure-methods.md) for perturbations. Implement project-locally.

Generate causal conditions before wording. Contrast meaningful boundaries while preserving identities, chronology, permissions and reachable state. Define legitimate behavior under the perturbation, including recovery, clarification or non-action; a tool error alone is not a task failure. Model-generated expectations remain proposals.

## Execution evidence

When executable, follow [injection/witness guidance](references/injection.md) through the real entrypoint/grader with reset and a bounded driver. Pin instrumentation; if it changes the program, establish its clean baseline first.

Classify candidate-permitted actions separately from operator faults. Identify historical/defective verifier versions rather than blaming current scoring. Separate writable paths where supported; scratch/timeouts do not imply host isolation.

Keep **armed**, **activated** and **outcome** distinct. Retain an activation witness and independent resulting-state/artifact evidence. An event before termination does not prove exit; exit alone does not identify its injection boundary. A success claim or configured fault name proves neither. An unreached trigger is not evidence of behavior under that fault; unavailable setup yields a proposal and named prerequisite.

Pair clean and legitimate-alternative controls; add no-op/non-activation controls when needed for attribution. Keep inputs, versions, reset and trial policy comparable. Replay and reduce irrelevant fields/steps while preserving feasibility, actual activation and the same distinguishing outcome. Recheck controls; retain failed reductions and unstable attribution. Every attempt consumes the parent's budget.

## Parent handoff

Freeze scored versions before changes; preserve earlier failures and development exposure. Return intent/source, hypothesis, exact conditions/family/access, proposed expectation, setup/reset/replay commands, witnesses, score, controls, reduction history and limits. Name unexecuted and non-activated work.

[Bootstrap](../bootstrap/SKILL.md) receives review cards, guesses/reasons and uncertainty; approval of expected behavior is distinct from labeling actual output. [Cross-Examine](../cross-examine/SKILL.md) receives a reproducible discrepancy and independent outcome witness for fresh intent review. No confirmed defect is a valid bounded result.

Surface review signals to the parent's [calibration-capture offer](../expert-mode/references/calibration-capture.md); builders do not independently request consent or assign human labels.
