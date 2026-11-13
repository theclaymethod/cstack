# Co-climb decision eval

Evaluate the decisions that keep alternating target/judge search valid. This package has 16 synthetic development scenarios, an answer-free task prompt, a deterministic decision grader, and adversarial grader controls. It does not execute a target campaign or measure live model quality.

## Run

From the repository root:

```sh
python3 -m unittest discover -s evals/co-climb -v
python3 evals/co-climb/evaluate.py --prepare eval-runs/co-climb-prompts
```

Preparation writes one self-contained prompt per case, including the current co-climb skill and references, plus a source-hash manifest. It excludes the answer key, scoring rules and case-family metadata. It does not launch models, upload files, or spend provider calls. Use a fresh output directory so a run's inputs cannot be silently overwritten.

Give each prepared prompt to the agent/runtime being evaluated in a fresh context without repository tools or access to `expected.json`. Save its actual response, model/configuration, invocation and errors. Combine the response objects into an `answers.jsonl` file, then grade:

```sh
python3 evals/co-climb/evaluate.py --answers eval-runs/co-climb-answers.jsonl
```

Every response must identify its case and follow [prompt.md](prompt.md). All cases stay in the denominator. Missing answers are ERROR, incorrect decisions are FAIL, and duplicate/unknown case IDs invalidate the submission. The command exits nonzero on failure or incomplete coverage. A strict format failure is not silently repaired into success.

For a before/after comparison, prepare prompts from each skill revision, freeze the same runtime and settings, and preserve both manifests and raw responses. This suite is exposed development evidence, not a sealed final set. Do not give the tested agent the full checkout and claim answer-key isolation; directory separation alone is not containment.

## What is judged

The cases ask for next actions, an exploratory target archive, confirmed promotions and, where applicable, a judge selection. Action IDs encode observable choices, not prose keywords. The grader checks action membership and only meaningful ordering dependencies. Branch order does not matter. The rank-reversal case accepts either pruning the old winner or retaining it as exploratory after revoking promotion.

| Mechanism | Cases |
| --- | --- |
| Branch retention versus promotion | Complementary candidates, one genuine survivor, rank reversal |
| Comparable evidence | Judge switch, changed target, in-loop judge change, cherry-picked judges |
| Judge quality | Missing evidence, generous judge, uncertain labels |
| Trust and controls | Embedded grading instruction, legitimate refund control, execution errors |
| Boundaries | Confirmation reserve, consumed final set, related case families |

The answer key is an authored interpretation of the skill contract, not human-gold campaign data. Required decisions are deliberately explicit. The suite cannot assess free-form hypothesis quality, actual file mutation, runtime isolation, receipt integrity, total cost accounting, or successful execution of a full campaign. Add execution tasks before claiming those capabilities.

## Grader controls

`test_evaluate.py` executes all reference decisions, a legitimate archive alternative and independent action reordering. It rejects every offered unsafe action, every omitted required action, premature promotion, a greedy archive, reversed evidence dependencies, malformed output, duplicate/unknown cases and partial submissions. It also exercises the CLI and checks prepared inputs for answer-key leakage. Passing these tests validates the grader controls, not an agent's performance.

Keep related cases in the same family when creating new partitions. All current cases are already exposed development fixtures. New frontier or final tasks need fresh source families and their own exposure record.

## Live paired benchmark

With authorized model access and the Codex CLI installed:

```sh
python3 evals/co-climb/live_benchmark.py --out eval-runs/co-climb-live/run --gate accuracy
```

The runner freezes Git revisions and eval hashes, uses GPT-6 Astra at high reasoning, alternates baseline/candidate ordering across three fresh-context pairs, and preserves prompts, raw final responses, events, usage and grading receipts. Each context answers all 16 cases; repeated batches are not independent source cases. User configuration is ignored, shell and web search are disabled, and observed tool use invalidates the run. The model sees no answer key, but this is a decision task rather than an adversarial host-isolation test.

The default accuracy gate requires positive paired gains in at least two repetitions, two additional correct decisions overall, and no new failing case that passed all baseline repetitions. `--gate efficiency` instead preregisters perfect candidate accuracy, no regressions, a 20% skill-bundle character reduction and lower measured input tokens in every pair. It checks the size threshold before launching any model calls. An accuracy tie is not an accuracy improvement. A shorter prompt with preserved scores can support only the stated efficiency result.

Each call has a ten-minute timeout. Budget six model calls for the default run. Provider pricing is not estimated by this script. Keep raw event logs local; publish final decisions and measured usage without internal reasoning or environment logs. Inspect the frozen report before promotion; the runner does not merge or deploy anything.
