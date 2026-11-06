---
name: expert-mode
description: Explicit session mode for an expert working with Claude, Codex, Cursor, or another agent. Use when the user invokes /expert-mode to quietly capture review judgments, corrections, and binary rubric criteria as repeatable local evals, with concise evidence-based replies.
---

# Expert Mode

Activate only when the user explicitly invokes `/expert-mode` or requests this mode. Discussing, naming, or configuring the skill is not activation. Stay active for the current session until they stop it. Resume after compaction within that session, but do not reactivate a new session merely because earlier records exist.

For a retrospective pass over an existing session, use [distill-me](../distill-me/SKILL.md); reading that reference does not activate either skill.

The expert keeps doing their work. You assist with the underlying task and quietly preserve their explicit judgments as eval data. This applies across domains, including clinical review, engineering, research, design, and operations. The expert supplies domain judgments; you preserve the evidence and resolve observable implementation facts yourself.

## Begin the session

Briefly restate the expert's goal and explain that explicit errors, corrections, and rubric criteria will be captured. Do not wait for confirmation of a clear goal. Identify the project, reviewed artifacts, existing eval records, and storage conventions from available context.

Reuse the project's local dataset format and location. If none exists, use a small JSONL dataset such as `evals/expert-review/reviews.jsonl`, with `rubric.jsonl` alongside it. State the chosen paths once. If the project or destination is genuinely unclear, ask one short setup question rather than writing into an unrelated directory. Do not place product review data in the skill installation.

Read [the record guidance](references/records.md) before the first write. Establish a session identifier. Carry active mode, dataset paths, relevant example/rubric identifiers, pending questions, and unsaved entries into available compaction summaries or a project-local handoff note. Observe only messages and artifacts available in this workflow. Do not imply that the mode monitors other applications, absent conversations, or work performed outside the agent's context. Do not mine unrelated conversations to infer the expert's intent.

## Capture while the expert works

- **Explicit error.** Save the reviewed item, exact output/version, recoverable inputs, expert's original judgment, and available source references before changing code or regenerating the artifact. An explicit error is worth recording immediately, even without a correction.
- **Correction.** Attach the expert's proposed replacement or required behavior to the same example, including their words, scope, conditions, and reasoning when supplied. A partial correction need not specify the entire expected output. Agent proposals stay separate until the expert endorses them.
- **Uncertainty.** A question or tentative concern is not a confirmed error. Preserve useful unresolved observations with an uncertain label; do not count them as negative examples. Silence, moving on, accepting a code change, or a passing test is not expert approval.
- **Preference.** Distinguish a preference from a factual error. An explicit preference may inform a scoped rubric; one rejected suggestion does not establish a universal rule. Do not manufacture affirmative examples from unremarked work. Capture positive labels when the expert asks for that coverage.

Prefer the raw material over your summary: the original artifact, relevant input/context, expert's words, and the relevant diff or graph relationships. Keep the expert's wording separate from your normalized interpretation. Use the smallest sufficient snapshot or immutable reference. An identifier pointing only to mutable current state is not a reproducible output version. If the original is unavailable, record that gap rather than substituting the fixed output.

A follow-up correction to the same output amends the existing example. A newly generated output is a new version and does not inherit approval. Deduplicate repeated statements and preserve conflicting or revised judgments as linked amendments instead of overwriting history.

## Extract the rubric without inventing it

When the expert states what they check, retain that wording and express clear criteria as separate binary yes-or-no questions. Record each question's passing answer and applicability. A pass can be either yes or no. Preserve conditions, thresholds, exceptions, and acceptable alternatives; leave choices the expert has not made unresolved.

An explicit general rule can be recorded on its first statement. A reusable rule inferred from one correction remains proposed. Repeated consistent examples can justify proposing a broader criterion, but do not silently promote the inference into the expert's confirmed rubric or rewrite their personal skill.

Reference the applicable rubric version from each example. Record an item-level answer only when the expert supplies it or their statement unambiguously answers that exact question. Overall incorrectness does not imply all criteria failed. Distinguish unanswered from not applicable.

## Spend the expert's attention carefully

Ask only when the answer would materially change the label, correction, rubric meaning, or association with the reviewed output. Prefer one short question grounded in their last statement, such as “Is this wrong generally, or only for this input?” Save the established facts first, leave the disputed fields unresolved, and continue independent work.

Before asking, distinguish an expert judgment or preference from an observable fact. Inspect the artifact, read the code, or run an already authorized check for facts you can establish yourself. Do not ask the expert to do those checks for you. Do not introduce a new experiment, medical conclusion, or product decision solely to fill a dataset field.

Use later explicit statements to resolve pending questions. Avoid repeated reminders, questionnaires, and interruptions for optional metadata. The mode is a companion to the work, not a separate annotation interview.

## Write the record, then verify the write

Persist each explicit judgment or correction in the same turn when the destination and evidence are available. Do not wait until session end. Use a JSON serializer for structured text and the project's append/versioning convention. Read back the saved record to confirm it parses, refers to the intended output, preserves the expert's statement, and leaves unsupported values unresolved.

Use stable record and example identifiers, with amendments linked to earlier records. With concurrent workers, keep one dataset writer or separate session files. Subagents can provide artifacts and observations; they cannot supply the human's endorsement. A repeated tool response or capture retry must not create duplicate examples.

If a write fails, say so briefly and retain a clearly marked unsaved entry for recovery. Report saved work only after checking the file. Local files are sufficient; this mode requires no database, service, container, or particular agent-tool API.

## Keep replies succinct and useful

Lead with the answer, finding, or concrete change. Use short sentences and plain language. Include the evidence, uncertainty, tradeoff, or expert decision that changes what happens next. Brevity must not hide a limitation or an unresolved choice. Label inferences where they appear; cite only sources and artifacts actually inspected.

Keep capture acknowledgments unobtrusive, usually at most a short line in the normal reply. Do not recite the schema, rubric, or dataset totals on every turn. Surface a record only when a clarification, correction, conflict, or persistence failure needs attention. Give supporting detail when the expert asks or the decision depends on it. Use lists or tables when they genuinely help comparison, not as a fixed reply template.

Apply the same candor as a good collaborator. Do not agree merely to preserve flow. If observable evidence conflicts with a judgment, explain the conflict and retain the expert's original statement; do not secretly replace their label with your own. Agreement with an agent is not independent validation.

## Export findings on request

When the user asks to export findings for sharing or eval creation, follow [the shared export workflow](references/export.md). Create a separate local handoff containing selected judgments, corrections, versioned rubric, necessary replay context, and unresolved gaps. Apply the referenced local PII filtering and review what masking does to the eval's meaning. Preserve the capture dataset; preparing an export does not send or publish it.

## Preserve the boundary of the mode

Recording is distinct from a replay-ready example. Replay requires recoverable inputs, the reviewed output/version, an explicit label, and an observable acceptance or rejection criterion. A confirmed rubric can provide the criterion without a complete replacement answer. Populated fields alone do not make a golden row. Keep the unresolved blockers visible and do not invent a grader.

Continue the work the user already authorized. Capture does not independently authorize product fixes, new test files, historical transcript mining, uploads, commits, publishing, or permanent changes to personal working rules. Keep sensitive source material within the project's established access boundary; reference existing artifacts when unnecessary copying would expose more context than the eval needs.

On session close or request, summarize what was actually saved, new or revised criteria, unresolved questions, and exact dataset paths. Stop capture when asked, without stopping separately authorized work. On reactivation, resume existing records instead of starting a duplicate dataset.
