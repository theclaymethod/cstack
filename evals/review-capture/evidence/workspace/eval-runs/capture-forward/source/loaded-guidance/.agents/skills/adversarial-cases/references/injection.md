# Injection, activation, and outcome witnesses

Use for executable perturbations. The parent owns the allowed scope and budget; a case builder does not gain authority to mutate production services, protected verifiers, or source labels by naming a failure hypothesis.

## Match the driver to the boundary

| Boundary | Small useful driver | Evidence to retain |
| --- | --- | --- |
| Product output/schema | Candidate variant returning a targeted malformed or misleading result. | Actual stdout/parsed output, native score, and independently checked resulting state. |
| Lifecycle/commit | Existing failpoint or an external process stop at an observed phase. | Versioned boundary observation, real exit/termination, complete/partial artifacts and ledger/state before/after. |
| Dependency response | Existing stub/proxy hook at a defined call or operation. | Selected call/attempt, fault response actually returned, retries and side-effect/state witness. |
| Input/evidence boundary | Minimal factual change, omission, conflict or stale version. | Original and changed source facts, expected relation, applicability and observed selected evidence. |

Use the real project runner. A separately simulated failure can test that simulation; it is not a trace of the actual product. Likewise, sending a signal to a process does not establish that a particular application phase was reached. Pair boundary-specific evidence with process/dependency observations.

If only an internal function/line trace hook is available, record the exact source hash, trigger predicate, and hook fragility. Verify that it targets the intended version and preserve an uninstrumented clean control. A local process exit tests process interruption; it does not model power loss, storage durability, or a network partition by itself. More realistic fault models are separate scoped experiments.

## Separate configured, reached, and effective

An executable injection description should specify a trigger predicate, action, witness location, attempt/duration bound, and reset. Capture activation evidence outside the candidate's claims. Confirm the intended effect independently when possible; an activation marker written before an action can survive even if that action fails.

For a no-op or unreachable-trigger control, retain the armed configuration and actual activation count. Zero activations means the faulty condition was not exercised. It does not establish recovery quality, and it is not a product defect. A clean control instead establishes normal behavior with the perturbation disabled.

Distinguish malformed harness setup from a legitimate injected fault. If the driver crashes before invoking the product, record setup error and missing coverage rather than blaming the product. Missing evidence remains incomplete.

## Preserve attribution and feasibility

Candidate attacks use candidate access. Operator resilience injections use separately authorized operator access. Record extra-access checks separately and avoid treating a broken evaluator caused by forbidden edits as a candidate exploit. Verification can inspect protected source where permitted, but scored reproduction must preserve the access boundary it claims.

Reset initial state between attempts, including partial prior work. Check original records, side effects, identity and membership, not only aggregate counts or success flags. Use independent observation of the relevant state rather than an evaluated program's own “success” field or the disputed verifier's verdict.

Probe permitted representation alternatives as well as wrong outcomes. Required record fields do not imply a closed set of keys unless the source contract says so. Include harmless added metadata and its preservation on a later operation where applicable, while retaining missing/wrong-field and prior-state-mutation controls. The [playground audit](../../../evals/adversarial-cases/CROSS_EXAMINE_LEDGER.md) isolates an extra ticket field rejected by a stricter native schema than the written contract.

## Reduce without changing the question

Try removing one condition or operation at a time. Keep a reduction only when the case remains feasible, the intended perturbation still activates, and the same requirement/outcome discrepancy remains. Preserve positive/alternative controls. For stochastic systems, declare repeats and report variability; a lucky single run is not stable reproduction.

Keep the clean case, faulted case, no-op case, and any historical vulnerable/repaired versions identifiable. Reusing a name, fixture ID, or nominal fault type does not establish equal conditions. Record all trials against the parent's budget and preserve previous receipts when changing the driver.
