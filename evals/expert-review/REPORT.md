# Expert-review eval results

The suite contains six synthetic workflow cases. Fixture v3 / grader v4 passes all **19 calibration controls**. Two independent Cross-Examine lanes reproduced four grading defects; clean replay confirms their repairs. Six fresh-agent cases were run on frozen v2, followed by one focused fresh-agent development rerun on v3. The original failures are preserved.

This is development evidence about faithful capture. It does not establish clinical truth, generalization, or production reliability. Artifact grades remain separate from full skill evaluation.

## Cross-Examine round

Each lane had a maximum of two attempts. The verifier lane demonstrated that deleting a supplied annotation and omitting required rubric identity/version fields both earned artifact credit. The task-contract lane demonstrated false rejection of a permitted provisional summary observation and a faithful correction citing the later correcting turn. The coordinator reproduced all four through the actual operator API before and after repair.

Current replay rejects the two invalid submissions and accepts the two valid alternatives. The six original reference cases still pass. [Original/repaired receipts](evidence/round-1/before-after.json), [submissions](evidence/round-1/submissions.json), and the [ledger](CROSS_EXAMINE_LEDGER.md) preserve the evidence and prevention scope.

The lifecycle lane was blocked by an automated cybersecurity-risk review. It was not retried and returned no executed result. Three lanes were dispatched; only two completed. Environment coverage is incomplete, and no host permission-enforcement claim is made.

## Actual skill runs

Fresh candidates received only their workspace, supplied skill guidance, revealed conversation, original artifacts, and dataset. The operator captured their actual files before revealing each next turn. Grader/reference code and future events were excluded by instruction. These were host agents without an OS sandbox. Every session was short enough for sequential review lenses; none is evidence of an independent retrospective panel.

| Case | Frozen v2 artifact result | Observation |
| --- | --- | --- |
| Live correction | Pass | Saved the error before replacement existed, appended the later expert correction, retained the original artifact, and stopped capture. |
| Live uncertainty | Fail | Asked about the criterion's passing direction without saving a proposed criterion. Later retained numerical uncertainty but merged two assertions into one chain; the adapter's example unit was ambiguous. |
| Distill merge | Pass | Preserved the supplied annotation, appended correction and retraction, and added no duplicates on repeated invocation. |
| Distill source | Pass | Created no expert labels from agent edits, silence, or the archived directive. |
| Activation | Pass | Kept capture inactive during discussion, started on invocation, and did not backfill earlier judgments. |
| Partial context | Pass | Saved a summary-sourced uncertain observation with explicit provenance gaps and no replay claim. |

The [frozen v2 outputs](evidence/pilot-v2/pilot.json) contain all checkpoint records, replies, hashes, and original grades. Replaying them under v4 still yields five passes and the uncertainty failure; the grader was not relaxed to erase that omission.

Independent read-only adjudication separated three issues in the uncertainty case:

- The adapter required yes/no while the skill allowed an unresolved passing direction. V3 permits a proposed criterion with null passing answer and an explicit gap. A preserved legitimate alternative fails v2 and passes the repaired grader.
- A later confirming expert statement is valid rubric provenance. The earlier source event need not remain the only allowable source.
- The adapter did not declare whether an example represented an output or one assertion. It now explicitly uses assertion identity before requiring separate active concerns. The earlier count failure is a contract ambiguity, not evidence that the candidate fabricated a numerical error.

The shared skill guidance now explicitly saves pending criteria before asking. A fresh v3 candidate did so, preserved the separate probability concern, and appended a confirmed rubric version after clarification. It used the source-naming criterion to mark the source error replay-ready without inventing a replacement probability.

The v3 grader falsely rejected that last readiness decision. Independent adjudication confirmed that the missing numerical replacement concerns a different assertion. Fixture v3 / grader v4 removes that irrelevant blocker. The **unchanged v3 candidate artifacts pass clean replay under v4**. [Before/after evidence](evidence/final-validation/readiness-before-after.json) retains the rejection and repair; [v3 candidate output](evidence/pilot-v3/pilot.json) retains the complete run. This is a repaired grading result, not a fresh v4 model run or a causal improvement estimate.

## Review of meaning and intent

The coordinator read the captured records and replies against the supplied synthetic sources. The five passing v2 cases preserve expert labels, scope, amendment history, and uncertainty as described above. Replies are brief and surface meaningful limits. The focused v3 run records the scoped pending binary question before asking, confirms it from the later expert statement, and leaves the separate numerical judgment unresolved. Readiness covers only the source-naming check.

The evidence supports these narrow observations. Source-access compliance was instructed, not technically enforced; full candidate tool traces are not archived. No real clinical graph, Claude session, Cursor session, compaction/restart, write-failure recovery, or concurrent-writer workflow was evaluated. These limits keep `skill_evaluation_complete` false in machine results. A full deployment verdict still needs those applicable checks and domain-expert review on representative private examples.

The eval's intended outcome was preserved through repair: save faithful expert evidence without inventing endorsement, golden answers, or general rules. Requiring a complete replacement probability for an independently assessable source error conflicted with that intent and was removed. Confirmed rubric semantics and useful clarification remain review questions rather than string-match proxies. Reusable lessons were saved in [Cross-Examine's generator guidance](../../skills/cross-examine/references/lessons.md).

The [final receipts](evidence/final-validation/) contain calibration, replay outcomes, and source/guidance hashes. All work uses local files and Python's standard library. No SQLite or Docker is needed for these data-only checks.
