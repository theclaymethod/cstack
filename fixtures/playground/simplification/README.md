# Offline ablation and migration controls

Run in a disposable playground workspace:

```sh
python3 -m simplification.run --out eval-runs/simplification
```

The command exercises `/ablation` and `/bitter-lesson` mechanics using the existing native evaluator. It needs only the standard library and makes no provider calls. Choose a new output directory; an existing run is preserved.

## What is simulated

The adapter renders a prompt from named units and embeds that actual text into a standalone candidate. The protected unit contains the complete native task contract. Fresh native subprocesses receive only real request/state payloads and emit actual support-agent outputs. `evaluate.py` grades those outputs and resulting state; the adapter does not introduce another grader.

Both model names, `old-fixture` and `new-fixture`, refer to programmed Python stand-ins. They use the conforming support implementation plus explicit responses to synthetic prompt cues. The old stand-in needs a legacy authorization reminder; the new one does not. Both need one of two duplicate reminders. Two fabricated compensating cues also exercise a pair-removal interaction. Planning material and an example supply removable noise; a planning detail depends on its parent. These behaviors are deliberately encoded controls, not measured properties of LLMs. The complete task and conforming algorithm are available to the processes.

The command runs a fixed diagnostic/search schedule rather than learning an optimizer. It establishes conditional removal effects, checks a combined candidate, and rejects the union of independently harmless deletions when it loses duplicate handling. It also demonstrates a group deletion that succeeds where single deletion fails.

## Evidence and accounting

The declared finite-case policy is zero observed pass regressions and zero quality loss against the original baseline. Burden is retained-unit count and rendered prompt UTF-8 bytes. No tokenizer, model usage, production latency savings, statistical non-inferiority or generalization is measured.

The driver reserves 20 confirmation case executions within a 200-case total budget. Its current schedule executes 164 native cases, including those 20 final cases. It freezes five exact final configurations before confirmation and closes fitting. Four configurations form a model-by-design matrix; the fifth confirms the old-model reduction. The same simplified prompt is used in both model rows. Existing runs, out-of-plan final calls and post-freeze edits are refused. Interrupted attempts stay charged. This is a one-shot protocol with no resume loader.

Read `results.json`, `contract.json`, `state.json`, and `native/executions.json`. Per-run directories retain immutable candidate snapshots, exact cases, stdout/stderr, native verdicts and source manifests. Completed evidence hashes and source identity are checked before comparisons. These checks detect drift; the processes have host permissions and this is not adversarial filesystem containment.

The selected artifact and diff are **offline fixture programs**, not a deployable production prompt. Confirmation cases remain readable, so confirmation checks workflow separation rather than unseen performance. Running the script also does not prove an agent followed either skill; use the separate exercises for agent-led work.

## Project-local adapter

For independent experiments, use `Experiment`, `configuration`, and `UNITS` from `simplification.protocol`. Start an `Experiment` in a new directory with a bounded `limit` and `confirmation_reserve`. `measure(label, config)` executes development cases; `compare(original, candidate)` applies the original-baseline finite policy. Lower burden is a separate selection decision.

`configuration(model, retained_units)` rejects unknown/duplicate units, removal of the protected contract and surviving dependents without parents. `freeze({label: config, ...})` declares exact final membership. `confirm(label)` runs that frozen configuration on confirmation cases; `finish()` requires all planned final executions to complete. Comparisons remain available after finish, while fitting stays closed. `quality_gate` also supports an explicitly supplied finite loss margin for policy tests; it does not compute statistical intervals.

Adapt these interfaces to a real project's model client, context assembly, usage accounting and sampling policy before making real-model claims. Keep implementations and dependencies local to that project.
