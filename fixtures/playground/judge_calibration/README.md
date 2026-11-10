# Offline judge-calibration mechanics

Run this project-local demonstration in a disposable playground workspace:

```sh
python3 -m judge_calibration.run --out eval-runs/judge-calibration
```

Choose an unused output path. The core run uses only Python's standard library. No SDK, credentials, hosted platform or provider is called. The reference-only skill works without this demonstration installed.

## What the result establishes

The native runner executes the original and conforming support candidates on the twelve existing cases, producing 24 actual output/label records across twelve source families. Those labels are code-derived synthetic outcomes, never human gold. Both outputs for a task stay together in one partition. Eight rows/four families go to each train, validation and final workflow role. The complete fixture and labels are readable; final-role validation is not independent blind model evidence.

`fixture_backend.py` is a deterministic stand-in, not Jev or an LLM. It emits the native-style Noul distribution or structured LLM verdict shape. Its candidate policies are predeclared claim-only and native-state checking. The latter reuses the source oracle deliberately, so improvement demonstrates protocol mechanics rather than independent judge learning. Typed probabilities are fixed synthetic scores, not calibrated forecasts.

The driver records the untuned training baseline, tries two LLM policy configurations and four typed policy/threshold configurations on validation, then freezes the exact final baseline and selected configurations. All planned predictions must finish and freeze before final comparison. Further fitting or unplanned final candidates are rejected. This guard applies within one nonresumable local campaign; another output directory is not a claim that old gold became unseen.

There are 102 fixture judge subprocess calls within a 200-call ceiling, including six calls for repeatability on one frozen item per backend. Repetition counts are separate from the number of source items. These are local program executions, not model invocations. Native source execution costs and fixture worker counters are separate. The fitting objective includes every selected row; errors/abstentions earn no agreement. Exact-match acceptance is only an illustrative fixture control, not a default deployment threshold.

## Read the evidence

- `dataset/` contains native source traces, separately projected inputs, private-by-convention label/provenance rows and source/content hashes. The expected task behavior is a permitted reference; the output's correctness verdict and gold metadata are excluded from judge inputs.
- `campaign/` preserves raw stdout/responses, normalized verdicts/errors, configurations, frozen manifests, campaign-anchored content hashes and completion/budget/exposure state. File hashes provide consistency, not security against a writer who can rewrite all state. The fixture workers retain local host permissions.
- `fitting.json` records the candidate grid and validation comparisons. `results.json` compares baseline/selected outcomes on final-role data, records stability separately and explicitly marks both live backends unrun.
- `selected-judge.fixture.json` is an offline fixture artifact with no production-release policy. It is not a deployable model or a judge calibrated to human labels.

The measurement module handles nominal/ordered weighted kappa, confusion counts, all-attempted coverage, class-conditional errors, family-bootstrap diagnostics, Brier/log loss and reliability bins. Undefined metrics and bootstrap replicates remain visible. Sparse families can leave intervals unavailable even with perfect point agreement. LLM verdicts have no native probability in this example; a missing probability is not an execution error.

The typed normalizer supports Noul and binary PASS/FAIL Choice. It tests yes/failure polarity, review bands, finite probability validity and the difference between probability and confidence. Native ordinal Score requests, real client/provider execution, fitting a probability calibrator and model weight training remain unrun. The skill references explain their capability-dependent treatment rather than pretending this binary fixture implements them all.

Use `python3 -m unittest discover -s tests -p test_judge_calibration.py -v` for the focused checks. The combined runner exposes `--suite judge-calibration`, and `--suite all` includes the demonstration and native tests.
