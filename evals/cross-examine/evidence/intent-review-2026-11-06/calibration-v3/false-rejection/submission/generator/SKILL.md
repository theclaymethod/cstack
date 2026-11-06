---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.

## Confirmed design lesson

Failure: A valid address update was rejected because its audit method differed from the reference solution.

Why: The observed database state is the independent outcome; credit and reset must agree with that outcome.

Generate instead: Judge observable task outcomes and preserved state independently of optional implementation traces.

Evidence: false-rejection, fixture version 2, sibling finding.json and replay artifacts; run the trusted grader for repair results.
