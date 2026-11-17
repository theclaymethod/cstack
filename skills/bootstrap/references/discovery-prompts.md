# Find the question that changes the spec

Use these prompts selectively when examples fit more than one rule. Work through them privately. Present concrete multiple-choice decisions, grouping related independent questions within the interview's question budget.

- **Check reachability and novelty.** “Can someone reach this state through a supported workflow? Which existing guard or check already handles it? What genuinely new outcome remains?” Resolve these from the product before spending an interview turn.

- **Find competing rules.** “What are two plausible promises that would both pass every example we have? Which session detail supports each? What could still be inference?”
- **Find the cheapest distinguishing example.** “Keep the user, action and starting state fixed. What single change makes the promises predict different visible results? Could a saved decision already settle which result is intended?” Prefer the example that resolves the most consequential pending checks with the least effort.
- **Ask from the user’s point of view.** “If this happened, would you expect A or B? Under A this person would experience __. Under B they would experience __.” Recommend one with a reason and allow a custom answer. Leave the check open until they decide.
- **Challenge the proposed proof.** “What wrong behavior could still pass the existing check? Which different but legitimate result must also pass? Could either answer to my question leave the check unchanged?” Drop questions whose answers make no observable difference.
- **Reconcile and stop.** “Which checks did this answer change? Which still stand? What did the owner defer?” Stop when the remaining interpretations imply the same checks, the consequential ambiguity is resolved, or the owner defers it.

## Example round

Topic: the refund agent's authority. These are proposed policies, not established requirements.

1. **Which error should the agent prioritize preventing?**
   - **A — recommended:** Prevent incorrect refunds. Escalate uncertain requests, even if legitimate refunds take longer.
   - **B:** Prevent rejected legitimate refunds. Allow more refunds when eligibility is uncertain.
2. **Who can change the refund policy?**
   - **A — recommended:** An authorized operator must approve policy changes.
   - **B:** The agent can change the policy within limits that the owner defines.

Accept a custom answer to either question. Ask about automatic refund limits after the error priority is settled. After this topic, read back the chosen policies and any remaining assumptions for confirmation.
