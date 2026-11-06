# Export findings for eval creation

Use this workflow when the user asks to export or share captured findings, corrections, or rubric criteria. Expert-mode and distill-me use the same handoff. Preparing a local export does not activate live capture or authorize sending, uploading, publishing, or committing source data.

## Select the evidence

Read the established project dataset. Select the requested scope; default to this session's findings when no broader scope was requested. Resolve each example's current state through its amendment history. Keep distinct judgments separate, including unresolved concerns about the same output. Include retractions and superseded definitions as provenance when needed; they are not extra independent eval cases.

Prepare a private `packet.json` using the project's ordinary tools. Adapt existing records into this portable JSON envelope:

```json
{
  "schema_version": 1,
  "examples": [],
  "rubric": [],
  "history": [],
  "artifacts": [],
  "limitations": []
}
```

For each example, preserve the recoverable input/context, original reviewed output/version, explicit label, expert statement and source, endorsed correction or null, applicable criterion IDs/versions and supported answers, unresolved gaps, and capture-time replay readiness. Preserve preferences and tentative observations as such. Golden content, thresholds, and rubric answers remain absent when unsupported. A rubric definition retains its question, passing answer, scope, status, version, and source statement.

Materialize the selected input/output context inside `examples` or `artifacts`. A private path by itself is not a portable replay input. Use bundle-relative or opaque artifact references. Include only the source excerpts needed to establish the judgment; a full transcript, project directory, screenshots, database, or attachment tree is not a default export.

Replace identifying example, item, source, criterion, graph-node, and graph-edge IDs with consistent opaque IDs before sanitization. Preserve the equality and relationships that matter to the task. Keep any reverse lookup and raw source references in the project's private storage, outside the handoff. An exact private quotation becomes a redacted projection after filtering; label that transformation rather than presenting it as unchanged verbatim evidence.

## Remove PII from the separate export

Read [Privacy Filter setup and limits](privacy-filter.md). Use the local model when available, or an already established local redaction process. Inspect nested values, source excerpts, corrections, rubric wording, object keys, IDs, numeric identifiers, URLs, file paths, and selected context. Images and non-text attachments need separate review or omission.

The [export helper](../scripts/export_findings.py) parses JSON and sanitizes values rather than treating JSON serialization as prose. It refuses changed identifier values or field names so redaction cannot silently collapse linked examples or break the schema. Rekey identifying references consistently in the private packet if that happens. It creates a new bundle and preserves capture files.

After setup, run from the working project, substituting the installed skill path:

```bash
TIKTOKEN_CACHE_DIR=.models/tiktoken \
  .venv-privacy-filter/bin/python /path/to/expert-mode/scripts/export_findings.py \
  private-eval-export/packet.json exports/expert-review-001 \
  --checkpoint .models/privacy-filter/original \
  --revision-file .models/privacy-filter.revision --device cpu
```

For a packet already sanitized through an explicitly chosen manual or other local process, the export helper itself needs only standard-library Python:

```bash
python3 /path/to/expert-mode/scripts/export_findings.py \
  private-eval-export/sanitized-packet.json exports/expert-review-001 \
  --already-redacted
```

That flag records that no model scan ran; it does not certify the data. Missing model setup or a failed scan stops the model-backed export, with no automatic raw-data fallback. Use a new destination for each revision.

The bundle contains:

- `findings.json`: the selected examples, rubric, context, and provenance after sanitization.
- `manifest.json`: hashes of exported content, processing method, available model revision, and separate review states. Raw-source hashes, paths, and identity lookups are excluded.
- `HANDOFF.md`: instructions for turning findings into evals without inventing gold answers or treating annotations as independent validation.

## Review privacy and eval meaning

Read back the bundle. Privacy review checks for remaining identifiers, secrets, identifying combinations, and project-specific or clinical identifiers the model may miss. Inspect every selected attachment separately. Eval-intent review checks that masking preserved the failure, correction, units, ordering, relevant dates/intervals, relationships, alternatives, and rubric applicability. For example, replacing two different people with the same placeholder can destroy a relationship test even if their names are hidden.

The helper carries original `replay_ready` into `capture_replay_ready` and clears exported `replay_ready`. A changed context must earn its post-redaction readiness. A supported scoped binary criterion may suffice without a full replacement answer. An uncertain annotation or an unrecoverable original stays incomplete. Use consistent synthetic replacements when needed and record the transformation; obtain expert reassessment if it changes the domain judgment.

Record the completed reviews in `review.json`, tied to the current SHA-256 of `findings.json`, with privacy and intent verdicts, coverage limits, and reviewer provenance appropriate for the audience. A changed bundle invalidates that receipt. Keep raw review notes private if they identify what was removed. Until review is complete, describe the bundle as prepared locally with reviews pending. This is a review step for the requested export, not a repeated approval gate for ordinary capture.

Report the bundle path, what it contains, filtering method, and any remaining gaps succinctly. Send it elsewhere only when the user directs that separate action.
