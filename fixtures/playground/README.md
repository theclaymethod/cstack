# cstack playground fixture

A reusable fixture inside cstack for trying the current skills against a small, deliberately imperfect project. The generated workspace copies every skill in the owning checkout, including help and course. The product is a deterministic Python support agent. Its bugs, requests, conversation excerpts, expected outcomes, and candidate examples are synthetic. There is no website or model-provider setup.

Use Python 3.11+ on macOS or Linux. The code uses the standard library; campaign commands use a Unix advisory lock. Candidate programs run with your local permissions. Only run code you authorize: subprocesses and timeouts are not a security sandbox.

## Start here

From the cstack repository root, create a fresh disposable workspace:

```sh
python3 fixtures/playground/scripts/new_workspace.py --out eval-runs/playground
cd eval-runs/playground
python3 scripts/sync_skills.py --check
python3 -m unittest discover -s tests -v
python3 evaluate.py run --candidate support_agent.py --suite development --out eval-runs/baseline
```

The canonical fixture contains the product, evaluator, cases, and exercises. It has no nested Git repository or installed skill copies. The workspace command creates a local Git repository, copies the current skills, and records the owning cstack source. It refuses existing destinations; use a new directory to reset. You can use an absolute output path outside cstack instead of `eval-runs/`.

In the generated workspace, the skills are copied into `.agents/skills`, with relative links for Claude Code and Cursor. Syncing refreshes unchanged copies and refuses to overwrite local skill edits. Start a new coding-agent session in this repo after a sync. Invoke `$hill-climb` in Codex, `/hill-climb` in Claude Code/Cursor, or ask the agent to read the relevant `.agents/skills/<name>/SKILL.md`.

The baseline passes four of eight development cases. That is an intentional fixture result, not an estimate of AI-agent performance. Every eval run executes the candidate file in a fresh subprocess for each selected case and saves its actual outputs, errors, traces, and identity under the chosen output directory.

## Try a full campaign

The example policy is deterministic: improve the development pass rate with zero regressions of previously passing cases, then compare baseline and candidate on the confirmation suite. The budget counts actual case attempts, including errors and confirmation. These choices belong to this exercise; Hill Climb does not impose them universally.

```sh
python3 evaluate.py start --campaign eval-runs/demo --max-case-runs 48 --reserve-case-runs 8
python3 evaluate.py try --campaign eval-runs/demo --candidate examples/candidates/regression.py --hypothesis "Fix common routing while reusing any existing ticket"
python3 evaluate.py try --campaign eval-runs/demo --candidate examples/candidates/improved.py --hypothesis "Require authorization and scope duplicate checks to an open ticket for the target account"
python3 evaluate.py finish --campaign eval-runs/demo
python3 evaluate.py status --campaign eval-runs/demo
python3 evaluate.py verify --campaign eval-runs/demo
```

The regression candidate scores 6/8 but breaks previously passing closed-ticket and unrelated-account cases, so the campaign rejects it. The improved candidate scores 8/8 and can earn selection through confirmation. The selected snapshot and patch are `best.py` and `best.diff` in the campaign directory. The example does not replace the live `support_agent.py`; review or run the selected snapshot directly.

You can also edit your own candidate and use the same commands. The baseline is snapshotted before search, and unsuccessful later proposals cannot replace the measured incumbent. Use a new output/campaign directory for a new experiment. The runner refuses incompatible source/configuration drift on resume. A stopped or interrupted attempt remains charged until its evidence is reconciled; it is not a free retry.

The confirmation cases are present in this repo. Their name does not hide them from the proposer or establish unseen generalization. All example results are synthetic development/confirmation observations.

## Run cstack's existing eval controls

In a generated workspace, the wrapper resolves the owning cstack checkout. Choose a fresh output directory:

```sh
python3 scripts/run_cstack_evals.py --suite all --out eval-runs/cstack-controls
```

This invokes the existing Expert Review and Cross-Examine calibration scripts, Bootstrap's replay and recorded audit, Hill Climb's recorded audit, the Adversarial Cases replay and recorded audit, project-local method, judge-calibration and simplification experiments, and the workspace's native tests. It saves each command's actual exit, stdout, and stderr. Use `--suite expert-review`, `cross-examine`, `bootstrap`, `bootstrap-audit`, `hill-climb-audit`, `adversarial-cases`, `adversarial-audit`, `methods`, `judge-calibration`, `simplification`, or `playground` for one suite. Use `--source /path/to/cstack` to override the recorded owner. These check the known synthetic controls; they do not launch models or establish that an agent followed every skill.

## Exercises

