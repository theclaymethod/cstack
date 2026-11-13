# cstack playground

This is the reusable fixture for practicing the current cstack skills, including help and course. In the cstack checkout it lives under `fixtures/playground`. Materialize a disposable workspace with `scripts/new_workspace.py --out <new-directory>` before running agent-led experiments. The support agent and every supplied conversation, case, expected result, and candidate are synthetic fixtures. They establish no human calibration or model-performance claim.

Start with README.md and the relevant exercise. Generated workspaces have copied skills under `.agents/skills`; `.claude/skills` and `.cursor/skills` link to them. Keep their sibling references intact. `scripts/sync_skills.py` updates unchanged installed copies from the owning checkout and refuses to overwrite local skill edits. Canonical fixture source does not contain nested Git metadata or installed skill copies.

`evaluate.py` owns actual candidate execution, deterministic grading, comparisons, and the example campaign ledger. Use its existing commands rather than implementing another evaluator. Candidate programs run with local host permissions; fresh subprocesses and timeouts provide repeatability, not containment.

During a hill-climb campaign, edit only the authorized target (normally `support_agent.py`). Keep `evaluate.py`, `evals/spec.json`, `evals/cases.jsonl`, and `evals/rubric.md` fixed. Changing those files creates a new campaign and baseline. Other exercises may explicitly authorize new cases or a copied verifier; keep those artifacts separate until reviewed.

Put trials, traces, reviews, and campaign outputs in ignored `eval-runs/`. Preserve prior attempts and source records. Human judgments collected during an exercise are scoped to what the user actually reviewed; supplied fixture statements are scripted source material, not live expert approval.

Run `python3 -m unittest discover -s tests -v` for executable project checks. Report development, confirmation, errors, and no-improvement outcomes faithfully. Confirmation fixtures remain available in the repository; their name does not enforce blindness or establish held-out generalization.

For ablation and model-migration exercises, `simplification.protocol` supplies a project-local adapter to the same native grader. Model names denote programmed stand-ins. Keep task/evaluator sources fixed and report prompt-byte savings separately from unmeasured model cost or latency.
