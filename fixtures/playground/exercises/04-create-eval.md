# Create Eval: use the native format

Start with your reviewed Bootstrap handoff or a scoped judgment captured from an actual run. Read `evals/spec.json`, `evals/rubric.md`, and `evals/cases.jsonl` for this project's existing format.

Handoff:

> Use Create Eval to turn the approved handoff into native JSONL cases under evals/generated. Use evaluate.py's existing run --cases option. Trace each input, context, expected outcome, and family to its approved source. Preserve acceptable alternatives and keep pending cases separate. Run legitimate and failing controls through the actual grader. If the desired action is beyond the current runtime/action vocabulary, report that integration gap rather than pretending an unrelated check measures it.

Required case fields are `id`, `suite`, `family`, `request`, `state`, and `expected`; inspect actual examples and runner validation for their types. Keep source authority separate from agent-generated expected outputs. If a new kind of state/action genuinely needs grading support, review that evaluator change as a new measurement revision before using its scores.

Completion: replayable approved cases in the native format, an explicit incomplete list, source/representation fidelity, and observed grader controls. Expectation approval alone does not establish a human label on a generated output or calibrate a semantic judge.
