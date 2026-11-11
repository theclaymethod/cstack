# Hand generated evidence to DSPy

Use this when an existing DSPy program can benefit from generated examples or diagnostic feedback. Keep the adapter, dependencies, data and execution code inside the consuming project. This skill does not require DSPy, a cstack fixture or a particular optimizer.

## Define the example boundary

Map only program-visible inputs into `dspy.Example(...).with_inputs(...)`. Expected criteria, source/approval status, ancestry, split membership and operator receipts stay outside those inputs. A criterion-only example is useful when the native metric judges the result without one canonical reference answer. Do not invent a golden ticket ID or explanatory wording just to fill an output field.

Export only examples with the authority required by the project. Proposed model labels remain proposed. Explicit synthetic fixture rules can establish fixture expectations without becoming human judgments. Validate native schema, expected behavior, source identity and input hashes before export; reject stale expectations after transformations.

Keep connected construction ancestry and exact duplicate inputs in one development partition. Persist membership and content identities, and reject changed files or source contracts on resume. Optimizers may repeatedly consult validation, so that partition is selection evidence, not an independent final test.

## Reuse native scoring

Have a project-local scalar metric call the existing grader with the original input, expected criteria and actual predicted result. Keep native PASS, FAIL and ERROR separately observable even if optimization maps nonpassing results to score zero. Preserve selected errors in reported denominators and count actual program, proposer, retry and confirmation costs.

For GEPA, return score plus evidence-backed feedback through the installed implementation's supported metric interface. Failed checks, observed state differences and explicit execution errors are useful feedback. A program-level metric does not establish attribution to an individual predictor. Inspect the installed API and pin the version tested instead of copying a floating signature blindly.

Faults qualify as optimization examples only when their relevant effects are visible to the program and the target can respond. A killed evaluator tests execution recovery; feeding its private activation receipt into the model would change the task.

## Verify compatibility before optimizing

Use real SDK Example, Prediction, Module and Evaluate objects with a deterministic local program. Check that labels do not enter program inputs, alternate valid outputs pass, wrong outcomes fail, errors remain visible and native aggregate semantics agree. Such a check establishes SDK/data/metric compatibility, not a prompt optimization gain.

A live campaign additionally needs the mutable DSPy program, model, proposer, budget, candidate execution and confirmation policy. Use [the campaign contract](campaign.md). Preserve the baseline when no candidate earns promotion.

The project-local playground demonstration uses DSPy 3.5.0 in an optional development environment and makes no model calls. It exports native JSONL plus metadata; Harbor tasks can continue to use their own format and execution boundary. No optimizer SDK becomes a skill installation dependency.

Sources: [DSPy Example](https://github.com/stanfordnlp/dspy/blob/main/dspy/primitives/example.py), [DSPy metrics](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/learn/evaluation/metrics.md), [DSPy GEPA](https://github.com/stanfordnlp/dspy/blob/main/dspy/teleprompt/gepa/gepa.py).
