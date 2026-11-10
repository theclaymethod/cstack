# Independent forward-use result

The new references were sufficient to adapt three recipes without importing or executing the supplied `methods.run` driver: structured contrast enumeration, record/field reduction with rechecked controls, and valid-output/nonzero-exit subprocess failure. No canonical fixture, evaluator, spec, rubric, skill or native suite was edited.

## Construction and authority

Original source: `evals/spec.json`, rules 3, 5, 6. An explicitly selected account must belong to `request.accounts`; otherwise clarify and preserve the supplied state. Creation on a listed explicit account must append exactly one valid ticket while preserving other state. The exact spec/evaluator/core-suite/rubric hashes are frozen in `frozen-contract.json`; individual case provenance and input hashes are in `provenance.json`.

The new pair holds the explicit selection `chosen`, affirmative request text and initial state constant. It changes only the sole available account: `available` versus `chosen`. Initial state includes an unrelated closed password ticket and opaque preferences. The first reduction removes the whole unrelated record; the second removes the whole preferences field. Every retained reduction preserves the same unauthorized-account creation defect and has its listed-account control rechecked. Both conditions are feasible native-schema inputs. No rejected reductions occurred; the run stops after two planned deletions and does not establish global or 1-minimal size.

All six cases and all descendants use one construction family and one adaptive development partition. Expectations are explicit synthetic fixture-contract labels, not human judgments or Bootstrap approvals. Proposed defect label: **baseline creates a VPN ticket on an explicit account absent from available accounts**. The native result and actual ticket state establish that narrow synthetic-contract violation. Parent adjudication remains separate.

## Actual results

| Arm | Selected/executed | PASS | FAIL | ERROR |
| --- | ---: | ---: | ---: | ---: |
| Baseline over three contrast pairs | 6/6 | 3 | 3 | 0 |
| Existing legitimate candidate over those pairs | 6/6 | 6 | 0 | 0 |
| Valid JSON then exit 7 treatment | 1/1 | 0 | 0 | 1 |

Each failing baseline artifact contains one appended ticket whose account is not in `request.accounts`; the driver independently checks that resulting state. All three legitimate listed-account controls pass under the real grader. The failure treatment is an operator-owned copied candidate with `flush`, stderr marker and explicit exit 7 appended after its normal JSON print. The captured stdout parses as complete JSON and exactly equals the matching clean output; the real subprocess exit is 7 and native outcome is ERROR. The ERROR remains in a selected denominator of one and is not exported as a bad model label. This models candidate subprocess nonzero termination after output, not a killed evaluator, power loss, storage durability or a hostile candidate exploit. There are no process interruptions, timing races or unresolved activations.

Execution used `evaluate.py run` for each arm, preserving native snapshot/manifest/traces/summary publication. Exact commands and stdout/stderr are retained in `commands.json`. Every candidate run used fresh native scratch state; candidate permissions remained ordinary host permissions, with no containment claim.

## DSPy handoff

The optional existing environment successfully ran DSPy 3.5.0 Example, Prediction, Module and Evaluate objects. A deterministic local Module directly called the existing improved candidate function six times, and the metric called native `evaluate.grade`. It passed all six examples (100%). Three extra metric-only checks accepted an alternative unique ticket ID, rejected an incorrect account as FAIL, and retained malformed output as ERROR. These checks did not execute another candidate or call any model.

Only `{request,state}` enters the Module through the `payload` input field. Criteria remain Example labels. `dspy-examples.jsonl` contains those example objects; `dspy-metadata.json` records authority, excluded operator-only evidence, source/case/provenance identities, and the declared resume validation policy. This is a frozen handoff, not a resumable campaign or implementation of a resume guard. All connected examples belong to adaptive development. Metadata and operator receipts do not enter model inputs. No golden ticket ID or required explanatory wording was invented.

Totals: **13 native subprocess case executions plus 6 deterministic SDK program executions = 19 program case executions**, 3 further metric-only checks, **0 owned-process interruptions**, **0 provider/network calls**, no installs. This remains below the 40-execution ceiling even if every extra metric-only check is charged as a case. Full unittest discovery was not run because the assigned experiment had a strict execution budget; the actual native runner and focused SDK checks above provide the evidence.

## Reproduction and limits

In a newly factory-created workspace, copy `adapt_recipe.py` into `eval-runs/forward-use/` and run `python3 eval-runs/forward-use/adapt_recipe.py`. Its existing-output refusal is intentional: use a fresh workspace/output for replay. Then run `sdk_handoff.py` with the project-local interpreter containing DSPy 3.5.0. The SDK file imports the existing native grader and improved candidate, and makes no model calls. The native output directories preserve candidate snapshots and case sources.

This is an independent adaptation from the references and raw spec, with no proven guidance problem. It establishes a controlled baseline defect and correct error accounting for these fixtures; it does not establish broad coverage, human calibration, prompt gains, GEPA compatibility, model performance, hidden validation or production behavior. Artifact inspection does not prove network isolation; the scripts contain no network or provider calls and only import the local deterministic candidate and installed SDK.
