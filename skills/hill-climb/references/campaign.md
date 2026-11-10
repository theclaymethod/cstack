# Campaign contract and evidence

Use when initializing, reviewing, or resuming a campaign. Keep the project's native runner, schemas, and record tools. Ordinary local JSON/JSONL and a Markdown decision trail are sufficient when no campaign system exists.

## Freeze what gives a score meaning

Record the mutable artifact and permitted components separately from the evaluator. The evaluation boundary includes selected input contents, source authority, required schema, graders/rubrics, entrypoint and dependencies, model settings, environment/reset, and trial policy. Capture content hashes and recoverable versions; retain baseline and candidate snapshots.

An editable prompt or program can legitimately change outputs. A changed test input, permissive grader, omitted case, different judge, or relaxed constraint changes the measurement. Abort or start a newly identified campaign with a new baseline when that happens. A hash detects changed bytes; it does not protect files from a process that can also rewrite the receipts. Use the project's actual access controls for claims that depend on separation, and disclose shared host permissions.

Record the objective's direction and aggregation, case/slice membership, and independent constraints. Define the treatment of errors and unknowns without erasing them from totals. A pass-rate objective and a latency objective may need a feasible frontier rather than a fabricated combined score. Trust thresholds, regression allowances, and promotion consequences belong to the owner.

## Execution and candidate records

Retain one record per attempt with:

| Field | Meaning |
| --- | --- |
| Identity | Campaign, candidate, parent, content hash, original location and snapshot. |
| Hypothesis | Observed mechanism, proposed change, expected gain and possible regressions. |
| Execution | Actual command, selected suite/case IDs, trial identity, environment/model facts, start/end, output/evidence paths. |
| Outcome | Per-case verdicts, raw metrics, errors/unknowns, baseline comparison, measured costs and unknown costs. |
| Decision | Retain/reject/inconclusive, reason, confirmation status, and exposure. |

Write an attempt reservation before starting work and its result afterward. Interrupted attempts retain reserved spend until reconciled from actual provider/runner receipts; missing completion is not a free retry. Keep author proposals separate from observed outcomes. A hash or successful subprocess exit alone does not show that the candidate executed or the intended behavior occurred: retain the runner's candidate identity and outcome evidence.

Distinguish incomplete execution from a completed run whose ledger commit was interrupted. Recover the latter only by validating full case coverage, candidate/source/configuration identity, actual output evidence, and score/constraint results against the original reservation. Persist recovered completion and retention/promotion decisions without rerunning the artifact or changing charged spend. Leave partial or unverifiable evidence visibly pending; a convenient completion flag is insufficient.

Preserve failed or timed-out attempts and partial artifacts. Candidate code executes with the actual runner's permissions; a scratch directory or timeout is not containment. Run only code within the project's authorized execution boundary. Stateful targets need reset and complete resulting-state/preservation observations.

## Budget and stopping

Use finite enforceable limits appropriate to the campaign: evaluations, model calls, tokens/dollars, compute, elapsed time, concurrency, or combinations. Specify what each counter includes. Reserve baseline and confirmation work before spending the search allocation. If some costs are unavailable, report unknown and use an enforceable available bound rather than claiming a dollar guarantee.

Compare candidates under a declared repeat/seed/cache/judge policy. Extra trials used to resolve uncertainty consume budget. Choosing the best of many noisy scores creates selection bias; confirmation should address it using task-appropriate repetitions and independently reserved examples where available.

Define stopping separately from promotion. Budget exhaustion, a plateau, or finding no admissible change can end a useful campaign with the baseline retained. A backend's stopping event does not establish that its chosen candidate met the owner's promotion constraints.

## Exposure and resume

Keep search, adaptive selection, confirmation, and final-test roles explicit. Record actual opened cases and feedback. Do not relabel an exposed set as unseen or use final-test mismatches to fit another candidate while retaining a final-test claim. When independent examples are unavailable, a fixed-task or development improvement is still useful within that scope.

On resume, compare the recorded contract, content/configuration hashes, completed and incomplete attempts, remaining budget, candidate identities, and prior exposure with current facts. Resume the same campaign only when these remain compatible. Preserve the old record when a changed evaluator, data, model, or policy requires a new baseline.

## Handoff

Keep the selected artifact independently recoverable and provide a diff from the original baseline. State whether it is the best observed development candidate or a confirmed selection. Include no-improvement and inconclusive states in the normal result format. Leave the live working target alone when it contains unrelated edits; deliver the selected snapshot and diff for integration instead.
