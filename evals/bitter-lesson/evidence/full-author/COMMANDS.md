The workspace was materialized with:

```sh
python3 work/bitter-lesson-build/frozen/fixtures/playground/scripts/new_workspace.py --source work/bitter-lesson-build/frozen --out work/bitter-lesson-build/runs/full-author
```

From this workspace, the actual authoring/execution sequence was:

```sh
python3 eval-runs/skill-exercise/prepare_handoff.py
python3 eval-runs/skill-exercise/author_cases.py
python3 eval-runs/skill-exercise/run_controls.py
python3 eval-runs/skill-exercise/verify_evidence.py
```

These authoring scripts reproduce the exercise artifacts and should run only in a fresh copy. The native run script refuses existing run paths. Exact native commands and exits are retained in `commands.json`; actual stdout/stderr is in `evidence/`. For a fresh individual native replay, choose a new output directory:

```sh
python3 evaluate.py run --candidate eval-runs/skill-exercise/controls/legitimate.py --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out eval-runs/skill-exercise-replay-legitimate
```

Verification of existing retained evidence (no candidate executions):

```sh
python3 eval-runs/skill-exercise/verify_evidence.py
```

No fixture tests, source modifications, network calls, paid/provider calls or injections were performed. Inspection used the installed skill files, relevant references, native source/spec/rubric/development examples and this task only.
