---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.

## Confirmed design lesson

Failure: Reset retained successful state from an earlier attempt. Why: a subsequent attempt could inherit credit. Generate instead: reconstruct disposable state from trusted initial values and clear per-attempt artifacts, including after partial, successful, and corrupt runs.

Evidence: sibling finding.json and candidate reproducer; operator result.json records frozen-grader replay.
