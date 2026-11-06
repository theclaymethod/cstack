# Eval author handoff

Use findings.json as evidence for constructing evals. One example is one specific
expert judgment. Preserve uncertainty, preferences, retractions, criterion versions,
and expert-endorsed alternatives. History is provenance, not extra independent rows.

Review privacy and intent separately. Confirm that masking preserved the failure,
correction, units, relationships, conditions, and applicability. Keep a changed or
incomplete example provisional. Capture readiness is not post-export readiness.

Materialized input/output context and an observable criterion are required for a
repeatable task. A scoped binary criterion can suffice without a full replacement.
Do not infer gold answers, numerical tolerances, endorsements, or population claims.

After local review, save review.json referencing findings.json's current SHA-256,
with privacy_review and intent_review verdicts, unresolved limits, and reviewer
provenance suitable for the intended audience. Recheck if the file changes. The
manifest records processing, not a guarantee of anonymization or permission to share.
Keep raw sources and any identity lookup outside the bundle. Sharing is a separate
user-directed action; this tool only writes local files.
