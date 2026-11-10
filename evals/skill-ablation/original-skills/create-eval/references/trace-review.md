# Local trace review

Use the project's existing trace viewer when it already exposes the necessary evidence. For a custom domain view, use [build-review-interface](ecosystem.md). For a small early-development batch, this pack includes a local Python 3.10+ reviewer with no third-party dependencies, database, Docker, or model API.

## Launch

Run from the working project, using the actual installed skill path:

```bash
python3 /path/to/skills/create-eval/scripts/review_traces.py \
  eval-runs/feature/traces.jsonl \
  --reviews eval-runs/feature/reviews.jsonl \
  --reviewer 'Reviewer name'
```

Open the URL printed by the command. It binds only to `127.0.0.1`, chooses a free port, and uses a per-launch access token. No browser opens or data uploads automatically. Keep the terminal running while reviewing; Ctrl+C stops it. Restart with the same paths to resume saved reviews. Use one server per review file. The loaded trace file is a snapshot: restart after adding or changing traces.

Review input and output together; expand context, references, messages, tool events, and run provenance. The default renderer shows text literally and nested JSON as expandable fields. It does not render active HTML, fetch images, resolve artifact paths, or draw a clinical graph. Adapt the UI when judgment needs tables, graph topology, diffs, or images. Keep primary evidence prominent and full available evidence accessible; do not replace source detail with a score.

Add an observation with its scope, reviewer, optional verdict, notes, correction, and proposed rubric questions. **Save review** persists it to local disk; **Save and next** advances after successful persistence. Changes are not auto-saved. Navigation prompts before discarding unsaved edits. Use **Add another observation** for a separate claim in the same output. Editing a saved observation appends an amendment; it does not erase the earlier record. Reviewer names are self-reported, not identity verification.

This is a discovery and review surface, not a blinded evaluator. It displays all fields in the supplied file. Give it only the permitted selected development traces, excluding reserved test sets and private calibration labels. A collapsed field is still exposed. Keep sampling and split selection outside the viewer.

## Trace contract

One JSON object per line. Required: unique string `id`, `input`, and either `output` or `error`. Input/output may be text or structured JSON. Include the actual available evidence; omit unavailable fields rather than fabricating them.

Useful optional fields:

| Field | Meaning |
| --- | --- |
| `scenario_id`, `family` | Stable scenario and related construction family; repeated attempts are not independent sources. |
| `input_origin` | For example `synthetic`, `expert-authored`, or `production`; do not infer from execution. |
| `execution_kind` | For example `actual-product`, `partial-product`, `mocked`, or `handwritten`; name simulated boundaries. |
| `feature`, `revision`, `config` | Actual feature/implementation/configuration identity; unavailable facts stay null. |
| `context`, `reference` | Permitted documents, source excerpts, fixtures, and expected task content needed for review. |
| `messages` | Available conversation messages with roles and content; preserve observable tool calls/results. |
| `events` | Other observable steps, tool arguments/results, retrievals, or failures; use call IDs to connect related events. |
| `state_before`, `state_after` | Relevant state for side-effect criteria, or durable references and hashes with replay instructions. |
| `started_at`, `duration_ms`, `attempt` | Actual measured run facts when available. |
| `unavailable` | Missing evidence or unimplemented stages that limit judgment. |

Preserve provider-native traces when converting them, and record the source mapping locally. This schema is an optional review projection, not a replacement telemetry standard. Capture at the product execution boundary so a real result or error is retained even when grading fails. A separate append-only event stream may be appropriate for long-running attempts; finalize its review projection without discarding partial runs. Never invent hidden internal reasoning.

## Review history and eval handoff

Every saved event records a unique `record_id`, stable `review_id`, prior record in `amends`, time saved, reviewer, trace ID, canonical trace SHA-256, input snapshot SHA-256, scope, verdict, notes, correction or null, and rubric question proposals. `PASS`/`FAIL` apply only to that saved scope. `DEFER` is uncertainty. `UNREVIEWED` means an observation without a decided verdict. The saved time is not a fabricated original judgment time.

Resolve the latest amendment per `review_id`, then match its trace ID **and hash**. Older reviews of changed outputs remain history, not labels for the new result. The UI shows saved observations only for the matching trace version. Proposed rubric questions have no confirmed passing answer or applicability. A typed correction is reviewer input; preserve who supplied it and do not assume another expert endorsed it.

The coding agent can read both JSONL files directly. To promote a record, use [from findings to cases](from-findings.md): verify reviewer authority, scope, recoverable evidence, current verdict, and the acceptance/rejection boundary. Merge session captures by the actual trace version and assertion, not by note wording. Keep incomplete records and disagreements visible. Do not train on observation-only or deferred entries as negatives, silently turn proposed questions into confirmed criteria, or treat every saved note as an independent eval.

Keep these local files in the project's private artifact location. For sharing, use [the export workflow](../../expert-mode/references/export.md), including a selected projection, privacy review, and eval-meaning review. The viewer itself performs no PII filtering and no export certification.
