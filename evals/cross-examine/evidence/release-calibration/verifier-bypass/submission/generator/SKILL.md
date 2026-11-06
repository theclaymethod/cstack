---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.

## Confirmed design lesson

Failure: Agent-writable success claims were accepted with an unchanged database.

Why: The observed database state is the independent outcome; credit and reset must agree with that outcome.

Generate instead: Check the complete required database outcome through evaluator-owned code; output flags are untrusted.

Evidence: verifier-bypass, fixture version 1, sibling finding.json and replay artifacts; run the trusted grader for repair results.
