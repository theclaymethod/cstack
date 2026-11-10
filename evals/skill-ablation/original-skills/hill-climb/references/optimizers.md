# Choose an optimization method

Read when selecting or adapting a backend. Reuse the project's existing program representation and evaluator. The methods below inform the workflow; none is a prerequisite, and their library defaults do not replace the campaign contract.

| Project situation | Useful option | Integration boundary |
| --- | --- | --- |
| Existing DSPy program | DSPy GEPA or MIPROv2 | Compile represented modules using the project's metric/examples; preserve actual selection membership and model configuration. |
| Existing Ax program | Ax's own optimizers | Use its native evaluator/feedback adapter; verify language/version support and actual validation coverage. |
| Text artifacts, prompts, skills, or code evaluated by an existing command | GEPA `optimize_anything`, or an agent-led loop | Translate candidates to the existing execution boundary; capture score and diagnostic feedback without changing grader semantics. |
| Large or complex traces | Halo-style diagnosis, optionally its engine | Produce evidence-backed hypotheses and proposed fixes; candidate edits, new executions, and promotion remain the campaign's responsibility. |

DSPy and Ax are separate frameworks. GEPA is a reflective search method with implementations/integrations that differ in budget, sampling, state, and interface. Pin the actual installed implementation before using code examples. An optimizer can count one metric evaluation while the evaluated program makes several model/tool calls.

GEPA-style feedback pairs a score with actionable evidence: failed assertions, outputs, tool results, concise trace excerpts, or costs. Keep evidence distinct from a model's explanation. Its per-example candidate archive can retain specialists, and component merging can suggest combinations; a merged artifact still needs execution. Search archive membership is not final promotion.

HALO's useful discipline is to inspect failure patterns across traces and anchor conclusions to selected evidence. Production telemetry and a particular collector are not entry requirements for Hill Climb. Use the execution evidence the project actually has; adopt heavier analysis tooling only when it earns its setup cost.

Some backends repeatedly use `valset` to choose candidates. Treat that as adaptive development data. Confirm selected artifacts separately under the campaign's agreed protocol. Account for final checks, retries, and proposer work when a library's main budget counter excludes them. Persist backend state together with the campaign contract; a backend checkpoint alone does not prove a compatible resume.

Primary sources inspected for this workflow:

- [DSPy GEPA implementation, revision 4e9db7a](https://github.com/stanfordnlp/dspy/blob/4e9db7a83e71e4c36315a2402ae7ffd0c6493404/dspy/teleprompt/gepa/gepa.py) and [MIPROv2](https://github.com/stanfordnlp/dspy/blob/4e9db7a83e71e4c36315a2402ae7ffd0c6493404/dspy/teleprompt/mipro_optimizer_v2.py).
- [Ax optimize helper, revision 3ad7b69](https://github.com/ax-llm/ax/blob/3ad7b69947e05f1770b1bd6cb1316a8ec7fcd106/src/ax/dsp/optimize.ts) and [Ax GEPA](https://github.com/ax-llm/ax/blob/3ad7b69947e05f1770b1bd6cb1316a8ec7fcd106/src/ax/dsp/optimizers/gepa.ts).
- [GEPA optimize_anything article](https://gepa-ai.github.io/gepa/blog/2026/02/18/introducing-optimize-anything/) and [public API, revision ce5b0d6](https://github.com/gepa-ai/gepa/blob/ce5b0d6e3d6af6c6dbec6de2c54536bbb961d309/src/gepa/optimize_anything.py). The live article's examples and inspected API differ; inspect the installed version before integration.
- [HALO walkthrough, revision b7f8509](https://github.com/context-labs/HALO/blob/b7f8509745d67b499b4e80efe20ea37c03426a74/demo/appworld/README.md) and [engine configuration](https://github.com/context-labs/HALO/blob/b7f8509745d67b499b4e80efe20ea37c03426a74/engine/engine_config.py).

These are source inspections, not a measured comparison or a guarantee of gains on the target project. Read current primary docs/source before installing an optional backend.
