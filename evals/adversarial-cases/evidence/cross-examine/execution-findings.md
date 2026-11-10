# Independent execution attacker: bounded no-defect result

No unsupported native PASS, rejected legitimate control, or misleading recovery was demonstrated in the exercised paths of the frozen `/adversarial-cases` construction workflow. The supplied defective proxy was not used as a new finding. Root and the independent intent reviewer retain adjudication authority.

The original requirement is in `../ORIGINAL-CONTRACT.md`. Target source is `../frozen`; a private workspace was materialized using its native factory. `observations.json` contains the structured contract, permissions, scenario cards and limits. `protected-source-sha256.json` matches 39 protected source/skill files to the pre-execution private-workspace hashes. Runner, original candidate, spec, cases, rubric and installed skills remained byte-identical.

## Observed boundaries

| Case or control | Actual observation | Native result / interpretation |
| --- | --- | --- |
| Clean creation, preserved-context and minimal inputs | Exactly one selected-account open VPN ticket; originals and other state preserved | PASS 2/2 |
| Legitimate unique ID and explanatory wording | Valid tickets with different ID prefix and note | PASS 2/2; no wording/ID false rejection |
| Creation claim with unchanged state | Zero new tickets in returned state | FAIL 2/2; no undeserved creation credit |
| Four intermediate one-condition reductions | Remove profile, other-account ticket, closed ticket, unused account; retain claim and two legitimate controls at each stage | 12 executed cases: false claim rejected, legitimate controls accepted |
| Malformed stdout | Candidate exits 0 with non-JSON stdout | ERROR 2/2, selected denominator 2 |
| Candidate runtime exception | Candidate actually exits 1; raw traceback retained | ERROR 2/2, selected denominator 2 |
| Corrected native scratch reset probe | No initial sentinel in each cwd; two distinct cwd paths independently absent after trials | PASS 2/2; narrow reset observation, no containment claim |
| Clean uninstrumented baseline | All eight canonical cases measured | Native score 0.5; known synthetic baseline behavior |
| Armed unreachable attempt-999 trigger | Activation count 0, no activation log, normal process exit; outputs exactly match clean | Not activated; native baseline 0.5 |
| Kill after two flushed trace rows, before third case | Matching source-pinned event and same PID exit -9; two actual cases, no summary | Remains pending, best null, all eight reserved case runs charged |
| Kill after complete summary publication | Matching event and exit -9; eight complete native case measurements retained | Status recovers complete baseline, score 0.5; no candidates rerun |
| Kill after `complete_attempt` returns before ledger save | Matching event and exit -9; in-memory transition not durable | Status recovers complete baseline, score 0.5; no candidates rerun |
| Kill after proposal decision before ledger save | Matching event and exit -9; proposal measured 8/8 PASS, no decision on disk | Status recovers `retain improvement`, best attempt 1, score 1.0 |

Every lifecycle recovery was followed by repeated status. Repeated state and evidence inventories were identical; recovery changed only `state.json` where reconciliation was needed. Completed measurements matched the clean baseline's actual outputs. Two-result partial evidence remained unchanged and pending. These experiments did not invent an expectation that every crash must cause task failure.

Activation evidence is operator-side: the injector pins the runner SHA-256, records the Python boundary, event, line, PID and source hash, fsyncs that record, then kills only itself. The parent process independently observes -9 for that same PID. The line-based partial trigger is version-fragile and protected by the source-hash precondition. Candidate claims alone are not used to establish an interruption. The unreachable trigger's normal exit and zero activations establish non-activation, not resilience under a crash.

## Setup mistakes and accounting

The first reset-probe revision inserted its diagnostic marker before importing `json` and `sys`. Both selected cases exited with `NameError`. This was an attacker construction setup error, not a target defect or a reset failure. Its sources, raw stderr, ERROR results and zero score are preserved in `evidence/native-reset-probe`. The first construction driver's final expectation assertion therefore exited 1 after its native experiments were complete. `finalize.py` corrected only the candidate wrapper in a new `reset-probe-r2.py` and ran two additional cases; the original failed artifacts were not replaced.

A separate deliberately mismatched operator source hash was rejected before native invocation. It consumed no candidate execution and activated no fault. Its setup receipt is retained.

Actual totals are **76 candidate case executions and four owned-process interruptions**, within 120/4 limits. Of these, 50 cases were lifecycle measurements and 26 custom/control/reduction executions. The 26 include the two setup-error probe cases. Lifecycle reservations total 56, exceeding actual lifecycle executions by six because the two-case interrupted attempt reserves eight. Reservations are not reported as executions. Zero provider, paid or network calls were made.

## Evidence and reproduction

- `workspace/eval-runs/attack-execution/evidence/counts.json`: reconciled actual totals.
- `workspace/eval-runs/attack-execution/evidence/commands.json`: native command receipts, raw stdout/stderr and exits.
- `workspace/eval-runs/attack-execution/evidence/lifecycle-observations.json`: before/after/repeated state, inventories, activations and actual executions.
- `workspace/eval-runs/attack-execution/evidence/score-observations.json`: native scores and independently derived ticket/state witnesses.
- `workspace/eval-runs/attack-execution/evidence/reduction/observations.json`: one-condition reduction history and rechecked controls.
- `workspace/eval-runs/attack-execution/evidence/protected-before.json` and `protected-after.json`: unchanged protected assets.
- `workspace/eval-runs/attack-execution/evidence/all-evidence-sha256.json`: raw evidence hashes.
- `workspace/eval-runs/attack-execution/evidence/construction-setup-error.json`: preserved construction failure and correction attribution.

`reproduce.py`, `finalize.py` and `reduce.py` are the executed drivers; `inject.py` is the operator-only tracer. The convenience wrapper `replay_private.py` invokes the frozen factory and these components in order, retaining the expected first-driver assertion failure followed by the corrected probe. The wrapper itself is unexecuted; its constituent commands were executed and checked. A replay would consume another 76-case/four-interruption budget. From the audit workspace root:

```sh
python3 work/adversarial-audit/attack-execution/replay_private.py --out work/adversarial-audit/attack-execution/reproduction-workspace
```

## Limits and unexecuted ideas

This is synthetic development construction using the native runner and actual local process observations. It is not held-out/model performance, human calibration, production reliability, exhaustive skill evaluation or security containment. Candidates have trusted local host access; no candidate attempt to modify protected source or escape the native temp cwd was made. Operator tracing is extra access and is not attributed to the evaluated candidate.

Each interrupted boundary was executed once, with deterministic source predicates. Four interruptions exhaust the allowance. Real external dependency/retry faults, power-loss/storage durability, full finish/confirmation interruption, and more crash trials were not executed. There is no external dependency hook in this fixture; candidate runtime errors are not relabeled as such a dependency injection. The two valid reset cwd observations cover that narrow behavior only.

Frozen audit `replay.py` and `inject_native.py` were inspected and left unchanged; replay was not executed because its interruptions would exceed this attacker's allowance. Its validation is a native control path, not an independent semantic judge of all skill behavior. No repair is requested from these observations.
