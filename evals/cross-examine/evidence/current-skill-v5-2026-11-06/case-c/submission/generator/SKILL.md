---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.

## Confirmed design lesson

Failure: A valid SQL-only update was rejected for omitting an optional audit marker. Why: a reference trajectory replaced the outcome contract. Generate instead: check required outcomes and preserved rows independently of optional reports or implementation traces.

Evidence: sibling finding.json and candidate reproducer; operator result.json records frozen-grader replay.
