# When the lesson stalls

| Situation | What to do |
| --- | --- |
| Not in a materialized playground | Create one with `scripts/new_workspace.py` into a new directory, or reuse an existing workspace. Do not write into `fixtures/playground`. |
| Doctor reports missing Python or a missing file | Give one setup action and pause live execution. Do not spend the sitting installing a toolchain. You can still show a fixture file and ask the question. |
| `evaluate.py` returns an error | Read the stderr. Record the error separately from a task failure. Preserve the output directory. Do not start a second writer into a directory that may be incomplete. |
| The learner is stuck | Point at one field in the evidence. Then offer a worked contrast if they want it. If they ask for the answer, give it, record `worked`, and invite a new attempt. |
| They move quickly | Shorten the explanation and ask the checkpoint question. Do not skip ahead in `completed`. |
| They say start in a used workspace | Continue from `next_action`, or materialize a new copy. Never delete the used one. |
| The session is interrupted | On return, run status, read the latest event, inspect `changed_or_missing` and `notes_to_reconcile`, then ask the saved question. |
| A file changed since the checkpoint | Show the path and the difference. Ask which version to use. Keep both. Do not treat the old score as a score of the new file. |
| Checkpoint revision conflict | Reread status. Another writer may be active. Stop if a second tutor is editing this workspace. |
| They want the product “fixed” during exercises 01–06 | Capture or measure first. Hill-climb is exercise 07. Do not edit `support_agent.py` early and then describe the baseline as the original bug. |
| A higher aggregate hides a regression | Put the per-case comparison next to the aggregate. The higher number is not the decision. |
| An example candidate was opened | It is exposed development material. Say so. Do not present it as an unseen solution. |
| A role that should be independent is the same session | Mark that part unreviewed. Do not relabel it as independent review. |
| The journal is missing an event or a file will not parse | Copy `eval-runs/tutor/progress` to a sibling folder before any repair. Do not skip the gap and mark later exercises complete. Continue from the last intact event, in a new workspace if the journal is damaged, and carry over only work you both can see. |
| Only `state.json` was copied | It is an unverified summary. Use it as a lead, inspect the files it names, and ask before recording reconstructed progress. Leave the copied summary unchanged. |
| Python cannot run | Append their words, the stage, and the next action to `eval-runs/tutor/progress/manual-notes.md`. Migrate only confirmed notes into a checkpoint once Python runs. |
| End of the sitting | Stop new runs. Save the exact next command or question. A missing receipt stays unfinished. |

Do not delete events, drafts, run directories, or a learner’s edit to recover a clean tree. A failed attempt is part of the record.
