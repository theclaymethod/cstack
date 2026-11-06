# Skill origins

These notes identify the source material used for C Stack. Source revisions describe the inspected inputs, not an automatic upstream synchronization mechanism. Some origin repositories are private and require their owner's access.

## Create Eval

Adapted from [theclaymethod/eval-creator-skill](https://github.com/theclaymethod/eval-creator-skill/blob/de41e65d18187d039cd8fb9f38968d3120788406/SKILL.md), revision `de41e65d18187d039cd8fb9f38968d3120788406`. The original skill's declared name is `create-eval`; its frontmatter declares MIT.

The portable version retains error analysis, binary criteria, deterministic checks where possible, expert-label calibration, source-based splits, and an independent check of eval intent. It adapts the source's behavioral, programmatic, agentic, and cold-start branches into a compact workflow. Private benchmark infrastructure and provider configuration are replaced with the current project's harness or a local-file package. Intake asks for missing facts rather than repeating an interview already answered in the session. Trust thresholds remain project decisions. Cross-Examine owns the bounded adversarial-hardening workflow.

## Run Eval

Adapted from the [original Evals Bootcamp Run Eval skill](https://github.com/theclaymethod/f-explainer/blob/5f57ca1516518939cf833a814aaba3104ea035f1/evals-bootcamp/evals-bootcamp-tutor/.claude/skills/run-eval/SKILL.md) in `theclaymethod/f-explainer`, revision `5f57ca1516518939cf833a814aaba3104ea035f1`.

The later [Bootcamp V2 reference version](https://github.com/theclaymethod/f-explainer/blob/5f57ca1516518939cf833a814aaba3104ea035f1/evals-bootcamp-v2/reference/ferritin-tutor/.agents/skills/run-eval/SKILL.md) informed the explicit boundary between human labels and model judgment, frozen results, and exposure tracking. Both files declare the same skill name and serve different course harnesses.

The portable version retains host-model judgment, deterministic mechanics, blind payloads, verdict freezing, separate failure-catch and acceptable-clear rates, and distinct development/calibration/final-test/regression/frontier roles. It uses an existing trusted project runner or narrow scratch scripts, without course progress files, private clinical cases, a fixed number of questions, or a second model API key. JSON is the dependency-free fallback; existing project formats remain supported.

## Original C Stack skills

Expert Mode and Distill Me were created for expert feedback capture and retrospective extraction. Their working-mode and review-pass patterns were informed by Pstack's Poteto Mode, Automate Me, and Reflect by Lauren Tan. See the preserved [Pstack MIT license](licenses/pstack-MIT.txt).

Cross-Examine originated in [theclaymethod/cross-examine](https://github.com/theclaymethod/cross-examine). Its historical eval evidence remains frozen under its original provenance. C Stack also contains subsequent capture-eval lessons developed in this project.
