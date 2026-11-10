# Synthetic generation: five later pilots

Research checked 2026-11-10. These are implementation proposals, not measured improvements. No generators were installed, provider calls made, or experiments run. This extends Bootstrap's existing [research](../skills/bootstrap/references/research.md) and [scenario guidance](../skills/bootstrap/references/scenarios.md); it does not repeat their tuple planning, contrast-pair, covering-array, or structured-world recommendations.

Start with a stateful replay pilot and validity-preserving reduction, then test whether mutation-guided selection adds distinct mechanisms. Keep solver integration conditional. Add generated judge challenges only when a semantic judge exists. The five pilots below can be evaluated independently; none requires a new evaluation framework.

## Playground boundary and evidence

The inspected playground accepts one request and ticket state per invocation. Its rubric distinguishes authorization, account selection, duplicate scope, and preservation. The existing evaluator accepts native JSONL through `run --cases`, executes candidate subprocesses, and grades observable effects. It does **not** provide a conversation scheduler or transactional service simulator. A stateful pilot would coordinate successive existing invocations externally, never claim unsupported tool semantics. See the local [rubric](../fixtures/playground/evals/rubric.md), [evaluator](../fixtures/playground/evaluate.py), and [playground instructions](../fixtures/playground/AGENTS.md).

Source checkout HEAD was `227c7746ded27a9fb3b4167d1927c78982ac5c9b`, but the playground was untracked: that commit does **not** pin these files. Inspected SHA-256 values: evaluator `c0af96b600a53ae0089f8b9f7c8ddfd20cbc6588dfe1aca625361fe532c85ee9`; rubric `cb133b50752a48098d463a562d7553ec5a5b29bfef1825b4e393e7de33d66dd8`. Preserve these identities when reproducing the proposed experiments.

## 1. Generate reachable action sequences

**Primary-source basis.** Hypothesis state machines generate sequences of primitive actions. `Bundle` carries values between rules; `precondition` restricts applicable actions; `invariant` checks after steps. Its documentation demonstrates comparison with a separate in-memory model and reduction to a short failing program. This establishes an available mechanism, not its effectiveness for agents. [Hypothesis, stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html).

**Proposed contract.** Input: an initial fixture, bounded action vocabulary, applicability predicates, contract-derived state model, candidate, and step/run limits. Output: ordered requests, initial and per-step state hashes, candidate observations, invariant failures, and a replayable witness. Expectations come from the contract model; candidate-returned state is observed and checked, never silently accepted as truth. Stop or mark subsequent steps invalid after malformed output or a broken prerequisite.

For the playground, start with only supported actions: authorized VPN ticket creation, repeated creation requests, guidance requests, and account changes. Reuse returned state after checking its shape and prior-state preservation. Avoid simulated ticket closure or outages until an explicitly separate environment adapter supplies those transitions.

**Falsifiable pilot.** Generate a creation followed by the same authorized request. The improved candidate should create once and subsequently add nothing; the intentionally flawed baseline should expose duplicate creation. Also exercise an unrelated account's open ticket before creation for the selected account, discriminating the supplied overly broad duplicate-check candidate. Record whether failures were found, replayed, and reduced, including unsuccessful search budgets. Existing static cases already exercise some of these boundaries: only a newly demonstrated sequence mechanism counts as added coverage.

**Effort/dependencies.** Medium: a small coordinator and independently reviewed transition model; optional Hypothesis dependency. Start with explicit short sequences if that answers the question. Do not adopt the framework when all meaningful behavior is one-shot, resets are unreliable, or the model merely copies candidate logic.

## 2. Ask for boundary witnesses with constraints

