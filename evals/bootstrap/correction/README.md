# Correcting an approved scenario during the interview

The developer establishes four cancellation scenarios on the first turn. On the second turn they reverse one notification decision. One branch changes a single date and another changes an entire series. The co-host rule remains open in both. Each branch starts a fresh Codex session and resumes that same session for turn two.

The runner seeds an empty project table with four named situations. It supplies the skill text, the table vocabulary and the developer messages to the model. Expected cells and the correction map stay in the grader. The runner snapshots the file after each turn and compares every situation and cell with the frozen fixture. It checks both artifacts, so a correct final table cannot hide a wrong first turn. Reordering rows is allowed. Raw chat replies remain in the local run directory.

| Skill source | Single-date correction | Whole-series correction |
| --- | --- | --- |
| Original, 9a65d68 | Pass | Pass |
| Previously published, 0ed7cb1 | Pass | Pass |
| Candidate in this commit | Pass | Pass |

In the first branch only B changed from notify to silent. In the other only C changed from silent to notify. A stayed notify and D stayed open. See the [before](results/candidate/one-date/turn-1.md) and [after](results/candidate/one-date/turn-2.md) files. This is a synthetic development check of recorded decisions. Supplying the row schema makes it unsuitable for scoring independent discovery of scenarios, interview efficiency or natural-language spec design. Both prior versions already handled these corrections.

From the cstack checkout, with the authenticated Codex CLI:

```sh
python3 evals/bootstrap/correction/controls.py evals/bootstrap/correction/case.json
python3 evals/bootstrap/correction/interview.py --case evals/bootstrap/correction/case.json --skill skills/bootstrap/SKILL.md --branch one-date --out /tmp/bootstrap-one-date
```

Use a fresh output directory per run. Repeat with `--branch series`. For an older skill, supply a file exported with `git show REV:skills/bootstrap/SKILL.md`. Manifests record the actual skill, runner, fixture hashes, CLI version and model alias. Each cell in the results table represents one two-turn trial.
