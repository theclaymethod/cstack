# Find the question that changes the spec

Use these prompts selectively when examples fit more than one rule. Work through them privately and bring the developer one concrete choice.

- **Check reachability and novelty.** “Can someone reach this state through a supported workflow? Which existing guard or check already handles it? What genuinely new outcome remains?” Resolve these from the product before spending an interview turn.

- **Find competing rules.** “What are two plausible promises that would both pass every example we have? Which session detail supports each? What could still be inference?”
- **Find the cheapest distinguishing example.** “Keep the user, action and starting state fixed. What single change makes the promises predict different visible results? Could a saved decision already settle which result is intended?” Prefer the example that resolves the most consequential pending checks with the least effort.
- **Ask from the user’s point of view.** “If this happened, would you expect A or B? Under A this person would experience __. Under B they would experience __.” If the developer is unsure, recommend one with a reason, then leave the check open until they decide.
- **Challenge the proposed proof.** “What wrong behavior could still pass the existing check? Which different but legitimate result must also pass? Could either answer to my question leave the check unchanged?” Drop questions whose answers make no observable difference.
- **Reconcile and stop.** “Which checks did this answer change? Which still stand? What did the owner defer?” Stop when the remaining interpretations imply the same checks, the consequential ambiguity is resolved, or the owner defers it.
