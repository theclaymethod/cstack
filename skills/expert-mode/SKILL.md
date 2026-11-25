---
name: expert-mode
description: Capture explicit expert judgments, corrections, and binary rubric criteria as local eval records throughout a working session. Activate ONLY on explicit /expert-mode or $expert-mode invocation or an explicit request to start this mode; never trigger implicitly. Keep replies concise.
---

# Expert Mode

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

When the expert corrects an output, capture the specific behavior they judged and the reason they gave. Leave unstated reasons open. Activate only on explicit request; installing skills, discussing capture, or configuring hooks does not activate capture. Stay active through compaction until stopped. A new session needs a new invocation. [Distill Me](../distill-me/SKILL.md) is retrospective and leaves this mode unchanged.

## Execution architecture

- **Inline live capture:** Keep observation and same-turn persistence in the active session under one writer (or separate concurrent files) so capture does not interrupt authorized work.
- **Opt-in session-gated hooks:** To avoid relying on model memory across turns or compaction, projects may configure optional local lifecycle hooks under [hook guidance](references/hooks.md). Hooks must stay dormant unless the current session has an explicit active marker.
- **Isolated export review:** For requested sharing, run a fresh read-only reviewer subagent on the redacted bundle only (never private source) to check PII and eval meaning under [export review](references/export.md). Without subagents, review inline and disclose source exposure; see [harness mapping](../run-eval/references/harnesses.md).

## Capture contract

When handing an authorized capture to another skill, put its permitted record pointer in the [shared decision ledger](../create-eval/references/decision-ledger.md). Keep the reviewed data in its capture store. Use the project's dataset or local JSONL. Read [record guidance](references/records.md) before writing; preserve session/path/record identities and pending or unsaved work through compaction. Observe only supplied or authorized conversation/artifacts.

Save the recoverable input, original reviewed output/version, expert's exact words and source before any repair. Keep interpretation separate. Missing originals stay missing; a regenerated output is a new item with no inherited approval.

Record explicit errors immediately, even without a correction. Preserve partial corrections and their scope. Tentative concerns remain uncertain; preferences are not factual errors. Agent suggestions, agreement, silence and passing checks supply no expert approval. Capture positive examples when requested.

Represent stated criteria as versioned binary questions with passing direction, applicability, thresholds, exceptions and alternatives. Either yes or no may pass. An explicit general rule needs no repetition; inferred rules remain proposals. Save unresolved formulations before asking. Assign item answers only where supported; overall failure does not fail every criterion, and unanswered differs from inapplicable.

## Persist and continue

Write supported observations in the same turn. Append linked amendments/retractions, preserve history and deduplicate retries. Read saved records back for wording, provenance and output association. Use one writer or separate concurrent files. Failed writes remain disclosed, recoverable unsaved entries.

Replay readiness needs recoverable input, original reviewed version, an explicit judgment and an observable criterion; a negative need not have a complete replacement answer. Keep useful incomplete records with blockers.

Ask only for decisions affecting the record; continue other authorized work. If evidence conflicts with a judgment, preserve its source while explaining the conflict. Report paths, unresolved questions and failures briefly. Stop capture when asked (clearing any session hook marker); reactivation reuses history.

Capture stays local unless you request an export and separately direct sharing. For requested sharing, follow [export and privacy review](references/export.md), preserving private originals and eval meaning. Capture itself authorizes no product change, unrelated-history search, publication or upload.
