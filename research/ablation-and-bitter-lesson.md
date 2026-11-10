# Ablation and the Bitter Lesson for eval-driven development

Researched 2026-11-10 against original papers and first-party documentation. This note proposes two skills; neither has been built. No model calls, ablation experiments, production changes, or performance measurements were made. Recommendations are design inferences, not demonstrated results for cstack.

## Proposed distinction

| Skill | Question | Default intervention |
| --- | --- | --- |
| `/ablation` | What can this system lose while preserving its required performance? | Remove authorized instructions, examples, context, tools, or workflow steps, keeping the model fixed. |
| `/bitter-lesson` | Does a model upgrade make inherited production complexity unnecessary? | Compare model/prompt combinations, then use ablation to test legacy steering and scaffolding. |

Both specialize the existing `/hill-climb` experiment discipline. Ablation minimizes a declared burden subject to quality constraints. Bitter Lesson adds a model-migration hypothesis and production handoff. Neither should promise that shorter prompts are better, that every upgrade permits deletion, or that the smallest candidate found is globally minimal.

## What removal research contributes

**Search structured deletions rather than trimming prose arbitrarily.** Zeller and Hildebrandt's delta-debugging algorithm tests subsets and complements against an oracle. Its guarantee is 1-minimality: no single remaining atom can be removed while preserving the oracle result. That is weaker than finding the smallest subset, and a stochastic agent-quality estimate does not inherit a deterministic guarantee. The paper also preserves unresolved outcomes. [Original ddmin paper](https://www.st.cs.uni-saarland.de/publications/files/zeller-tse-2002.pdf).

Hierarchical Delta Debugging uses tree structure to remove larger parts before smaller parts. Its authors show that later removals can enable deletions at earlier levels; ordinary HDD therefore does not guarantee 1-tree-minimality. Their HDD+ and HDD* variants revisit remaining material. Design inference: start with prompt sections, whole demonstrations, context sources, or workflow stages, then refine and revisit survivors within budget. Declare dependencies so removing a section does not silently break the remaining artifact. [Original HDD paper](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/hdd.pdf).

