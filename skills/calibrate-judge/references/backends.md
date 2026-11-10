# Adapt to judge capabilities

Inspect the consuming project's installed model/client and pin the actual implementation. These are method references, not bundled clients or provider installation requirements.

| Backend | Useful fitting levers | Retain |
| --- | --- | --- |
| Jev-style typed decision | Atomic questions, input state, yes/no polarity, option/level definitions; supported probability mappings and thresholds | Native decisions/distributions, reported model version, raw response and usage. Explanations remain unavailable unless the backend supplies them. |
| Traditional LLM judge | Instructions, examples, supported inference parameters and structured verdict schema | Actual output, parsed decision, concise evidence summary when supplied, parse/refusal/transport status and usage. |
| Specialized evaluator or trainable model | Supported rubric/reference template and optionally an authorized training interface | Checkpoint, training authority, compatible input/output template and separate score calibration. |

## Typed decisions

For TypeSafe Jev, Choice selects a category and returns probabilities; Noul returns the probability of yes; Score represents ordered levels. Define what yes and each category mean relative to the project's positive class. A yes to “is this acceptable?” has the opposite polarity to a yes to “does this violate the criterion?” Normalize explicitly and test both directions.

Preserve event probabilities. Jev's confidence is a concentration statistic, not interchangeable with probability of correctness. An expected ordinal score is not P(PASS). A conventional LLM's verbal certainty is not automatically calibrated probability either. Apply supported probability calibration or review thresholds to the actual chosen event, with the source question/options and label order frozen.

Keep questions atomic and give each the permitted evidence it needs. A bounded typed response can still be wrong, injected or unstable. Do not infer accuracy or robustness from schema validity, low latency or provider calibration claims. Inspect per-question errors and compare repeated calls on identical frozen evidence without counting them as new gold examples.

Sources: [TypeSafe System One](https://docs.typesafe.ai/concepts/system-one), [Choice](https://docs.typesafe.ai/primitives/choice.md), [Noul](https://docs.typesafe.ai/primitives/noul), [confidence](https://docs.typesafe.ai/confidence). [LangChain's Jev experiment](https://www.langchain.com/blog/jev-agent-evals-langsmith) separates human agreement and repeatability on a small frozen corpus; its repetitions do not establish broad independent coverage.

## Generative judges and optimizers

Use the project's declared schema, including explicit uncertain/error outcomes. Keep output length and evidence style out of correctness unless the task actually requires them. Parse deterministically and preserve malformed output, refusals and incomplete calls. Do not ask for private chain-of-thought or treat a plausible rationale as an independent correctness witness.

DSPy/GEPA can optimize judge instructions against authoritative development labels. Its proposer may receive observed-versus-expected decisions and approved expert explanations from exposed fitting cases. An adapter executes the proposed questions against a typed target; the target need not generate feedback text. Keep gold outside runtime inputs and count proposer, target, retry and confirmation work separately. See the [project-local data handoff](../../hill-climb/references/data-handoff.md).

When backend execution is unavailable or forbidden, prepare its configuration/interface and validate normalization with explicit fixtures. Report response-shape support separately from actual SDK/provider execution and real calibration. A deterministic stand-in is not a live model implementation.

Sources: [DSPy GEPA](https://github.com/stanfordnlp/dspy/blob/main/dspy/teleprompt/gepa/gepa.py), [Dropbox judge optimization](https://dropbox.tech/machine-learning/optimizing-dropbox-dash-relevance-judge-with-dspy), [Prometheus 2](https://arxiv.org/abs/2405.01535). Model-specific templates and benchmarks do not establish agreement with this project's experts.
