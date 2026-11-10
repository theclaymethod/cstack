# Independent forward-use report

The staged skill supported a concrete offline handoff and bounded baseline/candidate comparison. This run establishes local workflow and response-shape mechanics only. There is no human calibration, live Jev/LLM implementation, provider execution, independent final validation, or production-readiness evidence. No skill defect was proven by this exercise.

The fixture factory materialized this workspace from `../cstack`; installed skills and canonical native assets were left unchanged. `eval-runs/forward-calibration-02/protection.json` records protected hashes and direct equality to the factory source. The independent scenario is `forward_scenario.py`; it uses native `prepare`, `Campaign`, adapters, and statistics helpers rather than the full demo.

## Contract and source authority

The task is the supplied synthetic support agent. A whole output passes only when all fixed native contract checks pass. Labels came from 24 actual native executions: twelve original cases for each of `support_agent.py` and `examples/candidates/improved.py`. The source observations and native grader verdicts are retained in `eval-runs/forward-calibration-02/full-source/native-source/`.

The calibration subset keeps both product outputs for each selected family together. Development uses `dev-howto` and `dev-explicit`; final workflow confirmation uses `conf-howto` and `conf-targeted`. Each partition has four outcomes from two families: three PASS and one FAIL. Selection was declared by scenario identity before judge execution. All fixtures and annotations are readable, and label-producing preparation ran in this context. Thus final is an execution role; it is not blind evidence. These separately authored synthetic cases share a contract and are not independently sampled production traffic.

Judge payloads contain only an opaque outcome ID, request, initial state, allowed expected task behavior, evaluated output, and criterion revision. They omit correctness labels, annotation authority, partition, family, source filename, and selection metadata. Expected behavior is explicitly allowed reference evidence. The outer contract rejects extra `gold` fields in both backend probes. This is an inspected input boundary; the local processes have host filesystem access and are not contained from reading private labels. The candidate directly calls the same deterministic grader that produced the labels, making perfect agreement a deliberately circular mechanics control.

The baseline uses the predeclared `claim-only` fixture policy. The candidate uses `state-witness`; Jev-shaped decisions also change the fixed-score threshold from 0.8 to 0.5. This changes permitted judge policy and decision threshold without changing product criteria. There was one predeclared candidate, no learned prompt, no trained weights, no fitted probability mapping, and no owner-provided error-cost policy. Development acceptance requires exact fixture agreement and full coverage; production acceptance remains unspecified.

## Executed evidence

Development and final produced the same raw counts below; each table row is four outcomes, not eight independent examples. Failure is positive.

| Judge | Agreement | Kappa | TP | FN | FP | TN | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LLM-shape baseline | 2/4 | -0.3333 | 0 | 1 | 1 | 2 | 4/4 |
| LLM-shape candidate | 4/4 | 1 | 1 | 0 | 0 | 3 | 4/4 |
| Jev-shape baseline | 3/4 | 0 | 0 | 1 | 0 | 3 | 4/4 |
| Jev-shape candidate | 4/4 | 1 | 1 | 0 | 0 | 3 | 4/4 |

Each baseline misses its only gold failure: false passes among gold failures are 1/1. The LLM-shape baseline also falsely rejects 1/3 gold passes; the Jev-shape baseline falsely rejects 0/3. Both candidates catch 1/1 failures and reject 0/3 passes. Main comparison rows contain no UNKNOWN or ERROR. Two deliberate invalid-input subprocess probes are separate and each exits nonzero and normalizes to ERROR; they were not silently excluded from a scored corpus.

The Jev-shaped fixture reports fixed numbers 0.15 and 0.65, not provider-calibrated probabilities. On each four-row partition, Brier changes from 0.2975 to 0.0475 and log loss from 0.817995 to 0.229585. Reliability bins and raw scores are retained. These values exercise arithmetic and reflect changed discrimination as well as event predictions; they establish no probability calibration. LLM-shaped responses provide no probabilities, so Brier and log loss remain unavailable. Explanations for the typed format remain unavailable; LLM reasons explicitly identify the deterministic fixture rather than fabricated model reasoning.

Uncertainty uses the helper's paired whole-family percentile bootstrap: 200 draws, seed 17, nominal 95%, two declared families per partition. Kappa and failure-rate intervals are suppressed because 45/200 bootstrap draws have undefined statistics. Narrow coverage bounds of [1,1] reflect this fixed fixture and do not certify population reliability. Three identical replies for one frozen item per backend demonstrate deterministic fixture repeatability and add zero independent gold examples.

Native-shape normalization checks exercise Noul in both polarities and binary Choice with consistent failure decisions. Unsupported ordinal Score and malformed LLM JSON return ERROR; explicit LLM UNKNOWN is retained. These are local normalization tests, not SDK compatibility tests. No malicious process containment, live response transport, timeout recovery, or broad adversarial model robustness was established.

Both baseline and candidate configurations and all planned final predictions were frozen before comparison. An early final comparison was rejected. Final fitting was blocked after consumption. The full planned prediction evidence, inputs, configs, parser outputs, source checksums, and raw subprocess stdout/stderr are retained. Internal `Campaign.rows()` reads the fully exposed labels to check membership and projection; its phase guards should not be described as access control or actual blindness.

## Accounting and handoff

The actual call ledger contains exactly 24 native-source case subprocesses and 40 local fixture-judge subprocesses: 16 development, 16 final, six repeatability calls, and two invalid-input probes. All main observations completed; both invalid-input probes intentionally failed. There were zero provider calls, paid calls, generative proposer calls, or case/judge retries. The fixture factory also used local Git initialization, and Python platform detection used a local utility; these are not source-case or judge calls. No network operation was issued.

A first instrumentation-only attempt failed before native execution because the call tracker accidentally included Python platform detection's binary utility output. Its directory `eval-runs/forward-calibration/` is preserved. The corrected scenario used fresh identity `forward-calibration-02`; no completed case or judge execution was repeated by that correction. This was an experiment harness mistake, not a staged-skill finding.

The recoverable baseline, selected fixture configuration, adapter, worker invocation, and source manifest are recorded in `eval-runs/forward-calibration-02/judge-handoff.fixture.json`. Run envelopes follow `{"input": <inputs.jsonl row>, "config": <backend configuration>}` and the fixture worker accepts stdin using `python3 judge_calibration/fixture_backend.py`. This is an offline stand-in, explicitly marked nondeployable. A live handoff still needs an authorized backend/model and supported client, authoritative human or otherwise approved labels, a defined costly-error/review policy, a funded execution plan, and fresh independent confirmation evidence.

Raw evidence: `eval-runs/forward-calibration-02/calls.jsonl`, `summary.json`, `contract.json`, `development.json`, `final.json`, `checks.json`, `dataset/manifest.json`, and `campaign/*/predictions.jsonl`. The final result supports selecting the deterministic candidate for this exposed fixture; it supports no deployment or real-model performance claim.