**A removal effect is conditional on the configuration.** Sufficient Input Subsets studies retained input portions that preserve a particular model decision, including multiple disjoint sufficient subsets. ERASER distinguishes sufficiency from comprehensiveness measured through removal. Neither establishes reusable agent performance. [Sufficient Input Subsets](https://proceedings.mlr.press/v89/carter19a/carter19a.pdf), [ERASER](https://aclanthology.org/2020.acl-main.408.pdf).

Design inference: distinguish a diagnostic leave-one-out table from a deployable reduced system. If A and B contain duplicate guidance, deleting either alone may work while deleting both fails. Conversely, conflicting groups may need to be removed together. These are logical examples, not model measurements. Evaluate the combined candidate; selected group tests can investigate interactions. Report “removable in this tested configuration,” not “universally unnecessary.”

**Deletion, compression and replacement are separate treatments.** LLMLingua compresses prompts through budget control and iterative token selection. Its reported results do not identify which named rule or agent step is dispensable. The removal-based explanation literature likewise distinguishes the intervention, measured behavior, and summary. Design inference: make literal deletion the default ablation operation. Rewriting, summarizing, substituting retrieved content, disabling execution, or changing models should be separately identified treatments. [LLMLingua](https://aclanthology.org/2023.emnlp-main.825/), [Explaining by Removing](https://www.jmlr.org/papers/v22/20-1316.html).

## What preserving performance must mean

“No statistically significant regression” does not establish equivalence; a small experiment may simply be unable to detect a meaningful loss. Equivalence testing uses practical bounds declared before results. [Lakens, Equivalence Tests](https://journals.sagepub.com/doi/full/10.1177/1948550617697177).

Design inference: the usual ablation objective is non-inferiority, since an improvement need not be rejected for exceeding a symmetric equivalence interval. For higher-is-better quality, define `d = candidate − original baseline` and an owner-approved maximum loss `δ`. A valid one-sided lower confidence bound above `−δ` can support the stated non-inferiority claim under its assumptions. This is one possible confirmation method, not a universal recipe or default margin. Deterministic fixture checks can instead establish exact behavior on their finite cases, without implying population-level preservation.

Keep these boundaries in the proposed skill:

- Declare the quality measure, important slices, hard requirements, acceptable loss, evidence plan, and resource objective before selection. Tokens, tool count, latency, cost, and maintenance burden are different objectives. Fewer input tokens alone do not prove lower total cost or latency.
- Compare selected candidates with the **original baseline** throughout. Repeatedly accepting a small loss against the most recent reduced candidate can accumulate beyond the original allowance.
- Execute each changed candidate. Regrading old outputs cannot measure a deleted workflow stage. Preserve per-case outcomes, actual state changes, schema validity, unknowns, and infrastructure errors.
- Pair comparable cases and reset conditions, repeat stochastic trials as appropriate, and account for dependent task families and repeated trials. A shared random seed does not guarantee comparable trajectories across different workflows.
- Reserve confirmation evidence where possible. Repeatedly consulted validation is adaptive search evidence. Freeze the final combined candidate before confirmation; leave weak evidence inconclusive.

The original NLP significance-testing guide explains why test choice depends on metric and assumptions. Cawley and Talbot show how optimizing a noisy selection criterion biases evaluation. Anthropic's engineering guide distinguishes repeated trials, final environment outcomes, and reliability versus at-least-one-success metrics. These support the discipline above, without selecting a universal sample size or test for cstack. [Dror et al.](https://aclanthology.org/P18-1128.pdf), [Cawley and Talbot](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf), [Agent evaluation guide](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

The defensible deliverable is the least burdensome confirmed candidate found within budget, its exact deletion diff, original baseline, tested combinations, measured savings, regressions, and uncertainty. A no-removal result is valid. Only claim a completed local-minimality check when it actually ran under a defined oracle.

## What the Bitter Lesson does and does not support

Sutton's 2019 essay argues that general methods that exploit increasing computation, especially search and learning, have repeatedly overtaken approaches built around human domain knowledge. It is not a study of prompts, retrieval, modern model upgrades, or production reliability. Applying it here is a motivation to revisit inherited complexity, not a theorem that newer models need fewer instructions. The author's canonical site was unavailable during research; this university-hosted facsimile reproduces the essay and original URL/date. [The Bitter Lesson](https://www.cs.utexas.edu/~eunsol/courses/data/bitter_lesson.pdf).

There is more direct provider guidance for particular simplifications. OpenAI recommends simple, direct reasoning-model prompts, starting without examples, while retaining clear constraints and success criteria. Anthropic's migration guidance recommends dialing back some inherited thoroughness and aggressive tool-use instructions that newer models may overapply. These are model-specific recommendations, not proof that any production prompt should be shortened. [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices), [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Less orchestration can also require **more relevant context**. Jiang et al. demonstrate a simpler SWE-bench approach that places environment content directly into long-context models. It is a benchmark result, not a production guarantee. Anthropic similarly recommends minimal sufficient context, explicitly explaining that minimal does not necessarily mean short and warning against assuming shared knowledge. [Putting It All into Context](https://arxiv.org/html/2505.08120v1), [Effective context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents).

A supplementary 2026 preprint tests subsets of five agent components and reports task- and model-scale-dependent interactions; some combinations harmful at smaller scale help at larger scale. It is under review and limited to its tested systems. It reinforces the need to test interactions, not a monotonic “larger means less scaffolding” claim. [More Is Not Always Better](https://arxiv.org/abs/2605.05716).

## Proposed model-migration experiment

Design inference: test which legacy workarounds still earn their cost while preserving the production task. Inventory the actual assembled input, including system instructions, demonstrations, tool descriptions, retrieval, history, and orchestration. Identify why each candidate component exists. Task rules, necessary private/current facts, and explicit output requirements remain part of the contract; a stronger model cannot be assumed to know them.

Use this comparison where feasible:

| | Existing prompt/context design | Simplified design |
| --- | --- | --- |
| Current model | Production baseline | Simplification effect on current model |
| Candidate model | Model change with existing design | Proposed model-plus-design candidate |

Three cells establish the production baseline, the upgrade with design held fixed, and the simplification effect on the candidate model. The fourth supports estimating whether simplification behaves differently across models. This follows full-factorial design: change both factors explicitly rather than attributing a joint change to one. [NIST factorial-design guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm).

Keep case membership, evaluator, resets, and comparable settings fixed; record supported differences in model interfaces, reasoning settings, tools and budgets. If the old backend is unavailable, mark missing comparisons and use recoverable evidence honestly. A successful new-model simplification does not then establish that the upgrade caused the component to become unnecessary.

Candidate removals can include repeated reminders, compensatory reasoning recipes, legacy few-shot demonstrations, mandatory planning/reflection steps, and duplicate context. Where useful, compare against a clean task-contract prompt as another candidate. Each is a hypothesis; do not erase requirements because they resemble verbose instructions. Confirm the combined candidate against the production baseline as well as the candidate model with the existing design. Measure critical behavior and total execution costs, since a smarter model may spend more even with a shorter prompt.

For an authorized production rollout, deliver a versioned model/prompt/context/configuration bundle with the recoverable original. Shadow evaluation can copy inputs while discarding candidate responses, but agent side effects need suppression or isolation; it cannot measure user reactions to those responses. Canary exposure compares a bounded candidate population with a control and predefined rollback conditions. Google SRE describes these techniques; their application to a prompt migration is a design recommendation. Preparing the bundle does not itself deploy it. [Google SRE canary guidance](https://sre.google/workbook/canarying-releases/).

Re-evaluate when model versions, prompts, context assembly, tools, task distribution, or evaluator change. When exact model pinning is unavailable, retain the identifier and date plus that reproducibility limit. Offline evals, human review, monitoring and production experiments provide different evidence; preserve their distinctions. [OpenAI prompt-version guidance](https://developers.openai.com/api/docs/guides/prompt-engineering), [Anthropic evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

## Fit within cstack — proposed, not implemented

`/ablation` should reuse `/hill-climb` for frozen contracts, budgeting, candidate identity, execution, exposure and confirmation. Its distinct work is defining removal units, tracking conditional effects, testing combinations, minimizing burden, and preventing accumulated loss against the original baseline.

`/bitter-lesson` should use `/ablation` within a model-migration comparison and provide the production release handoff. `/run-eval` executes frozen candidates. `/bootstrap` or `/create-eval` fills missing behavior coverage; `/calibrate-judge` owns judge alignment. Keep the approved evaluator fixed while optimizing the product; `/cross-examine` investigates suspected scoring gaps separately.

Match the existing reference-only approach: skill instructions and method references, with runners, model adapters, datasets and experiments in the consuming project. Reuse an established project format; prefer Harbor for new executable agent tasks without forcing a migration.

The playground fixture can later validate bookkeeping, deletion combinations, dependency validity, baseline-relative quality gates, budget/error handling, and a simulated model-by-prompt comparison. Deterministic stand-ins would establish those mechanics only. Actual prompt quality, smarter-model behavior and production reliability require real model executions and representative evidence; none were tested in this research.
