# Skill-pack ablation

2026-11-10. Applied one literal-deletion candidate to all eleven `SKILL.md` entrypoints after completing the [Ablation/Bitter Lesson audit](../simplification/CROSS_EXAMINE_LEDGER.md). The audit confirms one operator-side accounting-evidence defect and its repair; no candidate-access exploit or wrong native task score was established.

## Selected change

Removed 59 passages: repeated purpose/setup prose, generic narration, and procedures already supplied by retained instructions or linked references. Frontmatter and every supporting reference, script and asset are unchanged from the repaired full-guidance baseline. No new wording was substituted. The accounting lesson added before this experiment remains intact.

| Measure | Original full entrypoints | Selected entrypoints | Reduction |
| --- | ---: | ---: | ---: |
| Words, whitespace-separated | 9,486 | 8,722 | 764 / 8.1% |
| UTF-8 bytes | 72,346 | 67,031 | 5,315 / 7.3% |

These measure entrypoint text only. Always-loaded frontmatter is unchanged. Supporting material was retained, so this does not establish the same reduction in total context consumed. Token usage, agent cost and latency savings are unmeasured.

[Original skill resources](original-skills/), [literal deletion units and hashes](deletion-units.json), [exact diff](candidate.diff), [selection](selection.json), [experiment contract](ABLATION-CONTRACT.md). This was one combined candidate, not leave-one-out attribution, an exhaustive search or a global-minimum result.

## Actual skill-use comparison

Six fresh non-forked agents received identical task packets with either full or shortened installed guidance, in separate playground workspaces. Same inherited host model configuration, no model override; an exact hosted model revision was unavailable. No provider-client or paid model calls were made. The [task packets](tasks/) and [quality checklist](quality-checks.json) were fixed before candidate outcomes were graded.

| Matched exercise | Skills exercised | Full | Shortened |
| --- | --- | ---: | ---: |
| Capture and repeated merge | Expert Mode, Distill Me | 8/8 checks | 8/8 checks |
| Approved authoring and controls | Bootstrap, Create Eval, Adversarial Cases | 8/8 | 8/8 |
| Execution, judge fitting mechanics and optimization | Run Eval, Hill Climb, Calibrate Judge, Ablation, Bitter Lesson, Cross-Examine | 12/12 | 12/12 |

Capture preserved scripted authority, the unproven narrative-to-native association, original/regenerated versions, an unrelated seeded annotation, amendments and unresolved urgency. Repeated merge added no duplicates and did not restart ongoing capture.

Authoring preserved exact typed request/state/expectation fidelity for approved A revision1 and corrected B revision2. Deferred urgency and the new unapproved contrast stayed excluded. Actual native controls accepted legitimate and alternative IDs and rejected false creation claims. Missing independent roles and real human labels remained explicit.

Operations actually ran the product and native campaign, rejecting a higher-scoring regressive candidate. Both versions inspected offline judge and simplification evidence, retained undefined kappa/uncertainty and probability limits, checked real combined deletions, and left formal proxy-audit adjudication unreviewed when independent roles were unavailable. All source artifacts and selected native outcomes were retained.

The coordinator reviewed semantics against source/output evidence and recomputed native verdicts with the existing grader. The coordinator also proposed the removals; this is not an independent human-rated study. [Semantic review](semantic-review.json), [native/source verification](verification/), and [raw executions](evidence/) separate those claims. Instruction-marker checks and scripted control passes alone were not credited as skill effectiveness.

## Frozen confirmation

The complete 47-file candidate skill bundle was [hash-frozen](confirmation-freeze.json) before two more fresh agents received the same combined confirmation task. Both passed all six reviewed checks: exact rich-state authoring, legitimate/alternative acceptance and false-claim rejection, real frozen new-model comparisons, honest missing old-model cells, retained ERROR/undefined-kappa accounting, and source/budget fidelity. [Confirmation review](confirmation-review.json).

Both confirmed a finite new-fixture reduction from nine units/4,193 bytes to two units/3,671 bytes, with 8/8 development and 4/4 confirmation for baseline and selected candidate. Neither executed the unavailable old backend or claimed production migration parity. Their additional search schedules differed: full guidance used 35 native cases and shortened guidance 99, both within 120. This does not support execution-efficiency or cost improvement.

Across the eight agent exercises, full-guidance runs used 297 native cases and shortened runs 363; each side also used 102 deterministic judge response processes. These are accounting totals across deliberately mixed controls, not aggregate product-success scores or independent gold examples. Cases, models and expectations are synthetic and exposed. Confirmation is a workflow role, not an unseen-data guarantee.

## Verification and limits

Both full and shortened packages passed all eleven existing control groups. Each native suite ran **56 tests: 55 passed, one optional DSPy SDK check skipped**. [Baseline controls](controls/baseline-controls/summary.json), [candidate controls](controls/candidate-controls/summary.json). All eleven selected skills also pass the skill validator, references remain reachable, and task/evaluator sources stay fixed.

To repeat agent use, materialize a fresh playground, install either the current skills or `original-skills/`, and give a fresh agent the matching task packet. Preserve a new output directory and execution budget. The scripts written during each observed run are retained beside that run; they are project-local exercise artifacts, not skill runtimes.

`verify_evidence.py --workspace <workspace> --source <cstack> --evidence <preserved-exercise> --out <receipt.json>` checks native receipts and installed source. Add `--skills <original-skills>` for full-guidance workspaces. It does not replace semantic review. Replays require a compatible recorded Python/native execution contract; changed environments need a new comparable run.

No paid/provider calls, new dependencies, production deployment, new labels or remote publication. The comparison supports retaining this combined reduction on these observed tasks only. It does not prove statistical non-inferiority, universal skill preservation, causality for individual deleted passages, broader discovery quality, live judge calibration or production-model migration quality. No follow-up tuning used the confirmation results.
