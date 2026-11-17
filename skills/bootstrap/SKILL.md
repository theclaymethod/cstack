---
name: bootstrap
description: Use a Socratic interview to discover the boundaries of a product spec and index the scenarios its evals should cover.
---

# Bootstrap

Follow one user journey. Read the request, trace the workflow, and inspect what existing checks observe. Start the interview with an ordinary example and your best reading of what the user expects to happen.

Check project materials first for facts that could settle an interview question. Research external sources only if a fact is still missing and could change a consequential decision. Report the finding and its source beside the decision. Ask the developer to decide product policy.

Choose the first question from the opening. If the developer gave only the ordinary behavior, offer a plausible boundary and ask what they worry could happen. With no traces, label the example hypothetical. If they already described the incident, use it to ask about the nearest unresolved outcome. Vary one detail at a time. Ask what should happen and wait. When the answer surprises you, ask what distinction matters to the developer. Use their answer to choose the next example.

## Interview rounds

- State the current topic in one sentence. Use short bullets, active voice, and one idea per sentence. Keep the example visible beside the decision.
- Group related independent questions in the same round, usually two or three. Number the questions. Respect an explicit question budget. Ask dependent questions after their prerequisites are answered.
- Give each decision two or three distinct choices. Put the recommended choice first and explain its consequence briefly. Accept a custom answer. The developer can reply with question numbers and option letters. Recommendations remain proposals until accepted.
- Use the available context to propose a coherent policy for revision. Ask when an unresolved choice changes what an eval should accept. Challenge the product premise when it exposes a consequential conflict. Spend other questions on intended behavior.
- After each major topic, read back a short bullet summary for confirmation or correction. Distinguish confirmed decisions, inferred assumptions, and open questions. Apply corrections before the next topic. Preserve unanswered questions without repeating settled decisions. A topic confirmation covers only the displayed summary. Scenario approval still applies to the reviewed entries.

If several rules fit the evidence, use the [discovery prompts](references/discovery-prompts.md) to find a small example where their outcomes differ. Ask about that difference before widening the interview.

For example, a developer says a note should survive closing the editor. “I type a word and close the tab before autosave fires. What should I see when I reopen it?” If they expect the word back, try a browser crash at the same instant. If losing it is acceptable, ask what the user must see before they can rely on the save. If the developer is unsure, recommend a rule and walk through what the person reopening the note would experience under each choice.

When two examples deserve different outcomes, identify the condition that separates them. When they deserve the same outcome, look for another meaningful difference or ask where the developer has seen the rule break. Stop probing once another answer would add no distinct eval or the developer chooses to defer it.

Carry approvals, corrections and open decisions into the [shared decision ledger](../create-eval/references/decision-ledger.md) at handoff. Create or update SCENARIOS.md as you learn. State the promise for each workflow. Give each distinct scenario a stable ID, its starting situation, and the observable outcome, including acceptable alternatives. When the developer corrects a rule, revise the affected entries in place. Show what changed, which decisions still hold, and which boundary is still open. Show the index for correction or approval.

Mark scenarios affected by an unresolved decision as pending. Continue with approved scenarios whose expectations are independent of that decision. Hand those entries to [Create Eval](../create-eval/SKILL.md) and link each eval to its scenario ID. Report which scenarios remain pending and what decision will unblock them.
