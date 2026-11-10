# Run Eval: execute and inspect

Handoff:

> Use Run Eval to execute support_agent.py against this project's development suite. Reuse evaluate.py, preserve the original cases, and retain the actual output/state/error for every selected case. Report results and limits with the evidence directory. Then run a candidate I select in a fresh output directory and compare exact case membership and per-case changes.

Commands:

```sh
python3 evaluate.py run --candidate support_agent.py --suite development --out eval-runs/run-baseline
python3 evaluate.py run --candidate examples/candidates/regression.py --suite development --out eval-runs/run-regression
python3 evaluate.py compare --baseline eval-runs/run-baseline --candidate eval-runs/run-regression
```

The regression candidate intentionally improves the aggregate while breaking previously passing behavior. Inspect those traces rather than interpreting a higher aggregate as permission to replace the product.

Completion: actual candidate executions, exact selected IDs, code identity, preserved state evidence, separate ERROR/FAIL counts, and a faithful comparison. The trace JSONL can also be opened with the installed Create Eval trace-review helper. These deterministic fixture checks are not semantic judge calibration or measured model performance.
