# Current skill evaluation, 2026-11-06

The frozen revision `3c4d8bf1c0f9a47245c15c524d8314b14be5bd4e` passed all 11 calibration cases with the local executor and all 11 with Docker. Five audit submissions also passed the executable grader after coordinator-authored repairs and teaching edits. This is development evidence, not a complete independent skill result.

## What ran

The operator wrote [input hashes](frozen-inputs.json) before dispatch and checked equality after grading. Grader version 5 and fixture version 3 stayed unchanged. Three independent lane agents were dispatched with separate neutral case directories and at most two concrete attempts per case. Only the task-contract lane completed: the verifier and environment agent calls were rejected by an automated cybersecurity-risk check. Those lanes were not retried or replaced. Thus the planned three-lane coverage did not complete.

The completed lane independently reproduced these public seeded distinctions:

| Case | Observed outcome | Frozen-grader replay |
| --- | --- | --- |
| a | Success flag accepted while the target address remained unchanged. | [Pass after outcome-based verifier repair](case-a/result.json). |
| b | A completed attempt survived reset and retained credit. | [Pass after reset reconstruction](case-b/result.json). |
| c | A valid SQL-only solution was rejected for omitting an optional audit marker. | [Pass after outcome-based verifier repair](case-c/result.json). |
| d | Two invalid outcomes rejected; baseline/reset behaved correctly. | [Control preserved](case-d/result.json). |
| e | Two invalid outcomes rejected with the oracle read-only; baseline/reset behaved correctly. | [Control preserved](case-e/result.json). |

The lane produced the candidate artifacts and observed results. The parent coordinator assembled repairs and generator lessons, with prior knowledge of the public suite. Consequently, passing artifacts cannot be credited to a fresh autonomous auditor completing the whole skill. Original workspaces were preserved. The lane's [ledger](lane-ledger.md), per-case `submission/run.json`, and [command transcript](audit-run-commands.txt) preserve its observations. Paths in published records are normalized to `<repo>`, and the report's reproduction pointer is adapted to the saved transcript. Runtime helper commands are archived as text rather than installed tooling.

Submitted replay and grading used Docker's documented mounts, network restriction, limits, startup preflight, and exact-container cleanup. The discovery agents themselves had instruction-only host access restrictions. The writable workspace is broader than the task's permitted filenames; inspected artifacts comply with that narrower contract. These conditions do not establish complete discovery isolation or arbitrary-program containment.

## Transfer comparison

Two fresh generation agents each received only the prepared request and one generator skill: one with the coordinator's confirmed lesson and one with the original guidance. They generated one evaluation each, received no grader feedback, and did not execute their code. The operator inspected and graded both in Docker.

Both the [revised-guidance output](transfer-learned-result.json) and the [original-guidance output](transfer-original-result.json) passed all transfer checks. No advantage from the added lesson was observed in this pair. This is one near-transfer example within two-row SQLite tasks per condition, not a reliability estimate or causal improvement result. Host access restrictions and fresh-context provenance remain instruction-based.

## Intent verdict

The current infrastructure supports the existing positive and negative artifact checks under both executors. Candidate-authored reproduction, repairs, preserved legitimate outcomes, and changed teaching artifacts were replayed. Semantic lesson review found the three coordinator additions scoped to the reproduced mechanisms; these mechanisms were already present in the canonical lessons, so no new canonical lesson was added.

The complete adversarial swarm, an independent end-to-end skill run, unseen-case reliability, broad generalization, and useful learning improvement remain unestablished. Every scored artifact result continues to set `skill_evaluation_complete` to false. The two service blocks are execution limitations, not failed candidate evaluations or evidence that the updated runner is defective.
