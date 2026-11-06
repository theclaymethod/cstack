# Customer-preservation contract resolution

Fixture v5 explicitly says **do not add or remove customers**. The related order-cancellation request says the same for orders. An address or status update must preserve collection membership; any implementation that reaches that outcome is still valid, with no required audit report or SQL sequence.

This is an authorized contract decision following the [v4 ambiguity](../../../shortened-skills/REPORT.md), not a claim that the old wording already prohibited extra rows. Historical results and reviewer disagreements remain intact.

The implementation is small: two contract sentences, fixture version 5, and one additional state in the existing invalid-outcome probe. Grader version 7 identifies that added coverage. No verifier rewrite, new test files, dependencies, or Docker were needed.

| What ran | Result |
| --- | --- |
| Existing calibration, including positive/negative transfer controls | 11/11 pass |
| Five existing audit cases for each prior proposal set | 10/10 executable graders pass |
| Nine existing runtime scenarios across four frozen shipping verifiers | 36/36 match the revised contract; recorded files remain unchanged |
| Fresh independent intent review | Accepts the observed shipping outcomes against v5, including extra-customer rejection and report-free success |

The reviewer read old and new contracts before implementations, then frozen verifier code and raw runtime evidence without aggregate grader verdicts or earlier reviewers' conclusions. See the [independent review](independent-review.md) and [results with frozen hashes and raw observations](results.json). The two previously generated proposal sets were replayed unchanged; these are development replays, not fresh agent scores.

The exact-membership concern is resolved for v5. Other coverage limits remain: no fresh adversarial search or held-out effectiveness claim, no enforced local permissions, and no independent final transfer-code review. Duplicate IDs require changing the declared primary-key schema and establish robustness only. The recorded unchanged-file checks do not cover every SQLite sidecar or concurrency behavior.
