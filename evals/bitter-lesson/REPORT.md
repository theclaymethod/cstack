# Current-model skill simplification

2026-11-10. Rewrote all eleven skill entrypoints around required outcomes and task constraints, giving the current model discretion over routine implementation. Selected guidance preserves the observed playground behavior with substantially less entrypoint text.

| Measure | Baseline 0.9.1 | Selected 0.9.2 | Reduction |
| --- | ---: | ---: | ---: |
| Whitespace-separated words | 8,722 | 4,429 | 4,293 / 49.2% |
| UTF-8 bytes | 67,031 | 37,757 | 29,274 / 43.7% |

The baseline is [`3b2c7d2`](https://github.com/theclaymethod/cstack/commit/3b2c7d25fff3c410b937f00bb0bcd2e6c393c2c8). This is a wording/structure rewrite, distinct from the preceding literal-deletion [ablation](../skill-ablation/REPORT.md). Frontmatter and all supporting references, scripts and assets are byte-identical. The new reference-only skills still contain no executable runtime. [Original entrypoints](original-entrypoints/), [candidate identities](candidate-manifest.json), [exact diff](candidate.diff), [selection](selection.json).

## What changed and stayed fixed

Replaced repeated implementation sequences with concise completion contracts and conditional reference pointers. Kept authority and evidence constraints: original reviewed versions, scoped expert statements, append-only amendments, exact approved input/state fidelity, legitimate alternatives, class/error/coverage semantics, protected evaluator/data, original-relative quality, complete predictions, budgets/reservations and exact final configuration. Cross-Examine still requires a fresh independent intent reviewer for formal acceptance. The prior durable-ledger lesson remains behind Ablation's mandatory quality reference.

Historical reasons for individual instructions are unknown where no source establishes them. The experiment tests whether this combined rewrite works on the current model; it does not prove each removed passage was an older-model workaround or establish the necessity of every retained clause.

## Model and experiment boundary

The user explicitly chose the **current model only**. Fresh agents inherited the same host model configuration without overrides; an exact hosted snapshot was unavailable. Only same-model full/simplified instruction comparisons were run. Older/newer hosted-model cells, upgrade effects and model-by-prompt interactions remain unrun. Programmed old/new fixture backends exercise workflow mechanics and are not hosted-model capability evidence.

One combined candidate was built and hash-frozen before confirmation. No restoration or confirmation-driven edit was needed. Native evaluator, cases, rubric, spec, support product and all skill resources stayed fixed. The burden objective is entrypoint size with zero observed regression on the declared checks. [Contract](CONTRACT.md), [frozen bundle](confirmation-freeze.json), [task packets](tasks/).

## Fresh skill-use evidence

Three fresh contexts per variant performed the same controlled tasks, covering every skill. The coordinator reviewed source/output evidence against the fixed [28-check rubric](quality-checks.json), while [native/source verification](verify_evidence.py) revalidated actual execution and installed guidance. Neither static instruction markers nor passing scripted machinery alone was counted as skill effectiveness.

| Matched exercise | Full guidance | Rewritten guidance |
| --- | ---: | ---: |
| Capture, stop and repeated retrospective merge | 8/8 | 8/8 |
| Approved scenario handoff, authoring and controls | 8/8 | 8/8 |
| Native execution, judge mechanics and optimization | 12/12 | 12/12 |

Capture retained the unrelated seed, original/regenerated versions, unproven narrative-to-native association, uncertainty and amendments; repeat merge added no duplicates or capture reactivation. A baseline source-role helper mistake was explicitly amended without erasing history or changing labels. It remains disclosed in that run.

Authoring preserved exact typed inputs/states for current approved revisions, kept urgency/proposed contrasts unapproved, accepted alternative IDs/metadata, and rejected claimed creation without a ticket. Operations actually ran the native campaign, rejected a higher-scoring regressive candidate, and retained judge errors, undefined uncertainty, probability limits, combined deletion effects and exposed confirmation. Formal proxy-audit acceptance remained unreviewed where independent roles were unavailable.

Two further fresh contexts received a less prescriptive owner request: build review-ready evals from new approved cases, reject false success while preserving alternatives, simplify only the authorized fixture backend, and assess limited stored judge observations. Both passed all **eight confirmation checks**, including exact nested-state fidelity, frozen execution, missing-model limits, 3/4 decided coverage and undefined kappa. [Confirmation rubric](confirmation-checks.json), [review](confirmation-review.json), [raw runs](evidence/).

Each valid confirmation measured full and selected new-fixture prompts at 8/8 development and 4/4 frozen confirmation, with no lost passes. Their selected prompt variants differ by a legitimate duplicate-reminder alternative; neither inferred old-production parity from those finite results.

## Excluded run and accounting

An initial shortened-guidance confirmation context opened global Create Eval/Run Eval copies resolving to the full 0.9.1 checkout. That context could not be made unexposed by later reading the correct files. It was frozen with **zero native attempts** and no candidate verdict, preserved under [excluded/confirm-short](excluded/confirm-short/), then replaced by a fresh context with explicit installed-copy paths. The candidate and owner task were unchanged. Actual read hashes and the replacement's source checks are retained.

Eight valid contexts and one excluded context were used. Valid full-guidance exercises consumed **352 native cases**; rewritten guidance consumed **356**. Each variant separately used **102 deterministic judge response processes**. These are accounting across mixed positive/negative/error controls, not pooled product scores or evidence of execution-efficiency gains. The coordinator both proposed and semantically graded the rewrite; this is not a blinded independent human study. [Semantic review](semantic-review.json), [verification receipts](verification/).

## Checks, replay and limits

Both packages passed all **eleven control groups**. Each native suite ran **56 tests: 55 passed and one optional DSPy SDK check skipped**. All eleven rewritten skills pass the skill validator. [Baseline controls](controls/baseline-controls/summary.json), [candidate controls](controls/candidate-controls/summary.json), [skill validation](skill-validation.json). No grader or runtime behavior changed to obtain these results.

To repeat skill use, materialize a fresh playground from the matching baseline/current checkout and give a fresh agent the relevant task packet. Per-run project-local scripts, cases, source hashes and exact commands are archived beside the evidence; use new output directories. `verify_evidence.py --workspace <workspace> --source <matching-checkout> --evidence <exercise> --out <receipt>` revalidates native receipts and installed source; semantic review is separate. The build script records the rewrite and its original experiment directory layout.

All cases, expectations and sample backends are synthetic and readable. Confirmation is a workflow role, not an unseen-data guarantee. The comparison supports this combined rewrite on observed tasks only: no population non-inferiority, universal preservation, individual-removal causality, global minimum, human-gold calibration, hosted-model upgrade or production reliability claim. No paid/provider-client calls, new dependencies, production changes or publication occurred.

Always-loaded discovery text is unchanged; supporting references remain available and may be loaded as needed. Entry text reduction does not establish the same reduction in total consumed context. Token usage, cost and model latency savings were not measured.
