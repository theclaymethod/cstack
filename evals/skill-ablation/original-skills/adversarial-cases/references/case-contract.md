# Case contract and handoff

Use the project's existing schema. These are required meanings where applicable, not a second universal eval format. A contract-only proposal can leave execution evidence unavailable; an executed case needs actual artifacts rather than placeholders filled with guesses.

| Meaning | Record |
| --- | --- |
| Identity | Stable case ID/revision, parent request, intent/source revision, construction/source family. |
| Requirement | Original behavior, acceptable alternatives, independent observable pass condition, unresolved judgments. |
| Hypothesis | Specific assumption challenged and why this case could expose its failure. |
| Conditions | Recoverable request/context, initial state, domain facts, preconditions and feasibility evidence. |
| Origin | Observed/synthetic/transformed, source pointers, generator/operator version, seed or construction method when useful. |
| Access | Candidate permissions, operator injection permissions, writable/protected artifacts, actual enforcement and limits. |
| Perturbation | What changes, where/when it changes, armed trigger, intended effect and bounded duration/attempt count. |
| Expectation | Proposed correct behavior under these conditions, authority and scope; not automatically a gold output label. |
| Execution | Actual setup/reset/entrypoint/scoring commands, versions, selected input identities, trials and artifacts. |
| Activation | Observed event(s), source of the witness, whether the trigger fired, whether the intended perturbation occurred. |
| Outcome | Actual output/state/error, independent requirement witness, native score, disagreement or insufficient evidence. |
| Controls | Clean baseline, valid alternatives, comparable fault-off/no-op/not-reached observations where relevant. |
| Reduction | Changes attempted, retained mechanism, controls rechecked, rejected reductions and budget used. |
| Limits | Unsupported assumptions, execution/access limits, non-activation, unresolved intent, exposure and excluded claims. |

Keep construction status separate from parent adjudication. Useful construction states include proposed, runnable, executed, not activated, and incomplete. The parent owns expectation approval, confirmed-finding status, and repair acceptance; preserve its source if it later supplies a decision.

## Scenario-only handoff

A Bootstrap card should make the situation and boundary easy to judge:

> Situation: An explicit ticket request arrives after a previous attempt timed out, and an open matching ticket is now visible.
> Proposed expectation: Use the existing ticket and avoid another creation, subject to the parent's duplicate/retry policy.
> Hypothesis: Retrying from the request alone may duplicate a committed side effect.
> Pending: Whether this fixture's timeout occurs before or after creation; no execution or user approval yet.

The unresolved timing is a material condition. Split before/after-commit variants or obtain the missing fact rather than letting wording imply one. A hand-authored expected behavior is a proposal even when plausible.

## Executed handoff

Report both the score and independent task evidence. For example, “the proxy accepted a creation claim, while the native state witness contained zero new tickets” is narrower and more inspectable than “the agent beat the eval.” Name the exact verifier/version and permissions used.

Validate retained native runs with the project's evidence checker, including raw output versus parsed output and the scored verdict. Establish required case/control and receipt identities from the parent's frozen coverage contract; counting only the records supplied can silently skip a missing case. Check a source inventory for required membership and against the actual supplied files: two matching empty inventories establish no preservation. These are evidence consistency checks, not protection against an operator who can rewrite host files. The [playground audit](../../../evals/adversarial-cases/CROSS_EXAMINE_LEDGER.md) records the scoped reproductions.

When no failure is demonstrated, retain the result: “fault activated and required recovery succeeded,” “trigger was never reached,” or “setup failed before the target boundary.” These support different claims and must not be collapsed into PASS/FAIL labels for the underlying capability.
