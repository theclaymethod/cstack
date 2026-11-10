# Calibrate Judge development report

Validated 2026-11-10 for C Stack 0.8.0. The new [Calibrate Judge skill](../../skills/calibrate-judge/SKILL.md) is Markdown instructions/references only. It supports Jev-style typed judgments and traditional LLM judges through project-local implementations. No model client, statistical dependency or runtime is bundled with the skill.

## Scope and actual results

The playground validates offline mechanics, not a live judge. The [native support contract](../../fixtures/playground/evals/spec.json), source cases, rubric and evaluator are unchanged. The native runner executes its original and conforming candidates on twelve cases, yielding 24 actual outputs across twelve source families. Labels are native code-derived synthetic outcomes, not human annotations. Both outputs for a task stay in the same partition: eight rows/four families per train, validation and final role.

The local backend is explicitly a deterministic response-shape fixture. It emits an LLM-style verdict or Jev-style Noul response. Predeclared policies use a success claim or the native state oracle; the latter is deliberately circular and cannot demonstrate independent model learning. Typed scores are synthetic probabilities for mechanics, not calibrated forecasts.

The driver records untuned baselines, selects among two LLM policy configurations and four typed policy/threshold configurations on validation, freezes the exact final plan, and completes every planned prediction before final comparison. Final-role evidence is fully readable synthetic data. It does not establish blind validation or unseen performance.

| Simulated backend/policy | Final-role agreement | Kappa | Coverage |
| --- | ---: | ---: | ---: |
| LLM-shaped baseline | 4/8 | -0.3333 | 8/8 |
| LLM-shaped selected state policy | 8/8 | 1 | 8/8 |
| Jev-shaped baseline | 6/8 | 0 | 8/8 |
| Jev-shaped selected state policy/threshold | 8/8 | 1 | 8/8 |

These values verify expected mechanics, not real Jev/LLM accuracy. Full confusion counts, failure catch, false-pass/false-rejection denominators, UNKNOWN/errors, probability losses/bins and uncertainty diagnostics remain in [the result](evidence/mechanics/results.json). Family-bootstrap replicates with undefined statistics suppress the affected interval; perfect point agreement on this small corpus does not establish trust. No probability calibrator or model weights were fitted.

One complete demonstration uses **24 native support executions and 102 local fixture-judge subprocesses**, including six repeated calls on one frozen source item per backend. The 200-call fixture ceiling covers baseline, selection, confirmation and repetitions. Repeated calls do not create independent gold examples. Actual provider calls, paid model calls and live calibration runs are **zero**. Selected artifacts explicitly say they are not deployable live judges and have no owner release policy.

## What was validated

- Hand-calculated nominal and ordinal-weighted kappa, class imbalance, zero-denominator/undefined statistics, abstention/error coverage, Brier/log loss and reliability bins.
- Family-aware uncertainty with limited independent families and visible undefined bootstrap replicates.
- Explicit yes/failure polarity, probability-versus-confidence handling, optional rationale, typed Noul/binary Choice and structured LLM parsing. Ordinal native Score execution remains unrun.
- Deterministic rejection of a false creation claim containing a claimed gold PASS instruction. This is fixture data handling, not live model prompt-injection resistance.
- Exact source/data/configuration/case membership, whitelisted public inputs, frozen response records and raw-to-normalized decision consistency.
- Complete final-prediction plans, blocked premature comparison/unplanned candidates, consumed-final fitting prevention, bounded calls and immutable run identities.

The “private” label file is private by convention on a shared host. Trusted workers receive only declared runtime evidence; the source behavior/reference fields are legitimate task criteria while correctness labels and provenance remain outside the payload. These inspected boundaries do not establish containment against malicious host access. The campaign is deliberately nonresumable and refuses existing output paths; it does not claim a cross-campaign exposure registry.

## Independent use and confirmed repairs

A fresh agent used the installed skill on its own eight-outcome/four-family subset. It executed **24 native source cases and 40 local fixture subprocesses**, including comparisons, repetitions and boundary probes, with zero provider/proposer calls. It produced a scoped [handoff](evidence/forward-use-report.md) with synthetic authority, exposed-final limits, suppressed intervals and no live readiness claim. Its initial instrumentation error occurred before case/judge execution and is disclosed. The raw [summary](evidence/forward-use/summary.json) and [checks](evidence/forward-use/checks.json) are retained.

Independent [review](evidence/review.md) found and replayed two defects in the initial implementation:

1. Malformed Choice probability arrays and extremely large numeric Noul values escaped as exceptions. The adapter now validates container/range before assumed operations and preserves ERROR; regressions cover both inputs.
2. A self-consistent rewrite of raw/parsed predictions plus the adjacent manifest could change accepted agreement without another execution. Completed predictions and manifests are now anchored in the campaign run record. The exact rewrite is rejected, with calls unchanged. This is a consistency repair, not a defense against rewriting every host asset and state object.

The reviewer independently rechecked both fixes. Reproductions used **24 local fixture calls total**, no provider calls or native source reruns. [Original/fixed evidence](evidence/review-reproduction/evidence-fixed.txt) and the before-fix source snapshots remain preserved. The protocol reference teaches the anchored-evidence requirement.

## Run and integration

Create a fresh workspace from the C Stack checkout:

```sh
python3 fixtures/playground/scripts/new_workspace.py --out eval-runs/calibration-playground
cd eval-runs/calibration-playground
python3 -m judge_calibration.run --out eval-runs/judge-calibration
```

The [local guide](../../fixtures/playground/judge_calibration/README.md) describes the exact artifacts and limits; [exercise 10](../../fixtures/playground/exercises/10-calibrate-judge.md) supports agent-led practice. The combined runner exposes `--suite judge-calibration`; `--suite all` now runs ten control groups. Existing optional DSPy compatibility still needs `--dspy-check` and its separate project-local development environment, with no model calls.

All **ten groups passed**. A final native-group rerun after adding the claimed-gold content control passed **45 native tests**, and all **nine skills** passed frontmatter validation. [Control summary](evidence/validation/summary.json), [native test log](evidence/validation/playground.stderr.txt) and [skill checks](evidence/skill-validation.json) retain the local observations. Historical paths/PIDs and source snapshots identify their original runs; use fresh output paths for replay.

Create Eval and Run Eval route judge fitting here; Hill Climb supplies optional bounded search while keeping product evaluators frozen. README graph, installation examples, metadata and the fixture now include the ninth skill. Harbor preference and existing formats remain intact. Human gold, live backend/client/model validation, cost budgets, probability recalibration, weight training and production acceptance remain future project-specific work. No live improvement, generalization, human calibration or production release is claimed by this addition.
