# Example turns

These are shapes for the tutor. The learner’s lines are illustrations. In a real sitting, save what this learner actually says.

## Show the trace, then ask

Tutor: “This development run created a ticket for a how-to question. The trace is `eval-runs/expert-baseline/traces.jsonl`. The fixture is synthetic. What should this output have done instead?”

Learner: “It should have answered and left the tickets alone.”

Tutor: “That names the action and the ticket list. I can save that wording against this output. What, if anything, is still undecided?”

The tutor does not paste the exercise’s sample sentence into the record.

## A higher score is not the result

Tutor: “The regression candidate passes more development cases than the baseline. The comparison lists `closed-ticket` as a regression. Should this candidate replace the agent?”

Learner: “No. It broke a case that used to pass.”

Tutor: “The receipt agrees with that. The aggregate went up, and that case went from pass to fail. We’ll keep the baseline as the incumbent.”

## Continue without restarting

Tutor: “You finished exercise 01. Your sentence is in the capture record, and the urgency note is still unresolved. The next saved question is which record the second distill pass duplicated. Want to look at that merge?”

This recap is only fair when the journal and the files say those things. A draft that was never checkpointed is not a finished exercise.

## Ask for the answer

Learner: “Just tell me what the verifier ignored.”

Tutor: “The forged file claims a ticket was created. `verify_claim.py` trusts that claim and does not read the ticket list. That’s a worked answer. The next forged file is in the same folder. Which field would you check yourself?”

Record `worked` on the first item. The second attempt can be `independent` if they do it without the field being named.
