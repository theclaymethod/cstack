---
name: generate-database-evals
description: Generate local database-update evaluations with a task, reset procedure, reference solution, and verifier.
---

# Generate database evaluations

State the required database outcome and the evaluated agent's access.
Supply a reset procedure, a legitimate reference solution, and a runnable
verifier that emits a JSON `passed` result. Keep the task self-contained.


## Verify database outcomes independently

For database-update tasks with agent-writable result or audit artifacts, derive
`passed` from the actual database through evaluator-owned verification code.
Compare the full required row set, including preserved IDs and unaffected
values; open existing state read-only and fail closed on missing or invalid
state. Treat result reports and optional audit logs as untrusted context.
Accept legitimate final states regardless of optional logs or SQL sequence.

Failure and reason: model-audit-01's verifier trusted `result.json.success`.
An agent could assert success while customer 1 still had `Old Road`, so the
score measured self-report rather than the shipping-address update. It also
rejected a valid direct SQL update that omitted the optional report.

Evidence: `model-audit-01/submission/attack.py` passes the original verifier
without updating SQLite; `alternative.py` achieves the required state without
a report but is rejected. The proposed `verify.py` rejects the forged report
and accepts both the reference solution and the direct update. Exact local
replays and limits are recorded in `model-audit-01/submission/finding.json`.


For resettable tasks where the database itself is agent-writable, reconstruct
the disposable database from trusted fixture data rather than assuming its
existing bytes or schema are valid. Reset optional artifacts and SQLite
sidecars under the same isolated lifecycle. In model-audit-01, replacing the
database bytes with `not sqlite` made the original reset raise
`sqlite3.DatabaseError`; the proposed `submission/reset.py` restored both
original rows. See the corrupt_database evidence in `submission/finding.json`.
This failure contaminates later attempts before capability is measured.
