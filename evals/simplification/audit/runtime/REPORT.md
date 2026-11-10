# Runtime adversarial audit

Original authority: sibling audit INTENT.md and frozen sources. Materialized own fixture workspace; never modified frozen or repair copies. Source identity before/after matches. Native usage: **33 actual cases**, 40 reserved, zero paid/provider/network calls. Budget ceiling 200. All native attempts and perturbations are retained.

## Confirmed controls

- Native legitimate workflow executes full original and reduced development runs (8+8), freezes exact original/reduced final membership, executes both finals (4+4), finishes, and accepts original-baseline quality comparisons with all cases PASS. Lower burden is independently recorded by the adapter.
- Changing the caller-owned plan after freeze does not alter the frozen plan. `assertion-correction.json` corrects a driver-only alias comparison mistake in the initial `observations.json`; original false assertion and original driver are preserved. No extra executions were needed: actual frozen state independently establishes the expected three retained units.
- Late fitting and repeated final calls are rejected. Operator changes to live final plan, completed summary bytes, and a source file are rejected before any further native execution. Source file restored exactly.
- Operator stop at a source-pinned trace hook, immediately before the second `run_case`, activates once. Worker exits 22. One flushed PASS trace proves one completed actual execution. Native ledger preserves all eight reserved cases as pending. Experiment state remains pending with pre-call reserved count zero because process exited before its finally; no resume loader exists. Missing final summary blocks comparison. This is expected conservative interruption behavior, not evidence of a successful run or uncharged retry.

## Confirmed narrow observation for parent adjudication

**Operator-side durable ledger drift is not checked by `Experiment.checked()` / `compare()`.** After a completed run, an operator may replace `native/executions.json` with `{"limit":0,"reserved":0,"actual_completed":0,"calls":[]}` and comparisons remain accepted. Native results/snapshots, experiment state and in-memory reservation remain intact. This makes the persisted ledger disagree with accepted comparison evidence. `Experiment.verify()` verifies its state/contract and completed native artifact hashes, but not the native ledger file.

This does **not** demonstrate a budget bypass, wrong quality verdict, candidate-access exploit, or unsupported rejection. The minimal 8-case replay confirms that a subsequent measure still fails the in-memory budget gate. Arbitrary ledger mutation requires operator access; public simplification configurations only generate bounded deterministic candidates. The project expressly disclaims adversarial filesystem containment. Treat this as a possible artifact reliability gap, not a security finding or evidence of bad task grading.

Minimal standalone replay (use fresh output):

```
python3 eval-runs/runtime-audit/minimal-ledger.py eval-runs/runtime-audit/another-fresh-ledger-replay
```

The executed minimized replay is `minimal-ledger-replay/observations.json`; original and zeroed ledgers are retained. Full driver is `reproduce.py` and accepts a fresh output path. Initial full attempt uses 25 actual cases; executed minimal replay uses 8. No other native executions occurred.

## Evidence

- `source-identity-before.json`, `source-identity-after.json`: frozen runtime/source identity.
- `clean/`: 24 actual case outputs, full source snapshots and native verdicts.
- `observations.json`, `assertion-correction.json`: controls and zero-ledger comparison witness.
- `ledger-original.json`, `ledger-perturbed.json`: exact original and perturbed ledger bytes.
- `interrupted/`, `activation.json`, `interrupt-process.json`, `interrupt-observations.json`: named boundary, actual termination, retained incomplete state and reservation witness.
- `minimal-ledger.py`, `minimal-ledger-replay/`: minimized executed ledger control and budget rejection.
- `usage.json`, `artifact-hashes.json`: actual usage and retained artifact hashes. Artifact manifest predates this report and intentionally does not hash itself.

No actual candidate-access exploit or undeserved quality acceptance established in this bounded lifecycle/configuration audit. No production/model-performance claim is supported by these synthetic fixture results.
