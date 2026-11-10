# Simplify without changing the model

Materialize a disposable workspace and start a new agent session. The local adapter is documented in [the simplification guide](../simplification/README.md). Its models and cases are synthetic.

Give your agent this request:

> Use `$ablation` to reduce the full `old-fixture` prompt through `simplification.protocol`, keeping that simulated model fixed. Preserve the protected contract and use `evaluate.py` for every quality result. Minimize retained units and rendered UTF-8 bytes with zero observed pass regressions and zero quality loss against the original baseline. Use at most 120 native case executions, reserving eight for baseline/selected confirmation. Test combined deletions and keep a recoverable baseline, removal history, actual outputs and final artifact under a new `eval-runs/` directory. No provider calls or dependencies. Report uncertainty and distinguish fixture confirmation from unseen evidence.

Read the native traces and candidate snapshots, not only the selected score. Check that attempted deletions and their combined result were executed, structurally invalid candidates were distinguished from failures, the original quality baseline stayed fixed, and a budget stop was not called global minimality. The scripted demo is a control, not an agent's answer to this request.
