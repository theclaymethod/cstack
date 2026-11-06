---
name: create-eval
description: Create repeatable evaluations from expert findings, real model outputs, or an explicit task contract. Use when authoring eval cases, binary rubrics, deterministic graders, or judge calibration; preserve source authority, independent splits, and the capability being measured.
---

# Create Eval

Turn a concrete failure or capability into a repeatable decision. Start with the project's existing eval format and runner. A small local dataset and an inspectable grader are sufficient; a new service, database, container, or model-provider setup is conditional on the task.

## Establish what the eval decides

Recover the intended capability, downstream decision, source of expert judgments, allowed alternatives, and observable success from the request and project. Ask only for information that changes the task or pass condition and cannot be found locally. Continue independent work while a material ambiguity is unresolved; keep the affected case provisional.

State the unit being judged: a specific assertion, output, or environment outcome. Two errors in one output are not necessarily one example. A negative judgment about one assertion does not establish that every neighboring assertion is wrong. Distinguish factual correctness, preferences, process requirements, and missing evidence.

Choose the appropriate route:

- A directly checkable property gets a deterministic predicate, including valid alternative representations where the contract permits them.
- Open-ended quality gets separate binary questions with explicit applicability, passing answers, and expert-supported boundaries.
- A stateful agent task gets a resettable environment and checks on the actual state change, including preservation requirements. Stored text alone does not exercise the agent's execution.
- With no observed outputs, build a provisional development set from the contract and obtain a real run when authorized. Explicit invariants can support initial checks; mark hypothetical failure claims as unobserved.

## Recover evidence before inventing cases

Read the relevant outputs, input context, expert statements, and existing cases. For Expert Mode or Distill Me data, resolve linked amendments, corrections, rubric versions, and retractions first. Preserve the original reviewed output rather than substituting a repaired result.

Read [from findings to cases](references/from-findings.md) when importing captured records or an export bundle. The export's privacy review and eval-meaning review are separate from expert label authority and judge calibration. A redacted projection needs enough context to preserve the actual failure.

Group demonstrated errors into a compact failure taxonomy with source examples. Keep hypotheses separate. Include legitimate should-pass controls and realistic near-boundary negatives; a judge that fails everything must not look successful. Synthetic cases remain synthetic until assessed; agent agreement cannot manufacture expert gold.

Preserve a supported negative example even without a replacement answer when its scoped rejection criterion is observable. Keep missing input, unendorsed corrections, unresolved criteria, and source gaps explicit. Useful annotations that cannot yet be replayed belong in the incomplete queue, outside scored denominators with their exclusion counts reported.

## Build the smallest useful package

Reuse project conventions. If none exist, follow [the local package contract](../run-eval/references/package.md): `rubric.md`, `cases.jsonl`, and `config.json`. Store outputs and run evidence separately from skill installations. JSON avoids adding a YAML dependency; use an existing YAML config when the project already supports it.

For each case, retain its input/context, reviewed output or execution entrypoint, applicable checks, source authority, construction family, and intended use. Keep expected task content separate from expert PASS/FAIL calibration labels. Label-bearing IDs, source notes, old verdicts, and gold rationales stay outside the blind judge payload. Approved reference answers may be supplied when the production grading task legitimately needs them.

Split by source record or construction family, not by cosmetic variants. Keep development, calibration, final test, regression, and frontier roles explicit. Cases inspected while fitting the rubric are development evidence; a case does not become unseen again by renaming its partition. Do not inspect final-test semantics while authoring unless the user requests opening that set.

Write one question per independent requirement. Record applicability and the passing direction instead of assuming every yes is good. Apply only criteria supported by the task or expert. Use a typed unknown or execution error when evidence is insufficient; neither silently becomes a correct answer or a domain failure.

## Validate the grader and its intent

Exercise clear passes, clear failures, and relevant boundary cases through the real grading path. A passing reference and a deliberately wrong control provide different evidence. Run existing checks or direct local replays; respect project rules on creating new test files. A small control set establishes those observations, not general correctness.

For a semantic judge, use separate expert-labeled development and calibration examples from both classes. Read [judge calibration](references/judges.md) before fitting or reporting a judge. Freeze the rubric, judge identity, prompt, parser, harness version, sampling, and budget before interpreting a comparison. Treat changes as a new eval revision and preserve earlier results.

Use [Cross-Examine](../cross-examine/SKILL.md) when adversarial hardening is requested or needed for a score that will drive decisions. Give it the intended capability, permitted shortcuts, access boundary, and frozen grading path. Keep any attack budget bounded. Its ledger should explain both reward-hacking flaws and valid solutions the grader rejects. In an ordinary drafting pass, record untested risks without claiming an adversarial audit occurred.

Run the resulting package through [Run Eval](../run-eval/SKILL.md) when execution is requested and within the authorized environment and budget. Contrast meaningful baselines when available, reporting cost and trial conditions. A saturated regression set can be useful; model discrimination is a separate claim.

## Finish with a reviewable result

Report the package path, measured capability, evidence sources, cases ready for replay, unresolved examples, actual validation, and limits. Distinguish grader calibration from product performance and development evidence from held-out evidence. Do not infer a release threshold or production-trust verdict from a small all-pass run.

Creating an eval does not authorize product fixes, paid campaigns, opening a sealed test set, publication, or uploading expert data. For a requested shareable handoff, use [the export workflow](../expert-mode/references/export.md).
