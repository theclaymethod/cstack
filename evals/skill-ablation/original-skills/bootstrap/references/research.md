# Synthetic scenarios for a project-specific `/bootstrap`

Research date: 2026-11-10. This review informed Bootstrap's workflow; the external generators and tools below were not installed or evaluated. The research pass read project source and public saved bookmarks without editing personal-site, syncing bookmarks, using credentials, making model-provider calls, or mutating cloud resources.

## Decision

Make `/bootstrap` produce a small, reviewable scenario-generation plan grounded in the current project's contracts and evidence. Generate structured worlds and truth with code; use models for language, hypotheses, and semantic review. Turn accepted scenarios into real harness runs and human-labelable traces. Keep synthetic discovery coverage, verifier validation, and production performance estimation separate.

The user's starting reference is [What Is Eval-Driven Development?](https://www.langchain.com/blog/what-is-eval-driven-development). This review investigates the synthetic-scenario methods needed to support that intent-first workflow.

The strongest bookmark-derived precedent is LangChain's eval-engineering workflow: inspect repository and traces, maintain reusable project World Knowledge, specify a task, build it, run the real harness, inspect evidence, and reconcile what the run proved. Its current implementation is more relevant than a generic dataset generator. The reusable knowledge must contain project facts and methods; each task's focal state and exact expected answer remain task-local. [LangChain skill, inspected lines 7–29, 73–102, 210–229](https://github.com/langchain-ai/langchain-skills/blob/fc2010384ddb4f0ccc5317e25c82c246f7bc6bf7/config/skills/eval-engineering/SKILL.md).

The project World Knowledge layer is an adapter to whichever evidence the project actually has: source/tests, documented contracts, replayable records, supplied traces, or expert observations. It must record availability and limitations, then derive relevant scenarios. It must not require a fixed trace store, collection procedure, production logging integration, or copied exemplar corpus. A trace supplies observed behavior; independent project facts establish truth.

## What was actually searched

The requested [bookmarks page](https://claytonkim.com/bookmarks) failed in the web tool. A sandboxed curl also failed DNS resolution. A subsequently approved read-only network request successfully accessed the site's public review API; no login or token was used. Local source confirmed GET `/api/v1/x-matter/review` is public-read and that the filter parameter is **`query`**, not `q`. An initial `q=eval` request was unfiltered; its result was excluded from topical evidence. The endpoint's own `mode: stubbed` describes reuse of materialized stored route state: `liveCredentialsUsed: false` and an explanation that no live X, model, or search provider calls occur. This does not mean the returned bookmarks were synthetic.

At the unfiltered observation, the API reported 3,642 review items, including 3,638 bookmarks. These are the currently exposed materialized records, not proof of a complete historical bookmark corpus. The searches below used `/api/v1/x-matter/review?query=<term>&limit=100`; synthetic was fully paginated with offset 100. Counts can change after this observation.

| Search | Total reported | Items retrieved |
| --- | ---: | ---: |
| synthetic | 131 | 131, two pages |
| eval | 886 | first 100 |
| hamel | 28 | 28 |
| shankar | 13 | 13 |
| metamorphic | 0 | 0 |
| counterfactual | 8 | 8 |
| benchmark | 473 | first 100 |
| test generation | 153 | first 100 |

Reproduce with, for example, [public saved search: synthetic](https://claytonkim.com/api/v1/x-matter/review?query=synthetic&limit=100). The exact phrase-matching semantics were not independently validated; these are API query counts. Search bodies can be bounded or incomplete, enriched summaries are not independent verification, and zero results do not prove the concept was never bookmarked. Relevant originals were followed to their owners' documentation/source. Research did not exhaustively review all 886 eval or 473 benchmark matches.

The local fallback investigated before API access was `/Users/clayton/dev/personal-site/apps/portfolio/design/docs/twitter-bookmarks-2026-10-15.json`, captured 2026-10-15, with 8,554 source rows scanned, 1,206 bookmarks selected, 1,204 design entries. Its curated design subset is not an authoritative full library. The old `~/.ft-bookmarks/bookmarks.db` identified by local code does not exist on this host. No local index was rebuilt. The two downloaded synthetic-search page hashes were `db2d83081610d4e4d164ba5111fd1b4d737ec7aa834793cc3812bcc3988d30fe` and `e675ec77fa36aeac8273c208f29ee1fb08e15e2dba6a698605d661765df51e37`; raw API responses remain temporary research inputs, not deliverables.

### Bookmark-to-primary-source trail

| Saved bookmark ID(s) | Saved source / lead | Primary source followed and relevance |
| --- | --- | --- |
| 2102542556013932990; 2116094008917127541 | [evals-skills](https://github.com/ai-evals-course/evals-skills) | Pinned `generate-synthetic-data`, `error-discovery`, and `validate-evaluator`: tuples, review, human calibration. Index revision `80d5f7b0127c7572ed9e9339937adbfd7240ffeb`. |
| 2099929381850468675 | [Hamel + Shreya's FAQ](https://hamel.dev/blog/posts/evals-faq/) | Authors' own guidance on synthetic data, failure discovery, labels, and practical caveats. |
| 2092267628869882164; 2092266609838604368 | [Vivek's practical guide announcement](https://twitter.com/Vtrivedy10/status/2092266609838604368) | Short link resolved to LangChain's eval-engineering skill. Followed [How We Build Agent Environments & Tasks](https://www.langchain.com/blog/building-agent-environments-and-tasks) and current source/references. |
| 2084693873599594570; 2084747098210099641 | [Human feedback workflow](https://x.com/Vtrivedy10/status/2084693873599594570/photo/1); [research questions](https://x.com/Vtrivedy10/status/2084747098210099641) | Saved posts advocate iterative repo/traces→spec→environment work; current upstream source supersedes older three-file layouts. Posts are practitioner claims, not controlled evidence. |
| 2068796834588574185 | [Counterfactual task-family comment](https://twitter.com/kalomaze/status/2068775691550937599) | Useful hypothesis: change meaningful conditions while holding the underlying task fixed. Followed Prime Intellect's first-party design rather than treating the comment as proof. |
| 2068774187704213735 | [Prime Intellect General Agent](https://www.primeintellect.ai/blog/general-agent) | Stateful synthetic tasks with data, tools, instructions, gold paths, and semantic verifiers. |
| 2100990591215783946 | [Bespoke Nimble](https://github.com/bespokelabsai/nimble) | Contrastive curation, evidence ablation, code-derived labels, family splits and integrity manifests. |
| 2039383474583609604; 2064381486573433027 | [text-albumentations](https://github.com/avbiswas/text-albumentations); [counterfactual task update](https://x.com/neural_avb/status/2064381486573433027/photo/1) | Corpus augmentation engine; assessed as a conditional prose tool, not a task/environment generator. |
| 2050009867830673679; 2070058945914573049; 2070142050956128529 | [Autodata author's announcement](https://x.com/jaseweston/status/2050009867830673679/photo/1) and saved reposts | Followed [Autodata paper v3](https://arxiv.org/abs/2606.25996v3); agentic data-creation/meta-optimization research. |
| 2052629564472631685 | [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | Task/trial/outcome distinctions; final state is distinct from the agent's claim. |
| 2102422882341322779; 2102434040695669189 | [Hamel + Shreya advanced eval guide](https://www.lennysnewsletter.com/p/advanced-evals-how-to-find-and-fix) | Duplicate saved URL demonstrates why bookmark count cannot stand in for unique evidence. Not relied on for claims beyond accessible primary material above. |

NIST combinatorial testing and the CheckList paper were additional targeted primary-source searches prompted by the requested coverage and metamorphic questions. They were **not established as saved bookmarks**.

## Methods worth encoding

### 1. Failure-driven dimensions and constrained coverage

The pinned evals-skills generator starts with anticipated failure regions, defines dimensions, reviews draft tuples with the domain owner, then separates tuple generation from natural-language generation. It filters unrealistic or repetitive outputs and runs retained inputs through the full pipeline. Its three-dimension, 20-tuple, and roughly 100-trace figures are workflow heuristics, not sample-size guarantees. [generate-synthetic-data, lines 14–100](https://github.com/ai-evals-course/evals-skills/blob/80d5f7b0127c7572ed9e9339937adbfd7240ffeb/skills/generate-synthetic-data/SKILL.md).

**Proposed adaptation:** derive every dimension from a cited project behavior, trace, incident, requirement, or explicit expert hypothesis. Examples of possible axes are request type, initial state, permissions, evidence freshness, ambiguity, dependency behavior, and required recovery. These are prompts for discovery, not a universal taxonomy to impose on every project. Record why each chosen axis should reveal a failure. Keep known facts distinct from hypotheses.

For a modest valid product space, enumerate combinations and filter constraints deterministically. For larger spaces, a covering-array planner can cover every feasible pair, with selected three-way or higher interactions for named risks. NIST defines t-way coverage and covering arrays and warns that pairwise testing misses faults requiring more interacting conditions. Its software findings do not prove an LLM suite is complete. [NIST ACTS FAQ](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/faqs).

**Proposed reporting:** list legal values, forbidden combinations, feasible t-tuples covered/missing, mandatory high-risk combinations, accepted scenario families, and budget exclusions. Recompute coverage after realism filtering; rejecting rows can remove the only coverage of an interaction. A randomly varied list is not demonstrated coverage. Pairwise selection is a budget choice, not a guarantee against longer state/history interactions. Keep scenarios for explicit temporal sequences when the order itself matters.

### 2. Structured truth first; prose second

LangChain's synthetic-data reference fixes seeded IDs, relationships, permissions, dates, state, and constraints in code, validates the world, then asks a model to express supplied facts. It requires fact IDs, request/output/generator/hash provenance, separate review, duplicate checks, and whole-world validation after merge. [Synthetic data reference](https://github.com/langchain-ai/langchain-skills/blob/fc2010384ddb4f0ccc5317e25c82c246f7bc6bf7/config/skills/eval-engineering/references/synthetic-data.md).

**Proposed adaptation:** generate the smallest relationship-complete fixture that makes the intended decision possible, plus meaningful distractors. A distractor should test a named confusion, such as a stale record or similarly named entity. More unrelated documents do not automatically create a better task. Check referential integrity, chronology, discoverability, access, and task preconditions before prose generation. Have the generator cite supplied fact IDs for every factual claim. Preserve a rejection reason rather than silently repairing meaning-changing mistakes.

An impossible request can be a valid scenario when the tested behavior is clarification, refusal, or escalation. Distinguish that deliberately infeasible user goal from an accidentally unsolvable environment. A successful reference path must include legitimate refusal/clarification outcomes where appropriate.

### 3. Contrast pairs, invariance, and metamorphic expectations

Nimble's curation recipe changes one relevant fact while preserving question and policy; the correct decision flips. It checks facts in separate calls, removes evidence sentences to look for answer leakage, derives labels in code, and preserves requests/responses. Missing evidence is treated as unknown during checks, rather than mislabeled false. [Nimble README, contrastive curation section](https://github.com/bespokelabsai/nimble#contrastive-data-curation).

The CheckList paper distinguishes minimum functionality, invariance under meaning-preserving perturbation, and directional expectations under known meaningful change. The framework tests relations between predictions without requiring a reference answer for every perturbed input. [Ribeiro et al., ACL 2020](https://aclanthology.org/2020.acl-main.442/).

**Proposed project-specific operators:**

- Rename irrelevant IDs or people consistently: the required outcome should stay equivalent.
- Reorder independent documents or tool-result rows: the decision should remain invariant unless order is part of the contract.
- Change exactly one authorization, freshness, threshold, or ownership fact: the expected decision should change in the documented direction.
- Add a plausible stale/conflicting source: the agent should resolve conflict using the project's evidence precedence.
- Remove a necessary fact: the agent should use the project's uncertainty/clarification behavior.
- Add tool failure and recovery state: verify the intended retry/idempotency behavior and forbidden duplicate effects.

These are recommendations, not facts about the target project. Each transformation needs explicit applicability conditions and a checked expected relation. A paraphrase may change meaning; an ID rename may alter routing; deleting evidence may change feasibility. Automatically validate the operator's preconditions and request expert review where semantics remain uncertain.

### 4. Realism, feasibility, and adversarial validation

Hamel and Shreya recommend synthetic cases for sparse traffic and rare known failures, followed by actual full-system traces and expert review. They explicitly say synthetic data cannot estimate production failure frequency and can miss specialized-domain details. [FAQ, synthetic-data and reliability sections](https://hamel.dev/blog/posts/evals-faq/#q-what-is-the-best-approach-for-generating-synthetic-data).

Prime Intellect's General Agent task structure combines state, domain tools, instructions, gold solution, and verification. It accepts generated tasks after empirical solver checks against difficulty bands. That is a useful feasibility pattern; the calibration models and synthetic tool worlds do not establish fidelity to a particular production app. [General Agent, Task Anatomy and synthesis description](https://www.primeintellect.ai/blog/general-agent).

**Proposed adaptation:** require a normal-discovery reference solution, state reset/isolation, and independent expected evidence. Test the verifier with a valid alternative, plausible wrong result, shortcut/reward hack, collateral side effect, and corrupt/missing evidence. A strong model failing is a diagnostic signal, not proof that the task is good. A weak model passing may expose leakage. Audit suspicious passes and classify environment/harness/verifier errors separately from capability failures. [LangChain verifier-design](https://github.com/langchain-ai/langchain-skills/blob/fc2010384ddb4f0ccc5317e25c82c246f7bc6bf7/config/skills/eval-engineering/references/verifier-design.md), [calibration](https://github.com/langchain-ai/langchain-skills/blob/fc2010384ddb4f0ccc5317e25c82c246f7bc6bf7/config/skills/eval-engineering/references/calibration.md).

### 5. Provenance, deduplication, and family splits

Nimble's dataset guide documents synthetic/model-checked labels rather than human labels, keeps contrast siblings and source families together, and uses an integrity manifest plus offline checks for hashes and overlapping sources, contexts, and IDs. [Dataset guide](https://github.com/bespokelabsai/nimble/blob/main/docs/DATASET.md).

**Proposed minimal record:** stable scenario ID; family/parent ID; real/synthetic/mutated origin; evidence pointers with revisions; dimension tuple; generator/prompt/seed versions; structured truth hash; emitted prose hash; constraints checked; relation/operator; reviewer identity and status; rejection reason; split; rubric/verifier version; and run/trace pointers. Avoid inventing a large framework before the first usable family exists.

Exact normalized hashes catch literal duplicates; token overlap or embeddings can surface near-duplicates for review. Semantic similarity is a retrieval signal, not proof that cases are equivalent. Keep all variants derived from one underlying issue, trace, document source, template, or world seed in one family. Split by family before tuning. When several lineage relations overlap, assign connected groups to a split. A shuffled row split leaks counterfactual siblings and template cues. Search for cross-split source and normalized-content overlap and record unresolved matches.

Maintain separate declared purposes: discovery/tuning examples, a frozen held-out family set, and a representative real-traffic sample for prevalence estimates. A challenge suite intentionally overrepresents difficult cases; its overall pass rate is a suite result, not a production reliability claim.

## Tools: adapt versus install

| Source/tool | Useful part | Proposed choice for `/bootstrap` |
| --- | --- | --- |
| ai-evals-course generate-synthetic-data | Failure dimensions, reviewed tuples, language as a separate step | Adapt the method; avoid installing the entire bundle or copying its arbitrary numeric targets. |
| LangChain eval-engineering | Project World Knowledge, task-local spec, deterministic synthetic facts, independent verifier fixtures | Primary design precedent. Adapt project-specific discovery and artifact boundaries; do not force Harbor or its full approval choreography into a different repo. |
| NIST ACTS | [Constraint-aware generation](https://csrc.nist.gov/CSRC/media/Projects/automated-combinatorial-testing-for-software/documents/acts_user_guide_3.2.pdf), including mixed-strength support in documented algorithms | Optional when dimension size justifies it. For small spaces, a tiny seeded enumerator and coverage checker is easier to inspect. Compatibility/setup was not tested. |
| CheckList | Templates, perturbations, expectation functions | Adapt semantics. The [upstream repository](https://github.com/marcotcr/checklist) includes model/notebook dependencies; install only if those facilities earn their cost. No compatibility run was performed. |
| Bespoke Nimble | Contrastive construction, evidence ablation, lineage, manifests, offline replay | Adapt curation ideas and audit source. Its local scorer adds Python 3.12, model weights, and Apple Silicon or NVIDIA setup; generation requires provider access. Do not assume synthetic labels are expert truth or that a local decision model is calibrated on this project's traces. |
| text-albumentations | [Structured text-corpus augmentations](https://github.com/avbiswas/text-albumentations) with explicit task selection and model adapters | Conditional for document-derived prose. [Package metadata](https://github.com/avbiswas/text-albumentations/blob/main/pyproject.toml) requires Python ≥3.10 plus OpenAI, Outlines, and Pydantic dependencies. It is aimed at instruction-tuning/distillation data, not complete task/environment correctness. Do not use automatic task selection as the scenario plan. |
| Autodata | Agentic data creation and feedback/meta-optimization | Research direction. The [paper](https://arxiv.org/abs/2606.25996v3) reports improvements in its studied settings, not plug-and-play correctness or value for this project. No implementation installed or reproduced. |
| General Agent / verifiers ecosystem | Stateful task/gold-path/semantic-verifier structure, empirical difficulty checks | Reference for larger environment generation. Keep the current project's harness and observed interfaces authoritative. |

The skill-index shortlist is discovery evidence only; an upstream file existing is not evidence that installation improves outcomes. No benchmarks, speedups, or tool-quality comparisons were measured in this research.

## Human labels and judge calibration

Use two explicit human decisions: whether the scenario/world is realistic and whether a particular resulting agent run succeeds under a clear criterion. A realistic input can produce a failing trace; a plausible output is not evidence that the scenario was feasible. Keep input approval separate from run labels.

The upstream error-discovery skill builds a review surface around the actual data shape, preserves human notes separately from agent suggestions, and mixes cluster representatives with random samples for discovery. It emphasizes that diversity sampling discovers modes rather than estimating their prevalence. [error-discovery](https://github.com/ai-evals-course/evals-skills/blob/80d5f7b0127c7572ed9e9339937adbfd7240ffeb/skills/error-discovery/SKILL.md).

**Proposed workflow:** give the expert the task, relevant input/context, trace, independent outcome evidence, and one criterion at a time. Offer pass/fail/uncertain with a short reason and evidence pointer. Hide the judge prediction during initial independent labels to reduce anchoring. Save every label with rubric version; adjudicate uncertain cases. Start with a small pilot and revise ambiguous criteria before bulk labeling. If multiple experts are necessary, label an overlapping subset independently, compare disagreements, and agree on rubric examples. An agent suggestion remains a suggestion until accepted; an unreviewed synthetic label must never be presented as a human verdict.

The pinned validate-evaluator skill separates prompt exemplars, iterative dev data, and final test data, then reports pass sensitivity and fail specificity against domain labels. It recommends balanced labels and exact judge-version pinning. [validate-evaluator](https://github.com/ai-evals-course/evals-skills/blob/80d5f7b0127c7572ed9e9339937adbfd7240ffeb/skills/validate-evaluator/SKILL.md).

**Qualification from inspection, not an upstream claim:** use family-disjoint splits in addition to class stratification. Its ~100 labels, split fractions, and 90%/80% thresholds are examples, not universal acceptance requirements. Report the confusion counts and uncertainty, including failure types with too few examples to assess. Choose acceptable false-pass/false-fail risks with the owner. Treat malformed judge output or missing independent evidence as an invalid judgment, not a failing agent.

The optional Rogan–Gladen correction is mathematically meaningful only when measured sensitivity/specificity transfer to the target distribution and their sum is sufficiently above one. Its example bootstrap holds production `p_obs` fixed, so it excludes production-sampling uncertainty; correlated variants also need family-aware resampling. The document's claim that improving TPR narrows intervals more than TNR does not follow universally from a denominator containing their sum. Do not copy these statistical claims into `/bootstrap` as settled guarantees. In a bootstrap skill, calibrated per-criterion labels and transparent limitations are enough; production prevalence estimation should be a separately justified analysis.

## Concrete `/bootstrap` deliverable contract

This is a proposed contract for the parent implementation, not an instruction to install any external skill:

1. Inspect the current project and record a bounded evidence map: entry points, agent/tool contracts, storage/state, focused tests, supplied traces, observed failures, access limits, and unresolved hypotheses.
2. Write a compact generation plan naming failure-relevant dimensions, legal tuples, interaction targets, scenario families, mutation operators, provenance, and reviewer needs. Separate evidence-backed facts from hypotheses.
3. Draft a few concrete tuples and one complete representative family with state, instruction, observable success, valid alternatives, prohibited effects, reference feasibility path, and review status. Scale only after checking the plan's realism.
4. Provide rerunnable deterministic builders/checkers when generated fixtures or combinatorial coverage justify code. Check complete structured truth before adding prose; retain fact-level provenance.
5. Emit a trace/review handoff that the existing cstack create/run/cross-examine workflow can consume, rather than inventing a parallel runner or claiming generation is evaluation.
6. Report what was observed, generated, reviewed by a human, executed through the real harness, and independently validated as separate states. If labels or access are missing, leave those states explicit and give the next concrete action.

The best initial success criterion is one evidence-grounded, feasible, inspectable scenario family and its runnable proof path, with a generation plan for coverage gaps. A large number of generated prompts is not itself the intended outcome.
