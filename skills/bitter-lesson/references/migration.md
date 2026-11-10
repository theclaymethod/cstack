# Comparing model and prompt changes

Use this reference for attribution, provider guidance and production release evidence.

## Model by design comparison

| | Existing design | One frozen simplified design |
| --- | --- | --- |
| Production model | Production baseline A | Simplification on production model B |
| Candidate model | Upgrade with design held fixed C | Proposed bundle D |

Run each available cell through the actual project execution boundary. Preserve per-case and repeated-trial membership, actual outputs/state, full configuration and costs. Reuse a recorded cell only when its artifact, inputs, evaluator, conditions and trial protocol satisfy the current comparison; regrading old outputs cannot measure a changed model or prompt.

`C − A` estimates the model change with the existing design. `D − C` estimates simplification on the candidate model. `D − A` compares the proposed release to production. `B − A` estimates simplification on the production model; `(D − C) − (B − A)` describes the interaction on the chosen outcome scale. These interpretations require comparable conditions and a credible sampling design. Do not attach causal certainty to an uncontrolled historical comparison. [NIST full-factorial design](https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm).

The three-cell A/C/D comparison is useful when B is unavailable. If A is also unavailable and cannot be recovered comparably, report that limit. D versus C can establish a new-model ablation result; it cannot establish that the upgrade enabled that reduction or that D meets the old production quality bar. Missing cells remain unrun. Independently tuned simplified prompts for each model are different treatments, not the same B/D column.

## What to reconsider

Sutton's essay motivates revisiting human-built complexity as general capabilities improve; it is not a theorem about prompt length. The author's original URL is reproduced in this [university-hosted facsimile of The Bitter Lesson](https://www.cs.utexas.edu/~eunsol/courses/data/bitter_lesson.pdf).

Provider recommendations are starting hypotheses. OpenAI recommends simple, direct reasoning-model prompts and trying zero-shot first while retaining clear constraints. Anthropic's migration guidance describes reducing some old thoroughness and aggressive tool-use prompting. Check the guidance for the actual selected model before applying it. [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices), [Anthropic prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Simpler scaffolding need not mean fewer context tokens: a long-context SWE-bench study supplies environment content directly. Keep task knowledge separate from the recipe for using it. [Putting It All into Context](https://arxiv.org/html/2505.08120v1), [Context-engineering guidance](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents).

Start with the project's identified workarounds and failure history. Use [Ablation's removal reference](../../ablation/references/removal.md) for dependencies and combinations, and its [quality reference](../../ablation/references/quality.md) for original-baseline constraints, uncertainty and evidence exposure. Neither shorter input nor a newer model identifier is an acceptance test.

## Production evidence

Offline evals should cover representative traffic and consequential behavior, including malformed outputs, failure/review paths and relevant tool state. When a model-based judge is used, keep its approved version fixed; do not tune it to reward the new prompt. Preserve actual error and unknown counts and check critical slices separately from averages.

Measure full execution costs and latency, including output/reasoning work, retries and tools. Cache policy, concurrency, rate limits and model effort can materially affect those measurements. Mark unknowns. Pin model versions when available and retain bundle content hashes and the original baseline. [Official prompt-version guidance](https://developers.openai.com/api/docs/guides/prompt-engineering).

An authorized shadow run copies requests and discards candidate responses; suppress or isolate side effects for agents. It does not reveal how users would respond to candidate behavior. Canary exposure compares bounded live traffic with a control and predeclared rollback conditions. Follow the project's existing release authority and rollback the complete model/prompt/configuration bundle. Preparing an experiment does not authorize deployment or new paid calls. [Google SRE canarying guidance](https://sre.google/workbook/canarying-releases/).

Revisit the comparison after a model alias/version, task distribution, context assembly, tool interface or evaluator changes. Keep offline checks, live measurements, human labels and deterministic stand-ins named separately; each supports different claims.
