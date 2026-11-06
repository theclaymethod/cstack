---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.

## Confirmed design lesson

Failure: Agent-writable success claims received credit without the requested update. Why: a self-report is not task state. Generate instead: inspect every required row through evaluator-owned code, independently of optional output flags.

Evidence: sibling finding.json and candidate reproducer; operator result.json records frozen-grader replay.
