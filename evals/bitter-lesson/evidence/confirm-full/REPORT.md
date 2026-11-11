# Synthetic eval package and prompt reduction

Built runnable native cases for A revision1 and B revision2; retained superseded B
revision1 in the decision history. Deferred C remains pending and outside scoring.
Source statements are scripted synthetic decisions, not independent human labels.
The source supplied no reviewed output; newly generated outputs receive their own
native verdicts. All canonical product/evaluator/spec/rubric/cases remain unchanged.

Eight actual control programs ran on both approved cases (16 attempts). The
conforming candidate and arbitrary alternative ID passed both. A claim of creation
without an appended ticket failed B. Nested original-ticket mutation, unrelated-state
mutation, wrong account and duplicate ID were rejected. Missing note produced two
schema ERRORs, distinct from task FAILs. See controls/results.json and native traces
for actual inputs, outputs, stdout/stderr, before/after state and check results.

The authorized new-fixture baseline passed 8/8 development cases. Seven frozen
development configurations consumed 56 attempts. The selected combined reduction
keeps contract and duplicate-b and passed 8/8 without regressions. Removing the last
duplicate cue failed the duplicate slice; removing just one conflicting cue also
regressed, while removing the pair worked. Exact configurations, parentage,
hypotheses, prompts, diffs and unsuccessful candidates are retained. Baseline and
selection were frozen before confirmation; both passed 4/4 on the same four cases
(eight more attempts). The finite zero-loss fixture gate passed. These readable,
inspected cases are exposed evidence; no unseen/generalization or statistical
non-inferiority claim follows. This is the smallest confirmed candidate found in
the declared bounded search, not a proven globally minimal prompt.

The rendered full prompt is 4,193 bytes and selected prompt is 3,667 bytes
(526 bytes removed; 9 units to 2). Exact measured values in comparison.json govern
if the fixture's text changes. Only the new-fixture existing/reduced contrast ran.
The unavailable, unauthorized old backend has no measured cells. Model effects,
upgrade-enabled simplification, production-relative quality, money, tokens and
model-latency savings remain unknown. The backend is a programmed Python stand-in;
the inherited host model did not change. No deployment or hosted-model experiment
occurred. The recoverable full bundle is the local rollback artifact; release is
outside this scope.

The existing agreement helpers analyzed the four stored PASS references: three
PASS decisions, one parsing ERROR. Coverage is 3/4 (75%), conditional agreement is
3/3 (100%), and all-selected matching is 3/4. Decided confusion is TN=3, TP=FN=FP=0;
the PASS class has one ERROR. Kappa is undefined because expected disagreement is
zero; failure catch is undefined because no gold FAILs exist. Independent source
families were not supplied, so no bootstrap interval is justified. Probabilities,
raw responses and original parser settings are unavailable. These observations
cannot calibrate an automated judge. Independent authoritative labels spanning
both classes, complete responses, a fixed judge/parser/input contract and an
authorized acceptance policy are still missing. No live judge fitting or release
threshold ran.

Total usage: 80 actual native case attempts out of 120; 16 grader controls, 56
prompt development, eight frozen confirmations. All attempts completed. Zero
provider/network/judge calls, nested agents or dependencies. Local native wall
times are fixture process overhead, not model latency. This authoring script and
the source snapshots make the package reviewable; hashes detect drift, not hostile
filesystem changes. Native candidates ran with host permissions, fresh per-case
processes and temporary working directories. There was no independent reviewer.

Run `python3 eval-runs/skill-exercise/build.py` only in a fresh disposable workspace
before evidence exists; it refuses overwrite. Replay the package with
`python3 evaluate.py run --candidate eval-runs/skill-exercise/selected-candidate.py
--cases eval-runs/skill-exercise/package/cases.jsonl --suite development --out <fresh>`.
That replay consumes two further native attempts and is not included in this run.

Read-only verification: `python3 eval-runs/skill-exercise/verify.py` checked all
17 native runs, all 80 attempts, source/snapshot consistency and frozen evidence
with zero additional executions. Its actual output is saved in verification.json.
