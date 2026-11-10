# Independent intent review

Verdict: a narrow accounting-integrity defect and its repair are substantiated. The original adapter accepts a completed task result while its persisted native execution receipt falsely reports zero limit, zero reservations and zero executions. The candidate rejects that contradiction. Both versions' support-task outputs remain correct in the supplied and independently repeated replay. This is an operator fault-injection result, not evidence of an incorrect support verdict, candidate access to the ledger, escaped containment, hidden-label access or defeated budget enforcement.

## Independence and original criteria

I read only `INTENT.md` first and recorded `criteria.md` before source review. I then inspected original skill/adapter/grader sources, the candidate diff and tests, and the specified raw observations and execution artifacts. I did not read other role reports, eval reports or conclusions, list agents, repair source, access providers or use the network. All reviewer artifacts are confined to this directory.

The criteria require the existing native grader to own support correctness; accept legitimate IDs and permitted actions; preserve contract, original baseline, errors, reservations and confirmation evidence; distinguish contribution from combined reduction; and limit migration, quality and access claims to their evidence.

## Direct evidence

The supplied before and after trace files are byte-for-byte identical. Each contains eight real subprocess results with all native support checks true: authorization, selected account, preserved prior tickets and other state, unique IDs, exact ticket delta and new-ticket fields. Both summaries retain all eight selected cases and report eight passes, zero failures/errors/unknowns. Their manifests identify the same candidate hash and native evaluator/case/rubric/spec hashes. The after state additionally binds the native receipt hash.

In both supplied replays, `ledger-before.json` records limit/reserved/executed equal to eight and one complete attempt. The perturbed `executions.json` instead declares zero and an empty attempt list. Before, `checked('original')` still returns the valid task record; after, it raises `Native execution ledger differs from reserved attempts`. The in-memory reservation stays eight in both. No further native call or budget overrun is demonstrated.

My own replay ran each source version from a fresh isolated directory using the provided reproducer. It independently produced the same distinction: original accepts, candidate rejects, with eight passes each and identical support traces. The reproducer explicitly writes the ledger from the controlling process after execution. Native candidate stdin contains request and state only; this experiment does not demonstrate a candidate locating or writing the ledger.

## Clean and legitimate controls

`run_controls.py` exercised the candidate through its public `Experiment` workflow with a 24-case limit and eight-case confirmation reserve:

| Run | Native cases | Result |
| --- | ---: | --- |
| Original old-fixture full configuration | 8 development | 8 PASS |
| Combined reduction: contract, legacy-auth, duplicate-b | 8 development | 8 PASS |
| Frozen original | 4 confirmation | 4 PASS |
| Frozen same combined reduction | 4 confirmation | 4 PASS |
| Legitimate alternate candidate | 8 development | 8 PASS |
| Original-source ledger replay | 8 development | 8 PASS; contradictory ledger accepted |
| Candidate-source ledger replay | 8 development | 8 PASS; contradictory ledger rejected |

Both development and confirmation baseline-relative gates were admissible with no regressions, errors or unknowns. The experiment finished with 24 reservations. The alternate candidate emitted unique IDs outside the reference naming convention and used `clarify` for the permitted generic trouble and existing-duplicate scenarios. Native execution accepted it. This tests representative valid original behavior, not every possible valid implementation.

Actual reviewer usage is exactly **48/48 native case executions**, across seven successful runs, including both replays; no unsuccessful attempts occurred. `case-usage.json` derives these counts from retained traces and summaries. No extra full test suite was run. Existing test code was inspected, including receipt field changes, receipt deletion/restoration and the interrupted-attempt reservation test.

## Repair and teaching adequacy

The runtime change computes a receipt from live reservations/calls, binds its hash into saved state, and requires the persisted JSON receipt to equal that live receipt on verification. Existing state/source/evidence checks continue to apply. This closes the reproduced uncoordinated disk-ledger drift for an existing experiment object, and also checks a missing ledger when recorded calls exist. It changes neither the grader nor candidate behavior.

The added quality-reference paragraph directly teaches the demonstrated lesson: correct task verdicts can coexist with contradictory receipts; compare counts and attempt identities across campaign and native records; retain charged incomplete attempts. It is sufficient for this confirmed issue. Bitter Lesson already directs removal work to Ablation and explicitly links its quality reference, so a duplicate paragraph is unnecessary. The original contribution/combined-removal distinction, original-baseline gates, exposed-confirmation limits, and migration-comparison requirements remain in place.

## Residual limits

This verdict establishes finite synthetic behavior and local accounting consistency only. It does not establish production model quality, efficiency, a minimal skill pack, exhaustive search, stochastic non-inferiority or an interaction between real model upgrades and simplification. My controls did not execute a model-migration factorial; those comparisons remain unrun here. Prompt bytes and runtime observations do not establish paid cost savings.

The adapter is expressly one-shot and is not a resumable optimizer or security sandbox. A trusted controller can mutate code, memory, saved hashes and files together; no protection against such coordinated rewriting is established. Local subprocesses have host permissions; fresh working directories and `-I` do not demonstrate filesystem containment. Cases and confirmation expectations are readable synthetic material, and confirmation here is a frozen workflow stage, not unseen evidence.

Reservations are conservative per-attempt charges. `actual_completed` sums completed calls; this review does not establish exact crash-time partial-execution metering. The candidate still refuses incomplete results as comparison evidence, and the inspected interruption test retains the full attempt reservation. No stronger crash-recovery claim is warranted.

`source-hashes.json` records SHA-256 hashes for original/candidate skill files, relevant execution sources and native eval assets, plus intent and reproducer. Native evaluator, support candidate, native-run helper and eval asset hashes are unchanged between the frozen and candidate sources. The exact repaired sources and independently executed artifacts remain recoverable alongside this report.
