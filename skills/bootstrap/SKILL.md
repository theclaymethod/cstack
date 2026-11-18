---
name: bootstrap
description: Use a Socratic interview to discover the boundaries of a product spec and index the scenarios its evals should cover.
---

# Bootstrap

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

## Intent interview

Follow one user journey. Read the request, project materials and existing checks first. Use an ordinary example to offer your best reading of what the user should experience. Label hypothetical examples. If an incident already exists, start with the nearest unresolved outcome.

- Find two plausible rules that fit the evidence. Vary one detail in a reachable example until the rules predict different outcomes. Ask which the owner wants. Use the answer to choose the next example.
- State the topic in one sentence. Ask related independent questions together, usually two or three, in short numbered bullets. Keep each example beside its question. Respect the owner's question budget. Wait before asking anything that depends on an earlier answer.
- Give two or three lettered choices. Put your recommendation first and explain its consequence. Accept a custom answer. A recommendation stays provisional until the owner accepts it.
- Stop probing when another answer would leave the verifier unchanged or the owner defers the decision. After the last answer on each major topic, pause. Your next turn is the readback: summarize decisions, assumptions and open questions in short bullets. End with a direct request to confirm or correct that summary and wait. An answer to an interview question is not confirmation of your summary. Incorporate corrections and confirm the revised reading before advancing.
- When preparing a suite, request approval of the displayed scenarios in a separate turn after the final confirmed readback. Keep scenarios that depend on deferred decisions pending.

## Finding a consequential question

Check project materials for facts that could settle an interview question. Research external sources only when a missing fact could change a consequential decision. Report the finding and source beside the decision. Ask the owner to decide product policy, including trade-offs that challenge the initial premise.

If several rules fit the evidence, use the [discovery prompts](references/discovery-prompts.md) to find a small example where their outcomes differ. Ask about that difference before widening the interview.

For example, a developer says a note should survive closing the editor. “I type a word and close the tab before autosave fires. What should I see when I reopen it?” If they expect the word back, try a browser crash at the same instant. If losing it is acceptable, ask what the user must see before they can rely on the save. If the developer is unsure, recommend a rule and walk through what the person reopening the note would experience under each choice.

When two examples deserve different outcomes, identify the condition that separates them. When they deserve the same outcome, look for another meaningful difference or ask where the developer has seen the rule break. Stop probing once another answer would add no distinct eval or the developer chooses to defer it.

## Review scenarios

After the developer confirms the final topic readback, present the scenario index and ask for approval of the displayed entries in a separate turn. Topic confirmation covers the interpretation. Scenario approval covers the reviewed entries.

Carry approvals, corrections and open decisions into the [shared decision ledger](../create-eval/references/decision-ledger.md) at handoff. Create or update SCENARIOS.md as you learn. State the promise for each workflow. Give each distinct scenario a stable ID, its starting situation, and the observable outcome, including acceptable alternatives. When the developer corrects a rule, revise the affected entries in place. Show what changed, which decisions still hold, and which boundary is still open.

Mark scenarios affected by an unresolved decision as pending. Continue with approved scenarios whose expectations are independent of that decision. Hand those entries to [Create Eval](../create-eval/SKILL.md) and link each eval to its scenario ID. Report which scenarios remain pending and what decision will unblock them.
