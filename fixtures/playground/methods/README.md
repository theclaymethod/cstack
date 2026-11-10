# Project-local method experiments

Run in a disposable playground workspace. The scripts use this project's native evaluator and task contract. They are examples to adapt, not an installed C Stack runtime. The core run needs only Python's standard library.

```sh
python3 -m methods.run --out eval-runs/methods
```

Use a new output path to reset. The driver refuses an existing destination and preserves source cases/spec/rubric/runner. It saves actual native traces, candidate snapshots, source identity, reduction history, fault configuration/events/process exits and dataset membership. Local processes have host permissions; these are trusted fixture candidates, not security containment tests.

## What runs

- `synthetic.py` constructs bounded structured contrasts and two-step request/state sequences. Every successor uses a native-valid actual prior output. A declared mutant ignores its own previously created ticket, passes all original static cases, and fails the repeated request. The reducer removes unrelated records one at a time, retains the same duplicate mechanism, checks conforming controls and rejects removing the prerequisite creation. A detection matrix selects witnesses against three explicit faulty candidates.
- `faults.py` runs clean, observed-noop, armed-unreached and three targeted process-stop trials. `fault_worker.py` pins source and maps named reservation/summary/completion boundaries to current native call/return events. It then tests once/persistent fsync/rename errors on the real atomic writer and native deadline/partial-output/nonzero/malformed candidates. These trace mappings are source-sensitive, not a stable product hook API. Storage exceptions do not simulate partial writes or power loss.
- `dspy_handoff.py` validates fixture-derived expectation authority, source/input identity and native schema, then exports JSONL plus a content/membership manifest. It groups connected ancestry and duplicate inputs together. Both partitions are exposed development data, including cases used for mutant selection; validation is not a final test.

Read `results.json` and the component results. Native case executions, reserved cases, process interruptions, candidate timeouts and DSPy program invocations are separate counters. An optional SDK check is explicitly `not-run` unless requested. Fault receipts do not become training examples.

The first native generation run reserves at most 300 case executions; the current deterministic search executes 95. Fault experiments execute 45 native cases with three owned-process interruptions and two candidate deadlines. Supervisor deadlines also bound workers. Every additional replay/test consumes its own work; source failure artifacts are never overwritten.

## Verify actual DSPy compatibility

Create an optional environment inside the generated project and install the pinned validation dependencies:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r methods/requirements-dspy.txt
.venv/bin/python -m methods.run --dspy-check --out eval-runs/methods-with-dspy
```

The validation snapshot pins DSPy 3.5.0 and its resolved dependencies. No model is configured. The check uses actual DSPy Example, Prediction, Module and Evaluate objects with this fixture's deterministic support function. Native criteria grade results, and the GEPA metric returns score plus failed checks and observed/required state deltas. It accepts valid outputs, rejects false creation claims, and retains schema/execution ERROR outcomes. This establishes compatibility, not optimization gains.

For a project-local program whose output is `dspy.Prediction(result=<native support output>)`:

```python
from methods.dspy_handoff import load, metric, gepa_metric

sets = load("eval-runs/methods-with-dspy/dspy-data")
trainset = sets["train"]
valset = sets["validation"]
```

Only `request` and `state` enter `example.inputs()`. The expected criteria stay in labels; there is no invented canonical ticket ID or reference note. Use `metric` with DSPy Evaluate and `gepa_metric` with the installed GEPA optimizer. Before a live compile, choose the mutable DSPy program, model/proposer, total budget and confirmation policy. Keep final confirmation separate from adaptive validation and retain native error accounting. This demonstration does not instantiate a live optimization campaign.

## Conditional methods

Explicit enumeration suffices for the initial action vocabulary. Add Hypothesis when its exploration/shrinking earns the dependency. Adopt Z3 only for constraints that justify independent encoding checks. Add a network adapter before testing Toxiproxy; no network dependency exists here. Native state is directly checkable, so semantic judges are deferred.

Harbor is preferred for new executable agent tasks. This fixture preserves its existing native JSONL runner; exporting examples does not migrate scoring. The skill references explain how to adapt methods to Harbor or another project's established format.
