# Offer review judgments as calibration evidence

Use this at review checkpoints when a user corrects an outcome, confirms a label, adjudicates a disagreement or changes a criterion. Adversarial reviews often surface useful signals; their authority and completeness still differ. Reuse [the shared records](records.md), not a second annotation store.

## Offer once, within the actual scope

When retention for calibration is not already authorized, offer a small concrete batch: which artifact/version and criterion, what the user actually judged, where records would be saved, and which items still need labels or context. Keep it about behavior, not serialization. For example:

> I can save your FAIL on vpn-07/v1 for “a ticket was actually created,” with the original input/trace, for later judge calibration. The urgency correction would stay pending because its criterion is unresolved. Save these locally?

Include the proposed interpretation when the source is ambiguous; keep guesses marked as proposals until affirmed. Permission to save does not approve an unreviewed guessed label. Existing explicit judgments need no second label-approval round just to transcribe them.

One coordinator offers and writes; builders/subagents surface candidates to it. Batch at a natural checkpoint rather than interrupting every correction. Continue the authorized review while the offer is pending. Silence is not consent. Respect decline/stop for that scope and avoid repeating an unanswered offer. Reopen only for a new scope or at the user's request.

Active Expert Mode, an explicit extraction request or an existing scoped capture agreement may already authorize recording. Reuse that permission and dataset; avoid duplicate offers/records. Required audit ledgers and authoring decision checkpoints continue under their existing task authority. The new offer concerns additional reusable calibration capture, not permission to do already-authorized task work.

Accepting a bounded offer authorizes those records or the agreed review scope; it does **not** activate ongoing Expert Mode or authorize unrelated session/history capture, uploads, model fitting, paid calls or publication. Record the scope and allow the user to stop it.

## Preserve signal type and origin

| Observed signal | What may be recorded | Calibration consequence |
| --- | --- | --- |
| User judges a specific original output/state on a named criterion | Direct scoped outcome judgment, original quote/source and exact artifact | Potential labeled outcome row when replay evidence is complete. A negative needs no canonical replacement. |
| User approves a scenario, general rule or expected behavior | Intent/criterion decision with exact revision and authority | Requirement or proposed rubric evidence; it does not label unseen outputs. |
| Correction with unclear artifact, criterion or passing direction | Supported source statement plus proposed interpretation and blockers | Incomplete candidate; do not manufacture a verdict or association. |
| Attacker, defender or independent model reviewer supplies a verdict | Agent-authored finding/judgment, actual source and review status | Model evidence, never automatic human gold. |
| Native verifier rejects an output or a repair passes controls | Code-derived observation with verifier/version and traces | Synthetic/deterministic evidence where appropriate; not a human label or approval of every criterion. |
| Agent changes code, a user accepts a repair, or nobody objects | Change/acceptance observation within its real scope | No inferred output labels. Ask only if a consequential label remains necessary. |

Origin is independent of judgment type: a scripted “user” in a fixture is synthetic even if its wording is a direct outcome label. Preserve whether a suggestion was shown before confirmation; human-confirmed suggestions are not independent annotations. Retain conflicting judgments and later adjudication rather than changing labels to improve agreement.

## Save an auditable candidate

After capture is authorized, preserve the recoverable original input/context/state, actual reviewed output or immutable artifact/version/hash, criterion ID/revision/passing direction and applicability, the user's words/source, supported label or unresolved value, authority/origin, construction family/lineage and exposure. Record capture consent scope separately from label authority. Keep unknowns explicit.

Use stable example, artifact-version, criterion and judgment-source identities. Read existing captures first, append amendments/retractions, and deduplicate retries or later Distill Me passes. A repaired/regenerated output gets a new version with no inherited label. Verify saved content; disclose failures and retain unsaved work. Keep originals in the project's approved private location and follow [export review](export.md) for any later sharing.

## Handoff to Calibrate Judge

Row readiness requires recoverable input and original reviewed artifact, a defined applicable criterion and an explicit supported outcome judgment from the declared authority. A useful correction can remain saved while those requirements are incomplete. Readiness for a row does not establish dataset adequacy, human-gold authority or release readiness.

Provide [Calibrate Judge](../../calibrate-judge/SKILL.md) with eligible rows and an explicit incomplete/excluded queue. Keep intent-only, inferred, agent-only, retracted and unsupported labels out of human-outcome supervision; retain their original evidence separately. Honor nonhuman sources only under a separately declared evidence policy, never by relabeling their authority.

Use resolved current annotations while preserving history. Group original/repaired/derived examples by source family and retain prior exposure. Adversarially selected corrections are ordinarily exposed development material, not an independent final set. Do not automatically promote captured records into a released dataset or assign them an unseen partition.

Judge runtime inputs contain only permitted task evidence. Captured verdicts, rationales, source/label-bearing identifiers and decision metadata stay with the comparator/fitting records. Dataset assembly and adapters remain project-local; this guide neither defines a new universal schema nor bundles a capture runtime.
