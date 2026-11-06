---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.

## Confirmed design lesson

Failure: INSERT OR IGNORE preserved a prior successful run, so the next attempt could receive inherited credit.

Why: The observed database state is the independent outcome; credit and reset must agree with that outcome.

Generate instead: Restore exact initial state and clear attempt artifacts on every reset; replay reset after successful and partial runs.

Evidence: stale-reset, fixture version 1, sibling finding.json and replay artifacts; run the trusted grader for repair results.
