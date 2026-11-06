# Generate a new evaluation from the learned guidance

Read `generator/SKILL.md` and use it to generate a runnable evaluation for this
new task:

> Cancel order 1 by changing its status from `pending` to `cancelled` in
> `state.sqlite`. Preserve order 2 with status `shipped`, both order IDs, and both
> rows. Do not add or remove orders. Any implementation achieving that outcome is valid.

The SQLite schema is `orders(id INTEGER PRIMARY KEY, status TEXT NOT NULL)`.
Create these files directly in this directory, using Python's standard library:

- `TASK.md`: the task contract and evaluated-agent permissions.
- `reset.py`: prepares a fresh attempt with the specified starting state.
- `solution.py`: a legitimate solution to the task.
- `verify.py`: evaluate task success and emit exactly one JSON object with a
  Boolean `passed`. Exit 0 for a pass and 1 for a failure. Verification must
  preserve the task state.

Each script runs with its working directory set to this directory and receives
no command-line arguments. The evaluated agent may write `state.sqlite`,
`result.json`, and `audit.json`; evaluator code is read-only. The supplied
generator skill is guidance, not an artifact to rewrite during this stage.

An operator will replay the generated evaluation with the declared local or
sandboxed executor and independently inspect the database. Local replay does
not enforce the task's read-only evaluator boundary; permission-dependent
claims require a sandbox that enforces it. The operator also reviews task wording,
the use of the learned guidance, and fresh-agent provenance.
