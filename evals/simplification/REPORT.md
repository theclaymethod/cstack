# Ablation and Bitter Lesson implementation

Validated 2026-11-10. The preceding C Stack work was committed and pushed to `main` as [`ac920a1`](https://github.com/theclaymethod/cstack/commit/ac920a1e00729cfcc9be38b13b1a4fe7260376fe) before these additions began. This report describes the subsequent local implementation.

## Delivered behavior

[Ablation](../../skills/ablation/SKILL.md) removes authorized prompt/context or workflow components under a declared quality constraint. It distinguishes conditional contribution from combined reduction, validates dependencies, tests interactions, anchors loss to the original baseline, and limits minimality and preservation claims to actual evidence.

[Bitter Lesson](../../skills/bitter-lesson/SKILL.md) applies that process to model migrations. It compares existing and simplified designs across models, preserves necessary task information, separates upgrade and simplification effects, and delivers a versioned production bundle with the project's release/rollback handoff.

Both skills contain Markdown instructions and references only. Executable adapters, candidates, evidence and dependencies remain project-local. Hill Climb links to the specialized workflows; README graph, installation, playground exercises and plugin manifests now cover eleven skills, version 0.9.0. Harbor remains preferred for new executable agent tasks; this fixture retains its native format.

## Offline mechanics

The new [project-local adapter](../../fixtures/playground/simplification/README.md) renders named prompt units into standalone candidate programs. Every score comes from fresh candidate subprocesses through the existing native `evaluate.py`; no second grader was added. Native evaluator, original cases/spec/rubric and support-agent source remain byte-identical to the pushed baseline.

The models and interactions are programmed controls. The old stand-in needs an authorization reminder; the new one does not. Both need one of two duplicate reminders. Compensating cue pairs exercise combined removal. This is synthetic fixture behavior, not model learning or evidence about commercial model capability.

The [main run](evidence/mechanics/results.json) executed **164 native cases** within a 200-case limit, including **20 separately reserved final cases**. It rejects the union of individually harmless deletions, distinguishes invalid dependencies before execution, accepts a combined conflict removal that individual removals cannot achieve, freezes five exact final configurations, and closes fitting before final selection.

| Confirmed configuration | Prompt units | Rendered UTF-8 bytes | Development | Confirmation |
| --- | ---: | ---: | ---: | ---: |
| Old, existing | 9 | 4193 | 8/8 | 4/4 |
| Old, reduced | 3 | 3746 | 8/8 | 4/4 |
| New, existing | 9 | 4193 | 8/8 | 4/4 |
| Old, shared simplified design | 2 | 3667 | 4/8 | 2/4 |
| New, shared simplified design | 2 | 3667 | 8/8 | 4/4 |

The selected old-model reduction retains contract, legacy authorization and one duplicate reminder. The new-model fixture retains contract and one duplicate reminder. Quality gates require zero observed loss/regressions against the original baseline; the proposed new bundle also passes the new model's existing-design comparison. Prompt bytes are measured, while token counts and model cost/latency savings are unmeasured.

## Independent use and confirmed repair

A fresh agent used both installed skills in an isolated materialized workspace without the scripted demo or test solutions. Its [report](evidence/forward/report.md) and [executed driver](evidence/forward-driver.py) record **137/160 native cases**: 112 development, 24 reserved confirmation and one malformed-output control. It recovered the same reductions, tested alternative duplicate reminders, checked group effects and produced exact prompts/diffs. No guidance ambiguity affected execution. This run preserves the pre-repair adapter revision and identifies its hash; it does not claim to validate the subsequent repair.

A separate observed mechanics flaw allowed direct mutation of the live final-plan dictionary to change the configuration after freeze. The before-repair reproduction executed four cases with the wrong final configuration. The fix checks live contract/state against saved snapshots as well as source/evidence hashes. The same [reproducer](evidence/review/reproduce.py) now rejects the change before any calls. [Before](evidence/review/before/reproduction.json) and [after](evidence/review/after/reproduction.json) records and the pre-fix source are preserved. The new regression also checks that mutating the caller's original plan does not alter its frozen copy.

## Validation

All **eleven control groups passed**. The native suite ran **55 tests: 54 passed, one optional DSPy SDK check skipped**. Ten new tests cover unit/dependency validity, both interaction directions, accumulated-loss rejection, model-dependent fixture behavior, confirmation budget protection, exact final membership, evidence/contract drift and charged interruptions. All eleven skill packages pass the skill validator. [Control summary](evidence/validation/summary.json), [native test log](evidence/validation/playground.stderr.txt), [skill validation](evidence/validation/skill-validation.json), [source hashes](evidence/source-sha256.json).

Reproduce from a fresh project workspace:

```sh
python3 fixtures/playground/scripts/new_workspace.py --out eval-runs/simplification-playground
cd eval-runs/simplification-playground
python3 -m simplification.run --out eval-runs/simplification
python3 scripts/run_cstack_evals.py --suite all --out eval-runs/controls
```

For the repair reproducer, pass `--project <materialized-playground>` and a fresh `--out`; add `--protocol <protocol-before-fix.py>` to exercise the preserved defect. Native candidate attempts, forward-use calls, repair replays and regression tests are separate counters, not one optimizer budget.

To replay the independent driver, copy `evidence/forward-driver.py` into the materialized workspace as `eval-runs/forward_driver.py`, then run `python3 eval-runs/forward_driver.py --out eval-runs/forward-repeat`. Its location determines the project root. A replay uses that workspace's adapter revision; the preserved original report identifies the pre-repair revision actually tested by the independent agent.

## Limits

Zero provider/paid calls, model-client dependencies, production side effects or deployments. All cases, expectations and model behaviors are synthetic and readable. Final membership exercises freezing and confirmation, not blindness or unseen generalization. No human gold, real prompt quality, probability calibration, statistical non-inferiority, global minimum, or production migration is established. Selected artifacts are offline fixture programs. The adapter is one-shot with no resume loader; subprocesses have host permissions and do not provide adversarial containment.

The subsequent [Cross-Examine audit](CROSS_EXAMINE_LEDGER.md) repairs durable execution-receipt verification. The [skill-pack ablation](../skill-ablation/REPORT.md) then tests literal entrypoint deletions against the repaired full baseline; the original results above retain their historical revision and scope.
