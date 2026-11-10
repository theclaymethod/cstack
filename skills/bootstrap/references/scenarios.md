# Synthetic scenario generation

Read before dispatching scenario authors. Use the researched methods in [the source review](research.md) to select techniques; tools are optional and should fit the project. A source's suggested volume or score target is a heuristic, not a Bootstrap requirement.

## Generate conditions, then language

Build a small coverage table from the intent contract: requirement, relevant dimensions, allowed combinations, expected boundary, and source. Dimensions earn their place when changing a value could change acceptable behavior or expose a credible failure. Examples include intent clarity, evidence sufficiency, prior state, tool availability, and whether action has been authorized. Persona or tone matters only when the product makes it relevant.

Separate generation into two passes:

1. Construct feasible tuples of conditions. Exclude impossible states and unsupported domain assumptions. Use domain fixtures or requirements to establish facts.
2. Render tuples into realistic requests, contexts, conversations, and initial state. Preserve the conditions while varying wording. Keep proposed expectations in a separate field.

Ask the user only about domain assumptions that materially affect realism or the boundary. Leave such scenarios provisional while generating other independent cases. A synthetic document may be valid fictional evidence in a self-contained task, but its external factual claims are not established by generation.

For scenarios with related records or environment state, use existing fixture builders or small seeded code to generate consistent IDs, relationships, dates, permissions, and state. Validate these facts before asking a model to write prose from the allowed facts. Retain fact/source IDs, check prose for unsupported claims, and validate the complete world again after merging workers' outputs. A simple routing input needs no world generator.

## Choose a method for the coverage gap

| Gap | Method | Check before review |
| --- | --- | --- |
| Broad initial coverage | Dimension/tuple generation with ordinary valid cases and supported alternatives. | Each tuple is feasible and tied to a requirement; coverage reflects meaningful conditions. |
| An ambiguous decision boundary | Minimal contrast pairs: change one relevant condition and propose whether the expected behavior flips. | The differing condition, not incidental wording, explains the judgment. |
| Wording sensitivity | Meaning-preserving transformations such as paraphrase or irrelevant-context insertion. | The transformation preserves facts, authorization, and expected behavior; group variants in one family. |
| A changed condition | Directional transformations such as removing evidence or changing prior state. | State the expected relationship explicitly; human review decides whether it holds. |
| A credible failure mechanism | Bounded adversarial proposals targeting a named requirement. | Separate realistic stress cases from artificial ones; verify the required access and environment. |
| Multi-step behavior | Scenario graphs or short conversations that include state transitions and tool responses. | Transitions are reachable, tool semantics match the project, and final/preserved state is observable. |

Use constrained pairwise coverage only when interactions across several dimensions are the concern; cover critical higher-order combinations explicitly. Exhaustive products and arbitrary paraphrase volume are usually less useful than a few distinct decision boundaries.

After rejecting infeasible or repetitive cases, recompute any claimed interaction coverage. Report uncovered combinations and budget limits rather than counting removed rows as covered.

## Worker brief

Give each scenario author a bounded assignment with:

- The intent revision, requirements, confirmed alternatives, and open questions.
- Its coverage slice and proposed output count/budget; other authors' initial answers remain withheld.
- Permitted project sources, relevant tools/state semantics, and the synthetic-data boundary.
- A scratch destination owned only by that author.
- Required output: situation/input and context, initial state where relevant, proposed expectation and concise reason, requirement link, assumptions, origin/source, method, and source/construction family.

Ask authors to return proposals and gaps, not gold labels. After the first independent pass, the coordinator can commission targeted additions for missed boundaries. Record that these later proposals were informed by earlier ones.

## Merge by meaning and verify feasibility

Deduplicate exact inputs and near-identical behavioral situations. Keep a pair when its changed condition changes the expected outcome; collapse decorative variants when review time is limited. Retain lineage when one source or template produced several cases. When families overlap, group connected derivatives conservatively rather than putting siblings into different partitions.

Inspect tool/API constraints, data availability, permissions, and reachable state. For executable scenarios, validate fixtures and reset using the project's facilities when available. A scenario can remain a useful contract proposal before implementation, but record which conditions are hypothetical and what is needed to run it. Avoid importing a tool's generated expected answer as an approved reference.

Track coverage by requirements and conditions exercised, plus remaining gaps. A synthetically balanced or adversarially selected batch does not estimate production prevalence. Preserve separate identities for synthetic input, simulated output, and actual execution trace.

## Reserve evidence before authoring

Group same-source, same-template, transformed, and repeated-attempt variants before selecting development and calibration roles. Hold independent scenario families and concrete outcomes away from evaluator authors where feasible. Have a fresh validator run a frozen evaluator over the permitted evidence, with human outcome labels withheld until verdicts freeze. Opening a mismatch for fitting makes that family development material.

When there is no independent family or no human-labeled output, state that limit. Bootstrap can still deliver runnable contract checks and development controls; reserve claims about judge calibration until the needed evidence exists.
