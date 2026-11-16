# Cross-skill handoff eval

Run four fresh sessions on one synthetic project. Only the project files carry across sessions. Each skill sees its task and the existing ledger path. The runner retains snapshots after every phase. Use an unused output directory.

```sh
python3 evals/skill-handoffs/replay.py /tmp/cstack-handoffs-new
python3 evals/skill-handoffs/grade.py /tmp/cstack-handoffs-new
```

Use `--ref COMMIT` on the replay to compare another skill revision on the same fixture. Each replay makes four model calls. Keep runtime logs local. Read the snapshots and actual tool executions before assigning the following semantic judgments. Grade equivalent IDs, filenames for detailed evidence, and wording equally.

| Transition | Observable criterion |
| --- | --- |
| Existing green case → Adversarial Cases | Identify the clear-everything shortcut. Trace a mixed-selection challenge to the product promise. Reject fixed display order and defer repeat archive. Stop at situations when asked only to brainstorm. |
| Situations → Create Eval | Score the supported situation only. Keep the native singleton, link the new row to the situation, accept reordered survivors, and reject at least one wrong result by actual execution. |
| Owner correction → Create Eval | Reconcile both the situation and its active row to preview semantics. Keep the singleton, valid order alternatives, and open repeat decision. Append a correction that lets the next reader recover the old decision. |
| Dispute → Cross-Examine | Follow the corrected expectation. Demonstrate an actual release-grader pass on wrong identities and a pass on a legitimate reordering. Record the row, evidence and next action in the shared ledger. Distinguish observed discrepancy from independent acceptance. Keep review-only work outside the active grader. |

The executable grader checks append-only history at *every* transition and independently replays controls. It does not decide whether prose is meaningful, whether a model actually performed those replays, or whether its proposed next action follows from them. Those judgments require the evidence review above. A case with missing evidence stays incomplete even when the final row is correct.

On a passing run, `python3 evals/skill-handoffs/grade.py RUN --negative-controls` verifies that the grader rejects three independently corrupted snapshots. One drops the audit handoff while preserving every final row. One restores the superseded behavior at the correction checkpoint. One silently replaces the release grader during a review-only audit.

## First paired replay

Each version completed four fresh GPT-6 Astra sessions. Both versions scored the mixed-selection case correctly before and after the correction, appended to the pre-existing ledger at every transition, rejected a fixed display order, and kept repeat archive undecided. Both audits reproduced the same-length substitution defect under the corrected promise, checked a valid reordering and left independent review pending. Neither changed the release grader.

The [current run](evidence/current.json) passed 24/24 executable checks. The [pre-network baseline](evidence/previous.json) at 5e8bd52 passed 23/24. Its initial handoff was in archive-handoff.md and its correction in SCENARIOS.md. The one measured difference was keeping the agreed situations.md path throughout. The old skills also caught the grading error. This run supplies no evidence of superior audit accuracy.

All three negative controls failed their intended checks. The initial session was told the ledger path and every session was told which skill to use. This exercises cross-session continuity on a synthetic project. Autonomous routing, ledger discovery, independent review and product execution were outside this run.
