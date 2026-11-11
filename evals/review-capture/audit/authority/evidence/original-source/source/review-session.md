# Scripted review session

This is a synthetic conversation fixture. The listed “reviewer” is a role in a test case, not a real expert or the current user. No actual run receipt is supplied by this document alone.

1. Agent: “For request `VPN setup guide`, the assistant reports that it opened a ticket.”
2. Reviewer: “For that how-to request, opening a ticket is wrong. Give guidance and leave existing tickets unchanged.”
3. Agent: “Then every VPN problem should get guidance only.”
4. Reviewer: “That does not follow. An explicit ticket request for a clear account should create a ticket unless an open VPN ticket already exists for that account.”
5. Agent: “I suggest urgent requests should always bypass clarification.”
6. Reviewer: “I have not decided the urgency policy.”
7. Reviewer: “For an account-specific duplicate check, an unrelated account's ticket must not block the requested new ticket.”

The rejected generalization, the agent suggestion, and the unresolved policy must remain distinct from the reviewer's scoped statements. Replay readiness requires actual input/output/state and criterion evidence beyond this narrative.
