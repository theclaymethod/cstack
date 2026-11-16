---
name: bootstrap
description: Use a Socratic interview to discover the boundaries of a product spec and index the scenarios its evals should cover.
---

# Bootstrap

Follow one user journey. Read the request, trace the workflow, and inspect what existing checks observe. Start the interview with an ordinary example and your best reading of what the user expects to happen.

Change one detail. Pick the variation whose answer would settle the most consequential uncertainty. Ask what should happen in that situation and wait. When the answer surprises you, ask what distinction matters to the developer. Use their answer to choose the next example.

For example, a developer says a note should survive closing the editor. “I type a word and close the tab before autosave fires. What should I see when I reopen it?” If they expect the word back, try a browser crash at the same instant. If losing it is acceptable, ask what the user must see before they can rely on the save.

When two examples deserve different outcomes, identify the condition that separates them. When they deserve the same outcome, look for another meaningful difference or ask where the developer has seen the rule break. Stop probing once another answer would add no distinct eval or the developer chooses to defer it.

Create or update SCENARIOS.md as you learn. State the promise for each workflow. Give each distinct scenario a stable ID, its starting situation, and the observable outcome, including acceptable alternatives. Show the index for correction or approval and mark open boundaries. [Create Eval](../create-eval/SKILL.md) uses the approved entries and links each eval to its scenario ID.
