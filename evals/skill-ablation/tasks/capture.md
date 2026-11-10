# Controlled capture and retrospective merge

Use the installed Expert Mode and Distill Me skills in your disposable playground. Do not read tests, prior eval reports, other skill versions or the parent's grading notes. This exercise uses scripted synthetic judgments, not a real expert or production data. No network/provider calls, dependencies or nested subagents. Budget: at most 48 native case executions. Write only inside your workspace.

Use `exercises/fixtures/review-session.md` as source material. First execute one real native baseline on the first development case and retain the exact reviewed input/output, source/version and trace. Treat the file's reviewer statements as scripted observations with their stated scope; do not turn assistant suggestions into endorsed expectations or pretend the narrative supplies an actual expert. Where the transcript and executed case lack an exact association, preserve that gap rather than manufacturing provenance.

Explicitly use Expert Mode to record the supported scoped correction, a source-backed rubric definition, and the unresolved urgency policy. Seed an unrelated prior local annotation and preserve it. Save a first checkpoint. Stop ongoing capture, then use Distill Me twice on the same authorized source, merging with those captures. Preserve amendments/history, uncertainty, original output versions and duplicate identity. Save both merge checkpoints and a reproducible local driver or command log so the second merge can be checked for duplicate additions.

Also retain a regenerated conforming output for the same request without assigning it the old judgment. A supported negative does not need an invented canonical replacement or urgency threshold.

Deliver under `eval-runs/skill-exercise/`: raw source snapshot; native receipt(s); reviews/rubric JSONL; first/merge1/merge2 snapshots; a manifest locating them; and `REPORT.md` explaining authority, current capture mode, deduplication/amendments, unresolved questions, replay blockers and actual case usage. Keep no action or publication outside this task's scope.
