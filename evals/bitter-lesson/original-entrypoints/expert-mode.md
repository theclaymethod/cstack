---
name: expert-mode
description: Capture expert judgments, corrections, and binary rubric criteria as local eval data throughout a session. Activate only on explicit /expert-mode invocation or a request for this mode. Keep replies concise.
---

# Expert Mode

Activate only when asked. Discussing or configuring the skill does not activate it. Stay active until stopped, including after compaction in this session. A new session needs a new invocation. For retrospective capture, use [Distill Me](../distill-me/SKILL.md).

## Start quietly

Reuse the project's dataset and storage conventions. Otherwise use local JSONL, such as `evals/expert-review/reviews.jsonl` and `rubric.jsonl`. State the paths once. Ask one setup question if the project or destination is unclear.

Read [the shared record guidance](references/records.md) before writing. Carry the active mode, session ID, paths, record IDs, pending questions, and unsaved entries through compaction. Observe only the available, authorized conversation and artifacts. This mode does not monitor other applications or search unrelated history.

## Capture judgments as they happen

Save the input, original reviewed output/version, expert's words, and source references before repairing or regenerating anything. Use a snapshot or immutable reference. If the original is missing, record the gap rather than substituting the fixed result. Keep the expert's wording separate from your interpretation.

- Record an explicit error immediately, even without a correction. Preserve partial corrections and their scope. Agent proposals become expected answers only when the expert endorses them.
- Keep tentative concerns uncertain and preferences distinct from factual errors. Silence, a code change, a passing test, or an agent's agreement does not establish expert approval. Capture positive examples when requested.
- Amend judgments about the same output. A regenerated output is a new version and inherits no approval. Link revisions, conflicts, and retractions instead of overwriting history or counting repeats as new examples.

## Preserve the rubric

Turn stated criteria into separate binary questions. Retain the original wording, passing answer, applicability, conditions, thresholds, exceptions, and acceptable alternatives. Either yes or no can mean pass. Persist unclear formulations as proposed before asking about them.

An explicit general rule can be recorded immediately. Broader rules inferred from corrections remain proposals until endorsed. Reference criterion versions, and assign item-level answers only when the expert's statement supports them. Overall incorrectness does not mean every criterion failed. Keep unanswered and not applicable distinct.

Ask occasional short questions when the answer changes a label, correction, criterion, or output association. Save known facts first and continue independent work. Inspect observable facts yourself with authorized tools. Do not invent experiments or domain decisions to complete a row.

## Save and verify

Write supported observations in the same turn. Use stable IDs, a serializer, and the project's amendment convention. Read the saved records back to verify parsing, source wording, output association, and unresolved fields. Use one writer or separate session files for concurrent work. Retries must not duplicate captures.

If saving fails, disclose it and retain a marked unsaved entry for recovery.

A captured observation becomes replay-ready only with recoverable input, the reviewed output/version, an explicit label, and an observable acceptance or rejection criterion. A supported criterion can suffice without a complete replacement answer. Preserve useful incomplete entries and their blockers.

## Keep the work moving

If evidence conflicts with an expert judgment, explain it while preserving their original label.

On close or request, report saved paths, meaningful rubric changes, unresolved questions, and write failures. Stop capture when asked while continuing separately authorized work. Reactivation reuses existing records.

Export only when requested, following [the shared export workflow](references/export.md), including local PII filtering and review of whether redaction preserves eval meaning. Preserve private originals. Preparing an export does not send or publish it.

Capture adds no authority to fix products, create test files, mine history, commit, upload, publish, or change standing personal rules. Keep sensitive evidence within the project's access boundary.
