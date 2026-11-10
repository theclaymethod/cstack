# Judge calibration from trusted labeled outcomes

Research checked 2026-11-10. Primary papers, official library documentation and vendor documentation. No user gold dataset was provided, no model was called or fitted, and no skill was built. Recommendations are design inferences from these sources, not measured performance in C Stack.

## Intended capability

Take recoverable inputs, original evaluated outputs, authoritative labels and their criterion scope, then produce a versioned judge that reproduces the project's grading standard on independently reserved examples. Deliver the judge configuration/program and evidence about its agreement, costly errors, abstentions, runtime and limits. A prompt or a high development score alone is insufficient.

Keep three jobs distinct:

- **Label agreement:** reproduce the reference outcome, with consequential errors visible.
- **Decision selection:** choose a threshold and any review/abstention policy for the project's costs.
- **Probability calibration:** test whether predicted probabilities match empirical event frequencies, and fit a supported mapping when justified.

A judge can produce good hard decisions without emitting probabilities. A probability calibrator can improve reliability without improving ranking or accuracy at a selected threshold. The official [threshold guide](https://scikit-learn.org/stable/modules/classification_threshold.html) and [probability-calibration guide](https://scikit-learn.org/stable/modules/calibration.html) distinguish these operations. Brier score and log loss are proper probabilistic scores but also reflect discrimination and uncertainty; neither alone isolates calibration quality.

## Two main backend routes

| Backend | What the skill could tune | What it must preserve |
| --- | --- | --- |
| Typed decision model | Question/instructions, option definitions, permitted context/examples, probability mapping and decision/review thresholds | Native labels/probabilities, actual capabilities and model identity. No invented textual explanation. |
| Generative LLM judge | Rubric/instructions, few-shot demonstrations, structured verdict format, supported inference settings and optional concise evidence summary | Original label meaning, permitted runtime evidence, parsing/error outcomes and costs. |
| Specialized evaluator or locally trainable classifier | Its supported template/criteria; optionally supervised weights or classifier head when capability and budget justify it | Training authority, separate calibration predictions, checkpoint identity and explicit deployment interface. |

A backend-neutral project adapter should expose input, frozen configuration, raw prediction, optional probabilities/rationale, normalized decision, execution status and measured usage. The source of truth remains the authoritative labels. It is unnecessary to impose one SDK or a hosted platform on all users.

### User clarification: Jev-style System One judges

The user identified [LangChain's post](https://x.com/LangChain/status/2101454284927959080) as the intended meaning of decision models. Direct X access returned 403; the primary [LangChain writeup](https://www.langchain.com/blog/jev-agent-evals-langsmith) and [authors' experiment repository](https://github.com/danielgshea/jev-as-a-judge) supply the underlying material. This resolves the category toward typed System One decisions such as Jev rather than only conventional classifiers.

The experiment freezes five weather-agent outputs and asks each judge to score them repeatedly. The repository reports one human reviewer and 100 repetitions per source case. Binary human agreement and continuous-score variance are separate measurements. Those 500 repeated decisions are not 500 independent labeled examples. The authors also disclose unset LLM sampling parameters and an unavailable hosted Jev version; do not infer a general provider ranking or causal architectural advantage.

Design implication: support typed question/instruction/option tuning and score-to-decision policies directly. Judge explanations remain optional by backend capability. Test gold agreement, same-input repeatability, probability reliability and operational cost separately. Keep source-case/family counts distinct from repeated calls and match candidate trials on the same frozen evidence. The article's use of “precision” for score variance should be normalized to repeatability/stability in a calibration report, distinct from classification precision.

### What typed decision models mean here

TypeSafe's official [System One description](https://docs.typesafe.ai/concepts/system-one) documents typed decisions and probabilities instead of generated reasoning. Its [Choice primitive](https://docs.typesafe.ai/primitives/choice.md) returns a selected category and option probabilities. [Noul](https://docs.typesafe.ai/primitives/noul) returns P(yes), with the question/criteria defining what yes means. These are concrete examples of a decision-model route, not a provider selection or performance endorsement.

The [confidence documentation](https://docs.typesafe.ai/confidence) is especially relevant: confidence summarizes distribution concentration and differs from the probability of the selected event. For a binary Choice, its example maps top probability 0.75 to confidence 0.5. Preserve native probabilities and their semantics; do not substitute a concentration statistic, an ordinal score or verbal certainty for P(failure). Vendor descriptions of trained calibration do not establish calibration against this project's gold. No private fine-tuning API is assumed.

## Gold quality and measurement unit

A row needs an immutable evaluated output/version, relevant task evidence, a stable criterion or aggregation rule, the original label and its authority, and construction/source lineage. Keep references that the real judge legitimately needs separate from human verdicts used as supervision. Gold rationales can help development feedback when authorized; they do not belong in blind final judge inputs.

If two humans label a subset independently, preserve their annotations and later adjudication. Human-human reliability provides context for ambiguous criteria, not a mathematical ceiling on judge-versus-adjudicator agreement. One label per item cannot measure inter-human agreement. [Cohen's original paper](https://journals.sagepub.com/doi/10.1177/001316446002000104) concerns agreement between independent categorization processes.

Do not silently amend gold to make the judge look better. Contradictory, missing or disputed labels need a visible adjudication/incomplete queue. Per-criterion labels do not automatically become whole-case gold. Human preference, source-supported correctness and process compliance can be different targets; [JudgeBench](https://arxiv.org/abs/2410.12784) demonstrates why preference agreement does not establish difficult factual/logical judging ability.

## Agreement report, including kappa

For paired nominal labels, use Cohen's kappa as a supplemental agreement statistic:

    p_o = observed agreement
    p_e = sum over classes of reference marginal × judge marginal
    kappa = (p_o - p_e) / (1 - p_e)

The official [API documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html) supports binary/multiclass categories and optional linear/quadratic weights. Use ordinary kappa for PASS/FAIL or unordered classes. Use weighted kappa only when the labels have meaningful order and the disagreement weights were chosen beforehand. Do not impose distance on arbitrary failure categories. Multiple human raters or missing human annotations may need another agreement design; do not mechanically apply a two-rater statistic.

Kappa is undefined on no paired cases or when expected agreement is one. For example, both parties labeling every item PASS does not create a meaningful chance-corrected statistic. Another illustrative case has 95 human passes and five human failures; an always-PASS judge has 95% raw agreement but kappa zero. Preserve counts, marginals and undefined reasons. Prevalence and marginal imbalance can change kappa substantially; avoid universal acceptance bands. [Feinstein and Cicchetti's original analysis](https://pubmed.ncbi.nlm.nih.gov/2348207/) addresses this limitation.

Kappa is symmetric and cannot express which error is costly. Existing C Stack guidance uses human **failure as the positive class**:

| Gold | Judge FAIL | Judge PASS |
| --- | --- | --- |
| FAIL | TP, caught failure | FN, false pass |
| PASS | FP, false rejection | TN, accepted pass |

Report full counts, prevalence, raw agreement, failure catch TP/(TP+FN), false passes among human failures FN/(TP+FN), and false rejection among human passes FP/(FP+TN). False outcomes among judge passes FN/(TN+FN) answer a different question and should have a distinct name. Zero denominators remain undefined. For multiclass data, retain the full confusion table and appropriate per-class summaries.

Keep UNKNOWN, refusal, malformed output, timeout and transport failures visible. Report attempted, valid-decided, abstained and errored counts by reference class. Coverage is valid-decided/attempted. Conditional agreement or kappa on the decided subset must be named as such and accompanied by all-case outcomes. Evaluate any human/LLM fallback as part of the combined system rather than assuming deferred cases get perfect answers. [Selective classification](https://jmlr.csail.mit.edu/papers/v11/el-yaniv10a.html) formalizes the risk-coverage distinction without supplying automatic guarantees for these judges.

Report uncertainty and its method. [Statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.stats.inter_rater.cohens_kappa.html) documents variance calculations for kappa. With related outputs, preserve paired labels and resample independent source/task families as clusters where that matches the sampling design. Row-weighted traffic and equal-weight task families are different estimands. Too few families, rare failures and undefined resamples limit inference. The original [clustered-bootstrap analysis](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.1467-9868.2007.00593.x) explains why dependence cannot be ignored. The skill should name assumptions rather than promise that any bootstrap interval is valid.

## Tuning protocol

1. Establish what counts as correct, label scope/authority, permitted references, intended population, costly mistakes, abstention/fallback policy and the owner's acceptance targets.
2. Audit source families and gold. Keep duplicate, same-source and transformed examples together. Use grouped development validation or cross-validation where appropriate, then reserve independent final evidence. [Official grouped-split guidance](https://scikit-learn.org/stable/modules/cross_validation.html).
3. Run the untuned judge and a simple class-frequency baseline where useful. Capture original verdicts/errors, configuration and costs before changing anything.
4. Inspect development disagreements. Tune rubric distinctions, instructions and examples; for typed models use native questions/options. Fit supported score mappings or thresholds on separate or out-of-fold predictions. Weight training is optional and requires an actual supported interface and justified budget.
5. Freeze the selected judge, model/version, input projection, rubric, examples, parser, calibrator, thresholds, repeats, cache/retry and fallback policy. Save blind predictions before a separate comparison accesses final labels.
6. Compare baseline and selected judge on the same final cases. Report kappa and uncertainty alongside class errors, coverage and costs. If policy/evidence is insufficient, report not yet calibrated rather than inventing a pass threshold.

Development feedback may reveal human outcomes to a proposer. That does not authorize leaking the current case's target label into the deployed judge. Final-test disagreement used to edit the judge becomes development exposure; renaming it cannot restore independence.

## Where DSPy/GEPA fits

DSPy GEPA is an optional way to optimize the mutable judge instructions against deterministic comparisons to authoritative development labels. Its [implementation](https://raw.githubusercontent.com/stanfordnlp/dspy/main/dspy/teleprompt/gepa/gepa.py) supports scalar scores and feedback. A generative reflection model can propose better questions for a typed target through a project-local adapter; the target does not need to generate rationales. Return observed/expected verdict, error direction and approved criterion feedback to the proposer, within the fitting data policy.

The [GEPA guide](https://raw.githubusercontent.com/stanfordnlp/dspy/main/docs/docs/getting-started/gepa-optimization.md) distinguishes reflective training updates, adaptive validation selection and final testing. Pin the installed API when implementing. Count inference, proposer calls, retries, repeats, calibration work and confirmation, not only optimizer metric calls. Dataset/metric compatibility alone is not empirical optimization.

A directly relevant primary example is [Dropbox's relevance-judge report](https://dropbox.tech/machine-learning/optimizing-dropbox-dash-relevance-judge-with-dspy): it optimizes against human 1–5 ratings, includes a malformed-JSON penalty and uses human-score gaps for feedback. Its particular loss and reported gains are task-specific, not recommended universal defaults.

## Robustness and model choice

Test label-preserving input formatting, supported answer styles, producer-identity hiding, terse correct versus persuasive wrong answers, repeated-run stability, and pairwise order swaps when pairwise judging applies. Preserve transformed-case ancestry and confirm label preservation rather than assuming every rewrite is irrelevant. [MT-Bench](https://arxiv.org/abs/2306.05685) studies position, verbosity and self-enhancement biases. [JudgeDeceiver](https://arxiv.org/abs/2403.17710) demonstrates attacks embedded in candidate responses; a typed result alone does not defeat them.

Specialized judges may be candidates, not authorities. [Prometheus 2](https://arxiv.org/abs/2405.01535) supports custom criteria with direct/pairwise assessment. [JudgeLM](https://arxiv.org/abs/2310.17631) trains against a teacher judge; teacher agreement does not establish human agreement. Evaluate the project's actual candidates on its labels instead of selecting a universal winner from unrelated benchmark scores.

## C Stack integration and next step

A proposed `/calibrate-judge` would own the gold-to-judge fitting and validation procedure. Create Eval supplies cases/criteria; Run Eval executes frozen predictions and comparisons; Hill Climb supplies an optional bounded search; Cross-Examine challenges shortcut judgments; synthetic/fault methods supply disclosed robustness controls. Reuse existing `skills/create-eval/references/judges.md` and the project-local DSPy handoff rather than introduce a competing gold/metric system or bundle model dependencies in a skill.

Preserve established data formats. Harbor remains the preference for new executable agent tasks; judge calibration often consumes labeled rows and an existing grader interface and does not inherently require containers. A skill can reference methods and produce project-local judge configuration, native adapter and calibration report. Model/provider selection, tuning budget, target rates, error costs and final evidence sufficiency remain owner decisions.

The current playground supports synthetic mechanics and adversarial checks. It has no newly provided human gold dataset or live judge in this research. A fixture can validate confusion/kappa arithmetic, degenerate cases, leakage guards and before/after fitting controls while remaining explicitly synthetic. True agreement with expert labels needs actual labeled data and actual judge executions. No new skill, judge, calibration claim or provider integration is delivered by this research note.
