# Judge calibration

For a complete gold-to-judge fitting and confirmation workflow, use [Calibrate Judge](../../calibrate-judge/SKILL.md). It supports typed decision models and generative LLM judges with project-local adapters; this reference remains the short calibration guidance for eval authoring.

Code checks still need behavioral evidence: a predicate can be implemented correctly while measuring the wrong thing. Use known legitimate outcomes, known incorrect outcomes, and contract-relevant boundaries. Preserve any parser or environment errors separately from task failures.

For semantic judgments, name the expert label source and the question being calibrated. Select examples from both supported classes. Keep same-source and same-template families in one partition. Use development cases to refine questions and examples; calibrate on a separately reserved set whose labels are withheld from the judge until verdicts freeze. Do not copy gold rationales or label-bearing scenario names into the blind payload.

An approved reference answer is task content that may be necessary to judge correctness. A human PASS/FAIL verdict is a calibration target. Record which reference material the real judge is allowed to see, and keep those roles distinct.

Judge each applicable criterion independently. Write a short source-bound observation, a concise rationale, and then PASS, FAIL, or UNKNOWN. These are audit summaries, not private chain-of-thought. Missing evidence, scope ambiguity, and execution errors must remain visible. Do not let the length or confidence of the output substitute for the criterion.

Freeze verdicts before computing agreement. If labels or prior comparisons were already read in the judging context, report contamination. A protected store can enforce access; a scratch directory and an instruction cannot. A fresh reviewing context improves separation only when its actual inputs exclude the labels.

Use **failure present** as the positive class:

- TP: expert FAIL, judge FAIL.
- FN: expert FAIL, judge PASS.
- TN: expert PASS, judge PASS.
- FP: expert PASS, judge FAIL.

Report raw counts first, then failure catch rate `TP/(TP+FN)` and acceptable-clear rate `TN/(TN+FP)`. A zero denominator is undefined. Count UNKNOWN and execution errors separately by gold class, report the decided fraction, and avoid a success claim based only on easy decided examples. Use a predeclared abstention policy if a decision requires one.

Thresholds, minimum evidence volume, false-pass tolerance, and release consequences belong to the project owner. Missing policy is not a pass. Kappa or aggregate accuracy may provide supporting context but cannot replace the two class rates and coverage. A small development match is not production calibration.

When a reserved case is opened to fit a rubric, preserve the original result, mark that case exposed, and replenish a future held-out set when needed. Freeze a new revision after changes; a rerun on the same revealed cases is development evidence. Record judge model/host identity when available and use unknown when it is not.
