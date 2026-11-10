# Evals before relevant production traces

Use this for a new product, a new feature, or an uncovered capability. Production traces are useful evidence, not an entry requirement. The first useful loop is **realistic input → actual feature run → inspectable trace → expert observation → repeatable check**.

## Define the feature and its coverage gaps

Recover the intended behavior, supported alternatives, current implementation entrypoint, and decision the eval should inform. For an existing product, isolate the feature delta: changed inputs, tools, knowledge, state transitions, and adjacent behavior that must remain valid. Preserve existing regression cases, but do not present unrelated old traces as evidence for the new feature.

Build a small scenario matrix from relevant axes: ordinary tasks, ambiguous or missing evidence, conflicting evidence, boundary conditions, tool failure, and state preservation where applicable. Include realistic should-pass scenarios. Tie every axis to the feature contract or a concrete failure hypothesis; do not add arbitrary persona variation. Start with a reviewable batch sized to the available expert time and execution budget.

Use `generate-synthetic-data` from [the existing skills](ecosystem.md) for structured dimension/tuple generation where useful. Generate input scenarios separately from their wording. Reuse permitted fixtures, expert walkthroughs, and real source material before fabricating domain facts. Keep scenario origin and source family. Ask for realism clarification only where it changes the case. Until reviewed, synthetic inputs and expected answers remain proposals.

## Capture actual development runs

Reuse the feature's CLI, UI, API, or existing harness. Instrument its existing execution boundary or export its telemetry; do not add a second runtime just for tracing. Preserve each attempt separately with the input, original result or error, available tool interactions and retrieved evidence, relevant state before/after, and implementation/configuration identity. Read [trace review](trace-review.md) for a minimal portable format.

Synthetic **inputs** can produce real **execution traces**. Record both facts separately. A hand-written example output, mocked tool, or simulated environment is useful provisional evidence only within that boundary. Do not describe it as a full product execution. An incomplete feature can still be exercised up to its actual boundary; identify the missing stages. If it cannot run, author contract checks and scenarios, keep execution unrun, and name the smallest missing entrypoint.

Keep errors, retries, timeouts, and partial outputs. Do not substitute an agent's corrected answer for the failed result. Record unavailable context as unavailable, not as an invented trace. Capture observable events and concise audit summaries, not private chain-of-thought. Use authorized local data and budget; paid or externally mutating runs require their existing authorization.

## Review before scaling

Make a few actual traces inspectable before producing a large batch. Prefer the product's existing viewer. Use `build-review-interface` for domain-specific rendering, such as graph nodes, edge direction, probabilities, and supporting sources. The bundled [local review tool](trace-review.md) is a dependency-free starting point for JSONL traces and structured feedback.

Read the input, output, and evidence together. Check tool arguments/results and state changes when the criterion requires them. Do not force every observation into a whole-output verdict: an expert may identify one incorrect edge while the rest remains unassessed. Capture scope, exact concern, optional correction, uncertainty, and proposed yes/no questions. Empty feedback is unreviewed, not PASS.

Use `error-discovery` to develop failure categories from notes. `/expert-mode` can capture judgments during the working session; `/distill-me` can recover them afterward. Merge duplicate captures by source trace, output version, and assertion. Preserve disagreements and later amendments. Reviewer UI labels are not automatically expert-endorsed golden rows.

## Promote evidence and close the loop

Apply [from findings to cases](from-findings.md): resolve provenance and current judgments, identify sufficient replay context, and retain incomplete observations outside scored denominators. Each promoted case should point back to its actual trace and review record. Group all variants and repeated attempts from one scenario into the same source family when splitting.

Choose code checks for explicit invariants and observed objective failures. Use binary judge criteria for supported interpretive boundaries, then calibrate against expert labels from both classes. Keep scenario coverage, product success, and judge agreement as separate claims. Early targeted batches do not estimate production failure prevalence.

Run the feature again after a change, producing a new trace linked to the same scenario; compare the intended improvement and adjacent regressions. Cross-Examine the evaluator's intent and shortcuts when the score will drive decisions. Preserve discovered reward-hacking flaws in its ledger. Stop the batch when the agreed budget is reached; report uncovered dimensions rather than generating arbitrary volume.

When relevant production data arrives, review it with the same existing trace-analysis skills. Use it to discover missed scenarios, compare distributions, and add source-separated cases. Preserve the synthetic/development origin of earlier cases and do not relabel them as production observations.
