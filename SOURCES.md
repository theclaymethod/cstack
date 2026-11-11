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

## Bootstrap

Bootstrap is original C Stack orchestration for interviewing about intent, reviewing proposed scenario expectations, and delegating evaluator authoring in the target project's format. It reuses Create Eval, Run Eval, and optional Cross-Examine rather than bundling another runner or tracing backend.

The [research review](skills/bootstrap/references/research.md) records the bookmarked leads, primary sources, inspected revisions where available, and access limits behind its synthetic scenario methods. External tools and skills are referenced rather than copied or required. Expectation approvals and human labels on concrete outcomes remain separate authorities.

## Hill Climb

Hill Climb is original C Stack orchestration for bounded candidate search, actual target execution, regression-aware comparisons, confirmation, and resumable evidence. It reuses the project's execution/grading path rather than bundling a generic optimizer or second evaluator.

The [research note](research/hill-climb.md) records inspected DSPy, Ax, GEPA, and Halo source revisions. The installed skill's [optimizer reference](skills/hill-climb/references/optimizers.md) retains the source links and integration boundaries. These projects inform methods and optional integrations; their code is not copied into the skill and their advertised results are not C Stack performance claims. The deterministic support-agent fixture and native campaign runner under `fixtures/playground/` are original test-project code. Disposable workspaces receive current skill copies rather than maintaining a second canonical pack.

## Adversarial Cases

Adversarial Cases is original shared C Stack guidance for constructing controlled challenges and fault-injection cases. Bootstrap keeps expectation approval and Cross-Examine keeps independent adjudication. The skill's activation/outcome distinction and controls draw on this project's reproduced schema and lifecycle cases, not a claim that a generic fault name proves execution.

Additional primary-source research is recorded in [synthetic-generation follow-ups](research/synthetic-generation-followups.md) and [failure-injection follow-ups](research/failure-injection-followups.md). Their implementation pilots are explicitly deferred; no Hypothesis, solver, proxy, or chaos framework is bundled or required by the skill.

## Project-local generation, failure methods and DSPy

The method references and `fixtures/playground/methods` are original C Stack work based on the synthetic-generation and failure-injection follow-up research. Executable demonstrations and optional DSPy development dependencies stay in the fixture; new skill additions are references only. DSPy 3.5.0 was checked from official PyPI and its installed source. Compatibility uses Example, Prediction, Module, Evaluate and a GEPA feedback metric without provider calls or optimization. [The methods report](evals/methods/REPORT.md) records evidence and scope.

LangChain's [eval-engineering](https://github.com/langchain-ai/langchain-skills/tree/main/config/skills/eval-engineering) is referenced for grounded task/environment/verifier engineering with useful production traces. Its SKILL.md was read directly from upstream; it is not vendored or automatically installed. Harbor is the preferred format for new executable agent tasks, with existing and owner-selected formats supported. The [format reference](skills/create-eval/references/formats.md) points to upstream task documentation and requires checking the installed version. No Harbor runtime or container execution was added or claimed by this format preference.

## Calibrate Judge

The reference-only Calibrate Judge skill and project-local offline controls are original work informed by [judge-calibration research](research/judge-calibration.md). References cover typed Jev-style decisions and traditional LLM judges without bundling model clients. Playground labels are native code-derived synthetic outcomes; its judge processes are deterministic response-shape fixtures. No provider model call or human-gold calibration was performed. [The development report](evals/calibrate-judge/REPORT.md) records baseline/selection mechanics, kappa/error/probability diagnostics, independent use, confirmed review repairs and limits.

## Ablation and Bitter Lesson

The reference-only skills and project-local deterministic simplification controls are original C Stack work informed by [primary-source research](research/ablation-and-bitter-lesson.md). Delta debugging and hierarchical reduction inform deletion search; statistical guidance informs quality-preservation claims. Sutton's essay motivates revisiting inherited complexity, while provider guidance supplies model-specific hypotheses. No upstream algorithm implementation is copied or required. The fixture explicitly programs model differences and prompt interactions; it validates mechanics without provider calls or production prompt-quality claims. [The report](evals/simplification/REPORT.md) records actual evidence and limits.

The [skill-pack ablation](evals/skill-ablation/REPORT.md) preserves original instructions, literal deletion units, matched host-agent executions and native evidence. This is a local exposed-fixture comparison; no general performance or runtime-cost reduction is claimed. The [Ablation/Bitter Lesson audit](evals/simplification/CROSS_EXAMINE_LEDGER.md) records the independently reviewed accounting correction applied before that comparison.

The [current-model prompt simplification](evals/bitter-lesson/REPORT.md) preserves baseline commit `3b2c7d2`, original entrypoints, candidate hashes and fresh playground executions. It changes instruction wording while retaining all supporting resources and task/evaluator contracts. This comparison uses one inherited host model; it makes no model-upgrade or production-efficiency claim.

## Review-to-calibration capture

The shared [capture guide](skills/expert-mode/references/calibration-capture.md), review hooks and [playground exercise](fixtures/playground/exercises/13-review-calibration-capture.md) are original C Stack work prompted by the owner's request to offer retention of useful review judgments. They reuse Expert Mode records and Calibrate Judge authority/exposure boundaries. Project-local example serializers and synthetic review sources are archived as development evidence, not packaged with the skills. The [report](evals/review-capture/REPORT.md) records the iterative source revision and validation limits; no actual user-session labels were retained.
