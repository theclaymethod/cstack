# Reviewing automated changes

At a checkpoint, summarize what each proposed change does, give a before/after case, and flag regressions or uncertainty. Offer these choices:

- **Review now.** The user can accept named changes, request revisions, or decline.
- **Continue.** Keep exploring until the current campaign’s agreed stopping condition, then return for review.
- **Continue for N more rounds.** Count completed search blocks (or attack/repair rounds for Cross-Examine). Stop for review after N, or sooner if the existing budget or stopping rule ends the run.

Honor a cadence the user already chose. The coordinator tracks remaining rounds across workers and resumes; nested skills return their evidence to it. During a batch, a tested candidate can be the next experimental parent. Preserve the approved baseline and record candidates as uncommitted patches or file snapshots with content hashes. Existing scope, budgets, independent review, and human-label requirements still apply.

At the stopping point, review the accumulated changes against the last accepted baseline. **Before creating any Git commit containing a proposed change, obtain explicit user acceptance of that specific change or tested bundle.** This includes local checkpoints, temporary branches, worktrees, forks, and commits made by workers. A request to continue, an automated verdict, a passing score, or silence leaves the changes pending. Keep pending work uncommitted and out of the active target.

Record acceptance against the reviewed content. If the user selects a subset, test that combination; if its behavior differs from what they accepted, present it again. Later edits require fresh acceptance. Commit only accepted content when committing is within scope. Push, merge, or deploy only under the corresponding authority. If nothing changed, report the result without asking for acceptance.