`/course` walks exercises 01–13 in order. `/help` reads this workspace and names one next skill. The table below is the eleven product skills. Exercises 09 and 13 are part of the same curriculum.

| Skill | Exercise |
| --- | --- |
| Expert Mode | [Capture a scoped correction while inspecting an actual run](exercises/01-expert-mode.md) |
| Distill Me | [Recover judgments and uncertainty without duplicate capture](exercises/02-distill-me.md) |
| Bootstrap | [Interview for a new password-reset behavior and review proposed scenarios](exercises/03-bootstrap.md) |
| Create Eval | [Turn reviewed cases into this project's native format](exercises/04-create-eval.md) |
| Run Eval | [Execute a candidate and inspect fresh traces](exercises/05-run-eval.md) |
| Cross-Examine | [Reproduce and repair a deliberately misleading verifier](exercises/06-cross-examine.md) |
| Hill Climb | [Improve the baseline with a finite campaign and regression constraints](exercises/07-hill-climb.md) |
| Ablation | [Remove components while keeping the model and quality bar fixed](exercises/11-ablation.md) |
| Bitter Lesson | [Compare prompt simplification across simulated model versions](exercises/12-bitter-lesson.md) |
| Calibrate Judge | [Align a judge with labeled outcomes using offline controls](exercises/10-calibrate-judge.md) |
| Adversarial Cases | [Construct controlled challenges with activation and outcome witnesses](exercises/08-adversarial-cases.md) |

The handoff blocks in these files are requests to your coding agent. Copying a skill or running the scripted candidate demo does not mean that skill was exercised by an agent. Keep supplied fixture judgments separate from real decisions you make during an exercise.

## Project map

`support_agent.py` is the editable product. It reads one `{request,state}` JSON object from stdin and emits `{action,account,state,note}`. Its initial bugs confuse a VPN mention with ticket authorization, ignore duplicate tickets, and guess ambiguous accounts.

`evals/spec.json` and `evals/rubric.md` state the synthetic exercise contract. `evals/cases.jsonl` contains eight development and four confirmation cases. `evaluate.py` is the sole project grading path: it checks the action/account, actual resulting ticket membership, original-record preservation, new-ticket fields, and unique IDs. A claim of success does not substitute for the expected state.

`examples/candidates/` contains known example changes for running controls. Inspecting them makes them exposed development material. `exercises/fixtures/verify_claim.py` is an intentionally bad verifier for the audit exercise; it is not the native grader.

Store experiments and user review records under ignored `eval-runs/`. For newly authored cases, use the native JSONL format and a separate file:

```sh
python3 evaluate.py run --candidate support_agent.py --cases evals/generated/password-reset.jsonl --suite development --out eval-runs/password-reset
```

Changing the core suite, rubric, spec, or evaluator establishes a new measurement boundary. Finish or preserve the prior campaign and start a new baseline instead of silently continuing its scores.

## Generation, faults and DSPy

Run `python3 -m methods.run --out eval-runs/methods` for bounded reachable generation, reduction, fault selection and process/subprocess/storage experiments. The [method guide](methods/README.md) covers actual artifacts, budgets, optional pinned DSPy SDK validation and the project-local dataset/metric handoff. [Exercise 09](exercises/09-methods-and-dspy.md) walks through the evidence. Use `--dspy-check` with the SDK environment, including with `scripts/run_cstack_evals.py`, to require the compatibility check. Default runs explicitly report that optional check as not run. The executable code stays in this fixture; skills contain method references only.

## Calibrate a judge offline

Run `python3 -m judge_calibration.run --out eval-runs/judge-calibration` to validate gold/prediction separation, typed/LLM response normalization, kappa and class-error reporting, bounded fixture-policy selection, and final exposure controls. See [the local guide](judge_calibration/README.md) and [exercise 10](exercises/10-calibrate-judge.md). Labels come from native synthetic task outcomes; both judge backends are deterministic simulations. No provider calls or human-calibration result are implied.

## Simplify with offline controls

Run `python3 -m simplification.run --out eval-runs/simplification` for removal dependencies, interaction controls, original-baseline quality gates and a frozen model-by-design comparison. See [the local guide](simplification/README.md) and exercises [11](exercises/11-ablation.md) and [12](exercises/12-bitter-lesson.md). The model effects are explicitly programmed; no provider calls, real prompt-quality measurements or production changes occur.

## Retain review judgments

[Exercise 13](exercises/13-review-calibration-capture.md) checks a scoped capture offer, consent, authority, amendments and a label-isolated calibration handoff. It uses scripted roles only; neither agent verdicts nor expectation approvals become human outcome labels.
