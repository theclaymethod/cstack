---
name: expert-mode
description: Capture expert judgments, corrections, and binary rubric criteria as local eval data throughout a session. Activate only on explicit /expert-mode invocation or a request for this mode. Keep replies concise.
---

# Expert Mode

Capture explicit judgments during the authorized work. Activate only on explicit request; discussion/configuration is not activation. Stay active through compaction until stopped. A new session needs a new invocation. [Distill Me](../distill-me/SKILL.md) is retrospective and leaves this mode unchanged.

## Capture contract

Use the project's dataset or local JSONL. Read [record guidance](references/records.md) before writing; preserve session/path/record identities and pending or unsaved work through compaction. Observe only supplied or authorized conversation/artifacts.

Save the recoverable input, original reviewed output/version, expert's exact words and source before any repair. Keep interpretation separate. Missing originals stay missing; a regenerated output is a new item with no inherited approval.

Record explicit errors immediately, even without a correction. Preserve partial corrections and their scope. Tentative concerns remain uncertain; preferences are not factual errors. Agent suggestions, agreement, silence and passing checks supply no expert approval. Capture positive examples when requested.

Represent stated criteria as versioned binary questions with passing direction, applicability, thresholds, exceptions and alternatives. Either yes or no may pass. An explicit general rule needs no repetition; inferred rules remain proposals. Save unresolved formulations before asking. Assign item answers only where supported; overall failure does not fail every criterion, and unanswered differs from inapplicable.

## Persist and continue

Write supported observations in the same turn. Append linked amendments/retractions, preserve history and deduplicate retries. Read saved records back for wording, provenance and output association. Use one writer or separate concurrent files. Failed writes remain disclosed, recoverable unsaved entries.

Replay readiness needs recoverable input, original reviewed version, an explicit judgment and an observable criterion; a negative need not have a complete replacement answer. Keep useful incomplete records with blockers.

Ask only for decisions affecting the record; continue other authorized work. If evidence conflicts with a judgment, preserve its source while explaining the conflict. Report paths, unresolved questions and failures briefly. Stop capture when asked; reactivation reuses history.

For requested sharing, follow [export and privacy review](references/export.md), preserving private originals and eval meaning. Capture itself authorizes no product change, unrelated-history search, publication or upload.
