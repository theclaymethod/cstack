---
name: author-short-tutor
description: Create or revise a short, agent-led course for one learner. Interview the course owner, research and agree on the teaching approach, verify the tutor statechart, then author focused exercises for a one-hour experience.
---

# Author a short tutor

Deliver a tutor someone can start with “teach me.” Give it a concrete opening example, materials it can show immediately, and a finish the learner can recognize. Match the host project's existing course format. An outline alone leaves the next tutor to invent the actual lesson.

## Interview the course owner before drafting lessons

Use the grilling skill when available. Map the decisions that depend on one another. Research facts yourself. Inspect the existing tutor, fixtures, and primary references; try a representative exercise. Present the credible sources by name, the specific idea each contributes, and any disagreement that would change what you teach. Distinguish a source's claim from your recommendation. Ask the owner which sources and school of thought to adopt, qualify, or exclude.

Interview in short rounds. Ask the decisions that are ripe together, recommend a concrete answer to each, and wait. Use the answers to choose the next questions. Begin with who enters, what they already know, the starting materials, and what they should do independently at the exit. Then probe boundaries with contrasts: which neighboring skill stays outside the hour? Where could two competent practitioners disagree? What may the tutor assume or supply? If time runs short, what gets cut first? Bring a proposed example and a plausible counterexample so the owner can correct your reading.

Return a short author brief: entry and exit, scope and exclusions, sources and stance, accepted assumptions, trade-offs, key exercises, evidence required at each gate, and deferred questions. Ask the owner to accept or amend it. Earlier explicit decisions carry forward. A missing answer stays open. Pause course construction until the owner confirms the brief. This interview is with the author; a learner entering the finished course starts with the example.

## Verify the tutor's path before writing the course

Use the statechart skill on the agreed brief. Model each key exercise, what the tutor shows, who supplies the decision, and what evidence advances it. Include wrong answers, hints, worked answers, fresh attempts, pause/resume, and time running out. A worked answer cannot establish independence. Resuming must restore the outstanding decision. An early exit reports partial progress. Write these and the owner's exercise-specific gates as invariants. Use a bounded model, run TLC, inspect counterexamples and correct the flow before drafting. Check that the independent finish and partial exit are both reachable; a model that never finishes can satisfy a completion invariant vacuously.

Show the owner the checked chart, its gate meanings, remaining limits, and any course decision the check reopened. If the checker is unavailable, label the chart unverified and identify the missing dependency. Build from the confirmed brief and checked transitions. After drafting, replay a successful path and an assisted path against the actual tutor prompts and materials; model checking alone cannot verify lesson wording.

## Choose what the learner does

Finish this sentence first: “Given ___, the learner can ___.” Use a decision or action you can observe. Choose one outcome small enough to practice and check in a sitting. If the source is a long curriculum, select a slice that ends in a useful result. Keep the rest available for another sitting.

Work backward from a fresh example of that decision. List what the learner would have to do to answer it. Circle only the moves being taught. Supply everything else: the scenario, data, definitions, populated starter, command, or candidate choices. When selecting an idea *is* the skill, give realistic alternatives and ask the learner to choose or amend one. Let them substitute their own project if they already have one.

## Write the actual exchanges

- Open with an artifact and its evidence side by side. In a sentence, explain what the learner will be able to do. Start there without a general intake or vocabulary quiz.
- Work one example aloud, naming the detail that changes your decision. On a parallel example, leave one meaningful blank, offer a bounded choice, or ask for one edit. Ask one question and wait. Keep the evidence visible while they answer.
- Write the tutor's private answer key as the decision and the evidence that supports it. Accept equivalent wording or a defensible alternative. If the learner misses, point at the relevant line or field and let them try again. If they request the answer, explain it and give them a fresh case. Distinguish worked, hinted, and independent attempts.
- Give feedback about the exact move they made. Once they demonstrate it independently, advance or finish. The tutor handles navigation, commands, and file edits unless performing one is itself the lesson. Save the learner's own decision in the resulting artifact.

## Example of sizing a blank

Suppose the objective is to decide whether a delivery met a promised time. Supply the order, timestamps, time zone, and the rule that arrival **at or before** the deadline counts. Work one: “Due 14:00, arrived 14:03. Late by three minutes.”

Then show “Due 16:30 · arrived 16:30 · status ___ (on time / late).” Accept “on time.” If they say “late,” point to “at or before” and let them reconsider. For an independent check, show “Due 09:10 · arrived 09:11 · status ___.” Accept “late.” Carry their label into the delivery log. Time-zone conversion, inventing a shipping policy, and writing a parser would each introduce a separate lesson.

## Budget and check the course

Plan for at most about an hour, including reading, answering, feedback, and one retry. As a starting budget, allow 5 minutes to orient, 10 for a worked example, 20 for guided practice, 10 for a fresh attempt, 5 to finish, and 10 of slack. Shorter is welcome. Prepare inputs beforehand and provide a labeled saved output when a tool failure would consume the session. Keep optional extensions after the finish.

Before handing over the course, walk the ordinary path and a missed-answer path with the actual materials. For **every learner prompt and scored criterion**, identify which taught move it exercises and where the information needed to answer was shown. Fill in, demonstrate, or remove any unrelated demand. Check that the final example changes the facts, keeps the same underlying task, and still requires the learner's judgment. Label time estimates as estimates until someone has taken the course.

End with the learner's finished example and a brief account of what they did independently. On pause, keep their work, level of assistance, and exact pending question so the next session can continue there.
