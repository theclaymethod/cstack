---
name: bootstrap
description: Bootstrap evaluators through an intent interview, parallel scenario generation, human approval of proposed expectations, and eval authoring in the target project's format. Use for /bootstrap or when turning a new behavior into its first reviewed evals.
---

# Bootstrap

Turn the user's intent into a small, reviewed set of scenarios and runnable evaluators. The user decides what behavior is acceptable; agents propose scenarios and implement checks. Work on one behavior at a time, including adjacent behavior that must keep working.

Bootstrap owns the interview, scenario review, and orchestration. [Create Eval](../create-eval/SKILL.md) owns evaluator authoring and calibration; [Run Eval](../run-eval/SKILL.md) owns execution; [Cross-Examine](../cross-examine/SKILL.md) owns optional adversarial review.

For deeper generated coverage, use the shared [synthetic methods](../adversarial-cases/references/synthetic-methods.md). Prefer Harbor for new executable agent evals while preserving existing/owner-selected formats; see [format selection](../create-eval/references/formats.md). Generators and adapters belong in the project, not this skill.

## Inspect the project and recover intent

Read project instructions, existing eval examples, schemas, runner commands, and any relevant intent already supplied in this session. Map where cases, checks, fixtures, and private labels belong. Reuse the project's runner and format; use [the local package contract](../run-eval/references/package.md) only if it has none.

Evidence gathering is project specific. Identify available requirements, user examples, authorized traces, fixtures, or domain documents and the project's way to access them. Use those sources when relevant; a trace integration, production corpus, or running implementation is not an entry requirement. Mark unavailable sources and continue with explicit requirements and synthetic proposals.

Interview in short rounds about missing decisions that change a scenario or its expected result:

- When should the behavior happen, and what observable outcome would satisfy the user?
- What plausible response or action would be unacceptable? Which alternatives are acceptable?
- What nearby behavior must remain intact? Where should the system ask, abstain, or defer?

Keep questions about desired behavior; infer technical choices from the project. Propose a reviewable first batch and execution scope using the user's time and budget. Leave coverage priorities, review volume, trust thresholds, and optional hardening with the user.

Record a short intent contract with the trigger, success, failures, alternatives, preserved behavior, and unresolved boundaries. Confirm missing product judgments before treating them as settled.

## Generate scenarios with subagents

Read [scenario generation](references/scenarios.md) before dispatch. Separate the scenario's facts and conditions from its wording. Pick dimensions because they affect the intent contract or test a plausible failure, then exclude impossible combinations.

For adversarial boundaries and injected-failure slices, have the scenario author use [Adversarial Cases](../adversarial-cases/SKILL.md). Supply the original intent revision, relevant raw facts, supported alternatives, candidate/operator access, and a bounded case/execution budget. Ask for proposed expectations, clean/alternative controls, and explicit execution or non-activation status. Contract-only proposals are valid before implementation. The builder returns construction evidence; Bootstrap still owns user approval, revisions, and the approved authoring handoff.

Dispatch independent scenario authors with distinct coverage assignments: ordinary successes and valid alternatives; boundaries and minimal contrast pairs; plausible failures and adjacent regressions. Combine assignments to fit available capacity. Give each author the same intent revision, relevant project facts, allowed fixtures, and a bounded output budget. Keep initial proposals independent and writes in separate scratch files. Authors return scenarios and proposed expectations, not approved labels or evaluator code.

Merge proposals by behavioral distinction, remove duplicates, and check feasibility against actual tools, data, and permissions. Preserve source and construction families across paraphrases and related variants. Show coverage gaps and unsupported assumptions. If delegation is unavailable, generate a bounded local draft and disclose that independent scenario coverage was not performed.

## Ask for intent labels

Read [labeling and checkpoints](references/labeling.md). Present short cards with stable IDs, the situation, proposed expected behavior, and a brief reason. Ask the user to approve, disapprove/correct, or defer. Support compact batch replies while preserving per-card decisions. Show product behavior, not evaluator implementation.

Distinguish two judgments:

- **Expectation approval:** what should happen in a scenario. This defines a requirement or reference behavior.
- **Outcome label:** whether a specific output, action, or resulting state is acceptable for a specified criterion. This can support calibration.

Approving an expectation does not label an unseen output. Generated guesses and agent consensus remain proposals until explicitly reviewed. Silence or an unanswered card is pending. A disapproval rejects the proposed expectation; it does not automatically approve its inverse. Resolve corrections and uncertainty on the affected cards, continuing work on approved independent cards.

Preserve reviewed text, revisions, decisions, and scope. Material edits require renewed review; an explicit user correction supplies that review for its exact replacement. On resume, resolve current decisions and amendments before dispatching authors. Keep unreviewed, deferred, and stale cards outside the approved authoring handoff.

## Have subagents author the evals

Freeze a handoff containing the intent revision, approved scenario revisions and their decision sources, supported alternatives, unresolved exclusions, and the project's format/runner mapping. Separate requirement references from private outcome labels.

Dispatch evaluator authors for independent approved groups using [Create Eval](../create-eval/SKILL.md). Give each a separate scratch output and ownership scope; the coordinator integrates into the canonical package. Authors receive the contract and permitted task evidence. Reserve calibration examples and their human outcome labels from authors; give the validator only the judge's permitted payload.

When implementation or execution setup is missing, produce contract-based cases and checks where possible, record the execution gap, and leave product execution unrun. Keep mocked outputs and environments explicit. Synthetic scenario origin and actual product execution are separate facts.

Before integration, validate the authored cases against the project's required schema and compare their inputs, context, initial state, families, and checks with the current approved scenarios. Matching IDs and expected labels alone does not establish fidelity. Preserve meaning across format conversion; return material changes for review and record any accepted alternative representation. Keep approved source records outside the author's changes so an edited case cannot redefine its own acceptance condition.

Integrate only against the current approved revisions. Keep pending cases in an incomplete queue with reasons. Once approved independent cases are authored, report partial completion without silently dropping the rest.

## Validate and hand off

Run legitimate outcomes, relevant failures, and boundary controls through the actual grading path, including supported alternatives. Contract-derived controls can establish specific check behavior; they do not become human calibration labels. For semantic judges, obtain explicit human outcome labels and follow [judge calibration](../create-eval/references/judges.md). Missing labels leave semantic calibration incomplete, while deterministic checks and other authorized work continue.

Keep construction families in one partition. Reserve independent examples from evaluator construction where feasible; a new paraphrase of a development case is not independent evidence. If no fresh set exists, report development checks only. Use [Run Eval](../run-eval/SKILL.md) for authorized execution, blind payloads, frozen verdicts, and comparison. Report unknowns and errors separately from behavior failures; distinguish evaluator agreement from product performance. Preserve earlier results when revising a check.

Offer a bounded [Cross-Examine](../cross-examine/SKILL.md) pass after the package and validation evidence are reviewable. Run it if already requested; otherwise leave it optional. Basic grader controls still belong in Bootstrap regardless of that choice.

Finish with the package path and run command, covered intent, approved and pending counts, observed validation results, and remaining execution/calibration gaps. Trust thresholds and release decisions remain the project's. Authoring evals does not authorize product changes, paid campaigns, uploads, or publication.
