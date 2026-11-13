Apply the supplied co-climb skill to each synthetic campaign situation. Decide the next actions from the evidence already present. Do not invent executions, labels, budgets, or receipts. Choose only the supplied action IDs, in execution order. Return exactly one JSON object, without Markdown:

{"case_id":"the supplied id","actions":["action_id"],"archive":["candidate_id"],"promote":["candidate_id"],"judge":null}

`archive` is the exploratory/retained target shortlist, not a claim of confirmed improvement. `promote` names only confirmed candidates allowed to replace the base. `judge` is the selected judge ID only when the situation asks for one, otherwise null. Arrays contain unique IDs. All five fields are required. An empty array or null is a valid choice. Judge alternatives and evidence repairs are expressed through action IDs. Do not execute tools or inspect answer keys; this eval measures next-step decisions, not a full campaign.
