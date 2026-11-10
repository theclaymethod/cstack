---
name: adversarial-cases
description: Construct controlled adversarial scenarios and executable fault-injection cases for Bootstrap, Cross-Examine, or a scoped eval workflow. Return proposed expectations, reproducible challenges, activation evidence, and outcome witnesses; the parent owns approval and adjudication.
---

# Adversarial Cases

Build the smallest useful challenge to a specific requirement or failure hypothesis. Give the parent enough evidence to distinguish a defect, a valid alternative, an unresolved product decision, and a fault that never activated. Case construction does not establish human labels, confirmed findings, or accepted repairs.

## Receive the parent's contract

Recover the original requirement and revision, raw input/context/state, supported alternatives, project runner, evaluated agent access, permitted operator injections, evidence boundaries, and case/execution budget. Read project instructions and existing fixtures. Resolve facts from the project before asking the parent for missing judgments. Continue independent construction while affected intent remains provisional.

Keep the intended outcome fixed across the challenge. State the exact assumption being tested and why the situation is feasible. Separate source-backed facts, synthetic fixtures, and hypotheses. An impossible user goal can legitimately test clarification or refusal; distinguish that from an accidentally impossible environment.

Use the parent's case format or the equivalent fields in [the case contract](references/case-contract.md). Keep artifacts in its eval workspace, outside the installed skill. Preserve source/construction families across variants, transformations, repeated runs, and minimization. The parent decides coverage priorities, volume, realism requirements, and allowed scope.

For generation/reduction/selection, read [synthetic methods](references/synthetic-methods.md). For lifecycle, subprocess, storage or dependency perturbations, read [failure methods](references/failure-methods.md). These are recipes for project-local implementations; no generator or fault runtime is bundled with this skill.

## Construct conditions before wording

Choose a meaningful boundary: authorization or evidence changes, stale/conflicting state, a malformed result, a partial operation, dependency failure, or an interrupted lifecycle transition. Tie it to a requirement and credible failure mechanism. Generate feasible conditions first, then render requests or conversation text from those facts.

Prefer a minimal contrast pair when it isolates the boundary. For stateful scenarios, preserve consistent identities, relationships, chronology, permissions, and reachable transitions. Existing fixture builders or small deterministic scripts can establish those facts. A model-generated document or expected answer remains a proposal, not independent domain truth.

Specify the correct response under the perturbation: recovery, safe non-action, clarification, or completion may each be legitimate when supported by intent. Preserve acceptable wording, implementation paths, and outcome representations. A tool error or inability to finish the original action is not itself proof of task failure.

## Make executable cases attributable

When execution is available, read [injection and witnesses](references/injection.md). Use the project's real entrypoint and scoring path with a resettable, bounded driver. Identify the injection boundary, trigger/preconditions, perturbation, and observable activation witness. Reuse existing hooks or the smallest local driver; record versions and coverage limits of instrumentation. If instrumentation changes the evaluated program, show its clean baseline before attributing behavior to the fault.

Classify access explicitly. A candidate exploit must work within the evaluated agent's actual access. An operator-injected crash or dependency failure is a resilience experiment, with its extra access recorded. A verifier challenge may use an explicitly supplied defective verifier or frozen historical version; identify that version rather than attributing its flaw to the current system. Keep operator and candidate writable paths separate where the environment supports it. Local scratch copies and timeouts do not establish containment.

Record armed, activated, and observed outcome separately. A configured fault name is insufficient. Retain operator-side activation evidence and the independently observed effect where available, such as a targeted event plus actual process exit, a failed dependency call, or a missing committed state transition. A hook event before termination alone does not prove termination; a process exit alone does not identify the intended injection point. Describe what the available witnesses jointly establish.

Use actual resulting state or artifacts to judge the original requirement independently of candidate success claims and the disputed score. Keep missing evidence, setup errors, and ambiguous expectations visible. If the trigger is not reached, report not activated; the run does not support a claim about behavior under that fault. If execution/setup is unavailable, return a proposed case and the smallest missing execution prerequisite.

## Control, replay, and minimize

Pair the challenge with a clean control and relevant legitimate alternatives. Include a non-activation or no-op control when activation could be mistaken for setup success. Keep inputs, versions, initial state, and the declared trial policy comparable. Verify reset between attempts and preserve original failed artifacts instead of replacing them with repaired outputs.

Replay within the parent's budget. Then remove irrelevant fields, steps, timing assumptions, or perturbations while preserving feasibility, observed activation, and the same distinguishing outcome. Minimize the mechanism rather than merely shortening its wording. Recheck controls after minimization; retain failed reductions and uncertainty where variability prevents stable attribution. Additional trials and minimization attempts consume the same declared budget.

Freeze each scored version and preserve evidence before changing a case or instrument. Record material changes as revisions; return changed expected behavior to the parent. Cases exposed during fitting or repair remain development evidence.

## Return the parent handoff

Return the requirement/source revision, failure hypothesis, case conditions, provenance/family, allowed access, proposed expectation, setup/reset/injection commands, activation and outcome evidence, actual score, controls, minimization history, and limits. Name unexecuted work and non-activated attempts explicitly. Use only observed results; a new manifest or claimed successful run is not proof that construction or execution happened.

For [Bootstrap](../bootstrap/SKILL.md), provide concise scenario cards with guessed expectations, reasons, and unresolved assumptions. Keep approval pending until the parent obtains the user's scoped decision; scenario approval is distinct from labeling a concrete output.

For [Cross-Examine](../cross-examine/SKILL.md), provide the reproducible challenge, access facts, native scoring result, and independent outcome witness. The parent and its independent intent reviewer decide whether the discrepancy is a finding and whether a repair preserves the original requirement. A bounded run with no demonstrated defect is a valid case-building result.
