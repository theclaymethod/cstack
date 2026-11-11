# Labeling and resumable checkpoints

Use this when presenting scenarios, collecting decisions, resuming a run, or handing approved cases to evaluator authors. Reuse the project's annotation tools and records. A short chat batch is enough for intent review; the existing [trace reviewer](../../create-eval/references/trace-review.md) can help when judging actual traces, but is not required for scenario approval.

## Review cards

For example, with a proposed behavior of routing requests for IT action:

> **S-02 · revision 1**
> Situation: An employee asks, “How do I connect to the VPN?”
> Proposed expectation: Answer with setup guidance; do not create a ticket solely for this question.
> Why: Distinguishes a how-to question from a request for IT to act.
> Decision: Approve / Disapprove or correct / Defer.

Keep the situation self-contained enough to judge. Show relevant facts or uncertainty rather than hiding assumptions in the reason. For a contrast pair, show what changed and why it might change the expected behavior. Give meaningful alternatives equal status rather than assuming one exact reference response.

Invite compact replies such as `approve S-01, S-02; S-03: ask which account first; defer S-04`. A user saying “approve all shown” covers only the exact displayed batch and revisions. Resolve ambiguous replies before promotion. Disapproval alone leaves the replacement expectation unresolved. “Looks reasonable” about the overall approach does not approve every case.

For outcome labeling, show the actual output/action/state and ask about a named criterion. Keep this separate from the expectation card, for example:

> **O-02 · output revision 1 · criterion: ticket routing**
> Observed: The agent created ticket 17 for the how-to question.
> Proposed label: FAIL on ticket routing, because the user requested guidance only.
> Decision: Approve label / Disapprove or correct / Defer.

An approved routing label says nothing about the factual correctness of the answer. A human label on a hypothetical or mocked outcome is valid only for that reviewed artifact; it is not an observed product result. Identify synthetic/mock provenance in the record.

Guesses make intent review easier but can anchor the reviewer. Record when a suggestion was shown and call the result a human-confirmed suggestion, rather than independent annotation. For independent outcome calibration, offer a pass without a suggested verdict if the user wants that stronger separation. Keep guessed expectations in the normal intent-review flow.

## Minimal record

Keep a small, durable checkpoint in the project's eval workspace. If there is no convention, use `eval-runs/bootstrap/<behavior>/` with `intent.md`, `scenarios.jsonl`, and `decisions.jsonl`; add the runner mapping and work status to `intent.md`. These are authoring records, not a new eval package format. Include the exact card text in scenario records; IDs alone are insufficient to replay what was approved.

Record the following in the existing format or equivalent fields:

| Record | Required meaning |
| --- | --- |
| Intent | Behavior and revision, source statements, confirmed boundaries and open questions. |
| Scenario | Stable ID and revision, intent revision, input/context/initial state, proposed expectation and rationale, applicable requirement, origin and source pointers, construction method and family. |
| Decision | Scenario or outcome ID and exact revision, judgment type, approve/disapprove/defer/correction, user statement/source, scope, and any amended decision it supersedes. |
| Outcome label | Actual artifact identity/version, criterion, PASS/FAIL or uncertainty, and the explicit human decision source. |
| Handoff | Approved revisions, exclusions and reasons, format/runner mapping, ownership, and validation/exposure status. |

Preserve previous records and append amendments. A material change to the situation, expected behavior, or intent boundary creates a new revision and makes affected approvals stale. Cosmetic reformatting may retain approval when the reviewed meaning is unchanged. Recompute the approved set before authoring or integration. Keep already-authored stale artifacts visibly provisional until reviewed again.

An explicit user correction is authority for the exact replacement they supplied: record the new revision and link that correction as its decision source. Ask for another review only when the correction is ambiguous or the agent adds a substantive interpretation. This keeps amendments reviewable without making the user approve their own words twice.

On resume, read existing checkpoints before generating more. Reuse stable IDs and resolved decisions, avoid re-asking answered questions, and show only new, changed, or unresolved cards. If the checkpoint and live user statement conflict, retain both and resolve the affected decision explicitly.

## Label boundaries

Expectation approvals can authorize deterministic contract checks before an implementation exists. They cannot establish judge agreement with human output labels. Likewise, an author-generated “good” or “bad” output is a control proposal, not gold merely because its author named it that way.

Keep calibration labels, decision rationales, label-bearing scenario names, split metadata, and private mappings out of judge inputs. A necessary reference answer is permitted task evidence only when the actual grading task requires it; declaring a reference answer does not make a prior human verdict visible to the judge. Follow the existing [blind projection contract](../../run-eval/references/package.md) rather than passing the whole authoring checkpoint to a validator.

User review of expectations need not invalidate a reserved set for evaluator fitting: keep reserved concrete artifacts and their outcome labels outside the author's context. If review examples or mismatch details are used to tune the evaluator, mark those families exposed and treat subsequent checks as development evidence. Isolation is a claim about actual inputs and access, not a directory name.

## Retain decisions for later calibration

Use the shared [capture-offer guidance](../../expert-mode/references/calibration-capture.md) when additional retention for judge calibration is useful. Existing authoring checkpoints need no new permission. Preserve expectation decisions as intent evidence and concrete output labels as scoped supervision; do not turn an approval batch into labels on generated outputs. The coordinator owns any new offer and reuses existing capture consent.
