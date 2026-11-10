# Independent intent review: initial observed replay

I read the original INTENT.md before frozen skills and fixture sources. I did not read attacker reports, earlier audit conclusions, or mutable repair copies, and authored no audited skill or implementation. This verdict concerns only the supplied replay and clean controls.

## Verdict

The observed replay establishes a bounded defect in verification of durable execution accounting. It does not establish a support-task grading exploit, forged candidate output, budget bypass, model-performance defect, or filesystem containment failure.

Original intent requires preserving actual attempts and accounting evidence. After a genuine eight-case measurement, the replay directly replaces native/executions.json with a zero-use ledger. Experiment.checked('original') accepts the result even though the durable ledger now contradicts the run artifacts, state.json, and the live reservation counter. Experiment.verify checks durable contract/state and completed result-file hashes but does not reconcile the native execution ledger. A checked experiment can therefore expose mutually inconsistent accounting artifacts without reporting that inconsistency. That is a defect relative to the requested evidence and accounting contract.

This is explicitly an operator fault injection outside the candidate payload. The reproducer performs the write from the controlling process; it is not evidence that a conforming candidate API grants ledger mutation. The local adapter is neither a resumable optimizer nor a security sandbox. The observed in-memory reservation remains eight against an eight-case limit, and the replay executes no subsequent candidate. Claims that this replay erased live budget charges, ran beyond budget, or showed unauthorized candidate access would be unsupported.

## Evidence and legitimate behavior

- Supplied observation.json records eight actual native executions, eight live reservations, an all-zero replacement durable ledger, and rejected=false from checked('original'). ledger-before.json records the original completed eight-case attempt.
- I independently ran the frozen native checked_run against defender-before/experiment/native/original. Its manifest, retained stdout/output, native grading, per-case results and counts reconcile: eight selected and executed development cases, eight PASS, zero FAIL/ERROR/UNKNOWN, score 1.0. This recheck invokes no candidate subprocesses.
- Therefore the original candidate's observed task correctness remains accepted on these eight synthetic cases. The corrupt ledger does not invalidate otherwise intact output/state evidence or justify altering the native grader. Accounting integrity and task correctness are separate claims.
- My separate clean public-API controls used 36 native executions. Full old design, old reduction {contract, legacy-auth, duplicate-b}, and new simplified design {contract, duplicate-b} each passed eight development and four confirmation cases. Freeze, confirmation and finish succeeded. Their finite fixture claims remain valid; no production, human-label, generalization or real-model-efficiency conclusion follows.

## Repair acceptance criteria

Reject inconsistent durable accounting before returning a checked/comparable result or continuing a public experiment workflow, while retaining the original eight-case charge and evidence. Rejection must name an accounting/evidence inconsistency, not reinterpret the genuine support outputs as incorrect. Clean public workflows and legitimate native-valid output variants must continue to work. Preserve incomplete attempts as charged; do not silently rewrite contradictory accounting into apparently verified history. No containment or resumability requirement is added by this finding.

## Frozen completion record

After the initial verdict, a separate native compatibility control changed only the conforming reference candidate's newly generated IDs to reviewer-unique-N. All twelve development/confirmation cases passed and checked_run reconciled the retained evidence. This supports continued acceptance of arbitrary valid unique IDs. Its receipt is native-valid-unique-id-receipt.json; the 36-case public adapter controls are recorded in clean-controls-receipt.json.

Final reviewer native case usage: 48/96 (36 public adapter controls + 12 native compatibility cases), all completed and passing. Evidence regrading added zero native executions. No failed execution attempts, paid/provider/network calls, audited artifact edits, or repair verdicts.

Independence disclosure: only after the initial verdict and compatibility control were complete, I called collaboration.list_agents to check whether the parent was still running. Its response unexpectedly included completed attacker final summaries. I did not open attacker reports, theories or raw evidence. The initial verdict above predates that exposure. At the parent's instruction, this review is now frozen; a fresh reviewer will independently assess the repair.
