# Calibrate a judge without model calls

Use `.agents/skills/calibrate-judge/SKILL.md` on this project. All supplied data is synthetic. No human gold dataset, live provider, model budget or production-release policy is supplied.

Recover the source task contract and define what evidence a judge may see. Run the [offline mechanics](../judge_calibration/README.md), or adapt a small comparison using the local helpers. Keep original runner/spec/rubric/cases unchanged. Save artifacts under a fresh `eval-runs` directory.

Inspect whether baseline and selected fixture policies reproduce native outcomes. Check raw response/normalized verdict consistency and explain false passes, false rejections, coverage and undefined kappa/intervals. Verify typed yes/no polarity and that concentration confidence does not become P(failure). Keep errors visible. For ordered labels, use only a declared category order and weighting.

Demonstrate that final prediction/configuration membership is frozen before comparison and that consumed final evidence cannot be used for further fitting in the same campaign. Explain the difference between these inspected input/state guards and security containment or genuine unseen data.

Return the fixture judge handoff, actual calls, source identities, metrics and limits. Keep human calibration/live readiness unverified. Identify the real gold, owner acceptance policy, supported client/model identity and run budget needed before a future live calibration. Do not request secrets or make provider calls to complete this exercise.
