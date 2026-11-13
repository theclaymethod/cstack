# Confirmed design lessons

## Reconstruct disposable state across attempts

Failure: A reset issued SQL against a database file writable by the evaluated agent. Corrupting that file made reset fail before it could restore the starting rows.

Why: Initialization trusted the structural validity of state controlled by the previous attempt. One attempt could prevent subsequent attempts from starting, even though reset worked after ordinary successful runs.

Generate instead: For fully disposable state, reconstruct from evaluator-owned fixture data. Exercise reset after completed, partial, empty, and structurally invalid states. Preserve application-owned data when the task requires it; reconstruction is appropriate only for state the eval owns and may discard.

Evidence: The [eval suite](https://github.com/theclaymethod/cross-examine/tree/main/evals/cross-examine) records the original failure in `evidence/model-audit-01/submission/finding.json`. Fixture version 2 reconstructs disposable state; `run.py` and `transfer.py` replay corrupt-state recovery for submitted resets.

## Match report validation to the declared contract

Failure: An audit delivered structured execution evidence, but the outer grader required the evidence field to be a string even though the request had not specified that restriction.

Why: A serialization choice was mistaken for evidence quality, rejecting a substantively useful report before its replay results could be assessed.

Generate instead: Declare artifact schemas explicitly. Where text and structured evidence serve the same purpose, accept both and assess their substance separately. Calibrate with realistic candidate-produced artifacts as well as handcrafted references. Validate required identity/version fields explicitly when downstream replay depends on them; a plausible question and valid quote do not establish a versioned criterion. If faithful uncertainty is part of the capability, provide a valid provisional representation for unknown fields instead of requiring an invented answer.

Evidence: The same suite's `evidence/model-audit-01/submission/finding.json` contains structured replay evidence. The current `run.py` accepts text, list, or object evidence, and `candidate.md` makes those formats explicit. In `evals/expert-review/evidence/round-1/before-after.json`, a criterion missing its required ID and version passes grader v1 and fails v2; the complete reference remains accepted. `evals/expert-review/evidence/pending-rubric-v3/before-after.json` also records a valid proposed criterion with an unknown passing direction rejected by v2 and accepted by v3. Confirmed criteria still require a passing answer.

## Keep control expectations aligned with supplied assets and permissions

Failure: A no-change control was compared against a different generator document from the one supplied to the auditor. A protected-oracle control also required a permission-limited finding instead of accepting a bounded clean conclusion.

Why: Both grading rules imposed requirements outside the candidate's contract. Correct restraint could be scored as failure.

Generate instead: Derive preservation checks from the exact supplied artifact. For negative controls, accept justified bounded conclusions and review access assumptions rather than requiring an invented defect.

For state-update evals, say whether collection membership may change; do not infer an exact row count from the reference state. The [fixture-v5 contract resolution](../../../evals/cross-examine/evidence/contract-v5/REPORT.md) makes the customer and order membership rules explicit and preserves the earlier ambiguous results.

Evidence: `evidence/contract/report.md` in the same suite records the mismatched documents and classification predicate. The current `run.py` compares against the materialized source and accepts either clean or access-limited conclusions for the protected-oracle control.

## Require the candidate's work before crediting the capability

Failure: The outer grader reproduced a reset defect itself and accepted an unchanged generator skill. A submission without its own reproducer or teaching change passed the executable proxy.

Why: Successful harness operations were mistaken for evidence that the evaluated agent performed the intended discovery and learning work.

Generate instead: Replay candidate-authored demonstrations and require promised output changes. Keep those necessary artifact checks separate from semantic review and discovery provenance. When a control receives a surprising supported finding, adjudicate the evidence rather than rejecting it by seed label. Freeze scored versions before candidate exposure; runs used to revise the grader are development evidence.

Evidence: The suite's `evidence/intent-review-2026-11-06/before.json` accepts the frozen incomplete submission; `after.json` rejects it under grader version 3. Its `LEDGER.md` records prevention scope and remaining claims that have not been established.


## Include supplied history in preservation checks

Failure: An incremental dataset grader compared its first checkpoint against an empty list. A candidate deleted the pre-existing annotation, supplied only a corrected replacement, and passed all artifact checks.

Why: Later append-only comparisons protected only history created during the run, overlooking the state the expert had already supplied. Correct final content hid destructive merging.

Generate instead: Snapshot supplied records in operator-owned state before candidate exposure. Compare the first checkpoint to that snapshot and every subsequent checkpoint to its predecessor. Keep valid amendments and retractions append-only while deduplicating their resolved examples.

Evidence: `evals/expert-review/evidence/round-1/submissions.json` preserves the seed-deletion submission. Its `before-after.json` records original artifact credit under grader v1 and rejection by v2's first-checkpoint preservation check; the seeded reference and repeated-invocation baseline pass.

## Separate example identity from the source of an amendment

Failure: A faithful linked correction cited the expert's correcting turn, but the grader required the latest record to cite the earlier error turn. Another permitted summary-derived provisional observation was rejected because the grader allowed only direct expert sources and an empty dataset.

Why: One reference representation was mistaken for the semantic contract. A later statement legitimately changes provenance without changing which example it amends; weaker evidence can legitimately support an incomplete observation without supporting a confirmed label.

Generate instead: Resolve amendments through stable example identity and retained lineage. Validate each statement against its own actual source, including a later expert statement that confirms a rubric definition. Declare whether an example represents an item or one specific assertion before imposing a chain count. Calibrate both allowed provenance representations and all permitted incomplete states, including an explicitly provisional summary or an honest report of no recoverable original. Preserve the stronger evidence requirements for confirmed labels and replay readiness.

Evidence: The same expert-review round records two false rejections under v1 and acceptance under v2, with original-source correction and empty partial-context references still passing. These fixes establish artifact acceptance, not independent validation of expert judgments.


## Match replay blockers to the judged assertion

Failure: An expert called an output wrong because its source was missing, while leaving its numerical probability undecided. The grader required a replacement probability before the separate source-error annotation could be replay-ready, rejecting a candidate that supplied a confirmed source-naming criterion and the original artifact.

Why: Completeness of a golden replacement was substituted for the actual observable criterion. The missing number was relevant to a different unresolved assertion, not to whether a source was named.

Generate instead: Define readiness for the specific judgment being replayed. Accept a supported binary rejection criterion without requiring an unrelated complete replacement. Keep separate uncertainties visible and review whether the proposed criterion actually distinguishes acceptable and unacceptable outcomes.

Evidence: `evals/expert-review/evidence/final-validation/readiness-before-after.json` records the unchanged v3 candidate rejected by grader v3 and accepted by grader v4 / fixture v3 after independent adjudication. Calibration still rejects incomplete confirmed criteria, while both complete replacements and criterion-only negative examples pass. This establishes only the scoped source-naming check, not numerical correctness or the validity of a replacement source.

## Bind captures to original evidence

Failure: A review-capture archive accepted altered saved state, a substituted output and an invented verbatim quote after capture-local hashes were refreshed.

Generate instead: Compare captured input/output/state with the retained original execution, and declared verbatim judgments with their actual cited source. Hash consistency within derived records does not establish those relations. Preserve native/source anchors separately and report operator-corruption probes without claiming candidate write access or malicious-writer containment.

Evidence: The [capture audit](../../../evals/review-capture/CROSS_EXAMINE_LEDGER.md) retains original/repaired checker outcomes, legitimate native controls and independent acceptance for the three demonstrated faults.