**Primary-source basis.** Z3Py supports asserted constraints, `check`, model extraction, and scoped `push`/`pop`. Results include `sat`, `unsat`, and `unknown`; a model satisfies the encoded formulas. These APIs were checked against the current official guide, not locally executed. [Z3Py introduction, solver and model sections](https://microsoft.github.io/z3guide/programming/Z3%20Python/Introduction/).

**Proposed contract.** Input: finite domains, named validity constraints, a target predicate, and a maximum number of witnesses. Output: a concrete structured assignment plus constraint revision, solver identity/settings, and result status; alternatively an explicit unsatisfiable or unresolved result. Render natural language only after independent fixture validation. Distinguish valid worlds with impossible user goals from internally contradictory worlds.

The useful query is specific: “Find a state where an open ticket exists, but none belongs to the selected account and issue.” It creates a mechanistic witness against an overly broad duplicate check. Another query fixes everything except whether the explicit account is available. Do not add a global validity constraint forbidding unavailable explicit accounts: the contract deliberately handles those requests by clarifying.

**Falsifiable pilot.** Enumerate a tiny bounded playground domain independently, then compare its feasible assignments and expected branches with solver-produced witnesses. Every retained assignment must pass the native loader and independent semantic checks. Run both supplied candidate variants through the existing evaluator on those cases. A disagreement with enumeration rejects the encoding; no new boundary relative to the simpler enumerator rejects the additional dependency.

**Effort/dependencies.** Medium: Z3 bindings, bounded encoding, and independent validation. Low-value for this tiny playground; more plausible later for intertwined permissions, chronology, quantities, or relational records. Never infer realism from satisfiability. Keep `unknown` unresolved, and abandon solver adoption when encoding maintenance exceeds the value of the witnesses.

## 3. Reduce failures while preserving their relation

**Primary-source basis.** Delta debugging repeatedly tests reduced inputs. The original `ddmin` result is 1-minimal under its test predicate: removing any single remaining element does not retain the failure. It need not be the globally smallest case, and unresolved tests matter. [Zeller and Hildebrandt, 2002, §§III–IV](https://www.st.cs.uni-saarland.de/publications/files/zeller-tse-2002.pdf).

**Proposed contract.** Input: a failing case or metamorphic family, validity predicate, named behavioral relation, target failure signature, removable units, and replay budget. Output: original and reduced artifacts, lineage, every attempted deletion's validity/outcome, unchanged mechanism, and termination reason. Return `reduced-within-budget` unless the required minimality checks actually finish.

Reduce structured units first: whole irrelevant tickets, unused account identities, independent context records, then wording. Preserve referenced identities and operator applicability. For a rename relation, rename every relevant reference consistently. For ticket-order permutations, compare contract observations after accounting for the transformed input: outputs must preserve **their own** input order. Raw output equality across permutations would mislabel valid behavior. Newly allocated ticket IDs may differ while both remain valid; compare contract-defined effects rather than reference-candidate strings.

**Falsifiable pilot.** Begin with an authorized request plus several unrelated tickets that makes the overly broad duplicate-check candidate fail. Remove records until one sufficient unrelated ticket remains, while the improved candidate still passes. For a duplicate-specific witness, retain the matching ticket and selected-account relationship. Reject reductions that replace the original defect with a crash, unauthorized request, unavailable account, or accidental impossibility. Have a reviewer confirm that the smaller witness explains the same mechanism.

**Effort/dependencies.** Small to medium: structured reducer and calls to the existing runner; no new framework required. Hypothesis can shrink generated draws, but its failure blobs have no compatibility guarantee across versions, so store concrete JSON and operation sequences as durable artifacts. [Hypothesis strategies](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html), [reproduction API](https://hypothesis.readthedocs.io/en/latest/reference/api.html#hypothesis.reproduce_failure). Do not automatically shrink nondeterministic provider runs until replay stability and a bounded repeated-trial policy exist.

## 4. Select cases by the defects they detect

**Primary-source basis.** Mutation testing inserts small code faults and checks whether tests detect them. PIT documents the distinction from execution coverage. A study of Java projects found a correlation between mutant and real-fault detection beyond coverage, with limitations; that result does not establish transfer to LLM agents. [PIT mechanism](https://pitest.org/), [Just et al., FSE 2014](https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html).

**Proposed contract.** Input: reviewed requirement-linked fault operators, generated cases, a conforming control, and explicit runner limits. Output: a case-by-mutant detection matrix, survivors, invalid/equivalent/untested statuses, and a small selected corpus. Example faults: ignore authorization denial, choose the first of several accounts, treat any ticket as a duplicate, overwrite an original record, or reuse an existing ID. Do not mutate the evaluator and candidate together.

Deduplicate exact fixture content first. Use identical detection vectors to nominate redundant cases, then inspect their requirements, conditions, and lineage before dropping anything: equal vectors against a finite mutant set do not prove semantic equivalence. Preserve a compact realistic witness and one boundary sibling when both aid review. Keep all reduced, transformed, and search-descended cases in their source family; overlapping ancestry forms one connected partition. A new random seed alone does not create independent evidence when template and construction remain shared.

**Falsifiable pilot.** Freeze a small fault catalog, compare static seeds with generated additions under equal execution budgets, and list exactly which previously surviving defects the additions detect while the conforming control passes. Reserve some fault mechanisms from generator feedback and report them separately. If gains disappear on those mechanisms, report overfitting. Track accepted distinct mechanisms and executions per witness, not just generated-row totals.

**Effort/dependencies.** Medium: a few explicit Python candidate variants and matrix bookkeeping; PIT itself targets the JVM and is unnecessary here. Do not adopt bulk mutation machinery when operators are unrealistic, equivalent mutants dominate, or survivors reveal oracle defects rather than missing cases. Mutation score remains a diagnostic for the declared fault catalog, never a production reliability estimate.

## 5. Generate verified judge challenges before trusting synthetic labels

**Primary-source basis.** JudgeBench constructs response pairs from verified correct and incorrect outputs, evaluates both response orders, and discusses checker/format disagreements and generator-selection bias. Its benchmark is evidence about the studied judges, not this project's judge. [JudgeBench v2, §§3–4](https://arxiv.org/html/2410.12784v2). Separate experiments found self-preference in the evaluated model and summarization settings; using a second model is not an independence guarantee. [Panickssery et al., 2024, §§2–4](https://arxiv.org/html/2404.13076v1).

**Proposed contract.** Input: an independently established outcome, legitimate alternative outputs, single-defect output transformations, rubric revision, and a frozen judge. Output: evidence-backed pass/fail/uncertain controls, provenance, judge verdicts, and per-criterion disagreements. Keep execution errors and invalid judgments separate from behavior failures. Label status must distinguish code-derived fixture truth, proposed model labels, reviewed labels, and actual human judgments.

**Falsifiable pilot.** In the playground, make valid outputs with different unique ticket IDs, then single-defect outputs with a wrong account, missing preserved ticket, duplicate ID, or extra ticket. Check these against the existing deterministic grader. They test grader/control construction; the playground has no semantic judge. A later semantic-judge pilot can use matched explanations around those outcomes, swap pair order, hide generator identity, and measure false passes, false failures, invalid decisions, and order disagreement on reserved families. Do not tune on those families and keep calling them held out.

**Effort/dependencies.** Small for deterministic controls; medium plus separately authorized provider access and expert review for semantic judging. Avoid semantic judges for properties that code already checks. Reject automatic gold labeling when independent evidence is absent, alternate valid solutions are penalized, or disagreement requires domain interpretation. Human review of synthetic outcomes establishes calibration only for the reviewed contract and sampled families; it cannot establish traffic prevalence or unseen-domain accuracy.

## What to retain from each pilot

Use the existing case format plus a sidecar for generator/model/solver versions, input and output hashes, parent/operator ancestry, constraint checks, reduction attempts, selection reasons, and trace pointers. Save rejected proposals and reasons, including unresolved realism. Hashes establish identity, not correctness; an embedding match or detection vector is a review aid, not a deduplication verdict. Pin tool versions at implementation time; Hypothesis documentation inspected here displayed 6.170.15, and no compatibility installation was tested.

The adoption decision should name one concrete gain: a reachable sequence defect, a previously missing valid boundary, a smaller faithful witness, an additional detectable fault, or a measured judge limitation. A larger synthetic corpus alone does not satisfy any of these tests.
