# Distill Me: recover scoped judgments

Use the session from Expert Mode, then invoke `$distill-me`. Ask the agent to merge the same evidence twice and inspect whether stable examples are duplicated or prior records disappear.

For a standalone fixture exercise, use `exercises/fixtures/review-session.md`. Its statements are scripted synthetic sources, not a live expert conversation or real human gold. Ask the agent to preserve that weaker authority and any missing execution context.

Handoff:

> Use Distill Me on the current session's judgments. Preserve exact source scope, uncertainty, and earlier records. If using the supplied review-session fixture instead, identify it as scripted source material and keep unsupported real-expert or replay-readiness claims provisional. Run the merge again and show whether it added a duplicate.

Completion: corrected account/duplicate behavior remains distinct from unresolved urgency policy; the agent's own suggestion is not promoted into a user judgment; repeated extraction preserves earlier history without duplicating the resolved examples.
