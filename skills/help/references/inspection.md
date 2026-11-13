# What Help inspects

The inspector reads the working tree and skips `.git`, `.agents`, `.claude`, `.cursor`, `node_modules`, `.venv`, `__pycache__`, and installed `skills/` copies. It does not execute candidates, write files, or upload anything. A cstack checkout (root `plugin.json` named `cstack`, with `skills/` and `fixtures/playground`) is classified before the scan, so pack history under `evals/` is not treated as the user's campaign.

| Artifact | Recognized by |
| --- | --- |
| Run receipt | A directory with `manifest.json`, `summary.json`, and `traces.jsonl`, when the manifest has `cases_source.sha256`. |
| Stale receipt | That manifest's `cases_source` hash, or an `identity.files` hash, differs from a file that still exists in the workspace. A changed candidate alone is not staleness; hill-climb is supposed to edit the target. |
| Untrustworthy newest receipt | The newest receipt is stale, `complete` is false, or its `UNKNOWN` count is above zero. |
| Campaign | `contract.json` with `identity.files`, next to `state.json`. |
| Incompatible campaign | One of those identity files exists and its hash differs. |
| Active campaign | `state.status` is `active`, or an attempt status is not `complete`. |
| Ledger | A markdown file whose name contains `LEDGER`. |
| Open ledger | A line `status:`, `review:`, or `validation:` set to open, unreviewed, unverified, or pending, or a task checkbox `- [ ]`. |
| Bootstrap pending | JSON under `eval-runs/`, or a path containing `bootstrap`, with `cards`, `scenarios`, or `pending` items whose status is pending or deferred. |
| Expert record | A JSONL row in the first 200 lines with `example_id` or `record_id`. |
| Replay-ready row | That row also has a criterion id, an input or output, a non-empty judgment that is not uncertain or proposed, and no `unresolved` or `replay_blockers` list. |
| User cases | A JSONL row with an id and `expected`, `request`, or `input`. The playground's shipped `evals/cases.jsonl` does not count. |
| Judge needed | A config or spec with a non-empty `checks.judge` list, or a judge-calibration directory that has no `results.json`. |
| Judge done | `results.json` inside a `judge-calibration` or `judge_calibration` directory, or beside `fitting.json`. |
| Adversarial set | An `eval-runs` directory named `case-build`, or JSON there with both `activation` and `outcome`. |
| Ablation | An `eval-runs` directory named `ablation` or `simplification` containing `state.json`, `results.json`, or a `selected*` file. |
| Model migration | JSON under `eval-runs` with `old_model` and `new_model`, or both the strings `old-fixture` and `new-fixture`. Incomplete when `complete` is false, `missing_cells` is non-empty, or neither `complete: true` nor a `selected`/`selection` field is present. |
| Course | `eval-runs/course/progress/state.json`, or event files when the summary is missing. |

The playground's shipped spec, rubric, and core cases are the fixture. User work is anything in the table above that is not that shipped case file. `workspace_kind` is `cstack-checkout`, `canonical-playground` (no `.cstack-source.json`), `playground`, or `project`.
