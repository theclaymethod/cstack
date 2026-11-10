# Choose a failure injection method

Implement experiments in the project being evaluated. Reuse its real runner and permitted test boundaries. This reference supplies selection and evidence rules, not an injected-failure runtime.

| Boundary | First experiment | Required observation |
| --- | --- | --- |
| Reservation, measurement or commit | Stop an owned process at a named before/after boundary | Source-pinned event, matching actual termination, surviving state, reservation and recovery behavior. |
| Candidate subprocess | Deadline, flushed JSON prefix then deadline, valid output then nonzero exit, malformed output | Actual captured bytes and exit/timeout, native error classification and denominator/accounting. |
| Atomic local publication | Fail selected fsync/rename once, then persistently | Selected operation/occurrence, actual raised API error, unchanged prior publication, retry and cleanup behavior. |
| Real network dependency | Consider a loopback proxy only when the dependency exists | Traffic traversed the proxy, actual client/server effects and retry/commit identity. Proxy configuration alone is insufficient. |

## Freeze a small experiment

Choose the required behavior before injecting. Pin source and the boundary's before/after meaning. Bound cases, retries, interruptions and wall time externally. Keep each treatment and its clean/no-op/nonactivation controls in separate initial states. Recovery deliberately reopens the failed state; resetting it first would remove the evidence.

Prefer explicit test-only hooks. A source-sensitive mapping from a named boundary to Python tracing can be a small initial driver, but must pin its source hash and document the mapping. A return event can occur during exception unwinding. Verify the successful operation and surviving artifacts instead of treating a function name as proof. Configured, reached, action performed and downstream effect are separate observations.

Operator injection has extra access. A candidate exploit must work with candidate permissions. Keep receipts out of candidate claims and name the actual enforcement boundary. Scratch directories, interpreter flags and timeouts alone are not containment.

## Observe the fault and recovery

A supervisor's exit result and a matching boundary event jointly establish a targeted process stop. A partial measurement stays incomplete and charged; complete identity-matching evidence can be reconciled without another execution when the contract allows it. Repeated recovery must preserve the original evidence and accounting.

For storage experiments, interpose only the owned runner's selected API reference. Record a one-shot failure followed by healthy operations separately from persistent failure. Check published bytes and temporary artifacts after every attempt. An injected OSError models that API failure, not real disk exhaustion or a partial write. Process exit does not model power loss or storage durability.

For subprocess tests, observe the flushed prefix before claiming that boundary was exercised. An external supervisor cutoff remains incomplete evidence. Capture nonzero exits even when stdout looks valid. Clean up owned processes; descendants need their own ownership/termination policy if the fixture creates them.

## Decide whether the result helps optimization

Task inputs and program-visible dependency failures may support better behavior when the target can observe and respond to them. Evaluator crashes, unavailable infrastructure and operator-only receipts usually test the execution system instead. Keep those results in reliability checks unless an explicit task contract makes them actionable program evidence. Do not label every failed execution as bad model behavior.

The C Stack playground demonstrates owned process stops, subprocess output failures and scoped fsync/rename errors. It has no network service, so proxy experiments remain deferred. Its named trace mappings are version-sensitive demonstrations, not a portable hook API.

Sources: [Python tracing](https://docs.python.org/3/library/sys.html#sys.settrace), [subprocess timeouts](https://docs.python.org/3/library/subprocess.html), [SQLite anomaly testing](https://www.sqlite.org/testing.html), [Toxiproxy](https://github.com/Shopify/toxiproxy).
