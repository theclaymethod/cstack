# Actual command log and replay

Commands ran from this disposable workspace, except the materialization command run from the enclosing build directory. Documentation/skill/source/evaluator reads are not candidate executions.

```sh
python3 work/bitter-lesson-build/frozen/fixtures/playground/scripts/new_workspace.py --source work/bitter-lesson-build/frozen --out work/bitter-lesson-build/runs/full-capture
```

Source preparation copied the review fixture byte-for-byte and serialized the first development case from `evals/cases.jsonl` into `source/first-development.jsonl`. No core input was edited. The exact retained selected case is the reproduction input.

```sh
python3 evaluate.py run --candidate support_agent.py --cases eval-runs/skill-exercise/source/first-development.jsonl --suite development --out eval-runs/skill-exercise/native/original
python3 eval-runs/skill-exercise/driver.py capture
python3 eval-runs/skill-exercise/driver.py stop
python3 evaluate.py run --candidate eval-runs/skill-exercise/source/regenerated.py --cases eval-runs/skill-exercise/source/first-development.jsonl --suite development --out eval-runs/skill-exercise/native/regenerated
python3 eval-runs/skill-exercise/driver.py regeneration
python3 eval-runs/skill-exercise/driver.py merge1
python3 eval-runs/skill-exercise/driver.py merge2
python3 eval-runs/skill-exercise/verify_artifacts.py
```

All commands exited 0. Native receipts retain the actual summary and trace. `driver.py` is an exercise-specific record serializer with source-backed candidate assertions; it is not another evaluator or a model of human expertise. It reads prior JSONL rows, skips stable identities, appends amendments, verifies parseability, and snapshots stages. Candidate execution uses the unchanged native `evaluate.py` exclusively.

To check duplicate behavior now without spending another case execution:

```sh
python3 eval-runs/skill-exercise/driver.py merge2
python3 eval-runs/skill-exercise/verify_artifacts.py
```

The optional repeat writes `merge2-repeat-result.json`, leaving the original checkpoints intact. For a fresh reconstruction, copy `source/` and `native/` into a new directory inside this workspace and invoke driver phases `capture`, `stop`, `regeneration`, `merge1`, `merge2` with `--base` pointing there. Those phases do not execute candidates. To regenerate actual native receipts, use fresh output directories (native runner refuses existing destinations); each native command costs one additional case execution and must be accounted for separately. This exercise did not perform those additional native reruns.
