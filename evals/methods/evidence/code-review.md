# Independent methods implementation review

One confirmed localized issue; no canonical files edited.

## P2 — Reject an existing execution label before replacing its source cases

Location: `fixtures/playground/methods/native.py:33–45`.

`Runs.run` reserves work and rewrites `<label>.jsonl` before the native runner rejects an existing output directory. Reusing a label with changed cases therefore corrupts the case-source path referenced by the earlier completed ledger entry. It also adds a pending reservation for an attempt that never reached candidate execution. The retained `trial/cases.jsonl` remains intact, so this does not falsify the native trace itself, but the outer ledger ceases to identify the original inputs consistently.

Concrete reproduction, using this checkout's actual native runner and conforming candidate:

1. Construct `Runs(review-scratch/duplicate-label, 10)`.
2. Call `run('trial', improved.py, [case_for('first', 'create')])`.
3. Call `run('trial', improved.py, [case_for('second', 'deny')])`.
4. The second call raises `FileExistsError` for `duplicate-label/trial`.
5. The outer `trial.jsonl` now has ID `second`; the retained native `trial/cases.jsonl` still has ID `first`. Both ledger entries refer to the same overwritten outer path. The ledger records `reserved=2`, `actual_completed=1`, with the second entry pending despite no second candidate launch.

Evidence remains under `work/methods-build/review-scratch/duplicate-label/`. Reject a duplicate label/existing case file/output directory before mutating reservations, cases, or the ledger; require the documented fresh label for retry.

## Checks and limits

Read all six implementation modules, `tests/test_methods.py`, native schema/grading/execution/recovery interfaces, README and relevant generation/failure/DSPy/format/ecosystem references. Checked all local Markdown links under `skills/` and the root README; no missing targets were found. Inspected the installed DSPy 3.5.0 GEPA metric call contract; the supplied five-argument-compatible metric signature and returned score/feedback shape match that interface.

The bounded valid-prefix sequence, independent expected criteria, noise deletion controls, candidate-specific witness, source validation, grouping by connected ancestry/exact inputs, explicit ERROR feedback, lifecycle evidence recovery and scoped storage injection were internally coherent on inspection. I found no confirmed target-intent mismatch in those paths. No full suite, broad generation/fault rerun, provider calls, network calls, or optimizer compilation was performed. External URLs and upstream claims were not revalidated. The parent may still be adding report/exercise documentation while this snapshot is reviewed.

## Fix verification

The duplicate-label issue is resolved in the reviewed staged implementation. Repeated the original real-run reproducer in `review-scratch/duplicate-label-fixed/`: first creation executed once; changed-case reuse of `trial` raised `ValueError` before any mutation. Original outer case bytes, retained case bytes and ledger bytes all stayed identical. Reservation remained one and call count remained one. The added regression checks the observable case/ledger/budget/call preservation.

Reviewed the reduced comparison schedule without a broad rerun. Each of three declared mutants now receives exactly one 12-case original corpus and one final 10-case generated corpus for the comparison: 36 + 30 = 66 executions. The construction/control schedule comprises 7 conforming static cases, 8 sequence steps, 13 reduction/control steps and one candidate-derived witness control: 29 executions. This totals the stated 95. Per-arm quantities are now explicitly case counts, and the scope distinguishes construction/selection work from the final comparison and makes no efficiency claim. No further confirmed functional issue found in the requested guard/accounting follow-up.

## Source-label consistency follow-up

Inspected the narrow `case_for` guidance adjustment against the original JSONL and rubric without running candidates/tests. The generated guidance template has exactly the `dev-howto` request (`How do I connect to the VPN?`, null account, sole `acct-a`) and empty-ticket state. Its expectation now exactly matches that existing source case: only `guidance`, null returned account, zero ticket delta. Denial and duplicate handling remain separately modeled. The added existing-test assertion compares generated expected criteria with original cases whenever their request/state input hashes match, so this particular widening cannot recur silently for the fixed corpus. No issue found in the narrow fix.
