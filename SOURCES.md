# Skill origins

These notes identify the source material used for C Stack. Source revisions describe the inspected inputs, not an automatic upstream synchronization mechanism. Some origin repositories are private and require their owner's access.

## Retired standalone repositories

C Stack is the maintained home for the following skills. Their former repositories were archived on 2026-11-06 after adding migration notices and linking their repository homepages here. Original documentation, branches, and Git history remain in the archives; visibility is unchanged.

| Archived repository | Maintained replacement | Preservation |
| --- | --- | --- |
| [theclaymethod/cross-examine](https://github.com/theclaymethod/cross-examine) | [Cross-Examine](skills/cross-examine/SKILL.md) and its [eval suite](evals/cross-examine/README.md) | All 359 unchanged source/eval files were verified against the standalone revision below. C Stack expands its lessons; packaging docs differ. The original local capture skills and expert-review suite also match their C Stack copies. |
| [theclaymethod/eval-creator-skill](https://github.com/theclaymethod/eval-creator-skill) | [Create Eval](skills/create-eval/SKILL.md) and [Run Eval](skills/run-eval/SKILL.md) | The general workflow is adapted here. Original `benchmarks-mono` adapters, scripts, templates, and methodology remain available in the private archive. They are not bundled into C Stack, and its portable workflow is not a drop-in replacement for those adapter commands. |

The standalone source revisions below remain the provenance anchors; later archive commits change only the README by prepending migration instructions. Neither repository had open issues or pull requests. Cross-Examine had only its main branch; Eval Creator's other branches had no commits ahead of main.

`f-explainer` remains active as a broader course/project repository. Reusing its Run Eval skill does not subsume its other material. Other proposed skills remain outside this pack until selected.

## Existing trace-analysis workflows

[AI Evals Course's Evals Skills](https://github.com/ai-evals-course/evals-skills/tree/80d5f7b0127c7572ed9e9339937adbfd7240ffeb), inspected at revision `80d5f7b0127c7572ed9e9339937adbfd7240ffeb`, is referenced for synthetic input generation, error discovery, custom review interfaces, deterministic checks, judge design and calibration, pipeline audits, and RAG evaluation. The upstream repository declares Apache-2.0. Its skills are not copied or bundled here.

The early-development reference connects those workflows to actual feature execution before relevant production traffic exists. The local reviewer is original C Stack code informed by the upstream local-file/browser review approach. It deliberately starts with a small snapshot and scoped observations rather than requiring a hosted tracing product, embeddings, clustering, database, or fixed batch size. Domain-specific review UIs remain the upstream interface skill's role.

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
